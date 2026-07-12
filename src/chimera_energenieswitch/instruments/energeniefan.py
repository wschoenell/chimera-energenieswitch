from chimera.interfaces.fan import Fan
from chimera_energenieswitch.instruments.energenieswitch import EnergenieSwitch


class EnergenieFan(Fan, EnergenieSwitch):
    def __init__(self):
        super(EnergenieSwitch, self).__init__()
