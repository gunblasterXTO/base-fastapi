# responsible to handle HTTP request and produces correspond response
from fastapi import Depends, status
from fastapi.responses import JSONResponse

from app.db import db, Session
from app.helpers.logger import logger
from app.helpers.response import PostSuccessResponse
from app.v1.auth.dao import UserDAO
from app.v1.auth.dto import LoginRequestDTO, RegisterRequestDTO
from app.v1.auth.service import AuthService

auth_service = AuthService(UserDAO())


class AuthViews:
    async def registration(
        self,
        user: RegisterRequestDTO,
        db_sess: Session = Depends(db.get_session)
    ) -> JSONResponse:
        """
        Register new user if related information haven't been in the db.
        """
        logger.debug("Registering new user...")
        new_user = auth_service.register_new_user(user, db_sess).model_dump()
        return JSONResponse(
            content=PostSuccessResponse(data=new_user).model_dump(),
            status_code=status.HTTP_201_CREATED
        )

    async def login(
        self,
        user: LoginRequestDTO,
        db_sess: Session = Depends(db.get_session)
    ) -> JSONResponse:
        """
        Login user if the related information is correct.
        """
        logger.debug("Logging in user...")
        user_db = auth_service.authenticate_user(user, db_sess).model_dump()
        return JSONResponse(
            content=PostSuccessResponse(data=user_db).model_dump(),
            status_code=status.HTTP_200_OK
        )
