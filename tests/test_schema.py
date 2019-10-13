import unittest
import jsonschema
import yaml

class TestSchema(unittest.TestCase):

    def setUp(self) -> None:
        with open("epsonprojector/devices/configurations/schema.yaml") as fobj:
            self._schema = yaml.load(fobj.read(), Loader=yaml.SafeLoader)

    def test_fail_no_content(self):
        try:
            jsonschema.validate(instance={}, schema=self._schema)
            self.assertFalse()
        except jsonschema.exceptions.ValidationError as inst:
            self.assertEqual(inst.message, "'commands' is a required property")


    def test_fail_wrong_content(self):
        try:
            jsonschema.validate(instance={"not_commands":{}}, schema=self._schema)
            self.assertFalse()
        except jsonschema.exceptions.ValidationError as inst:
            self.assertIn("Additional properties are not allowed", inst.message)

        try:
            jsonschema.validate(instance={"commands": {}}, schema=self._schema)
            self.assertFalse()
        except jsonschema.exceptions.ValidationError as inst:
            self.assertEqual("{} is not of type 'array'", inst.message)

    def test_commands_no_array(self):
        try:
            jsonschema.validate(instance={"commands":{}}, schema=self._schema)
            self.assertFalse()
        except jsonschema.exceptions.ValidationError as inst:
            self.assertEqual(inst.message, "{} is not of type 'array'")

    def test_commands_too_short(self):
        try:
            jsonschema.validate(instance={"commands": [] }, schema=self._schema)
            self.fail()
        except jsonschema.exceptions.ValidationError as inst:
            self.assertEqual(inst.message, "[] is too short")

    def test_invalid_command_object(self):
        cmd_obj = {}
        try:
            jsonschema.validate(instance={"commands": [cmd_obj]}, schema=self._schema)
            self.fail()
        except jsonschema.exceptions.ValidationError as inst:
            self.assertEqual(inst.message, "'command' is a required property")

        cmd_obj["command"] = "test_command"
        try:
            jsonschema.validate(instance={"commands": [cmd_obj]}, schema=self._schema)
            self.fail()
        except jsonschema.exceptions.ValidationError as inst:
            self.assertEqual(inst.message, "'request_parameters' is a required property")

        cmd_obj["request_parameters"] = {}
        try:
            jsonschema.validate(instance={"commands": [cmd_obj]}, schema=self._schema)
            self.fail()
        except jsonschema.exceptions.ValidationError as inst:
            self.assertEqual(inst.message, "'response_parameters' is a required property")

        cmd_obj["response_parameters"] = {}
        try:
            jsonschema.validate(instance={"commands": [cmd_obj]}, schema=self._schema)
            self.fail()
        except jsonschema.exceptions.ValidationError as inst:
            self.assertEqual(inst.message, "{} is not of type 'array'")



if __name__ == '__main__':
    unittest.main()
