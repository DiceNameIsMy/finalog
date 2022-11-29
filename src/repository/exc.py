from dataclasses import dataclass


class RepositoryException(Exception):
    pass


class DoesNotExist(RepositoryException):
    pass


@dataclass
class InvalidData(RepositoryException):
    detail: str
    code: str
