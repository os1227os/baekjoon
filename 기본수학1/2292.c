#include <stdio.h>

long long num, ans= 1, check_number;  // 숫자의 범위가 10000000000이여서 longlong 으로 선언

int main(){
  scanf("%lld", &num); 
  for(int i=1; check_number*6+1<num;i++){ // 한바퀴씩 돌아보는 것을 for문으로 작성
    check_number += i;  // 한바퀴씩 돌때마다 check_number에 i를 더해줌 
    ans++; // 다음 바퀴로 갈때마다 정답에 1씩 더해준다.
  }
  printf("%lld\n", ans);

  return 0;

