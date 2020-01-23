import bpy

from .draw_functions import *
from .functions import *


#operator to add modifier if needed
class CurveHelperAddModifier(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "curvehelper.addmodifier"
    bl_label = "Add or Modify FCurves modifier"
    
    fcurve_type_items = [
        ('BONE', 'Bone', ""),
        ('OBJECT', 'Object', ""),
        ]
    fcurve_type : bpy.props.EnumProperty(items=fcurve_type_items,
                                            name="Type",
                                            )
    modify_if_existing : bpy.props.BoolProperty(name="Modify Existing Modifier")
    modifiers_items = [
        ('GENERATOR', 'Generator', ""),
        ('FNGENERATOR', 'Built-In Function', ""),
        ('ENVELOPE', 'Envelope', ""),
        ('CYCLES', 'Cycles', ""),
        ('NOISE', 'Noise', ""),
        ('LIMITS', 'Limits', ""),
        ('STEPPED', 'Stepped Interpolation', ""),
        ]
    modifiers_list : bpy.props.EnumProperty(items=modifiers_items,
                                            name="Modifiers",
                                            )

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
        common_props = wm.curvehelper_commonproperties[0]
        
        ### TODO ### add copy from active

        ### TODO ### show affected fcurves
        
        layout.prop(self, 'fcurve_type')
        layout.prop(self, 'modify_if_existing')
        
        col = layout.column(align=True)
        box = col.box()
        row = box.row(align=False)
        row.prop(self, 'modifiers_list', text = "")
        row.prop(common_props, 'mute')
        
        ### MODIFIER PROPERTIES ###
        box = col.box()
        if self.modifiers_list == 'GENERATOR': drawGeneratorProperties(box, context)
        elif self.modifiers_list == 'FNGENERATOR': drawFNGeneratorProperties(box, context)
        elif self.modifiers_list == 'ENVELOPE': drawEnvelopeProperties(box, context)
        elif self.modifiers_list == 'CYCLES': drawCyclesProperties(box, context)
        elif self.modifiers_list == 'NOISE': drawNoiseProperties(box, context)
        elif self.modifiers_list == 'LIMITS': drawLimitsProperties(box, context)
        elif self.modifiers_list == 'STEPPED': drawSteppedProperties(box, context)
            
        ### COMMON PROPERTIES ###
        box = col.box()
        drawCommonProperties(box, context)

    def execute(self, context):
        wm = context.window_manager
        common_props = wm.curvehelper_commonproperties[0]

        if wm.curvehelper_debug: print("CurveHelper --- start add operator") ###debug
        
        for obj in getSelectedObjects(context.scene):
            
            if self.fcurve_type == 'BONE': curve_list = getSelectedBonesFCurves(obj)
            else: curve_list = getSelectedFCurves(obj)
                
            for curve in curve_list:
                if wm.curvehelper_debug: print("CurveHelper --- treating FCurve : " + curve.data_path) ###debug
                if not self.modify_if_existing:
                    modifier = curve.modifiers.new(type=self.modifiers_list)
                else:
                    if curve.modifiers:
                        chk_mod = 0
                        for mod in curve.modifiers:
                            if mod.type == self.modifiers_list:
                                modifier = mod
                                chk_mod = 1
                                break
                        if chk_mod == 0:
                            modifier = curve.modifiers.new(type = self.modifiers_list)
                    else: 
                        modifier = curve.modifiers.new(type = self.modifiers_list)
                #set modifier keys
                setPropertiesFromDataset(common_props, modifier)
                if self.modifiers_list == 'GENERATOR':  setPropertiesFromDataset(wm.curvehelper_generatorproperties[0], modifier)
                elif self.modifiers_list == 'FNGENERATOR':  setPropertiesFromDataset(wm.curvehelper_fngeneratorproperties[0], modifier)
                elif self.modifiers_list == 'ENVELOPE':  setPropertiesFromDataset(wm.curvehelper_envelopeproperties[0], modifier)
                elif self.modifiers_list == 'CYCLES':  setPropertiesFromDataset(wm.curvehelper_cyclesproperties[0], modifier)
                elif self.modifiers_list == 'NOISE':  setPropertiesFromDataset(wm.curvehelper_noiseproperties[0], modifier)
                elif self.modifiers_list == 'LIMITS':  setPropertiesFromDataset(wm.curvehelper_limitsproperties[0], modifier)
                elif self.modifiers_list == 'STEPPED': setPropertiesFromDataset(wm.curvehelper_steppedproperties[0], modifier)
                
        ### TODO ### print log
        ### TODO ### return info log
        redrawContextAreas(context)
                    
        return {'FINISHED'}