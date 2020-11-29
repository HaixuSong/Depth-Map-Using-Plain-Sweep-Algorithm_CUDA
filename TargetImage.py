from IPython.display import clear_output
import matplotlib.image as mpimg
from ImageABC import ImageABC, IP
import numpy as np
from collections.abc import Iterable


class TargetImage(ImageABC):
    # if image path given, load image
    # if groundTruthPath given, store the point cloud as numpy array
    def __init__(self, ep, cp, bound, ip=IP, path=None, groundTruthPath=None):
        super().__init__(ep, cp, bound, ip)

        if not path is None:
            self.path = path
            try:
                self.data = mpimg.imread(self.path)
            except:
                raise Exception("Can't read {} as an image.".format(self.path))

        if not groundTruthPath is None:
            self.pointCloud = TargetImage.readPlyFile(groundTruthPath)

    # read ply file
    # only read vertex and store them as numpy array
    @staticmethod
    def readPlyFile(groundTruthPath):
        res = []
        with open(groundTruthPath, "r") as file:
            count = 0
            # see if this is ply format
            for line in file:
                count += 1
                splitLine = line.split()
                if splitLine[0] == 'ply': break
                if count == 10:
                    raise Exception('File {} seems not like a normal ply file'.format(groundTruthPath))
            count = 0
            # read header, get vertex number
            for line in file:
                splitLine = line.split()
                if splitLine[0] == 'element' and splitLine[1] == 'vertex':
                    try:
                        count = float(splitLine[2])

                    except:
                        raise Exception("Can't read how many vertex.")
                if splitLine[0] == "end_header": break
            total = count
            # start reading data and put them in list
            for line in file:
                if count % 1000 == 0:
                    clear_output(wait=True)
                    print("Loading:\t{}%".format(round((total - count) / total * 100)), end='\r')
                count -= 1
                lineList = []
                for data in line.split():
                    lineList.append(float(data))
                res.append(lineList)
                if count == 0: break
        return np.array(res)

    # check and load InputImages
    # if loaded, it means this object is ready for fitting
    def load(self, iterable):
        if isinstance(iterable, Iterable):
            self.source = iterable
        else:
            raise Exception("Expected a list to be loaded.")
        # check if all element loaded is instance of ImageABC
        for _ in iterable:
            if not isinstance(_, ImageABC) and not _.data is None:
                raise Exception("Items should be InputImage type.")
        return

    # fitting the target using plane sweep algorithm
    def fit(self, similarityFunction="", depthRange=(0, 30), planes=100, windowSize=21):
        pass
        # check if each parameter is valid
        # check similarithFunction

        # check depth range
        if not(isinstance(depthRange, Iterable) and len(depthRange) == 2):
            raise Exception("{} is an invalid depthRange.".format(depthRange))
        if depthRange[0] > depthRange[1]: depthRange = (depthRange[1], depthRange[0])

        # check planes:
        if planes <= 10:
            raise Exception("Too few planes, try more.")

        # check windowSize
        if windowSize <= 0:
            raise Exception("Invalid window size, should be greater than 0.")
        if windowSize % 2 == 0:
            raise Exception("Window size should be an odd number.")
#     def getDepth(self, cord):


#     def showGroundTruth():


if __name__ == "__main__":
    print("Start Testing \n-----------------")
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

    cord = (-15.0744, -11.9719, -1.79769)
    targetImage = TargetImage(
        ep=ep_m, cp=cmpos_m, bound=bound_m,
        path="./data/0005.png",
        groundTruthPath="./data/fountain.ply")
    targetImage.drawProjection(cord)
