import bpy


class FCurveHelperPanel(bpy.types.Panel):
    bl_label = "FCurves Helper"
    bl_idname = "FCURVESHELPER_PT_panel"
    bl_space_type = 'GRAPH_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Modifiers"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator('fcurvehelper.addmodifier')

        row = layout.row()
        row.operator('fcurvehelper.removemodifier')
