import bpy

from .functions import getSelectedObjects, getFCurvesFromBone, getFCurves


class FCurveHelperPanel(bpy.types.Panel):
    bl_label = "FCurves Helper"
    bl_idname = "FCURVESHELPER_PT_panel"
    bl_space_type = 'GRAPH_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Modifiers"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator('fcurvehelper.addmodifier', icon = 'ADD')

        row = layout.row()
        row.operator('fcurvehelper.removemodifier', icon = 'REMOVE')


# fcurves inspector draw functions
def drawModifier(layout, modifier, mod_index, obj, curve):
    row = layout.row(align=True)
    row.label(icon = 'MODIFIER_ON')
    row.label(text = modifier.type)
    op = row.operator('fcurvehelper.removemodifierinspector', text = "", icon = 'X')
    op.object_name = obj.name
    op.fcurve_datapath = curve.data_path
    op.fcurve_arrayindex = curve.array_index
    op.modifier_index = mod_index

def drawCurve(layout, curve, obj):
    row = layout.row(align=True)
    
    row.label(icon = 'GRAPH')
    row.label(text = curve.data_path + " " + str(curve.array_index))

    if curve.modifiers:
        mod_index = -1
        col = layout.column(align=True)
        for mod in curve.modifiers:
            mod_index += 1
            box = col.box()
            #box.scale_y = 0.75
            drawModifier(box, mod, mod_index, obj, curve)

def drawCurveInspectorBone(context, layout):
    wm = context.window_manager
    for obj in getSelectedObjects(context.scene):
        if obj.type == 'ARMATURE':
            for bone in obj.data.bones:
                if (    not wm.fcurvehelper_show_only_selected_bones
                    or 
                        (     wm.fcurvehelper_show_only_selected_bones 
                        and bone.select
                        )
                ):
                    row = layout.row(align=True)
                    row.label(text = obj.name, icon = 'TRIA_RIGHT')
                    row.label(text = bone.name, icon = 'BONE_DATA')
                    curve_list = getFCurvesFromBone(bone, obj)
                    if curve_list:
                        col = layout.column(align=True)
                        for curve in curve_list:
                            box = col.box()
                            box.scale_y = 0.5
                            drawCurve(box, curve, obj)

def drawCurveInspectorObject(context, layout):
    for obj in getSelectedObjects(context.scene):
        row = layout.row(align=True)
        row.label(text = obj.name, icon = 'TRIA_RIGHT')
        curve_list = getFCurves(obj)
        if curve_list:
            col = layout.column(align=True)
            for curve in curve_list:
                box = col.box()
                box.scale_y = 0.5
                drawCurve(box, curve, obj)

class FCurveHelperInspectorSubPanel(bpy.types.Panel):
    bl_label = "FCurves Inspector"
    bl_idname = "FCURVESHELPER_PT_inspector_subpanel"
    bl_space_type = 'GRAPH_EDITOR'
    bl_region_type = 'UI'
    bl_parent_id = 'FCURVESHELPER_PT_panel'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def draw(self, context):
        wm = context.window_manager
        curve_type = wm.fcurvehelper_fcurve_type

        layout = self.layout
        row = layout.row(align=True)
        row.prop(wm, 'fcurvehelper_fcurve_type')
        split = row.split()
        split.prop(wm, 'fcurvehelper_show_only_selected_bones', text = "", icon = 'RESTRICT_SELECT_OFF')
                
        if curve_type == 'OBJECT':
            split.enabled = False
            drawCurveInspectorObject(context, layout)
        elif curve_type == 'BONE':
            drawCurveInspectorBone(context, layout)
        elif curve_type == 'AUTO' and context.mode == 'POSE':
            drawCurveInspectorBone(context, layout)
        else:
            split.enabled = False
            drawCurveInspectorObject(context, layout)