import bpy

from .interface import update_functions


# noinspection PyNoneFunctionAssignment
class VRT_Notification(bpy.types.PropertyGroup):
    """Holder for issue information"""

    module_manager_order = 1

    timestamp: bpy.props.FloatProperty(subtype="TIME", unit="TIME")  # type: ignore

    issue_type: bpy.props.EnumProperty(  # type: ignore
        name="Info Type",
        items=(
            ("INFO", "INFO", ""),
            ("WARNING", "WARNING", ""),
            ("ERROR", "ERROR", ""),
        ),
        default="INFO",
    )

    text: bpy.props.StringProperty()  # type: ignore

    code: bpy.props.StringProperty()  # type: ignore


# noinspection PyNoneFunctionAssignment
class VRT_Text(bpy.types.PropertyGroup):
    """Holder for the various properties saved to the BLEND file"""

    version: bpy.props.IntProperty(default=0)  # type: ignore

    notifications: bpy.props.CollectionProperty(type=VRT_Notification)  # type: ignore

    notification_index: bpy.props.IntProperty(default=0)  # type: ignore

    notification_alert: bpy.props.BoolProperty(default=False)  # type: ignore

    display_errors: bpy.props.BoolProperty(  # type: ignore
        name="Display Errors",
        description="Toggles whether errors are visible in the VRT Notifications screen",
        default=True,
    )

    display_warnings: bpy.props.BoolProperty(  # type: ignore
        name="Display Warnings",
        description="Toggles whether warnings are visible in the VRT Notifications screen",
        default=True,
    )

    display_infos: bpy.props.BoolProperty(  # type: ignore
        name="Display Infos",
        description="Toggles whether infos are visible in the VRT Notifications screen",
        default=True,
    )


# noinspection PyNoneFunctionAssignment
class BVT_Fracture(bpy.types.PropertyGroup):
    """Holder for VRT fracture properties"""

    module_manager_order = 1

    name: bpy.props.StringProperty(  # type: ignore
        name="Name", default="Fracture 1"
    )  # type: ignore
    group_id: bpy.props.StringProperty(  # type: ignore
        name="Group ID", default="fracture_01"
    )  # type: ignore


# noinspection PyNoneFunctionAssignment
class BVT_Section(bpy.types.PropertyGroup):
    """Holder for VRT section properties"""

    module_manager_order = 1

    def get_name(self):
        return self.get("name", "Section")

    def set_name(self, value):
        name_old = self.get("name", "Section")

        if (
            (context := bpy.context) is not None
            and (scene := context.scene) is not None
            and (scene_objects := scene.objects) is not None
        ):

            for obj in scene_objects:
                if not "SECTION" in obj:
                    continue
                if obj["SECTION"] == name_old:
                    obj["SECTION"] = value
            self["name"] = value

    name: bpy.props.StringProperty(  # type: ignore
        default="Section", get=get_name, set=set_name
    )  # type: ignore


# noinspection PyNoneFunctionAssignment
class BVT_ViewLayer(bpy.types.PropertyGroup):
    """Holder for VRT View Layer properties"""

    version: bpy.props.IntProperty(default=1)  # type: ignore

    use_uv_grid: bpy.props.BoolProperty(  # type: ignore
        name="Toggle UV Grid",
        description="Show VRAGE material UV Grid overlay",
        default=False,
    )

    use_color_grid: bpy.props.BoolProperty(  # type: ignore
        name="Toggle Color Grid",
        description="Show VRAGE material Color Grid overlay",
        default=False,
    )


class BVT_Scene(bpy.types.PropertyGroup):
    """Holder for VRT Scene properties"""

    export_name: bpy.props.StringProperty(
        name="Block Base Name",
        description='Base name of block to export (e.g. "CargoContainer")',
    )

    sections_list: bpy.props.CollectionProperty(type=BVT_Section)

    version: bpy.props.IntProperty(  # type: ignore
        default=1
    )  # type: ignore

    paint_color_ui: bpy.props.FloatVectorProperty(  # type: ignore
        name="Paint Color",
        description="Change display color of colorable VRAGE materials",
        size=3,
        default=(0.5, 0.5, 0.5),
        subtype="COLOR",
        soft_min=0.0,
        soft_max=1.0,
        step=3,
        precision=6,
        update=update_functions.update_paint_color_ui,
    )  # type: ignore

    use_parallax_ui: bpy.props.BoolProperty(  # type: ignore
        name="Toggle Parallax",
        description="Enable VRAGE material parallax occlusion mapping",
        default=True,
        update=update_functions.update_use_parallax_ui,
    )  # type: ignore

    fractures_list: bpy.props.CollectionProperty(type=BVT_Fracture)  # type: ignore

    fractures_list_active_index: bpy.props.IntProperty()  # type: ignore

    export_directory: bpy.props.StringProperty(  # type: ignore
        name="Quick Export Directory",
        description='Root directory for exporting model. (parent directory of "NonFractured", "Fractured"...)',
        subtype="DIR_PATH",
        update=update_functions.update_export_path_ui,
    )

    sections_list_active_index: bpy.props.IntProperty()  # type: ignore

    export_variant: bpy.props.EnumProperty(  # type: ignore
        items=[
            ("NON_FRACTURED", "Non-fractured", "Export as undamaged, base variant"),
            ("FRACTURED", "Fractured", "Export as fractured variant"),
            ("DEFORMED", "Deformed", "Export as deformed fractured variant"),
            (
                "NONE",
                "None",
                "Export directly into selected directory, without variant suffix",
            ),
        ],
        name="Export Variant",
        description="Variant of the block to export. Selects subdirectory in root directory",
    )

    export_limit: bpy.props.EnumProperty(  # type: ignore
        items=[
            ("SELECTED_OBJECTS", "Selected Objets", "Export only selected objects"),
            (
                "ACTIVE_COLLECTION",
                "Active Collection",
                "Export only the currently active collection",
            ),
            ("VISIBLE_OBJECTS", "Visible Objets", "Export all visible objects"),
        ],
        name="Limit to",
        description="Limit which objects to export",
    )  # type: ignore


def register_properties():
    bpy.types.Scene.vrt = bpy.props.PointerProperty(type=BVT_Scene)
    bpy.types.ViewLayer.vrt = bpy.props.PointerProperty(type=BVT_ViewLayer)
    bpy.types.Text.vrt = bpy.props.PointerProperty(type=VRT_Text)


def unregister_properties():
    del bpy.types.Text.vrt
    del bpy.types.ViewLayer.vrt
    del bpy.types.Scene.vrt
