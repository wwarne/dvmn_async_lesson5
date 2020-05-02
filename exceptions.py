from typing import Optional


class MinechatException(Exception):
    def __init__(self, title: str, message: Optional[str] = '') -> None:
        self.title = title
        self.message = message
        super().__init__(message)


class InvalidToken(MinechatException):
    pass


class UnknownError(MinechatException):
    pass
