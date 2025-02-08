#include <BluetoothSerial.h>
#include <ESP32Servo.h>

BluetoothSerial SerialBT;
Servo myServo;

void setup() {
  Serial.begin(9600);
  SerialBT.begin("ESP32-Control"); 
  myServo.attach(4);
  Serial.println("ESP32 Bluetooth Control Started!");
}

void loop() {
  if (SerialBT.available()) {
    String command = SerialBT.readStringUntil('\n');
    command.trim();
    Serial.println("Received: " + command);
    
    if (command == "light on") {
      Serial.println("Light ON");
      myServo.write(180);
    } else if (command == "light off") {
      Serial.println("Light OFF");
      myServo.write(0);
    } else if (command == "window open") {
      Serial.println("Window OPEN");
    } else if (command == "window close") {
      Serial.println("Window CLOSE");
    } else {
      Serial.println("Invalid command");
    }
  }
}