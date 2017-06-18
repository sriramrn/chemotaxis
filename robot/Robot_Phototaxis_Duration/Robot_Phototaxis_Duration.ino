#include <Servo.h>

Servo servoleft;
Servo servoright;

int Runduration = 4800; //max duration of run in milliseconds
int Runvelocity = 100;  //PWM shift from 'zero' for max velocity

int Tumbletime = 2400;  //duration for one complete rotation at max velocity

int Runcounter  = 0;
int Runs = 100;

int EnableSensor = 12;
int Lightsensor = 0;
int Value = 0;
int Range = 900;
int Offset = 400;

float Scale_duration = Runduration/float(Range-Offset);

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
  int RD = int(Runduration-((Value-Offset)*Scale_duration));
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
  servoleft.writeMicroseconds(1600);
  servoright.writeMicroseconds(1600);
  delay(int(random(0,Tumbletime)));
  servoleft.detach();
  servoright.detach();
}
