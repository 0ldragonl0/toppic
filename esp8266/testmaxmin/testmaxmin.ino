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
    //WiFiMulti.addAP("NETGEAR", "ECC22E550B");
    //WiFiMulti.addAP("true_home2G_792", "ilovestudy");


    pinMode(A0, INPUT);
    pinMode(5, OUTPUT);   
}

void loop() {
  // put your main code here, to run repeatedly:
    float out = analogRead(A0);
   
    USE_SERIAL.println(out);

    delay(1000);//1000 msec = 1 sec


}
