## Description

This directory is the source code of CUDA version plane sweep algorithm with arbitrary planes and arbitrary plane depth range. 

## Compiling

Using command line:

```
nvcc main.cu
```

## Input and Output

Since I didn't use any dependent libraries, the input files are csv format. Each line represents scaled RGB value. Output file is also in csv format. Each line represent a pixel. There's only one value in each line, which represents the depth of that pixel.

## Running 

You can use -h or --help for help information. It will tell you how to use it.

```
a.exe -h
```

You can use -r or --range to tell the parameters of the planes. 9, 4, 60 represents there are 60 planes ranged from 9 to 4. 9 and 4 could be reversed. The algorithm inside may pick the larger one as 'from' automatically.

```
a.exe -r 9,4,60
```

