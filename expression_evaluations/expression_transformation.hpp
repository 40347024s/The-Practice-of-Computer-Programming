#ifndef __expression_transformation__
#define __expression_transformation__

#include "stack.hpp"
char *Infix2Postfix(char []);
int EvaluatePostfix(const char [], int);
#endif