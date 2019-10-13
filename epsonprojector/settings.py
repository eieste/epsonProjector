import os


class Settings:

    #: Path to Device Configration YAMLs
    DEVICE_CONFIGURATIONS_PATH = os.path.join(os.getcwd(), "epsonprojector", "devices/configurations")


conf = Settings()
