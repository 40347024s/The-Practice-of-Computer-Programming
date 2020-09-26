#include <cstdio>
#include <cstdlib>
#include <cstring>
#include "expression_transformation.hpp"

int main () {
    // char infix_expr[100] = "(a/(b-c+d))*(e-a)*c";
    // char postfix_expr[100] = "abc?d+/ea-*c*";
    char infix_expr[100] = "(8/(7-6+5))*(4-8)*6";
    char postfix_expr[100] = "876-5+/48-*6*";
    printf("%s = %d\n", postfix_expr, EvaluatePostfix(postfix_expr, strlen(postfix_expr)));
    return 0;
}