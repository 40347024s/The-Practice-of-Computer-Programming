#ifndef __stack__
#define __stack__

#include "link_list.hpp"

struct Stack {
public:
    void Push(int);
    void Pop();
    int Top();
    bool Empty();
    void Print();
    Node *head_;
    int size_;
};

#endif