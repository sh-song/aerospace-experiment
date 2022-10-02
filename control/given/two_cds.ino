#define MotorSpeedPin 5 // PWM control
#define CCWPin 4 // counter clockwise
#define CWPin 3 // clockwise
#define Cds1Pin A1 // photo resistor(Main CDS sensor)
#define Cds2Pin A3 // photo resistor(Sub CDS sensor)
/* parameters */
int motorSpeedVal = 0; // PWM
int Cds1Val = 0; // photo resistor(CdS sensor) value
int Cds2Val = 0; // photo resistor(CdS sensor) value
int PreCdsVal = 0; // previous step CdS sensor value
int MotorDir = 0; // Motor direction of rotation(CW or CCW) trigger, if MotorDir = 1, CW

void setup() {
    pinMode(MotorSpeedPin, OUTPUT);
    pinMode(CCWPin, OUTPUT);//counter clockwise 
    pinMode(CWPin, OUTPUT);//clockwise
    Serial.begin(9600);
}

void loop() { 
    LP_MODE(); 
    delay(50);
}

void motor_R(int motorPWM) {
    analogWrite(MotorSpeedPin, motorPWM);
}

void motorCW() { 
    digitalWrite(CWPin, HIGH); 
    digitalWrite(CCWPin, LOW);
}

void motorCCW() {
    digitalWrite(CWPin, LOW);
    digitalWrite(CCWPin, HIGH);
}

int Cds1_read() {
    return analogRead(Cds1Pin);
}
int Cds2_read() {
    return analogRead(Cds2Pin);
}

void LP_MODE() {
    int Bright1lf = 120;
    int Bright2lf = 200;
    Cds1Val = Cds1_read(); //read the sensor 1 data
    Cds2Val = Cds2_read(); //read the sensor 2 data
    Serial.print(Cds1Val);
    Serial.print(",");
    Serial.println(Cds2Val);

    /*scanning motion*/
    if ((motorSpeedVal == 0) && (Cds1Val > Bright1lf && Cds2Val > Bright2lf)) {
        motorCW();
        motor_R(200);
    }

    /*cmd motor*/
    if (Cds1Val > Bright1lf && Cds2Val <= Bright2lf)
        motorCW();
    if (Cds1Val <= Bright1lf && Cds2Val > Bright2lf)
        motorCCW();

    if (Cds1Val <= Bright1lf || Cds2Val <= Bright2lf) {
        motorSpeedVal = 150;
    } else {
        motorSpeedVal = 200;
    }

    motor_R(motorSpeedVal);
}