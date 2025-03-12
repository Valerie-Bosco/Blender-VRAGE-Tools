import bpy
import mathutils

from bpy.types      import PropertyGroup
from bpy.props      import (EnumProperty,
                            FloatProperty,
                            FloatVectorProperty,
                            IntProperty,
                            StringProperty,
                            BoolProperty,
                            PointerProperty,
                            CollectionProperty)

# Utils
def scene_register():
    bpy.types.Scene.vrt = PointerProperty(type=VRT_Scene)


def scene_unregister():
    del bpy.types.Scene.vrt


# Update functions
def update_paint_color_ui(self, context):
    updated_color = context.scene.vrt.paint_color_ui
    context.view_layer['VRT_paint_color'] = tuple(mathutils.Vector(updated_color) - mathutils.Vector((0.5, 0.5, 0.5)))


def update_use_parallax_ui(self, context):
     use_parallax = context.scene.vrt.use_parallax_ui
     context.view_layer['VRT_disable_parallax'] = bool(not use_parallax)


# Collection properties
class VRT_Section(PropertyGroup):
    """Holder for VRT section properties"""

    autoload_ignore = None

    name: StringProperty(
        default="Section"
    )


# Main class
class VRT_Scene(PropertyGroup):
    """Holder for VRT Scene properties"""

    paint_color_ui: FloatVectorProperty(
        name='Paint Color',
        description="Change display color of colorable VRage materials",
        size=3,
        default=(0.5, 0.5, 0.5),
        subtype='COLOR',
        soft_min=0.0,
        soft_max=1.0,
        step=3,
        precision=6,
        update=update_paint_color_ui
        )

    use_parallax_ui: BoolProperty(
        name="Toggle Parallax",
        description="Enable VRage material parallax occlusion mapping",
        default=True,
        update=update_use_parallax_ui
    )

    sections_list: CollectionProperty(
        type=VRT_Section
        )

    sections_list_active_index: IntProperty()

    export_name: StringProperty(
        name="Block Base Name",
        description='Base name of block to export (e.g. "CargoContainer")'
    )

    export_directory: StringProperty(
        name="Quick Export Directory",
        description='Root directory for exporting model. (parent directory of "NonFractured", "Fractured"...)',
        subtype='FILE_PATH'
    )

    export_variant: EnumProperty(
        items=[
            ('NON_FRACTURED', "Non-fractured", "Export as undamaged, base variant"),
            ('FRACTURED', "Fractured", "Export as fractured variant"),
            ('DEFORMED', "Deformed", "Export as deformed fractured variant")
            ],
        name="Export Variant",
        description="Variant of the block to export. Selects subdirectory in root directory"
    )