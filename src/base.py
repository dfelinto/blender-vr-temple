"""
Base
****

Basic class for all inherited classes.
"""

class Base:
    def __init__(self, parent):
        self._parent = parent

    def loop(self):
        pass
