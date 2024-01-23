# responsible for cover business logic, core functionality of the application.
# reusable, abstract from interface and focus on underlying business logic.
# might be dependent to controller according to use cases.
from __future__ import annotations
from datetime import datetime, timedelta
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from app.core.settings import Settings
from app.db import Session
from app.db.models.user_mgmt import Users
from app.helpers.exceptions import (
    credentials_exception,
    internal_exception,
    registration_exception,
    session_exist_exception,
    uname_pwd_exception
)
from app.helpers.logger import logger
from app.v1.auth.dao import SessionDAO, UserDAO
from app.v1.auth.dto import (
    LoginRequestDTO,
    LoginResponseDTO,
    RegisterRequestDTO,
    RegisterResponseDTO,
    TokenDataDTO
)


class AuthService:
    def __init__(self, session_service: SessionService, user_dao: UserDAO):
        self.oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")
        self.pwd_context = CryptContext(
            schemes=["argon2"], deprecated="auto"
        )
        self.session_service = session_service
        self.user_dao = user_dao

    def register_new_user(
        self,
        new_user: RegisterRequestDTO,
        db_sess: Session
    ) -> RegisterResponseDTO:
        """
        Register new user.

        Args:
            - new_user: user object coming from client.
            - db_sess: database session.

        Return:
            - user_obj: user object created from new_user param.
        """
        existing_user = (
            self.user_dao.get_user_by_username(
                new_user.username, db_sess
            )
        )
        if existing_user:
            raise registration_exception

        user_db = self.user_dao.create_new_user(new_user, db_sess)
        if not user_db:
            raise internal_exception

        return RegisterResponseDTO(id=user_db.id, username=user_db.name)

    def login_user(
        self, user: LoginRequestDTO, db_sess: Session
    ) -> LoginResponseDTO:
        user_db = self.authenticate_user(user, db_sess)
        if not user_db:
            raise uname_pwd_exception

        user_session = self.session_service.create_session(
            user.username, db_sess
        )
        if user_session is None:
            raise internal_exception
        if len(user_session) == 0:
            raise session_exist_exception

        token_data = TokenDataDTO(sub=user.username, session=user_session)
        access_token = self.create_access_token(data=token_data)
        return LoginResponseDTO(access_token=access_token, token_type="bearer")

    def create_access_token(
        self,
        data: TokenDataDTO,
        exp_delta: timedelta = timedelta(minutes=Settings.TOKEN_EXP_MINUTES)
    ) -> str:
        """
        Create JWT token.

        Args:
            - data: jwt information details
            - exp_delta: jwt expiry time limit

        Return:
            - encoded_jwt
        """
        expiry = datetime.utcnow() + exp_delta
        data.exp = expiry
        encoded_jwt = jwt.encode(
            claims=dict(data), key=Settings.SECRET_KEY, algorithm=Settings.ALGO
        )
        return encoded_jwt

    @staticmethod
    def verify_access_token(token: str) -> TokenDataDTO:
        """
        Parse access token detail.

        Args:
            - token: token from client

        Return:
            - token_data
        """
        payload = jwt.decode(
            token=token, key=Settings.SECRET_KEY, algorithms=Settings.ALGO
        )
        token_data = TokenDataDTO(**payload)
        if not (token_data.sub and token_data.session):
            raise credentials_exception
        return token_data

    def create_hash_password(self, password: str) -> str:
        """
        Create hash password.

        Args:
            - password: plain text password

        Return:
            - hash_password
        """
        return self.pwd_context.hash(password)

    def verify_password(self, plain_pass: str, hashed_pass: str) -> bool:
        """
        Verify inputted password is as similar with hashed password.

        Args:
            - plain_pass: password coming from client request
            - hashed_pass: password coming from database

        Return:
            - True or False
        """
        return self.pwd_context.verify(plain_pass, hashed_pass)

    def authenticate_user(
        self,
        user: LoginRequestDTO,
        db_sess: Session
    ) -> Optional[Users]:
        """
        Authenticate user by its credentials.

        Args:
            - username: username coming from client.
            - password: hashed password coming from client.
            - db_sess: database session.

        Return:
            - user: user object that fits to given username and password.
        """
        user_db = self.user_dao.get_user_by_username(user.username, db_sess)
        if not user_db:
            logger.debug(f"Wrong username ({user})")
            return None

        if not self.verify_password(user.password, str(user_db.pass_hash)):
            logger.debug(f"Wrong password ({user})")
            return None

        return user_db


class SessionService:
    def __init__(self, session_dao: SessionDAO):
        self.session_dao = session_dao

    def create_session(
        self, username: str, db_sess: Session
    ) -> str | None:
        """
        Create new session after login.

        Args:
            - user_id
            - token: containing session_token and expiry time,
                data is coming from AuthService

        Return:
            - session_id
        """
        active_session = self.session_dao.get_session_by_username(
            username=username, db_sess=db_sess
        )
        if active_session:
            logger.debug(f"{username} has an active session")
            return ""

        session = self.session_dao.create_new_session(username, db_sess)
        session_id = str(session.id) if session else None
        return session_id
