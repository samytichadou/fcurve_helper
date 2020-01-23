import bpy


### FUNCTIONS ###

# return selected object
def getSelectedObjects(scene):
    object_list = []
    for obj in scene.objects:
        if obj.select_get():
            object_list.append(obj)
    return object_list

# return armature active bones fcurves
def getSelectedBonesFCurves(object):
    curves_list = []
    if object.animation_data:
        if object.type == 'ARMATURE':
            bones_list = []
            for bone in object.data.bones:
                if bone.select:
                    bones_list.append(bone.name)
            for curve in object.animation_data.action.fcurves:
                if curve.select:
                    if curve.data_path.startswith("pose.bones"):
                        for bone in bones_list:
                            if bone in curve.data_path:
                                curves_list.append(curve)                            
    return curves_list

# return bones fcurves
def getSelectedFCurves(object):
    curves_list = []
    if object.animation_data:
        for curve in object.animation_data.action.fcurves:
            if curve.select:
                curves_list.append(curve)
    return curves_list

# get props from modifiers
def getModifierProperties(modifier):
    properties_list = []
    for prop in modifier.bl_rna.properties:
        if not prop.is_readonly:
            properties_list.append(prop)
    return properties_list

# redraw context areas
def redrawContextAreas(context):
    for area in context.screen.areas:
        area.tag_redraw()
        
# set props from RNA
def setPropertiesFromDataset(dataset, modifier):
    for prop in dataset.bl_rna.properties:
        if not prop.is_readonly and prop.identifier != 'name':
            try:
                print("CurveHelper --- setting %s to %s" % (prop.identifier, str(getattr(dataset, prop.identifier)))) ###debug
                setattr(modifier, '%s' % prop.identifier, getattr(dataset, prop.identifier))
            except KeyError:
                print("CurveHelper --- %s not set, KeyError" % prop.identifier) ###debug
                pass


### DRAW FUNCTIONS ###

# COMMON PROPS
def drawCommonProperties(layout, context):
    common_props = context.window_manager.curvehelper_commonproperties[0]
    
    row = layout.row(align=False)
    col = row.column(align=True)
    if common_props.use_restricted_range: icon = 'DISCLOSURE_TRI_DOWN'
    else: icon = 'DISCLOSURE_TRI_RIGHT'
    col.prop(common_props, 'use_restricted_range', icon = icon)
    if common_props.use_restricted_range:
        row = col.row(align=True)
        row.prop(common_props, 'frame_start')
        row.prop(common_props, 'frame_end')
        row = col.row(align=True)
        row.prop(common_props, 'blend_in')
        row.prop(common_props, 'blend_out')
        
    row = layout.row(align=False)
    col = row.column(align=True)
    if common_props.use_influence: icon = 'DISCLOSURE_TRI_DOWN'
    else: icon = 'DISCLOSURE_TRI_RIGHT'
    col.prop(common_props, 'use_influence', icon = icon)
    if common_props.use_influence:
        col.prop(common_props, 'influence', slider = True)
    
# GENERATOR PROPS
def drawGeneratorProperties(layout, context):
    generator_props = context.window_manager.curvehelper_generatorproperties[0]
    
    col = layout.column(align=True)
    col.prop(generator_props, 'mode', text = '')
    col.prop(generator_props, 'use_additive', toggle = True)

    col.separator()
    col.prop(generator_props, 'poly_order')

    col = layout.column()
    if generator_props.mode == "POLYNOMIAL":
        row = col.row(align=True)
        row.label(text = "y =")
        row.prop(generator_props, 'coefficients', text = "", index = 0)
        row.label(text = "")
        row.label(text = "+")
        for i in range(1, generator_props.poly_order+1):
            row = col.row(align=True)
            row.label(text = "")
            row.prop(generator_props, 'coefficients', text = "", index = i)
            if i > 1: row.label(text = "x^"+str(i))
            else: row.label(text = "x")
            if i != generator_props.poly_order: row.label(text = "+")
            else: row.label(text = "")

    else:
        n = -1
        for i in range(0, generator_props.poly_order):
            n += 1
            row = col.row(align=True)
            if n == 0: row.label(text = "y =")
            else: row.label(text = "")
            row.label(text = "(")
            row.prop(generator_props, 'coefficients', text = "", index = n)
            row.label(text = "x +")
            n += 1
            row.prop(generator_props, 'coefficients', text = "", index = n)
            if n == generator_props.poly_order*2-1: row.label(text = ")")
            else: row.label(text = ")x")
    
