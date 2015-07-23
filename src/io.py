"""
Input/Output
************

Takes the three different inputs, process the data and call the corresponding event.
It also handles head transformation/navigation.
"""

from . import base

class Base(base.Base):
    def __init__(self, parent):
        base.Base.__init__(self, parent)

    def loop(self):
        pass
