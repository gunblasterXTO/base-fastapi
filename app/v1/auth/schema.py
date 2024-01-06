# responsible to validate data input and data output schema
from pydantic import BaseModel


class LoginDTO(BaseModel):
    username: str
    password: str
