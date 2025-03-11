import bpy

import mathutils




def refresh_ui(self, context):
    if context and context.screen:
            for a in context.screen.areas:
                a.tag_redraw()

def on_vrt_paintcolor_update(self, context):
    updated_color = context.scene.VRT_paint_color_ui
    bpy.context.view_layer['VRT_paint_color'] = tuple(mathutils.Vector(updated_color) - mathutils.Vector((0.5, 0.5, 0.5)))

def on_vrt_sections_list_update(self, context):
    print("sections changed")

def on_vrt_parallax_update(self, context):
     use_parallax = context.scene.VRT_use_parallax_ui
     bpy.context.view_layer['VRT_disable_parallax'] = bool(not use_parallax)




