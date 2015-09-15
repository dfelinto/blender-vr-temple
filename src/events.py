"""
Events Manager
**************

Centralize the communication between the game elements, the navigation devices, the input systems and the sound engine.
"""

from bge import (
        logic,
        )

from . import base

TODO = True

class Base(base.Base):
    def __init__(self, parent):
        base.Base.__init__(self, parent)

    def setFlashlightMode(self, power=True):
        """
        Activate or Deactivate the flashlight
        """
        self.logger.debug("setFlashlightMode({0})".format(power))
        logic.sendMessage("light")

        if power:
            self._parent.sound.setVolumeLow()

        else:
            self._parent.sound.setVolumeNormal()


    def setSonarMode(self, power=True):
        """
        Activate or Deactivate the sonar
        """
        self.logger.debug("setSonarMode({0})".format(power))
        logic.sendMessage("sonar")

        if power:
            self._parent.sound.setVolumeHigh()

        else:
            self._parent.sound.setVolumeNormal()

    def throwRock(self):
        """
        Throw a rock (to hit a pendulum)
        """
        self.logger.debug("throwRock()")
        logic.sendMessage("rock")

    def spawnEnemy(self, enemy):
        """
        A new enemy got spawned
        """
        self._parent.score.spawn(enemy.enemy)

    def hitEnemy(self, enemy):
        """
        Enemy got hit, congratulations
        """
        self._parent.score.hit(enemy.enemy)
        enemy.kill()

    def hitByEnemy(self, enemy):
        """
        Enemy got the upper hand
        """
        self._parent.score.hitBy(enemy.enemy)
        enemy.kill()

    def evadeEnemy(self, enemy):
        """
        Enemy got too distant, it can go away
        """
        self._parent.score.evade(enemy.enemy)
        enemy.kill()

    def startLap(self):
        """
        Start a new lap
        """
        self.logger.debug('New Lap')

        self._parent.bumpSpeed()

        self._parent.ai.spawnEnemies()

    def gameOver(self):
        """
        The game time is over
        """
        self.logger.debug('Game Over')

        TODO
        """
        do something funky
        """
        logic.endGame()
