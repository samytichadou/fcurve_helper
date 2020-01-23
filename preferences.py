import bpy
import os


addon_name = os.path.basename(os.path.dirname(__file__))

class CurveHelperAddonPrefs(bpy.types.AddonPreferences) :
    bl_idname = addon_name

    def draw(self, context) :
        wm = context.window_manager
        layout = self.layout
        layout.prop(wm, "curvehelper_debug")
            

# get addon preferences
def get_addon_preferences():
    addon = bpy.context.preferences.addons.get(addon_name)
    return getattr(addon, "preferences", None)