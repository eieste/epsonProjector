from epsonprojector.devices import GenericDevice, EpsonDevice
from epsonprojector.exception import UnknownDeviceError, ConnectionInUseError


class GenericInterface(object):

    DEVICES = {
        "generic": GenericDevice,
        "epson_device": EpsonDevice,
    }

    CONNECTIONS = {}

    @classmethod
    def new_device_connection(cls, device_name="generic", *args, **kwargs):
        """
            Create a new Connection to the given device

            :param device_name: name of available device (All devices can be found in each Interface in Interface.DEVICES
            :param tty: name of serial interface
            :return obj: Specific Device object. (origin object of GenericDevice)
        """
        if not cls.has_device(device_name):
            raise UnknownDeviceError(f"Your {device_name} device is not a known device")

        dev_class = cls.DEVICES[device_name]
        actx, kwctx = cls.generate_device_context(dev_class, *args, **kwargs)

        if cls.has_connection(*actx, **kwctx):
            raise ConnectionInUseError(f"A connection with the given Parameters is already in use. Please use get_device_connection method")

        serial_interface = cls(*actx, **kwctx)

        dev_obj = dev_class(serial_interface)
        cls.create_new_connection(dev_obj, *actx, **kwctx)

        return dev_obj

    @classmethod
    def generate_device_context(cls, device_class, *args, **kwargs):
        """
            Generate Context for Device initializeation
            context descripes args/kwargs

            :param args:
            :param kwargs:
            :param device_class: Class of Device that consumes tthis context

            :return tuple: tuple of args, kwargs
        """
        return (args, kwargs)

    @classmethod
    def has_device(cls, device_name):
        """
            Checks if device exists in current interface

            :param device_name: name of device
            :return:
        """
        if device_name.lower() in [ dev.lower() for dev in GenericInterface.DEVICES]:
            return True
        return False

    @classmethod
    def create_new_connection(cls, device_object, *args, **kwargs):
        """
            Add the given connection to global index, to prevent multiple connections to the same device

            :param device_object: Device object
            :param args: Possible args to generate connection identification
            :param kwargs: Possible kwargs to generate connection identification
            :return bool: True if connection sucessfully added (false if connection with the same identifyer already exists)
        """
        raise NotImplementedError("Please implement this method in your device class")


    @classmethod
    def has_connection(cls, *args, **kwargs):
        """
            Check if connection with identifier already exists

            :param args: Possible args to generate a identifier
            :param kwargs: Possible kwargs to generate a identifier
            :return:
        """
        raise NotImplementedError("Please implement this method in your interface class")

    def send_command(self, *args, **kwargs):
        """
            FooBar

            :param args:
            :param kwargs:
            :return:
        """
        raise NotImplementedError("please implement this method in your interface class")