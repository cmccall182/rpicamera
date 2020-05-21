/**
 * @copyright (C) 2017 Melexis N.V.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */
#include "MLX90640_I2C_Driver.h"
#include <bcm2835.h>
#include <signal.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#define SLAVE_ADDR 0x33

void MLX90640_I2CInit()
{   
    bcm2835_i2c_begin();
    bcm2835_i2c_setSlaveAddress(SLAVE_ADDR);
}

int MLX90640_I2CRead(uint8_t slaveAddr, uint16_t startAddress, uint16_t nMemAddressRead, uint16_t *data)
{
    uint8_t sa;                                                          
    int cnt = 0;
    int i = 0;
    char cmd[2] = {0,0};
    char i2cData[1664] = {0};
    uint16_t *p;
    
    p = data;
    sa = (slaveAddr << 1);
    cmd[0] = startAddress >> 8;
    cmd[1] = startAddress & 0x00FF;
    bcm2835_i2c_begin();
    //printf("attempting to set slave _addr\n");
    bcm2835_i2c_setSlaveAddress(0x33);
    //i2c.stop();
    usleep(5);    
    //ack = i2c.write(sa, cmd, 2, 1);
    //printf("attempting to write i2c\n");
    if(bcm2835_i2c_write_read_rs((char*)&cmd,2,(char*)&i2cData, 2*nMemAddressRead) != BCM2835_I2C_REASON_OK) {
       printf("write failed\n");
       return -1;
    }
    
    //printf("%d", sa);         
    //sa = sa | 0x01;
    //ack = i2c.read(sa, i2cData, 2*nMemAddressRead, 0);
    
    //if (ack != 0x00)
    //{
    //    return -1; 
    //}          
    //i2c.stop();   
    bcm2835_i2c_end();
    for(cnt=0; cnt < nMemAddressRead; cnt++)
    {
        i = cnt << 1;
        *p++ = (uint16_t)i2cData[i]*256 + (uint16_t)i2cData[i+1];
    }
    
    return 0;   
} 

void MLX90640_I2CFreqSet(int freq)
{
    bcm2835_i2c_set_baudrate(1000*freq);
}

int MLX90640_I2CWrite(uint8_t slaveAddr, uint16_t writeAddress, uint16_t data)
{
    uint8_t sa;
    //int ack = 0;
    char cmd[4] = {0,0,0,0};
    static uint16_t dataCheck;
    

    sa = (slaveAddr << 1);
    //printf("%d", sa);
    cmd[0] = writeAddress >> 8;
    cmd[1] = writeAddress & 0x00FF;
    cmd[2] = data >> 8;
    cmd[3] = data & 0x00FF;

    bcm2835_i2c_begin();
    bcm2835_i2c_setSlaveAddress(SLAVE_ADDR);
    usleep(5);    
    if(bcm2835_i2c_write((char*)&cmd,4) != BCM2835_I2C_REASON_OK)
	return -1;
           
    bcm2835_i2c_end();   
    
    MLX90640_I2CRead(slaveAddr,writeAddress,1, &dataCheck);
    
    if ( dataCheck != data)
    {
        return -2;
    }    
    
    return 0;
}

