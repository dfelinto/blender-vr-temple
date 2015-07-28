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
        """
        print("setFlashlightMode({0})".format(power))
        logic.sendMessage("light")

    def setSonarMode(self, power=True):
        """
        """
        print("setSonarMode({0})".format(power))
        logic.sendMessage("sonar")
        TODO

        if power:
            self._parent.sound.increaseVolume()

        else:
            self._parent.sound.decreaseVolume()

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
        """
        print("throwRock()")
        logic.sendMessage("rock")
