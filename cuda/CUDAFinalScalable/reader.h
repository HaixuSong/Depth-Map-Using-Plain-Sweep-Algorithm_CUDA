#ifndef reader
#define reader

struct inputImage {
	float ip[9];
	float ep[9];
	float cp[3];
	float pm[12];
	int resolution[2];
	float* data;
};

struct ioParam {
	int len;
	struct inputImage** arr;
	struct targetImage tar;
};

struct targetImage {
	float ip[9];
	float ep[9];
	float cp[3];
	float pm[12];
	int resolution[2];
};


struct ioParam read(char* inputFlag, char* outputFlag);

#endif // !helper
