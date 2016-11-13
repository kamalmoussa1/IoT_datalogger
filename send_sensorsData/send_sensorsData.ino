/* The code burned on ESP8266_Huzzah breakout as Micor-controller
*  that recieve sensors data of temprature, pressure, and
* altitude and then send these data through Wi-fi.
* The Two bins of Software Serial are (12,14) as Rx, Tx

Author: Ahmed Atallah
Last Edit 10 Nov 2016
*/

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <SoftwareSerial.h>

SoftwareSerial swSer(12, 14);
const char* ssid = "Your SSID ";
const char* password = "Your Password";
const char* host = "esp8266fs";

int port = 80;
WiFiServer server(port);

/* send response to the client
code - HTTP response code, can be 200 for "Standard response for successful HTTP requests" or 404 for "Not found"
content_type - HTTP content type, like "text/plain" or "image/png"
content - actual content body */

void setup(void){
  Serial.begin(9600);
  WiFi.begin(ssid, password);
  Serial.println("");

  //** Wait for connection **//

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print("Attempting to connect to WEP network, SSID: ");
    Serial.println(ssid);
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address:// ");
  Serial.println(WiFi.localIP());

  server.begin();
  Serial.println("HTTP server started");
  swSer.begin(9600);

}

void loop(void){
  WiFiClient client = server.available();
  if (client){

    Serial.println("New Client Detected");
    while(1){
      if (client.connected()){
        String command = client.readStringUntil('\r');
        if (command=="GET"){

          //** Read sensor data from software serial **//
          String data = swSer.readStringUntil('\n') ;
          Serial.println( data );
          if (data != ""){
            Serial.println("ok ... sending sensors data");
            client.print(data);
          }
          else{
            client.println("oh");
            Serial.println("No data to be transfered");
          }

        }
      }
      delay(500);

    }


    // ** closing the client connection **//
    client.stop();

  }


}
