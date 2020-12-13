CUDA version of plane sweep algorithm.

There are 2 directories here:

-----

* CUDAFinalSpecial:
  * CUDA version plane sweep algorithm for specific use: Load five image data from csv files and generate depth map data into csv file.
  * The projection matrix and inverse projection matrix are all pre-calculated and fixed in this code.
  * The CUDA kernel can deal with arbitrary image size.
* CUDAFinalScalable:
  * Still working on this one.
  * Trying to write scalable C and CUDA code so that it can deal with arbitrary input numbers, input file type, input parameters.
  * Trying to write structured code so that each function are separated into different parts. This would be easy for future updates if we have better algorithm based on plane-sweeping.
  * Trying to write scalable CUDA code to optimize the GPU performance on arbitrary GPU device. This is quite hard actually. I don't think I can do this.
  * Still working on this one. 

