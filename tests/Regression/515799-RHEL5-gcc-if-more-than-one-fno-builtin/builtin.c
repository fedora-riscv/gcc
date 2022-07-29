#include <stdio.h>

/* Compile flags:
 *   gcc -fno-builtin-isascii -fno-builtin-isalnum -o builtin builtin.c
 *
 * Expected output:
 *   Using custom isascii() function
 *   ret = 0
 *
 * Expected return value:
 *   0
 */

int isascii(int c)
{
        printf("Using custom isascii() function\n");
        return 0;
}

main()
{
        int c = 65;
        int ret;

        ret = isascii(c);
        printf("ret = %d\n", ret);

        return ret;
}
