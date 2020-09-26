#include <stdio.h>
#include <stdlib.h>
#include "link_list.hpp"

void Print(const Node *head, char c) {
    if (c=='s') {
        printf("Current stack: ");
    }
    else if (c=='q') {
        printf("Current queue: ");
    }
    else {
        printf("Current list: ");
    }
    while (head!=NULL)
    {
        printf("%d ", head->val);
        head = head->next;
    }
    printf("\n");
    
}

Node *AddNode2Head(Node **head, int val) {
    Node *tmp = (Node *)malloc(sizeof(Node));
    tmp->val = val;
    tmp->next = *head;
    *head = tmp;

    return *head;
}

Node *AddNode2Last(Node **head, int val) {
    Node *tmp = (Node *)malloc(sizeof(Node));
    tmp->val = val;
    tmp->next = NULL;
    Node *cur = *head;
    if (cur==NULL) {
        *head = tmp;
    }
    else {
        while (cur->next!=NULL)
        {
            cur = cur->next;
        }
        cur->next = tmp;
    }
    
    return *head;
}

Node *Push(Node *&head, int val) {
    Node *tmp = (Node *)malloc(sizeof(Node));
    tmp->val = val;
    tmp->next = head;
    head = tmp;

    return head;
}

Node *SortList(Node **head) {
    Node *new_head = NULL;
    Node *max_node = *head;
    Node *max_prev_node = *head;
    Node *cur = *head;
    Node *prev = *head;
    while (*head!=NULL)
    {
        if (cur->val > max_node->val) {
            max_node = cur;
            max_prev_node = prev;
        }
        prev = cur;
        cur = cur->next;
        if (cur==NULL) {
            if (max_node!=*head) {
                max_prev_node->next = max_node->next;
            }
            else {
                *head = max_node->next;
            }
            max_node->next = new_head;
            new_head = max_node;

            cur = *head;
            prev = *head;
            max_prev_node = *head;
            max_node = *head;
        }
    }
    *head = new_head;
    return *head;
}
Node *InsertNode(Node **head, const Node *node, int index) {
    Node *cur = *head, *prev = *head;
    for (int i = 0; i < index; i++)
    {
        if (cur==NULL) {
            break;
        }
        prev = cur;
        cur = cur->next;
    }
    Node *tmp = (Node *)malloc(sizeof(Node));
    tmp->val = node->val;
    if (prev==NULL && cur==NULL) {
        *head = tmp;
    }
    else {
        if (index==0) {
            tmp->next = prev;
            *head = tmp;
        }
        else {
            tmp->next = prev->next;
            prev->next = tmp;
        }
    }
    return *head;
}