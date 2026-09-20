"""
VRAGE Tools, Copyright 2025,
Keen Software House s.r.o., Na Petynce 213/23b, Břevnov, 169 00 Praha 6, Czech Republic, Company number: 05264561

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
(VRAGE Tools) distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from bpy.app.handlers import persistent

from .MSFT.MSFT_Physics import MSFT_Physics_register, MSFT_Physics_unregister
from .modules.ALXAddonUpdater.ALXAddonUpdater.ALX_AddonUpdater import Alx_Addon_Updater
from .modules.ALXModuleManager.ALXModuleManager.module_manager import (
    ALXModuleManager,
    SET_module_manager,
)
from .operators import *
from .view_layer.view_layer import *

bl_info = {
    "name": "Blender-VRAGE-Tools",
    "author": "Valerie Bosco[House Arhal], Keen Software House[Original Developer]",
    "description": "A Blender Add-on to streamline and simplify the creation of 3D assets for Space Engineers 2",
    "blender": (3, 6, 0),
    "version": (0, 4, 0),
    "location": "",
    "warning": "",
    "category": "Generic",
}

ALX_module_manager = ALXModuleManager(path=__path__, bl_info=bl_info, mute=False)
SET_module_manager(ALX_module_manager)

addon_updater = Alx_Addon_Updater(
    path=__path__,
    bl_info=bl_info,
    engine="Github",
    engine_user_name="Valerie-Bosco",
    engine_repo_name="XNALara-io-Tools",
    manual_download_website="https://github.com/Valerie-Bosco/XNALara-io-Tools/releases/tag/main_branch_latest",
)

from . import BVT_properties


def register():
    ALX_module_manager.register_modules()
    addon_updater.register_addon_updater(mute=True)

    MSFT_Physics_register()
    BVT_properties.register_properties()

    bpy.app.handlers.load_post.append(file_load_handler)


def unregister():
    ALX_module_manager.unregister_modules()
    addon_updater.unregister_addon_updater()

    MSFT_Physics_unregister()
    BVT_properties.unregister_properties()

    bpy.app.handlers.load_post.remove(file_load_handler)


# noinspection PyUnresolvedReferences
@persistent
def file_load_handler(dummy):
    bpy.ops.scene.vrt_section_repopulate_list(
        "INVOKE_DEFAULT",
    )
    bpy.context.scene.msft_physics_exporter_props.enabled = (
        False  # Disable havok extension. It can mess with glTF imports
    )
