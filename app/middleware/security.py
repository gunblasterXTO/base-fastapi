from typing import Tuple, Optional

from fastapi import Depends

from app.db import db, Session
from app.db.models.user_mgmt import Sessions
from app.helpers.exceptions import credentials_exception
from app.helpers.logger import logger
from app.v1.auth.service import AuthService, SessionService
from app.v1.auth.dao import SessionDAO, UserDAO
from app.v1.auth.dto import TokenDataDTO


class SecurityMiddleware:
    def __init__(
        self,
        auth_service: AuthService = AuthService(
            session_service=SessionService(SessionDAO()),
            user_dao=UserDAO()
        ),
        db_sess: Session = Depends(db.get_session)
    ):
        self.auth_service = auth_service
        self.db_sess = db_sess

    def authenticate_user(
        self, auth_header: Optional[str]
    ) -> Tuple[str, str, str]:
        """
        Ensure user is a valid user that has access to other backend services.

        Args:
            - auth_header: Auhtorization header from client request

        Return:
            - sub_id: user hash id
            - sub: username
        """
        if not auth_header:
            logger.debug("No authorization header provided")
            raise credentials_exception

        token = auth_header.replace("Bearer ", "")
        token_detail = self.check_jwt_token(token)
        _ = self.check_session(token_detail)

        return token_detail.sub_id, token_detail.sub, token_detail.session

    def check_jwt_token(self, token: str) -> TokenDataDTO:
        """
        Parse JWT token from client request.

        Args:
            - token

        Return:
            - token_detail
        """
        return self.auth_service.verify_token(token=token)

    def check_session(self, token: TokenDataDTO) -> Sessions:
        """
        Ensure session is exist and active.

        Args:
            - token

        Return:
            - Sessions
        """
        return (
            self.auth_service
            .validate_session(token=token, db_sess=self.db_sess)
        )
