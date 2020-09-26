#ifndef __queue__
#define __queue__

#include "link_list.hpp"

typedef struct Queue {
    void PushBack(int);
    void PopFront();
    void Print();
    int Top();
    bool Empty();
    int size_;
    Node *head_;
    Node *tail_;
}Queue;

#endif