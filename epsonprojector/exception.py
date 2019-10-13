class UnknownDeviceError(KeyError):
    pass


class ConnectionInUseError(ConnectionError):
    pass


class NotADeviceError(ReferenceError):
    pass

class UnknownResponse(ValueError):
    pass