'''Matrix utilities.'''

import numpy as np
from typing import List, Union

def scaleMatrix(scale: Union[float, List[float]]) -> np.ndarray:
    '''
    Scale matrix for scaling an object.

    :param scale: A scalar value for uniform scaling or a list of three values [sx, sy, sz] for non-uniform scaling.
    '''
    if np.isscalar(scale):
        scale = [scale, scale, scale]

    scale.append(1)
    return np.diag(scale)


def translationMatrix(t: List[float]) -> np.ndarray:
    '''
    Generates a translation matrix for moving an object.

    :param t: A list of translation values [tx, ty, tz].
    '''
    n = len(t)
    T = np.identity(n+1,dtype='f')
    T[:n,-1] = t
    return T


def rotationMatrixZ(angle: float) -> np.ndarray:
    '''
    Generates a rotation matrix for rotating an object around the Z axis.

    :param angle: Rotation angle.
    '''
    c = np.cos(angle)
    s = np.sin(angle)
    R = np.identity(4)
    R[0,0] = c
    R[0,1] = s
    R[1,0] = -s
    R[1,1] = c
    return R


def rotationMatrixX(angle: float) -> np.ndarray:
    '''
    Generates a rotation matrix for rotating an object around the X axis.

    :param angle: Rotation angle.
    '''
    c = np.cos(angle)
    s = np.sin(angle)
    R = np.identity(4)
    R[1,1] = c
    R[1,2] = s
    R[2,1] = -s
    R[2,2] = c
    return R


def rotationMatrixY(angle: float) -> np.ndarray:
    '''
    Generates a rotation matrix for rotating an object around the X axis.

    :param angle: Rotation angle.
    '''
    c = np.cos(angle)
    s = np.sin(angle)
    R = np.identity(4)
    R[0,0] = c
    R[0,2] = s
    R[2,0] = -s
    R[2,2] = c
    return R


def poseMatrix(position: List[float] = [0, 0, 0], orientation: float = 0, scale: Union[float, List[float]] = 1) -> np.ndarray:
    '''
    Returns a combined TRS matrix for the pose of a model.

    :param position: the position of the model
    :param orientation: the model orientation (for now assuming a rotation around the Z axis)
    :param scale: the model scale, either a scalar for isotropic scaling, or vector of scale factors
    :return: the 4x4 TRS matrix
    '''
    # apply the position and orientation of the object
    R = rotationMatrixZ(orientation)
    T = translationMatrix(position)

    # ... and the scale factor
    S = scaleMatrix(scale)
    return np.matmul(np.matmul(T,R),S)


def orthoMatrix(l: float, r: float, t: float, b: float, n: float, f: float) -> np.ndarray:
    '''
    Returns an orthographic projection matrix

    :param l: Left clip plane
    :param r: Right clip plane
    :param t: Top clip plane
    :param b: Bottom clip plane
    :param n: Near clip plane
    :param f: Far clip plane
    :return: A 4x4 orthographic projection matrix
    '''
    return np.array(
        [
        [2./(r-l),      0.,         0.,         (r+l)/(r-l) ],
        [0.,            -2./(t-b),   0.,         (t+b)/(t-b) ],
        [0.,            0.,         2./(f-n),  (f+n)/(f-n) ],
        [0.,            0.,         0.,         1.          ]
        ]
    )

def frustumMatrix(l: float, r: float, t: float, b: float, n: float, f: float) -> np.ndarray:
    '''
    Returns a frustum projection matrix (perspective projection).

    :param l: Left clip plane.
    :param r: Right clip plane.
    :param t: Top clip plane.
    :param b: Bottom clip plane.
    :param n: Near clip plane.
    :param f: Far clip plane.
    :return: A 4x4 frustum matrix.
    '''
    return np.array(
        [
            [ 2*n/(r-l),      0,          (r+l)/(r-l),    0 ],
            [ 0,              -2*n/(t-b),  (t+b)/(t-b),    0 ],
            [ 0,              0,          -(f+n)/(f-n),   -2*f*n/(f-n) ],
            [ 0,              0,          -1,             0 ]
            ]
    )


# Homogeneous coordinates helpers
def homog(v: List[float]) -> np.ndarray:
    '''
    Converts 3D vector to homogeneous coordinates.

    :param v: A 3D vector [x, y, z].
    '''
    return np.hstack([v,1])

def unhomog(vh: np.ndarray) -> np.ndarray:
    '''
    Converts 4D vector to 3D coordinates.

    :param vh: A 4D vector [x, y, z, w].
    '''
    return vh[:-1]/vh[-1]

def matmul(L):
    R = L[0]
    for M in L[1:]:
        R = np.matmul(R,M)
    return R
