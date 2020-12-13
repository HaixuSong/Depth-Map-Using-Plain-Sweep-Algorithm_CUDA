This directory contains all csv files.
Each csv file is actually numpy generated, so all data are ranged 0-1.

The reason why I used numpy generated csv as input of c code is that:
  I found it hard using libpng to read png files directly.
  So I used:
    png file
      |
      |matplotlib.mpimg.imread
      |
    numpy ndarray
      |
      |reshape, np.savetxt
      |
    csv file
      |
      |stdlib.h
      |
    array in c

The transfering code is in transfer.ipynb