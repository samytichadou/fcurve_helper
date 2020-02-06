import bpy

from .functions import getSelectedObjects, getSelectedBonesFCurves, getSelectedFCurves, redrawContextAreas


#operator to remove modifier
class FCurveHelperRemoveModifier(bpy.types.Operator):
    """Remove selected FCurves Modifiers"""
    bl_idname = "fcurvehelper.remove_modifier"
    bl_label = "Remove Modifiers"
    bl_options = {'UNDO'}
    
    remove_all : bpy.props.BoolProperty(name="Remove All")
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        wm = context.window_manager
        layout = self.layout
        
        ### TODO ### show affected fcurves
        
        layout.prop(wm, 'fcurvehelper_fcurve_type')
        
        col = layout.column(align=True)
        box = col.box()
        row = box.row(align=False)
        split = row.split()
        if self.remove_all: split.enabled = False
        split.prop(wm, 'fcurvehelper_modifiers_list', text = "")

        row.prop(self, 'remove_all')

        split2 = row.split()
        if self.remove_all: split2.enabled = False
        op = split2.operator("fcurvehelper.copy_active_modifier", text = "Copy Active")
        op.from_remove = True

    def execute(self, context):
        wm = context.window_manager

        if wm.fcurvehelper_debug: print("FCurveHelper --- starting remove operator") ###debug
        
        for obj in getSelectedObjects(context.scene):
            
            if wm.fcurvehelper_fcurve_type == 'AUTO':
                if context.mode == 'POSE': curve_list = getSelectedBonesFCurves(obj)
                else: curve_list = getSelectedFCurves(obj)
            elif wm.fcurvehelper_fcurve_type == 'BONE': curve_list = getSelectedBonesFCurves(obj)
            else: curve_list = getSelectedFCurves(obj)
                
            for curve in curve_list:
                if not curve.lock:
                    if wm.fcurvehelper_debug: print("FCurveHelper --- treating FCurve : " + curve.data_path) ###debug
                    if curve.modifiers:
                        for mod in curve.modifiers:
                            if self.remove_all:
                                if wm.fcurvehelper_debug: print("FCurveHelper --- %s removed" % mod.type) ###debug
                                curve.modifiers.remove(mod)
                                curve.modifiers.update()
                            else:
                                if mod.type == wm.fcurvehelper_modifiers_list:
                                    if wm.fcurvehelper_debug: print("FCurveHelper --- %s removed" % mod.type) ###debug
                                    curve.modifiers.remove(mod)
                                    curve.modifiers.update()
                
        ### TODO ### print log
        ### TODO ### return info log

        redrawContextAreas(context)
        context.scene.frame_current = context.scene.frame_current
                    
        return {'FINISHED'}