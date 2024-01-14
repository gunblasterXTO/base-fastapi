# responsible for cover business logic, core functionality of the application.
# reusable, abstract from interface and focus on underlying business logic.
# might be dependent to controller according to use cases.
from fastapi import HTTPException, status

from app.db import Session
from app.helpers.logger import logger
from app.v1.auth.controller import UserController
from app.v1.auth.dto import (
    RegisterRequestDTO,
    RegisterResponseDTO,
    User
)


class AuthService:
    def __init__(self, user_controller: UserController):
        self.user_controller = user_controller

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
            - user: user object created from new_user param.
        """
        existing_user = (
            self.user_controller.get_user_by_username(
                new_user.username, db_sess
            )
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User is already registered"
            )
        user = self.user_controller.create_new_user(new_user, db_sess)
        return user

    def authenticate_user(
        self,
        username: str,
        password: str,
        db_sess: Session
    ) -> User:
        """
        Authenticate user by its credentials.

        Args:
            - username: username coming from client.
            - password: hashed password coming from client.
            - db_sess: database session.

        Return:
            - user: user object that fits to given username and password.
        """
        user = self.user_controller.get_user_by_username(username, db_sess)
        if user and user.pwd == password:
            return user
        else:
            logger.error("Wrong username or password")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
