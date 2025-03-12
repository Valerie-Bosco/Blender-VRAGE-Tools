import bpy

from .utilities.easybpy import *
from .functions.fn_operators import *
from .functions.fn_ui import refresh_ui
from .functions.fn_preferences import get_preferences

from bpy.types import Context, Operator

class VRT_OT_DummyOperator(Operator):
    bl_idname = "scene.vrt_do_nothing"
    bl_label = "Do Nothing"
    bl_description = "This operator does nothing"
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        return {'FINISHED'}

class VRT_OT_ReLinkProjectMaterials(Operator):
    bl_idname = "scene.vrt_relink_project_materials"
    bl_label = "Re-link VRage Project Materials"
    bl_description = "Link materials from asset library, delete unused materials slots and purge unused data"

    @classmethod
    def poll(cls, context):
        cls.poll_message_set("Asset library not set in add-on preferences")
        prefs = get_preferences()
        return (prefs.vrage_project_asset_lib != "")

    def execute(self, context):
        op_fix_vrage_project_materials(self, context)
        return {'FINISHED'}

class VRT_OT_ResetPaintColor(Operator):
    bl_idname = "scene.vrt_reset_paint_color"
    bl_label = "Reset Paint Color"
    bl_description = "Reset VRage material paint color to Default"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    def execute(self, context):
        context.scene.vrt.paint_color_ui = (0.5, 0.5, 0.5)
        return {'FINISHED'}

class VRT_OT_CleanNames(Operator):
    bl_idname = "scene.vrt_clean_names"
    bl_label = "Clean Names"
    bl_description = "Clean names of selected objects, removing .001, etc. suffix"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        objs = get_selected_objects()

        if len(objs) == 0:
            self.report({'WARNING'}, "Nothing selected")
            return {'CANCELLED'}

        clean_names(objs)

        return {'FINISHED'}


class VRT_OT_AddRigidBody(Operator):
    bl_idname = "scene.vrt_add_rigid_body"
    bl_label = "Add Rigid Body"
    bl_description = "Add preset rigid body to selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        objs = get_selected_objects()

        if len(objs) == 0:
            self.report({'WARNING'}, "Nothing selected")
            return {'CANCELLED'}

        for obj in objs:
            set_active_object(obj)

            # Add a rigid body physics type if not already present
            if not obj.rigid_body:
                bpy.ops.rigidbody.object_add()

            # Set the rigid body type to passive
            obj.rigid_body.type = 'PASSIVE'

        return {'FINISHED'}

class VRT_OT_ExportCollisions(Operator):
    bl_idname = "scene.vrt_export_collisions"
    bl_label = "Export Collisions"
    bl_description = "Clean selected object names, apply scale and open exporter dialogue with preset settings"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        cls.poll_message_set("MSFT_Physics module not installed")
        return ('MSFT_Physics' in context.preferences.addons.keys())

    def execute(self, context):
        objs = get_selected_objects()
        clean_names(objs) # remove duplicate suffixes

        # apply scale
        bpy.ops.object.transform_apply(
            location=False,
            rotation=False,
            scale=True,
            properties=True,
            isolate_users=True
            )

        # Invoke glTF export
        context.scene.msft_physics_exporter_props.enabled = True # Enable havok extention
        export_gltf_physics_invoke()
        return {'FINISHED'}

class VTR_OT_LinkCollisionsToFracture(Operator):
    bl_idname = "scene.vrt_link_collisions_to_fracture"
    bl_label = "Link Collisions to Fracture"
    bl_description = "Link selected colliders to active fracture object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_objs = get_selected_objects()
        active_obj = get_active_object()

        if len(selected_objs) < 2:
            self.report({'WARNING'}, "Select two or more objects")
            return {'CANCELLED'}

        success = collision_custom_prop(self, context, selected_objs, active_obj)
        if not success:
            self.report({'ERROR'}, "Some colliders share the same base name. Colliders must each have a unique base name")
            return {'CANCELLED'}
        refresh_ui(self, context)
        self.report({'INFO'}, "Done")
        return {'FINISHED'}

