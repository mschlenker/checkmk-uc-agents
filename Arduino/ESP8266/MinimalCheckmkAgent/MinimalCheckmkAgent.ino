#include <DHT.h> // Load the DHT11/22 library
#include <ESP8266WiFi.h> // Load ESP WiFi library

// (C) 2022 Mattias Schlenker for tribe29 GmbH
// Due to the libraries used, this code is licensed unter GPL V2

// Agent output as follows:
/*
<<<check_mk>>>
AgentOS: arduino
<<<local>>>
0 "Dummy Arduino" - This is OK.
*/

// The file wifi_secrets.h in the same directory as this file contains the SSID and PSK, two
// lines are enough. If you are not using version control you might just use these lines:
// #define ESSID "mynetworkname"
// #define WPAPSK "mypresharedkey"
#include "wifi_secrets.h"

// Should we use serial debugging? This adds messages to the serial console at 9600 baud.
// Use it until the sensor is calibrated and you have read out the IP address.
#define SERIALDEBUG

// Let's start a single server on port 6556, see:
// https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml?search=checkmk
WiFiServer server(6556);

void setup() {
  // Initialize LED as output
  pinMode(LED_BUILTIN, OUTPUT);
  // The LED on the ESP12 is inverted, so pull to high to switch off:
  digitalWrite(LED_BUILTIN, HIGH);
  // Start serial connection:
  #ifdef SERIALDEBUG
  Serial.begin(9600);
  Serial.print("Connecting to WiFi");
  #endif
  WiFi.begin(ESSID, WPAPSK);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    #ifdef SERIALDEBUG
    Serial.print(".");
    #endif
  }
  #ifdef SERIALDEBUG
  // Print out the IP settings to the serial console:
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  #endif
  server.begin();
}

void loop() {
  WiFiClient client = server.available(); 
  // The Checkmk "protocol" is dead simple: As soon as a request is incoming, we answer it.
  // In http you'd wait for one empty line before answering, since this marks end of request.
  if (client) {
    digitalWrite(LED_BUILTIN, LOW);
    #ifdef SERIALDEBUG
    Serial.println("Client available");
    #endif
    client.println("<<<check_mk>>>\nAgentOS: arduino");
    client.println("<<<local>>>\n0 \"Dummy Arduino\" - This is OK.");
    // Die Verbindung beenden
    client.stop();
    #ifdef SERIALDEBUG
    Serial.println("Client disconnected");
    Serial.println("");
    #endif
    digitalWrite(LED_BUILTIN, HIGH);
  }
}
// Start the loop all over again…
