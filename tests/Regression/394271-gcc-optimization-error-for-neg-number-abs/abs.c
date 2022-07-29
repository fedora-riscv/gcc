#include <stdio.h>
#include <stdlib.h>

int
main ()
{
  int i = 2;
  if (-10 * abs (i - 1) == 10 * abs (i - 1))
    return 1;

  return 0;
}