class VTR_OT_SelectLinkedCollisions(Operator):
    bl_idname = "scene.vrt_select_linked_fracture_collisions"
    bl_label = "Select Linked Collisions"
    bl_description = "Select colliders that are linked to active fracture object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = get_selected_objects()

        # check that 1 object is selected
        if not len(obj) == 1:
            self.report(type={'WARNING'}, message="Select one object")
            return {'CANCELLED'}
        obj = obj[0]

        # check that object has collision attribs
        if not 'group' in obj.keys():
            self.report(type={'WARNING'}, message="Object has no linked collisions")
            return {'CANCELLED'}

        deselect_all_objects()
        for coll in obj['group'].split("|"):
            # Find objects which share the same root name
            matching_objs = []
            for obj in context.view_layer.objects:
                # Name matches
                if obj.name == coll:
                    matching_objs.append(obj)
                # Name partially matches
                elif obj.name[:-4] == coll:
                    # make sure last 4 chars are duplicate suffix
                    if obj.name[-4] == "." and obj.name[-3:].isdigit():
                        matching_objs.append(obj)

            select_objects(matching_objs)
        return {'FINISHED'}

class VTR_OT_UnlinkCollisionsFractureCollisions(Operator):
    bl_idname = "scene.vrt_unlink_fracture_collisions"
    bl_label = "Unlink Collisions from Fracture"
    bl_description = "Unlink all colliders from active fracture object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        objs = get_selected_objects()
        for obj in objs:
            if 'group' in obj.keys():
                del obj['group']
            if 'ColliderMeshGroups' in obj.keys():
                del obj['ColliderMeshGroups']
        refresh_ui(self, context)
        return {'FINISHED'}


class VRT_OT_section_add(Operator):
    bl_idname = "scene.vrt_section_add"
    bl_label = "Add Section"
    bl_description = "Add a new section group to the scene"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    def execute(self, context):
        my_list = context.scene.vrt.sections_list
        active_index = context.scene.vrt.sections_list_active_index

        to_index = min(len(my_list), active_index + 1)

        my_list.add()
        my_list.move(len(my_list) - 1, to_index)
        context.scene.vrt.sections_list_active_index = to_index

        return {'FINISHED'}

class VRT_OT_section_remove(Operator):
    bl_idname = "scene.vrt_section_remove"
    bl_label = "Remove active Section"
    bl_description = "Delete the active section group from the scene"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    @classmethod
    def poll(cls, context):
        cls.poll_message_set('Scene has no section groups')
        return len(context.scene.vrt.sections_list) > 0

    def execute(self, context):
        my_list = context.scene.vrt.sections_list
        active_index = context.scene.vrt.sections_list_active_index

        section_name = my_list[active_index].name

        my_list.remove(active_index)
        to_index = min(active_index, len(my_list) - 1)
        context.scene.vrt.sections_list_active_index = to_index

        # If given section name is no longer in sections list
        if not section_name in [s.name for s in my_list]:
            scene_objs = context.scene.objects
            for obj in scene_objs:
                if not 'SECTION' in obj:
                    continue
                if obj['SECTION'] == section_name:
                    del obj['SECTION']

        refresh_ui(self, context)
        return {'FINISHED'}

class VRT_OT_Section_Assign(Operator):
    bl_idname = "object.vrt_section_assign"
    bl_label = "Assign"
    bl_description = "Assign the selected objects to the active section group"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    def execute(self, context):
        sections_list = bpy.context.scene.vrt.sections_list
        active_section_index = bpy.context.scene.vrt.sections_list_active_index

        if len(sections_list) == 0:
            self.report({'WARNING'},message="No active section group!")
            return {'CANCELLED'}

        objs = get_selected_objects()
        for obj in objs:
            obj['SECTION'] = sections_list[active_section_index].name

        refresh_ui(self, context)
        return {'FINISHED'}

class VRT_OT_Section_Remove(Operator):
    bl_idname = "object.vrt_section_remove"
    bl_label = "Remove"
    bl_description = "Remove the selected objects from the active section group"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    def execute(self, context):
        sections_list = bpy.context.scene.vrt.sections_list
        active_section_index = bpy.context.scene.vrt.sections_list_active_index

        objs = get_selected_objects()
        for obj in objs:
            if not 'SECTION' in obj:
                continue
            if obj['SECTION'] == sections_list[active_section_index].name:
                del obj['SECTION']

        refresh_ui(self, context)
        return {'FINISHED'}

