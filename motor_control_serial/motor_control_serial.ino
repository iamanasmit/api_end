#include <BluetoothSerial.h>
#include <ESP32Servo.h>

BluetoothSerial SerialBT;
Servo myServo;

void setup() {
  Serial.begin(9600);       // USB Serial (PC)
  SerialBT.begin("ESP32-Control");  // Bluetooth Serial
  myServo.attach(18);
  Serial.println("ESP32 Control Started!");
}

void loop() {
  String command = "";

  // Check Serial (USB from PC)
  if (Serial.available()) {
    command = Serial.readStringUntil('\n');
  }

  // Check Bluetooth
  if (SerialBT.available()) {
    command = SerialBT.readStringUntil('\n');
  }

  command.trim();  // Remove extra spaces or newlines

  if (command.length() > 0) {
    Serial.println("Received: " + command);

    if (command == "light on") {
      Serial.println("Light ON");
      myServo.write(60);
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
