#include "String.h"
#include <iostream>

using namespace::std;

String::String (): capacity_(0), size_(0){
    str_ = new char[capacity_+1];
    str_[0] = '\0';
}
String::String (const String &str): capacity_(str.capacity_), size_(str.size()){
    str_ = new char[capacity_+1];
    for ( int i=0 ; i<size_ ; i+=1 )
        str_[i] = str[i];
    str_[size_] = '\0';
}
String::String (const char s[]): capacity_(strlen(s)), size_(strlen(s)){
    if (s==nullptr)
        s = "";
    str_ = new char[capacity_+1];
    for ( int i=0 ; i<size_ ; i+=1 )
        str_[i] = s[i];
    str_[size_] = '\0';
}
char &String::operator[] (size_t pos) { return const_cast<char &>(static_cast<const String &>(*this)[pos]); }
const char &String::operator[] (size_t pos) const {
    if (pos>=size_)
        return str_[size_];
    else
        return str_[pos];
}
String &String::operator += (const String &str) {
    if (capacity_-size_ <= str.size()) {
        capacity_ += str.size();
        char *temp = new char[capacity_+1];
        for ( int i=0 ; i<size_ ; i+=1 )
            temp[i] = str_[i];
        temp[size_] = '\0';
        delete [] str_;
        str_ = temp;
    }
    for ( int i=0 ; i<str.size() ; i+=1 )
        str_[size_+i] = str[i];
    size_ += str.size();
    str_[size_] = '\0';
    return (*this);
}
String &String::operator += (const char s[]) {
    if (capacity_-size_ <= strlen(s)) {
        capacity_ += strlen(s);
        char *temp = new char[capacity_+1];
        for ( int i=0 ; i<size_ ; i+=1 )
            temp[i] = str_[i];
        temp[size_] = '\0';
        delete []str_;
        str_ = temp;
    }
    for (int i=0 ; i<strlen(s) ; i+=1 )
        str_[size_+i] = s[i];
    size_ += strlen(s);
    str_[size_] = '\0';
    return (*this);
}
String &String::operator += (char c) {
    if (capacity_<=size_) {
        capacity_ += 1;
        char *temp = new char[capacity_+1];
        for ( int i=0 ; i<size_ ; i+=1 )
            temp[i] = str_[i];
        temp[size_] = '\0';
        delete [] str_;
        str_ = temp;
    }
    str_[size_] = c;
    size_ += 1;
    str_[size_] = '\0';
    return (*this);
}
void String::clear() {
    size_ = 0;
    str_[size_] = '\0';
}
String &String::operator = (const String &str) {
    String temp = str;
    temp.swap(*this);
    return (*this);
}
String &String::operator = (const char s[]) {
    if (capacity_ < strlen(s)) {
        capacity_ = strlen(s);
        delete str_;
        str_ = new char[capacity_+1];
    }
    size_ = strlen(s);
    for ( int i=0 ; i<size_ ; i+=1 )
        str_[i] = s[i];
    str_[size_] = '\0';
    return (*this);
}
String &String::operator = (char c) {
    if (capacity_ < 1) {
        capacity_ = 1;
        delete str_;
        str_ = new char[capacity_+1];
    }
    size_ = 1;
    str_[0] = c;
    str_[1] = '\0';
    return (*this);
}
void String::swap (String &str) {
    std::swap(str_, str.str_);
    std::swap(size_, str.size_);
    std::swap(capacity_, str.capacity_);
}


String operator + (const String &lhs, const String &rhs) {
    String temp(lhs);
    return temp += rhs;
}
String operator + (const String &lhs, const char rhs[]) {
    String temp(rhs);
    return lhs + temp;
}
String operator + (const char *lhs, const String &rhs) {
    String temp(lhs);
    return temp + rhs;
}
String operator + (const String &lhs, char rhs) {
    String temp;
    temp += rhs;
    return lhs + temp;
}
String operator + (char lhs, const String &rhs) {
    String temp;
    temp += lhs;
    return temp + rhs;
}
std::ostream &operator << (std::ostream &os, const String &str) {
    for ( int i=0 ; i<str.size() ; i+=1 )
        cout << str.c_str()[i];
    
    return os;
}
bool operator < (const String &lhs, const String &rhs) {
    int index = 0;
    while (index<lhs.size() && index<rhs.size()) {
        if (lhs[index] < rhs[index])
            return true;
        else if (lhs[index] > rhs[index])
            return false;
        index += 1;
    }
    if (index==lhs.size() && index<rhs.size())
        return true;
    else
        return false;
}
bool operator < (const char lhs[], const String &rhs) {
    String temp(lhs);
    return temp < rhs;
}
bool operator < (const String &lhs, const char rhs[]) {
    String temp(rhs);
    return lhs < temp;
}
bool operator > (const String &lhs, const String &rhs) {
    int index = 0;
    while (index<lhs.size() && index<rhs.size()) {
        if (lhs[index] > rhs[index])
            return true;
        index += 1;
    }
    if (index<lhs.size() && index==rhs.size())
        return true;
    else
        return false;
}
bool operator > (const char lhs[], const String &rhs) {
    String temp(lhs);
    return temp > rhs;
}
bool operator > (const String &lhs, const char rhs[]) {
    String temp(rhs);
    return lhs > temp;
}
bool operator <= (const String &lhs, const String &rhs) {
    return !(lhs > rhs);
}
bool operator <= (const char lhs[], const String &rhs) {
    return !(lhs > rhs);
}
bool operator <= (const String &lhs, const char rhs[]) {
    return !(lhs > rhs);
}
bool operator >= (const String &lhs, const String &rhs) {
    return !(lhs < rhs);
}
bool operator >= (const char lhs[], const String &rhs) {
    return !(lhs < rhs);
}
bool operator >= (const String &lhs, const char rhs[]) {
    return !(lhs < rhs);
}
bool operator == (const String &lhs, const String &rhs) {
    return !(lhs != rhs);
}
bool operator == (const char lhs[], const String &rhs) {
    return !(lhs != rhs);
}
bool operator == (const String &lhs, const char rhs[]) {
    return !(lhs != rhs);
}
bool operator != (const String &lhs, const String &rhs) {
    int index = 0;
    while (index<lhs.size() && index<rhs.size()) {
        if (lhs[index]!=rhs[index])
            return true;
        index += 1;
    }
    if (index==lhs.size() && index==rhs.size())
        return false;
    else
        return true;
}
bool operator != (const char lhs[], const String &rhs) {
    String temp(lhs);
    return temp!=rhs;
}
bool operator != (const String &lhs, const char rhs[]) {
    String temp(rhs);
    return lhs!=temp;
}