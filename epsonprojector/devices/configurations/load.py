from cerberus import Validator
import yaml
import os
from epsonprojector.settings import conf
from jsonschema import validate


class LoadConfiguration:

    _SCHEMA = None

    def __init__(self, device):
        self._device = device

        if self._SCHEMA is None:
            # Load Schema
            with open(os.path.join(conf.DEVICE_CONFIGURATIONS_PATH, "schema.yaml"), "r") as fobj:
                self._SCHEMA = yaml.load(fobj.read(), Loader=yaml.SafeLoader)

        self.autload_config()


    def autload_config(self):
        with open(os.path.join(conf.DEVICE_CONFIGURATIONS_PATH, self._device.get_config_file()), "r") as fobj:
            config = yaml.load(fobj.read(), Loader=yaml.SafeLoader)
            validate(instance=config, schema=self._SCHEMA)
            self._data = config

    def find_command(self, command):
        print(self._data)
        for item in self._data["commands"]:
            if item["command"] == command or item["name"] == command:
                return item

    def find_parameter(self, command_item, parameter):
        for item in command_item:
            print(item)
            if item["parameter"] == parameter or item["name"] == parameter:
                return item