int CWPin = 3;
int CCWPin = 4;
int motorSpeedPin = 5;
void setup() {
pinMode(CWPin, OUTPUT); pinMode(CCWPin, OUTPUT); pinMode(motorSpeedPin, OUTPUT);
Serial.begin(9600); }
void loop() { if(Serial.available()) {
char inputCmd = Serial.read();
switch case 'R':
(inputCmd) {
MotorRightMove();
break; case 'L':
MotorLeftMove();
break; case '1':
case '2': case '3':
MotorSpeedControl(inputCmd); break;
} }
}
void MotorRightMove() {
digitalWrite(CWPin, HIGH);
digitalWrite(CCWPin, LOW); }
void MotorLeftMove() { digitalWrite(CWPin, LOW); digitalWrite(CCWPin, HIGH);
}
void MotorSpeedControl(char inputChar) {
switch(inputChar){ case '1':
analogWrite(motorSpeedPin, 130);
break; case '2':
analogWrite(motorSpeedPin, 150);
break; case '3':
analogWrite(motorSpeedPin, 180);
break; }
}