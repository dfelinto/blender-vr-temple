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
            "_sonar_power",
            )

    def __init__(self, parent):
        base.Base.__init__(self, parent)

        # Flashlight
        self._flashlight_power = False

        # Sonar
        self._sonar_power = False

    def loop(self):
        pass

    def flashlightButton(self):
        """
        Flashlight was de/actived
        """
        self._flashlight_power = not self._flashlight_power
        self.setFlashlightMode(power = self._flashlight_power)

    def sonarButton(self):
        """
        Sonar button was pressed
        """
        self._sonar_power = not self._sonar_power
        self.setSonarMode(power = self._sonar_power)
