"""
Events Manager
**************

Centralize the communication between the game elements, the navigation devices, the input systems and the sound engine.
"""

from bge import (
        logic,
        )

from . import base

class Base(base.Base):
    def __init__(self, parent):
        base.Base.__init__(self, parent)

    def setFlashlightMode(self, power=True):
        """
        Activate or Deactivate the flashlight
        """
        self.logger.debug("setFlashlightMode({0})".format(power))
        logic.sendMessage("light")

        if power:
            self._parent.sound.setVolumeLow()

        else:
            self._parent.sound.setVolumeNormal()


    def setSonarMode(self, power=True):
        """
        Activate or Deactivate the sonar
        """
        self.logger.debug("setSonarMode({0})".format(power))
        logic.sendMessage("sonar")

        if power:
            self._parent.sound.setVolumeHigh()

        else:
            self._parent.sound.setVolumeNormal()

    def throwRock(self):
        """
        Throw a rock (to hit a pendulum)
        """
        self.logger.debug("throwRock()")
        logic.sendMessage("rock")