# FNGENERATOR PROPS
def drawFNGeneratorProperties(layout, context):
    fngenerator_props = context.window_manager.curvehelper_fngeneratorproperties[0]
    
    col = layout.column(align=True)
    col.prop(fngenerator_props, 'function_type', text = "")
    col.prop(fngenerator_props, 'use_additive', toggle = True)
    
    col = layout.column()
    col.prop(fngenerator_props, 'amplitude')
    col.prop(fngenerator_props, 'phase_multiplier')
    col.prop(fngenerator_props, 'phase_offset')
    col.prop(fngenerator_props, 'value_offset')

# ENVELOPE PROPS
def drawEnvelopeProperties(layout, context):
    envelope_props = context.window_manager.curvehelper_envelopeproperties[0]
    
    col = layout.column(align=True)
    col.label(text = "Envelope:")
    col.prop(envelope_props, 'reference_value')

    row = col.row(align=True)
    row.prop(envelope_props, 'default_min')
    row.prop(envelope_props, 'default_max')

# ENVELOPE PROPS
def drawCyclesProperties(layout, context):
    cycles_props = context.window_manager.curvehelper_cyclesproperties[0]
    
    row = layout.row()
    col = row.column(align=True)
    col.label(text = "Before:")
    col.prop(cycles_props, 'mode_before', text = "")
    col.prop(cycles_props, 'cycles_before')

    col = row.column(align=True)
    col.label(text = "After:")
    col.prop(cycles_props, 'mode_after', text = "")
    col.prop(cycles_props, 'cycles_after')

# NOISE PROPS
def drawNoiseProperties(layout, context):
    noise_props = context.window_manager.curvehelper_noiseproperties[0]
    
    layout.prop(noise_props, "blend_type")

    row = layout.row()
    col = row.column()
    col.prop(noise_props, "scale")
    col.prop(noise_props, "strength")
    col.prop(noise_props, "offset")

    col = row.column()
    col.prop(noise_props, "phase")
    col.prop(noise_props, "depth")

# LIMITS PROPS
def drawLimitsProperties(layout, context):
    limits_props = context.window_manager.curvehelper_limitsproperties[0]
    
    row = layout.row()
    col = row.column()
    col.prop(limits_props, "use_min_x")
    col.prop(limits_props, "min_x")

    col = row.column()
    col.prop(limits_props, "use_min_y")
    col.prop(limits_props, "min_y")

    row = layout.row()
    col = row.column()
    col.prop(limits_props, "use_max_x")
    col.prop(limits_props, "max_x")

    col = row.column()
    col.prop(limits_props, "use_max_y")
    col.prop(limits_props, "max_y")

# STEPPED PROPS
def drawSteppedProperties(layout, context):
    stepped_props = context.window_manager.curvehelper_steppedproperties[0]
    
    col = layout.column()
    col.prop(stepped_props, 'frame_step')
    col.prop(stepped_props, 'frame_offset')
    
    col = layout.column(align=True)
    col.prop(stepped_props, 'use_frame_start')
    row = col.row()
    if not stepped_props.use_frame_start: row.enabled = False
    row.prop(stepped_props, 'frame_start')
    
    col = layout.column(align=True)
    col.prop(stepped_props, 'use_frame_end')
    row = col.row()
    if not stepped_props.use_frame_end: row.enabled = False
    row.prop(stepped_props, 'frame_end')
    

### OPERATORS ###

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
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        wm = context.window_manager
        layout = self.layout
        common_props = wm.curvehelper_commonproperties[0]
        
        # show affected fcurves
        
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
            
        
        ### common properties
        #for prop in common_props.bl_rna.properties:
        #    if not prop.is_readonly and prop.identifier != 'name':
        #        layout.prop(common_props, '%s' % prop.identifier)

    def execute(self, context):
        print("CurveHelper --- start add operator") ###debug
        wm = context.window_manager
        common_props = wm.curvehelper_commonproperties[0]
        
        for obj in getSelectedObjects(context.scene):
            
            if self.fcurve_type == 'BONE': curve_list = getSelectedBonesFCurves(obj)
            else: curve_list = getSelectedFCurves(obj)
                
            for curve in curve_list:
                print("CurveHelper --- treating FCurve : " + curve.data_path) ###debug
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
                
        # print log
        # return info log
        redrawContextAreas(context)
                    
        return {'FINISHED'}


