import bpy

from bpy.types      import PropertyGroup
from bpy.props      import (EnumProperty,
                            FloatProperty,
                            FloatVectorProperty,
                            IntProperty,
                            StringProperty,
                            BoolProperty,
                            PointerProperty,
                            CollectionProperty)


# Main class
class VRT_ViewLayer(PropertyGroup):
    """Holder for VRT View Layer properties"""

    def register():
        bpy.types.ViewLayer.vrt = PointerProperty(type=VRT_ViewLayer)

    def unregister():
        del bpy.types.ViewLayer.vrt

    version: IntProperty(
        default=1
    )

    use_uv_grid: BoolProperty(
        name='Toggle UV Grid',
        description='Show VRAGE material UV Grid overlay',
        default=False,
        )

    use_color_grid: BoolProperty(
        name='Toggle Color Grid',
        description='Show VRAGE material Color Grid overlay',
        default=False,
        )