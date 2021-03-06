import bpy

from .functions import setPropertiesFromDataset, getActiveModifier


class FCurveHelperCopyActiveModifier(bpy.types.Operator):
    """Copy Active Modifier from FCurve"""
    bl_idname = "fcurvehelper.copy_active_modifier"
    bl_label = "Copy Active Modifier"
    bl_options = {'UNDO', 'INTERNAL'}

    from_remove : bpy.props.BoolProperty(default=False)

    @classmethod
    def poll(cls, context):
        return context.area.type == 'GRAPH_EDITOR' and context.active_editable_fcurve is not None and context.active_editable_fcurve.modifiers

    def execute(self, context):
        wm = context.window_manager
        if wm.fcurvehelper_debug: print("FCurveHelper --- starting Copy Active Modifier operator") ###debug
        
        fcurve = context.active_editable_fcurve
        if wm.fcurvehelper_debug: print("FCurveHelper --- treating " + fcurve.data_path + str(fcurve.array_index)) ###debug

        modifier = getActiveModifier(fcurve)

        wm.fcurvehelper_modifiers_list = modifier.type
        if wm.fcurvehelper_debug: print("FCurveHelper --- active modifier : " + modifier.type) ###debug

        # set props if op called from add modifier operator
        if not self.from_remove:
            setPropertiesFromDataset(modifier, wm.fcurvehelper_commonproperties[0])
            if modifier.type == 'GENERATOR':        setPropertiesFromDataset(modifier, wm.fcurvehelper_generatorproperties[0])
            elif modifier.type == 'FNGENERATOR':    setPropertiesFromDataset(modifier, wm.fcurvehelper_fngeneratorproperties[0])
            elif modifier.type == 'ENVELOPE':       setPropertiesFromDataset(modifier, wm.fcurvehelper_envelopeproperties[0])
            elif modifier.type == 'CYCLES':         setPropertiesFromDataset(modifier, wm.fcurvehelper_cyclesproperties[0])
            elif modifier.type == 'NOISE':          setPropertiesFromDataset(modifier, wm.fcurvehelper_noiseproperties[0])
            elif modifier.type == 'LIMITS':         setPropertiesFromDataset(modifier, wm.fcurvehelper_limitsproperties[0])
            elif modifier.type == 'STEPPED':        setPropertiesFromDataset(modifier, wm.fcurvehelper_steppedproperties[0])

        return {'FINISHED'}