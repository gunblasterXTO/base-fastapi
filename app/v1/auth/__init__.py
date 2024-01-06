from fastapi import APIRouter

from .view import AuthViews

auth_views = AuthViews()
auth_r = APIRouter(prefix="/auth")

auth_r.add_api_route(path="/login", endpoint=auth_views.login, methods=["GET"])
