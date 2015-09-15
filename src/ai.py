"""
Artificial Intelligence
***********************

Control the enemies behaviour (bats, ghosts, pendulum)
"""
from bge import (
        logic,
        types,
        )

import os

TODO = True

from . import base

class Base(base.Base):
    __slots__ = (
            "_bats",
            "_ghosts",
            "_pendulums",
            "_target",
            "_trail_seeker",
            )

    def __init__(self, parent):
        base.Base.__init__(self, parent)

        self._bats = []
        self._ghosts = []
        self._pendulums = []

        self._trail_seeker = None
        self._initializeEnemies()
        self._initializeTrailSeeker()

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
        logger = self.logger
        events = self.events
        speed = self._parent.speed

        for obj in objects:
            enemy = obj.get('enemy')

            if enemy not in enemies:
                continue

            if enemy == 'bat':
                self._bats.append(Bat(scene, obj, self._target, speed, events, logger))

            elif enemy == 'ghost':
                self._ghosts.append(Ghost(scene, obj, self._target, speed, events, logger))

            else: # 'pendulum'
                self._pendulums.append(Pendulum(scene, obj, speed, events, logger))

    def loop(self):
        ray_position = self._parent.io.head_position

        if self._parent.io.is_sonar or \
           self._parent.io.is_flashlight:
            ray_direction = self._parent.io.head_direction

        if self._parent.io.is_sonar:
            Bat.hit(self._target, ray_position, ray_direction)

        if self._parent.io.is_flashlight:
            Ghost.hit(self._target, ray_position, ray_direction)

        for bat in self._bats:
            bat.attack(ray_position)

        for ghost in self._ghosts:
            ghost.attack(ray_position)

        for pendulum in self._pendulums:
            pendulum.evade(ray_position)

    def spawnEnemies(self):
        """
        populate enemies
        """
        TODO

        """
        randomly get those numbers
        dont forget to get the offset based on current frame
        """

        for frame in 10, 500, 1000:
            self._trail_seeker.getPosition(
                    frame,
                    self._spawnEnemies,
                    {'frame':frame},
                    )

        for frame in 20, 600, 1300:
            self._trail_seeker.getOrientation(
                    frame,
                    self._spawnEnemies,
                    {'frame':frame},
                    )

        for frame in 30, 680, 1400:
            self._trail_seeker.getTransform(
                    frame,
                    self._spawnEnemies,
                    {'frame':frame},
                    )

    def _spawnEnemies(self, value, user_data):
        """
        actually populate enemies
        """
        TODO

        frame = user_data['frame']
        print(frame, value)

    def trailSeek(self):
        """
        see if we are to be activated
        """
        self._trail_seeker.loop()

    def trailSeeker(self, ob, controller, actuator):
        """
        Store the object we use to evaluate
        the trail for enemy spawning
        """
        self._trail_seeker = Seeker(ob, controller, actuator)

    def _initializeTrailSeeker(self):
        """
        """
        scene = logic.getCurrentScene()
        objects = scene.objects

        ob = objects.get('Seeker')
        cont = ob.controllers.get('controller')
        act = cont.actuators.get('actuator')

        self.trailSeeker(ob, cont, act)


class Seeker:
    def __init__(self, ob, controller, actuator):
        self._ob = ob
        self._controller = controller
        self._actuator = actuator
        self._activate = False
        self._stack = []

    def _changeFrame(self, frame):
        self._ob['frame'] = frame
        self._controller.activate(self._actuator)

    def _getPosition(self, frame):
        self._changeFrame(frame)
        return self._ob.worldPosition

    def getPosition(self, frame, callback, user_data=None):
        """
        Get position of the animation at a given frame

        :param frame: animation frame
        :type frame: int
        :param callback: callback function
        :type callback: function(mathutils.Vector, user_data)
        :param user_data: user data passed back to callback function
        :type user_data: Object
        """
        self._stack.insert(0, (self._getPosition, frame, callback, user_data))

    def _getOrientation(self, frame):
        self._changeFrame(frame)
        return self._ob.worldOrientation

    def getOrientation(self, frame, callback, user_data=None):
        """
        Get orientation matrix of the animation at a given frame

        :param frame: animation frame
        :type frame: int
        :param callback: callback function
        :type callback: function(mathutils.Matrix, user_data)
        :param user_data: user data passed back to callback function
        :type user_data: Object
        """
        self._stack.insert(0, (self._getOrientation, frame, callback, user_data))

    def _getTransform(self, frame):
        self._changeFrame(frame)
        return (self._ob.worldPosition, self._ob.worldOrientation)

    def getTransform(self, frame, callback, user_data=None):
        """
        Get position and orientation matrix of the animation at a given frame

        :param frame: animation frame
        :type frame: int
        :param callback: callback function
        :type callback: function(((mathutils.Vector, mathutils.Matrix), user_data)
        :param user_data: user data passed back to callback function
        :type user_data: Object
        """
        self._stack.insert(0, (self._getTransform, frame, callback, user_data))

    def loop(self):
        """
        activate the actuator to return any stacked query
        """
        if self._stack:
            func, frame, callback, user_data = self._stack.pop()
            value = func(frame)
            callback(value, user_data)


