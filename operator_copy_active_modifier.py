import bpy


class FCurveHelperCopyActiveModifier(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "fcurvehelper.copy_active_modifier"
    bl_label = "Copy Active Modifier"

    fcurve_type = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        print(self.fcurve_type)
        return {'FINISHED'}