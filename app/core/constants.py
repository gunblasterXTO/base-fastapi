from enum import Enum


class ResponseStatusMsg(Enum):
    SUCCESS = "Success"
    FAIL = "Fail"


class ResponseMsg(Enum):
    INTERNAL_ERROR = "Internal server error"
    BAD_REQUEST = "Bad request"
    NOT_FOUND = "Data not found"
