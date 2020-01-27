import bpy

from .functions import createDummyProperties, getSelectedObjects, getSelectedBonesFCurves, getSelectedFCurves, redrawContextAreas


#operator to remove modifier
class FCurveHelperRemoveModifier(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "fcurvehelper.removemodifier"
    bl_label = "Remove FCurves modifier"
    
    fcurve_type_items = [
        ('BONE', 'Bone', ""),
        ('OBJECT', 'Object', ""),
        ]
    fcurve_type : bpy.props.EnumProperty(items=fcurve_type_items,
                                            name="Type",
                                            )
    remove_all : bpy.props.BoolProperty(name="Remove All")
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def __init__(self):
        createDummyProperties()
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        wm = context.window_manager
        layout = self.layout
        
        ### TODO ### show affected fcurves
        
        layout.prop(self, 'fcurve_type')
        
        col = layout.column(align=True)
        box = col.box()
        row = box.row(align=False)
        row.prop(wm, 'fcurvehelper_modifiers_list', text = "")
        row.prop(self, 'remove_all')
        op = row.operator("fcurvehelper.copy_active_modifier", text = "Copy Active")
        op.fcurve_type = self.fcurve_type

    def execute(self, context):
        wm = context.window_manager

        if wm.fcurvehelper_debug: print("FCurveHelper --- starting remove operator") ###debug
        
        for obj in getSelectedObjects(context.scene):
            
            if self.fcurve_type == 'BONE': curve_list = getSelectedBonesFCurves(obj)
            else: curve_list = getSelectedFCurves(obj)
                
            for curve in curve_list:
                if wm.fcurvehelper_debug: print("FCurveHelper --- treating FCurve : " + curve.data_path) ###debug
                if curve.modifiers:
                    for mod in curve.modifiers:
                        if self.remove_all:
                            if wm.fcurvehelper_debug: print("FCurveHelper --- %s removed" % mod.type) ###debug
                            curve.modifiers.remove(mod)
                        else:
                            if mod.type == wm.fcurvehelper_modifiers_list:
                                if wm.fcurvehelper_debug: print("FCurveHelper --- %s removed" % mod.type) ###debug
                                curve.modifiers.remove(mod)
                
        ### TODO ### print log
        ### TODO ### return info log
        redrawContextAreas(context)
                    
        return {'FINISHED'}