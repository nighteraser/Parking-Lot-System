#include <Servo.h>
Servo servo;

int trigPin = 5;
int echoPin = 6;
int Green_LED_Pin = 3;
int Red_LED_Pin = 4;
int motor_Pin = 9;
float duration;
int distance;
int isopen = 0;


void setup() {
  servo.attach(motor_Pin);
  servo.write(90); // Initialize the servo to 90 degrees
  Serial.begin(9600);
  // Sets the trigPin as an Output
  pinMode(trigPin, OUTPUT);
  // Sets the echoPin as an Input
  pinMode(echoPin, INPUT);
  pinMode(Green_LED_Pin, OUTPUT);
  pinMode(Red_LED_Pin, OUTPUT);
}

int waitForRespond() {
  if (Serial.available() > 0) {
    String message = Serial.readStringUntil('\n');
    message.trim(); // Remove any leading or trailing whitespace
    if (message == "hi") {
      return 1; 
    }
  }
  return 0;
}


int get_distance() {
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);

  // Calculating the distance
  distance = duration * 0.034 / 2;

  return distance;
}
void open(){
  digitalWrite(Green_LED_Pin, HIGH);
  digitalWrite(Red_LED_Pin, LOW);
  servo.write(180);
}
void close(){
  digitalWrite(Green_LED_Pin, LOW);
  digitalWrite(Red_LED_Pin, HIGH);
  servo.write(90);
}

void loop() {
  distance = get_distance();
//  Serial.print("Distance: ");
//  Serial.println(distance);

  if (distance <= 7 && waitForRespond() == 1 && isopen == 0) { 
    isopen = 1;
  } else if(isopen == 1 && distance > 7){
    isopen = 0;
  }
  delay(1000); 
//  delay(2000);
  if ( isopen == 1 ){
    open();
  }else{ 
    close();
  }

}
