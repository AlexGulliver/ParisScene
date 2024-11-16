'''Framebuffer Class.'''

from OpenGL.GL import *

from typing import Optional

class Framebuffer:
    '''
    Basic class to handle rendering to texture using a framebuffer object.
    '''

    def __init__(self, attachment: int = GL_COLOR_ATTACHMENT0, texture: Optional["Texture"] = None) -> None:
        '''
        Initialise the framebuffer

        :param attachment: Which output of the rendering process to save (GL_COLOR_ATTACHMENT0, GL_DEPTH_ATTACHMENT, ...)
        :param texture: (optional) if provided, link the framebuffer to the texture
        '''
        self.attachment = attachment
        self.fbo = glGenFramebuffers(1)

        if texture is not None:
            self.prepare(texture)

    def bind(self) -> None:
        '''
        Binds framebuffer.
        '''
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)

    def unbind(self) -> None:
        '''
        Unbinds framebuffer.
        '''
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def prepare(self, texture: "Texture", target: Optional[int] = None, level: int = 0) -> None:
        '''
        Prepare the Framebuffer by linking its output to a texture

        :param texture: The texture object to render to
        :param target: The target of the rendering, if not the default for the texture (use for cube maps)
        :param level: The mipmap level (ignore)
        '''
        if target is None:
            target = texture.target

        self.bind()
        glFramebufferTexture2D(GL_FRAMEBUFFER, self.attachment, target, texture.textureid, level)
        if self.attachment == GL_DEPTH_ATTACHMENT:
            glDrawBuffer(GL_NONE)
            glReadBuffer(GL_NONE)

        self.unbind()