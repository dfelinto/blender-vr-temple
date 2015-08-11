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
        sound,
        debug,
        )

class Temple:
    __slots__ = (
            "_is_debug",
            "ai",
            "debug",
            "events",
            "io",
            "logger",
            "sound",
            )

    def __init__(self):
        self.logger = logger.Base(self)

        self.events = events.Base(self)
        self._debug()

        self.io = io.Base(self)
        self.ai = ai.Base(self)
        self.sound = sound.Base(self)

    @property
    def is_debug(self):
        return self._is_debug

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
        self.sound.loop()


def main():
    logic.temple = Temple()
