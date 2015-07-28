"""
Events Manager
**************

Centralize the communication between the game elements, the navigation devices, the input systems and the sound engine.
"""

from bge import (
        logic,
        )

from . import base

TODO = True

class Base(base.Base):
    def __init__(self, parent):
        base.Base.__init__(self, parent)

    def setFlashlightMode(self, power=True):
        """
        Activate or Deactivate the flashlight
        """
        print("setFlashlightMode({0})".format(power))
        logic.sendMessage("light")

        if power:
            self._parent.sound.setVolumeLow()

        else:
            self._parent.sound.setVolumeNormal()


    def setSonarMode(self, power=True):
        """
        Activate or Deactivate the sonar
        """
        print("setSonarMode({0})".format(power))
        logic.sendMessage("sonar")
        TODO

        if power:
            self._parent.sound.setVolumeHigh()

        else:
            self._parent.sound.setVolumeNormal()

        """
        if power = True:
            * volume gets higher
            * screen get blurry
            * if pointing to a bat for long, bat goes away (handled in ai.py)

        else:
            * volume gets lower
            * screen back to normal
        """

    def throwRock(self):
        """
        Throw a rock (to hit a pendulum)
        """
        print("throwRock()")
        logic.sendMessage("rock")
