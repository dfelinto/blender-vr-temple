"""
Input/Output
************

Takes the three different inputs, process the data and call the corresponding event.
It also handles head transformation/navigation.
"""

from . import base

class Base(base.Base):
    __slots__ = (
            "_flashlight_power",
            )

    def __init__(self, parent):
        base.Base.__init__(self, parent)

        # Flashlight
        self._flashlight_power = False

    def loop(self):
        pass

    def flashlightButton(self):
        """
        Flashlight was de/actived
        """
        self._flashlight_power = not self._flashlight_power
        self.setFlashlightMode(power = self._flashlight_power)
