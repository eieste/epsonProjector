from epsonprojector.devices.generic import GenericDevice
import re
from epsonprojector.devices.generic import ParsedResponse

response_re = re.compile(r'(?P<cmd>\w+)\=(?P<param>\w*)\s?')


class EpsonDevice(GenericDevice):
    config_file = "epson.yaml"

    def __getattr__(self, item):
        """
            Overwrites GenericDevice __getattr_ method to implement _status methods
            :param item: Name of called method
            :return method: Return a wrapper method
        """
        if item[-7:] != "_status":
            return super(EpsonDevice, self).__getattr__(item)
        else:
            def status_command(*args, **kwargs):
                cmd = self._conf.find_command(item[:-7])
                command = self.build_command(cmd, status=True)
                if command is False:
                    raise ValueError("Cant build command")
                answer = self.send(command)
                a = cmd["response_parameters"]
                if answer.status:
                    aw = self._conf.find_parameter(a, answer.parameter)
                    return aw
                return "WTF?"
            return status_command

    def build_command(self, command, parameter=None, status=False, *args, **kwargs):

        if status is False and not parameter is None:
            return f"{command['command']} {parameter['parameter']}"
        elif status is True and parameter is None:
            return f"{command['command']}?"
        return False

    def parse_command(self, answer, *args, **kwargs):
        aw = answer.decode("UTF-8")

        if "err" in aw:
            return ParsedResponse(None, None, False)

        if ":" == aw:
            return ParsedResponse(None, None, True)

        try:
            match = response_re.match(aw)
            return ParsedResponse(match.group("cmd"), match.group("param"), True)
        except Exception as e:
            return ParsedResponse(None, None, None)