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
        Flashlight button was pressed
        """
        self._flashlight_power = not self._flashlight_power
        self.setFlashlightMode(power = self._flashlight_power)

        """
        * rotate the flashlight based on user position orientation (CAVE and OCULUS)
        * also should make the ghost react, and if it stays long in the same ghost, kills the ghost
        * mute the sound (or make a lound flashlight sound)
        """

    def sonarButton(self):
        """
        Sonar button was pressed
        """
        self._sonar_power = not self._sonar_power
        self.setSonarMode(power = self._sonar_power)

        """
        * screen get blurry
        * volume gets higher
        * if pointing to a bat for long, bat goes away
        """

    def rockButton(self):
        """
        Rock button was pressed
        """
        self.throwRock()

        """
        * should be thrown relative to your current orientation
        * if it hits a bat, make it faster
        """
