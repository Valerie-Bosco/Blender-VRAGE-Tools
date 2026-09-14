import bpy

from bpy.types  import PropertyGroup
from bpy.props      import (EnumProperty,
                            FloatProperty,
                            FloatVectorProperty,
                            IntProperty,
                            StringProperty,
                            BoolProperty,
                            PointerProperty,
                            CollectionProperty)






def get_blend_data():

    if '.vrt-data' not in bpy.data.texts:
        data = bpy.data.texts.new('.vrt-data')
    else:
        data = bpy.data.texts['.vrt-data']

    return data