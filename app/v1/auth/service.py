# responsible for cover business logic, core functionality of the application.
# reusable, abstract from interface and focus on underlying business logic.
# might be dependent to controller according to use cases.
from app.db import Session
from app.helpers.exceptions import (
    internal_exception,
    registration_exception,
    uname_pwd_exception
)
from app.helpers.logger import logger
from app.v1.auth.dao import UserDAO
from app.v1.auth.dto import (
    LoginRequestDTO,
    LoginResponseDTO,
    RegisterRequestDTO,
    RegisterResponseDTO
)


class AuthService:
    def __init__(self, user_dao: UserDAO):
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

    def authenticate_user(
        self,
        user: LoginRequestDTO,
        db_sess: Session
    ) -> LoginResponseDTO:
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
            logger.error(f"Wrong username/password ({user})")
            raise uname_pwd_exception

        return LoginResponseDTO(username=user_db.name)
