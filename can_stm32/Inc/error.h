/*
 * error.h
 *
 *  Created on: Nov 4, 2021
 *      Author: onur
 */

#ifndef INC_ERROR_H_
#define INC_ERROR_H_

#include "main.h"

void Error_Handler(void);

#ifdef  USE_FULL_ASSERT
void assert_failed(uint8_t *, uint32_t);
#endif /* USE_FULL_ASSERT */

#endif /* INC_ERROR_H_ */
