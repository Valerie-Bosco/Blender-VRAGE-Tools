import bpy

def get_asset_library_name_list() -> list:
    asset_libraries = [
        ("", "None", "", 0, 0),
    ]
    i = 1
    for lib in bpy.context.preferences.filepaths.asset_libraries:
        asset_libraries.append(
            (lib.name, lib.name, "asset library", 0, i)
        )
        i += 1
    return asset_libraries

def on_asset_lib_pref_update(self, context):
    updated = self.vrage_project_asset_lib
    print(updated)

def get_preferences():
    """Returns the preferences of the addon"""

    if __package__.find(".") == -1:
        addon = __package__
    else:
        addon = __package__[:__package__.find(".")]

    return bpy.context.preferences.addons.get(addon).preferences