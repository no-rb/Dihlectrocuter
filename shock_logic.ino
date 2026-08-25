int modeButton = A1;
int triggerButton = A0;
unsigned long sleepTimeout = 30000; //Run the sleepPrevention every 30 seconds
unsigned long nextTimeout = 0; //keep track of when to run sleep prevention
bool armed = false; //We can't just trigger directly, because a trigger might be received during sleep prevention, so we arm it, and fire when ready. Disarming is done in the fire() function.

void setup() {
  Serial.begin(115200);
  pinMode(modeButton, OUTPUT);
  pinMode(triggerButton, OUTPUT);
  //Buttons on the remote are active LOW
  digitalWrite(modeButton,HIGH); 
  digitalWrite(triggerButton,HIGH);
  }

void loop() {

  //if(Serial.available()){ //Triggers on anything! CAREFUL!
  if (Serial.read()=='T'){
    Serial.read(); //discard the data in the serial buffer
    armed=true; 
  }

  if(millis()>nextTimeout){
    sleepPrevention(); //4*(100+50)... sleep prevention routine takes around 600 milliseconds
  }

  if (armed) {
    fire();
  }

}

void fire(){
    buttonPress(triggerButton,500);
    armed=false;

}

void buttonPress(int button, int duration){
  digitalWrite(button, LOW);
  delay(duration);
  digitalWrite(button, HIGH);
}

void sleepPrevention(){
  for(int repetitions=4;repetitions>0;repetitions--){
  buttonPress(modeButton,100);
  delay(50);
  }
  nextTimeout=millis()+sleepTimeout;
}