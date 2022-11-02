#define MotorSpeedPin 5 // PWM control
#define CCWPin 4 // counter clockwise
#define CWPin 3 // clockwise
//TODO : in arduino, int => int8_t
static const int A1= 55;
static const int A3= 57;
#define Cds1Pin A1 // photo resistor(Main CDS sensor)
#define Cds2Pin A3 // photo resistor(Sub CDS sensor)
#define PI 3.1415926535

#include <thread>
#include <chrono>
#include <cmath>
#include <iostream>

class Cds {
private:
    int pin_;
    double radius_;
    double area_;
    int raw_[3]  = {0, 0, 0};
    int est_[2] = {0, 0};
public:
    Cds(int pin, double radius) { //TODO: int pin => uint8_t pin
        pin_ = pin;
        radius_ = radius;
        area_ = radius * radius * PI;
    };
    
    void update() {
        raw_[0] = raw_[1];
        raw_[1] = raw_[2];
        //raw_[2] = analogRead(pin_); TODO
        raw_[2] +=7;
        if (raw_[2]>1024){
            std::cout << "--------end-----------" <<std::endl;
        }
    };

    void estimate() { //moving avg
        est_[0] = est_[1];

        int tmp = 0;
        for (int i=0; i<2; ++i) {
            tmp += (raw_[i] / 3);
        };
        est_[1] = tmp;            
    };

    void get_data(int* arr){
        arr[0] = est_[0];
        arr[1] = est_[1];
    }
};

// class Motor {
// private:
//         int dir; //0==ccw, 1==cw
//         int speedVal; // PWM

// public:
//     Motor(int _dir, int _speedVal) {
//         dir = -1; //init
//         speedVal = 0; //init
//     };

//     void setCCW() {
//         dir = 0;
//     };

//     void setCW() {
//         dir = 1;
//     };

//     void setSpeed(int _speedVal) {
//         speedVal = _speedVal;
//     };

//     void write() {
//         //speed
//         analogWrite(MotorSpeedPin, this->speedVal);

//         if (this->dir == 0) {
//             //ccw
//             digitalWrite(CWPin, LOW);
//             digitalWrite(CCWPin, HIGH);
//         }
//         else if (this->dir == 1) {
//             digitalWrite(CWPin, HIGH); 
//             digitalWrite(CCWPin, LOW);
//         } else {
//         cout << "something went wrong..." << endl;
//         }
//     };

// };


class MPU {
private:



}

class Gradient {
private:
    double gain_;
    double prev_norm_;
    double cur_norm_;
    double grad_;
    double stepsize;

    double calc_norm_(double n1, double n2) {
        double out = n1*n1 + n2*n2;
        out = sqrt(out);
        return out;
    };

public:
    Gradient(double gain){
        gain_ = gain;
    };

    double get_stepsize(int c1[], int c2[]) {
        prev_norm_ = calc_norm_(double(c1[0]), double(c2[0]));
        cur_norm_ = calc_norm_(c1[1], c2[1]);
        std::cout << "\nprev_norm" << std::endl;
        std::cout << prev_norm_ << std::endl;
        std::cout << "cur_norm" << std::endl;
        std::cout << cur_norm_ << std::endl;
        
        grad_ = cur_norm_ - prev_norm_;
        stepsize = grad_ * gain_;
        return stepsize;
    }
};


int main() {
    
    // Setup
    // Motor motor();
    Cds cds1(Cds1Pin, 3.3);
    Cds cds2(Cds2Pin, 1.1);
    Gradient gradient(0.1);
    int c1[2] = {0, 0};
    int c2[2] = {0, 0};
    double stepsize;

    // Loop
    while (1) {
        
        std::this_thread::sleep_for(std::chrono::milliseconds(200));
        cds1.update();
        cds2.update();

        cds1.estimate();
        cds2.estimate();

        cds1.get_data(c1); //0==prev, 1==cur
        cds2.get_data(c2);

        stepsize = gradient.get_stepsize(c1, c2);


        std::cout << "stepsize" << std::endl;
        std::cout << stepsize << std::endl;

        //TODO::: motor input

   };
    return 0;
}
