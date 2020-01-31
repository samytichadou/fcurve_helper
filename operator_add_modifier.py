import bpy

from .draw_functions import *
from .functions import *


#operator to add modifier if needed
class FCurveHelperAddModifier(bpy.types.Operator):
    bl_idname = "fcurvehelper.addmodifier"
    bl_label = "Add or Modify FCurves modifier"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def __init__(self):
        createDummyProperties()
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        wm = context.window_manager
        layout = self.layout
        common_props = wm.fcurvehelper_commonproperties[0]
        
        ### TODO ### show affected fcurves
        
        layout.prop(wm, 'fcurvehelper_fcurve_type')
        layout.prop(wm, 'fcurvehelper_add_mode')
        
        col = layout.column(align=True)
        box = col.box()
        row = box.row(align=False)
        row.prop(wm, 'fcurvehelper_modifiers_list', text = "")
        row.prop(common_props, 'mute')
        row.operator("fcurvehelper.copy_active_modifier", text = "Copy Active")
        
        ### MODIFIER PROPERTIES ###
        box = col.box()
        if wm.fcurvehelper_modifiers_list == 'GENERATOR': drawGeneratorProperties(box, context)
        elif wm.fcurvehelper_modifiers_list == 'FNGENERATOR': drawFNGeneratorProperties(box, context)
        elif wm.fcurvehelper_modifiers_list == 'ENVELOPE': drawEnvelopeProperties(box, context)
        elif wm.fcurvehelper_modifiers_list == 'CYCLES': drawCyclesProperties(box, context)
        elif wm.fcurvehelper_modifiers_list == 'NOISE': drawNoiseProperties(box, context)
        elif wm.fcurvehelper_modifiers_list == 'LIMITS': drawLimitsProperties(box, context)
        elif wm.fcurvehelper_modifiers_list == 'STEPPED': drawSteppedProperties(box, context)
            
        ### COMMON PROPERTIES ###
        box = col.box()
        drawCommonProperties(box, context)

    def execute(self, context):
        wm = context.window_manager
        common_props = wm.fcurvehelper_commonproperties[0]

        if wm.fcurvehelper_debug: print("FCurveHelper --- starting add/modify operator") ###debug
        
        for obj in getSelectedObjects(context.scene):
            
            if wm.fcurvehelper_fcurve_type == 'AUTO':
                if context.mode == 'POSE': curve_list = getSelectedBonesFCurves(obj)
                else: curve_list = getSelectedFCurves(obj)
            elif wm.fcurvehelper_fcurve_type == 'BONE': curve_list = getSelectedBonesFCurves(obj)
            else: curve_list = getSelectedFCurves(obj)
                
            for curve in curve_list:
                modifier = ''
                if wm.fcurvehelper_debug: print("FCurveHelper --- treating FCurve : " + curve.data_path) ###debug
                # add mode
                if wm.fcurvehelper_add_mode == 'ADD':
                    modifier = curve.modifiers.new(type=wm.fcurvehelper_modifiers_list)
                # add and modify mode
                else:
                    if curve.modifiers:
                        chk_mod = 0
                        for mod in curve.modifiers:
                            if mod.type == wm.fcurvehelper_modifiers_list:
                                modifier = mod
                                chk_mod = 1
                                break
                        if chk_mod == 0 and wm.fcurvehelper_add_mode == 'ADD_MODIFY':
                            modifier = curve.modifiers.new(type = wm.fcurvehelper_modifiers_list)
                    else: 
                        if wm.fcurvehelper_add_mode == 'ADD_MODIFY':
                            modifier = curve.modifiers.new(type = wm.fcurvehelper_modifiers_list)
                #set modifier keys
                if modifier != '':
                    setPropertiesFromDataset(common_props, modifier)
                    if wm.fcurvehelper_modifiers_list == 'GENERATOR':       setPropertiesFromDataset(wm.fcurvehelper_generatorproperties[0], modifier)
                    elif wm.fcurvehelper_modifiers_list == 'FNGENERATOR':   setPropertiesFromDataset(wm.fcurvehelper_fngeneratorproperties[0], modifier)
                    elif wm.fcurvehelper_modifiers_list == 'ENVELOPE':      setPropertiesFromDataset(wm.fcurvehelper_envelopeproperties[0], modifier)
                    elif wm.fcurvehelper_modifiers_list == 'CYCLES':        setPropertiesFromDataset(wm.fcurvehelper_cyclesproperties[0], modifier)
                    elif wm.fcurvehelper_modifiers_list == 'NOISE':         setPropertiesFromDataset(wm.fcurvehelper_noiseproperties[0], modifier)
                    elif wm.fcurvehelper_modifiers_list == 'LIMITS':        setPropertiesFromDataset(wm.fcurvehelper_limitsproperties[0], modifier)
                    elif wm.fcurvehelper_modifiers_list == 'STEPPED':       setPropertiesFromDataset(wm.fcurvehelper_steppedproperties[0], modifier)
                
        ### TODO ### print log
        ### TODO ### return info log
        redrawContextAreas(context)
                    
        return {'FINISHED'}