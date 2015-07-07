"""
Dummy Module
************

Hack package to bypass Sphinx/Apidoc requirements
"""

import sys
import builtins

def load_module(name, module):
    sys.modules[name] = module

def load_global(name, value):
    builtins.__dict__[name] = value

from . import (
        bge,
        bgl,
        blf,
        mathutils,
        )

# blender/bge modules
load_module('bge', bge)
load_module('bgl', bgl)
load_module('blf', blf)
load_module('mathutils', mathutils)

# misc hacks
sys.argv.extend(('--', 'dummy.blend'))
