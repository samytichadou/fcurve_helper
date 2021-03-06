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
        
# set props from dataset
def setPropertiesFromDataset(datasetin, datasetout):
    wm = bpy.context.window_manager
    for prop in datasetin.bl_rna.properties:
        if not prop.is_readonly and prop.identifier != 'name':
            try:
                if wm.fcurvehelper_debug: print("FCurveHelper --- setting %s to %s" % (prop.identifier, str(getattr(datasetout, prop.identifier)))) ###debug
                setattr(datasetout, '%s' % prop.identifier, getattr(datasetin, prop.identifier))
            #handle generator array error
            except ValueError:
                if wm.fcurvehelper_debug: print("FCurveHelper --- setting %s array after ValueError" % prop.identifier) ###debug
                propin = getattr(datasetin, prop.identifier)
                propout = getattr(datasetout, prop.identifier)
                idx = -1
                for n in propin:
                    idx += 1
                    propout[idx] = n
            except (KeyError, AttributeError):
                if wm.fcurvehelper_debug: print("FCurveHelper --- %s not set, KeyError" % prop.identifier) ###debug
                pass

# returning proper f curve from object, index and array
def returnFCurve(object, data_path, array_index):
    if object.animation_data:
        try:
            for curve in object.animation_data.action.fcurves:
                if curve.data_path == data_path and curve.array_index == array_index:
                    return curve
        except AttributeError:
            pass

# get active modifier from curve
def getActiveModifier(curve):
    if curve.modifiers:
        for mod in curve.modifiers:
            if mod.active:
                return mod