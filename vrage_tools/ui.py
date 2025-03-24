import bpy

from bpy.types import Panel

from .utilities.documentation_link import display_docu_link

class VRT_PT_Panel(Panel):
    bl_idname = 'VRT_PT_Panel'
    bl_label = 'VRAGE Tools'
    bl_category = 'VRAGE'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 0

    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout

        layout.operator('scene.vrt_relink_project_materials',text="Fix Project Materials", icon='MATERIAL')
        layout.operator("scene.vrt_clean_names", text="Clean Names", icon='SORTALPHA')

        layout.operator("wm.vrt_notification_display", icon='INFO')

class VRT_PT_Panel_subpanel_physics(Panel):
    bl_idname = 'VRT_PT_Panel_subpanel_physics'
    bl_label = "Physics"
    bl_parent_id = 'VRT_PT_Panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 0

    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout

        layout.operator("scene.vrt_add_rigid_body", text="Add Rigid Body", icon='PHYSICS')
        layout.operator('scene.vrt_export_collisions',text="Export Collisions", icon='EXPORT')
        layout.label(text="Fractures:")
        layout.operator('scene.vrt_link_collisions_to_fracture',        text="Link Collisions", icon='LINKED')
        layout.operator('scene.vrt_unlink_fracture_collisions',         text="Unlink Collisions", icon='UNLINKED')
        layout.operator('scene.vrt_select_linked_fracture_collisions',  text="Select Linked", icon='RESTRICT_SELECT_OFF')


class VRT_UL_sections(bpy.types.UIList): # List item class

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        layout.alignment = 'LEFT'
        row = layout.row()
        row.alignment = 'EXPAND'
        row.prop(item, "name", text="", emboss=False, icon='GROUP')

class VRT_PT_Panel_subpanel_sections(Panel):
    bl_idname = 'VRT_PT_Panel_subpanel_sections'
    bl_label = "Section Groups"
    bl_parent_id = 'VRT_PT_Panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 1

    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        list_owner_path, list_prop_name = "scene.vrt.sections_list".rsplit('.', 1)
        list_owner = context.path_resolve(list_owner_path)

        index_owner_path, index_prop_name = "scene.vrt.sections_list_active_index".rsplit('.', 1)
        index_owner = context.path_resolve(index_owner_path)

        layout = self.layout

        # Draw Collection list
        row = layout.row()
        row.template_list(
            "VRT_UL_sections",
            "my_list_id",
            list_owner, list_prop_name,
            index_owner, index_prop_name,
        )
        # Draw Collection list buttons
        col = row.column()
        props = col.operator("scene.vrt_section_add", text="", icon='ADD')

        row = col.row()
        # row.enabled = len(context.scene.vrt.sections_list) > 0
        props = row.operator("scene.vrt_section_remove", text="", icon='REMOVE')


        # Draw Section action buttons
        if len(context.scene.vrt.sections_list) > 0:
            row = layout.row()
            row_left = row.row(align=True)
            row_right = row.row(align=True)

            row_left.operator("object.vrt_section_assign")
            row_left.operator("object.vrt_section_remove")

            row_right.operator("object.vrt_section_select")
            row_right.operator("object.vrt_section_deselect")


class VRT_PT_Materials(Panel):
    bl_idname = 'VRT_PT_Materials'
    bl_label = 'Materials'
    bl_category = 'VRAGE'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 1

    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        row = layout.row(heading='', align=False)
        row.use_property_split = True
        row.alignment = 'EXPAND'
        row.prop(context.scene.vrt, 'paint_color_ui', text='Paint Color')
        row.operator('scene.vrt_reset_paint_color', text='', icon_value=715)

        layout.prop(context.scene.vrt, 'use_parallax_ui', text="Parallax")

class VRT_PT_Materials_subpanel_uv(Panel):

    bl_idname = 'VRT_PT_Materials_subpanel_uv'
    bl_label = ""
    bl_parent_id = 'VRT_PT_Materials'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 0

    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        layout = self.layout

        layout.prop(context.view_layer.vrt, 'use_uv_grid')

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=False, heading="")
        # row.enabled = context.view_layer['VRT_use_uv_grid']

        row.prop(context.view_layer.vrt, 'use_color_grid')


class VRT_PT_Export(Panel):
    bl_idname = 'VRT_PT_Export'
    bl_label = 'Quick Export'
    bl_category = 'VRAGE'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 2

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.alignment = 'EXPAND'
        col.prop(context.scene.vrt, "export_name", text="Name")
        col.separator()
        col.prop(context.scene.vrt, "export_directory", text="Directory")
        col.separator()
        col.prop(context.scene.vrt, "export_variant", text="Variant")

        layout.label(text="Quick Export:", icon='EXPORT')
        grid = layout.grid_flow(row_major=True, columns=2, even_columns=True, even_rows=True, align=True)
        op = grid.operator('scene.vrt_quick_export', text="LOD 0"); op.export_lod = 0
        op = grid.operator('scene.vrt_quick_export', text="LOD 1"); op.export_lod = 1
        op = grid.operator('scene.vrt_quick_export', text="LOD 2"); op.export_lod = 2
        op = grid.operator('scene.vrt_quick_export', text="LOD 3"); op.export_lod = 3
        op = grid.operator('scene.vrt_quick_export', text="LOD 4"); op.export_lod = 4
        grid.operator('scene.vrt_quick_export_collisions', text="Collision")