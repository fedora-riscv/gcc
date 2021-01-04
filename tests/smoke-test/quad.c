#include <quadmath.h>
#include <stdlib.h>
#include <stdio.h>

int
main (void)
{
  __float128 r = strtoflt128 ("1.23456789", NULL);

  int prec = 20;
  int width = 46;
  char buf[128];

  r = 2.0q;
  r = sqrtq (r);
  int n = quadmath_snprintf (buf, sizeof buf, "%+-#*.20Qe", width, r);
  if ((size_t) n < sizeof buf)
    /* Prints: +1.41421356237309504880e+00 */
    printf ("%s\n", buf);
  quadmath_snprintf (buf, sizeof buf, "%Qa", r);
  if ((size_t) n < sizeof buf)
    /* Prints: 0x1.6a09e667f3bcc908b2fb1366ea96p+0 */
    printf ("%s\n", buf);
  n = quadmath_snprintf (NULL, 0, "%+-#46.*Qe", prec, r);
  if (n > -1)
    {
      char *str = malloc (n + 1);
      if (str)
	{
	  quadmath_snprintf (str, n + 1, "%+-#46.*Qe", prec, r);
	  /* Prints: +1.41421356237309504880e+00 */
	  printf ("%s\n", str);
        }
      free (str);
    }

  return 0;
}
