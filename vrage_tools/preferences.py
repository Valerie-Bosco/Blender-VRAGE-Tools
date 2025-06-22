import bpy
import time

from bpy.types import AddonPreferences
from bpy.props import EnumProperty, StringProperty, BoolProperty, FloatProperty


def items_project_asset_lib(self, context):
    asset_libraries = [
        ('0', "None", "", 0, 0),
    ]
    i = 1
    for lib in bpy.context.preferences.filepaths.asset_libraries:
        asset_libraries.append(
            (lib.name, lib.name, "asset library", 0, i)
        )
        i += 1
    return asset_libraries

def update_project_asset_lib(self, context):
    updated = self.project_asset_lib


class VRT_AddonPreferences(AddonPreferences):
    bl_idname = __package__

    project_asset_lib: EnumProperty(
        items=items_project_asset_lib,
        name="VRAGE Project Asset Library",
        description="Asset library containing materials, etc. for your VRAGE project",
        update=update_project_asset_lib,
    ) # type: ignore

    # Update Checker
    addon_latest_version: StringProperty()
    addon_current_version: StringProperty()
    addon_needs_update: BoolProperty(
        default=False
    )
    addon_update_message: StringProperty()
    addon_last_check: FloatProperty(
        subtype='TIME',
        unit='TIME',
        default=0.0
    )
    addon_cache_releases: StringProperty()
    addon_cache_tags: StringProperty()


    def draw(self, context):
        preferences = get_preferences()
        layout = self.layout

        box = layout.box()
        row = box.row()
        row.label(text="Update Status", icon='FILE_REFRESH')

        col = row.column(align=True)
        row = col.row()
        row.alignment = 'RIGHT'

        row = row.row(align=True)
        op = row.operator('wm.vrt_get_current_version', text="Releases", icon='URL')

        row = box.row(align=True)
        row.scale_y = 2.0
        split = row.split(align=True)

        if preferences.addon_last_check != 0:
            if preferences.addon_needs_update:
                split.alert = True
                op = split.operator('wm.vrt_get_current_version', text=preferences.addon_update_message, icon='ERROR')
            else:
                op = split.operator('wm.vrt_get_current_version', text=preferences.addon_update_message, icon='CHECKMARK')
                split.enabled = False

            split = row.split(align=True)
            op = split.operator('wm.vrt_check_update', text="", icon='FILE_REFRESH')

            row = box.row(align=True)
            row.alignment = 'RIGHT'
            row.label(text= "Last check: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(preferences.addon_last_check)))

        else:
            op = split.operator('wm.vrt_check_update', icon='FILE_REFRESH')

        row = layout.row()
        row.prop(self, "project_asset_lib", text="Project Asset Library")


def get_preferences():
    """Returns the preferences of the addon"""
    return bpy.context.preferences.addons.get(__package__).preferences