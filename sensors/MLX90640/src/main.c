#include "MLX90640_API.h"
#include "MLX90640_I2C_Driver.h"
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <bcm2835.h>
#include <math.h>
#include <stdint.h>
#include <time.h>
#include <string.h>

const int8_t slave_addr = 0x33;
static float temps[768];
paramsMLX90640 mlx90640;
int is_valid = 1;
const char file_exten[] = ".csv";

int main() {
	time_t current;
	time_t next_day;
	int fifo;
	int status;
	uint16_t eeProm[832];
	FILE* fp;
	if (!bcm2835_init()) {
		printf("cannot init bcm2835\n");
		return -1;	
	}
	status = MLX90640_DumpEE(slave_addr, eeProm);
	if (status != 0) {
		printf("failed to load params");
		return -1;
	}
	status = MLX90640_ExtractParameters(eeProm, &mlx90640);
	if (status != 0) {
		printf("failed to load params");
		return -1;
	}
	bcm2835_i2c_set_baudrate(100000);
	MLX90640_SetRefreshRate(slave_addr, 0x02);
	char filepath[100];
	char date[20];
	struct tm* current_day;
	time(&next_day);
	current_day = localtime(&next_day);
	sprintf(date, "%d-%d-%d", current_day->tm_year + 1900, current_day->tm_mon + 1, current_day->tm_mday);
	strcpy(filepath, "/mnt/database/data/");
	strcat(filepath, date);
	strcat(filepath, file_exten);
	fp = fopen(filepath, "ab+");
	if( fp <= 0 )
	{
		printf("invalid file path");
		return -1;
	}
	usleep(5000000); //max time before a good measurement
	while (1) {
		for(int8_t i = 0; i < 2; i++)
		{
			uint16_t frame[834];
			int status = MLX90640_GetFrameData(slave_addr, frame);
			if (status < 0) {
				printf("error");
				return -1;
			}
			float vdd = MLX90640_GetVdd(frame, &mlx90640);
			float Ta = MLX90640_GetTa(frame, &mlx90640);
			float Tr = Ta - 8;
			float emiss = 0.95; 
			MLX90640_CalculateTo(frame, &mlx90640, emiss, Tr, temps);
		}
		char date[20];
		struct tm* ts;
		time(&current);
		ts = localtime(&current);
		sprintf(date, "%d:%d:%d", ts->tm_hour, ts->tm_min, ts->tm_sec);
		if( fp > 0 )
		{
			fprintf(fp, "%s\r\n", date);
			for( int i = 0; i < 768; i++) 
			{
				if((i+1) % 32 == 0)
				{
					fprintf(fp, "%f", temps[i]);
					fputs("\n", fp);
				}
				else
				{
					fprintf(fp, "%f,", temps[i]);
				}
			}
			fflush(fp);
		}
		if( ts->tm_mday != current_day->tm_mday )
		{
			if( fp > 0 )
			{
				fclose(fp);
			}
			char filepath[100];
			char date[20];
			time(&next_day);
			current_day = localtime(&next_day);
			sprintf(date, "%d-%d-%d", current_day->tm_year + 1900, current_day->tm_mon + 1, current_day->tm_mday);
			strcpy(filepath, "/mnt/database/data/");
			strcat(filepath, date);
			strcat(filepath, file_exten);
			fp = fopen(filepath, "ab+");
		}
		usleep(5000); //wait 5ms btw measurements
	}
}
