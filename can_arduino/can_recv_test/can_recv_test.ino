#include <SPI.h>

const int SPI_CS_PIN = 9;
const int CAN_INT_PIN = 2;

#include "mcp2515_can.h"
mcp2515_can CAN(SPI_CS_PIN); // Set CS pin

unsigned char len = 0;
unsigned char buf[8];

void setup() {
    SERIAL_PORT_MONITOR.begin(115200);
    while(!Serial); // wait for Serial

    while (CAN_OK != CAN.begin(CAN_500KBPS)) {             // init can bus : baudrate = 500k
        SERIAL_PORT_MONITOR.println("CAN init fail, retry...");
        delay(100);
    }    
    //SERIAL_PORT_MONITOR.println("CAN init ok!");
}

void loop() {

    //SERIAL_PORT_MONITOR.println("checkReceive");
    if (CAN_MSGAVAIL == CAN.checkReceive()) {
      //SERIAL_PORT_MONITOR.print(CAN.getCanId(), HEX); SERIAL_PORT_MONITOR.print(":");
      // read data,  len: data length, buf: data buf
      CAN.readMsgBuf(&len, buf);
      // print the data
      for (int i = 0; i < len; i++) {
          SERIAL_PORT_MONITOR.print(buf[i], HEX); SERIAL_PORT_MONITOR.print(" ");
          //SERIAL_PORT_MONITOR.print((char) buf[i]); 
      }
      SERIAL_PORT_MONITOR.println();
    }
}
