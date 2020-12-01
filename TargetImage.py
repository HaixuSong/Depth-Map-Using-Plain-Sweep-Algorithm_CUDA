from IPython.display import clear_output
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from ImageABC import ImageABC, IP
import numpy as np
from collections.abc import Iterable
from simf import simFunc


class TargetImage(ImageABC):
    # if image path given, load image
    # if groundTruthPath given, store the point cloud as numpy array
    def __init__(self, ep, cp, bound, ip=IP, path=None, groundTruthPath=None, resolution=None):
        super().__init__(ep, cp, bound, ip)
        if resolution is not None: self.resolution = resolution
        if path is not None:
            self.path = path
            try:
                self.data = mpimg.imread(self.path)
                self.resolution = self.data.shape[0:2]
            except:
                raise Exception("Can't read {} as an image.".format(self.path))

        if not groundTruthPath is None:
            self.pointCloud, self.vertexCount = TargetImage.readPlyFile(groundTruthPath)

        if self.resolution is None: raise Exception("Please tell me the resolution.")

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
        return np.array(res), total

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
    def fit(self, similarityFunction="SSD", depthRange=(0, 30), planes=100, windowSize=21):
        pass
        # check if each parameter is valid
        # check similarithFunction
        if similarityFunction not in simFunc:
            raise Exception("Invalid similarity function. Should be on of {}.".format(simFunc.keys()))
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
        # finish checking input parameters

        # generate depth estimation space
        f = simFunc[similarityFunction]
        ip_i = np.linalg.inv(self.ip)
        ep_i = np.linalg.inv(self.ep)
        estimationSpace = np.ones(shape=(*self.resolution, planes)) * depthRange[1]
        for i in range(planes):
            clear_output(wait=True)
            print("Fitting:\t{}%\t{}/{}".format(round((i + 1)/planes * 100), i+1, planes))
            depth = depthRange[1] - (depthRange[1] - depthRange[0]) / planes * i
            for row in range(self.resolution[0]):
                print("row:{}".format(row), end='\r')
                for col in range(self.resolution[1]):
                    cord = np.array((col, row, 1)).reshape((3, 1))
                    cord = np.dot(ep_i, np.dot(ip_i, cord * depth)) + self.cp.reshape((3, 1))
                    res = f(cord, windowSize=windowSize, sourceList=self.source)
                    if res is None: continue
                    estimationSpace[row][col][i] = res

        # get argmin of the z axis
        depthIndex = estimationSpace.argmin(axis=2)
        depthMap = depthRange[1] - depthIndex * ((depthRange[1] - depthRange[0]) / planes)
        setattr(self, "fitted", depthMap)
        plt.imshow(getattr(self, "fitted"), cmap="viridis")

    # draw resultDepthMap
    def drawResultDepthMap(self):
        if hasattr(self, "fitted"):
            plt.imshow(getattr(self, "fitted"))
        else:
            raise Exception("Not fitted yet.")

    # lazy initialize groundTruthDepthMap
    # calculate using projMatrix.dot(wldCord.reshape(4,)), the third value represents depth
    def showGroundTruthDepthMap(self):
        if self.pointCloud is None: raise Exception("Can't get ground truth")
        if hasattr(self, "groundTruthDepthMap"):
            plt.imshow(getattr(self, "groundTruthDepthMap"), cmap='viridis')
            plt.colorbar()
            plt.show()
            return
        groundTruthDepthMap = np.ones(shape=self.resolution)*1000
        count = 0
        for point in self.pointCloud:
            count += 1
            if count % 1000 == 0:
                clear_output(wait=True)
                print("Processing:\t{}%\t{}/{}".format(round(count / self.vertexCount * 100), count, self.vertexCount))
            projection = np.dot(self.projMatrix, ImageABC.getHomoCord(point).reshape((4, 1))).reshape((3, ))
            depth = projection[2]
            pixCord = ImageABC.getCartCord(projection)
            x = round(pixCord[0])
            y = round(pixCord[1])
            if self.pixInBound((x, y)):
                groundTruthDepthMap[y][x] = min(depth, groundTruthDepthMap[y][x])
        groundTruthDepthMap[groundTruthDepthMap >= 1000] = -1
        groundTruthDepthMap[groundTruthDepthMap <= 0 ] = np.amax(groundTruthDepthMap) + 1
        setattr(self, "groundTruthDepthMap", groundTruthDepthMap)
        plt.imshow(groundTruthDepthMap, cmap='viridis')
        plt.colorbar()
        plt.show()


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
