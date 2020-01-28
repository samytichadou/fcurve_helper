import bpy
import os


addon_name = os.path.basename(os.path.dirname(__file__))

class FCurveHelperAddonPrefs(bpy.types.AddonPreferences) :
    bl_idname = addon_name

    inspector_curve_size : bpy.props.FloatProperty(name="Curve Size in Inspector", min=0.1, max=1, default=0.5)
    inspector_modifier_size : bpy.props.FloatProperty(name="Curve Size in Inspector", min=0.1, max=2, default=1)

    def draw(self, context) :
        wm = context.window_manager
        layout = self.layout
        layout.prop(wm, "fcurvehelper_debug")

        row = layout.row()
        row.prop(self, 'inspector_curve_size')
        row.prop(self, 'inspector_modifier_size')
            

# get addon preferences
def get_addon_preferences():
    addon = bpy.context.preferences.addons.get(addon_name)
    return getattr(addon, "preferences", None)