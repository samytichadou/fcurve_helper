import bpy

from .functions import getSelectedObjects, getFCurvesFromBone, getFCurves
from .preferences import get_addon_preferences

### PANEL ###

class FCurveHelperPanel(bpy.types.Panel):
    bl_label = "FCurves Helper"
    bl_idname = "FCURVESHELPER_PT_panel"
    bl_space_type = 'GRAPH_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Helper"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator('fcurvehelper.addmodifier', icon = 'ADD')

        row = layout.row()
        row.operator('fcurvehelper.removemodifier', icon = 'REMOVE')

### INSPECTOR ###

# fcurves inspector draw functions
def drawModifier(layout, modifier, mod_index, obj, curve):
    row = layout.row(align=True)
    row.label(icon = 'MODIFIER_ON')
    row.prop(modifier, 'active', text="", emboss=False)
    row.label(text = modifier.type)

    row2 = row.row(align=True)
    if curve.lock: row2.enabled = False

    row2.prop(modifier, 'mute', text="", invert_checkbox=True, emboss=False)

    op = row2.operator('fcurvehelper.removemodifierinspector', text = "", icon = 'X', emboss=False)
    op.object_name = obj.name
    op.fcurve_datapath = curve.data_path
    op.fcurve_arrayindex = curve.array_index
    op.modifier_index = mod_index

    op = row.operator('fcurvehelper.copy_active_modifier_inspector', text = "", icon = 'COPYDOWN', emboss=False)
    op.object_name = obj.name
    op.fcurve_datapath = curve.data_path
    op.fcurve_arrayindex = curve.array_index

def drawCurve(layout, curve, obj):
    prefs = get_addon_preferences()
    modifier_size = prefs.inspector_modifier_size
    
    row = layout.row(align=True)
    if curve == bpy.context.active_editable_fcurve: row.label(icon = 'RADIOBUT_ON')
    else: row.label(icon = 'RADIOBUT_OFF')
    #hide
    if curve.hide: icon = 'HIDE_ON'
    else: icon = 'HIDE_OFF'
    row.prop(curve, 'hide', text="", icon=icon, emboss=False)
    #selection state
    if curve.select: icon = 'RESTRICT_SELECT_OFF'
    else: icon = 'RESTRICT_SELECT_ON'
    row.prop(curve, 'select', text="", icon=icon, toggle=False, emboss=False)
    #name
    if "pose.bones[" in curve.data_path:
        name = curve.data_path.split('"].')[1] + " " + str(curve.array_index)
    else:
        name = curve.data_path + " " + str(curve.array_index)
    row.label(text = name)
    #mute
    if curve.mute: icon = 'CHECKBOX_DEHLT'
    else: icon = 'CHECKBOX_HLT'
    row.prop(curve, 'mute', text="", icon=icon, emboss=False)
    #lock
    if curve.lock: icon = 'LOCKED'
    else: icon = 'UNLOCKED'
    row.prop(curve, 'lock', text="", icon=icon, emboss=False)

    split = row.split()
    if curve.lock: split.enabled = False
    op = split.operator('fcurvehelper.paste_modifier_inspector', text = "", icon = 'PASTEDOWN', emboss = False)
    op.object_name = obj.name
    op.fcurve_datapath = curve.data_path
    op.fcurve_arrayindex = curve.array_index

    if curve.modifiers:
        mod_index = -1
        col = layout.column(align=True)
        for mod in curve.modifiers:
            mod_index += 1
            box = col.box()
            box.scale_y = modifier_size
            drawModifier(box, mod, mod_index, obj, curve)

def drawCurveInspectorBone(context, layout):
    prefs = get_addon_preferences()
    curve_size = prefs.inspector_curve_size
    wm = context.window_manager
    for obj in getSelectedObjects(context.scene):
        if obj.type == 'ARMATURE':
            for bone in obj.data.bones:
                if (wm.fcurvehelper_show_all_bones
                    or 
                        (not wm.fcurvehelper_show_all_bones 
                        and bone.select
                        )
                ):
                    curve_list = getFCurvesFromBone(bone, obj)
                    if curve_list:

                        chk_display_obj = 0
                        if wm.fcurvehelper_show_only_modifiers:
                            for curve in curve_list:
                                if curve.modifiers: 
                                    chk_display_obj = 1
                                    break
                        else :
                            chk_display_obj = 1

                        if chk_display_obj:
                            row = layout.row(align=True)
                            row.label(text = obj.name, icon = 'ARMATURE_DATA')
                            row.label(text = bone.name, icon = 'BONE_DATA')
                            col = layout.column(align=True)

                            for curve in curve_list:
                                if wm.fcurvehelper_show_only_modifiers:
                                    if curve.modifiers:
                                        box = col.box()
                                        box.scale_y = curve_size
                                        drawCurve(box, curve, obj)
                                else:
                                    box = col.box()
                                    box.scale_y = curve_size
                                    drawCurve(box, curve, obj)

def drawCurveInspectorObject(context, layout):
    prefs = get_addon_preferences()
    curve_size = prefs.inspector_curve_size
    wm = context.window_manager
    for obj in getSelectedObjects(context.scene):
        curve_list = getFCurves(obj)
        if curve_list:
            row = layout.row(align=True)
            row.label(text = obj.name, icon = 'MESH_CUBE')
            col = layout.column(align=True)
            for curve in curve_list:
                if wm.fcurvehelper_show_only_modifiers:
                    if curve.modifiers:
                        box = col.box()
                        box.scale_y = curve_size
                        drawCurve(box, curve, obj)
                else:
                    box = col.box()
                    box.scale_y = curve_size
                    drawCurve(box, curve, obj)

class FCurveHelperInspectorSubPanel(bpy.types.Panel):
    bl_label = "FCurves Inspector"
    bl_idname = "FCURVESHELPER_PT_inspector_subpanel"
    bl_space_type = 'GRAPH_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Helper"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def draw(self, context):
        wm = context.window_manager
        curve_type = wm.fcurvehelper_fcurve_type

        layout = self.layout
        row = layout.row(align=True)
        row.prop(wm, 'fcurvehelper_fcurve_type')
        row.prop(wm, 'fcurvehelper_show_only_modifiers', text="", icon="MODIFIER_ON")
        split = row.split()
        split.prop(wm, 'fcurvehelper_show_all_bones', text = "", icon = 'GROUP_BONE')
                
        row = layout.row(align=True)
        row.prop(wm, 'fcurvehelper_add_mode', text = "Paste")

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