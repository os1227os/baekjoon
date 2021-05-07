#include<stdio.h>
int main(){
	int user;
	int count = 0;
	
	scanf("%d", &user);
	
	while(user > 0){
		if(user % 5 == 0){
			user -=5;
			count++;
		}
		else if(user % 3 ==0){
			user -=3;
			count++;
		}
		else if(user > 5){
			user -=5;
			count++;
		}
		else{
			count = -1;
			break;
		}
		
	}
	printf("%d", count);
}
