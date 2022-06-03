int s1_s2_red = 7;
int s1_s2_yellow = 6;
int s1_s2_green = 5;

int s3_green = 8;
int s3_yellow = 9;
int s3_red = 10;

int p3_green = 11;
int p3_red = 12;

int s1_lightSensor=1;
int s2_lightSensor=5;
int s3_lightSensor=3;

int lightThreshold=50;

int minimumGreenTimeS3=5;
int minimumGreenTimeS1S2=5;
int maximumGreenTimeS1S2=10;
int maximumGreenTimeS3=10;
int yellowTime=5;
int intermittentTime=yellowTime;

int maxTotalTime=maximumGreenTimeS1S2+maximumGreenTimeS3+yellowTime+intermittentTime;

int greenS1S2_startTime, yellowS1S2_startTime, redS1S2_startTime,intermittentP3_startTime,greenS3_startTime, yellowS3_startTime, redS3_startTime;

bool carsAtS1,carsAtS2,carsAtS3;

int button = 13; // switch is on pin 13
unsigned long milliseconds,previousReading=0;
unsigned int cycle_seconds;
int timeSum;
bool buttonPressed=false;

String data="";
String carsWaitingData="";

void setup(){
  Serial.begin(57600);
  pinMode(s1_s2_red, OUTPUT);
  pinMode(s1_s2_yellow, OUTPUT);
  pinMode(s1_s2_green, OUTPUT);

  pinMode(s3_green, OUTPUT);
  pinMode(s3_yellow, OUTPUT);
  pinMode(s3_red, OUTPUT);

  pinMode(p3_green, OUTPUT);
  pinMode(p3_red, OUTPUT);

  pinMode(button, INPUT);

  digitalWrite(s1_s2_green, HIGH);
  digitalWrite(s1_s2_yellow, LOW);

  greenS1S2_startTime=0;
  yellowS1S2_startTime=greenS1S2_startTime+maximumGreenTimeS1S2;
  redS1S2_startTime=yellowS1S2_startTime+yellowTime;
  intermittentP3_startTime=yellowS1S2_startTime;
  greenS3_startTime=redS1S2_startTime;
  yellowS3_startTime=greenS3_startTime+maximumGreenTimeS3;
  redS3_startTime=yellowS3_startTime+yellowTime;
  //Serial.println(greenS1S2_startTime);
  //Serial.println(yellowS1S2_startTime);
  //Serial.println(redS1S2_startTime);
  //Serial.println(intermittentP3_startTime);
  //Serial.println(greenS3_startTime);
  //Serial.println(yellowS3_startTime);
  //Serial.println(redS3_startTime);
 
}

void parseWebsiteInput(String str){
  
  String strs[6];
  int StringCount = 0;
  while (str.length() > 0)
  {
    int index = str.indexOf('-');
    if (index == -1) // No space found
    {
      strs[StringCount++] = str;
      break;
    }
    else
    {
      strs[StringCount++] = str.substring(0, index);
      str = str.substring(index+1);
    }
  }

  minimumGreenTimeS3 = strs[0].toInt();
  minimumGreenTimeS1S2 = strs[1].toInt();
  lightThreshold = strs[2].toInt();
  yellowTime = strs[3].toInt();
  intermittentTime=yellowTime;
  maximumGreenTimeS3 = strs[4].toInt();
  maximumGreenTimeS1S2 = strs[5].toInt();
  
  greenS1S2_startTime=0;
  yellowS1S2_startTime=greenS1S2_startTime+maximumGreenTimeS1S2;
  redS1S2_startTime=yellowS1S2_startTime+yellowTime;
  intermittentP3_startTime=yellowS1S2_startTime;
  greenS3_startTime=redS1S2_startTime;
  yellowS3_startTime=greenS3_startTime+maximumGreenTimeS3;
  redS3_startTime=yellowS3_startTime+yellowTime;
  maxTotalTime=maximumGreenTimeS1S2+maximumGreenTimeS3+yellowTime+intermittentTime;
//  Serial.println(maxTotalTime);
  
}


