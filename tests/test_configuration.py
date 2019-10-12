import unittest
from jsonschema import validate
from epsonprojector.settings import conf
import os
import yaml


class ConfigurationTestCase(unittest.TestCase):

    def test_all_configs(self):
        with open(os.path.join(conf.DEVICE_CONFIGURATIONS_PATH, "schema.yaml"), "r") as fobj:
            schema = yaml.load(fobj.read(), Loader=yaml.SafeLoader)

        for root, dirs, files in os.walk(conf.DEVICE_CONFIGURATIONS_PATH):
            for file in files:

                if file.endswith(".yaml") and not "schema.yaml" in file:

                    with open(os.path.join(conf.DEVICE_CONFIGURATIONS_PATH, file), "r") as fobj:
                        data = fobj.read()
                    validate(schema=schema, instance=yaml.load(data, Loader=yaml.SafeLoader))



if __name__ == '__main__':
    unittest.main()
