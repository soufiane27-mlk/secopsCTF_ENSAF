#include <stdio.h>
#include <string.h>
#include <unistd.h>

struct __attribute__((__packed__)) data {
  char buf[32];
  int guard1;
  int guard2;
};

void ignore(void)
{
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);
}

void get_flag(void)
{
  char flag[1024] = { 0 };
  FILE *fp = fopen("flag.txt", "r");
  fgets(flag, 1023, fp);
  printf(flag);
}

int main(void) 
{
  struct data second_words;
  ignore(); /* ignore this function */

  printf("Salam labass 3lik, Hada challenge Sahel ghir 9ra lcode mzian ?\n");
  fgets(second_words.buf, 64, stdin);
  sleep(2);
	puts("Ohh anchufo wach atjib lflag Ohhhhh.....");
	sleep(2);
	puts("3... 2... 1...");
	sleep(2);

  if (second_words.guard1 == 0xdeadbeef && second_words.guard2 == 0x0badc0de) {
    get_flag();
  }
  else {
    printf("Hardluck, 9ra chwia 3la structure de donnee");
  }

  return 0;
}
