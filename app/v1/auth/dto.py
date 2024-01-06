# responsible to store DTOs (Data Transfer Object) between client
# and server and internal business logic.
from pydantic import BaseModel


class LoginRequestDTO(BaseModel):
    username: str
    password: str


class RegisterRequestDTO(BaseModel):
    username: str
    email: str
    password: str
    country_origin: str


class RegisterResponseDTO(BaseModel):
    user_id: int
    username: str


class User(BaseModel):
    user_id: int
    username: str
    pwd: str
