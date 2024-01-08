# responsible for cover business logic, core functionality of the application.
# reusable, abstract from interface and focus on underlying business logic.
# might be dependent to controller according to use cases.
from fastapi import HTTPException, status

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
        self, new_user: RegisterRequestDTO
    ) -> RegisterResponseDTO:
        existing_user = (
            self.user_controller.get_user_by_username(new_user.username)
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User is already registered"
            )
        user = self.user_controller.create_new_user(new_user)
        return user

    def authenticate_user(self, username: str, password: str) -> User:
        user = self.user_controller.get_user_by_username(username)
        if user and user.pwd == password:
            return user
        else:
            logger.error("Wrong username or password")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
