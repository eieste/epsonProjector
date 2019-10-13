from epsonprojector.devices import EpsonDevice, EpsonTW5200Device
from epsonprojector.exception import UnknownDeviceError, ConnectionInUseError
from epsonprojector.interfaces.generic import GenericInterface
import serial


class SerialInterface(GenericInterface):

    DEVICES = {
        "epson_device": EpsonDevice,
        "tw5200": EpsonTW5200Device
    }

    CONNECTIONS = {
    }

    def __init__(self, tty):
        self._tty = tty
        self._conn = serial.Serial(self._tty, 9600, timeout=5)

    @classmethod
    def create_new_connection(cls, device_object, *args, **kwargs):
        tty = kwargs["tty"]
        if not cls.has_connection(*args, **kwargs):
            cls.CONNECTIONS[tty] = device_object
            return True
        return False

    @classmethod
    def has_connection(cls, *args, **kwargs):
        tty = kwargs["tty"]
        if tty in SerialInterface.CONNECTIONS:
            return True
        return False

    def send_command(self, command):
        self._conn.write(f"{command}\r".encode("UTF-8"))
        line = self._conn.readline()
        return line

    @classmethod
    def generate_device_context(cls, device_class, *args, **kwargs):
        kwargs["tty"] = device_class.DEFAULT_TTY
        return args, kwargs