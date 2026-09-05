class UserNotFoundException(Exception):
    detail: str = "user not found"


class UserNotCorrectPasswordException(Exception):
    detail: str = "User not correct password"