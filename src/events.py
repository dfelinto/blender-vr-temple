"""
Events Manager
**************

Centralize the communication between the game elements, the navigation devices, the input systems and the sound engine.
"""

from . import base

class Base(base.Base):
    def __init__(self, parent):
        base.Base.__init__(self, parent)

    def loop(self):
        pass

    def setFlashlightMode(power=True):
        """
        """
        print("setFlashlightMode({0})".format(power))
