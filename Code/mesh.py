'''Mesh Classes.'''

from material import Material
import numpy as np

from texture import Texture

from typing import Optional, List

class Mesh:
    '''
    Simple class to hold a mesh data.
    '''
    def __init__(self,
                 vertices: Optional[np.ndarray] = None, 
                 faces: Optional[np.ndarray] = None,
                 normals: Optional[np.ndarray] = None,
                 textureCoords: Optional[np.ndarray] = None, 
                  material: Material = Material()
                ):
        '''
        Initialises a mesh object.

        :param vertices: A numpy array containing all vertices
        :param faces: [optional] An int array containing the vertex indices for all faces.
        :param normals: [optional] An array of normal vectors, calculated from the faces if not provided.
        :param material: [optional] An object containing the material information for this object
        '''
        self.name = 'Unknown'
        self.vertices = vertices
        self.faces = faces
        self.material = material
        self.colors = None
        self.textureCoords = textureCoords
        self.textures = []
        self.tangents = None
        self.binormals = None

        if vertices is not None:
            print('Creating mesh')
            print('- {} vertices'.format(self.vertices.shape[0]))
            if faces is not None:
                print('- {} faces'.format(self.faces.shape[0]))

        if normals is None:
            if faces is None:
                print('(W) Warning: the current code only calculates normals using the face vector of indices, which was not provided here.')
            else:
                self.calculate_normals()
        else:
            self.normals = normals

        if material.texture is not None:
            self.textures.append(Texture(material.texture))
            #self.textures.append(Texture('lena.bmp'))


    def calculate_normals(self):
        '''
        Method to calculate normals from the mesh faces.

        Normals computer by:
        1. Calculating normal for each face using cross product of two vectors in the face.
        2. Averaging the normals for each vertex across the faces it belongs to.
        '''

        self.normals = np.zeros((self.vertices.shape[0], 3), dtype='f')
        if self.textureCoords is not None:
            self.tangents = np.zeros((self.vertices.shape[0], 3), dtype='f')
            self.binormals = np.zeros((self.vertices.shape[0], 3), dtype='f')

        for f in range(self.faces.shape[0]):
            # first calculate the face normal using the cross product of the triangle's sides
            a = self.vertices[self.faces[f, 1]] - self.vertices[self.faces[f, 0]]
            b = self.vertices[self.faces[f, 2]] - self.vertices[self.faces[f, 0]]
            face_normal = np.cross(a, b)

            # tangent
            if self.textureCoords is not None:
                txa = self.textureCoords[self.faces[f, 1], :] - self.textureCoords[self.faces[f, 0], :]
                txb = self.textureCoords[self.faces[f, 2], :] - self.textureCoords[self.faces[f, 2], :]
                face_tangent = txb[0]*a - txa[0]*b
                face_binormal = -txb[1]*a + txa[1]*b

            # blend normal on all 3 vertices
            for j in range(3):
                self.normals[self.faces[f, j], :] += face_normal
                if self.textureCoords is not None:
                    self.tangents[self.faces[f, j], :] += face_tangent
                    self.binormals[self.faces[f, j], :] += face_binormal

        # finally we need to normalize the vectors
        self.normals /= np.linalg.norm(self.normals, axis=1, keepdims=True)
        if self.textureCoords is not None:
            self.tangents /= np.linalg.norm(self.tangents, axis=1, keepdims=True)
            self.binormals /= np.linalg.norm(self.binormals, axis=1, keepdims=True)


class CubeMesh(Mesh):
    '''
    Class to represent a cube mesh, inherits from Mesh class.
    '''
    def __init__(self, texture: Optional[Texture] = None, inside: bool = False):
        '''
        Initialises cube mesh.

        :param texture: An optional texture to apply to the cube.
        :param inside: If True, the cube's faces are flipped (default: False).
        '''

        vertices = np.array([

            [-1.0, -1.0, -1.0],  # 0
            [+1.0, -1.0, -1.0],  # 1

            [-1.0, +1.0, -1.0],  # 2
            [+1.0, +1.0, -1.0],  # 3

            [-1.0, -1.0, +1.0],  # 4
            [-1.0, +1.0, +1.0],  # 5

            [+1.0, -1.0, +1.0],  # 6
            [+1.0, +1.0, +1.0]  # 7

        ], dtype='f')

        faces = np.array([

            # back
            [1, 0, 2],
            [1, 2, 3],

            # right
            [2, 0, 4],
            [2, 4, 5],

            # left
            [1, 3, 7],
            [1, 7, 6],

            # front
            [5, 4, 6],
            [5, 6, 7],

            # bottom
            [0, 1, 4],
            [4, 1, 6],

            # top
            [2, 5, 3],
            [5, 7, 3],

        ], dtype=np.uint32)

        if inside:
            faces = faces[:, np.argsort([0, 2, 1])]

        textureCoords = None # np.array([], dtype='f')

        Mesh.__init__(self, vertices=vertices, faces=faces, textureCoords=textureCoords)

        if texture is not None:
            self.textures = [
                texture
            ]
