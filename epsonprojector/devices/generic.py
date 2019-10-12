from epsonprojector.devices.configurations.load import LoadConfiguration
from epsonprojector.interfaces.generic import GenericInterface


class GenericDevice:
    config_file = ""
    _conf = None

    def __init__(self, conn):
        if not isinstance(conn, GenericInterface):
            raise AttributeError("Invalid Interface")
        self._conn = conn

        if not self._conf:
            self.initialize_config()

    def __getattr__(self, item, *args, **kwargs):
        if item[-7:] != "_status":
            cmd = self._conf.find_command(item)
            def set_command(*args, **kwargs):
                parameter = self._conf.find_parameter(cmd["request_parameters"], args[0])
                print(parameter)
                return self.send(f"{cmd['command']} {parameter['parameter']}")
            return set_command

        else:
            cmd = self._conf.find_command(item[:-7])
            answer = self.send(f"{cmd['command']}?")

            return self._conf.find_parameter(cmd["response_parameters"], answer)


    def get_config_file(self):
        return self.config_file

    def initialize_config(self):
        self._conf = LoadConfiguration(self)

    def connect(self):
        pass

    def send(self, command):
        return "success"

    def read(self):
        pass
