#ifndef __My_std_string__String__
#define __My_std_string__String__

#include <stdio.h>
#include <string.h>
#include <algorithm>

class String {
public:
    String ();
    String (const String &str);
    String (const char s[]);
    ~String () {delete [] str_;};
    size_t size() const {return size_;};
    const char *c_str() const {return str_;};
    char &operator[] (size_t pos);
    const char &operator[] (size_t pos) const;
    String &operator += (const String &str);
    String &operator += (const char s[]);
    String &operator += (char c);
    void clear();
    String &operator = (const String &str);
    String &operator = (const char s[]);
    String &operator = (char c);
    void swap (String &str);
    
private:
    char *str_ = nullptr;
    size_t capacity_ = 0, size_ = 0;
};

String operator + (const String &lhs, const String &rhs);
String operator + (const String &lhs, const char rhs[]);
String operator + (const char lhs[], const String &rhs);
String operator + (const String &lhs, char rhs);
String operator + (char lhs, const String &rhs);
std::ostream &operator << (std::ostream &os, const String &str);
bool operator < (const String &lhs, const String &rhs);
bool operator < (const char lhs[], const String &rhs);
bool operator < (const String &lhs, const char rhs[]);
bool operator > (const String &lhs, const String &rhs);
bool operator > (const char lhs[], const String &rhs);
bool operator > (const String &lhs, const char rhs[]);
bool operator <= (const String &lhs, const String &rhs);
bool operator <= (const char lhs[], const String &rhs);
bool operator <= (const String &lhs, const char rhs[]);
bool operator >= (const String &lhs, const String &rhs);
bool operator >= (const char lhs[], const String &rhs);
bool operator >= (const String &lhs, const char rhs[]);
bool operator == (const String &lhs, const String &rhs);
bool operator == (const char lhs[], const String &rhs);
bool operator == (const String &lhs, const char rhs[]);
bool operator != (const String &lhs, const String &rhs);
bool operator != (const char lhs[], const String &rhs);
bool operator != (const String &lhs, const char rhs[]);

#endif /* defined(__My_std_string__String__) */