void loop() {
  //Serial.println(analogRead(s1_lightSensor));
  //Serial.println(analogRead(s2_lightSensor));
  //Serial.println(analogRead(s3_lightSensor));
  milliseconds = millis();
  if(milliseconds%1000>=0 && milliseconds%1000<21 &&milliseconds/1000!=previousReading/1000){
    cycle_seconds++;
    cycle_seconds%=maxTotalTime;
    previousReading=milliseconds;
  if (Serial.available() > 0) {
    data = Serial.readStringUntil('\n');
    parseWebsiteInput(data);
    cycle_seconds = 0;
    
//  Serial.println(minimumGreenTimeS3);
//  Serial.println(minimumGreenTimeS1S2);
//  Serial.println(lightThreshold);
//  Serial.println(yellowTime);
//  Serial.println(maximumGreenTimeS3);
//  Serial.println(maximumGreenTimeS1S2);
  }
//    Serial.print("You sent me: ");
//    Serial.println(data);
    char carsWaitingData[25];
  carsWaitingData[0] = '\0';

  strcat(carsWaitingData, carsAtS1?"1":"0");
  strcat(carsWaitingData, "-");
  strcat(carsWaitingData, carsAtS2?"1":"0");
  strcat(carsWaitingData, "-");
  strcat(carsWaitingData, carsAtS3?"1":"0");
//    carsWaitingData= carsAtS1+"-"+carsAtS2+"-"+carsAtS3;
    Serial.println(cycle_seconds);
    Serial.println(carsWaitingData);
//Serial.println(carsAtS1);
  //Serial.println(carsAtS2);
  //Serial.println(carsAtS3);
    carsAtS1=false;
    carsAtS2=false;
    carsAtS3=false;
  }
//  Serial.println("S1");
//  Serial.println(analogRead(s1_lightSensor));
//  Serial.println("S2");
//  Serial.println(analogRead(s2_lightSensor));
//  Serial.println("S3");
//  Serial.println(analogRead(s3_lightSensor));
  carsAtS1= carsAtS1 || analogRead(s1_lightSensor)<lightThreshold;
  carsAtS2= carsAtS2 || analogRead(s2_lightSensor)<lightThreshold;
  carsAtS3= carsAtS3 || analogRead(s3_lightSensor)<lightThreshold;
  
  //LIGHT SENSING
  
  if(digitalRead(s3_green)==HIGH && !carsAtS3 && (carsAtS1||carsAtS2)){
    if(cycle_seconds>greenS3_startTime+minimumGreenTimeS3){
      cycle_seconds=yellowS3_startTime;
    }
  }
  
  if(digitalRead(s1_s2_green)==HIGH && carsAtS3 && !carsAtS1 && !carsAtS2){
    if(cycle_seconds>greenS1S2_startTime+minimumGreenTimeS1S2){
      cycle_seconds=yellowS1S2_startTime;
    }
  }
  //Serial.println(greenS3_startTime+minimumGreenTimeS3);
  //Serial.println(yellowS3_startTime);
  int minimumTimeForButtonToChangeLights=greenS3_startTime+minimumGreenTimeS3;
  //BUTTON PRESSING
  if(buttonPressed && cycle_seconds==minimumTimeForButtonToChangeLights){
    //timeSum=yellowS3_startTime-cycle_seconds;
    cycle_seconds=yellowS3_startTime;
    buttonPressed=false;
  return;  
  }
  if (digitalRead(button) == HIGH && !buttonPressed){
    delay(15); // software debounce
    if (digitalRead(button) == HIGH && digitalRead(p3_red)==HIGH) {
      // if the switch is HIGH, ie. pushed down - change the lights!
      if (cycle_seconds>=minimumTimeForButtonToChangeLights && cycle_seconds < yellowS3_startTime){
      //timeSum=yellowS3_startTime-cycle_seconds;
        cycle_seconds=yellowS3_startTime;
      }
    else{
      buttonPressed=true;
    }
    }
  }
  //cycle_seconds=(milliseconds%32000)/1000;
  //if(timeSum!=0){  
  //  cycle_seconds+=timeSum;
  //  timeSum=0;
  //}
  if(cycle_seconds < yellowS1S2_startTime){
    digitalWrite(s1_s2_green, HIGH);
    digitalWrite(s1_s2_yellow, LOW);
    digitalWrite(s1_s2_red, LOW);
    digitalWrite(s3_green, LOW);
    digitalWrite(s3_yellow, LOW);
    digitalWrite(s3_red, HIGH);
    digitalWrite(p3_green, HIGH);
    digitalWrite(p3_red, LOW);
  }
  
  if(cycle_seconds==yellowS1S2_startTime){
    digitalWrite(s1_s2_green, LOW);
    digitalWrite(s1_s2_yellow, HIGH);
  }
  
  
  if(cycle_seconds>intermittentP3_startTime && cycle_seconds < greenS3_startTime){
    if(cycle_seconds%2!=0){
      digitalWrite(p3_green, LOW);
    }else{
      digitalWrite(p3_green, HIGH);
    }
  }
  
  if(cycle_seconds==greenS3_startTime){
    digitalWrite(s1_s2_green, LOW);
    digitalWrite(s1_s2_yellow, LOW);
    digitalWrite(s1_s2_red, HIGH);
    digitalWrite(s3_green, HIGH);
    digitalWrite(s3_yellow, LOW );
    digitalWrite(s3_red, LOW);
    digitalWrite(p3_green, LOW);
    digitalWrite(p3_red, HIGH);
  }
  
  if(cycle_seconds == yellowS3_startTime){
    digitalWrite(s3_green, LOW);
    digitalWrite(s3_yellow, HIGH);
  }
}
