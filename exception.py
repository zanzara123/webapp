class UserNotFoundException(Exception):
    detail: str = "user not found"


class UserNotCorrectPasswordException(Exception):
    detail: str = "User not correct password"

class TokenExpireException(Exception):
    detail: str = "Token has expired"

class TokenNotCorrectException(Exception):
    detail: str = "token has not correct"