"""
Timeline
********

Control the flux of the game, and the time related events (spawn of enemies, game end, game start, ...).
"""

from bge import (
        logic,
        )

from . import base

TODO = True

class Base(base.Base):
    def __init__(self, parent):
        base.Base.__init__(self, parent)

        self._setupMineKart()

    def _setupMineKart(self):
        """
        Dynamically set the Mine Kart parent (Proxy)
        (since it's linked, it can't be done previously)
        """
        scene = logic.getCurrentScene()

        proxy = scene.objects.get('Proxy')
        kart = scene.objects.get('Mine Kart')

        kart.setParent(proxy)


