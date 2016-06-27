/**
 * PLUGGIE
 * AT DORM
 *  value = true
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
    //WiFiMulti.addAP("NETGEAR", "ECC22E550B");
    //WiFiMulti.addAP("true_home2G_792", "ilovestudy");


    pinMode(A0, INPUT);
    pinMode(5, OUTPUT);   
}

void loop() {
    // wait for WiFi connection
    if((WiFiMulti.run() == WL_CONNECTED)) {
        
        float out = analogRead(A0);

        HTTPClient http;
        float mymax=0.0, mymin=0.0;
        for(int i=0;i<200;i++){
          if(mymax < out){
            mymax = out;
          }
          USE_SERIAL.println(out);
        }

        // current = (mymax-middle) x 0.05
        // cureent = (mymax-686) x 0.05
        // power = current x voltage(226)
        //  power = (mymax-686) x 0.05 x 226
        float power = (mymax-637) * 11.3; // power หน่วยเป็น w
        power = power / 1000; // power หน่วยเป็น kW
        String u = String(power);
        USE_SERIAL.println(u);
        USE_SERIAL.print("[HTTP] begin...\n");
//        //http.begin("https://192.168.1.12/test.html", "7a 9c f4 db 40 d3 62 5a 6e 21 bc 5c cc 66 c8 3e a1 45 59 38"); //HTTPS
        http.begin("http://172.20.10.2:8000/updateusage/4/"+u+"/"); //HTTP

        int httpCode = http.GET();

        if(httpCode > 0) {
            // HTTP header has been send and Server response header has been handled
            USE_SERIAL.printf("[HTTP] GET... code: %d\n", httpCode);

            // file found at server
            if(httpCode == 200) {
                String payload = http.getString();
                USE_SERIAL.println(payload);
                if(payload == "Off"){
                  digitalWrite(5,LOW);
                }
                else{
                  digitalWrite(5,HIGH);
                }
                   
            }
        } else {
            USE_SERIAL.printf("[HTTP] GET... failed, error: %s\n");
        }
        
        http.end();
               
    }

    delay(3000);//1000 msec = 1 sec

}

