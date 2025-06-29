#include <WiFi.h>
#include <HTTPClient.h>
#include <LiquidCrystal.h>
#include <ArduinoJson.h>
#include <ESP32Servo.h>

// Wi-Fi credentials and Gemini API key
const char* ssid = "test";
const char* password = "testing123";
const char* api_key = "AIzaSyCaV7n-BV78lCJeuwsrKc3tbJnqnsxr5Ac";

// LCD pin configuration: RS, EN, D4, D5, D6, D7 → GPIOs
LiquidCrystal lcd(19, 23, 18, 17, 16, 15);

Servo myservo;
const int servoPin = 2;

String currentWord = "";

void fetchAndDisplayWord() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient https;
    String url = String("https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-002:generateContent?key=") + api_key;
    https.begin(url);
    https.addHeader("Content-Type", "application/json");

    String payload = R"({
      "contents": [
        {
          "parts": [
            { "text": "Generate a single English word (3-7 letters) for ASL fingerspelling practice. Only output the word, nothing else. Do not use J, P, T, Z" }
          ]
        }
      ]
    })";

    int httpCode = https.POST(payload);
    if (httpCode > 0) {
      String response = https.getString();
      DynamicJsonDocument doc(8192);
      DeserializationError error = deserializeJson(doc, response);

      if (!error && doc.containsKey("candidates")) {
        String word = doc["candidates"][0]["content"]["parts"][0]["text"].as<String>();
        word.trim();
        word.replace("\n", "");
        word.replace("\r", "");
        word.toUpperCase();
        currentWord = word;
        Serial.print("WORD:");
        Serial.println(word); // Send to Python

        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print(word.substring(0, 16));
        if (word.length() > 16) {
          lcd.setCursor(0, 1);
          lcd.print(word.substring(16, 32));
        }
      } else {
        lcd.clear();
        lcd.print("Gemini error");
        currentWord = "HELLO";
        Serial.println("WORD:HELLO");
      }
    } else {
      lcd.clear();
      lcd.print("HTTP Error");
      currentWord = "HELLO";
      Serial.println("WORD:HELLO");
    }
    https.end();
  } else {
    lcd.clear();
    lcd.print("WiFi error");
    currentWord = "HELLO";
    Serial.println("WORD:HELLO");
  }
}

void setup() {
  Serial.begin(115200);
  myservo.attach(servoPin);
  myservo.write(0);
  lcd.begin(16, 2);
  lcd.print("Connecting...");

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\n✅ WiFi connected");
  lcd.clear();
  lcd.print("WiFi connected");

  fetchAndDisplayWord();
}

void loop() {
  if (Serial.available() > 0) {
    String received = Serial.readStringUntil('\n');
    received.trim();
    if (received.equalsIgnoreCase("SERVO")) {
      for (int i = 0; i < 4; i++) {
        myservo.write(90);
        delay(500);
        myservo.write(0);
        delay(500);
      }
      Serial.println("DONE");
      fetchAndDisplayWord(); // Get and display a new word after servo
    } else if (received.length() > 0) {
      // Display letters as before
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print(received.substring(0, 16));
      if (received.length() > 16) {
        lcd.setCursor(0, 1);
        lcd.print(received.substring(16, 32));
      }
      Serial.print("Displayed: ");
      Serial.println(received);
    }
  }
}