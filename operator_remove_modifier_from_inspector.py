import bpy

from .functions import createDummyProperties, getSelectedObjects, getSelectedBonesFCurves, getSelectedFCurves, redrawContextAreas


#operator to remove modifier
class FCurveHelperRemoveModifierInspector(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "fcurvehelper.removemodifierinspector"
    bl_label = "Remove FCurves modifier from Inspector"
    bl_options = {'UNDO', 'INTERNAL'}
    
    object_name : bpy.props.StringProperty()
    fcurve_datapath : bpy.props.StringProperty()
    fcurve_arrayindex : bpy.props.IntProperty()
    modifier_index : bpy.props.IntProperty()
    
    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        wm = context.window_manager

        if wm.fcurvehelper_debug: print("FCurveHelper --- starting remove operator from inspector") ###debug

        obj = bpy.data.objects[self.object_name]

        for curve in obj.animation_data.action.fcurves:
            if curve.data_path == self.fcurve_datapath and curve.array_index == self.fcurve_arrayindex:
                modifier = curve.modifiers[self.modifier_index]
                if wm.fcurvehelper_debug: print("FCurveHelper --- %s removing" % modifier.type) ###debug
                curve.modifiers.remove(modifier)

                break
                                                    
        ### TODO ### print log
        ### TODO ### return info log
        redrawContextAreas(context)
                    
        return {'FINISHED'}