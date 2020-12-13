#include<stdio.h>
#include"helper.h"
#include"reader.h"

int main(int argc, char* argv[]) {
	struct planeParam plp;
    int UIStatus;
    char inputFlag[100];
    char outputFlag[100];

    // UI
    UIStatus = UI(argc, argv, &plp, inputFlag, outputFlag);
    if (UIStatus != 0) {
        printf("\nApplication terminates.\n");
        return 0;
    }

    // Read Files using the flags
    struct ioParam iop;
    iop = read(inputFlag, outputFlag);
}