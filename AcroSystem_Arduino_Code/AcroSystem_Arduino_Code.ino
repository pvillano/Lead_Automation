/*
 * Author: Patrick McGuire
 * Date: 17 April 2019
 */



// connect these ports to given pins
//motor 1 - x dir
const int dirPin  = 3; //dir+ to 3
const int stepPin = 4; //pul+ to 4
const int enPin   = 5; //en+ to 5

// lengthwise motors 
//motors 2 and 3 - y dir
const int dirPinLong = 6; //dir+ to 6
const int stepPinLong = 7; //pul+ to 7
const int enPinLong = 10; //en+ to 10

//all dir- to gnd

int current_x = 0;
int current_y = 0;
int goal_x = 0;
int goal_y = 0;
String current_xs = "x = ";
String current_ys = "y = ";

int help = 0;



void setup() {

  Serial.begin(9600); 
  Serial.println("Begin motor control");
  Serial.println();
  
  // Print function list for user selection
  // Serial.println("Enter number for control option:");
  
  // Sets the two pins as Outputs
  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);

  pinMode(enPin,OUTPUT);
  digitalWrite(enPin,LOW);

// lengthwise motors
  pinMode(stepPinLong,OUTPUT);  
  pinMode(dirPinLong,OUTPUT);
  pinMode(enPinLong,OUTPUT);
  digitalWrite(enPinLong,LOW);



  
}

// moves partial step in one direction (CCW) and then returns to position

void loop() {
  if (help == 0){
      Serial.println("Serial available: " + Serial.available());
      if (Serial.available() == 0){
        Serial.println("Enter x coordinate: ");
        goal_x = Serial.read();
        delay(5000);
      }
      
      //if (Serial.available() == 0){
        Serial.println("Enter y coordinate: ");
        goal_y = Serial.read() - 10*goal_x;
        delay(5000);
      //}
      
    help++;        
  }


  
/*
  digitalWrite(dirPin,HIGH); // allow movement in one direction
  // Makes 200 pulses for making one full cycle rotation (can be changed by switches on driver)
  Serial.println("Short away");
  for(int x = 0; x < 1600; x++) {
    digitalWrite(stepPin,HIGH); 
    delayMicroseconds(500); 
    digitalWrite(stepPin,LOW); 
    delayMicroseconds(500); 
  }
  delay(1000); // One second delay

  // lengthwise motors
    digitalWrite(dirPinLong,HIGH); // allow movement in one direction
    Serial.println("Long left");
  // Makes 200 pulses for making one full cycle rotation (can be changed by switches on driver)
  for(int x = 0; x < 1600; x++) {
    digitalWrite(stepPinLong,HIGH); 
    delayMicroseconds(500); 
    digitalWrite(stepPinLong,LOW); 
    delayMicroseconds(500); 
  }
  delay(1000); // One second delay

  digitalWrite(dirPin,LOW); // changes the rotations direction
  Serial.println("Short towards");
  // Makes 400 pulses for making two full cycle rotation
  for(int x = 0; x < 1600; x++) {
    digitalWrite(stepPin,HIGH);
    delayMicroseconds(0500);
    digitalWrite(stepPin,LOW);
    delayMicroseconds(0500);
  }
  delay(1000);

  // lengthwise motors
    digitalWrite(dirPinLong,LOW); // changes the rotations direction
  // Makes 400 pulses for making two full cycle rotation
    Serial.println("Long right");
  for(int x = 0; x < 1600; x++) {
    digitalWrite(stepPinLong,HIGH);
    delayMicroseconds(0500);
    digitalWrite(stepPinLong,LOW);
    delayMicroseconds(0500);
  }
  delay(1000);
*/


  while ((current_x != goal_x) && (current_y != goal_y)){
    Serial.println("***************************");
    Serial.println("Current coordinate: ");
    Serial.print(current_xs + current_x + ", " + current_ys + current_y);
    Serial.println("***************************");
    
    if (current_x > goal_x){
        digitalWrite(dirPin,LOW); // changes the rotations direction
        Serial.println("Short towards");
        current_x--;
            
        // Makes 400 pulses for making two full cycle rotation
        for(int x = 0; x < 1600; x++) {
          digitalWrite(stepPin,HIGH);
          delayMicroseconds(0500);
          digitalWrite(stepPin,LOW);
          delayMicroseconds(0500);
        }

        Serial.println();
Serial.println("***************************");
    Serial.println("Current coordinate: ");
    Serial.print(current_xs + current_x + ", " + current_ys + current_y);
    Serial.println();
    Serial.println("***************************");
    Serial.println();
    
    delay(300);
    }

    if (current_y > goal_y){
        // lengthwise motors
        digitalWrite(dirPinLong,LOW); // changes the rotations direction
        current_y--;
        
        // Makes 400 pulses for making two full cycle rotation
        Serial.println("Long right");
        for(int x = 0; x < 1600; x++) {
          digitalWrite(stepPinLong,HIGH);
          delayMicroseconds(0500);
          digitalWrite(stepPinLong,LOW);
          delayMicroseconds(0500);
        }
        delay(300);

        Serial.println();
Serial.println("***************************");
    Serial.println("Current coordinate: ");
    Serial.print(current_xs + current_x + ", " + current_ys + current_y);
    Serial.println();
    Serial.println("***************************");
    Serial.println();
    }

    if (current_x < goal_x){
        digitalWrite(dirPin,HIGH); // allow movement in one direction
        // Makes 200 pulses for making one full cycle rotation (can be changed by switches on driver)
        current_x++;
        
        Serial.println("Short away");
        for(int x = 0; x < 1600; x++) {
          digitalWrite(stepPin,HIGH); 
          delayMicroseconds(500); 
          digitalWrite(stepPin,LOW); 
          delayMicroseconds(500); 
        }
        delay(300); // One second delay

        Serial.println();
Serial.println("***************************");
    Serial.println("Current coordinate: ");
    Serial.print(current_xs + current_x + ", " + current_ys + current_y);
    Serial.println();
    Serial.println("***************************");
    Serial.println();
    }

    if (current_y < goal_y){
        // lengthwise motors
        digitalWrite(dirPinLong,HIGH); // allow movement in one direction
        Serial.println("Long left");
        // Makes 200 pulses for making one full cycle rotation (can be changed by switches on driver)
        current_y++;
        
        for(int x = 0; x < 1600; x++) {
          digitalWrite(stepPinLong,HIGH); 
          delayMicroseconds(500); 
          digitalWrite(stepPinLong,LOW); 
          delayMicroseconds(500); 
        }
        delay(300); // One second delay  

        Serial.println();
Serial.println("***************************");
    Serial.println("Current coordinate: ");
    Serial.print(current_xs + current_x + ", " + current_ys + current_y);
    Serial.println();
    Serial.println("***************************");
    Serial.println();
    }

    
  }  

  
/*
 * Movement: 1 inch
 * Range: 3.75 inches by 31 inches
 */
  
}
