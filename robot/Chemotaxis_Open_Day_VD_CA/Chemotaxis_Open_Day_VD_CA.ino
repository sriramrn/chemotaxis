#include <Servo.h>

Servo servoleft;
Servo servoright;

int Runduration = 2000; //max duration of run in milliseconds
int Runvelocity = 100;  //PWM shift from 'zero' for max velocity

int Tumbletime = 2400;  //duration for one complete rotation at max velocity

int EnableSensor = 9;
int Lightsensor = 0;
int Value = 0;
int Range = 900;
int Offset = 550;

int xpin = 1;
int xval = 0;
int xthresh = 3;

void setup() {
  pinMode(EnableSensor,OUTPUT);
  Serial.begin(9600); 
}

void loop() {
  while (Value<1000)
  {
    Tumble();
    Run();
  } 
}

void Run() {
  
  digitalWrite(EnableSensor,HIGH);
  delay(50);
  Value = analogRead(Lightsensor);
  digitalWrite(EnableSensor,LOW);
  int RD = int(Runduration-Runduration*(float(Value-Offset)/float(Range-Offset)));
  int RV = int(Runvelocity-Runvelocity*(float(Value-Offset)/float(Range-Offset)));
    
  if (RD<0)
  {RD=0;}
  if (RV<40)
  {RV=40;}
  
  Serial.println("Sensor Value = "+String(Value)+"\nRun Duration = "+String(RD)+"\nRun Velocity = "+String(RV)+"\n\n");
  
  servoleft.attach(12);
  servoright.attach(13);
  servoleft.writeMicroseconds(1500+RV);
  servoright.writeMicroseconds(1500-RV);

  if (Value < Range-0.5*(Range-Offset)) {
    int rdby6= int(RD/6)+36;
    for (int i=0; i<6; i++)
    {
      xval=analogRead(xpin);
      if (xval>=xthresh) {rdby6 = 0; Serial.println("Collision Alert");} 
      delay(rdby6);    
    }
  }
  else {
    delay(RD);
  }
  
  servoleft.detach();
  servoright.detach();
  
}


void Tumble() {
  servoleft.attach(12);
  servoright.attach(13);
  int dir = int(random(0,2));
  if (dir==1)
  {
  servoleft.writeMicroseconds(1550);
  servoright.writeMicroseconds(1550);
  }
  else
  {
  servoleft.writeMicroseconds(1450);
  servoright.writeMicroseconds(1450);
  }
  delay(int(random(0,Tumbletime)));
  servoleft.detach();
  servoright.detach();
}
