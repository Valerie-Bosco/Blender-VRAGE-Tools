import bpy

from bpy.types  import PropertyGroup
from bpy.props      import (EnumProperty,
                            FloatProperty,
                            FloatVectorProperty,
                            IntProperty,
                            StringProperty,
                            BoolProperty,
                            PointerProperty,
                            CollectionProperty)


class VRT_Notification(PropertyGroup):
    """Holder for issue information"""

    timestamp: FloatProperty(
        subtype='TIME',
        unit='TIME'
    )

    issue_type: EnumProperty(
        name='Info Type',
        items=(
            ('INFO', 'INFO', ''),
            ('WARNING', 'WARNING', ''),
            ('ERROR', 'ERROR', '')
            ),
        default='INFO'
    )

    text: StringProperty()

    code: StringProperty()


class VRT_Text(PropertyGroup):
    """Holder for the various properties saved to the BLEND file"""

    def register():
        bpy.types.Text.vrt = PointerProperty(type=VRT_Text)

    def unregister():
        del bpy.types.Text.vrt

    version: IntProperty(
        default=0
    )

    # Notifications
    notifications: CollectionProperty(
        type=VRT_Notification
    )

    notification_index: IntProperty(
        default=0
    )

    notification_alert: BoolProperty(
        default=False
    )

    display_errors: BoolProperty(
        name="Display Errors",
        description="Toggles whether errors are visible in the VRT Notifications screen",
        default=True
    )

    display_warnings: BoolProperty(
        name="Display Warnings",
        description="Toggles whether warnings are visible in the VRT Notifications screen",
        default=True
    )

    display_infos: BoolProperty(
        name="Display Infos",
        description="Toggles whether infos are visible in the VRT Notifications screen",
        default=True
    )


def get_blend_data():

    if '.vrt-data' not in bpy.data.texts:
        data = bpy.data.texts.new('.vrt-data')
    else:
        data = bpy.data.texts['.vrt-data']

    return data