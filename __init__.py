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

classes = (CurveHelperAddModifier,
            CurveHelperCommonProperties,
            CurveHelperGeneratorProperties,
            CurveHelperFNGeneratorProperties,
            CurveHelperEnvelopeProperties,
            CurveHelperCyclesProperties,
            CurveHelperNoiseProperties,
            CurveHelperLimitsProperties,
            CurveHelperSteppedProperties,
            CurveHelperAddonPrefs,
            )

def register():

    ### OPERATORS ###
    from bpy.utils import register_class
    for cls in classes :
        register_class(cls)
    
    ### PROPS ###
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
    
    bpy.types.WindowManager.curvehelper_debug = bpy.props.BoolProperty(name = "Debug Toggle", default=True)

    ### HANDLER ###
    bpy.app.handlers.load_post.append(fcurvehelper_startup)

def unregister():
    
    ### OPERATORS ###
    from bpy.utils import unregister_class
    for cls in reversed(classes) :
        unregister_class(cls)

    ### PROPS ###
    del bpy.types.WindowManager.curvehelper_commonproperties
    del bpy.types.WindowManager.curvehelper_generatorproperties
    del bpy.types.WindowManager.curvehelper_fngeneratorproperties
    del bpy.types.WindowManager.curvehelper_envelopeproperties
    del bpy.types.WindowManager.curvehelper_cyclesproperties
    del bpy.types.WindowManager.curvehelper_noiseproperties
    del bpy.types.WindowManager.curvehelper_limitsproperties
    del bpy.types.WindowManager.curvehelper_steppedproperties

    del bpy.types.WindowManager.curvehelper_debug

    ### HANDLER
    bpy.app.handlers.load_post.remove(fcurvehelper_startup)