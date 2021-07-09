#include <omp.h>
int main ()
{
  #pragma omp parallel for schedule(dynamic)
  for (int i = 0; i < 10; i++);
}
