import os

import yaml
from jsonschema import validate

from epsonprojector.settings import conf


class LoadConfiguration:

    _schema = None

    def __init__(self, device):
        self._device = device

        if self._schema is None:
            # Load Schema
                self._schema = self._read_schema()

        self._data = self.autload_config()

    def get_config(self):
        return self._data

    def _get_schema(self):
        return self._schema

    def _read_schema(self):
        schema = {}
        with open(os.path.join(conf.DEVICE_CONFIGURATIONS_PATH, "schema.yaml"), "r") as fobj:
            schema = yaml.load(fobj.read(), Loader=yaml.SafeLoader)
        return schema

    def _read_config(self):
        config = {}
        with open(os.path.join(conf.DEVICE_CONFIGURATIONS_PATH, self._device.get_config_file()), "r") as fobj:
            config = yaml.load(fobj.read(), Loader=yaml.SafeLoader)
        return config

    def autload_config(self):
        data = self._read_config()
        validate(instance=data, schema=self._get_schema())
        return data

    def find_command(self, command):
        for item in self.get_config()["commands"]:
            if "command" in item:
                if item["command"].lower() == command.lower():
                    return item
            if "name" in item:
                if item["name"].lower() == command.lower():
                    return item

    def find_parameter(self, command_item, parameter):
        for item in command_item:
            if "parameter" in item:
                if item["parameter"].lower() == parameter.lower():
                    return item

            if "name" in item:
                if item["name"].lower() == parameter.lower():
                    return item