### PROPERTIES ###

## COMMON
class CurveHelperCommonProperties(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    mute : bpy.props.BoolProperty(name = "Muted")
    use_restricted_range : bpy.props.BoolProperty(name = "Restrict Frame Range")
    
    frame_start : bpy.props.FloatProperty(name = "Start Frame")
    frame_end : bpy.props.FloatProperty(name = "End Frame")
    blend_in : bpy.props.FloatProperty(name = "Blend In")
    blend_out : bpy.props.FloatProperty(name = "Blend Out")
    
    use_influence : bpy.props.BoolProperty(name = "Use Influence")
    
    influence : bpy.props.FloatProperty(name = "Influence", min = 0, max = 1, default = 1)

## GENERATOR
class CurveHelperGeneratorProperties(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    use_additive : bpy.props.BoolProperty(name = "Additive")
    mode_items = [
        ('POLYNOMIAL', 'Expanded Polynomial', ""),
        ('POLYNOMIAL_FACTORISED', 'Factorised Polynomial', ""),
        ]
    mode : bpy.props.EnumProperty(name = "Mode", items = mode_items)
    
    poly_order : bpy.props.IntProperty(name = "Poly Order", min = 1)
    coefficients : bpy.props.FloatVectorProperty(name = "Coefficients", size = 32)
    
## FNGENERATOR
class CurveHelperFNGeneratorProperties(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    amplitude : bpy.props.FloatProperty(name = "Amplitude", default = 1)
    phase_multiplier : bpy.props.FloatProperty(name = "Phase Multiplier", default = 1)
    phase_offset : bpy.props.FloatProperty(name = "Phase Offset")
    value_offset : bpy.props.FloatProperty(name = "Value Offset")
    
    use_additive : bpy.props.BoolProperty(name = "Additive")
    
    function_type_items = [
        ('SIN', 'Sine', ""),
        ('COS', 'Cosine', ""),
        ('TAN', 'Tangent', ""),
        ('SQRT', 'Square Root', ""),
        ('LN', 'Natural Logarithm', ""),
        ('SINC', 'Normalized Sine', ""),
        ]
    function_type : bpy.props.EnumProperty(name = "Type", items = function_type_items)

## ENVELOPE
class CurveHelperEnvelopeProperties(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    reference_value : bpy.props.FloatProperty(name = "Reference Value")
    default_min : bpy.props.FloatProperty(name = "Min", default = -1)
    default_max : bpy.props.FloatProperty(name = "Max", default = 1)

## CYCLES
class CurveHelperCyclesProperties(bpy.types.PropertyGroup) :
    '''name : StringProperty() ''' 
    mode_items = [
        ('NONE', 'No Cycles', ""),
        ('REPEAT', 'Repeat Motion', ""),
        ('REPEAT', 'Repeat Motion', ""),
        ('REPEAT_OFFSET', 'Repeat with Offset', ""),
        ('MIRROR', 'Repeat Mirrored', ""),
        ]
    mode_before : bpy.props.EnumProperty(name= "Before Mode", items = mode_items)
    cycles_before : bpy.props.IntProperty(name = "Before")
    mode_after : bpy.props.EnumProperty(name= "After Mode", items = mode_items)
    cycles_after : bpy.props.IntProperty(name = "After")

## NOISE
class CurveHelperNoiseProperties(bpy.types.PropertyGroup) :
    '''name : StringProperty() ''' 
    blend_items = [
        ('REPLACE', 'Replace', ""),
        ('ADD', 'Add', ""),
        ('SUBSTRACT', 'Substract', ""),
        ('MULTIPLY', 'Multiply', ""),
        ]
    blend_type : bpy.props.EnumProperty(name = "Blend Type", items = blend_items)

    scale : bpy.props.FloatProperty(name = "Scale", default = 1)
    strength : bpy.props.FloatProperty(name = "Strength", default = 1)
    phase : bpy.props.FloatProperty(name = "Phase", default = 1)
    offset : bpy.props.FloatProperty(name = "Offset")
    depth : bpy.props.IntProperty(name = "Depth")

## LIMITS
class CurveHelperLimitsProperties(bpy.types.PropertyGroup) :
    '''name : StringProperty() ''' 
    use_min_x : bpy.props.BoolProperty(name = "Minimum X")
    use_min_y : bpy.props.BoolProperty(name = "Minimum Y")
    use_max_x : bpy.props.BoolProperty(name = "Maximum X")
    use_max_y : bpy.props.BoolProperty(name = "Maximum Y")

    min_x : bpy.props.FloatProperty(name = "Minimum X")
    min_y : bpy.props.FloatProperty(name = "Minimum Y")
    max_x : bpy.props.FloatProperty(name = "Maximum X")
    max_y : bpy.props.FloatProperty(name = "Maximum Y")

## STEPPED    
class CurveHelperSteppedProperties(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    frame_step : bpy.props.FloatProperty(name = "Step Size", default = 2)
    frame_offset : bpy.props.FloatProperty(name = "Offset")
    
    use_frame_start : bpy.props.BoolProperty(name = "Use Start Frame")
    frame_start : bpy.props.FloatProperty(name = "Start Frame")
    
    use_frame_end : bpy.props.BoolProperty(name = "Use End Frame")
    frame_end : bpy.props.FloatProperty(name = "End Frame")


### REGISTER ###
    
def register():
    bpy.utils.register_class(CurveHelperAddModifier)
    bpy.utils.register_class(CurveHelperCommonProperties)
    bpy.utils.register_class(CurveHelperGeneratorProperties)
    bpy.utils.register_class(CurveHelperFNGeneratorProperties)
    bpy.utils.register_class(CurveHelperEnvelopeProperties)
    bpy.utils.register_class(CurveHelperCyclesProperties)
    bpy.utils.register_class(CurveHelperNoiseProperties)
    bpy.utils.register_class(CurveHelperLimitsProperties)
    bpy.utils.register_class(CurveHelperSteppedProperties)
    
    bpy.types.WindowManager.curvehelper_commonproperties = \
        bpy.props.CollectionProperty(type = CurveHelperCommonProperties)
    bpy.types.WindowManager.curvehelper_generatorproperties = \
        bpy.props.CollectionProperty(type = CurveHelperGeneratorProperties)
    bpy.types.WindowManager.curvehelper_fngeneratorproperties = \
        bpy.props.CollectionProperty(type = CurveHelperFNGeneratorProperties)
    bpy.types.WindowManager.curvehelper_envelopeproperties = \
        bpy.props.CollectionProperty(type = CurveHelperEnvelopeProperties)
    bpy.types.WindowManager.curvehelper_cyclesproperties = \
        bpy.props.CollectionProperty(type = CurveHelperCyclesProperties)
    bpy.types.WindowManager.curvehelper_noiseproperties = \
        bpy.props.CollectionProperty(type = CurveHelperNoiseProperties)
    bpy.types.WindowManager.curvehelper_limitsproperties = \
        bpy.props.CollectionProperty(type = CurveHelperLimitsProperties)
    bpy.types.WindowManager.curvehelper_steppedproperties = \
        bpy.props.CollectionProperty(type = CurveHelperSteppedProperties)
    
def unregister():
    bpy.utils.unregister_class(CurveHelperAddModifier)
    bpy.utils.unregister_class(CurveHelperCommonProperties)
    bpy.utils.unregister_class(CurveHelperGeneratorProperties)
    bpy.utils.unregister_class(CurveHelperFNGeneratorProperties)
    bpy.utils.unregister_class(CurveHelperCyclesProperties)
    bpy.utils.unregister_class(CurveHelperNoiseProperties)
    bpy.utils.unregister_class(CurveHelperLimitsProperties)
    bpy.utils.unregister_class(CurveHelperSteppedProperties)
    
    del bpy.types.WindowManager.curvehelper_commonproperties
    del bpy.types.WindowManager.curvehelper_generatorproperties
    del bpy.types.WindowManager.curvehelper_fngeneratorproperties
    del bpy.types.WindowManager.curvehelper_envelopeproperties
    del bpy.types.WindowManager.curvehelper_cyclesproperties
    del bpy.types.WindowManager.curvehelper_noiseproperties
    del bpy.types.WindowManager.curvehelper_limitsproperties
    del bpy.types.WindowManager.curvehelper_steppedproperties

if __name__ == "__main__":
    register()