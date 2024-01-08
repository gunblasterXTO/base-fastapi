import time

from fastapi import Request, Response
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint
)

from app.helpers.logger import logger
from app.middleware.logger import LogMiddleware


log_middlware = LogMiddleware(logger=logger)


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

        response = await call_next(request)

        total_time = time.time() - start_time
        log_middlware.record_resp(response=response, time=total_time)

        return response
