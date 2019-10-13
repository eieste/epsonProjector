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


    @mock.patch('epsonprojector.interfaces.generic.GenericInterface.has_connection', return_value=False)
    @mock.patch('epsonprojector.interfaces.generic.GenericInterface.create_new_connection', return_value=False)
    def test_same_device(self, *args):
        generic = GenericInterface.new_device_connection("epson_device")

    def test_generate_context(self):
        ainfo, kwinfo = GenericInterface.generate_device_context("device_class","a","b","c", d="e")
        self.assertTupleEqual(ainfo, ("a","b","c"))
        self.assertDictEqual(kwinfo, {"d":"e"})

if __name__ == '__main__':
    unittest.main()
