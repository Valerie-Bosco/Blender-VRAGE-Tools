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

from .operators                     import *
from .preferences                   import *
from .ui                            import *

from .scene.scene                   import *
from .view_layer.view_layer         import *
from .text.text                     import *
from .utilities.documentation_link  import *
from .utilities.notifications       import *

# imports for MSFT_Physics module
from .utilities.MSFT_Physics        import (MSFTPhysicsExporterProperties, 
                                            MSFTPhysicsImporterProperties,
                                            MSFTPhysicsSceneAdditionalSettings,
                                            MSFTPhysicsBodyAdditionalSettings,
                                            )
from io_scene_gltf2 import exporter_extension_layout_draw

classes = (
    # VRAGE Tools classes
    VRT_AddonPreferences,

    VRT_PT_Panel,
    VRT_PT_Panel_subpanel_physics,
    VRT_UL_sections,
    VRT_PT_Panel_subpanel_sections,
    VRT_MT_Menu_subpanel_sections_more_options,
    VRT_PT_Materials,
    VRT_PT_Export,

    VRT_Section,
    VRT_Scene,
    VRT_ViewLayer,
    VRT_Notification,
    VRT_Text,

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
    VRT_OT_Section_Repopulate_List,
    VRT_OT_QuickExport,
    VRT_OT_QuickExportCollisions,
    VRT_OT_DocuLink,
    VRT_OT_NotificationDisplay,
    VRT_OT_DeleteNotification,
    VRT_OT_ClearnNotification,

    # MSFT_Physics classes
    MSFTPhysicsExporterProperties, 
    MSFTPhysicsImporterProperties,
    MSFTPhysicsSceneAdditionalSettings,
    MSFTPhysicsBodyAdditionalSettings,
)


def draw_export(context, layout):
    exportProps = bpy.context.scene.msft_physics_exporter_props
    # header, body = layout.panel(
    #     "VRT_Havok_physics_exporter", default_closed=False
    # )
    layout.use_property_split = False
    layout.prop(exportProps, "enabled")
    layout.active = exportProps.enabled


def draw_import(context, layout):
    importProps = bpy.context.scene.msft_physics_importer_props
    # header, body = layout.panel(
    #     "VRT_Havok_physics_importer", default_closed=False
    # )
    layout.use_property_split = False
    layout.prop(importProps, "enabled")
    layout.active = importProps.enabled



def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # VRAGE Tools
    bpy.types.Scene.vrt = PointerProperty(type=VRT_Scene)
    bpy.types.ViewLayer.vrt = PointerProperty(type=VRT_ViewLayer)
    bpy.types.Text.vrt = PointerProperty(type=VRT_Text)
    
    # MSFT_Physics
    bpy.types.Scene.msft_physics_exporter_props = bpy.props.PointerProperty(type=MSFTPhysicsExporterProperties)
    bpy.types.Scene.msft_physics_importer_props = bpy.props.PointerProperty(type=MSFTPhysicsImporterProperties)
    bpy.types.Scene.msft_physics_scene_viewer_props = bpy.props.PointerProperty(type=MSFTPhysicsSceneAdditionalSettings)
    bpy.types.Object.msft_physics_extra_props = bpy.props.PointerProperty(type=MSFTPhysicsBodyAdditionalSettings)
    exporter_extension_layout_draw['MSFT_Physics'] = draw_export

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    # VRAGE Tools properties
    del bpy.types.Scene.vrt
    del bpy.types.ViewLayer.vrt
    del bpy.types.Text.vrt
    
    # MSFT_Physics
    del bpy.types.Scene.msft_physics_exporter_props
    del bpy.types.Scene.msft_physics_scene_viewer_props
    del bpy.types.Object.msft_physics_extra_props
    del exporter_extension_layout_draw['MSFT_Physics']

# glTF extension is created after register()/unregister() definitions
from .utilities.MSFT_Physics import *