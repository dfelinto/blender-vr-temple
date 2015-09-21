"""
Timeline
********

Control the flux of the game, and the time related events (spawn of enemies, game end, game start, ...).
"""

from bge import (
        logic,
        )

from . import base
from time import time

TODO = True

class Base(base.Base):
    __slots__ = (
            "_animation",
            "_fps",
            "_frames_lap",
            "_frames_game",
            "_initial_time",
            "_initial_frame",
            "_lap",
            )

    def __init__(self, parent):
        base.Base.__init__(self, parent)

        self._setupMineKart()
        self._setupTime()

    def loop(self):
        self._updateTime()

    @property
    def lap_frames(self):
        return self._frames_lap

    @property
    def current_frame(self):
        return self._animation_proxy['frame']

    def _setupTime(self):
        self._fps = 25.0 * 10.0 * 0.25
        self._frames_lap = 15000 # roughly 1 minute (25 * 60)
        self._frames_game = self._frames_lap * 5
        self._lap = 0

        self._initial_time = time()
        self._initial_frame = self._getInitialFrame()

        self._updateTime()

    def _setupMineKart(self):
        """
        Dynamically set the Mine Kart parent (Proxy)
        (since it's linked, it can't be done previously)
        """
        scene = logic.getCurrentScene()

        proxy = scene.objects.get('Proxy')
        kart = scene.objects.get('Mine Kart')

        kart.worldPosition = proxy.worldPosition
        kart.worldOrientation = proxy.worldOrientation

        kart.setParent(proxy)
        self._animation_proxy = proxy

    def _getInitialFrame(self):
        """
        Randomly (seed based) pick an initial position on the lap
        """
        TODO
        return 0

    def _updateTime(self):
        current_time = time()
        delta_time = current_time - self._initial_time
        frame_game = self._initial_frame + self._fps * delta_time * self._parent.speed

        if frame_game > self._frames_game:
            self._parent.events.gameOver()

        frame_lap = frame_game % self._frames_lap
        lap = frame_game // self._frames_lap

        if lap > self._lap:
            self._lap += 1
            self._parent.events.startLap()

        self._animation_proxy['frame'] = frame_lap
        # self.logger.debug(int(lap), int(frame_lap), int(frame_game))


