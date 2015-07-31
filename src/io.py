"""
Input/Output
************

Takes the three different inputs, process the data and call the corresponding event.
It also handles head transformation/navigation.
"""

from bge import (
        logic,
        )

from mathutils import Vector
from . import base

TODO = True

class Base(base.Base):
    __slots__ = (
            "_camera",
            "_direction_object",
            "_flashlight_power",
            "_matrix"
            "_sonar_power",
            "_use_headtrack",
            "_headtrack_user",
            )

    def __init__(self, parent):
        base.Base.__init__(self, parent)

        scene = logic.getCurrentScene()
        objects = scene.objects

        # Flashlight
        self._flashlight_power = False

        # Sonar
        self._sonar_power = False

        # Head Tracking is disabled unless enabled from BlenderVRg
        self._use_headtrack = False

        # Flashlight and Rock thrower
        self._direction_object = objects.get('Spot')

        if not self._direction_object:
            raise Exception('"Spot" object not found in the scene')

        self._camera = objects.get('Camera', scene.active_camera)

        # Matrix is set once per frame
        self._resetMatrix()

    def loop(self):
        self._resetMatrix()
        self._updateDirection()

    @property
    def is_sonar(self):
        return self._sonar_power

    @property
    def is_flashlight(self):
        return self._flashlight_power

    @property
    def head_direction(self):
        """
        Get the direction of the player's head

        :rtype: mathutils.Vector (normalized)
        """
        ray_orientation = self.head_orientation
        direction = ray_orientation * Vector((0.0, 0.0, -1.0))

        return direction.normalized()

    @property
    def head_orientation(self):
        """
        Get the direction of the player's head

        :rtype: mathutils.Quaternion
        """
        matrix = self._getHeadMatrix()
        return matrix.to_quaternion()

    @property
    def head_position(self):
        """
        Get the direction of the player's head

        :rtype: mathutils.Vector
        """
        matrix = self._getHeadMatrix()
        return matrix.translation

    def _resetMatrix(self):
        self._matrix = None

    def enableHeadTrack(self, user):
        """
        Use Headtrack (instead of mouse) to control the scene
        Called from BlenderVR processor file

        :param user: BlenderVR User
        """
        self._headtrack_user = user
        self._use_headtrack = True

    def _getHeadMatrix(self):
        """
        :rtype: mathutils.Matrix
        """
        if self._matrix:
            return self._matrix

        if self._use_headtrack:
            TODO
            """
            UNTESTED, 150% likely to be wrong, though the idea is that
            """
            self._matrix = self._headtrack_user.getPosition() * \
                    self._headtrack_user.getVehiclePosition() * \
                    self._camera.worldTransform
        else:
            self._matrix = self._camera.worldTransform

        return self._matrix

    def _updateDirection(self):
        """
        Rotate the flashlight and the rock thrower according to the
        current head orientation
        """
        position = self.head_position
        orientation = self.head_orientation

        self._direction_object.worldOrientation = orientation
        self._direction_object.worldPosition = position

    def flashlightButton(self):
        """
        Flashlight button was pressed
        """
        if self._sonar_power and not self._flashlight_power:
            # we can do only one action at time
            return

        self._flashlight_power = not self._flashlight_power
        self._parent.events.setFlashlightMode(power=self._flashlight_power)

        """
        * also should make the ghost react, and if it stays long in the same ghost, kills the ghost
        """

    def sonarButton(self):
        """
        Sonar button was pressed
        """
        if self._flashlight_power and not self._sonar_power:
            # we can do only one action at time
            return

        self._sonar_power = not self._sonar_power
        self._parent.events.setSonarMode(power=self._sonar_power)

    def rockButton(self):
        """
        Rock button was pressed
        """
        self._parent.events.throwRock()

        """
        * if it hits a bat, make it faster
        """
