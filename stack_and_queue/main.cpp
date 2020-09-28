#include <stdio.h>
#include <stdlib.h>
#include "stack.hpp"
#include "queue.hpp"
#include "link_list.hpp"

int main() {
    printf("=========== Link List =============\n");
    Node *stack = NULL;
    Node *queue = NULL;
    int arr[10] = {0,5,9,8,4,1,6,7,3,2};
    for (int i = 0; i < 10; i++)
    {
        AddNode2Head(&stack, arr[i]);
        Print(stack, 's');
    }
    Push(stack, 30);
    Print(stack, 's');
    for (int i = 0; i < 10; i++)
    {
        AddNode2Last(&queue, arr[i]);
        Print(queue, 'q');
    }
    Node node = {.val=999, .next=NULL};
    InsertNode(&queue, &node, 2);
    Print(queue, 'q');
    node.val = 888;
    InsertNode(&queue, &node, 1);
    Print(queue, 'q');
    node.val = 777;
    InsertNode(&queue, &node, 0);
    Print(queue, 'q');
    node.val = 666;
    InsertNode(&queue, &node, 100);
    Print(queue, 'q');
    node.val = 555;
    Node *empty_head = NULL;
    InsertNode(&empty_head, &node, 100);
    Print(empty_head, 's');
    SortList(&queue);
    Print(queue, 'q');
    printf("=========== My Stack =============\n");
    Stack s = {.size_ = 0, .head_ = NULL};
    for (int i = 0; i < 10; i++)
    {
        s.Push(i*2);
        printf("After push %d, size is %d\ncurrent stack: ", i*2, s.size_);
        s.Print();
    }
    while (!s.Empty())
    {
        int top = s.Top();
        s.Pop();
        printf("After pop %d, size is %d\ncurrent stack: ", top, s.size_);
        s.Print();
    }
    printf("=========== My Queue =============\n");
    Queue q = {.head_=NULL, .tail_=NULL, .size_=0};
    for (int i = 0; i < 10; i++)
    {
        q.PushBack(i*2);
        printf("After push_back %d, size is %d\ncurrent queue: ", i*2, q.size_);
        q.Print();
    }
    while (!q.Empty())
    {
        int top = q.Top();
        q.PopFront();
        printf("After pop_front %d, size is %d\ncurrent queue: ", top, q.size_);
        q.Print();
    }
    return 1;
}