"""
Sound
*****

Connected with the game events systems it deals directly with the OSC server
"""

from . import base

class Base(base.Base):
    def __init__(self, parent):
        base.Base.__init__(self, parent)

    def loop(self):
        pass
