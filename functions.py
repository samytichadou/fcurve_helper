import bpy


# return selected object
def getSelectedObjects(scene):
    object_list = []
    for obj in scene.objects:
        if obj.select_get():
            object_list.append(obj)
    return object_list

# return armature active bones fcurves
def getSelectedBonesFCurves(object):
    curves_list = []
    if object.animation_data:
        if object.type == 'ARMATURE':
            bones_list = []
            for bone in object.data.bones:
                if bone.select:
                    bones_list.append(bone.name)
            for curve in object.animation_data.action.fcurves:
                if curve.select:
                    if curve.data_path.startswith("pose.bones"):
                        for bone in bones_list:
                            if bone in curve.data_path:
                                curves_list.append(curve)                            
    return curves_list

# return bones fcurves
def getSelectedFCurves(object):
    curves_list = []
    if object.animation_data:
        for curve in object.animation_data.action.fcurves:
            if curve.select:
                curves_list.append(curve)
    return curves_list

# get props from modifiers
def getModifierProperties(modifier):
    properties_list = []
    for prop in modifier.bl_rna.properties:
        if not prop.is_readonly:
            properties_list.append(prop)
    return properties_list

# redraw context areas
def redrawContextAreas(context):
    for area in context.screen.areas:
        area.tag_redraw()
        
# set props from RNA
def setPropertiesFromDataset(dataset, modifier):
    wm = bpy.context.window_manager
    for prop in dataset.bl_rna.properties:
        if not prop.is_readonly and prop.identifier != 'name':
            try:
                if wm.curvehelper_debug: print("CurveHelper --- setting %s to %s" % (prop.identifier, str(getattr(dataset, prop.identifier)))) ###debug
                setattr(modifier, '%s' % prop.identifier, getattr(dataset, prop.identifier))
            except KeyError:
                if wm.curvehelper_debug: print("CurveHelper --- %s not set, KeyError" % prop.identifier) ###debug
                pass

# create properties
def createDummyProperties():
    wm = bpy.context.window_manager
    chk_creation = 0
    if not wm.curvehelper_commonproperties: 
        wm.curvehelper_commonproperties.add()
        chk_creation = 1
    if not wm.curvehelper_steppedproperties: 
        wm.curvehelper_steppedproperties.add()
        chk_creation = 1
    if not wm.curvehelper_generatorproperties: 
        wm.curvehelper_generatorproperties.add()
        chk_creation = 1
    if not wm.curvehelper_fngeneratorproperties: 
        wm.curvehelper_fngeneratorproperties.add()
        chk_creation = 1 
    if not wm.curvehelper_envelopeproperties: 
        wm.curvehelper_envelopeproperties.add()
        chk_creation = 1
    if not wm.curvehelper_cyclesproperties: 
        wm.curvehelper_cyclesproperties.add()
        chk_creation = 1
    if not wm.curvehelper_noiseproperties: 
        wm.curvehelper_noiseproperties.add()
        chk_creation = 1
    if not wm.curvehelper_limitsproperties: 
        wm.curvehelper_limitsproperties.add()
        chk_creation = 1
    if chk_creation == 1 and wm.curvehelper_debug: print("CurveHelper --- dummy properties created") ###debug