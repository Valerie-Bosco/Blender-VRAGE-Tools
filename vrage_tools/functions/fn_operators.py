import os
from pathlib import Path
import bpy
from ..utilities.easybpy import *

from ..preferences import get_preferences


def op_fix_vrage_project_materials(self, context):


    prefs = get_preferences()

    def compare_names(name: str, ref: str):
        if name == ref:
            return True
        if name[:-4] == ref:
            if name[-3:].isdigit():
                return True
        else:
            return False

    ##### Remove unused slots
    scene_objects = bpy.context.scene.objects
    for obj in scene_objects:
        if obj.type != "MESH":
            continue
        if obj.hide_viewport:
            continue
        if not obj.name in bpy.context.view_layer.objects:
            continue
        deselect_all_objects()
        select_object(obj)
        bpy.ops.object.material_slot_remove_unused()

    ##### Find material .blend
    asset_libraries = bpy.context.preferences.filepaths.asset_libraries
    material_library_name = prefs.project_asset_lib
    for asset_lib in asset_libraries:
        if asset_lib.name != material_library_name:
            continue

        library_path = Path(asset_lib.path)

        if not os.path.exists(library_path):
            self.report({'ERROR'}, message='Asset library path missing')
            return {'CANCELLED'}

        blend_files = [fp for fp in library_path.glob("**/*.blend") if fp.is_file()]

        if blend_files == []:
            self.report({'ERROR'}, message='Asset library empty')
            return {'CANCELLED'}

    ##### Append materials
    # Init list of material base names
    imported_material_names = []
    # Get a list of all materials in the current scene
    scene_materials = bpy.data.materials

    for blend_file in blend_files:
        with bpy.data.libraries.load(str(blend_file), assets_only=True, link=True) as (data_from, data_to):
            # Get a list of the materials in the external file
            external_materials = data_from.materials
            # Init list of materials to append
            materials_to_append = []
            # Go through all the materials in the current scene
            for scene_material in scene_materials:
                for external_material in external_materials:
                    if external_material in materials_to_append:
                            continue
                    if compare_names(scene_material.name,external_material):
                        # Add material name to list
                        materials_to_append.append(external_material)
            # Add the external material to the current scene
            for mat in materials_to_append:
                print(f"Appending {mat}")
                data_to.materials.append(mat)
            # Make names accessible outside of loop
            imported_material_names.append(materials_to_append)

    # ##### Rename materials
    # for imported_material in data_to.materials:
    # #    imported_material.asset_clear()
    #     for mat_name in imported_material_names:
    #         if compare_names(imported_material.name,mat_name):
    #             imported_material.name = mat_name

    ##### Replace materials
    # Go through all the objects in the current scene
    for obj in scene_objects:
        # Go through all the material slots of the object
        for index, material_slot in enumerate(obj.material_slots):
            # Get the material in the current material slot
            old_material = material_slot.material
            if old_material is None:
                continue
            new_material = None

            if old_material.name[:-4] in bpy.data.materials:
                new_material = old_material.name[:-4]
            else:
                new_material = old_material.name

            if new_material is not None:
                for mat in bpy.data.materials:
                    if mat.name == new_material:
                        obj.material_slots[index].material = mat
            # # Go through all imported materials
            # for imported_material in data_to.materials:
            #     # If the material names match, use the external material
            #     if compare_names(slot_material.name,imported_material.name):
            #         obj.material_slots[index].material = imported_material

    # Purge unused
    bpy.ops.outliner.orphans_purge(do_recursive=True)
    print("done")
    self.report({'INFO'}, message='Done')

def clean_names(objs):
     for obj in objs:
            # if not "Fracture_" in obj.name:
            #     continue
            if not obj.name[-4] == ".":
                continue
            if not obj.name[-3:].isdigit():
                continue

            init_name = obj.name
            new_name = obj.name[:-4]
            obj.name = new_name
            # sometimes just setting the name doesn't work if there is a hidden object in the scene with that name.
            # This addresses that problematic object directly and switches the names:
            if not obj.name == new_name:
                bpy.data.objects[new_name].name = init_name
                obj.name = new_name

def collision_custom_prop(self, context, selected_objs, active_obj) -> bool:

    # Get the names of all objects except the active one
    names = [obj.name for obj in selected_objs if obj != active_obj]
    # Clean names
    for i, name in enumerate(names):
        if not name[-4] == ".":
            continue
        if not name[-3:].isdigit():
                continue
        names[i] = name[:-4]
    # Check for duplicates
    if not len(names) == len(set(names)):
        return False
    # Combine the names into a single string
    combined_names = '|'.join(names)

    active_obj["ColliderMeshGroups"] = combined_names
    active_obj["group"] = combined_names
    return True

def export_variant_suffix(variant) -> str:
    match variant:
        case 'NON_FRACTURED':
            return ""
        case 'FRACTURED':
            return "_Fractured"
        case 'DEFORMED':
            return "_Deformed"

def export_variant_dir(variant) -> str:
    match variant:
        case 'NON_FRACTURED':
            return "NonFractured"
        case 'FRACTURED':
            return "Fractured"
        case 'DEFORMED':
            return "Deformed"

def export_lod_suffix(lod):
    if lod:
        return f"_LOD{lod}"
    else:
        return ""

def export_fbx_quick(filepath):
    bpy.ops.export_scene.fbx(
    filepath=filepath,
    check_existing=False,
    # Include
    use_selection=True,
    object_types={'EMPTY', 'MESH', 'ARMATURE', 'OTHER'},
    use_custom_props=True,
    # Transform
    apply_scale_options='FBX_SCALE_ALL',
    )

def export_gltf_physics_invoke():
    bpy.ops.export_scene.gltf(
            'INVOKE_DEFAULT',
            export_format = 'GLTF_SEPARATE',
            will_save_settings=False,
            use_selection=True,
            export_yup=True,
            export_gpu_instances=False,
            export_apply=False,
            export_texcoords=False,
            export_normals=False,
            export_materials='NONE',
            export_morph=False,
            export_skins=False,
            export_animations=False
            )

def export_gltf_physics_quick(filepath):
    bpy.ops.export_scene.gltf(
            filepath=filepath,
            export_format = 'GLTF_SEPARATE',
            will_save_settings=False,
            use_selection=True,
            export_yup=True,
            export_gpu_instances=False,
            export_apply=False,
            export_texcoords=False,
            export_normals=False,
            export_materials='NONE',
            export_morph=False,
            export_skins=False,
            export_animations=False
            )