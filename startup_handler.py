import bpy

from bpy.app.handlers import persistent

# create properties
def createDummyProperties():
    wm = bpy.context.window_manager
    chk_creation = 0
    if not wm.fcurvehelper_commonproperties: 
        wm.fcurvehelper_commonproperties.add()
        chk_creation = 1
    if not wm.fcurvehelper_steppedproperties: 
        wm.fcurvehelper_steppedproperties.add()
        chk_creation = 1
    if not wm.fcurvehelper_generatorproperties: 
        wm.fcurvehelper_generatorproperties.add()
        chk_creation = 1
    if not wm.fcurvehelper_fngeneratorproperties: 
        wm.fcurvehelper_fngeneratorproperties.add()
        chk_creation = 1 
    if not wm.fcurvehelper_envelopeproperties: 
        wm.fcurvehelper_envelopeproperties.add()
        chk_creation = 1
    if not wm.fcurvehelper_cyclesproperties: 
        wm.fcurvehelper_cyclesproperties.add()
        chk_creation = 1
    if not wm.fcurvehelper_noiseproperties: 
        wm.fcurvehelper_noiseproperties.add()
        chk_creation = 1
    if not wm.fcurvehelper_limitsproperties: 
        wm.fcurvehelper_limitsproperties.add()
        chk_creation = 1
    if chk_creation == 1 and wm.fcurvehelper_debug: print("FCurveHelper --- dummy properties created") ###debug

@persistent
def fcurvehelper_startup(scene):
    createDummyProperties()