# responsible for handling user input, business flow,
# intermediary between view and the business logic (service).
# stateless, handle particular request and not retain state between request.
from app.v1.auth.dto import (
    RegisterRequestDTO,
    RegisterResponseDTO,
    User
)


class UserController:
    def __init__(self):
        pass

    def get_user_by_id(self, user_id: int) -> User:
        # in actual case might have database query here
        return User(user_id=user_id, username="gunblasterXTO", pwd="")

    def get_user_by_username(self, username: str) -> User:
        return User(user_id=1, username=username, pwd="")

    def create_new_user(
        self, new_user: RegisterRequestDTO
    ) -> RegisterResponseDTO:
        return RegisterResponseDTO(user_id=2, username=new_user.username)
