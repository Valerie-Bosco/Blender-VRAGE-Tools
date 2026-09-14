import bpy


class MSFTPhysicsSettingsViewportPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MSFT Physics"
    bl_label = "MSFT Physics"
    bl_idname = "OBJECT_PT_MSFT_Physics_Viewport_Extensions"

    @classmethod
    def poll(cls, context):
        if context.object and context.object.rigid_body:
            return True
        return None

    def draw(self, context):
        layout = self.layout

        if (context_scene := context.object) is not None:
            row = layout.row()
            row.prop(context_scene.msft_physics_scene_viewer_props, "draw_velocity")
            row = layout.row()
            row.prop(context_scene.msft_physics_scene_viewer_props, "draw_mass_props")


class MSFTPhysicsSettingsPanel(bpy.types.Panel):
    bl_label = "MSFT Physics Extensions"
    bl_idname = "OBJECT_PT_MSFT_Physics_Extensions"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "physics"

    @classmethod
    def poll(cls, context):
        if context.object and context.object.rigid_body:
            return True
        return None

    def draw(self, context):
        layout = self.layout

        if (context_object := context.object) is not None:
            row = layout.row()
            row.prop(context_object.msft_physics_extra_props, "is_trigger")
            row = layout.row()
            row.prop(context_object.msft_physics_extra_props, "gravity_factor")
            row = layout.row()
            row.prop(context_object.msft_physics_extra_props, "linear_velocity")
            row = layout.row()
            row.prop(context_object.msft_physics_extra_props, "angular_velocity")

            row = layout.row()
            row.prop(context_object.msft_physics_extra_props, "enable_inertia_override")
            row = layout.row()
            row.enabled = (
                context_object.msft_physics_extra_props.enable_inertia_override
            )
            row.prop(context_object.msft_physics_extra_props, "inertia_major_axis")
            row = layout.row()
            row.enabled = (
                context_object.msft_physics_extra_props.enable_inertia_override
            )
            row.prop(context_object.msft_physics_extra_props, "inertia_orientation")

            row = layout.row()
            row.prop(context_object.msft_physics_extra_props, "enable_com_override")
            row = layout.row()
            row.prop(context_object.msft_physics_extra_props, "center_of_mass")
            row.enabled = context_object.msft_physics_extra_props.enable_com_override

            row = layout.row()
            row.prop(context_object.msft_physics_extra_props, "friction_combine")
            row = layout.row()
            row.prop(context_object.msft_physics_extra_props, "restitution_combine")
