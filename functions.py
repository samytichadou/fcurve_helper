import bpy


# return selected object
def getSelectedObjects(scene):
    object_list = []
    for obj in scene.objects:
        if obj.select_get():
            object_list.append(obj)
    return object_list

# return selected armature active bones fcurves
def getSelectedBonesFCurves(object):
    curves_list = []
    if object.animation_data:
        try:
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
        except AttributeError: pass
    return curves_list

# return all armature active bones fcurves
def getFCurvesFromBone(bone, object):
    curves_list = []
    try:
        for curve in object.animation_data.action.fcurves:
            if curve.data_path.startswith("pose.bones"):
                if bone.name in curve.data_path:
                    curves_list.append(curve)
    except AttributeError: pass                     
    return curves_list

# return selected objects fcurves
def getSelectedFCurves(object):
    curves_list = []
    if object.animation_data:
        try:
            for curve in object.animation_data.action.fcurves:
                if curve.select and not curve.data_path.startswith("pose.bones"):
                    curves_list.append(curve)
        except AttributeError: pass
    return curves_list

# return objects fcurves
def getFCurves(object):
    curves_list = []
    if object.animation_data :
        try:
            for curve in object.animation_data.action.fcurves:
                if not curve.data_path.startswith("pose.bones"):
                    curves_list.append(curve)
        except AttributeError: pass
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
                if wm.fcurvehelper_debug: print("FCurveHelper --- setting %s to %s" % (prop.identifier, str(getattr(dataset, prop.identifier)))) ###debug
                setattr(modifier, '%s' % prop.identifier, getattr(dataset, prop.identifier))
            except KeyError:
                if wm.fcurvehelper_debug: print("FCurveHelper --- %s not set, KeyError" % prop.identifier) ###debug
                pass

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