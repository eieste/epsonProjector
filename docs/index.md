# Projector Commands

with this Libary you can control your rs232 capable projector device.
its also possible to extend this libary with your own commands.


example:
```python

from epsonprojector.interfaces import SerialInterface 


device = SerialInterface.get_device_connection("TW5200", tty="/dev/ttyUSB0")

device.power_on())

```