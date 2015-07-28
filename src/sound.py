"""
Sound
*****

Connected with the game events systems it deals directly with the OSC server
It also provides a phantom layer, which mimics OSC with local BGE sound resources.
"""

from bge import (
        logic,
        )

from . import base

TODO = True

class Base(base.Base):
    def __init__(self, parent):
        base.Base.__init__(self, parent)
        self._setupEnemies()

    def _setupEnemies(self):
        """
        """
        is_debug = self._parent.is_debug

        for bat in self._parent.ai.bats:
            bat.setSound(Bat(bat.sound_source, force_fallback=is_debug))

        for ghost in self._parent.ai.ghosts:
            ghost.setSound(Ghost(ghost.sound_source, force_fallback=is_debug))

        for pendulum in self._parent.ai.pendulums:
            pendulum.setSound(Pendulum(pendulum.sound_source, force_fallback=is_debug))

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

class BlenderSoundObject:
    def __init__(self, kx_object):
        pass

    def load(self, sound):
        TODO

    def loop(self, value):
        TODO

    def mute(self, value):
        TODO

    def start(self, value):
        TODO

    def volume(self, value):
        TODO


class OSCSoundObject:
    def __init__(self, osc, kx_object):

        # because of the following line, the kx_object 4x4 orientation matrix will
        # 1) be sent to the OSC client
        # 2) be updated each time the kx_object moved
        self._osc_object = osc.getObject(kx_object)

    def load(self, sound):
        """
        OSC message: /object 1 sound HiThere.wav

        value type: str
        """
        self._osc_object.sound(sound)

    def loop(self, value):
        """
        OSC message: /object 1 loop 1

        value type: bool
        """
        self._osc_object.loop(value)

    def mute(self, value):
        """
        OSC message: /object 1 mute 0

        value type: bool
        """
        self._osc_object.mute(value)

    def start(self, value):
        """
        OSC message: /object 1 start 1

        value type: bool
        """
        self._osc_object.start(value)

    def volume(self, value):
        """
        OSC message: /object 1 volume %45

        value type: float (0.0 to 1.0)
        """
        self._osc_object.volume("%{0}".format(int(value * 100)))


class Enemy:
    osc = logic.BlenderVR.getPlugin('osc') if hasattr(logic, 'BlenderVR') else None
    audio_folder = logic.expandPath('//../audio/')

    def __init__(self, sound_source, sound_init, sound_end, force_fallback):
        if force_fallback or not self.osc:
            self._sound_wrapper = BlenderSoundObject(sound_source)
        else:
            self._sound_wrapper = OSCSoundObject(self.osc, sound_source)

        self._sound_init = sound_init
        self._sound_end = sound_end

    def play_init(self):
        """
        Play sound for when the object is active (e.g., flying)
        """
        self._sound_wrapper.load(self._sound_init)
        self._sound_wrapper.loop(True)
        self._sound_wrapper.mute(False)
        self._sound_wrapper.volume(0.45)
        self._sound_wrapper.start(True)

    def play_end(self):
        """
        Play sound for when the object ends (e.g., is hit by rock)
        """
        self._sound_wrapper.load(self._sound_end)
        self._sound_wrapper.loop(True)
        self._sound_wrapper.mute(False)
        self._sound_wrapper.volume(0.45)
        self._sound_wrapper.start(True)

    @property
    def sound_init(self):
        return os.path.join(self._audio_folder, self._sound_init)

    @property
    def sound_end(self):
        return os.path.join(self._audio_folder, self._sound_end)


class Bat(Enemy):
    sound_init = "bat.m4a"
    sound_end = "bat_end.m4a"

    def __init__(self, sound_source, force_fallback=False):
        Enemy.__init__(self, sound_source, self.sound_init, self.sound_end, force_fallback)


class Ghost(Enemy):
    sound_init = "ghost.m4a"
    sound_end = "ghost_end.m4a"

    def __init__(self, sound_source, force_fallback=False):
        Enemy.__init__(self, sound_source, self.sound_init, self.sound_end, force_fallback)


class Pendulum(Enemy):
    sound_init = "pendulum.m4a"
    sound_end = "pendulum_end.m4a"

    def __init__(self, sound_source, force_fallback=False):
        Enemy.__init__(self, sound_source, self.sound_init, self.sound_end, force_fallback)


