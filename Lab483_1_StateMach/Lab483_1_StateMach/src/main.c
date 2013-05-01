/*
 * main.c
 *
 * Created: 9/27/2012 11:48:27 PM
 *  Author: Nate
 */ 


#include <stdlib.h>
#include <asf.h>
#include "FreeRTOS.h"
#include "task.h"
#include "partest.h"


#define led_testLED_TASK_PRIORITY			( tskIDLE_PRIORITY + 1 )
#define led_test500_MILLISECOND_TOGGLE				( 4 )

/* Task to be created. */
void vFlashLed500ms( void * blinktime )
{
	unsigned int hundredsofms = 0;
  for( ;; )
  {
		hundredsofms++;
		if (hundredsofms == 4)
			vParTestToggleLED( led_test500_MILLISECOND_TOGGLE );
		
		vTaskDelay(100/portTICK_RATE_MS);
  }
  vTaskDelete(NULL); //Task deletes itself if shit gets out of hand
}

/* Function that creates a task. */
void vStartBlink( void )
{
static unsigned char ucParameterToPass = 0;


  /* Create the task, storing the handle.  Note that the passed parameter 
  ucParameterToPass must exist for the lifetime of the task, so in this 
  case is declared static.  If it was just an an automatic stack variable 
  it might no longer exist, or at least have been corrupted, by the time
  the new task attempts to access it. */
  xTaskCreate( vStartBlink, "LED test", 300, &ucParameterToPass, led_testLED_TASK_PRIORITY, 
               NULL );

 
 }
 
 int main()
 {
	 board_init();
	 vParTestInitialise();
	 vStartBlink();
	 while(1)
	 {
		
	 }	
 }



