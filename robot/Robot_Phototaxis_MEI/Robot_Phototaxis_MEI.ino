#include <Servo.h>

Servo servoleft;
Servo servoright;

int Runduration = 2500; //max duration of run in milliseconds
int Runvelocity = 100;  //PWM shift from 'zero' for max velocity

int init_Runduration = Runduration;

int Tumbletime = 2400;  //duration for one complete rotation at max velocity

int tumble_dist[]={963, 256, 561, 644, 323, 178, 963, 378, 304, 110, 394, 442, 269, 178, 93, 230, 512, 467, 342, 502, 1168, 396, 513, 
                   440, 429, 505, 376, 354, 711, 405, 770, 286, 358, 503, 343, 409, 243, 711, 167, 361, 502, 576, 509, 371, 449, 301,
                   535, 500, 689, 681, 801, 378, 99, 369, 197, 361, 80, 772, 608, 279, 150, 580, 675, 467, 309, 653, 631, 480, 689, 
                   512, 43, 485, 814, 223, 393, 143, 660, 437, 235, 610, 170, 660, 167, 723, 359, 230, 545, 465, 705, 428, 468, 314, 
                   670, 489, 597, 349, 215, 720, 170, 456, 610, 590, 228, 587, 283, 452, 444, 156, 570, 525, 374, 370, 645, 472, 76, 
                   236, 696, 184, 102, 571, 82, 574, 336, 50, 250, 623, 417, 352, 140, 354, 681, 428, 590, 521, 445, 893, 649, 373, 
                   560, 231, 373, 305, 786, 606, 537, 386, 273, 107, 529, 264, 86, 130, 439, 318, 234, 646, 329, 522, 591, 495, 443, 
                   534, 198, 517, 259, 564, 726, 439, 426, 179, 307, 584, 343, 257, 344, 373, 491, 177, 864, 542, 512, 598, 403, 230,
                   231, 509, 310, 233, 347, 574, 439, 269, 452, 280, 634, 552, 247, 443, 884, 722, 443, 646, 479, 457, 759, 55, 545, 
                   552, 650, 507, 262, 328, 390, 319, 419, 91, 264, 136, 390, 633, 534, 441, 622, 13, 335, 312, 167, 595, 440, 707, 
                   456, 593, 452, 780, 509, 559, 532, 257, 557, 314, 274, 448, 365, 416, 9, 618, 303, 584, 428, 362, 277, 213, 8, 213, 
                   525, 274, 272, 233, 557, 187, 642, 369, 551, 243, 188, 190, 435, 835, 500, 269, 258, 482, 345, 501, 770, 165, 549,
                   619, 573, 184, 169, 154, 408, 829, 267, 841, 405, 496, 483, 591, 647, 372, 656, 673, 520, 332, 299, 457, 366, 429,
                   269, 348, 517, 473, 712, 435, 352, 488, 303, 759, 483, 687, 561, 770, 494, 466, 252, 624, 590, 360, 685, 482, 316,
                   511, 359, 154, 423, 770, 347, 681, 181, 552, 551, 392, 402, 448, 270, 481, 587, 576, 377, 234, 362, 458, 150, 318, 
                   418, 221, 439, 373, 334, 422, 79, 629, 277, 350, 397, 284, 396, 476, 196, 277, 342, 510, 236, 447, 609, 151, 243,
                   563, 469, 374, 701, 581, 496, 394, 572, 238, 240, 396, 155, 555, 897, 417, 437, 443, 474, 417, 370, 5, 372, 447, 
                   118, 279, 219, 687, 53, 164, 35, 494, 663, 340, 362, 436, 540, 147, 666, 332, 662, 458, 92, 302, 315, 274, 444, 822,
                   658, 113, 758, 510, 358, 339, 234, 119, 295, 384, 351, 91, 396, 347, 146, 258, 420, 466, 340, 344, 443, 518, 179,
                   887, 316, 294, 382, 631, 403, 374, 246, 477, 806, 521, 766, 657, 202, 547, 299, 750, 475, 725, 378, 366, 351, 576,
                   347, 164, 668, 613, 461, 381, 289, 722, 792, 239, 508, 196, 343, 187, 404, 484, 309, 541, 453, 16, 385, 522, 536,
                   370, 176, 527, 393, 170, 639, 392, 765, 304, 524, 618, 554, 391, 615, 242};

int Runcounter  = 0;
int Runs = 100;

int Lightsensor = 0;
int Value = 0;
int Prev_value = 0;
int Range = 842;
int Offset = 0;

int index=0;

float Scale_duration = Runduration/float(Range-Offset);

void setup() {
}

void loop() {
  
  if (Runcounter==0)
  {RandomTumble();}
  
  while (Runcounter<=Runs)
  {
    SkewedTumble();
    Run();
  }
}

void Run() {
  Runcounter++;
  Value = analogRead(Lightsensor);
  if (Runcounter==1)
  {Prev_value==Value;}

  if (Value-Prev_value<0)
  {Runduration = init_Runduration-1500;}
  if (Value-Prev_value>0)
  {Runduration = init_Runduration+1500;}
  if (Runduration<0)
  {Runduration=0;}
  
  servoleft.attach(12);
  servoright.attach(13);
  servoleft.writeMicroseconds(1500+Runvelocity);
  servoright.writeMicroseconds(1500-Runvelocity);
  delay(Runduration);
  servoleft.detach();
  servoright.detach();
  
  Prev_value=Value;
}


void RandomTumble() {
  servoleft.attach(12);
  servoright.attach(13);
  servoleft.writeMicroseconds(1600);
  servoright.writeMicroseconds(1600);
  delay(int(random(0,Tumbletime)));
  servoleft.detach();
  servoright.detach();
}


void SkewedTumble() {
  servoleft.attach(12);
  servoright.attach(13);
  int lr=floor(random(0,2));
  if (lr==0){
  servoleft.writeMicroseconds(1600);
  servoright.writeMicroseconds(1600);
  }
  if (lr==1){
  servoleft.writeMicroseconds(1400);
  servoright.writeMicroseconds(1400);
  }
  index=int(random(0,499));
  Tumbletime=tumble_dist[index];
  delay(Tumbletime);
  servoleft.detach();
  servoright.detach();
}

