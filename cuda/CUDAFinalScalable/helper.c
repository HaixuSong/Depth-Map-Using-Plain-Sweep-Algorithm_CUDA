#include "helper.h"
#include<string.h>

int UI(int argc, char* argv[], struct planeParam* plp, char* inputFlag, char* outputFlag) {

    //input -h for help
    if (argc == 2 && (strcmp(argv[1], "--help") == 0 || strcmp(argv[1], "-h") == 0)) {
        printf("CUDA Version Plane Sweep Alogrithm\n");
        printf("\nUsage: psalgo [OPTION]...\n");
        printf("\nOptions:\n");
        printf("%5s, %-10s %-50s\n", "-h", "--help", "Show helping information.");
        printf("%5s, %-10s %-50s\n", "-r", "--range", "Followed by 3 integers as plane range and numbers.");
        printf("%5s, %-10s %-50s\n", "-i", "--input", "Followed by input flags.");
        printf("%5s, %-10s %-50s\n", "-o", "--output", "Specifying output flags.");
        printf("\nExplaining:\n");
        printf("Input and Output flags:\n");
        printf("  Flags are used to read and write input image and parameters."
            "If you wanna have your own reader source file, please make sure you passed the valid flags.\n");
        printf("-r -i and -o have to be specified together\n");
        printf("  You have to specify planes range and number, input flags and output flags together "
            "so that the program knows all information needed for the algorithm.\n");
        printf("Use , as seperator:\n");
        printf("  Use , as sepeartor in one parameter. For example, -r 4,9,60\n");
        printf("What --range followed by\n");
        printf("  Three integers. First two representing range, the third one representing how many planes."
            "Range could be either greater first or less first. We recognize it automatically. \n");
        printf("\nExamples:\n");
        printf("psalgo -h\n");
        printf("  Shows the helping information.\n");
        printf("psalgo -r 4,9,60 -i 0004,0005,0006 -o 0005\n");
        printf("  Planes are ranged from 4 to 9, 60 planes in total; Input flags are 0004, 0005 and 0006; "
            "Output flags is 0005. Flags are used for reader.\n");
        return 1;
    }

    // input inputPara
    // if (argc == 7 && (strcmp(argv[1], "-r") == 0 || strcmp(argv[1], "--range") == 0)) {
    if (argc == 7) {
        // Flags representing if each command is already specified
        int cmdFlag[3] = {0, 0, 0};

        for (int i = 1; i < 7; ++i) {
            // processing -r or --range
            if (strcmp(argv[i], "-r") == 0 || strcmp(argv[i], "--range") == 0) {
                char* pch;
                cmdFlag[0] = 1;
                pch = strtok(argv[i + 1], ",");
                plp->from = atoi(pch);
                pch = strtok(NULL, ",");
                plp->to = atoi(pch);
                pch = strtok(NULL, ",");
                plp->numbers = atoi(pch);
                if (plp->from < plp->to) {
                    int cache = plp->from;
                    plp->from = plp->to;
                    plp->to = cache;
                }
                ++i;
                continue;
            }

            // processing -i or --input
            if (strcmp(argv[i], "-i") == 0 || strcmp(argv[i], "--input") == 0) {
                cmdFlag[1] = 1;
                if (strlen(argv[i + 1]) >= 99) {
                    printf("Input flags are so long, please redesign it and make it shorter. \n");
                    return 1;
                }
                strcpy(inputFlag, argv[i+1]);
                ++i;
                continue;
            }

            // processing -o or --output
            if (strcmp(argv[i], "-o") == 0 || strcmp(argv[i], "--output") == 0) {
                cmdFlag[2] = 1;
                if (strlen(argv[i + 1]) >= 99) {
                    printf("Output flags are so long, please redesign it and make it shorter. \n");
                    return 1;
                }
                strcpy(outputFlag, argv[i + 1]);
                ++i;
                continue;
            }

            // other circumstances
            printf("Unknown input format, please use -h for help.\n");
            return 1;
        }

        if (cmdFlag[0] == 0 || cmdFlag[1] == 0 || cmdFlag[2] == 0) {
            printf("-r, -i, -o are all needed. Please specify all of them.\n");
            return 1;
        }
        
        printf("%d planes from %d to %d\n", plp->numbers, plp->from, plp->to);
        printf("Input flag is: %s\n", inputFlag);
        printf("Output flag is: %s\n", outputFlag);
        return 0;
    }

    // all other invalid inputs
    else {
        printf("Invalid command. Please check how to make valid command by '-h' or '--help'.\n");
        return 1;
    }
}