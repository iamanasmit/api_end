#include <WiFi.h>
#include <ESP32Servo.h>

Servo myServo;

const char* ssid = "ESP32-Control";
const char* password = "12345678";

WiFiServer server(80);

void setup() {
  Serial.begin(9600);
  myServo.attach(4);
  WiFi.softAP(ssid, password);
  server.begin();
  Serial.println("ESP32 Web Server Started!");
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    String request = client.readStringUntil('\r');
    Serial.println(request);
    
    if (request.indexOf("/light/on") != -1) {
      Serial.println("Light ON");
      myServo.write(180);
    }
    if (request.indexOf("/light/off") != -1) {
      Serial.println("Light OFF");
      myServo.write(0);
    }
    if (request.indexOf("/window/open") != -1) {
      Serial.println("Window OPEN");
    }
    if (request.indexOf("/window/close") != -1) {
      Serial.println("Window CLOSE");
    }

    // Improved HTML UI
    client.println("HTTP/1.1 200 OK");
    client.println("Content-type:text/html");
    client.println();
    client.println("<html><head><title>ESP32 Control</title>");
    client.println("<style>");
    client.println("body { font-family: Arial, sans-serif; text-align: center; background-color: #f4f4f4; }");
    client.println("h2 { color: #333; }");
    client.println(".container { width: 90%; max-width: 400px; margin: auto; }");
    client.println("button { display: block; width: 100%; padding: 10px; margin: 10px 0; font-size: 18px; border: none; cursor: pointer; }");
    client.println(".on { background-color: green; color: white; }");
    client.println(".off { background-color: red; color: white; }");
    client.println(".window { background-color: blue; color: white; }");
    client.println("</style></head><body>");
    client.println("<div class='container'>");
    client.println("<h2>ESP32 Appliance Control</h2>");
    client.println("<a href='/light/on'><button class='on'>Light ON</button></a>");
    client.println("<a href='/light/off'><button class='off'>Light OFF</button></a>");
    client.println("<a href='/window/open'><button class='window'>Window OPEN</button></a>");
    client.println("<a href='/window/close'><button class='window'>Window CLOSE</button></a>");
    client.println("</div>");
    client.println("</body></html>");
    client.println();
    client.stop();
  }
}
