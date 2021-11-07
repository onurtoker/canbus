/*
 * canbus.h
 *
 *  Created on: Nov 4, 2021
 *      Author: onur
 */

#ifndef INC_CANBUS_H_
#define INC_CANBUS_H_

#include "main.h"

extern CAN_HandleTypeDef hcan1;

extern void MX_CAN1_Init(void);
extern void CAN_RX_Config(void);
extern void CAN_TX_Config(void);

extern HAL_StatusTypeDef CAN_write(CAN_HandleTypeDef*, uint16_t, uint8_t*);
extern HAL_StatusTypeDef CAN_read(CAN_HandleTypeDef*, uint16_t*, uint8_t*);

#endif /* INC_CANBUS_H_ */
