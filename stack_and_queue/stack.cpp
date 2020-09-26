#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "stack.hpp"

void Stack::Push(int val) {
    Node *tmp = (Node *)malloc(sizeof(Node));
    if (tmp==NULL) {
        printf("Cannot allocate a new memory.\n");
        return;
    }
    tmp->val = val;
    tmp->next = head_;
    head_ = tmp;
    size_ += 1;
}

void Stack::Pop() {
    Node *cur = head_;
    head_ = head_->next;
    size_ -= 1;
    free(cur);
}

int Stack::Top() {
    assert(head_!=NULL);
    return head_->val;
}

bool Stack::Empty() {
    return true?size_<=0:false;
}

void Stack::Print() {
    Node *cur = head_;
    while (cur!=NULL)
    {
        printf("%d ", cur->val);
        cur = cur->next;
    }
    printf("\n");
}