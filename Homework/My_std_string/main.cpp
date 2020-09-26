#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "String.h"

using namespace std;

String foo () {
    String temp = " test ";
    return temp;
}

int main(int argc, const char * argv[]) {
    String mystring1,mystring2("World"); //default ctor
    String mystring4[2] = {mystring2,mystring1}; //copy ctor
    mystring1 += "Hello ";
    mystring1 += mystring2;
    String mystring3(mystring1); //copy ctor
    printf("my1: %s(%lu)\nmy2: %s(%lu)\nmy3: %s(%lu)\n",mystring1.c_str(), mystring1.size(), mystring2.c_str(), mystring2.size(), mystring3.c_str(), mystring3.size());
    printf("my4: %s(%lu)\n",mystring4[1].c_str(), mystring4[1].size());
    printf("After swap...\n");
    mystring1.swap(mystring2);
    printf("my1: %s(%lu)\nmy2: %s(%lu)\nmy3: %s(%lu)\n",mystring1.c_str(), mystring1.size(), mystring2.c_str(), mystring2.size(), mystring3.c_str(), mystring3.size());
    printf("After assignment...\n");
    mystring1 = mystring2; //copy assignment
    mystring2 = "Hello Moto";
    mystring3 = 'x';
    mystring4[0] = foo();
    printf("my1: %s(%lu)\nmy2: %s(%lu)\nmy3: %s(%lu)\n",mystring1.c_str(), mystring1.size(), mystring2.c_str(), mystring2.size(), mystring3.c_str(), mystring3.size());
    printf("my4: %s(%lu)\n",mystring4[0].c_str(), mystring4[0].size());
    printf("After plus...\n");
    mystring1 = mystring1 + foo();
    //mystring1 = mystring1 + "test";
    printf("my1: %s(%lu)\nmy2: %s(%lu)\nmy3: %s(%lu)\n",mystring1.c_str(), mystring1.size(), mystring2.c_str(), mystring2.size(), mystring3.c_str(), mystring3.size());
    printf("After null character...\n");
    mystring1[4] = '\0';
    mystring2 = mystring1 + mystring3;
    mystring3 += mystring1;
    cout << "my1: " << mystring1 << "(" << mystring1.size() << ")" << endl << "my2: " << mystring2 << "(" << mystring2.size() << ")" << endl << "my3: " << mystring3 << "(" << mystring3.size() << ")" << endl;
    printf("Compare(==)...\n");
    char test[50] = "Hello World test ";
    test[4] = '\0';
    printf("com1 == com2? %d\n",mystring1==mystring2);
    printf("com1 == str? %d\n",mystring1=="");
    printf("str == com1? %d\n",test==mystring1);
    mystring2 = "Hello World test ";
    test[4] = 'o';
    printf("str == com2? %d\n",test==mystring2);
    printf("Compare(>)...\n");
    strcpy(test, "Hello World test ");
    test[4] = '\0';
    cout << "my1: " << mystring1 << endl;
    cout << "my2: " << mystring2 << endl;
    printf("com1 > com2? %d\n",mystring1>mystring2);
    printf("com1 > str? %d\n",mystring1>"");
    printf("str > com1? %d\n",test>mystring1);
    test[4] = 'o';
    printf("str > com2? %d\n",test>mystring2);
    printf("Compare(<)...\n");
    strcpy(test, "Hello World test ");
    test[4] = '\0';
    printf("com1 < com2? %d\n",mystring1<mystring2);
    printf("com1 < str? %d\n",mystring1<"");
    printf("str < com1? %d\n",test<mystring1);
    test[4] = 'o';
    printf("str < com2? %d\n",test<mystring2);
    mystring2[4] = '\0';
    printf("com1 < com2? %d\n",mystring1<mystring2);
    printf("Compare(<=)...\n");
    strcpy(test, "Hello World test ");
    test[4] = '\0';
    printf("com1 <= com2? %d\n",mystring1<=mystring2);
    printf("com1 <= str? %d\n",mystring1<="");
    printf("str <= com1? %d\n",test<=mystring1);
    test[4] = 'o';
    printf("str <= com2? %d\n",test<=mystring2);
    printf("Compare(>=)...\n");
    strcpy(test, "Hello World test ");
    test[4] = '\0';
    printf("com1 >= com2? %d\n",mystring1>=mystring2);
    printf("com1 >= str? %d\n",mystring1>="");
    printf("str >= com1? %d\n",test>=mystring1);
    test[4] = 'o';
    printf("str >= com2? %d\n",test>=mystring2);
    printf("Compare(!=)...\n");
    strcpy(test, "Hello World test ");
    test[4] = '\0';
    printf("com1 != com2? %d\n",mystring1!=mystring2);
    printf("com1 != str? %d\n",mystring1!="");
    printf("str != com1? %d\n",test!=mystring1);
    test[4] = 'o';
    printf("str != com2? %d\n",test!=mystring2);
    mystring1 += mystring1 + mystring1;
    cout << "my1: " << mystring1 << "(" << mystring1.size() << ")" << endl;
    return 0;
}
