import unittest
from unittest import mock
from epsonprojector.devices.epson import EpsonDevice


class EpsondeviceTestCase(unittest.TestCase):

    def test_build_command(self):
        ser = mock.MagicMock()
        dev = EpsonDevice(ser)

        result = dev.build_command({"command": "CMD"}, {"parameter": "PARM"})
        self.assertEqual(result, "CMD PARM")

        result = dev.build_command({"command":"CMD"}, status=True)
        self.assertEqual(result, "CMD?")

    def test_parse_command(self):
        ser = mock.MagicMock()
        dev = EpsonDevice(ser)

        result = dev.parse_command(b"KEY=VALUE")
        self.assertEqual(result.command, "KEY")
        self.assertEqual(result.parameter, "VALUE")
        self.assertEqual(result.status, True)

        result = dev.parse_command(b"KEY=0A")
        self.assertEqual(result.command, "KEY")
        self.assertEqual(result.parameter, "0A")
        self.assertEqual(result.status, True)

        result = dev.parse_command(b"KEY=VALUE:")
        self.assertEqual(result.command, "KEY")
        self.assertEqual(result.parameter, "VALUE")
        self.assertEqual(result.status, True)

        result = dev.parse_command(b"KEY=VALUE:\r")
        self.assertEqual(result.command, "KEY")
        self.assertEqual(result.parameter, "VALUE")
        self.assertEqual(result.status, True)

        result = dev.parse_command(b"ERR")
        self.assertEqual(result.command, None)
        self.assertEqual(result.parameter, None)
        self.assertEqual(result.status, False)

        result = dev.parse_command(b"PWR=00")
        self.assertEqual(result.command, "PWR")
        self.assertEqual(result.parameter, "00")
        self.assertEqual(result.status, True)

        result = dev.parse_command(b"IRGENDETWAS")
        self.assertEqual(result.command, None)
        self.assertEqual(result.parameter, None)
        self.assertEqual(result.status, None)


    def test_getattr(self):

        ser = mock.MagicMock()
        dev = EpsonDevice(ser)

        def find_command():
            def wrapper(*args, **kwargs):
                return {"command": "test", "name": "testmethod", "request_parameters":[{"name":"testparam","parameter":"abc"}], "response_parameters":[]}
            return wrapper

        with mock.patch("epsonprojector.devices.configurations.load.LoadConfiguration.find_command", new_callable=find_command) as mock_obj:
            dev.testmethod("abc")

        with mock.patch("epsonprojector.devices.configurations.load.LoadConfiguration.find_command", new_callable=find_command) as mock_obj:
            dev.testmethod_status()

if __name__ == '__main__':
    unittest.main()