# ############################################################
# Enemy Classes
# ############################################################

class Enemy:
    ray_filter = ''
    instances = 0
    attack_distance_squared = 0.01
    evade_distance_squared = 100.0

    def __init__(self, speed, events, logger):
        self._dupli_object = None
        self._sound = None
        self._active = False
        self._speed = speed
        self._state_init = Enemy.getState(3)
        self._state_end = Enemy.getState(6)
        self._id = self.__class__.calculateId()
        self.logger = logger
        self.events = events
        self.evade_distance_squared

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
        if obj and obj.ai._active:
            obj.ai.events.hitEnemy(obj.ai)

    def kill(self):
        """
        Send message to eliminate the object
        It is called when we hit the enemy or the enemy hits us
        """
        if not self._active:
            return

        self._active = False
        logic.sendMessage(self.subject)
        self.logger.debug('kill', self._dupli_object.name)

    def addObject(self, scene, object_name, object_origin):
        """
        Spawn a new object in the game

        :type object_origin: mathutils.Vector
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
        self.events.spawnEnemy(self)

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

    def attack(self, origin):
        """
        Check if enemy is close enough to eat

        :type origin: mathutils.Vector
        """
        if not self._active:
            return

        obj = self._dupli_object
        distance_squared = (obj.worldPosition - origin).length_squared

        if distance_squared < self.attack_distance_squared:
            self.events.hitByEnemy(self)

        elif distance_squared > self.evade_distance_squared:
            self.events.evadeEnemy(self)

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

        # setup the logic bricks
        self._setupLogicBricks()

    def _setupLogicBricks(self):
        sensors = self._dupli_object.sensors

        # messenger sensor used to end the object
        hermes = sensors.get('hermes')
        hermes.subject = self.subject

        # near sensor used to detect the proximity with the player
        near = sensors.get('Near')
        near.distance *= self._speed

        self.evade_distance_squared = pow(near.distance * 2.0, 2)


class FlyingEnemy(Enemy):
    def __init__(self, name, scene, obj, target, speed, events, logger):
        super(FlyingEnemy, self).__init__(speed, events, logger)
        self._target = target

        self._setDupliObject(self.addObject(scene, name, obj))

        # our own _setupLogicBricks()
        actuators = self._dupli_object.actuators
        sensors = self._dupli_object.sensors

        # adjust the chase velocity based on the scene speed
        brain = actuators.get('brain')
        brain.target = target
        brain.velocity *= speed
        brain.turnspeed *= speed
        brain.acceleration *= speed


class Bat(FlyingEnemy):
    enemy = 'BAT'
    ray_filter = 'bat'

    def __init__(self, scene, obj, target, speed, events, logger):
        super(Bat, self).__init__('Bat', scene, obj, target, speed, events, logger)


class Ghost(FlyingEnemy):
    enemy = 'GHOST'
    ray_filter = 'ghost'
    attack_distance_squared = 0.25
    activation_distance = 30.0

    def __init__(self, scene, obj, target, speed, events, logger):
        super(Ghost, self).__init__('Ghost', scene, obj, target, speed, events, logger)


class Pendulum(Enemy):
    enemy = 'PENDULUM'
    ray_filter = 'pendulum'

    def __init__(self, scene, obj, speed, events, logger):
        super(Pendulum, self).__init__(speed, events, logger)

        group = self.addObject(scene, 'Pendulum.Group', obj)
        self._setDupliObject(group.groupMembers.get('Pendulum.Sphere'))

    def attack(self):
        """
        Called from Logic Brick callback
        We are already hitting the player
        """
        if not self._active:
            return

        self.events.hitByEnemy(self)

    def evade(self, origin):
        """
        Check if enemy is too far
        """
        if not self._active:
            return

        obj = self._dupli_object
        distance_squared = (obj.worldPosition - origin).length_squared

        if distance_squared > self.evade_distance_squared:
            self.events.evadeEnemy(self)

    def end(self):
        """
        End the object, called from Logic Bricks
        """
        super(Pendulum, self).end()
        self.events.hitEnemy(self)


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


def attacked(cont):
    """
    Called from Logic Bricks upon collision with enemy

    Only pendulum collides this way, the other objects
    Use the steering actuator which is incompatible with
    physics sensors
    """
    sensor = cont.sensors[0]
    for obj in sensor.hitObjectList:
        obj.ai.attack()


def trailSeeking(cont):
    """
    activate trail seeking actuator
    """
    logic.temple.ai.trailSeek()


