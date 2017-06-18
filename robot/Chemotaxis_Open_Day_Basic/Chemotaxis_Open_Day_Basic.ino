#include <Servo.h>

Servo servoleft;
Servo servoright;

int Runduration = 2000; //max duration of run in milliseconds
int Runvelocity = 100;  //PWM shift from 'zero' for max velocity

int Tumbletime = 4800;  //duration for one complete rotation at max velocity

int Runcounter  = 0;
int Runs = 100;

int EnableSensor = 12;
int Lightsensor = 0;
int Value = 0;
int Range = 850;
int Offset = 550;

float Scale_duration = Runduration-Runduration*(float(Value-Offset)/float(Range-Offset));

void setup() {
  pinMode(EnableSensor,OUTPUT);
  Serial.begin(9600); 
}

void loop() {
  while (Runcounter<=Runs)
  {
    Tumble();
    Run();
  }
}

void Run() {
  Runcounter++;
  digitalWrite(EnableSensor,HIGH);
  delay(50);
  Value = analogRead(Lightsensor);
  digitalWrite(EnableSensor,LOW);
  int RD = int(Runduration-Runduration*(float(Value-Offset)/float(Range-Offset)));
  Serial.println(RD);
  if (RD<0)
  {RD=0;}
  servoleft.attach(12);
  servoright.attach(13);
  servoleft.writeMicroseconds(1500+Runvelocity);
  servoright.writeMicroseconds(1500-Runvelocity);
  delay(RD);
  servoleft.detach();
  servoright.detach();
}


void Tumble() {
  servoleft.attach(12);
  servoright.attach(13);
  servoleft.writeMicroseconds(1550);
  servoright.writeMicroseconds(1550);
  delay(int(random(0,Tumbletime)));
  servoleft.detach();
  servoright.detach();
}

// this provides a heartbeat on pin 9, when robot is happy :)
uint8_t hbval = 128;
int8_t hbdelta = 8;
void heartbeat() {
  if (hbval > 192) hbdelta = -hbdelta;
  if (hbval < 32) hbdelta = -hbdelta;
  hbval += hbdelta;
  analogWrite(LED_HB, hbval);
  delay(20);
}
