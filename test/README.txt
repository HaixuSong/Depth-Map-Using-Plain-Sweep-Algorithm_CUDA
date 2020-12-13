The images in this directory are all the same with original data but different in resolution.
We used this as python sequence code fitting data, since the original data may take hours to fit. 

The original data's resolution is 3072 * 2048, here's is 307 * 205.
Both width and height are 0.1 of original.

So when using these data as input or target images, you have to manually change internal parameters. For example:
Original data ip(internal parameter):
[2759.48, 0,       1520.69]
[0,       2764.16, 1006.81]
[0,       0,       1      ]
New ip:
[275.948, 0,       152.069]
[0,       276.416, 100.681]
[0,       0,       1      ]