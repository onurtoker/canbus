/*
 * canbus.c
 *
 *  Created on: Nov 4, 2021
 *      Author: onur
 */

#include "main.h"
#include "canbus.h"
#include <stdio.h>

CAN_TxHeaderTypeDef TxHeader;
uint32_t TxMailbox;
CAN_RxHeaderTypeDef RxHeader;


/**
  * @brief CAN1 Initialization Function
  * @param None
  * @retval None
  */
void MX_CAN1_Init(void)
{

  hcan1.Instance = CAN1;
  hcan1.Init.Prescaler = 4;
  hcan1.Init.Mode = CAN_MODE_NORMAL;
  hcan1.Init.SyncJumpWidth = CAN_SJW_1TQ;
  hcan1.Init.TimeSeg1 = CAN_BS1_7TQ;
  hcan1.Init.TimeSeg2 = CAN_BS2_8TQ;
  hcan1.Init.TimeTriggeredMode = DISABLE;
  hcan1.Init.AutoBusOff = DISABLE;
  hcan1.Init.AutoWakeUp = DISABLE;
  hcan1.Init.AutoRetransmission = DISABLE;
  hcan1.Init.ReceiveFifoLocked = DISABLE;
  hcan1.Init.TransmitFifoPriority = DISABLE;
  if (HAL_CAN_Init(&hcan1) != HAL_OK)
  {
    Error_Handler();
  }

}

/**
 * @brief           CAN Filter Configuration
 * @param[in]
 * @return
 */
void CAN_RX_Config(void)
{
    CAN_FilterTypeDef  sFilterConfig;

    /*Configure CAN filters*/
    sFilterConfig.FilterBank = 0;
    sFilterConfig.FilterMode = CAN_FILTERMODE_IDMASK;
    sFilterConfig.FilterScale = CAN_FILTERSCALE_32BIT;
    //sFilterConfig.FilterIdHigh = 0x111 << 5;
    sFilterConfig.FilterIdHigh = 0x000 << 5;
    sFilterConfig.FilterIdLow = CAN_ID_STD;
    //sFilterConfig.FilterMaskIdHigh = 0x7ff << 5;
    sFilterConfig.FilterMaskIdHigh = 0x000 << 5;
    sFilterConfig.FilterMaskIdLow = CAN_ID_STD;
    sFilterConfig.FilterFIFOAssignment = CAN_RX_FIFO0;
    sFilterConfig.FilterActivation = ENABLE;
    sFilterConfig.SlaveStartFilterBank = 13;

    //Filter Configuration
    if (HAL_CAN_ConfigFilter(&hcan1, &sFilterConfig) != HAL_OK)
    {
        printf("HAL_CAN_ConfigFilter Error\r\n");
    }

//    //Activation can RX notification
//    if (HAL_CAN_ActivateNotification(&hcan1, CAN_IT_RX_FIFO0_MSG_PENDING) != HAL_OK)
//    {
//    	printf("HAL_CAN_RXIntEnable Error\r\n");
//    }

}

/**
 * @brief           CAN TX Configuration
 * @param[in]
 * @return
 */
void CAN_TX_Config(void)
{

}

HAL_StatusTypeDef CAN_write(CAN_HandleTypeDef* hcan, uint16_t id, uint8_t* TxData)
{
	TxHeader.DLC = 8;  // data length
	TxHeader.IDE = CAN_ID_STD;
	TxHeader.RTR = CAN_RTR_DATA;
	TxHeader.StdId = id;  // ID
	return(HAL_CAN_AddTxMessage(hcan, &TxHeader, TxData, &TxMailbox));
}

HAL_StatusTypeDef CAN_read(CAN_HandleTypeDef* hcan, uint16_t* id, uint8_t* RxData)
{
	HAL_StatusTypeDef rc = HAL_CAN_GetRxMessage(hcan, CAN_RX_FIFO0, &RxHeader, RxData);
	*id = RxHeader.StdId;

	return(rc);
}

