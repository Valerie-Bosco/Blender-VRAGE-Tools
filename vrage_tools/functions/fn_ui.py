import bpy
import mathutils


def refresh_ui(self, context):
    if context and context.screen:
            for a in context.screen.areas:
                a.tag_redraw()