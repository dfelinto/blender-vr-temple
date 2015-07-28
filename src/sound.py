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

        self._setupSoundEngine()
        self._setupEnemies()

    def _setupSoundEngine(self):
        """
        """
        is_debug = self._parent.is_debug
        osc = not is_debug and \
              logic.BlenderVR.getPlugin('osc') if hasattr(logic, 'BlenderVR') else None

        if osc and osc.isAvailable():
            self._engine = OSCSoundEngine(osc)
        else:
            self._engine = AudaspaceSoundEngine()

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

    def setVolumeLow(self):
        """
        Low volume, flashlight is on
        """
        self._engine.setVolumeLow()

    def setVolumeNormal(self):
        """
        Normal volume, initial
        """
        self._engine.setVolumeNormal()

    def setVolumeHigh(self):
        """
        High volume, sonar is on
        """
        self._engine.setVolumeLow()


# ############################################################
# Sound Engines Wrappers
# ############################################################

class SoundEngine:
    def __init__(self, volumes):
        self._volumes = volumes

    def setVolumeLow(self):
        """
        Set the lowest volume level
        """
        self._volume = self._volumes[0]
        self._updateVolume()

    def setVolumeNormal(self):
        """
        Set the regular (initial) volume level
        """
        self._volume = self._volumes[1]
        self._updateVolume()

    def setVolumeHigh(self):
        """
        Set the highest volume level
        """
        self._volume = self._volumes[2]
        self._updateVolume()


class AudaspaceSoundEngine(SoundEngine):
    def __init__(self):
        SoundEngine.__init__(self, volumes=[0.15, 0.4, 0.85])
        self.setVolumeNormal()

    def _updateVolume(self):
        TODO


class OSCSoundEngine(SoundEngine):
    def __init__(self, osc):
        SoundEngine.__init__(self, volumes=[0.15, 0.4, 0.85])
        self._osc = osc
        self._initializeSound()

    def _initializeSound(self):
        """
        Define global OSC parameters
        """
        osc_global = self._osc.getGlobal()
        osc_global.start(True) # OSC msg: '/global start 1'
        osc_global.mute(False) # OSC msg: '/global mute 0'
        self.setVolumeNormal()

    def _updateVolume(self):
        """
        OSC message: /global volume %40
        """
        try:
            osc_global = self._osc.getGlobal()
            osc_global.volume("%{0}".format(int(self._volume * 100)))

        except Exception as E:
            print(E)


# ############################################################
# Sound Objects Wrappers
# ############################################################

class AudaspaceSoundObject:
    def __init__(self, kx_object):
        pass

    def play(self, sound, volume=0.5):
        """
        Load and play sound file

        sound type: str
        volume type: float (0.0 to 1.0)
        """
        TODO


class OSCSoundObject:
    def __init__(self, osc, kx_object):

        # because of the following line, the kx_object 4x4 orientation matrix will
        # 1) be sent to the OSC client
        # 2) be updated each time the kx_object moved
        self._osc_object = osc.getObject(kx_object)

    def play(self, sound, volume=0.5):
        """
        Load and play sound file

        sound type: str
        volume type: float (0.0 to 1.0)
        """
        self._sound_wrapper._load(sound)
        self._sound_wrapper._loop(True)
        self._sound_wrapper._mute(False)
        self._sound_wrapper._volume(volume)
        self._sound_wrapper._start(True)

    def _load(self, sound):
        """
        OSC message: /object 1 sound HiThere.wav

        sound type: str
        """
        self._osc_object.sound(sound)

    def _loop(self, value):
        """
        OSC message: /object 1 loop 1

        value type: bool
        """
        self._osc_object.loop(value)

    def _mute(self, value):
        """
        OSC message: /object 1 mute 0

        value type: bool
        """
        self._osc_object.mute(value)

    def _start(self, value):
        """
        OSC message: /object 1 start 1

        value type: bool
        """
        self._osc_object.start(value)

    def _volume(self, value):
        """
        OSC message: /object 1 volume %45

        value type: float (0.0 to 1.0)
        """
        self._osc_object.volume("%{0}".format(int(value * 100)))


# ############################################################
# Enemies Sound Classes
# ############################################################

class Enemy:
    osc = logic.BlenderVR.getPlugin('osc') if hasattr(logic, 'BlenderVR') else None
    audio_folder = logic.expandPath('//../audio/')

    def __init__(self, sound_source, sound_init, sound_end, force_fallback):
        if force_fallback or not self.osc:
            self._sound_wrapper = AudaspaceSoundObject(sound_source)
        else:
            self._sound_wrapper = OSCSoundObject(self.osc, sound_source)

        self._sound_init = sound_init
        self._sound_end = sound_end

    def play_init(self):
        """
        Play sound for when the object is active (e.g., flying)
        """
        self._sound_wrapper.play(self._sound_init)

    def play_end(self):
        """
        Play sound for when the object ends (e.g., is hit by rock)
        """
        self._sound_wrapper.play(self._sound_end)

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


