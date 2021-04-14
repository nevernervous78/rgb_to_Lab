__author__ = "Danielo Pelliccia"
__copyright__ = "Copyright 2020, Rubens Technologies"

__license__ = "MIT"
__version__ = "0.0.1"

import numpy as np

def rgb2lab(R,G,B,C):

    # Normalise values
    r = R/C
    g = G/C
    b = B/C

    # Convert to XYZ. Need to decide what RGB we are using
    # http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html

    # sRGB
    M = np.array([[0.4360747,  0.3850649,  0.1430804], \
                 [0.2225045,  0.7168786,  0.0606169], \
                 [0.0139322,  0.0971045,  0.7141733]])

    rgb = np.array([r,g,b])

    XYZ = np.dot(M,rgb)*100

    X = XYZ[0]
    Y = XYZ[1]
    Z = XYZ[2]

    # Convert to CIE LAB
    # https://en.wikipedia.org/wiki/CIELAB_color_space
    # CIE XYZ tristimulus for D50 illuminant
    Xn = 96.4242
    Yn = 100.
    Zn = 82.5188

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

# Input the raw data reading of our sensor
R = 18628
G = 31805
B = 16424
C = 65535
L,a,b = rgb2lab(R,G,B,C)
print(L, a, b)
