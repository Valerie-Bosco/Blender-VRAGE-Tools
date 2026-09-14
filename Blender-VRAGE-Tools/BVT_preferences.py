import bpy
from bpy.types import AddonPreferences

from .modules.ALXAddonUpdater.ALXAddonUpdater.ALX_AddonUpdaterUI import (
    update_settings_ui,
)


def items_project_asset_lib(self, context):
    asset_libraries = [
        ("0", "None", "", 0, 0),
    ]
    i = 1
    for lib in bpy.context.preferences.filepaths.asset_libraries:
        asset_libraries.append((lib.name, lib.name, "asset library", 0, i))
        i += 1
    return asset_libraries


def update_project_asset_lib(self, context):
    updated = self.project_asset_lib


# noinspection PyNoneFunctionAssignment
class VRT_AddonPreferences(AddonPreferences):
    bl_idname = __package__

    project_asset_lib: bpy.props.EnumProperty(  # type: ignore
        items=items_project_asset_lib,
        name="VRAGE Project Asset Library",
        description="Asset library containing materials, etc. for your VRAGE project",
        update=update_project_asset_lib,
    )  # type: ignore

    auto_check_update: bpy.props.BoolProperty(  # type: ignore
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=False,
    )

    updater_interval_months: bpy.props.IntProperty(  # type: ignore
        name="Months",
        description="Number of months between checking for updates",
        default=0,
        min=0,
    )  # type: ignore
    updater_interval_days: bpy.props.IntProperty(  # type: ignore
        name="Days",
        description="Number of days between checking for updates",
        default=7,
        min=0,
        max=31,
    )  # type: ignore
    updater_interval_hours: bpy.props.IntProperty(  # type: ignore
        name="Hours",
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23,
    )  # type: ignore
    updater_interval_minutes: bpy.props.IntProperty(  # type: ignore
        name="Minutes",
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59,
    )  # type: ignore

    def draw(self, context):
        layout = self.layout

        update_settings_ui(context, layout)

        row = layout.row()
        row.prop(self, "project_asset_lib", text="Project Asset Library")


def get_preferences():
    """Returns the preferences of the addon"""
    return bpy.context.preferences.addons.get(__package__).preferences
