extern void *malloc (__SIZE_TYPE__) __attribute__((malloc,transaction_safe));

static int __attribute__((transaction_safe))
something (void)
{
  return 0;
}

struct large { int foo[500]; };

int
main (void)
{
  int *p;
  struct large *lp;

  __transaction_atomic {
    p = malloc (sizeof (*p) * 100);
    lp = malloc (sizeof (*lp) * 100);

    /* No instrumentation necessary; P and LP are transaction local.  */
    p[5] = 123;
    lp->foo[66] = 123;

    if (something ())
      __transaction_cancel;
  }

  __transaction_relaxed {
    ++p[5];
  }

  return ((p[5] == 124) ? 0 : 1);
}
