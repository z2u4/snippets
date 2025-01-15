#include <iostream>
#include <cmath>

using namespace std;

class b2d{
    public:
    //var declaration
    int d;
    long long b;

    void decimal(int decimal){
        d = decimal;
        b = get_binary();
    }

    void binary(long long binary){
        b = binary;
        d = get_decimal();
    }
    private:
    //convert int to binary
    long long get_binary(){
        b = 0;
    int remainder, i = 1, step = 1;
    while (d!=0)
    {
        remainder = d%2;
        d /= 2;
        b += remainder*i;
        i *= 10;
    }
    return b;
    }
    //convert binary to int
    int get_decimal(){
             d = 0;
            int i = 0, remainder;
        while (b!=0)
            {
                    remainder = b%10;
                    b /= 10;
                    d += remainder*pow(2,i);
                    ++i;
            }
            return d;
    }
};


int main() {
    b2d x;
    x.binary(111110000);
    cout << x.d;
    x.decimal(344);
    cout << endl << x.b;