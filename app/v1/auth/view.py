# responsible to handle HTTP request and produces correspond response
from fastapi import status
from fastapi.responses import JSONResponse

from app.helpers.logger import logger
from app.helpers.response import PostSuccessResponse
from app.v1.auth.controller import UserController
from app.v1.auth.dto import LoginRequestDTO, RegisterRequestDTO
from app.v1.auth.service import AuthService

user_controller = UserController()
auth_service = AuthService(user_controller)


class AuthViews:
    async def registration(self, user: RegisterRequestDTO) -> JSONResponse:
        new_user = auth_service.register_new_user(user).model_dump()
        return JSONResponse(
            content=PostSuccessResponse(data=new_user).model_dump(),
            status_code=status.HTTP_201_CREATED
        )

    async def login(self, user: LoginRequestDTO) -> JSONResponse:
        logger.debug("User loggin in")
        _ = auth_service.authenticate_user(
            username=user.username, password=user.password
        )
        return JSONResponse(
            content=PostSuccessResponse(data=[{}]).model_dump(),
            status_code=status.HTTP_200_OK
        )
