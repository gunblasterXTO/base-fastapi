# responsible for handling user input, updating the model,
# intermediary between view (FE - interface) and the business logic
from app.v1.auth.schema import LoginDTO


class AuthController:
    def get_user(self, user: LoginDTO) -> bool:
        return True
