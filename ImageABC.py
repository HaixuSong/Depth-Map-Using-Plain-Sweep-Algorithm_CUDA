import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Circle
from collections.abc import Iterable
from abc import ABCMeta, abstractmethod

IP = np.array([[2759.48, 0, 1520.69],
               [0, 2764.16, 1006.81],
               [0, 0, 1]])


class ImageABC(metaclass=ABCMeta):
    # initiate an instance with picture path, external parameters, internal parameters, camera positions and bounds
    # all input parameters will turn into numpy arrays
    # raise exception when path or shape is not correct
    @abstractmethod
    def __init__(self, ep, cp, bound, ip=IP):
        self.ep = ImageABC.typeChange(ep, (3, 3))
        self.cp = ImageABC.typeChange(cp, (1, 3))
        self.bound = ImageABC.typeChange(bound, (3, 2))
        self.ip = ImageABC.typeChange(ip, (3, 3))
        self.projMatrix = np.dot(self.ip, np.hstack((self.ep, -np.dot(self.ep, self.cp.reshape((3, 1))))))
        self.data = None

    # input vector as Cartesian coordinate
    # return homogeneous coordinates
    # vect: np.array
    @staticmethod
    def getHomoCord(vect):
        if len(vect.shape) == 1: return np.hstack((vect, [1]))
        if len(vect.shape) == 2 and vect.shape[1] == 1: return np.vstack((vect, [[1]]))
        raise ValueError("function getHomoCord must have an input with shape (n,) or (n, 1)")

    # input vector is homogeneous coordinate
    # return Cartesian coordinate
    # vect: np.array
    @staticmethod
    def getCartCord(vect):
        if len(vect.shape) == 1:
            res, div = np.split(vect, [vect.shape[0] - 1])
            return res / div[0]
        if len(vect.shape) == 2 and vect.shape[1] == 1:
            res, div = np.split(vect, [vect.shape[0] - 1])
            return res / div[0][0]
        raise ValueError("function getCardCord must have an input with shape (n,) or (n, 1)")

        # change input iterable data into nparray with shape

    # if not iterable or can't change into shape, raise exception
    @staticmethod
    def typeChange(iterable, shape):
        if isinstance(iterable, Iterable):
            res = np.array(iterable)
        else:
            raise Exception('Input should be iterable. \n{} is not iterable.'.format(iterable))
        try:
            return res.reshape(shape)
        except:
            raise Exception('Invalid input shape. Can\'t change {} into shape {}'.format(iterable, shape))

    # show the picture
    def show(self):
        if self.data is None:
            raise Exception("There's no image loaded. Please check your code.")
        plt.imshow(self.data)
        plt.show()

    # draw a point on the picture and show it
    def drawPoint(self, cord, size=50, color='red'):
        if self.data is None:
            raise Exception("There's no image loaded. Please check your code.")
        fig, ax = plt.subplots()
        circ = Circle(cord, size, color=color)
        ax.imshow(self.data)
        ax.add_patch(circ)
        plt.show()

    # given a world coordinate, we get the projection of that point on the image
    def getProjection(self, cord):
        try:
            res = ImageABC.getHomoCord(ImageABC.typeChange(cord, (3, 1)))
        except:
            try:
                res = ImageABC.typeChange(cord, (4, 1))
            except:
                raise Exception("Invalid coordinate. Can't change\n{}\n into shape (3, 1) or (4, 1)".format(cord))
        return ImageABC.getCartCord(np.dot(self.projMatrix, res))

    # given world coordinate of a point, draw the projection of that point on picture
    def drawProjection(self, cord):
        if self.data is None:
            raise Exception("There's no image loaded. Please check your code.")
        pixCord = self.getProjection(cord)
        print(pixCord)
        if (pixCord[0] < 0 or pixCord[0] > self.data.shape[0]) or (pixCord[1] < 0 or pixCord[1] > self.data.shape[1]):
            print('Pixel Coordinate Out of Bound.')
        self.drawPoint(pixCord)

    def showWindow(self, cord, windowSize=21):
        if self.data is None:
            raise Exception("There's no image loaded. Please check your code.")
        # check windowSize
        if windowSize <=0:
            raise Exception("windowSize should be greater than 0.")
        if windowSize % 2 == 0:
            raise Exception("windowSize should be an odd number.")
        x = round(cord[0])
        y = round(cord[1])
        cord = (x, y)
        halfSize = windowSize // 2
        window = self.data[cord[1]-halfSize+1:cord[1]+halfSize+1, cord[0]-halfSize+1:cord[0]+halfSize+1, :]
        plt.imshow(window)

    def showProjectionWindow(self, cord, windowSize=21):
        if self.data is None:
            raise Exception("There's no image loaded. Please check your code.")
        # check windowSize
        if windowSize <=0:
            raise Exception("windowSize should be greater than 0.")
        if windowSize % 2 == 0:
            raise Exception("windowSize should be an odd number.")
        projCord = self.getProjection(cord).reshape((2,))
        # print(projCord)
        self.showWindow(projCord, windowSize=windowSize)

if __name__ == "__main__":
    print("Start Testing \n-----------------")
    obj = ImageABC()

