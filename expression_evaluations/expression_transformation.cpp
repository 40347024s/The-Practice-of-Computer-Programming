#include <cstdio>
#include <cstdlib>
#include <cctype>
#include <cstring>
#include "stack.hpp"
#include "expression_transformation.hpp"

char *Infix2Postfix(char expr[]) {
    Stack s = {.head_=NULL, .size_=0};

    return expr;
}

int EvaluatePostfix(const char expr[], int size) {
    Stack s = {.size_=0, .head_=NULL};
    for (int i = 0; i < size; i++)
    {
        if (isdigit(expr[i])) {
            s.Push(expr[i]-'0');
        }
        else {
            switch (expr[i])
            {
                case '+':
                {
                    int rval = s.Top();
                    s.Pop();
                    int lval = s.Top();
                    s.Pop();
                    s.Push(lval + rval);
                }
                    break;
                case '-':
                {
                    int rval = s.Top();
                    s.Pop();
                    int lval = s.Top();
                    s.Pop();
                    s.Push(lval - rval);
                }
                    break;
                case '*':
                {
                    int rval = s.Top();
                    s.Pop();
                    int lval = s.Top();
                    s.Pop();
                    s.Push(lval * rval);
                }
                    break;
                case '/':
                {
                    int rval = s.Top();
                    s.Pop();
                    int lval = s.Top();
                    s.Pop();
                    s.Push(lval / rval);
                }
                    break;
                default:
                {
                    printf("Type Error: Unknown operator type.\n");
                    exit(-1);
                }
                    break;
            }
        }
    }
    
    return s.Top();
}

