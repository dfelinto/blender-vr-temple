"""
Artificial Intelligence
***********************

Control the enemies behaviour (bats, ghosts, pendulum)
"""

"""
Short Term Task list:

* check for hitting, if position last long, triggers object death

* remember to store a unique property in each of the spawned objects to make them unique for messages
"""

from bge import (
        logic,
        types,
        )

import os

from . import base

TODO = True

class Base(base.Base):
    __slots__ = (
            "_bats",
            "_ghosts",
            "_pendulums",
            "_target",
            )

    def __init__(self, parent):
        base.Base.__init__(self, parent)

        self._bats = []
        self._ghosts = []
        self._pendulums = []

        self._initializeEnemies()

    @property
    def bats(self):
        return self._bats

    @property
    def ghosts(self):
        return self._ghosts

    @property
    def pendulums(self):
        return self._pendulums

    def _initializeEnemies(self):
        """
        * bge.logic.addObject ...
        store unique property in each to use the messenger system
        populate the self._* lists
        """
        scene = logic.getCurrentScene()
        objects = scene.objects

        enemies = {'bat', 'ghost', 'pendulum'}
        self._target = scene.active_camera

        for obj in objects:
            enemy = obj.get('enemy')

            if enemy not in enemies:
                continue

            if enemy == 'bat':
                self._bats.append(Bat(scene, obj, self._target))

            elif enemy == 'ghost':
                self._ghosts.append(Ghost(scene, obj, self._target))

            else: # 'pendulum'
                self._pendulums.append(Pendulum(obj))

    def loop(self):
        if self._parent.io.is_sonar or \
           self._parent.io.is_flashlight:
            ray_position = self._parent.io.head_position
            ray_direction = self._parent.io.head_direction

        if self._parent.io.is_sonar:
            Bat.hit(self._target, ray_position, ray_direction)

        if self._parent.io.is_flashlight:
            Ghost.hit(self._target, ray_position, ray_direction)


# ############################################################
# Enemy Classes
# ############################################################

class Enemy:
    ray_filter = ''
    instances = 0

    def __init__(self):
        self._dupli_object = None
        self._sound = None
        self._active = False
        self._state_init = Enemy.getState(3)
        self._state_end = Enemy.getState(6)
        self._id = self.__class__.calculateId()

    @staticmethod
    def getState(state):
        """
        Return the bitwise flag corresponding to this state
        """
        return 1 << (state - 1)

    @property
    def sound_source(self):
        """
        Return the object to use as reference for the sound origin
        """
        return self._dupli_object

    @property
    def subject(self):
        """
        Message subject to use with the Message sensor to end the object
        """
        return "{0}.die.{1}".format(self.ray_filter, self._id)

    @classmethod
    def calculateId(cls):
        """
        Generates a new id based on the number of added instances
        """
        cls.instances += 1
        return cls.instances

    @classmethod
    def hit(cls, camera, origin, direction):
        """
        Try to hit an enemy from this origin at this direction
        If succeds, send a message to end the object

        :type origin: mathutils.Vector
        :type direction: mathutils.Quaternion
        """
        obj, hit, normal = camera.rayCast(origin + direction, origin, 20.0, cls.ray_filter, 1, 1)
        if obj:
            logic.sendMessage(obj.ai.subject)
            print('sending message: ', obj.ai.subject)

    def addObject(self, scene, object_name, object_origin):
        """
        Spawn a new object in the game
        """
        return scene.addObject(object_name, object_origin)

    def setSound(self, sound):
        """
        Setup OSC sound engine, called from sound.py
        """
        self._sound = sound

    def init(self):
        """
        Initialize the object, called from Logic Bricks
        """
        self._active = True
        self._sound.playInit()

    def end(self):
        """
        End the object, called from Logic Bricks
        """
        self._sound.playEnd()

    def changeState(self):
        """
        Called when the object changes to a relevant state, called from Logic Bricks
        """
        state = self._dupli_object.state

        if state & self._state_init:
            self.init()

        elif state & self._state_end:
            self.end()

    def _setDupliObject(self, obj):
        """
        Setup the duplicated object to integrate with our Python code
        """
        bge_wrappers = {
                types.KX_GameObject : KX_EnemyGameObject,
                types.BL_ArmatureObject : BL_EnemyArmatureObject,
                }

        bge_class = obj.__class__
        assert(bge_class in bge_wrappers)

        # replace the BGE object class with our own
        self._dupli_object = bge_wrappers[bge_class](obj, self)


class Bat(Enemy):
    ray_filter = 'bat'

    def __init__(self, scene, obj, target):
        super(Bat, self).__init__()

        self._setDupliObject(self.addObject(scene, 'Bat', obj))

        brain = self._dupli_object.actuators.get('brain')
        brain.target = target

        hermes = self._dupli_object.sensors.get('hermes')
        hermes.subject = self.subject


class Ghost(Enemy):
    ray_filter = 'ghost'

    def __init__(self, scene, obj, target):
        super(Ghost, self).__init__()

        self._ray_filter = 'ghost'
        self._setDupliObject(self.addObject(scene, 'Ghost', obj))

        brain = self._dupli_object.actuators.get('brain')
        brain.target = target

        hermes = self._dupli_object.sensors.get('hermes')
        hermes.subject = self.subject


class Pendulum(Enemy):
    def __init__(self, obj):
        super(Pendulum, self).__init__()
        self._setDupliObject(obj)


# ############################################################
# Custom KX_GameObject Wrapper
# ############################################################

class KX_EnemyGameObject(types.KX_GameObject):
    def __init__(self, old_object, ai_class):
        self.ai = ai_class

# Hack for BlenderVR syncronization to recognize this class
KX_EnemyGameObject.__name__ = 'KX_GameObject'


class BL_EnemyArmatureObject(types.BL_ArmatureObject):
    def __init__(self, old_object, ai_class):
        self.ai = ai_class

# Hack for BlenderVR syncronization to recognize this class
BL_EnemyArmatureObject.__name__ = 'BL_ArmatureObject'


# ############################################################
# Callback from Logic Bricks
# ############################################################

def changeState(cont):
    """
    Called from Logic Bricks upon change to relevant states
    (e.g., start chasing, or end object)
    """
    enemy = cont.owner
    enemy.ai.changeState()


