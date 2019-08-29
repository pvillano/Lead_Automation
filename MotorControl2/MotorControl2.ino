// connect these ports to given pins
//motor 1 - x dir
const int dirPinX  = 3; //dir+ to 3
const int stepPinX = 4; //pul+ to 4
const int enPinX   = 5; //en+ to 5

// lengthwise motors 
//motors 2 and 3 - y dir
const int dirPinY = 6; //dir+ to 6
const int stepPinY = 7; //pul+ to 7
const int enPinY = 10; //en+ to 10

const int maxInterval = 150;
const int minInterval = 25;
const int accelSteps = 30;

class Motor{
  char motorName;
  int dirPin;
  int stepPin;
  int enPin;
  int curDir;
  float curPos;
  int conversionFactor;
  bool stepping;
  unsigned long stepsRemaining;
  unsigned long lastMoveMicros;
  int interval;
  int accelStepsLeft;

  public:
    Motor(int dPin, int sPin, int ePin, char n){
    motorName = n;
    dirPin = dPin;
    stepPin = sPin;
    enPin = ePin;
    pinMode(dirPin, OUTPUT);
    pinMode(stepPin, OUTPUT);
    pinMode(enPin, OUTPUT);
    digitalWrite(enPin, LOW);
    curDir = 1;
    curPos = 0.0;
    conversionFactor = 115;
    stepping = false;
    stepsRemaining = 0;
    lastMoveMicros = 0;
    interval = 150;
    accelStepsLeft = accelSteps;
  }

  void setInterval(int i){
    interval = i;
  }

  void MoveTo(float target){
    if (stepping){
      return;
    }
    /*Serial.println("Moving");
    Serial.print(curPos);
    Serial.print(" ");
    Serial.print(target);
    Serial.print(" ");
    Serial.println(curDir);*/
    if ((target < curPos) and (curDir == 1)){
      digitalWrite(dirPin, HIGH);
      curDir = -1;
      //Serial.println("Switched direction");
    } 
    if ((target > curPos) and (curDir == -1)){
      digitalWrite(dirPin, LOW);
      curDir = 1;
      //Serial.println("Switched direction");
    } 
    stepsRemaining = abs(target-curPos)*conversionFactor;
    stepping = true;
  }

  void Update(){
    if ((stepsRemaining > 0) and ((micros()-lastMoveMicros) > interval)){
      lastMoveMicros = micros();
      Step(stepsRemaining);
      curPos += (float(curDir)/conversionFactor);
      stepsRemaining -= 1;
      //updateSpeed();
    }
    if (stepsRemaining == 0 and stepping){
      stepping = false;
      Serial.print(motorName);
      Serial.print("Reached Target ");
      Serial.println(curPos);
    }
  }

  void updateSpeed(){
    if (stepsRemaining == 0){
      interval = maxInterval;
      return;
    }
    if ((stepsRemaining < accelSteps) and (interval < maxInterval)){
      float change = 2*interval;
      int stepsLeft = stepsRemaining-1;
      change = change/((4*stepsLeft)+1);
      //change = change*(accelSteps-stepsLeft)/(accelSteps);
      interval = interval+change;
      Serial.println(change);
      return;
    }
    /*if (accelStepsLeft == accelSteps){
      accelStepsLeft -= 1;
      interval = 0.4142*interval;
      return;
    }*/
    if (accelStepsLeft > 0){
      accelStepsLeft -= 1;
      float change = 2*interval;
      float stepsLeft = accelSteps-accelStepsLeft;
      change = change/((4*stepsLeft)+1);
      change = change*(accelSteps-stepsLeft)/(accelSteps);
      interval = max(interval-change, minInterval);
      return;
    }
    interval = minInterval;
  }

  void Step(int stepsRemaining){
    if ((stepsRemaining % 2)==0){
      digitalWrite(stepPin, HIGH);
    } else {
      digitalWrite(stepPin, LOW);
    }
  }

  bool Stepping(){
    return stepping;
  }
  
};

Motor yMotor(dirPinY, stepPinY, enPinY, 'y');
Motor xMotor(dirPinX, stepPinX, enPinX, 'x');
int curStep = 0;
int i = 0;
  
void setup() {
  Serial.begin(9600); 
  Serial.println("Begin motor control");
}

void loop() {
  yMotor.Update();
  xMotor.Update();
  if((not yMotor.Stepping()) and (not xMotor.Stepping()) and (i < 9)){
    SerialCommand();
  }
}

void NextStep(){
  if (curStep == 0){
    xMotor.MoveTo(0);
    yMotor.MoveTo(0);
  }
  if(curStep == 1){
    xMotor.MoveTo(0);
    yMotor.MoveTo(40);
  }
  if(curStep == 2){
    xMotor.MoveTo(25);
    yMotor.MoveTo(40);
  }
  if(curStep == 3){
    xMotor.MoveTo(25);
    yMotor.MoveTo(0);
    curStep = -1;
  }
  curStep += 1;
}

void SerialCommand(){
  Serial.println("Enter target x:");
  while(Serial.available() == 0){
    delay(50);
  }
  float xTarget = Serial.parseFloat();
  Serial.flush();
  Serial.println("Enter target y:");
  while(Serial.available() == 0){
    delay(50);
  }
  float yTarget = Serial.parseFloat();
  Serial.flush();
  /*Serial.print("Moving to (");
  Serial.print(xTarget);
  Serial.print(", ");
  Serial.print(yTarget);
  Serial.println(")");*/
  xMotor.MoveTo(xTarget);
  yMotor.MoveTo(yTarget);
}

