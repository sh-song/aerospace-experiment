
#include<Wire.h>
const int MPU6050 = 0x68; // MPU6050 i2c address
int AcX, AcY, AcZ, GyX, GyY, GyZ, Tmp; // 16 bit integer void setup() {
Wire.begin();
Wire.beginTransmission(MPU6050);
Wire.write(0x6B); // PWR_MGMT_1 register
Wire.write(0); // wakes up the MPU6050 Wire.endTransmission(true);
Serial.begin(9600);
}
void loop() {
Wire.beginTransmission(MPU6050);
Wire.write(0x3B); // starting with register ACCEL_XOUT_H Wire.endTransmission(false);
Wire.requestFrom(MPU6050, 14, true); // 14 bytes data AcX = Wire.read() << 8 | Wire.read();
AcY = Wire.read() << 8 | Wire.read();
AcZ = Wire.read() << 8 | Wire.read();
Tmp = Wire.read() << 8 | Wire.read();
GyX = Wire.read() << 8 | Wire.read();
GyY = Wire.read() << 8 | Wire.read();
GyZ = Wire.read() << 8 | Wire.read();
Serial.print(" AcX= "); Serial.print(AcX);
Serial.print(" AcY= "); Serial.print(AcY);
Serial.print(" AcZ= "); Serial.print(AcZ);
Serial.print(" Tmp= "); Serial.print(Tmp/340.00+36.53); Serial.print(" GyX= "); Serial.print(GyX);
Serial.print(" GyY= "); Serial.print(GyY);
Serial.print(" GyZ= "); Serial.print(GyZ);
delay(20);
}