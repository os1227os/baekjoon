```c
#include <stdio.h>
#include <string.h>


int main(void){
  
  char arr[101];   //  최대 100개 길이의 문자를 받기 위한 배열 선언.
  scanf("%s",  arr);
  int len, sum;   // 문자의 길이를 넣어줄 len 변수와 크로아티아 언어가 나오면 줄여줄 sum 변수 선언. 

  len = strlen(arr);  //  둘다 변수에 문자를 넣어준다 
  sum = strlen(arr);  //  둘다 변수에 문자를 넣어준다
  for(int i=0; i<len; i++){   // 문자의 길이만큼 for문 실행. 
      
    if( arr[i] == 'c' || arr[i] =='s' || arr[i] == 'z'){  // 만약 c,s,z 가 들어오면 
     if (arr[i+1] == '=' || arr[i+1] == '-') sum--;  // 다음 문자에 '=' , '-' 가 있는지 확인후 만약 있다면 크로아티아 언어가 있다는 뜻이니 sum에서 길이 차감.
    }
    else if ( arr[i] == 'n' || arr[i] =='l'){  //  같은 방식으로 n,l 이 있는지 확인
      if (arr[i+1] == 'j') sum--;  // 그리고 다음문자에 'j' 가 있다면 크로아티아 문자라는 뜻이니 sum 에서 차감.
    }
    else if (arr[i] =='d'){  // 문자에 d 가 있다면
      if( arr[i+1] == '-') sum--;  // 다음 문자에 - 가 있는지 확인후 있다면 sum 차감
      else if (arr[i+1] == 'z' && arr[i+2] == '=') sum--; // 만약 - 가 아닌 z 가 있다면 그 다음 문자에 = 가 있는지 확인 둘다 있다면 sum 차감
    }
  }

  printf("%d\n", sum); // 처음 문자 길이에서 sum 차감한 갯수만큼 출력.
  
  return 0;
}


```
