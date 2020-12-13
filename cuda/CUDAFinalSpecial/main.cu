#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<cuda_runtime.h>
#include<math.h>
#include<time.h>


struct planeParam {
    int from;
    int to;
    int numbers;
};

#define RESOLUTIONX 3072
#define RESOLUTIONY 2048

// constant memory declaration
__constant__ float pm3_d[12];
__constant__ float pm4_d[12];
__constant__ float pm5_d[12];
__constant__ float pm6_d[12];
__constant__ float pm7_d[12];

__constant__ float pi5_d[12];


void checkCUDAError(cudaError_t e) {
    if (e == 0) return;
    printf("\nError: %s\n", cudaGetErrorName(e));
    printf("%s\n", cudaGetErrorString(e));
    exit(0);
}


int UI(int argc, char* argv[], struct planeParam* plp) {

	//input -h for help
	if (argc == 2 && (strcmp(argv[1], "--help") == 0 || strcmp(argv[1], "-h") == 0)) {
		printf("CUDA Version Plane Sweep Alogrithm\n");
		printf("\nUsage: psalgo [OPTION]...\n");
		printf("\nOptions:\n");
		printf("%5s, %-10s %-50s\n", "-h", "--help", "Show helping information.");
		printf("%5s, %-10s %-50s\n", "-r", "--range", "Followed by 3 integers as plane range and numbers.");
		printf("\nExplaining:\n");
		printf("Use , as seperator:\n");
		printf("  Use , as sepeartor in one parameter. For example, -r 4,9,60\n");
		printf("What --range followed by\n");
		printf("  Three integers. First two representing range, the third one representing how many planes."
			"Range could be either greater first or less first. We recognize it automatically. \n");
		printf("\nExamples:\n");
		printf("psalgo -h\n");
		printf("  Shows the helping information.\n");
		printf("psalgo -r 4,9,60\n");
		printf("  Planes are ranged from 4 to 9, 60 planes in total.\n");
		return 1;
	}

	// input range
	if (argc == 3 && (strcmp(argv[1], "-r") == 0 || strcmp(argv[1], "--range") == 0)) {
		// processing -r or --range
		char* pch;
		pch = strtok(argv[2], ",");
		if (pch == NULL) {
			printf("Invalid range input. Please check your command or use -h for help.\n");
			return 1;
		}
		plp->from = atoi(pch);
		pch = strtok(NULL, ",");
		if (pch == NULL) {
			printf("Invalid range input. Please check your command or use -h for help.\n");
			return 1;
		}
		plp->to = atoi(pch);
		pch = strtok(NULL, ",");
		if (pch == NULL) {
			printf("Invalid range input. Please check your command or use -h for help.\n");
			return 1;
		}
		plp->numbers = atoi(pch);

		// make plp.from > plp.to
		if (plp->from < plp->to) {
			int cache = plp->from;
			plp->from = plp->to;
			plp->to = cache;
		}

		printf("%d planes from %d to %d\n", plp->numbers, plp->from, plp->to);
		return 0;
	}

	// all other invalid inputs
	else {
		printf("Invalid command. Please check how to make valid command by '-h' or '--help'.\n");
		return 1;
	}
}


void read(float* dataArray, const char* fileName) {
	FILE* dataFile = fopen(fileName, "r");
	if (dataFile == NULL) {
		printf("Unable to open file: %s.\n", fileName);
		exit(1);
	}

	char line[500];
	int count = 0;
	// loop for each line
	while (fgets(line, sizeof(line), dataFile)) {
		char* token;
		token = strtok(line, ",");

		// check if this is an empty line
		if (strcmp(token, "\n") == 0) {
			printf("Finish reading file: %s at line %d.\n", fileName, count / 3 + 1);
			return;
		}

		// read 3 tokens of that line
		if (token == NULL) {
			printf("Can't read csv file properly on line %d.\n", count / 3 + 1);
			exit(1);
		}
		// write float of that token into dataArray
		dataArray[count] = (float)atof(token);
		++count;

		token = strtok(NULL, ",");
		if (token == NULL) {
			printf("Can't read csv file properly on line %d.\n", count / 3 + 1);
			exit(1);
		}
		dataArray[count] = (float)atof(token);
		++count;

		token = strtok(NULL, "\n");
		if (token == NULL) {
			printf("Can't read csv file properly on line %d.\n", count / 3 + 1);
			exit(1);
		}
		dataArray[count] = (float)atof(token);
		++count;

	}
	fclose(dataFile);
}


