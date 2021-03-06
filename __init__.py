'''
Copyright (C) 2018 Samy Tichadou (tonton)
samytichadou@gmail.com

Created by Samy Tichadou (tonton)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {  
 "name": "FCurve Helper",  
 "author": "Samy Tichadou (tonton)",  
 "version": (1, 0),  
 "blender": (2, 82, 0),  
 "location": "Graph Editor",  
 "description": "Utilities to help with FCurves handling",  
  "wiki_url": "https://github.com/samytichadou/fcurve_helper",  
 "tracker_url": "https://github.com/samytichadou/fcurve_helper/issues/new",  
 "category": "Animation"}


import bpy


# IMPORT SPECIFICS
##################################

from .startup_handler import fcurvehelper_startup

from .properties import *
from .operator_add_modifier import *
from .operator_copy_active_modifier import *
from .operator_copy_modifier_inspector import *
from .operator_paste_modifier_inspector import *
from .operator_remove_modifier import *
from .operator_remove_modifier_from_inspector import *
from .gui import *
from .preferences import *


# register
##################################

classes = (FCurveHelperAddModifier,
            FCurveHelperCommonProperties,
            FCurveHelperGeneratorProperties,
            FCurveHelperFNGeneratorProperties,
            FCurveHelperEnvelopeProperties,
            FCurveHelperCyclesProperties,
            FCurveHelperNoiseProperties,
            FCurveHelperLimitsProperties,
            FCurveHelperSteppedProperties,
            FCurveHelperAddonPrefs,
            FCurveHelperCopyActiveModifier,
            FCurveHelperCopyModifierInspector,
            FCurveHelperPasteModifierInspector,
            FCurveHelperRemoveModifier,
            FCurveHelperPanel,
            FCurveHelperInspectorSubPanel,
            FCurveHelperRemoveModifierInspector,
            )

def register():

    ### OPERATORS ###
    from bpy.utils import register_class
    for cls in classes :
        register_class(cls)
    
    ### PROPS ###
    bpy.types.WindowManager.fcurvehelper_commonproperties = \
        bpy.props.CollectionProperty(type = FCurveHelperCommonProperties)
    bpy.types.WindowManager.fcurvehelper_generatorproperties = \
        bpy.props.CollectionProperty(type = FCurveHelperGeneratorProperties)
    bpy.types.WindowManager.fcurvehelper_fngeneratorproperties = \
        bpy.props.CollectionProperty(type = FCurveHelperFNGeneratorProperties)
    bpy.types.WindowManager.fcurvehelper_envelopeproperties = \
        bpy.props.CollectionProperty(type = FCurveHelperEnvelopeProperties)
    bpy.types.WindowManager.fcurvehelper_cyclesproperties = \
        bpy.props.CollectionProperty(type = FCurveHelperCyclesProperties)
    bpy.types.WindowManager.fcurvehelper_noiseproperties = \
        bpy.props.CollectionProperty(type = FCurveHelperNoiseProperties)
    bpy.types.WindowManager.fcurvehelper_limitsproperties = \
        bpy.props.CollectionProperty(type = FCurveHelperLimitsProperties)
    bpy.types.WindowManager.fcurvehelper_steppedproperties = \
        bpy.props.CollectionProperty(type = FCurveHelperSteppedProperties)
    
    bpy.types.WindowManager.fcurvehelper_debug = bpy.props.BoolProperty(name = "Debug Toggle", default=False)

    modifiers_items = [
        ('GENERATOR', 'Generator', ""),
        ('FNGENERATOR', 'Built-In Function', ""),
        ('ENVELOPE', 'Envelope', ""),
        ('CYCLES', 'Cycles', ""),
        ('NOISE', 'Noise', ""),
        ('LIMITS', 'Limits', ""),
        ('STEPPED', 'Stepped Interpolation', ""),
        ]
    bpy.types.WindowManager.fcurvehelper_modifiers_list = bpy.props.EnumProperty(items=modifiers_items,
                                            name="Modifiers",
                                            )
    fcurve_type_items = [
        ('AUTO', 'Automatic', ""),
        ('BONE', 'Bone', ""),
        ('OBJECT', 'Object', ""),
        ]
    bpy.types.WindowManager.fcurvehelper_fcurve_type = bpy.props.EnumProperty(items=fcurve_type_items,
                                            name="Type",
                                            )

    add_mode_items = [
        ('ADD_MODIFY', 'Add or Modify Existing', ""),
        ('MODIFY', 'Modify Existing Only', ""),
        ('ADD', 'Add', ""),
        ]                                          
    bpy.types.WindowManager.fcurvehelper_add_mode = bpy.props.EnumProperty(items=add_mode_items,
                                            name="Mode",
                                            )
    bpy.types.WindowManager.fcurvehelper_paste_mode = bpy.props.EnumProperty(items=add_mode_items,
                                            name="Paste Mode",
                                            default = 'ADD',
                                            )

    bpy.types.WindowManager.fcurvehelper_show_all_bones = bpy.props.BoolProperty(name = "Show all Bones")
    bpy.types.WindowManager.fcurvehelper_show_only_modifiers = bpy.props.BoolProperty(name = "Show only FCurves with Modifier")
    bpy.types.WindowManager.fcurvehelper_is_copied = bpy.props.BoolProperty()

    ### HANDLER ###
    bpy.app.handlers.load_post.append(fcurvehelper_startup)

def unregister():
    
    ### OPERATORS ###
    from bpy.utils import unregister_class
    for cls in reversed(classes) :
        unregister_class(cls)

    ### PROPS ###
    del bpy.types.WindowManager.fcurvehelper_commonproperties
    del bpy.types.WindowManager.fcurvehelper_generatorproperties
    del bpy.types.WindowManager.fcurvehelper_fngeneratorproperties
    del bpy.types.WindowManager.fcurvehelper_envelopeproperties
    del bpy.types.WindowManager.fcurvehelper_cyclesproperties
    del bpy.types.WindowManager.fcurvehelper_noiseproperties
    del bpy.types.WindowManager.fcurvehelper_limitsproperties
    del bpy.types.WindowManager.fcurvehelper_steppedproperties
    del bpy.types.WindowManager.fcurvehelper_modifiers_list
    del bpy.types.WindowManager.fcurvehelper_fcurve_type
    del bpy.types.WindowManager.fcurvehelper_add_mode
    del bpy.types.WindowManager.fcurvehelper_paste_mode
    del bpy.types.WindowManager.fcurvehelper_show_all_bones
    del bpy.types.WindowManager.fcurvehelper_show_only_modifiers
    del bpy.types.WindowManager.fcurvehelper_is_copied

    del bpy.types.WindowManager.fcurvehelper_debug

    ### HANDLER
    bpy.app.handlers.load_post.remove(fcurvehelper_startup)