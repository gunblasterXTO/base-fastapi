# responsible to handle HTTP request and produces correspond response
from fastapi import status
from fastapi.responses import JSONResponse

from app.helpers.response import PostSuccessResponse
from app.v1.auth.controller import AuthController
from app.v1.auth.schema import LoginDTO

auth_controller = AuthController()


class AuthViews:
    async def login(self, user: LoginDTO) -> JSONResponse:
        _ = auth_controller.get_user(user)
        return JSONResponse(
            content=PostSuccessResponse(data=[{}]).model_dump(),
            status_code=status.HTTP_200_OK
        )
