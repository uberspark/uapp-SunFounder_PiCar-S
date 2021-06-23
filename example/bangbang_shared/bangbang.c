
#include "bangbang.h"
#include "i2c_functions.h"
/* Array used for retruning the results
   result_array[0] - speed
   result_array[1] - step
   result_array[2] - turn_angle
*/
__attribute__ ((section("i2c_section_4"))) static  int result_array[8]  = {0};

/* Private Functions */
void calculate_speed(int *array,int arr_len,int fw_speed,int *sp, int *st){
   const int a_step = 2;
   const int b_step = 8;
   const int c_step = 24;
   const int d_step = 40;
   if((array[0] == 0) && (array[1] == 0) && (array[2] == 1) &&
      (array[3] == 0) && (array[4] == 0) ){
      *st = 0;
   }
   else if(((array[0] == 0) && (array[1] == 1) && (array[2] == 1) &&
      (array[3] == 0) && (array[4] == 0) ) ||
      ((array[0] == 0) && (array[1] == 0) && (array[2] == 1) &&
      (array[3] == 1) && (array[4] == 0))) {
      *st =  a_step;
      *sp = fw_speed - 10;
   }
   else if(((array[0] == 0) && (array[1] == 1) && (array[2] == 0) &&
      (array[3] == 0) && (array[4] == 0) ) ||
      ((array[0] == 0) && (array[1] == 0) && (array[2] == 0) &&
      (array[3] == 1) && (array[4] == 0))) {
      *st = b_step;
      *sp = fw_speed - 15;
   }
   else if(((array[0] == 1) && (array[1] == 1) && (array[2] == 0) &&
      (array[3] == 0) && (array[4] == 0) ) ||
      ((array[0] == 0) && (array[1] == 0) && (array[2] == 0) &&
      (array[3] == 1) && (array[4] == 1))) {
      *st = c_step;
      *sp = fw_speed - 25;
   }
   else if(((array[0] == 1) && (array[1] == 0) && (array[2] == 0) &&
      (array[3] == 0) && (array[4] == 0) ) ||
      ((array[0] == 0) && (array[1] == 0) && (array[2] == 0) &&
      (array[3] == 0) && (array[4] == 1))) {
      *st = d_step;
      *sp = fw_speed - 35;
   }
   else{
      *st = d_step;
      *sp = fw_speed - 40;
   }
}


void calculate_angle(int *array,int arr_len,int *turn_angle, int st){
   if((array[0] == 0) && (array[1] == 0) && (array[2] == 1) &&
      (array[3] == 0) && (array[4] == 0) ){
      *turn_angle = 90;
   }
   else if(((array[0] == 0) && (array[1] == 1) && (array[2] == 1) &&
      (array[3] == 0) && (array[4] == 0) ) ||
      ((array[0] == 0) && (array[1] == 1) && (array[2] == 0) &&
      (array[3] == 0) && (array[4] == 0)) ||
      ((array[0] == 1) && (array[1] == 1) && (array[2] == 0) &&
      (array[3] == 0) && (array[4] == 0)) ||
      ((array[0] == 1) && (array[1] == 0) && (array[2] == 0) &&
      (array[3] == 0) && (array[4] == 0)) ) {
      *turn_angle = (int)(90 - st);
   }
   else if(((array[0] == 0) && (array[1] == 0) && (array[2] == 1) &&
      (array[3] == 1) && (array[4] == 0) ) ||
      ((array[0] == 0) && (array[1] == 0) && (array[2] == 0) &&
      (array[3] == 1) && (array[4] == 0)) ||
      ((array[0] == 0) && (array[1] == 0) && (array[2] == 0) &&
      (array[3] == 1) && (array[4] == 1)) ||
      ((array[0] == 0) && (array[1] == 0) && (array[2] == 0) &&
      (array[3] == 0) && (array[4] == 1)) ) {
      *turn_angle = (int)(90 + st);
   }
}


/* Public function */
int * calculate_angle_speed(int *array,int fw_speed,int turn_angle,int st){
   int speed = fw_speed;
   int step = st;
   int turning_angle = turn_angle;
   calculate_speed(array,NUM_REF,fw_speed,&speed,&step);
   calculate_angle(array,NUM_REF,&turning_angle,step);
   /* Return the other three parameters to the caller (Python) */
   result_array[0] = speed;
   result_array[1] = step;
   result_array[2] = turning_angle;
   return result_array;
}
