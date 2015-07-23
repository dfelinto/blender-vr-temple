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

    def loop(self):
        pass

    def setFlashlightMode(power=True):
        """
        """
        print("setFlashlightMode({0})".format(power))
        logic.sendMessage("light")

    def setSonarMode(power=True):
        """
        """
        print("setSonarMode({0})".format(power))
        logic.sendMessage("sonar")
        TODO

    def throwRock():
        """
        """
        print("throwRock()")
        logic.sendMessage("rock")
