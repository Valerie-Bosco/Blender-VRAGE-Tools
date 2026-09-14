import os

import mathutils


def update_paint_color_ui(self, context):
    updated_color = context.scene.vrt.paint_color_ui
    context.view_layer["VRT_paint_color"] = tuple(
        mathutils.Vector(updated_color) - mathutils.Vector((0.5, 0.5, 0.5))
    )


def update_use_parallax_ui(self, context):
    use_parallax = context.scene.vrt.use_parallax_ui
    context.view_layer["VRT_disable_parallax"] = bool(not use_parallax)


def update_export_path_ui(self, context):
    context.scene.vrt.export_directory = os.path.abspath(
        context.scene.vrt.export_directory
    )
