#include <stdio.h>


int main(void){
  
  int i,num1,num2,result1,result2;


  scanf("%d %d",&num1,&num2);

  result1 = (num1/100) + (num1 /10) % 10 *10 + (num1 % 10) *  100;
  result2 = (num2/100) + (num2 /10) % 10 *10 + (num2 % 10) * 100;

  if(result1 < result2){
    printf("%d",result2);
  }
  else printf("%d",result1);

  return 0;
}
