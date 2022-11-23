#include <Adafruit_MLX90614.h>

const int buzzer = 18; //buzzer to arduino pin 9
Adafruit_MLX90614 mlx = Adafruit_MLX90614();
const int buttonPin = 15; // push button
int buttonState = 0;   

void setup() {
  pinMode(buzzer, OUTPUT); // Set buzzer - pin 9 as an output
  pinMode(buttonPin, INPUT);
  digitalWrite(buzzer, LOW);
  Serial.begin(115200);
  while (!Serial);
  if (!mlx.begin()) {
    Serial.println("Error connecting to MLX sensor.");
    while (1);
  };
  
}
void loop() {
  double temp = mlx.readObjectTempC();
  buttonState = digitalRead(buttonPin);
  if(buttonState == HIGH){
  Serial.println("TEMP: ");
  Serial.println(mlx.readObjectTempC());
  if(mlx.readObjectTempC() > 30){
    digitalWrite(buzzer, HIGH);
  }else{
  digitalWrite(buzzer, LOW);
  }    
  }else{
    digitalWrite(buzzer, LOW);
  //   Serial.println("TEMP: ");
  // Serial.println(mlx.readObjectTempC());
  }
  delay(500);
}
