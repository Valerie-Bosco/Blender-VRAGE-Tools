import bpy

from bpy.types import AddonPreferences
from bpy.props import EnumProperty


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
    print(updated)


class VRT_AddonPreferences(AddonPreferences):
    bl_idname = __package__

    project_asset_lib: EnumProperty(
        items=items_project_asset_lib,
        name="VRage Project Asset Library",
        description="Asset library containing materials, etc. for your VRage project",
        update=update_project_asset_lib,
    ) # type: ignore

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.prop(self, "project_asset_lib", text="Project Asset Library")

def get_preferences():
    """Returns the preferences of the addon"""
    return bpy.context.preferences.addons.get(__package__).preferences