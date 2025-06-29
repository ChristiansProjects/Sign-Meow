#include <WiFi.h>
#include <HTTPClient.h>
#include <LiquidCrystal.h>
#include <ArduinoJson.h>
#include <ESP32Servo.h>

// Wi-Fi credentials and Gemini API key
const char* ssid = "test";
const char* password = "testing123";
const char* api_key = "AIzaSyCaV7n-BV78lCJeuwsrKc3tbJnqnsxr5Ac";

// LCD pin configuration
LiquidCrystal lcd(19, 23, 18, 17, 16, 15);

// Servo and LED setup
Servo myservo;
const int servoPin = 2;
const int ledPin = 4;
bool shouldBlink = false;
unsigned long lastBlinkTime = 0;
int blinkCount = 0;
const int blinkDuration = 200; // ms per blink state

String currentWord = "";

void startBlinking() {
  shouldBlink = true;
  blinkCount = 0;
  lastBlinkTime = millis();
  digitalWrite(ledPin, HIGH); // Start with LED on
}

void updateBlinking() {
  if (!shouldBlink) return;
  
  unsigned long currentTime = millis();
  if (currentTime - lastBlinkTime >= blinkDuration) {
    digitalWrite(ledPin, !digitalRead(ledPin));
    lastBlinkTime = currentTime;
    blinkCount++;
    
    if (blinkCount >= 6) { // 3 blinks (on-off counts as 2)
      shouldBlink = false;
      digitalWrite(ledPin, LOW);
    }
  }
}

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
        Serial.println(word);

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
  
  // Initialize components
  myservo.attach(servoPin);
  myservo.write(0);
  
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
  
  lcd.begin(16, 2);
  lcd.print("Connecting...");

  // Connect to WiFi
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
  updateBlinking(); // Handle LED blinking in the background
  
  if (Serial.available() > 0) {
    String received = Serial.readStringUntil('\n');
    received.trim();
    
    if (received.equalsIgnoreCase("SERVO")) {
      // Activate servo (LED blinking already started)
      for (int i = 0; i < 4; i++) {
        myservo.write(90);
        delay(500);
        myservo.write(0);
        delay(500);
      }
      Serial.println("DONE");
      fetchAndDisplayWord();
    } 
    else if (received.equalsIgnoreCase("LED_BLINK")) {
      startBlinking(); // Start blinking immediately
    }
    else if (received.length() > 0) {
      // Display received message on LCD
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print(received.substring(0, 16));
      if (received.length() > 16) {
        lcd.setCursor(0, 1);
        lcd.print(received.substring(16, 32));
      }
    }
  }
}