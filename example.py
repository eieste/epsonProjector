from epsonprojector.interfaces.serial import SerialInterface



dev = SerialInterface.new_device_connection("tw5200")

dev.pwr("on")