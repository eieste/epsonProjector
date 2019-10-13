from epsonprojector.devices.configurations.load import LoadConfiguration
# from epsonprojector.interfaces.generic import GenericInterface
from collections import namedtuple

ParsedResponse = namedtuple("ParsedResponse", ("command", "parameter", "status"))


class GenericDevice:
    config_file = ""
    _conf = None

    def __init__(self, conn):
        # ToDo check if conn inherith from Generic Interface
        # if not isinstance(conn, epsonprojector.interfaces.GenericInterface):
        #    raise AttributeError("Invalid Interface")
        self._conn = conn

        # Load Config if not done yet
        if not self._conf:
            self.initialize_config()

    def __getattr__(self, item):
        """
            Intercept all method calls to implement them on projector commands

            :param item: Name of called method
            :return method: Return a wrapper method
        """
        # Try to find command in config
        cmd = self._conf.find_command(item)

        # Wrapper Command
        def set_command(*args, **kwargs):
            # Try to find Parameters from wrapper called args in Command
            parameter = self._conf.find_parameter(cmd["request_parameters"], args[0])
            # Create a projector command based on previously collected information
            command = self.build_command(cmd, parameter)
            if command is False:
                raise ValueError("Cant build command")
            # Transmit Projector Command
            answer = self.send(command)
            return answer

        return set_command

    def build_command(self, command, parameter):
        """
            Creates a command from Command and Parameter object

            :param command: dict of command information from config
            :param parameter: dict of parameter informations from config
            :return any: Command to send via Interface
        """
        raise NotImplementedError("Please implement this method")

    def parse_command(self, command, parameter, *args, **kwargs):
        """
            Try to parse responses from Projector

            :param answer: Data that returned from projector
            :return ParsedResponse: Tuple with the parsed Information
        """
        raise NotImplementedError("Please implement this method")

    def get_config_file(self):
        """
            Get path to configfile

            :return path: String path to configfile
        """
        return self.config_file

    def initialize_config(self):
        """
            Initialize Config Loading
        """
        self._conf = LoadConfiguration(self)

    def connect(self):
        # ToDo I dont know
        pass

    def send(self, command):
        """
            Send command via Initialized Interface

            :param command: Projector Command
            :return: Parsed Projector answer
        """
        answer = self._conn.send_command(command)
        response = self.parse_command(answer)
        return response

    def read(self):
        # ToDo I dont know
        pass
