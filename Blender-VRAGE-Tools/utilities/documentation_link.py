import bpy
import webbrowser

from bpy.types              import Operator
from bpy.props              import StringProperty


class VRT_OT_DocuLink(Operator):
    """Opens the relevant Space Engineers Wiki page, containing more usage information and / or tutorials"""
    bl_idname = "wm.vrt_docu_link"
    bl_label = "Documentation Link"
    bl_options = {'REGISTER', 'UNDO'}

    section: StringProperty()

    page: StringProperty()

    code: StringProperty()

    url: StringProperty()


    def execute(self, context):

        if self.url == "":
            webbrowser.open("https://spaceengineers2.wiki.gg/wiki/Modding/" + self.section + self.page + self.code)
        else:
            webbrowser.open(self.url)

        return {'FINISHED'}


def display_docu_link(row, section="", page="", code="", url=""):
    """Pass it a row onto which the info-button should be placed"""

    col = row.column(align=True)
    link = col.operator('wm.docu_link', text="", icon='INFO')

    if section != "":
        link.section = section
    if page != "":
        link.page = page
    if code != "":
        link.code = code
    if url != "":
        link.url = url