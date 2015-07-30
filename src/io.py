"""
Input/Output
************

Takes the three different inputs, process the data and call the corresponding event.
It also handles head transformation/navigation.
"""

from mathutils import Vector
from . import base

TODO = True

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

    @property
    def is_sonar(self):
        return self._sonar_power

    @property
    def is_flashlight(self):
        return self._flashlight_power

    @property
    def head_direction(self):
        TODO
        return Vector()

    @property
    def head_position(self):
        TODO
        return Vector()

    def flashlightButton(self):
        """
        Flashlight button was pressed
        """
        if self._sonar_power and not self._flashlight_power:
            # we can do only one action at time
            return

        self._flashlight_power = not self._flashlight_power
        self.setFlashlightMode(power = self._flashlight_power)

        """
        * rotate the flashlight based on user position orientation (CAVE and OCULUS)
        * also should make the ghost react, and if it stays long in the same ghost, kills the ghost
        """

    def sonarButton(self):
        """
        Sonar button was pressed
        """
        if self._flashlight_power and not self._sonar_power:
            # we can do only one action at time
            return

        self._sonar_power = not self._sonar_power
        self.setSonarMode(power = self._sonar_power)

    def rockButton(self):
        """
        Rock button was pressed
        """
        self.throwRock()

        """
        * should be thrown relative to your current orientation
        * if it hits a bat, make it faster
        """
