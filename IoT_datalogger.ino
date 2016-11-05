
/*
 This demo is based on:
       1. SD card datalogger and HelloKeypad examples by Arduino
       2. BMP280 test example by Adafruit 
 -----------------------------------------------------------------------
 This demo shows how to log data from BMP280 to an SD card and send it wirelessly using ESP8266 wifi module. 

 The circuit:
 * SD card attached to SPI bus as follows:
 ** MOSI(Master Out Slave In)  - pin 11
 ** MISO(Master In Slave Out)- pin 12
 ** SCK(Serial Clock) - pin 13
 ** CS - pin 10
 
 * Keypad attatched to digital pins D9-D2 
 
 * BMP280 attatched to I2C bus as follows: 
 ** SDA - pin A4
 ** SCL - pin A5
 

By: kamal Moussa
---------
 
 */
 
#include <Key.h>
#include <Keypad.h>
#include <Wire.h>     //I2C wiring for BMP280 sensor  :: we can use either I2C or SPI
#include <SPI.h>    //SPI wiring for SD card module
#include <SD.h>     //allow SD card to function 
#include <Adafruit_Sensor.h>  //reference lib. to adafruit products 
#include <Adafruit_BMP280.h>     //to work with BMP sensor 

#define SeaLevel (1013.25)   //in hPa
#define chipSelect 10
#define IR_pin     2
 
/*------------Keypad declearations---------------*/

const byte Rows= 4; //number of rows on the keypad
const byte Cols= 4; //number of columns on the keypad

char keymap[Rows][Cols]=
{
{'1', '2', '3', 'A'},
{'4', '5', '6', 'B'},
{'7', '8', '9', 'C'},
{'*', '0', '#', 'D'}
};

String password="";
String user="";
int x=0;
      /*------pins connections------*/
byte rowPins[Rows] = {9,8,7,6}; //D9-D6 :: connect to the row pinouts of the keypad
byte colPins[Cols] = {5,4,3,2}; //D5-D2 :: connect to the column pinouts of the keypad

Keypad myKeypad= Keypad(makeKeymap(keymap), rowPins, colPins, Rows, Cols);   //an instance of the Keypad class



/*--------data declearaion--------------------*/
double T = 0;     // Temperature 
double P = 0;     // Pressure
double A = 0;     // Altitude
double H = 0;     // Humidity  
/*---------------------------------------*/


/*
 FILE NAMING NOTE:: 
 FAT file systems have a limitation when it comes to naming conventions. You must use the 8.3 format; 8 characters or fewer and 3character extension 
*/

/*--------creat 3 files for logs ---------*/
char dataFileName[] =   "logdata.txt"; 
char trialsFileName[] = "trials.txt"; 
char usersFileName[] =  "userinfo.txt"; 
/*---------------------------------------*/


/*------- creat 3 file objecs-----------*/
File dataLog;
File trialsLog;
File usersLog;
/*-------------------------------------*/

Adafruit_BMP280 bmp;  //creat bmp object, 


void setup() {
  
/*--------- Open serial communications and wait for port to open: ----------*/
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
 
   pinMode(chipSelect, OUTPUT); 

 /*---------see if the card is present and can be initialized:----------*/
 
  Serial.print("Initializing SD card...");
  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed, or not present");  // don't do anything more:
    while(1);
  }
  Serial.println("card initialized.");

/*----------- see if the card is present and can be initialized: --------*/ 


//  Serial.println(F("BMP280 test"));
//    if (!bmp.begin()) {  
//    Serial.println(F("Could not find a valid BMP280 sensor, check wiring!"));
//    while (1);
//  }
//  
//  Serial.println("BMP initialized."); 

  /*-------------- initialize files------------*/
  
            /*-----data file--------*/
            
    dataLog = SD.open(dataFileName, FILE_WRITE);
    String HeaderString= "Tempreature(C)    ressure(hPa)    Altitude(m)";
    dataLog.println(HeaderString);
    dataLog.flush();  // Saves the file
    dataLog.close();
    
            /*-----trials file------------*/
    trialsLog = SD.open(trialsFileName, FILE_WRITE);  //users fil
    trialsLog.close();

  /*---------------------------------------------*/


   if(verifyUser()){
   Serial.print("Welcome, ");
   Serial.println(user);
   /*
    * write user name to esp 
    * 
    * 
    */
   }
   else{
    Serial.print(F("Not allowed"));
   }

}


/*---------------main loop---------------------------*/
void loop() {

  if(!digitalRead(IR_pin)){

    /*
     * 
     * 
     * 
     */

  }
  
}
    

/*------------- raed data from the sensor and send a string to esp --------*/
void getSensorsData(){
  
  String dataString = "";
  
  /*--------- read sensor values and append to the string:-----------*/
   T = bmp.readTemperature();                      // in Cْ
   P = bmp.readPressure()/100.0F ;                 // in hPa
   A = bmp.readAltitude(SeaLevel);                 // in m

  dataString=  String(T)+","+String(P)+","+String(A);    
  
  Serial.println(dataString);

  //Serial.write(dataString); //write to serial 

 //Serial.println("getsensordata:: I got all of them, sir");
}


/*-------------  log data to DATALOG file on the SD card ----------------*/
void savedata(){

  
  dataLog = SD.open(dataFileName, FILE_WRITE);      //reopen to write new data 


  /*------ save new data to DataLog file --------------*/
    if (dataLog) {
          dataLog.print(T);
          dataLog.print("   "); dataLog.print(P);
          dataLog.print("   "); dataLog.print(H);
          dataLog.print("   "); dataLog.print(H);
          dataLog.print("   "); dataLog.print(A);
         
          dataLog.flush();
          dataLog.close();
    }
    else {
    Serial.println("error opening DataLog.txt"); 
     //; //do nothig
    }
    
//  Serial.println("save data:: I'm Ok");
}


/*-----------verify user data against pre-verified users data-------------------*/
 bool verifyUser(){  
  
     String inputPass = getPassword();
        
    usersLog = SD.open(usersFileName);    
    trialsLog =SD.open(trialsFileName, FILE_WRITE);  
    
      if (usersLog) {
        while (usersLog.available()) {
          String myline=usersLog.readStringUntil(',');
          String tempsupline = myline;
          if(x==1){
            user =tempsupline;
            x=0;
            break;

            }
          if(tempsupline==inputPass){
            x=1;
            password =tempsupline;
            trialsLog.print(password);
            trialsLog.print("       "); 
            trialsLog.println("P"); 
            }
          else{
            
            x=0;
            }
      
         }

      usersLog.close();
         if(password==""){
            trialsLog.print(inputPass);
            trialsLog.print("       "); 
            trialsLog.println("F"); 
            Serial.println("not matched");
            
            trialsLog.flush();
            trialsLog.close();
    
            return false;
         }
         else{
            Serial.print("Pssword: "); Serial.println(password);
            Serial.print("User: "); Serial.println(user);
          return true;
         }
 
  } 
  else {
    Serial.println("error opening test.txt");
  }


}

/*-------------get password as an inout from the keypad-------------*/
String getPassword(){


  Serial.println("What password, please?....");
   String password = "";

   while(password.length()!= 4)
   {
       char key= myKeypad.getKey();
     if(key){
       password+=key;      
     }
   }

return password;
   
  
}







