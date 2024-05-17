class FlatTerrain(BaseArena):
    """Flat terrain with no obstacles.

    Attributes
    ----------
    root_element : mjcf.RootElement
        The root MJCF element of the arena.
    friction : Tuple[float, float, float]
        The sliding, torsional, and rolling friction coefficients of the
        ground, by default (1, 0.005, 0.0001).

    Parameters
    ----------
    size : Tuple[float, float], optional
        The size of the arena in mm, by default (50, 50).
    friction : Tuple[float, float, float]
        The sliding, torsional, and rolling friction coefficients of the
        ground, by default (1, 0.005, 0.0001).
    ground_alpha : float
        Opacity of the ground, by default 1 (fully opaque).
    scale_bar_pos : Tuple[float, float, float], optional
        If supplied, a 1 mm scale bar will be placed at this location.
    """

    def __init__(
        self,
        size: Tuple[float, float] = (100, 100),
        friction: Tuple[float, float, float] = (1, 0.005, 0.0001),
        ground_alpha: float = 1.0,
        scale_bar_pos: Optional[Tuple[float, float, float]] = None,
    ):
        super().__init__()

        ground_size = [*size, 1]
        chequered = self.root_element.asset.add(
            "texture",
            type="2d",
            builtin="checker",
            width=300,
            height=300,
            rgb1=(0.3, 0.3, 0.3),
            rgb2=(0.4, 0.4, 0.4),
        )
        grid = self.root_element.asset.add(
            "material",
            name="grid",
            texture=chequered,
            texrepeat=(10, 10),
            reflectance=0.1,
            rgba=(1.0, 1.0, 1.0, ground_alpha),
        )
        self.root_element.worldbody.add(
            "geom",
            type="plane",
            name="ground",
            material=grid,
            size=ground_size,
            friction=friction,
        )

        self.friction = friction
        if scale_bar_pos:
            self.root_element.worldbody.add(
                "geom",
                type="cylinder",
                size=(0.05, 0.5),
                pos=scale_bar_pos,
                rgba=(0, 0, 0, 1),
                euler=(0, np.pi / 2, 0),
            )

    def get_spawn_position(
        self, rel_pos: np.ndarray, rel_angle: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        return rel_pos, rel_angle
    


class ObstacleArenaGrp7(FlatTerrain):
    def __init__(
        self,
        size: Tuple[float, float] = (100, 100),
        friction: Tuple[float, float, float] = (1, 0.005, 0.0001),
        ground_alpha: float = 1.0,
        scale_bar_pos: Optional[Tuple[float, float, float]] = None,
        plane_angles: Tuple[Dict[str, float], Dict[str, float]] = (
            {'x_angle': np.pi / 4, 'y_angle': np.pi / 3},  # Plane 1 tilt angles around X and Y
            {'x_angle': -np.pi / 4, 'y_angle': np.pi / 3}  # Plane 2 tilt angles around X and Y
        ),
        plane_materials: Tuple[Dict[str, Any], Dict[str, Any]] = (
            {'color': (0.8, 0.0, 0.0, 1.0), 'texture': 'checker'},
            {'color': (0.0, 0.8, 0.0, 0.2), 'texture': 'checker'}
        )
    ):
        super().__init__(size=size, friction=friction, ground_alpha=ground_alpha, scale_bar_pos=scale_bar_pos)

        chequered = self.root_element.find('texture', 'checker')
        ground_size = [*size, 1]

        grid_micha = self.root_element.asset.add(
            "material",
            name="grid_micha",
            texture=chequered,
            texrepeat=(10, 10),
            reflectance=0.1,
            rgba=(1.0, 0.0, 0.0, ground_alpha),
        )
        self.root_element.worldbody.add(
            "geom",
            type="plane",
            name="ground2",
            material=grid_micha,
            size=ground_size,
            friction=friction,
            pos = [0, 10, 0],
            euler = [90, 0, 0]
        )
        
        # # Create two tilted planes with custom materials and angles
        # self.create_tilted_plane('plane1', plane_angles[0], size, plane_materials[0], pos=[0.0, 0.0, 0.0])
        # self.create_tilted_plane('plane2', plane_angles[1], size, plane_materials[1], pos=[-25.0, 0.0, 0.1])

        # # Create material
        # material = self.root_element.asset.add(
        #     "material",
        #     name=f"material_plane_micha",
        #     texture=self.root_element.asset.find('texture', plane_materials[0].get('texture', 'checker')),
        #     texrepeat=(10, 10),
        #     rgba=plane_materials[0].get('color')
        # )

        # # Add the tilted plane to the world body
        # self.root_element.worldbody.add(
        #     "geom",
        #     type="plane",
        #     name='plane_micha',
        #     material=material,
        #     size=[*size, 1],  # The third size value is ignored for planes in MJCF
        #     pos=[0, 0, 20],
        #     euler=[45,0,0],
        #     friction=self.friction
        # )

    def create_tilted_plane(
        self,
        name: str,
        angles: Dict[str, float],
        size: Tuple[float, float],
        material_props: Dict[str, Any],
        pos: List[float] = None,
    ):
        pos = pos  # Slightly above the flat ground
        euler = [angles['x_angle'], angles['y_angle'], 0]  # Rotation around X and Y axes
        
        # Create material
        material = self.root_element.asset.add(
            "material",
            name=f"material_{name}",
            texture=self.root_element.asset.find('texture', material_props.get('texture', 'checker')),
            texrepeat=(10, 10),
            rgba=material_props.get('color', (1, 1, 1, 1))
        )
        
        # Add the tilted plane to the world body
        self.root_element.worldbody.add(
            "geom",
            type="plane",
            name=name,
            material=material,
            size=[*size, 1],  # The third size value is ignored for planes in MJCF
            pos=pos,
            euler=euler,
            friction=self.friction
        )

# # Example usage
# arena = ObstacleArenaGrp7(
#     plane_angles=(
#         {'x_angle': 0.1, 'y_angle': 0.2},
#         {'x_angle': 0.3, 'y_angle': 0.4}
#     ),
#     plane_materials=(
#         {'color': (0.8, 0.3, 0.3, 0.1), 'texture': 'checker'},
#         {'color': (0.3, 0.3, 0.8, 0.3), 'texture': 'checker'}
#     )
# )