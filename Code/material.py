'''Material and MaterialLibarry Class.'''

from typing import List, Optional

class Material:
    """
    Class to represent a material and its properties alongside an optional texture.
    """
    def __init__(
            self, 
            name: Optional[str] = None, 
            Ka: List[float] = [1.0, 1.0, 1.0], 
            Kd: List[float] = [1.0, 1.0, 1.0], 
            Ks: List[float] = [1.0, 1.0, 1.0],
            Ns: float = 10.0,
            texture: Optional["Texture"] = None,
        ) -> None:
        """
        Initialises the material.
        :param name: Material name.
        :param Ka: Ambient colour of material [R, G, B].
        :param Kd: Diffuse colour of material [R, G, B].
        :param Ks: Specular colour of material [R, G, B].
        :param Ns: Shininess coefficient.
        :param texture: Optional texture.
        """
        self.name = name
        self.Ka = Ka
        self.Kd = Kd
        self.Ks = Ks
        self.Ns = Ns
        self.texture = texture
        self.alpha = 1.0

class MaterialLibrary:
    """
    Material library class.
    """
    def __init__(self) -> None:
        """
        Initialise material library.
        """
        self.materials = []
        self.names = {}

    def add_material(self, material: Material) -> None:
        """
        Adds a material to the library.

        :param material: The material to add.
        """
        self.names[material.name] = len(self.materials)
        self.materials.append(material)
