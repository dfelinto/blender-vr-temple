"""
Debug
*****

This module is intended to run and debug the demo without BlenderVR
"""

from bge import (
        events,
        logic,
        render,
        )


LEFT_EYE = render.LEFT_EYE
ONEKEY = events.ONEKEY
TWOKEY = events.TWOKEY
THREEKEY = events.THREEKEY

from . import base


class Base(base.Base):
    def __init__(self, parent):
        base.Base.__init__(self, parent)

        print("Starting Debug Mode")
        scene = logic.getCurrentScene()
        scene.pre_draw_setup.append(self._preDrawSetup)
        self._keys = []

    def _preDrawSetup(self):
        stereo_eye = render.getStereoEye()

        if stereo_eye == LEFT_EYE:
            self.loop()

    def loop(self):
        """
        Run once per frame called from a callback
        """
        self._keyboard()
        self._parent.io.loop()
        self._parent.ai.loop()
        self._parent.sound.loop()

    def _keyboard(self):

        # little hack to make key state to work with python callbacks
        # otherwise we get state == 2 for all the pressed keys
        active_events = logic.keyboard.active_events
        active_keys = active_events.keys()

        if ONEKEY in active_keys and ONEKEY not in self._keys:
            self._parent.io.flashlightButton()

        if TWOKEY in active_keys and TWOKEY not in self._keys:
            self._parent.io.sonarButton()

        if THREEKEY in active_keys and THREEKEY not in self._keys:
            self._parent.io.rockButton()

        self._keys = set(active_keys)
