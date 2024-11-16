'''Skybox Class'''

from BaseModel import BaseModel, DrawModelFromMesh
from mesh import *
from matutils import *
from texture import *
from shaders import *
from cubeMap import CubeMap
import numpy as np

class SkyBoxShader(BaseShaderProgram):
    "Skybox Shader Class"
    def __init__(self, name: str = 'skybox') -> None:
        '''
        Intialises SkyBoxShader.

        :param name: Name of shader program.
        '''
        BaseShaderProgram.__init__(self, name=name)
        self.add_uniform('sampler_cube')

    def bind(self, model: 'BaseModel', M: np.ndarray) -> None:
        '''
        Binds shader program with current model's transformation matrix and projection-view matrix.

        :param model: Model to which shader is being applied.
        :param M: Transformation matrix of the model.
        '''
        BaseShaderProgram.bind(self, model, M)
        P = model.scene.P  # get projection matrix from the scene
        V = model.scene.camera.V  # get view matrix from the camera
        Vr = np.identity(4)
        Vr[:3, :3] = V[:3, :3]

        self.uniforms['PVM'].bind(np.matmul(P, np.matmul(V, M)))
        #self.uniforms['PVM'].bind(np.matmul(V, M))

class SkyBox(DrawModelFromMesh):
    "Skybox Class"
    def __init__(self, scene: 'Scene') -> None:
        '''
        Intialises SkyBox

        :param scene: Scene object.
        '''
        DrawModelFromMesh.__init__(self, scene=scene, M=poseMatrix(scale=10.0),
                                   mesh=CubeMesh(texture=CubeMap(name='skybox/paris'), inside=True),
                                   shader=SkyBoxShader(), name='skybox')

    def draw(self) -> None:
        '''
        Draws the skybox while disabling depth writes to ensure it is always rendered in the background.
        '''
        glDepthMask(GL_FALSE)
        DrawModelFromMesh.draw(self)
        glDepthMask(GL_TRUE)

