import unittest
from epsonprojector.interfaces.serial import SerialInterface
from epsonprojector.devices.epson import EpsonDevice
from epsonprojector.devices.generic import GenericDevice
from unittest import mock
from unittest.mock import MagicMock


class SerialinterfaceTestCase(unittest.TestCase):

    @mock.patch("serial.Serial")
    def test_new_device_connection(self, mocked):
        dev = SerialInterface.new_device_connection("epson_device")
        self.assertIsInstance(dev, GenericDevice)

    @mock.patch("serial.Serial")
    def test_create_new_interface(self, mocked):

        result = SerialInterface.create_new_connection("imadeviceobjectfortest", tty="testtty")
        self.assertEqual(SerialInterface.CONNECTIONS["testtty"], "imadeviceobjectfortest")
        self.assertEqual(result, True)

        result = SerialInterface.create_new_connection("imanotherdeviceobjectfortest", tty="testtty")
        self.assertEqual(SerialInterface.CONNECTIONS["testtty"], "imadeviceobjectfortest")
        self.assertEqual(result, False)

    def test_has_connection(self):
        SerialInterface.CONNECTIONS = {}
        self.assertEqual(SerialInterface.has_connection(tty="demotty"), False)

        SerialInterface.CONNECTIONS = {"demotty":"demodevice"}
        self.assertEqual(SerialInterface.has_connection(tty="demotty"), True)

    def test_generate_context(self):
        device = MagicMock()
        device.DEFAULT_TTY = "TestTTY"
        actx, kwctx = SerialInterface.generate_device_context(device)
        self.assertTupleEqual(actx, ())
        self.assertDictEqual(kwctx, {"tty":"TestTTY"})


if __name__ == '__main__':
    unittest.main()
