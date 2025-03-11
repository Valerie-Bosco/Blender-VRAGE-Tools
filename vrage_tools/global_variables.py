import bpy

from .functions.fn_ui import on_vrt_paintcolor_update, on_vrt_parallax_update

class VRT_Section(bpy.types.PropertyGroup):
    autoload_ignore = None
    name: bpy.props.StringProperty(
        default="Section"
    ) # type: ignore


def create():
    bpy.types.Scene.VRT_paint_color_ui = bpy.props.FloatVectorProperty(
        name='Paint Color', 
        description="Change display color of colorable VRage materials", 
        size=3, 
        default=(0.5, 0.5, 0.5), 
        subtype='COLOR', 
        soft_min=0.0, 
        soft_max=1.0, 
        step=3, 
        precision=6, 
        update=on_vrt_paintcolor_update
        )
    
    bpy.types.Scene.VRT_use_parallax_ui = bpy.props.BoolProperty(
        name="Toggle Parallax",
        description="Enable VRage material parallax occlusion mapping",
        default=True,
        update=on_vrt_parallax_update
    )

    bpy.types.ViewLayer.VRT_use_uv_grid = bpy.props.BoolProperty(
        name='Toggle UV Grid', 
        description='Show VRage material UV Grid overlay', 
        default=False, 
        )
    
    bpy.types.ViewLayer.VRT_use_color_grid = bpy.props.BoolProperty(
        name='Toggle Color Grid', 
        description='Show VRage material Color Grid overlay', 
        default=False, 
        )
    
    bpy.utils.register_class(VRT_Section)
    bpy.types.Scene.VRT_sections_list = bpy.props.CollectionProperty(
        type=VRT_Section
        )
    bpy.types.Scene.VRT_sections_list_active_index = bpy.props.IntProperty()
    bpy.types.Scene.VRT_export_name = bpy.props.StringProperty(
        name="Block Base Name",
        description='Base name of block to export (e.g. "CargoContainer")'
    )
    bpy.types.Scene.VRT_export_directory = bpy.props.StringProperty(
        name="Quick Export Directory",
        description='Root directory for exporting model. (parent directory of "NonFractured", "Fractured"...)',
        subtype='FILE_PATH'
    )
    bpy.types.Scene.VRT_export_variant = bpy.props.EnumProperty(
        items=[
            ('NON_FRACTURED', "Non-fractured", "Export as undamaged, base variant"),
            ('FRACTURED', "Fractured", "Export as fractured variant"),
            ('DEFORMED', "Deformed", "Export as deformed fractured variant")
            ],
        name="Export Variant",
        description="Variant of the block to export. Selects subdirectory in root directory"
    )

def destroy():
    del bpy.types.Scene.VRT_paint_color_ui
    del bpy.types.ViewLayer.VRT_use_uv_grid
    del bpy.types.ViewLayer.VRT_use_color_grid
    bpy.utils.unregister_class(VRT_Section)
    del bpy.types.Scene.VRT_sections_list
    del bpy.types.Scene.VRT_sections_list_active_index
    del bpy.types.Scene.VRT_export_name
    del bpy.types.Scene.VRT_export_directory
    del bpy.types.Scene.VRT_export_variant


