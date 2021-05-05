#include <stdio.h>
int number,d,t; // number 는 몇번쨰 분수, d는 몇번째 대각선, 
int main(){
  scanf("%d", &number);   // 사용자 입력값 받기

  for(;d*(d+1)/2 < number;d++){
  }

  t = number - d*(d-1)/2;
    // 14   -  5 * (4) /2 = 14 - 10 = ( t = 4 )

  if ( d % 2 == 0 ){
    printf("%d/%d", t, d-t+1);
  }

  else 
  printf("%d/%d",d-t+1,t);

	return 0; 
}

