#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "queue.hpp"

void Queue::PushBack(int val) {
    Node *tmp = (Node *)malloc(sizeof(Node));
    tmp->val = val;
    tmp->next = NULL;

    if (head_==NULL) {
        head_ = tmp;
        tail_ = tmp;
    }
    else {
        tail_->next = tmp;
        tail_ = tmp;
    }
    size_ += 1;
}

void Queue::PopFront() {
    Node *tmp = head_;
    head_ = head_->next;
    size_ -= 1;
    
    free(tmp);
}

int Queue::Top() {
    assert(head_!=NULL);
    return head_->val;
}

void Queue::Print() {
    Node *cur = head_;
    while (cur!=NULL)
    {
        printf("%d ", cur->val);
        cur = cur->next;
    }
    printf("\n");
}

bool Queue::Empty() {
    return true?size_<=0:false;
}
