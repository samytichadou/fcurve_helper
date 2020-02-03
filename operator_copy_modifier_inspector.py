import bpy

from .functions import setPropertiesFromDataset, returnFCurve, getActiveModifier


class FCurveHelperCopyModifierInspector(bpy.types.Operator):
    """Copy this Modifier"""
    bl_idname = "fcurvehelper.copy_modifier_inspector"
    bl_label = "Copy Modifier"
    bl_options = {'UNDO', 'INTERNAL'}

    object_name : bpy.props.StringProperty()
    fcurve_datapath : bpy.props.StringProperty()
    fcurve_arrayindex : bpy.props.IntProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        wm = context.window_manager
        wm.fcurvehelper_is_copied = True
        if wm.fcurvehelper_debug: print("FCurveHelper --- starting Copy Active Modifier from Inspector operator") ###debug
        
        object = bpy.data.objects[self.object_name]
        fcurve = returnFCurve(object, self.fcurve_datapath, self.fcurve_arrayindex)
        if wm.fcurvehelper_debug: print("FCurveHelper --- treating " + fcurve.data_path + str(fcurve.array_index)) ###debug

        modifier = getActiveModifier(fcurve)

        wm.fcurvehelper_modifiers_list = modifier.type
        if wm.fcurvehelper_debug: print("FCurveHelper --- active modifier : " + modifier.type) ###debug

        # set props if op called from add modifier operator
        setPropertiesFromDataset(modifier, wm.fcurvehelper_commonproperties[0])
        if modifier.type == 'GENERATOR':        setPropertiesFromDataset(modifier, wm.fcurvehelper_generatorproperties[0])
        elif modifier.type == 'FNGENERATOR':    setPropertiesFromDataset(modifier, wm.fcurvehelper_fngeneratorproperties[0])
        elif modifier.type == 'ENVELOPE':       setPropertiesFromDataset(modifier, wm.fcurvehelper_envelopeproperties[0])
        elif modifier.type == 'CYCLES':         setPropertiesFromDataset(modifier, wm.fcurvehelper_cyclesproperties[0])
        elif modifier.type == 'NOISE':          setPropertiesFromDataset(modifier, wm.fcurvehelper_noiseproperties[0])
        elif modifier.type == 'LIMITS':         setPropertiesFromDataset(modifier, wm.fcurvehelper_limitsproperties[0])
        elif modifier.type == 'STEPPED':        setPropertiesFromDataset(modifier, wm.fcurvehelper_steppedproperties[0])

        return {'FINISHED'}