import bpy

from bpy.types import AddonPreferences
from bpy.props import EnumProperty

from .functions.fn_preferences import *


class VRT_AddonPreferences(AddonPreferences):
    bl_idname = __package__

    vrage_project_asset_lib: EnumProperty(
        items= get_asset_library_name_list(),
        name="VRage Project Asset Library",
        description="Asset library containing materials, etc. for your VRage project",
        update=on_asset_lib_pref_update,
    ) # type: ignore

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.prop(self, "vrage_project_asset_lib", text="Project Asset Library")