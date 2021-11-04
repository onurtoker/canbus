#include <SPI.h>

const int SPI_CS_PIN = 9;
const int CAN_INT_PIN = 2;

#include "mcp2515_can.h"
mcp2515_can CAN(SPI_CS_PIN); // Set CS pin

unsigned char stmp[8] = {1,2,3,4,5,6,7,0};

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
    stmp[7] = stmp[7] + 1;
    if (stmp[7] == 100) {
        stmp[7] = 0;
    }

    CAN.sendMsgBuf(0x111, 0, 8, stmp);
    delay(1000);                       // send data per 100ms
    SERIAL_PORT_MONITOR.println("CAN BUS sendMsgBuf ok!");
}
