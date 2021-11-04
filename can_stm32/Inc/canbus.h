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

#endif /* INC_CANBUS_H_ */
