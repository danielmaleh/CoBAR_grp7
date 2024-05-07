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
            {'color': (0.8, 0.0, 0.0, 0.2), 'texture': 'checker'},
            {'color': (0.0, 0.8, 0.0, 0.2), 'texture': 'checker'}
        )
    ):
        super().__init__(size=size, friction=friction, ground_alpha=ground_alpha, scale_bar_pos=scale_bar_pos)
        
        # Create two tilted planes with custom materials and angles
        self.create_tilted_plane('plane1', plane_angles[0], size, plane_materials[0], pos=[25.0, 0.0, 0.1])
        self.create_tilted_plane('plane2', plane_angles[1], size, plane_materials[1], pos=[-25.0, 0.0, 0.1])

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