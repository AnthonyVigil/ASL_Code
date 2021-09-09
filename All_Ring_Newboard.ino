//All_Ring_Newboard
//Oguz Yetkin oyetkin@gmail.com modified for 6th generation ASL Device with Anthony Vigil 11/4/2020
//based on
//ringtest3
//Oguz Yetkin oyetkin@gmail.com written for 5th generation ASL Device with Prissha Krishna Moorthy
//oyetkin@gmail.com 3/6/2020

const int NSENSORS = 15;
int sensorValues[NSENSORS] = {0};             //number of sensors, assumed equal to number of leds
int pins[NSENSORS] = {A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14};  //analog inputs of all sensors
int LEDs[NSENSORS] = {9, 11, 13, 3, 5, 7, 19, 17, 15, 33, 31, 21, 53, 51, 49};        //LEDs corresponding to inputs above
//Added by Oguz Yetkin OY 11/04/2020
int Transistors[NSENSORS] = {8,10,12,2,4,6,18,16,14,24,22,20,52,50,48};


int active_led = 0;                             //LED currently being flashed, from LEDs array
int flash_duration = 5;                        //duration of LED flash in ms. Equal to LED off time
//LEDs might not need an off time
//int epoch_duration = flash_duration * NSENSORS + flash_duration;
long old_millis = 0;
// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(115200);
  pinMode(9, OUTPUT);
  old_millis = millis();
  for (int i = 0; i < NSENSORS; i++) {
    pinMode(LEDs[i], OUTPUT);
    pinMode(Transistors[i], OUTPUT);
    digitalWrite(LEDs[i], LOW);
    digitalWrite(Transistors[i], LOW);
  }
}

// the loop routine runs over and over again forever:
void loop() {
  long time_elapsed = millis() - old_millis;
  int led_state = HIGH;

  for (int LED = 0; LED < NSENSORS; LED++) {

    for (int sensor = 0; sensor < NSENSORS; sensor++) {
      digitalWrite(LEDs[LED], HIGH);
      // if the device doesn't work, comment the next line back in
      //delay(flash_duration);

      digitalWrite(Transistors[sensor], HIGH);
      //delay(1);  //Anthony use this if needed
      int val = analogRead(pins[sensor]);
      delay(1);  //Anthony use this if needed
      digitalWrite(Transistors[sensor], LOW);
      
      Serial.print(val);
      //if(LED<NSENSORS && sensor < NSENSORS-1){
      Serial.print(" ");
      //}
      digitalWrite(LEDs[LED], LOW);
      delay(2*flash_duration);
    }
    digitalWrite(LEDs[LED], LOW);
  }
  Serial.println();
}
