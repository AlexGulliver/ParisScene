'''Texture Class to load texture files and store in OpenGL.'''

import pygame
from OpenGL.GL import *
import numpy as np


class ImageWrapper:
    def __init__(self, name: str) -> None:
        '''
        Load image from file using pyGame.

        :param name: Name of texture image file to be loaded.
        '''
        # load the image from file using pyGame - any other image reading function could be used here.
        print('Loading image: texture/{}'.format(name))
        self.img = pygame.image.load('./textures/{}'.format(name))

    def width(self) -> int:
        '''
        Returns width of loaded image.
        '''
        return self.img.get_width()

    def height(self) -> int:
        '''
        Returns width of loaded image.
        '''
        return self.img.get_height()

    def data(self, format: int = GL_RGB) -> bytes:
        '''
        Converts pygame image object to byte array for OpenGL use.

        :param format: The format of the texture data (GL_RGB or GL_RGBA).
        '''
        # convert the python image object to a plain byte array for passsing to OpenGL
        if format == GL_RGBA:
            return pygame.image.tostring(self.img, "RGBA", 1)
        elif format == GL_RGB:
            return pygame.image.tostring(self.img, "RGB", 1)


class Texture:
    '''
    Class to handle texture loading.
    '''
    def __init__(self, name: str, 
                 img: np.ndarray = None, 
                 wrap: int = GL_REPEAT, 
                 sample: int = GL_NEAREST, 
                 format: int = GL_RGBA, 
                 type: int = GL_UNSIGNED_BYTE, 
                 target: int = GL_TEXTURE_2D
                 ) -> None:
        '''
        Intialises a texture object and loads texture data in OpenGL.

        :param name: The texture file name.
        :param img: Optional numpy array with texture data. If None, image is loaded from file.
        :param wrap: The texture wrapping mode. Default is GL_REPEAT.
        :param sample: The texture sampling method. Default is GL_NEAREST.
        :param format: The internal format of the texture. Default is GL_RGBA.
        :param type: The data type of the texture. Default is GL_UNSIGNED_BYTE.
        :param target: The target texture type. Default is GL_TEXTURE_2D.
        '''
        self.name = name
        self.format = format
        self.type = type
        self.wrap = wrap
        self.sample = sample
        self.target = target

        self.textureid = glGenTextures(1)

        print('* Loading texture {} at ID {}'.format('./textures/{}'.format(name), self.textureid))

        self.bind()

        if img is None:
            img = ImageWrapper(name)

            # load the texture in the buffer
            glTexImage2D(self.target, 0, format, img.width(), img.height(), 0, format, type, img.data(format))
        else:
            # if a data array is provided use this
            glTexImage2D(self.target, 0, format, img.shape[0], img.shape[1], 0, format, type, img)


        # set what happens for texture coordinates outside [0,1]
        glTexParameteri(self.target, GL_TEXTURE_WRAP_S, wrap)
        glTexParameteri(self.target, GL_TEXTURE_WRAP_T, wrap)

        # set how sampling from the texture is done.
        glTexParameteri(self.target, GL_TEXTURE_MAG_FILTER, sample)
        glTexParameteri(self.target, GL_TEXTURE_MIN_FILTER, sample)

        self.unbind()

    def set_shadow_comparison(self) -> None:
        '''
        Sets shadow comparison mode for texture.
        '''
        self.set_parameter(GL_TEXTURE_COMPARE_MODE, GL_COMPARE_REF_TO_TEXTURE)

    def set_parameter(self, param: int, value: int) -> None:
        '''
        Sets texture parameter.

        :param param: Texture parameter.
        :param value: Value to assign to parameter.
        '''
        self.bind()
        glTexParameteri(self.target, param, value)
        self.unbind()

    def set_wrap_parameter(self, wrap: int = GL_REPEAT) -> None:
        '''
        Sets wrap mode for texture.

        :param wrap: Wrap mode (GL_REPEAT, GL_CLAMP_TO_EDGE)
        '''
        self.wrap = wrap
        self.bind()
        glTexParameteri(self.target, GL_TEXTURE_WRAP_S, wrap)
        glTexParameteri(self.target, GL_TEXTURE_WRAP_T, wrap)
        self.unbind()

    def set_sampling_parameter(self, sample: int = GL_NEAREST) -> None:
        '''
        Sets sampling method for texture.

        :param sample: Sampling method (GL_NEAREST, GL_LINEAR, etc.)
        '''
        self.sample = sample
        self.bind()
        glTexParameteri(self.target, GL_TEXTURE_MAG_FILTER, sample)
        glTexParameteri(self.target, GL_TEXTURE_MIN_FILTER, sample)
        self.unbind()

    def set_data_from_image(self, data: np.ndarray, width: int = None, height: int = None) -> None:
        '''
        Sets texture data from numpy array or image.

        :param data: Texture data.
        :param width: Optional width.
        :param height: Optional height.
        '''
        if isinstance(data, np.ndarray):
            width = data.shape[0]
            height = data.shape[1]

        self.bind()

        # load the texture in the buffer
        glTexImage2D(self.target, 0, self.format, width, height, 0, self.format, self.type, data)

        self.unbind()

    def bind(self) -> None:
        '''
        Binds texture to current OpenGL context.
        '''
        glBindTexture(self.target, self.textureid)

    def unbind(self) -> None:
        '''
        Unbinds texture from current OpenGL context.
        '''
        glBindTexture(self.target, 0)
