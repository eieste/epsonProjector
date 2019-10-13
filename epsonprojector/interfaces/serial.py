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

    @staticmethod
    def new_device_connection(device_name="generic", tty="/dev/ttyUSB0"):
        if tty in SerialInterface.CONNECTIONS:
            raise ConnectionInUseError(f"a connection with tty {tty} is already in use. Please use get_device_connection method")

        if device_name in SerialInterface.DEVICES:
            serial_interface = SerialInterface(tty)
            dev_class = SerialInterface.DEVICES[device_name]
            dev_obj = dev_class(serial_interface)
            SerialInterface.CONNECTIONS[tty] = dev_obj
            return dev_obj
        else:
            raise UnknownDeviceError(f"Your {device_name} device is not a known device")

    @classmethod
    def create_new_connection(cls, device_object, *args, **kwargs):
        tty = kwargs.pop("tty")
        if not cls.has_connection(*args, **kwargs):
            cls.CONNECTIONS[tty] = device_object
            return True
        return False

    @classmethod
    def has_connection(cls, *args, **kwargs):
        tty = kwargs.pop("tty")
        if tty in SerialInterface.CONNECTIONS:
            return True
        return False

    def send_command(self, command):
        self._conn.write(f"{command}\r".encode("UTF-8"))
        line = self._conn.readline()
        return line
