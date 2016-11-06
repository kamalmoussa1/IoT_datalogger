 
 
 //by: Ahmad Atallah
  
  #include <ESP8266WiFi.h>
  #include <WiFiClient.h>
  #include <ESP8266WebServer.h>

  //const char* ssid = "AndroidAP";
  //const char* password = "d51a47164114";

  const char* ssid = "TP-LINK_2F3686";
  const char* password = "47861268";

  const char* host = "esp8266fs";

  int port = 80;
  WiFiServer server(port);
  /* send response to the client
     code - HTTP response code, can be 200 for "Standard response for successful HTTP requests" or 404 for "Not found"
     content_type - HTTP content type, like "text/plain" or "image/png"
    content - actual content body */


  /* main method */

  void setup(void){
    Serial.begin(115200);
    WiFi.begin(ssid, password);
    Serial.println("");

    // Wait for connection
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


    }

  void loop(void){
    WiFiClient client = server.available();
    if (client){
       //sensors data
       Serial.println("New Client Detected");
       String testing_data [6]= {"Ahmad,54,54,25","Kamal,19.1,52.8,34.5","Esraa,58,32,65","Ibraheem,54,49,58.4","Haitham,98,75,54","Sumyaa,32,21.1,29"};
       //String testing_data [6]= {""};

       for(int i = 0; i< 6 ; i++){
            if (client.connected()){
              String command = client.readStringUntil('\r');
              if (command=="GET"){

  //             String data2="54,54,25";
  //             String data ="19.1,52.8,34.5";
                 String data = testing_data[i];
                 Serial.println(data);

                 if (data != ""){
                     Serial.println("ok ... sending sensors data");
  //                 client.print(data2);
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


        // closing the client connection
        //delay(100);
        client.stop();


    }

  }
