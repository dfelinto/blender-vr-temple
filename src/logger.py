"""
Logger
*****

Handles all printing/logging operations
"""

from bge import logic


class Base:
    def __new__(self, parent):
        if not hasattr(logic, 'BlenderVR'):
            return Printer()

        else:
            return Logger()


# ############################################################
# Fallback logger (aka stdout)
# ############################################################

class Printer:
    def __getattr__(self, attrname):
        if attrname in self.__dict__:
            return self.__dict__[attrname]
        else:
            return Print(attrname)


class Print:
    def __init__(self, function):
        self._function = function

    def __call__(self, *args, **kwargs):
        print(self._function, *args)


# ############################################################
# BlenderVR logger
# ############################################################

class Logger:
    def __init__(self):
        self._blendervr = logic.BlenderVR

    def __getattr__(self, attrname):
        if attrname in self.__dict__:
            return self.__dict__[attrname]
        else:
            return self._blendervr.logger.__dict__[attrname]


