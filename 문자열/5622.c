#include <stdio.h>
#include <string.h>


int main(void){
  
  char arr[15],anw;
  int time=0,len; 
  scanf("%s", arr);
  len = strlen(arr);

  for(int i=0; i<len; i++){
    char x = arr[i] - 'A';
    if( x <= 2 ){
      time += 2;
    }
    else if ( x < 2 || x <= 5){
      time += 3;
    }
    else if( x < 5 || x <= 8){
      time += 4;
    }
    else if ( x < 8 || x <= 11){
      time += 5;
    }
    else if ( x < 11 || x <= 14){
      time += 6;
    }
    else if ( x < 14 || x <= 18){
      time += 7;
    }
    else if ( x < 18 || x <= 21){
      time += 8;
    } 
    else if ( x < 21 || x <= 25){
      time += 9;
    }
    else {
      time += 10;
    }
    time += 1;  
  }
  printf("%d\n", time);

  return 0;
}


