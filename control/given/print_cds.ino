int CWPin = 3;
int CCWPin = 4;
int motorSpeedPin = 5; int cdsPin = A1;
void setup() {
pinMode(CWPin, OUTPUT); pinMode(CCWPin, OUTPUT); pinMode(motorSpeedPin, OUTPUT); Serial.begin(9600); digitalWrite(CWPin, LOW); digitalWrite(CCWPin, HIGH); analogWrite(motorSpeedPin, 100);
}
void loop() {
int val = analogRead(cdsPin);
Serial.println(val); delay(50);
}