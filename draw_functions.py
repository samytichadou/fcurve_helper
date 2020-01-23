import bpy


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