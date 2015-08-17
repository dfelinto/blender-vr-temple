"""
Scoring System
**************

Keep track of player's progress, score and final results
"""

from . import base

TODO = True

class Base(base.Base):
    __slots__ = (
            "_bats_fails",
            "_bats_hits",
            "_bats_total",
            "_bats_evade",
            "_ghosts_fails",
            "_ghosts_hits",
            "_ghosts_total",
            "_ghosts_evade",
            "_pendulums_fails",
            "_pendulums_hits",
            "_pendulums_total",
            "_pendulums_evade",
            )

    def __init__(self, parent):
        base.Base.__init__(self, parent)

        self._bats_total = 0
        self._bats_hits = 0
        self._bats_fails = 0
        self._bats_evade = 0

        self._ghosts_total = 0
        self._ghosts_hits = 0
        self._ghosts_fails = 0
        self._ghosts_evade = 0

        self._pendulums_total = 0
        self._pendulums_hits = 0
        self._pendulums_fails = 0
        self._pendulums_evade = 0

    def _updateScore(self):
        TODO
        print(
                self._bats_total, self._bats_hits, self._bats_fails, self._bats_evade,
                self._ghosts_total, self._ghosts_hits, self._ghosts_fails, self._ghosts_evade,
                self._pendulums_total, self._pendulums_hits, self._pendulums_fails, self._pendulums_evade,
                )

    def spawn(self, enemy):
        """
        Add a new enemy in the game
        """
        assert(enemy in {'BAT','GHOST','PENDULUM'})

        if enemy == 'BAT':
            self._bats_total += 1
        elif enemy == 'GHOST':
            self._ghosts_total += 1
        else:
            self._pendulums_total += 1

        self._updateScore()

    def hit(self, enemy):
        """
        Hit (kill) an enemy
        """
        assert(enemy in {'BAT','GHOST','PENDULUM'})

        if enemy == 'BAT':
            self._bats_hits += 1
        elif enemy == 'GHOST':
            self._ghosts_hits += 1
        else:
            self._pendulums_hits += 1

        self._updateScore()

    def hitBy(self, enemy):
        """
        Got attacked by an enemy
        """
        assert(enemy in {'BAT','GHOST','PENDULUM'})

        if enemy == 'BAT':
            self._bats_fails += 1
        elif enemy == 'GHOST':
            self._ghosts_fails += 1
        else:
            self._pendulums_fails += 1

        self._updateScore()

    def evade(self, enemy):
        """
        Enemy goes away
        """
        assert(enemy in {'BAT','GHOST','PENDULUM'})

        if enemy == 'BAT':
            self._bats_evade += 1
        elif enemy == 'GHOST':
            self._ghosts_evade += 1
        else:
            self._pendulums_evade += 1

        self._updateScore()


