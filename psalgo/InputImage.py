from .ImageABC import ImageABC, IP
import matplotlib.image as mpimg
import numpy as np


class InputImage(ImageABC):
    def __init__(self, path, ep, cp, bound, ip=IP):
        super().__init__(ep, cp, bound, ip)
        self.path = path
        try:
            self.data = mpimg.imread(self.path)
        except:
            raise Exception("Can't read {} as an image.".format(self.path))



if __name__ == "__main__":
    print("Start Testing \n-----------------")
    # load internal parameters of camera
    ip = np.array([[2759.48, 0, 1520.69],
                   [0, 2764.16, 1006.81],
                   [0, 0, 1]])

    # load external parameters of camera
    ep_l = np.array([[0.994915, -0.100715, 0.00117536],
                     [-0.00462005, -0.0339759, 0.999412],
                     [-0.100616, -0.994335, -0.0342684]])
    ep_m = np.array([[0.962742, -0.270399, 0.00344709],
                     [-0.0160548, -0.0444283, 0.998884],
                     [-0.269944, -0.961723, -0.0471142]])
    ep_r = np.array([[0.890856, -0.454283, -0.00158434],
                     [-0.0211638, -0.0449857, 0.998763],
                     [-0.453793, -0.889721, -0.0496901]])

    # load camera positions
    cmpos_l = np.array([-15.8818, -3.15083, 0.0592619])
    cmpos_m = np.array([-14.1604, -3.32084, 0.0862032])
    cmpos_r = np.array([-12.404, -3.81315, 0.110559])

    # load picture resolution
    resolution = (3072, 2048)

    # load 3D bounds
    bound_l = ((-20.6108, -7.91985), (-21.9686, -8.77828), (-3.49947, 1.71626))
    bound_m = ((-20.9042, -9.85972), (-21.68, -8.77828), (-6.68267, 1.71626))
    bound_r = ((-21.0826, -12.6952), (-12.6362, -8.77828), (-3.82552, 1.67881))

    leftImage = InputImage("./data/0006.png", ep=ep_l, cp=cmpos_l, bound=bound_l)
    cord = (-15.0744, -11.9719, -1.79769)
    leftImage.drawProjection(cord)
