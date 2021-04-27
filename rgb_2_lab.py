__author__ = "Daniele Pelliccia"
__copyright__ = "Copyright 2020, Rubens Technologies"

__license__ = "MIT"
__version__ = "0.0.1"

import numpy as np

def rgb2lab(R,G,B,C, illuminant='D50'):

    # Normalise values
    r = R/C
    g = G/C
    b = B/C

    # Linearise RGB values
    rgb = np.array([r,g,b])
    for i,j in enumerate(rgb):
        if j > 0.04045 :
            rgb[i] = ( ( j + 0.055 ) / 1.055 ) ** 2.4
        else :
            rgb[i] = j / 12.92

    # Convert to XYZ. Need to decide what RGB we are using
    # http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html
    # https://en.wikipedia.org/wiki/CIELAB_color_space

    if illuminant == 'D50':
        # sRGB
        M = np.array([[0.4360747,  0.3850649,  0.1430804], \
                     [0.2225045,  0.7168786,  0.0606169], \
                     [0.0139322,  0.0971045,  0.7141733]])
        Xn = 96.4242
        Yn = 100.
        Zn = 82.5188
    elif illuminant == 'D65':
        M = np.array([[0.4124564,  0.3575761,  0.1804375], \
                      [0.2126729,  0.7151522,  0.0721750], \
                      [0.0193339,  0.1191920,  0.9503041]])
        # D65 illuminant
        Xn = 95.0489
        Yn = 100.
        Zn = 108.5188
    else:
        print("Error. 'D50' or 'D65' are the only allowed values for illuminant.")
        return

    XYZ = np.dot(M,rgb)*100

    X = XYZ[0]
    Y = XYZ[1]
    Z = XYZ[2]

    def f(t):
        delta = 6./29
        if (t>delta**3):
            value = t**(1/3)
        else:
            value = t/(3*delta**2) + 4/29
        return value

    # Finally convert to Lab
    L = 116*f(Y/Yn) - 16
    a = 500*(f(X/Xn)-f(Y/Yn))
    b = 200*(f(Y/Yn)-f(Z/Zn))

    return (L,a,b)
