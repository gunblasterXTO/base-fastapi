import time

from fastapi import Request, Response
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint
)

from app.core.constants import ExcludeAuthMiddlewarePath
from app.helpers.logger import logger
from app.middleware.logger import LogMiddleware
from app.middleware.security import SecurityMiddleware


log_middlware = LogMiddleware(logger=logger)
security_midleware = SecurityMiddleware()


class Middlewares(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """
        Main entry when call this class in fastapi.add_middleware.

        Args:
            - request: client request detail including url, json body, etc.
            - call_next: to call the endpoint/next process
        """
        start_time = time.time()
        await log_middlware.record_req(request=request)

        if (
            ExcludeAuthMiddlewarePath.REGISTER.value not in request.url.path
            or ExcludeAuthMiddlewarePath.LOGIN.value not in request.url.path
        ):
            auth_header = request.headers.get("Authorization", "")
            user_id, username, sess_id = security_midleware.authenticate_user(
                auth_header=auth_header
            )
            request.session_id = sess_id  # type: ignore
            request.username = username  # type: ignore
            request.user_id = user_id  # type: ignore

        response = await call_next(request)

        total_time = time.time() - start_time
        log_middlware.record_resp(response=response, time=total_time)

        return response
