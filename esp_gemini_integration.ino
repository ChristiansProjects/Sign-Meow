#include <WiFi.h>
#include <HTTPClient.h>
#include <LiquidCrystal.h>
#include <ArduinoJson.h>

// Wi-Fi credentials and Gemini API key
const char* ssid = "test";
const char* password = "testing123";
const char* api_key = "AIzaSyCaV7n-BV78lCJeuwsrKc3tbJnqnsxr5Ac";

// LCD pin configuration: RS, EN, D4, D5, D6, D7 → GPIOs
LiquidCrystal lcd(19, 23, 18, 17, 16, 15);

void setup() {
  Serial.begin(115200);
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

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient https;

    String url = String("https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-002:generateContent?key=") + api_key;

    https.begin(url);
    https.addHeader("Content-Type", "application/json");

    String payload = R"({
      "contents": [
        {
          "parts": [
            { "text": "Generate a text that is 32 characters long." }
          ]
        }
      ]
    })";

    int httpCode = https.POST(payload);
    if (httpCode > 0) {
      String response = https.getString();
      Serial.println("\n✅ Response:");
      Serial.println(response);

      DynamicJsonDocument doc(8192);
      DeserializationError error = deserializeJson(doc, response);

      if (error) {
        Serial.print("❌ JSON Parse Error: ");
        Serial.println(error.c_str());
        lcd.clear();
        lcd.print("JSON error");
      } else if (doc.containsKey("candidates")) {
        String text = doc["candidates"][0]["content"]["parts"][0]["text"].as<String>();
        Serial.println("\n💬 Gemini says:");
        Serial.println(text);

        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print(text.substring(0, 16));  // First 16 characters

        lcd.setCursor(0, 1);
        lcd.print(text.length() > 16 ? text.substring(16, 32) : "");  // Next 16 if available
      } else if (doc.containsKey("error")) {
        String msg = doc["error"]["message"].as<String>();
        Serial.println("❌ API Error: " + msg);
        lcd.clear();
        lcd.print("API Error:");
        lcd.setCursor(0, 1);
        lcd.print(msg.substring(0, 16));
      } else {
        Serial.println("❌ Unexpected response");
        lcd.clear();
        lcd.print("Bad response");
      }
    } else {
      Serial.print("❌ HTTP error: ");
      Serial.println(https.errorToString(httpCode));
      lcd.clear();
      lcd.print("HTTP Error");
    }

    https.end();
  }
}

void loop() {
  // No repeating logic
}