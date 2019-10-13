import unittest
from epsonprojector.devices.configurations import load
from unittest import mock


def find_command_get_config():
    def wrapper(*args, **kwargs):
        return {"commands":
                    [
                        {
                            "command": "command_hello",
                            "name": "name_hello",
                            "find_parameter": [
                                {
                                    "parameter": "param_foo",
                                    "another_key": "another_value"
                                },
                                {
                                    "parameter": "same_parameter_name",
                                    "name": "same_parameter_name"
                                },

                                {
                                    "parameter": "param_test",
                                    "name": "name_foo"
                                }

                            ]
                        },
                        {
                            "command": "command_welt",
                            "name": "name_welt"
                        },
                        {
                            "command": "command_foo",
                            "name": "name_FOO",
                            "test_key": "TestValue"
                        },
                        {
                            "command": "command_bar",
                            "name": "NAME_BAR"
                        },
                    ]
                }
    return wrapper


class LoadConfigCase(unittest.TestCase):

    @mock.patch("epsonprojector.devices.configurations.load.LoadConfiguration.get_config", new_callable=find_command_get_config)
    @mock.patch("epsonprojector.devices.configurations.load.LoadConfiguration.__init__", return_value=None)
    def test_find_command(self, *args, **kwargs):
        lo = load.LoadConfiguration()

        com_foo = lo.find_command("command_foo")
        self.assertDictEqual(com_foo, {
                            "command": "command_foo",
                            "name": "name_FOO",
                            "test_key": "TestValue"
                        })

        nam_foo = lo.find_command("name_foo")
        self.assertDictEqual(nam_foo, {
                            "command": "command_foo",
                            "name": "name_FOO",
                            "test_key": "TestValue"
                        })

        self.assertEqual(lo.find_command("name_FOO")["command"], "command_foo")
        self.assertEqual(lo.find_command("not_exists"), None)

    @mock.patch("epsonprojector.devices.configurations.load.LoadConfiguration.__init__", return_value=None)
    def test_find_parameter(self, *args, **kwargs):
        lo = load.LoadConfiguration()

        full_list = lo.find_parameter(find_command_get_config()(), "commands")
        self.assertEqual(full_list, None)

        test_params = find_command_get_config()()["commands"][0]["find_parameter"]
        self.assertDictEqual(lo.find_parameter(test_params, "param_foo"), {
                                    "parameter": "param_foo",
                                    "another_key": "another_value"
                                })

        self.assertDictEqual(lo.find_parameter(test_params, "name_foo"), {
                                    "parameter": "param_test",
                                    "name": "name_foo"
                                })

        self.assertDictEqual(lo.find_parameter(test_params, "same_parameter_name"), {
                                    "parameter": "same_parameter_name",
                                    "name": "same_parameter_name"
                                })
        self.assertEqual(lo.find_parameter(test_params, "invalid_parameter"), None)

if __name__ == '__main__':
    unittest.main()
