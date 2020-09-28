#ifndef __link_list__
#define __link_list__

typedef struct Node{
    int val;
    Node *next;
}Node;


void Print(const Node *, char t);
Node *AddNode2Head(Node **, int);
Node *AddNode2Last(Node **, int);
Node *Push(Node *&, int);
Node *SortList(Node **);
Node *InsertNode(Node **, const Node *, int);

#endif
