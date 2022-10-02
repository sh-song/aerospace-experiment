int cdsPin = A1;
void setup() { Serial.begin(9600);
}
void loop() {
int val = analogRead(cdsPin); Serial.println(val);
delay(100);
}