"""
Artificial Intelligence
***********************

Control the enemies behaviour (bats, ghosts, pendulum)
"""

"""
Short Term Task list:

* Initialize the Bat/Ghost objects
  (I may want a flat list of them btw, instead of a Bats() class)

* call the addObject actuator for every single of those objects, to keep tag of them
(instead of let this happening automatically)

* check for their states, and initialize their sound if they are in a valid state

* check for hitting, if position last long, triggers object death

* remember to store a unique property in each of the spawned objects to make them unique for messages
"""

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

        self._bats = Bats()
        self._ghosts = Ghosts()
        self._pendulum = Pendulums()

        self._initalizeEnemies()

    def _initializeEnemies(self):
        """
        * bge.logic.addObject ...
        store unique property in each to use the messenger system
        populate the self._* lists
        """
        TODO


    def loop(self):
        if self._parent.io.is_sonar or \
           self._parent.io.is_flashlight:
            ray_direction = self._parent.io.head_direction
            ray_position = self._parent.io.head_position

        if self._parent.io.is_sonar:
            self._bats.hit(ray_position, ray_direction)

        if self._parent.io.is_flashlight:
            self._ghosts.hit(ray_position, ray_direction)


class Enemies:
    __slots__ = (
            "ray_filter",
            )

    def __init__(self):
        self._ray_filter = ""

    def hit(origin, direction):
        """
        try to hit an enemy from this origin at this direction
        """
        TODO


class Bats(Enemies):
    def __init__(self):
        Enemies.__init__(self)

        self._ray_filter = "bat"
        self._bats = []


class Ghosts(Enemies):
    def __init__(self):
        Enemies.__init__(self)

        self._ray_filter = "ghost"
        self._ghosts = []


class Pendulum(Enemies):
    def __init__(self):
        Enemies.__init__(self)
