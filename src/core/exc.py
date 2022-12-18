class DomainException(Exception):
    pass


class DoesNotExist(DomainException):
    pass


class InvalidData(DomainException):
    pass
