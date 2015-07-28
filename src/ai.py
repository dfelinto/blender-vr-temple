"""
Artificial Intelligence
***********************

Control the enemies behaviour (bats, ghosts, pendulum)
"""

"""
Short Term Task list:

* check for their states, and initialize their sound if they are in a valid state

* check for hitting, if position last long, triggers object death

* remember to store a unique property in each of the spawned objects to make them unique for messages
"""

from bge import (
        logic,
        )

from . import base

TODO = True

class Base(base.Base):
    __slots__ = (
            "_bats",
            "_ghosts",
            "_pendulums",
            )

    def __init__(self, parent):
        base.Base.__init__(self, parent)

        self._bats = []
        self._ghosts = []
        self._pendulums = []

        self._initializeEnemies()

    def _initializeEnemies(self):
        """
        * bge.logic.addObject ...
        store unique property in each to use the messenger system
        populate the self._* lists
        """
        scene = logic.getCurrentScene()
        objects = scene.objects

        enemies = {'bat', 'ghost', 'pendulum'}

        for obj in objects:
            enemy = obj.get('enemy')

            if enemy not in enemies:
                continue

            if enemy == 'bat':
                self._bats.append(Bat(scene, obj))

            elif enemy == 'ghost':
                self._ghosts.append(Ghost(scene, obj))

            else: # 'pendulum'
                self._pendulums.append(Pendulum(scene, obj))

    def loop(self):
        if self._parent.io.is_sonar or \
           self._parent.io.is_flashlight:
            ray_direction = self._parent.io.head_direction
            ray_position = self._parent.io.head_position

        if self._parent.io.is_sonar:
            self._bats.hit(ray_position, ray_direction)

        if self._parent.io.is_flashlight:
            self._ghosts.hit(ray_position, ray_direction)


class Enemy:
    def __init__(self):
        self._ray_filter = ""

    def hit(origin, direction):
        """
        try to hit an enemy from this origin at this direction
        """
        TODO

    def addObject(self, scene, object_name, object_origin):
        """
        Spawn a new object in the game
        """
        return scene.addObject(object_name, object_origin)


class Bat(Enemy):
    def __init__(self, scene, obj):
        Enemy.__init__(self)

        self._ray_filter = 'bat'
        self._dupli_object = self.addObject(scene, 'Bat', obj)


class Ghost(Enemy):
    def __init__(self, scene, obj):
        Enemy.__init__(self)

        self._ray_filter = 'ghost'
        self._dupli_object = self.addObject(scene, 'Ghost', obj)


class Pendulum(Enemy):
    def __init__(self, scene, obj):
        Enemy.__init__(self)
        self._dupli_object = obj