__device__
void matrixMul(float* matrix1, float* matrix2, float* result, int x, int y, int z) {
	for (int i = 0; i < x; ++i) {
		for (int j = 0; j < z; ++j) {
			float summ = 0;
			for (int k = 0; k < y; ++k) {
				summ += matrix1[i * y + k] * matrix2[k * z + j];
			}
			result[i * z + j] = summ;
		}
	}
}


__global__
void psalgo(int from, int to, int numbers, float* data3_d, float* data4_d, float* data5_d, float* data6_d, float* data7_d, float* result) {
	unsigned int tx = blockIdx.x * blockDim.x + threadIdx.x;
	unsigned int ty = blockIdx.y * blockDim.y + threadIdx.y;
	if (tx < RESOLUTIONX && ty < RESOLUTIONY) {
		int planeCount = 0;
		float depth = from;
		float step = (float)(from - to) / (float)numbers;
		float wldCord[4];
		float pixCord[4];
		float projCord[3];
		float pixColor[15];
		int x, y;

		float miniResult = from;
		float miniLoss = -1;
    
		while (planeCount <= numbers) {
			
			pixCord[0] = tx * depth;
			pixCord[1] = ty * depth;
			pixCord[2] = depth;
			pixCord[3] = 1;
			matrixMul(pi5_d, pixCord, wldCord, 3, 4, 1);
			wldCord[3] = 1;
			
			// Projection on data3
			matrixMul(pm3_d, wldCord, projCord, 3, 4, 1);
			projCord[0] = projCord[0] / projCord[2];
			projCord[1] = projCord[1] / projCord[2];
			x = (int)round(projCord[0]);
			y = (int)round(projCord[1]);
			if (x >= RESOLUTIONX || x < 0 || y < 0 || y >= RESOLUTIONY) {
				pixColor[0] = -1;
				pixColor[1] = -1;
				pixColor[2] = -1;
			}
			else {
				int index = 3 * (y * RESOLUTIONX + x);
				pixColor[0] = data3_d[index];
				pixColor[1] = data3_d[index + 1];
				pixColor[2] = data3_d[index + 2];
			}
			
			// Projection on data4
			matrixMul(pm4_d, wldCord, projCord, 3, 4, 1);
			projCord[0] = projCord[0] / projCord[2];
			projCord[1] = projCord[1] / projCord[2];
			x = (int)round(projCord[0]);
			y = (int)round(projCord[1]);
			if (x >= RESOLUTIONX || x < 0 || y < 0 || y >= RESOLUTIONY) {
				pixColor[3] = -1;
				pixColor[4] = -1;
				pixColor[5] = -1;
			}
			else {
				int index = 3 * (y * RESOLUTIONX + x);
				pixColor[3] = data4_d[index];
				pixColor[4] = data4_d[index + 1];
				pixColor[5] = data4_d[index + 2];
			}
			// Projection on data5
			matrixMul(pm5_d, wldCord, projCord, 3, 4, 1);
			projCord[0] = projCord[0] / projCord[2];
			projCord[1] = projCord[1] / projCord[2];
			x = (int)round(projCord[0]);
			y = (int)round(projCord[1]);
			if (x >= RESOLUTIONX || x < 0 || y < 0 || y >= RESOLUTIONY) {
				pixColor[6] = -1;
				pixColor[7] = -1;
				pixColor[8] = -1;
			}
			else {
				int index = 3 * (y * RESOLUTIONX + x);
				pixColor[6] = data5_d[index];
				pixColor[7] = data5_d[index + 1];
				pixColor[8] = data5_d[index + 2];
			}
			// Projection on data6
			matrixMul(pm6_d, wldCord, projCord, 3, 4, 1);
			projCord[0] = projCord[0] / projCord[2];
			projCord[1] = projCord[1] / projCord[2];
			x = (int)round(projCord[0]);
			y = (int)round(projCord[1]);
			if (x >= RESOLUTIONX || x < 0 || y < 0 || y >= RESOLUTIONY) {
				pixColor[9] = -1;
				pixColor[10] = -1;
				pixColor[11] = -1;
			}
			else {
				int index = 3 * (y * RESOLUTIONX + x);
				pixColor[9] = data6_d[index];
				pixColor[10] = data6_d[index + 1];
				pixColor[11] = data6_d[index + 2];
			}
			// Projection on data7
			matrixMul(pm7_d, wldCord, projCord, 3, 4, 1);
			projCord[0] = projCord[0] / projCord[2];
			projCord[1] = projCord[1] / projCord[2];
			x = (int)round(projCord[0]);
			y = (int)round(projCord[1]);
			if (x >= RESOLUTIONX || x < 0 || y < 0 || y >= RESOLUTIONY) {
				pixColor[12] = -1;
				pixColor[13] = -1;
				pixColor[14] = -1;
			}
			else {
				int index = 3 * (y * RESOLUTIONX + x);
				pixColor[12] = data7_d[index];
				pixColor[13] = data7_d[index + 1];
				pixColor[14] = data7_d[index + 2];
			}
			
			
			// Now Calculate SAD
			float r = 0, g = 0, b = 0;
			int count = 0;
			for (int i = 0; i < 5; ++i) {
				if (pixColor[3 * i + 0] < 0) continue;
				r += pixColor[3 * i + 0];
				g += pixColor[3 * i + 1];
				b += pixColor[3 * i + 2];
				++count;
			}
			
			if (count > 2){
				r /= count; g /= count; b /= count;
				
				float loss = 0;
				for (int i = 0; i < 5; ++i) {
					if (pixColor[3 * i + 0] < 0) continue;
					loss += (float)fabs(pixColor[3 * i + 0] - r);
					loss += (float)fabs(pixColor[3 * i + 1] - g);
					loss += (float)fabs(pixColor[3 * i + 2] - b);
				}
				loss /= count;

				if (miniLoss < 0 || loss < miniLoss) {
					miniLoss = loss;
					miniResult = depth;
				}
				
			}
			depth -= step;
			++planeCount;
		}

		result[ty * RESOLUTIONX + tx] = miniResult;
		
	}
}




