/*
 * canbus.c
 *
 *  Created on: Nov 4, 2021
 *      Author: onur
 */

#include "main.h"
#include "canbus.h"
#include <stdio.h>

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
    sFilterConfig.FilterIdHigh = 0x111 << 5;
    sFilterConfig.FilterIdLow = CAN_ID_STD;
    sFilterConfig.FilterMaskIdHigh = 0x7ff << 5;
    sFilterConfig.FilterMaskIdLow = CAN_ID_STD;
    sFilterConfig.FilterFIFOAssignment = CAN_RX_FIFO0;
    sFilterConfig.FilterActivation = ENABLE;
    sFilterConfig.SlaveStartFilterBank = 13;

    //Filter Configuration
    if (HAL_CAN_ConfigFilter(&hcan1, &sFilterConfig) != HAL_OK)
    {
        printf("HAL_CAN_ConfigFilter Error\r\n");
    }

    //Activation can RX notification
    if (HAL_CAN_ActivateNotification(&hcan1, CAN_IT_RX_FIFO0_MSG_PENDING) != HAL_OK)
    {
    	printf("HAL_CAN_IntEnable Error\r\n");
    }
}

/**
 * @brief           CAN TX Configuration
 * @param[in]
 * @return
 */
void CAN_TX_Config(void)
{

}
