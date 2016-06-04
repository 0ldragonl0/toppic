/**
 * BasicHTTPClient.ino
 *
 *  Created on: 24.05.2015
 *
 */

#include <Arduino.h>

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>

#include <ESP8266HTTPClient.h>

#define USE_SERIAL Serial

ESP8266WiFiMulti WiFiMulti;

void setup() {

    USE_SERIAL.begin(115200);
   // USE_SERIAL.setDebugOutput(true);

    USE_SERIAL.println();
    USE_SERIAL.println();
    USE_SERIAL.println();

    for(uint8_t t = 4; t > 0; t--) {
        USE_SERIAL.printf("[SETUP] WAIT %d...\n", t);
        USE_SERIAL.flush();
        delay(1000);
    }

    WiFiMulti.addAP("Nun", "nunnun555");

    pinMode(A0, INPUT);
   
}

void loop() {
    // wait for WiFi connection
    if((WiFiMulti.run() == WL_CONNECTED)) {

        unsigned int out = (unsigned int )analogRead(A0);
        String id ="9";
        
        HTTPClient http;
        
        USE_SERIAL.print("[HTTP] begin...\n");
        // configure traged server and url
        //http.begin("https://192.168.1.12/test.html", "7a 9c f4 db 40 d3 62 5a 6e 21 bc 5c cc 66 c8 3e a1 45 59 38"); //HTTPS
        http.begin("http://127.0.0.1:8000/updateusage/"+id+"/"+out+"/"); //HTTP
        http.addHeader("Content-Type", "application/x-www-form-urlencoded");

        USE_SERIAL.print("[HTTP] POST...\n");

        // start connection and send HTTP header
        String n = String("id="+id+"&num=");
        n += out;
        int httpCode = http.POST(n);
        http.writeToStream(&Serial);
        USE_SERIAL.printf("%d \n",httpCode);
        
      
        http.end();
    }

    delay(100);//msec
}
