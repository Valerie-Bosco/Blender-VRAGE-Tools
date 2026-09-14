import bpy

physics_material_combine_types = [
    ("AVERAGE", "Average", "", 0),
    ("MINIMUM", "Minimum", "", 1),
    ("MAXIMUM", "Maximum", "", 2),
    ("MULTIPLY", "Multiply", "", 3),
]


# noinspection PyNoneFunctionAssignment
class PG_MSFTPhysicsSceneAdditionalSettings(bpy.types.PropertyGroup):
    draw_velocity: bpy.props.BoolProperty(  # type: ignore
        name="Draw Velocities", default=False
    )
    draw_mass_props: bpy.props.BoolProperty(  # type: ignore
        name="Draw Mass Properties", default=False
    )


# noinspection PyNoneFunctionAssignment
class PG_MSFTPhysicsBodyAdditionalSettings(bpy.types.PropertyGroup):
    is_trigger: bpy.props.BoolProperty(name="Is Trigger", default=False)  # type: ignore
    gravity_factor: bpy.props.FloatProperty(  # type: ignore
        name="Gravity Factor", default=1.0
    )
    linear_velocity: bpy.props.FloatVectorProperty(  # type: ignore
        name="Linear Velocity", default=(0, 0, 0)
    )
    angular_velocity: bpy.props.FloatVectorProperty(  # type: ignore
        name="Angular Velocity", default=(0, 0, 0)
    )

    enable_inertia_override: bpy.props.BoolProperty(  # type: ignore
        name="Override Inertia Tensor", default=False
    )
    inertia_major_axis: bpy.props.FloatVectorProperty(  # type: ignore
        name="Inertia Major Axis", default=(1, 1, 1)
    )
    inertia_orientation: bpy.props.FloatVectorProperty(  # type: ignore
        name="Inertia Orientation", subtype="EULER"
    )

    enable_com_override: bpy.props.BoolProperty(  # type: ignore
        name="Override Center of Mass", default=False
    )
    center_of_mass: bpy.props.FloatVectorProperty(  # type: ignore
        name="Center of Mass", default=(0, 0, 0)
    )

    friction_combine: bpy.props.EnumProperty(  # type: ignore
        name="Friction Combine mode", items=physics_material_combine_types
    )
    restitution_combine: bpy.props.EnumProperty(  # type: ignore
        name="Restitution Combine mode",
        items=physics_material_combine_types,
    )


# noinspection PyNoneFunctionAssignment
class PG_MSFTPhysicsExporterProperties(bpy.types.PropertyGroup):
    enabled: bpy.props.BoolProperty(  # type: ignore
        name="VRAGE MSFT_Physics",
        description="Include rigid body data in the exported glTF file.",
        default=True,
    )


# noinspection PyNoneFunctionAssignment
class PG_MSFTPhysicsImporterProperties(bpy.types.PropertyGroup):
    enabled: bpy.props.BoolProperty(  # type: ignore
        name="VRAGE MSFT_Physics",  # bl_info['name'],
        description="Include rigid body data from the imported glTF file.",
        default=True,
    )