class VRT_OT_Section_Select(Operator):
    bl_idname = "object.vrt_section_select"
    bl_label = "Select"
    bl_description = "Select all objects from the active section group"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    def execute(self, context):
        sections_list = bpy.context.scene.vrt.sections_list
        active_section_index = bpy.context.scene.vrt.sections_list_active_index

        objs = bpy.context.view_layer.objects
        for obj in objs:
            if not 'SECTION' in obj:
                continue
            if obj['SECTION'] == sections_list[active_section_index].name:
                select_object(obj)

        return {'FINISHED'}

class VRT_OT_Section_Deselect(Operator):
    bl_idname = "object.vrt_section_deselect"
    bl_label = "Deselect"
    bl_description = "Deselect all objects from the active section group"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    def execute(self, context):
        sections_list = bpy.context.scene.vrt.sections_list
        active_section_index = bpy.context.scene.vrt.sections_list_active_index

        objs = bpy.context.view_layer.objects
        for obj in objs:
            if not 'SECTION' in obj:
                continue
            if obj['SECTION'] == sections_list[active_section_index].name:
                deselect_object(obj)

        return {'FINISHED'}


class VRT_OT_QuickExport(Operator):
    bl_idname = "scene.vrt_quick_export"
    bl_label = "Quick Export"
    bl_description = "Export selected objects as this LOD directly into its variant folder under selected directory"
    bl_options = {'REGISTER', 'INTERNAL'}

    export_lod: bpy.props.IntProperty(name="LOD") # type: ignore

    @classmethod
    def poll(cls, context):
        name_set = bool(context.scene.VRT_export_name) # name not ""
        dir_set = bool(context.scene.vrt.export_directory) # path not ""
        if dir_set: # if path is not empty string, check that it's valid
            dir_set = os.path.exists(context.scene.vrt.export_directory)

        if not name_set:
            cls.poll_message_set("Model name not set")
        if not dir_set:
            cls.poll_message_set("Export directory is not valid")
        if not name_set and not dir_set:
            cls.poll_message_set("Model name and export directory is not valid")

        return name_set*dir_set

    # ivoke a confirmation popup
    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if not get_selected_objects():
            self.report(type={'WARNING'}, message="Select one or more objects")
            return {'CANCELLED'}

        name = context.scene.VRT_export_name
        dir = context.scene.vrt.export_directory
        var = context.scene.vrt.export_variant
        lod = self.export_lod

        subdir = export_variant_dir(var)
        filename = f"{name}{export_variant_suffix(var)}{export_lod_suffix(lod)}"
        os.makedirs(name=os.path.join(dir, subdir), exist_ok=True)

        filepath = os.path.join(dir, subdir, f"{filename}.fbx")
        export_fbx_quick(filepath)

        return {'FINISHED'}

class VRT_OT_QuickExportCollisions(Operator):
    bl_idname = "scene.vrt_quick_export_collisions"
    bl_label = "Export Collisions"
    bl_description = "Clean Fracture names, apply scale and export selected objects directly into its variant folder under selected directory"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        name_set = bool(context.scene.VRT_export_name) # name not ""
        dir_set = bool(context.scene.vrt.export_directory) # path not ""
        if dir_set: # if path is not empty string, check that it's valid
            dir_set = os.path.exists(context.scene.vrt.export_directory)
        physics_installed = ('MSFT_Physics' in context.preferences.addons.keys())

        poll_message = ""
        if not name_set:
            poll_message += "Model name not set. "
        if not dir_set:
            poll_message += "Export directory is not valid. "
        if not physics_installed:
            poll_message += "MSFT_Physics module not installed. "
        cls.poll_message_set(poll_message)

        return name_set*dir_set*physics_installed

    # ivoke a confirmation popup
    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        objs = get_selected_objects()
        if not objs:
            self.report(type={'WARNING'}, message="Select one or more objects")
            return {'CANCELLED'}
        clean_names(objs) # remove duplicate suffixes

        # apply scale
        bpy.ops.object.transform_apply(
            location=False,
            rotation=False,
            scale=True,
            properties=True,
            isolate_users=True
            )

        # Invoke glTF export
        context.scene.msft_physics_exporter_props.enabled = True # Enable havok extention

        name = context.scene.VRT_export_name
        dir = context.scene.vrt.export_directory
        var = context.scene.vrt.export_variant

        subdir = export_variant_dir(var)
        filename = f"{name}{export_variant_suffix(var)}"
        os.makedirs(name=os.path.join(dir, subdir), exist_ok=True)

        filepath = os.path.join(dir, subdir, f"{filename}_collision")
        export_gltf_physics_quick(filepath)
        return {'FINISHED'}