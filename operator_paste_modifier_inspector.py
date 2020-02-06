import bpy

from .functions import setPropertiesFromDataset, returnFCurve


class FCurveHelperPasteModifierInspector(bpy.types.Operator):
    """Paste copied Modifier here"""
    bl_idname = "fcurvehelper.paste_modifier_inspector"
    bl_label = "Paste Modifier"
    bl_options = {'UNDO', 'INTERNAL'}

    object_name : bpy.props.StringProperty()
    fcurve_datapath : bpy.props.StringProperty()
    fcurve_arrayindex : bpy.props.IntProperty()

    @classmethod
    def poll(cls, context):
        return context.window_manager.fcurvehelper_is_copied

    def execute(self, context):
        wm = context.window_manager
        wm.fcurvehelper_is_copied = True
        if wm.fcurvehelper_debug: print("FCurveHelper --- starting Paste Modifier from Inspector operator") ###debug
        
        object = bpy.data.objects[self.object_name]
        fcurve = returnFCurve(object, self.fcurve_datapath, self.fcurve_arrayindex)
        if wm.fcurvehelper_debug: print("FCurveHelper --- treating " + fcurve.data_path + str(fcurve.array_index)) ###debug

        modifier = ''
        # add mode
        if wm.fcurvehelper_paste_mode == "ADD":
            modifier = fcurve.modifiers.new(type = wm.fcurvehelper_modifiers_list)
        # add and modify mode
        else:
            if fcurve.modifiers:
                chk_mod = 0
                for mod in fcurve.modifiers:
                    if mod.type == wm.fcurvehelper_modifiers_list:
                        modifier = mod
                        chk_mod = 1
                        break
                if chk_mod == 0 and wm.fcurvehelper_paste_mode == 'ADD_MODIFY':
                    modifier = fcurve.modifiers.new(type = wm.fcurvehelper_modifiers_list)
            else: 
                if wm.fcurvehelper_paste_mode == 'ADD_MODIFY':
                    modifier = fcurve.modifiers.new(type = wm.fcurvehelper_modifiers_list)

        if wm.fcurvehelper_debug: ###debug
            if modifier != '': print("FCurveHelper --- added : " + modifier.type) ###debug
            else: print("FCurveHelper --- no modifier to set") ###debug
        
        if modifier != '':
            # set props
            setPropertiesFromDataset( wm.fcurvehelper_commonproperties[0], modifier)
            if modifier.type == 'GENERATOR':        setPropertiesFromDataset(wm.fcurvehelper_generatorproperties[0], modifier)
            elif modifier.type == 'FNGENERATOR':    setPropertiesFromDataset(wm.fcurvehelper_fngeneratorproperties[0], modifier)
            elif modifier.type == 'ENVELOPE':       setPropertiesFromDataset(wm.fcurvehelper_envelopeproperties[0], modifier)
            elif modifier.type == 'CYCLES':         setPropertiesFromDataset(wm.fcurvehelper_cyclesproperties[0], modifier)
            elif modifier.type == 'NOISE':          setPropertiesFromDataset(wm.fcurvehelper_noiseproperties[0], modifier)
            elif modifier.type == 'LIMITS':         setPropertiesFromDataset(wm.fcurvehelper_limitsproperties[0], modifier)
            elif modifier.type == 'STEPPED':        setPropertiesFromDataset(wm.fcurvehelper_steppedproperties[0], modifier)

        return {'FINISHED'}