# responsible to store DTOs (Data Transfer Object) between client
# and server and internal business logic.
from datetime import datetime
from pydantic import BaseModel


class LoginRequestDTO(BaseModel):
    username: str
    password: str


class LoginResponseDTO(BaseModel):
    access_token: str
    token_type: str


class RegisterRequestDTO(BaseModel):
    username: str
    email: str
    password: str


class RegisterResponseDTO(BaseModel):
    username: str


class TokenResponseDTO(BaseModel):
    access_token: str
    token_type: str


class TokenDataDTO(BaseModel):
    """JWT standard structure"""
    sub: str  # username
    session: str
    exp: datetime | None = None  # expiry of the token
