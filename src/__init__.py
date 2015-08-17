"""
Blender-VR Temple Source
************************
"""

from bge import (
        logic,
        )

from . import (
        ai,
        events,
        io,
        logger,
        score,
        sound,
        debug,
        )

TODO = True

class Temple:
    __slots__ = (
            "_is_debug",
            "_speed",
            "ai",
            "debug",
            "events",
            "io",
            "logger",
            "score",
            "sound",
            )

    def __init__(self):
        # initialize them before so they don't clash recursion upon Base inheritance
        self.events = None
        self.logger = None

        self._speed = 1.0

        self.logger = logger.Base(self)
        self.events = events.Base(self)

        self._debug()

        self.io = io.Base(self)
        self.ai = ai.Base(self)
        self.score = score.Base(self)
        self.sound = sound.Base(self)

    @property
    def is_debug(self):
        return self._is_debug

    @property
    def speed(self):
        return self._speed

    def bumpSpeed(self):
        """
        Increase global speed
        """
        self._speed *= 1.5

        TODO

        """
        change base speed of kart animation
        """

    def _debug(self):
        """
        If BlenderVR is not running hookup the debug module
        """
        self._is_debug = not hasattr(logic, 'BlenderVR')

        if not self._is_debug:
            return

        self.debug = debug.Base(self)

    def run(self):
        """
        Run once per frame, called from the processor file
        """
        self.io.loop()
        self.ai.loop()
        self.score.loop()
        self.sound.loop()


def main():
    logic.temple = Temple()
