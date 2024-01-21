# responsible for handling user input, business flow,
# intermediary between view and the business logic (service).
# stateless, handle particular request and not retain state between request.
from typing import Optional

from app.db import Session
from app.db.models.user_mgmt import Users
from app.helpers.logger import logger
from app.v1.auth.dto import RegisterRequestDTO


class UserDAO:
    def __init__(self):
        pass

    @staticmethod
    def get_user_by_username(
        username: str, db_sess: Session
    ) -> Optional[Users]:
        """
        Get user data from username.

        Args:
            - username: user's username from client request
            - db_sess: database session dependency

        Return:
            - user_obj: user object if any
        """
        user = db_sess.query(
            Users.id, Users.name
        ).filter(
            Users.name == username
        ).first()
        return user

    @staticmethod
    def create_new_user(
        new_user: RegisterRequestDTO, db_sess: Session
    ) -> Optional[Users]:
        """
        Create new user record.

        Args:
            - new_user:  user detail from client request
            - db_sess: database session dependency

        Return:
            - user_obj: newly created user record containing necessary detail
        """
        new_user_dict = {
            "name": new_user.username,
            "email": new_user.email,
            "pass_hash": f"{new_user.password}notreallyhash",
            "pass_salt": f"{new_user.password}notreallysalt"
        }
        new_user_obj = Users(**new_user_dict)
        db_sess.add(new_user_obj)

        try:
            db_sess.commit()
            user_obj = new_user_obj
        except Exception as err:
            db_sess.rollback()
            logger.error(f"Fail to add user {new_user}: {err}")
            user_obj = None

        return user_obj
