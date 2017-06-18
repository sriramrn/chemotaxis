#include <Servo.h>

Servo servoleft;
Servo servoright;

int Runduration = 4800; //max duration of run in milliseconds
int Runvelocity = 100;  //PWM shift from 'zero' for max velocity

int Tumbletime = 2400;  //duration for one complete rotation at max velocity

int Runcounter  = 0;
int Runs = 100;

int Lightsensor = 0;
int Value = 0;
int Range = 842;
int Offset = 0;

float Scale_duration = Runduration/float(Range-Offset);

void setup() {
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
  Scale_duration = Runduration/float(Range-Offset);
  Value = analogRead(Lightsensor);
  int RD = int(Runduration-(Value*Scale_duration));
  if (RD<0)
  {RD=0;}
  servoleft.attach(12);
  servoright.attach(13);
  servoleft.writeMicroseconds(1500+Runvelocity);
  servoright.writeMicroseconds(1500-Runvelocity);
  delay(RD);
  servoleft.detach();
  servoright.detach();
  Offset = Value;
}


void Tumble() {
  servoleft.attach(12);
  servoright.attach(13);
  servoleft.writeMicroseconds(1600);
  servoright.writeMicroseconds(1600);
  delay(int(random(0,Tumbletime)));
  servoleft.detach();
  servoright.detach();
}
