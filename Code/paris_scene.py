'''Contains code for Paris Olympic Opening Ceremony Scene.'''

import pygame
import numpy as np

# import the scene class
from cubeMap import FlattenCubeMap
from scene import Scene
from lightSource import LightSource
from blender import load_obj_file
from BaseModel import DrawModelFromMesh
from shaders import *
from ShadowMapping import *
from sphereModel import Sphere
from skyBox import *
from environmentMapping import *

class ParisScene(Scene):
    '''
    Paris 2024 Olympic Opening Scene Class
    '''
    def __init__(self):
        Scene.__init__(self)

        # Light Source
        self.light = LightSource(self, position=[0, 4., -3.])

        # Shaders
        self.shaders='phong'

        # Shadows
        self.shadows = ShadowMap(light=self.light)
        self.show_shadow_map = ShowTexture(self, self.shadows)

        # Skybox
        self.skybox = SkyBox(scene=self)

        self.show_light = DrawModelFromMesh(scene=self, M=poseMatrix(position=self.light.position, scale=0.2), mesh=Sphere(material=Material(Ka=[10,10,10])), shader=FlatShader())

        self.environment = EnvironmentMappingTexture(width=400, height=400)

        self.sphere = DrawModelFromMesh(scene=self, M=poseMatrix(), mesh=Sphere(), shader=EnvironmentShader(map=self.environment))

        # Animation
        self.parislogo_initial_translation = translationMatrix([-4, 9, -5.5])
        self.parislogo_initial_rotation = rotationMatrixY(np.radians(270))
        self.parislogo_initial_scale = scaleMatrix([0.5, 0.5, 0.5])

        # Models
        parislogo = load_obj_file('models/parislogo.obj')
        self.parislogo = DrawModelFromMesh(scene=self, M=np.matmul(self.parislogo_initial_translation, np.matmul(self.parislogo_initial_rotation, self.parislogo_initial_scale)), mesh=parislogo[0], shader=self.shaders)

        hedge = load_obj_file('models/hedgeTextured.obj')
        self.hedge = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([9.5, -10, 0]), np.matmul(rotationMatrixY(np.radians(90)), scaleMatrix([0.125, 0.025, 0.025]))), mesh=hedge[0], shader=self.shaders)             

        hedge2 = load_obj_file('models/hedgeTextured.obj')
        self.hedge2 = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-9.5, -10, 0]), np.matmul(rotationMatrixY(np.radians(90)), scaleMatrix([0.125, 0.025, 0.025]))), mesh=hedge[0], shader=self.shaders)             

        hedge3 = load_obj_file('models/hedgeTextured.obj')
        self.hedge3 = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-3.7, -10, -9.5]), np.matmul(rotationMatrixY(np.radians(0)), scaleMatrix([0.075, 0.025, 0.025]))), mesh=hedge[0], shader=self.shaders)             

        road = load_obj_file('models/road.obj')
        self.road = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([7, -10, 4]), np.matmul(rotationMatrixY(np.radians(131)), scaleMatrix([0.85, 0.85, 0.85]))), mesh=road[0], shader=self.shaders)             

        stand = load_obj_file('models/stand.obj')
        self.stand = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-1, -9.5, -1]), np.matmul(rotationMatrixY(np.radians(30)), scaleMatrix([1, 1, 1]))), mesh=stand[0], shader=self.shaders)             

        eiffeltower = load_obj_file('models/eiffeltower.obj')
        self.eiffeltower = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-3.4, -10, -5]), np.matmul(rotationMatrixY(np.radians(45)), scaleMatrix([0.28, 0.28, 0.28]))), mesh=eiffeltower[0], shader=EnvironmentShader(map=self.environment))             

        skateramp = load_obj_file('models/skateramp.obj')
        self.skateramp = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-6, -10, 4]), np.matmul(rotationMatrixY(np.radians(0)), scaleMatrix([0.1, 0.1, 0.1]))), mesh=skateramp[0], shader=self.shaders)             

        house = load_obj_file('models/house.obj')
        self.house = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([9.5, -10, -9.5]), np.matmul(rotationMatrixY(np.radians(270)), scaleMatrix([0.28, 0.28, 0.29]))), mesh=house[0], shader=self.shaders)             

        self.flattened_cube = FlattenCubeMap(scene=self, cube=self.environment)

        # Model Animations
        self.animation_active = False
        self.frame = 0

    def logo_animate(self):
        '''
        Paris logo animation which rotates it about Y-axis and oscillates vertically.
        '''
        # Increment frame count
        self.frame += 1

        # Animate rotation around Y-axis
        rotation_angle = np.radians(self.frame * 0.75)  # Adjust rotation speed as needed
        rotation_matrix = rotationMatrixY(rotation_angle)

        # Animate vertical oscillation
        oscillation_height = 0.5
        vertical_oscillation_speed = 0.005
        y_offset = oscillation_height * np.sin(self.frame * vertical_oscillation_speed)

        # Update the position, keeping the initial transformation
        translation_matrix = translationMatrix([0, y_offset, 0])  # Only animate the Y offset

        # Combine the initial transformations with the animation
        self.parislogo.M = np.matmul(
            self.parislogo_initial_translation,  # Initial position
            np.matmul(
                translation_matrix,  # Vertical animation
                np.matmul(rotation_matrix, self.parislogo_initial_scale)  # Rotation and scale
            )
        )

    def draw_shadow_map(self):
        '''
        Draws shadow map to handle occlusions and depth.
        '''
        # Clear scene and depth buffer to handle occlusions.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
    def draw_reflections(self):
        '''
        Draws skybox and models with reflections.
        '''
        self.skybox.draw()

        for model in self.models:
            model.draw()

    def draw(self, framebuffer=False):
        '''
        Draw all models in the scene
        
        :param framebuffer: Whether to render to a framebuffer.
        '''
        if self.animation_active == True:
            self.logo_animate()
        else:
            pass

        # first we need to clear the scene, we also clear the depth buffer to handle occlusions
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # when using a framebuffer, we do not update the camera to allow for arbitrary viewpoint.
        if not framebuffer:
            self.camera.update()

        # first, we draw the skybox
        self.skybox.draw()

        # render the shadows
        self.shadows.render(self)

        # when rendering the framebuffer we ignore the reflective object
        if not framebuffer:

            self.environment.update(self)

            self.parislogo.draw()
            self.hedge.draw()
            self.hedge2.draw()
            self.hedge3.draw()
            self.road.draw()
            self.stand.draw()
            self.eiffeltower.draw()
            self.skateramp.draw()
            self.house.draw()

            # if enabled, show flattened cube
            self.flattened_cube.draw()

            self.show_shadow_map.draw()

        # then we loop over all models in the list and draw them
        for model in self.models:
            model.draw()

        self.show_light.draw()

        # once we are done drawing, we display the scene
        # Note that here we use double buffering to avoid artefacts:
        # we draw on a different buffer than the one we display,
        # and flip the two buffers once we are done drawing.
        if not framebuffer:
            pygame.display.flip()

    def keyboard(self, event):
        '''
        Process additional keyboard events for this demo.
        '''
        Scene.keyboard(self, event)

        if event.key == pygame.K_c:
            if self.flattened_cube.visible:
                self.flattened_cube.visible = False
            else:
                print('--> showing cube map')
                self.flattened_cube.visible = True

        elif event.key == pygame.K_7:
            print('--> no face culling')
            glDisable(GL_CULL_FACE)

        elif event.key == pygame.K_8:
            print('--> glCullFace(GL_FRONT)')
            glEnable(GL_CULL_FACE)
            glCullFace(GL_FRONT)

        elif event.key == pygame.K_9:
            print('--> glCullFace(GL_BACK)')
            glEnable(GL_CULL_FACE)
            glCullFace(GL_BACK)

        elif event.key == pygame.K_BACKQUOTE:
            if glIsEnabled(GL_DEPTH_TEST):
                print('--> disable GL_DEPTH_TEST')
                glDisable(GL_DEPTH_TEST)
            else:
                print('--> enable GL_DEPTH_TEST')
                glEnable(GL_DEPTH_TEST)
        
        # Start animation when "S" is pressed, stop with "F"
        elif event.key == pygame.K_s:
            print('--> starting animation')
            self.animation_active = True

        elif event.key == pygame.K_f:
            print('--> stopping animation')
            self.animation_active = False

if __name__ == '__main__':
    scene = ParisScene()
    scene.run()