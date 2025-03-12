# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "VRAGE Tools",
    "author" : "Keen Software House",
    "description" : "",
    "blender" : (4, 0, 0),
    "version" : (0, 1, 2),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}


import bpy

from .operators                 import *
from .preferences               import *
from .ui                        import *

from .scene.scene               import *
from .view_layer.view_layer     import *

classes = (
    VRT_AddonPreferences,

    VRT_PT_Panel,
    VRT_PT_Panel_subpanel_physics,
    VRT_UL_sections,
    VRT_PT_Panel_subpanel_sections,
    VRT_PT_Materials,
    VRT_PT_Export,

    VRT_Section,
    VRT_Scene,
    VRT_ViewLayer,

    VRT_OT_DummyOperator,
    VRT_OT_ReLinkProjectMaterials,
    VRT_OT_ResetPaintColor,
    VRT_OT_CleanNames,
    VRT_OT_AddRigidBody,
    VRT_OT_ExportCollisions,
    VTR_OT_LinkCollisionsToFracture,
    VTR_OT_SelectLinkedCollisions,
    VTR_OT_UnlinkCollisionsFractureCollisions,
    VRT_OT_section_add,
    VRT_OT_section_remove,
    VRT_OT_Section_Assign,
    VRT_OT_Section_Remove,
    VRT_OT_Section_Select,
    VRT_OT_Section_Deselect,
    VRT_OT_QuickExport,
    VRT_OT_QuickExportCollisions,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    VRT_Scene.register()
    VRT_ViewLayer.register()


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    VRT_Scene.unregister()
    VRT_ViewLayer.unregister()