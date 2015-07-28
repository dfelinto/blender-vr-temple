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
            "sound",
            )

    def __init__(self):
        self.events = events.Base(self)

        self._debug()
        self._setup()

        self.io = io.Base(self)
        self.ai = ai.Base(self)
        self.sound = sound.Base(self)

    @property
    def is_debug(self):
        return self._is_debug

    def _debug(self):
        """
        if BlenderVR is not running hookup the debug module
        """
        self._is_debug = not hasattr(logic, 'BlenderVR')

        if not self._is_debug:
            return

        self.debug = debug.Base(self)

    def _setup(self):
        """
        setup required settings and bge related events
        """
        pass
        # store global objects

    def run(self):
        """
        run once per frame, called from the processor file
        """
        self.io.loop()
        self.sound.loop()


def main():
    import bge
    bge.logic.temple = Temple()
