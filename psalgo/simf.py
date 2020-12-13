# from InputImage import InputImage
import numpy as np


# sum of squared difference
# windowSize is tested, no need to re-test
def _ssd(cord, windowSize, sourceList):
    windowList = []
    for image in sourceList:
        pixCord = image.getProjection(cord).reshape((2,))
        x = round(pixCord[0])
        y = round(pixCord[1])
        halfSize = windowSize // 2
        if not image.pixInBound((x, y)): return None
        if not image.pixInBound((x - halfSize, y - halfSize)): return None
        if not image.pixInBound((x + halfSize, y + halfSize)): return None
        windowList.append(image.data[y - halfSize: y + halfSize + 1, x - halfSize: x + halfSize + 1, :])

    summ = np.zeros(shape=((windowSize, windowSize, 3)))
    for window in windowList:
        summ += window
    avg = summ / len(windowList)

    summ = 0
    for window in windowList:
        error = np.sum((window - avg) ** 2)
        summ += error
    return summ


# sum of absolute difference
def _sad(cord, windowSize, sourceList):
    windowList = []
    for image in sourceList:
        pixCord = image.getProjection(cord).reshape((2,))
        x = round(pixCord[0])
        y = round(pixCord[1])
        halfSize = windowSize // 2
        if not image.pixInBound((x, y)): return None
        if not image.pixInBound((x - halfSize, y - halfSize)): return None
        if not image.pixInBound((x + halfSize, y + halfSize)): return None
        windowList.append(image.data[y - halfSize: y + halfSize + 1, x - halfSize: x + halfSize + 1, :])

    summ = np.zeros(shape=((windowSize, windowSize, 3)))
    for window in windowList:
        summ += window
    avg = summ / len(windowList)

    summ = 0
    for window in windowList:
        error = np.sum(np.absolute(window - avg))
        summ += error
    return summ


# negative correlation coefficient
def _ncc(cord, windowSize, sourceList):
    if len(sourceList) != 2:
        raise Exception("There should be 2 items as source if you want to use NCC.")
    if windowSize == 1:
        raise Exception("How correlation is calculated between two numbers?")
    windowList = []
    for image in sourceList:
        pixCord = image.getProjection(cord).reshape((2,))
        x = round(pixCord[0])
        y = round(pixCord[1])
        halfSize = windowSize // 2
        if not image.pixInBound((x, y)): return None
        if not image.pixInBound((x - halfSize, y - halfSize)): return None
        if not image.pixInBound((x + halfSize, y + halfSize)): return None
        windowList.append(image.data[y - halfSize: y + halfSize + 1, x - halfSize: x + halfSize + 1, :].reshape((windowSize**2, 3)))

    summ = 0
    for i in range(3):
        summ += np.corrcoef(windowList[0][:, i], windowList[1][:, i])[0][1]
    return -summ


simFunc = {
    "SSD": _ssd,
    "SAD": _sad,
    "NCC": _ncc
}