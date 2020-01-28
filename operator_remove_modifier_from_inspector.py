import bpy

from .functions import createDummyProperties, getSelectedObjects, getSelectedBonesFCurves, getSelectedFCurves, redrawContextAreas, returnFCurve


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
        if returnFCurve(obj, self.fcurve_datapath, self.fcurve_arrayindex):
            curve = returnFCurve(obj, self.fcurve_datapath, self.fcurve_arrayindex )
            modifier = curve.modifiers[self.modifier_index]

            if wm.fcurvehelper_debug: print("FCurveHelper --- %s removing" % modifier.type) ###debug

            curve.modifiers.remove(modifier)
            curve.modifiers.update()
                                                    
        ### TODO ### print log
        ### TODO ### return info log

        redrawContextAreas(context)
        context.scene.frame_current = context.scene.frame_current
                    
        return {'FINISHED'}