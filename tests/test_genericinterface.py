import unittest
from unittest import mock

from epsonprojector.interfaces.generic import GenericInterface
from epsonprojector.exception import *

class GenericInterfaceTest(unittest.TestCase):

    # @mock.patch('epsonprojector.interfaces.generic.GenericInterface.has_device', return_value=True)

    def test_unknown_device(self):
        with self.assertRaises(UnknownDeviceError) as context:
            GenericInterface.new_device_connection("whatadevice")

    @mock.patch('epsonprojector.interfaces.generic.GenericInterface.has_connection', return_value=True)
    def test_existing_connection(self, mock):
        with self.assertRaises(ConnectionInUseError) as context:
            GenericInterface.new_device_connection("generic")


    def test_direct_init(self):
        with self.assertRaises(NotADeviceError) as context:
            GenericInterface("test")


if __name__ == '__main__':
    unittest.main()
