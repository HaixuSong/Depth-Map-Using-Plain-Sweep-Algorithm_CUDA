#include<string.h>
#include<stdio.h>
#include<stdlib.h>
#include "reader.h"

struct ioParam read(char* inputFlag, char* outputFlag) {
	struct ioParam res;
	int count = 0;

	for (int i = 0; inputFlag[i] != '\0'; ++i) {
		if (inputFlag[i] == ',') ++count;
	}
	res.len = count + 1;
	res.arr = malloc(res.len * sizeof(struct inputImage*));

	
	char* pch;
	pch = strtok(inputFlag, ",");
    // For each flag
	for (int i = 0; i < res.len; ++i) {
		struct inputImage* iimage = malloc(sizeof(struct inputImage));
		res.arr[i] = iimage;

		// read .iecp
		char* iecpName[100];
		strcpy(iecpName, pch);
		strcat(iecpName, ".png.iecp");

		FILE* iecpFile = fopen(iecpName, "r");
		if (iecpFile == NULL) {
			perror("Unable to open the file");
			exit(1);
		}

		char line[500];
		int count = 0;
		while (fgets(line, sizeof(line), iecpFile)) {
			char* token;
			token = strtok(line, " ");

			// read ip
			if (count == 0) {
				int ipCount = 0;
				while (ipCount < 9) {
					float num = (float)atof(token);
					iimage->ip[ipCount] = num;
					token = strtok(NULL, " ");
					++ipCount;
				}
			}

			// read cp
			if (count == 1) {
				int cpCount = 0;
				while (cpCount < 3) {
					float num = (float)atof(token);
					iimage->cp[cpCount] = num;
					token = strtok(NULL, " ");
					++cpCount;
				}
			}

			// read resolution
			if (count == 2) {
				iimage->resolution[0] = atoi(token);
				token = strtok(NULL, " ");
				iimage->resolution[1] = atoi(token);
			}

			// read ep
			if (count == 3) {
				int epCount = 0;
				while (epCount < 9) {
					float num = (float)atof(token);
					iimage->ep[epCount] = num;
					token = strtok(NULL, " ");
					++epCount;
				}
			}

			// read pm
			if (count == 4) {
				int pmCount = 0;
				while (pmCount < 12) {
					float num = (float)atof(token);
					iimage->pm[pmCount] = num;
					token = strtok(NULL, ",");
					++pmCount;
				}
			}

			++count;
		}


		// read .csv according to resolution




	}


	return res;
}