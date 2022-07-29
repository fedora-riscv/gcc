template <bool C> int func (void);

template <class T> struct Foo
{
  static const unsigned int a = sizeof (T);

  //enum { b = a };

  enum
  {
    c = sizeof (func < (a == 0) > ())
  };
};

Foo <int> x;
