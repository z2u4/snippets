#include <iostream>
#include <chrono>
#include <ctime> 
#include <stdexcept>
#include <thread>
using namespace std;

class StopWatch{
    long get_current_time(){
        //get current time
        auto current_time = std::chrono::system_clock::now();
        //current time conversion
        std::chrono::duration<double, std::milli> fp_ms = std::chrono::duration<double>(current_time.time_since_epoch());
        return fp_ms.count();
    }

    long start_time;
    long end_time;
    bool toggle;
public:
    StopWatch(){
        start_time = end_time =0;
    }

    void start(){
        start_time = get_current_time();
    }

    long end(){
        if(start_time == 0) throw std::invalid_argument( "invalid timer operation" );
        end_time = get_current_time();
        return end_time - start_time;
    }

    void delay_test(int seconds){
         std::this_thread::sleep_for (std::chrono::milliseconds(seconds));
    }
};

int main(){
    StopWatch x;
    x.start();
    x.delay_test(2);
    cout << x.end();
}