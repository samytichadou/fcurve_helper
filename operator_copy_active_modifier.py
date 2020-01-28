import bpy


class FCurveHelperCopyActiveModifier(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "fcurvehelper.copy_active_modifier"
    bl_label = "Copy Active Modifier"
    bl_options = {'INTERNAL'}

    fcurve_type : bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return context.area.type == 'GRAPH_EDITOR' and context.active_editable_fcurve is not None

    def execute(self, context):
        print(self.fcurve_type)
        print(context.active_editable_fcurve.data_path)
        print(context.active_editable_fcurve.array_index)
        return {'FINISHED'}