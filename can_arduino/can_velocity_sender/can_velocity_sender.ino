#include <SPI.h>

const int SPI_CS_PIN = 9;
const int CAN_INT_PIN = 2;

#include "mcp2515_can.h"
mcp2515_can CAN(SPI_CS_PIN); // Set CS pin

unsigned char stmp[8] = {0,0,0,0,0,0,0,0};

void setup() {
    SERIAL_PORT_MONITOR.begin(115200);
    while(!Serial){};

    while (CAN_OK != CAN.begin(CAN_500KBPS)) {             // init can bus : baudrate = 500k
        SERIAL_PORT_MONITOR.println("CAN init fail, retry...");
        delay(100);
    }
    SERIAL_PORT_MONITOR.println("CAN init ok!");
}


void loop() {
    // send data:  standrad frame, data len = 8, stmp: data buf
    stmp[0] = stmp[0] + 1;
    if (stmp[0] == 100) {
        stmp[0] = 0;
    }

    CAN.sendMsgBuf(0x06a, 0, 8, stmp);
    stmp[0] = stmp[0] + 20;
    CAN.sendMsgBuf(0x09a, 0, 8, stmp);
    stmp[0] = stmp[0] - 20;
    
    delay(100);                       // send data per 100ms
    SERIAL_PORT_MONITOR.println("CAN BUS sendMsgBuf ok!");
}
