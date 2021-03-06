/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2021 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */

#include "main.h"
#include "sysclk.h"
#include "gpio.h"
#include "timer.h"
#include "uart.h"
#include "canbus.h"
#include <stdio.h>

CAN_HandleTypeDef hcan1;
TIM_HandleTypeDef htim6;
UART_HandleTypeDef huart2;

uint8_t TxData[8];
uint8_t RxData[8];
//int datacheck = 0;

//// see canbus.c to enable/disable this callback function
//void HAL_CAN_RxFifo0MsgPendingCallback(CAN_HandleTypeDef *hcan)
//{
//	HAL_CAN_GetRxMessage(hcan, CAN_RX_FIFO0, &RxHeader, RxData);
//	if (RxHeader.DLC == 8)
//		datacheck = 1;
//}

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
	/* MCU Configuration----------------------------------------------------------*/
	/* Reset of all peripherals, Initializes the Flash interface and the Systick. */
	HAL_Init();
	/* Configure the system clock */
	SystemClock_Config();
	/* Initialize all configured peripherals */
	MX_GPIO_Init();
	MX_USART2_UART_Init();
	MX_CAN1_Init();
	MX_TIM6_Init();

	CAN_RX_Config();
	CAN_TX_Config();
	// Start the CAN bus
    if (HAL_CAN_Start(&hcan1) != HAL_OK)
        printf("HAL_CAN_Start Error\r\n");

	//HAL_GPIO_WritePin(LD3_GPIO_Port, LD3_Pin, GPIO_PIN_SET);
	//HAL_GPIO_WritePin(LD3_GPIO_Port, LD3_Pin, GPIO_PIN_RESET);

    uint16_t breakPC = 0x01FF;
    uint16_t wheelRPM = 0x0000;
    TxData[2] = 0x20; TxData[3] = 0x03; TxData[4] = TxData[5] = TxData[6] = TxData[7] = 0;

    while (1) {
		// Transmit break pedal command
		TxData[0] = 0x00FF & breakPC;
		TxData[1] = breakPC >> 8;
		if (CAN_write(&hcan1, (uint16_t) 0x060, TxData) != HAL_OK) {
			 printf("CAN bus error\r\n");
			 printf("System RESET needed\r\n");
			 //Error_Handler ();
		}
		HAL_Delay(20);
		printf("breakPC = %04x ", breakPC);

		// Receive example
		uint16_t fid;
		HAL_StatusTypeDef rc;
		rc = CAN_read(&hcan1, &fid, RxData);
		if (rc == HAL_OK) {
			//printf("\r\n%04x : ", fid);
			//for (int i=0; i<8; i++) printf("%02x ", RxData[i]);
			wheelRPM = ((uint16_t) RxData[0]) + (((uint16_t) RxData[1]) << 8);
			printf("wheelRPM = %04x\r\n", wheelRPM);

			if ((wheelRPM < 0x0005) && (breakPC > 0))
				breakPC = 0.98*breakPC;
			if (wheelRPM > 0x0005)
				breakPC += wheelRPM / 10;
		}

	}

}

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
