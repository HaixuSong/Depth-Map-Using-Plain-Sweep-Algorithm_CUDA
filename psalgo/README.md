## Description

A python model for Plane-Sweep-Algorithm. You can use these APIs for tuning parameters and fitting depth map.

## APIs

#### Import

Two classes are exposed. You can just simply import all things.

```python
from psalgo import *
```

or 

```python
from psalgo import InputImage, TargetImage
```

#### InputImage

* **Initializing**

  ```python
  input = InputImage(path, ep, cp, bound, ip)
  ```

  > path (string) : source image path
  >
  > ep (numpy array (3 * 3)) : external camera parameters
  >
  > cp (numpy array (3, or 3 * 1 or 1 * 3)) : camera world coordinate position
  >
  > bound (numpy array (3 or 3 * 1 or 1 * 3)) : boundaries of estimation space
  >
  > ip (numpy array (3, 3)) : internal camera parameters
  >
  > return: an InputImage instance

* **InputImage.getHomoCord (static method)**

  ```python
  cartCoord = InputImage.getHomoCord(vect)
  ```

  > vect (numpy array (n, or n, 1)) : the vector you wanna do transfer.
  >
  > return (numpy array (n-1, or n-1, 1)) : return the Cartesian Coordinate of a Homogeneour Coordinate.

* **InputImage.getCartCord (static method)**

  ```
  homoCoord = InputImage.getCartCord(vect)
  ```

  > Reverse of the previous method

* **InputImage.show**

  ```python
  inputImageInstance.show()
  ```

  > show the picture of the source image

* **InputImage.drawPoint**

  ```python
  inputImageInstance.drawPoint(cord, size=50, color='red')
  ```

  > cord (a length 2 iterable) : the pixel coordinate in format of (x, y)
  >
  > size (int) : the window width to draw.
  >
  > color (string) : a color to draw point
  >
  > draw a window from source image with cord centralized.

* **InputImage.getProjection**

  ```python
  inputImageInstance.getProjection(cord)
  ```

  > cord (a length 3 or 4 iterable) : the world coordinate
  >
  > return (numpy array) : the pixel coordinate projected of that world coordinate on source image.

* **InputImage.drawProjection**

  ```python
  inputImageInstance.getProjection(cord)
  ```

  > cord (a length 3 or 4 iterable) : the world coordinate
  >
  > draw the projection of that world coordinate on source image

* **InputImage.showWindow**

  ```python
  inputImageInstance.showWindow(cord, windowSize=21)
  ```

  > cord (a length 2 iterable) : the pixel coordinate
  >
  > windowSize (int) : window width to be shown
  >
  > show window with windowSize width central of cord

* **InputImage.showProjectionWindow**

  ```python
  inputImageInstance.showProjectionWindow(cord, windowSize=21)
  ```

  > cord (a length 3 or 4 iterable) : the world coordinate
  >
  > windowSize (int) : window width to be shown
  >
  > show window with windowSize width central of projected pixel

* **InputImage.pixInBound**

  ```python
  inputImageInstance.pixInBound(cord)
  ```

  > cord (a length 2 iterable) : the pixel coordinate
  >
  > return (Boolean) : if the pixel coordinate in range.

#### TargetImage

* **Initializing**

  ```python
  input = InputImage(ep, cp, bound, ip, path=None, groundTruth=None)
  ```

  > ep (numpy array (3 * 3)) : external camera parameters
  >
  > cp (numpy array (3, or 3 * 1 or 1 * 3)) : camera world coordinate position
  >
  > bound (numpy array (3 or 3 * 1 or 1 * 3)) : boundaries of estimation space
  >
  > ip (numpy array (3, 3)) : internal camera parameters
  >
  > path (string) : source image path
  >
  > groundTruth (string) : path of ground truth, point cloud file in ply format
  >
  > return: an InputImage instance

* **All API of InputImage**

  > Note: If you didn't specify the target image source path, some of its APIs using source images won't work.

* **TargetImage.drawResultDepthMap**

  ```python
  targetImageInstance.drawResultDepthMap()
  ```

  > Draw depth map we fitted before.
  >
  > If you haven't fit before, this will raise an error.

* **TargetImage.showGroundTruthDepthMap**

  ```python
  targetImageInstance.showGroundTruthDepthMap()
  ```

  > Draw ground truth depth map from point clouds in CSV.
  >
  > Used lazy initialization. The ground truth may cost 5 minutes when you first call this function, but 1 seconds when you call it again.

* **TargetImage.load**

  ```python
  targetImageInstance.load(iterable)
  ```

  > iterable (iterable of InputImage instances) : load a list of InputImage instances so that we can fit the depth map later.

* **TargetImage.fit**

  ```
  targetImageInstance.fit(similarityFunction="SSD", depthRange=(0, 30), planes=100, windowSize=21)
  ```

  > similarityFunction (string) : either of "SAD", "SSD", "NCC". Tell which similarity function we wanna use.
  >
  > depthRange (interable of 2 numbers) : Tell the deepest plane's and the nearest plane's depth.
  >
  > planes (int) : How many planes we trying to estimate.
  >
  > windowSize: The window width we trying to calculate the similarity function.

#### Similarity Functions

* **SAD**
  Sum of absolute difference. After getting the projected window on each image. Calculate the sum of all pixel loss. Each pixel loss is defined as absolute of difference between that pixel color and average color of all correlated pixel on all source images.
* **SSD**
  Sum of squared difference. After getting the projected window on each image. Calculate the sum of all pixel loss. Each pixel loss is defined as square of difference between that pixel color and average color of all correlated pixel on all source images.

* **NCC**
  Normalized Cross Correlation. After getting the projected window on each image. Calculate the cross correlation of two windows. The higher its NCC, the lower its loss.

