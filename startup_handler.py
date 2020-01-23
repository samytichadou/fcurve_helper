import bpy

from bpy.app.handlers import persistent
from .functions import createDummyProperties

@persistent
def fcurvehelper_startup(scene):
    createDummyProperties()