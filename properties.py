import bpy


## COMMON
class FCurveHelperCommonProperties(bpy.types.PropertyGroup) :
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
class FCurveHelperGeneratorProperties(bpy.types.PropertyGroup) :
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
class FCurveHelperFNGeneratorProperties(bpy.types.PropertyGroup) :
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
class FCurveHelperEnvelopeProperties(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    reference_value : bpy.props.FloatProperty(name = "Reference Value")
    default_min : bpy.props.FloatProperty(name = "Min", default = -1)
    default_max : bpy.props.FloatProperty(name = "Max", default = 1)

## CYCLES
class FCurveHelperCyclesProperties(bpy.types.PropertyGroup) :
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
class FCurveHelperNoiseProperties(bpy.types.PropertyGroup) :
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
class FCurveHelperLimitsProperties(bpy.types.PropertyGroup) :
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
class FCurveHelperSteppedProperties(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    frame_step : bpy.props.FloatProperty(name = "Step Size", default = 2)
    frame_offset : bpy.props.FloatProperty(name = "Offset")
    
    use_frame_start : bpy.props.BoolProperty(name = "Use Start Frame")
    frame_start : bpy.props.FloatProperty(name = "Start Frame")
    
    use_frame_end : bpy.props.BoolProperty(name = "Use End Frame")
    frame_end : bpy.props.FloatProperty(name = "End Frame")