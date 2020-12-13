This directory is CUDA source code for plane sweep algorithm.

**(This is a course project, so I didn't have enough time working on this. Now this directory is not finished yet. I'll keep working on this in the future)**

I tried my best to make this scalable so that if you have a better solution(like similarity function) based on plane-sweep algorithm, you can just replace part of the file to yours.

For example:

> If you have a better projection method. I used point to point projection, you want to make it window to window. Easy. Just replace projecter.c to yours and rewrite the function.
> If you have a better selector. I used SSD (sum of absolute difference). If you wanna use SSD or NCC, just replace the selecter.c.

## How each part works

main.c -> main function
reader.c -> read files and ip, ep, cp, projMatrix
projecter.cu -> how each thread project a pixle to wldCoord, then project to each image
selecter.cu -> how each pixel calculate loss and select the minimum loss
outputer.c -> output file

## Explaining

**Why I made loss calculation and plane selection both in selecter.cu instead of separating them.**

After reading a lot of papers, you may find that nowadays methods are more complex. Some of the loss functions works for specific selecting method. If you split these two into 2 source, you can't make the API between two source fixed. So that the code is no more scalable. 

