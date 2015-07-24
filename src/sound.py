"""
Sound
*****

Connected with the game events systems it deals directly with the OSC server
It also provides a phantom layer, which mimics OSC with local BGE sound resources.
"""

from . import base

class Base(base.Base):
    def __init__(self, parent):
        base.Base.__init__(self, parent)

    def loop(self):
        pass

    def increaseVolume(self):
        """
        """
        pass

    def decreaseVolume(self):
        """
        """
        pass

    """
    * bat
        - mp3
        - position
        - ...

    * starts
    """
