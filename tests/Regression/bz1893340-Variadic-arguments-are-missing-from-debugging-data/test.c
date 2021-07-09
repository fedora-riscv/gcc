#include <stdarg.h>
void foo(int args, ...) {
    va_list ap;
    va_start(ap, args);
    va_end(ap);
}
