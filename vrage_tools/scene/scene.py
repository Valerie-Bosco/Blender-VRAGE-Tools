import bpy
import mathutils
import os

from bpy.types      import PropertyGroup
from bpy.props      import (EnumProperty,
                            FloatProperty,
                            FloatVectorProperty,
                            IntProperty,
                            StringProperty,
                            BoolProperty,
                            PointerProperty,
                            CollectionProperty)


from ..utilities.notifications  import display_notification

# Update functions
def update_paint_color_ui(self, context):
    updated_color = context.scene.vrt.paint_color_ui
    context.view_layer['VRT_paint_color'] = tuple(mathutils.Vector(updated_color) - mathutils.Vector((0.5, 0.5, 0.5)))


def update_use_parallax_ui(self, context):
     use_parallax = context.scene.vrt.use_parallax_ui
     context.view_layer['VRT_disable_parallax'] = bool(not use_parallax)

def update_export_path_ui(self, context):
    context.scene.vrt.export_directory = os.path.abspath(context.scene.vrt.export_directory)


# Collection properties
class VRT_Section(PropertyGroup):
    """Holder for VRT section properties"""

    autoload_ignore = None

    name: StringProperty(
        default="Section"
    ) # type: ignore


# Main class
class VRT_Scene(PropertyGroup):
    """Holder for VRT Scene properties"""

    version: IntProperty(
        default=1
    ) # type: ignore

    paint_color_ui: FloatVectorProperty(
        name='Paint Color',
        description="Change display color of colorable VRAGE materials",
        size=3,
        default=(0.5, 0.5, 0.5),
        subtype='COLOR',
        soft_min=0.0,
        soft_max=1.0,
        step=3,
        precision=6,
        update=update_paint_color_ui
        ) # type: ignore

    use_parallax_ui: BoolProperty(
        name="Toggle Parallax",
        description="Enable VRAGE material parallax occlusion mapping",
        default=True,
        update=update_use_parallax_ui
    ) # type: ignore

    sections_list: CollectionProperty(
        type=VRT_Section
        ) # type: ignore

    sections_list_active_index: IntProperty() # type: ignore

    export_name: StringProperty(
        name="Block Base Name",
        description='Base name of block to export (e.g. "CargoContainer")'
    ) # type: ignore

    export_directory: StringProperty(
        name="Quick Export Directory",
        description='Root directory for exporting model. (parent directory of "NonFractured", "Fractured"...)',
        subtype='FILE_PATH',
        update = update_export_path_ui
    ) # type: ignore

    export_variant: EnumProperty(
        items=[
            ('NON_FRACTURED', "Non-fractured", "Export as undamaged, base variant"),
            ('FRACTURED', "Fractured", "Export as fractured variant"),
            ('DEFORMED', "Deformed", "Export as deformed fractured variant")
            ],
        name="Export Variant",
        description="Variant of the block to export. Selects subdirectory in root directory"
    ) # type: ignore