int main(int argc, char* argv[]) {
	clock_t start, finish;
	int total_time;

    float pm3[] = {1275.26, -2877.31, -148.52, 754.647, -747.178, -1000.76, 2663.54, -12946.3, -0.604314, -0.791759, -0.0890082, -10.1165};
    float pm4[] = {1768.22, -2606.58, -79.9353, 12002.6, -515.384, -1020.13, 2710.72, -10582.4, -0.453793, -0.889721, -0.0496901, -9.01598};
    float pm5[] = {2246.17, -2208.64, -62.134, 24477.4, -316.161, -1091.08, 2713.64, -8334.18, -0.269944, -0.961723, -0.0471142, -7.01217};
    float pm6[] = {2592.44, -1790, -48.8682, 35535.5, -114.072, -1095.02, 2728.03, -5423.57, -0.100616, -0.994335, -0.0342684, -4.72891};
    float pm7[] = {2890.6, -1253.12, -37.3055, 46750.1, 105.251, -1060.63, 2741.94, -1799.29, 0.0943235, -0.995311, -0.0214366, -1.68246};

	float pi5[] = { 0.00034888542585823415, -5.808190865675488e-06, -0.7946427612701072, -14.1604, -9.798911120446392e-05, -1.6072973979090537e-05, -0.7965288644222046, -3.32084, 1.2491902020089363e-06, 0.00036136950280672903, -0.41284422473450133, 0.0862032 };


    struct planeParam plp;
    int UIStatus;

    // UI
    UIStatus = UI(argc, argv, &plp);
    if (UIStatus != 0) {
        printf("\nApplication terminates.\n");
        return 0;
		}
	
	
    // Read png data into float array
    int dataSize = RESOLUTIONX * RESOLUTIONY * 3 * sizeof(float);
    float* data3 = (float*)malloc(dataSize);
    float* data4 = (float*)malloc(dataSize);
    float* data5 = (float*)malloc(dataSize);
    float* data6 = (float*)malloc(dataSize);
    float* data7 = (float*)malloc(dataSize);
    read(data3, "0003.csv");
    read(data4, "0004.csv");
    read(data5, "0005.csv");
    read(data6, "0006.csv");
    read(data7, "0007.csv");
    printf("Done reading pixels into array.\n");

    // allocate global memory on gpu
    float *data3_d, *data4_d, *data5_d, *data6_d, *data7_d, *result_d;
    checkCUDAError(cudaMalloc((float**)&data3_d, dataSize));
    checkCUDAError(cudaMalloc((float**)&data4_d, dataSize));
    checkCUDAError(cudaMalloc((float**)&data5_d, dataSize));
    checkCUDAError(cudaMalloc((float**)&data6_d, dataSize));
    checkCUDAError(cudaMalloc((float**)&data7_d, dataSize));
	checkCUDAError(cudaMalloc((float**)&result_d, RESOLUTIONX * RESOLUTIONY * sizeof(float)));

    // write png data into gpu
    checkCUDAError(cudaMemcpy(data3_d, data3, dataSize, cudaMemcpyHostToDevice));
    checkCUDAError(cudaMemcpy(data4_d, data4, dataSize, cudaMemcpyHostToDevice));
    checkCUDAError(cudaMemcpy(data5_d, data5, dataSize, cudaMemcpyHostToDevice));
    checkCUDAError(cudaMemcpy(data6_d, data6, dataSize, cudaMemcpyHostToDevice));
    checkCUDAError(cudaMemcpy(data7_d, data7, dataSize, cudaMemcpyHostToDevice));

	checkCUDAError(cudaMemcpyToSymbol(pm3_d, pm3, 12 * sizeof(float)));
	checkCUDAError(cudaMemcpyToSymbol(pm4_d, pm4, 12 * sizeof(float)));
	checkCUDAError(cudaMemcpyToSymbol(pm5_d, pm5, 12 * sizeof(float)));
	checkCUDAError(cudaMemcpyToSymbol(pm6_d, pm6, 12 * sizeof(float)));
	checkCUDAError(cudaMemcpyToSymbol(pm7_d, pm7, 12 * sizeof(float)));

	checkCUDAError(cudaMemcpyToSymbol(pi5_d, pi5, 12 * sizeof(float)));
	
	
	// defining dim and grid, then launch kernel
	dim3 threads(16, 16);
	dim3 grid((int)ceil(1.0 * RESOLUTIONX / threads.x), (int)ceil(1.0 * RESOLUTIONY / threads.y));
	start = clock();
	printf("Now launching kernel.\n");
	psalgo<<<grid, threads>>>(plp.from, plp.to, plp.numbers, data3_d, data4_d, data5_d, data6_d, data7_d, result_d);
	cudaError_t error_check = cudaGetLastError();
	if (error_check != cudaSuccess) {
		printf("%s\n", cudaGetErrorString(error_check));
		return 0;
	}
	checkCUDAError(cudaDeviceSynchronize());
	finish = clock();
	total_time = (int)(finish - start);
	printf("\nDone psalgo with GPU in %d miliseconds.\n", total_time);

	// get result from gpu
	float* result = (float*)malloc(RESOLUTIONX * RESOLUTIONY * sizeof(float));
	checkCUDAError(cudaMemcpy(result, result_d, RESOLUTIONX * RESOLUTIONY * sizeof(float), cudaMemcpyDeviceToHost));

	// write result into csv
	FILE* output = fopen("output.csv", "w");
	if (output == NULL) {
		printf("Can't open file for output.\n");
		return 1;
	}
	for (int i = 0; i < RESOLUTIONX * RESOLUTIONY; ++i) {
		fprintf(output, "%f\n", result[i]);
	}
	fclose(output);
	
	// free cuda memory
	checkCUDAError(cudaFree(data3_d));
	checkCUDAError(cudaFree(data4_d));
	checkCUDAError(cudaFree(data5_d));
	checkCUDAError(cudaFree(data6_d));
	checkCUDAError(cudaFree(data7_d));
	checkCUDAError(cudaFree(result_d));

}			 

