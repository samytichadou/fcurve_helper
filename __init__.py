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
 "version": (0, 1),  
 "blender": (2, 82, 0),  
 "location": "Operators",  
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
    
    bpy.types.WindowManager.fcurvehelper_debug = bpy.props.BoolProperty(name = "Debug Toggle", default=True)

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

    del bpy.types.WindowManager.fcurvehelper_debug

    ### HANDLER
    bpy.app.handlers.load_post.remove(fcurvehelper_startup)