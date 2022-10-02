int CWPin = 3;
int CCWPin = 4;
int motorSpeedPin = 5; 
//Clockwise
void setup() {
pinMode(CWPin, OUTPUT); pinMode(CCWPin, OUTPUT); pinMode(motorSpeedPin, OUTPUT);
}
void loop() {
digitalWrite(CWPin, HIGH); digitalWrite(CCWPin, LOW); analogWrite(motorSpeedPin, 200);
}