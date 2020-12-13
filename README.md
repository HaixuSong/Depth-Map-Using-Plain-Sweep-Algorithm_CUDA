# Plane Sweep Algorithm -- Python Module and CUDA Code

Course Project of CPE810----Special Topics in Computer Engineering: GPU and Multicore Programming

----

/psalgo -- A python module to test and tune the plane sweep algorithm.

/cuda -- CUDA version plane sweep algorithm

/data -- Images and parameters of fountain-P11

/report -- Final presentation and final report

/test -- Low resolution of original images, used for python testing

main.ipynb -- Python API example

output.png -- CUDA kernel output

pkg.txt -- Python packages used

groundTruth.png -- Calculated ground truth using ply file with python.

#### Note

The groundTruth.png generated may have some error in it. The error is that not all the pixels are showing the correct color of object. The reason is that I calculated the depth image using the vertexes in ply file instead of faces. This may cause a problem that not all the pixel points on the image will get a projection from a vertex in the point cloud. So the pixels with no projection will show the background color. And that's why the depth map I generated is not accurate. There are several ways to solve this problem. One is continue using vertex projection, but do a KNN vote on the pixel that didn't have a projection. One is using faces instead of vertexes in the ply file to calculate the depth. 



