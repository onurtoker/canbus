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

CAN_TxHeaderTypeDef TxHeader;
CAN_RxHeaderTypeDef RxHeader;

uint8_t TxData[8];
uint8_t RxData[8];

uint32_t TxMailbox;

int datacheck = 0;

void HAL_CAN_RxFifo0MsgPendingCallback(CAN_HandleTypeDef *hcan)
{
	HAL_CAN_GetRxMessage(hcan, CAN_RX_FIFO0, &RxHeader, RxData);
	if (RxHeader.DLC == 8)
	{
		datacheck = 1;
	}
}

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
    if (HAL_CAN_Start(&hcan1) != HAL_OK)
        printf("HAL_CAN_Start Error\r\n");

	// Transmit example
    while (1) {
		TxHeader.DLC = 8;  // data length
		TxHeader.IDE = CAN_ID_STD;
		TxHeader.RTR = CAN_RTR_DATA;
		TxHeader.StdId = 0x103;  // ID
		uint8_t TxData[] = {0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08}; // Tx Buffer
		if (HAL_CAN_AddTxMessage(&hcan1, &TxHeader, TxData, &TxMailbox) != HAL_OK)
		{
			 printf("CAN bus error\r\n");
			 printf("System RESET needed\r\n");
			 Error_Handler ();
		}
		else
			printf("CAN bus OK\r\n");
		HAL_Delay(100);
	}

    // Receive example
	while (1) {
		//HAL_GPIO_WritePin(LD3_GPIO_Port, LD3_Pin, GPIO_PIN_SET);
		if (datacheck) {
			printf("\r\n%04lx : ", RxHeader.StdId);
			for (int i=0; i<8; i++)
				printf("%02x ", RxData[i]);
			datacheck = 0;
		}
		//HAL_GPIO_WritePin(LD3_GPIO_Port, LD3_Pin, GPIO_PIN_RESET);
	}

}

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
