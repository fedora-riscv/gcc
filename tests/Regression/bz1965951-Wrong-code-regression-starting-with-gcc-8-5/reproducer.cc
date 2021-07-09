#include <iostream>
struct S1 { virtual ~S1() = default; };
struct S2 { virtual void f1() = 0; };
struct S3: S1, S2 {
    void f1() { f2(); }
    virtual void f2() = 0;
};
struct S4: S3 {
    void f2() { std::cout << "called\n"; }
    using S2::f1;
};
int main() { S4().f1(); }
