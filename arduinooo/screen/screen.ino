#include <MCUFRIEND_kbv.h>
#include <TouchScreen.h>
#include <Adafruit_GFX.h>
#include <stdio.h>
MCUFRIEND_kbv tft;


const int XP=9,XM=A3,YP=A2,YM=8; //320x480 ID=0x9488
const int TS_LEFT=172,TS_RT=919,TS_TOP=957,TS_BOT=168;
TouchScreen ts = TouchScreen(XP, YP, XM, YM, 300);

Adafruit_GFX_Button btnOnOff, btnSync, btnPause;

#define MINPRESSURE 10
#define MAXPRESSURE 10000
#define BLACK 0x0000
#define NAVY 0x000F
#define DARKGREEN 0x03E0
#define DARKCYAN 0x03EF
#define MAROON 0x7800
#define PURPLE 0x780F
#define OLIVE 0x7BE0
#define LIGHTGREY 0xC618
#define DARKGREY 0x7BEF
#define BLUE 0x001F
#define GREEN 0x07E0
#define CYAN 0x07FF
#define RED 0xF800
#define MAGENTA 0xF81F
#define YELLOW 0xFFE0
#define WHITE 0xFFFF
#define ORANGE 0xFD20
#define GREENYELLOW 0xAFE5
#define PINK 0xF81F
#define BKGCOLOR 0x0003



bool lights = false;
bool syncLights = false;
bool PauseLights = false;

uint8_t memSs = -1;
float memTempeMen =-1.0;
int memMenJour = -1;
int memSwipe = -1; 
float memT = -1;
int memcpt = -1;
float memtab = -1;


int cpt = 0; 
long cptDate = 9000; 
int menuCpt = 0;
int swipeCpt = 0;
int resSwipe = 0;

int pixel_x, pixel_y;     //Touch_getXY() updates global vars


float mintab =-1; 
float maxtab = 1;
float mintabh =-3; 
float maxtabh = 1;
int dejaPasse = -1;
int dejaPasse5 = -1;
bool dejaPasseL = true;
int ledsRotations= 1;
int vitesse = 5;
int cptVitesse = 0;

int redValue = 0;
int greenValue = 0;
int blueValue = 0;

const char dayOfW[][8] = {"Lundi", "Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"};
const char monthofY[][9] = {"Janvier", "Fevrier","Mars","Avril","Mai","Juin","Juillet","Aout","Septembre","Octobre","Novembre","Decembre"};

bool down ;
float h ;
float t ;


int var_id = 0;
String var_content = "";
String values[20];
String memvalues[20];


void readSerialPort(int *var_id, String *var_content,String values[]) {
  int mySize = 1;
  while (Serial.available()) {
    String msg = "";
    delay(10);
    while (Serial.available() > 0) {
      msg += (char)Serial.read();
      mySize++;
      delay(1);
    }
    Serial.flush();
    int sep_index = msg.indexOf('=');
    *var_id = msg.substring(0, sep_index).toInt();
    *var_content = msg.substring(sep_index + 1, mySize);
    // *var_content = *var_content/100;
    // Serial.print(*var_content);
    updateValues(var_id,var_content,values);
    delay(100);
  }  
}



void updateValues(int *var_id, String *var_content,String values[]){
    values[*var_id] = *var_content;
    // allValues(values);
    Serial.write("ok");
}

void allValues(String values[]){
    tft.fillRect(0, 0, 320, 480, WHITE); 
    // delay(1);
    tft.setCursor(0,0);
    tft.setTextSize(2);
    tft.setTextColor(PURPLE);
    for(int i=0; i < 20 ; i++){
        tft.print(i);
        tft.print(" == ");
        tft.println(values[i]);
    }
    
}


bool Touch_getXY(void){
    TSPoint p = ts.getPoint();
    pinMode(YP, OUTPUT);      //restore shared pins
    pinMode(XM, OUTPUT);
    digitalWrite(YP, HIGH);   //because TFT control pins
    digitalWrite(XM, HIGH);
    bool pressed = (p.z > MINPRESSURE && p.z < MAXPRESSURE);
    if (pressed) {
        pixel_y = map(p.x, 957, 168, 0, 320); //.kbv makes sense to me
        pixel_x = map(p.y, 919, 172, 0, 480);
    }
    return pressed;
}


void barMenu(void){
  // tft.fillRect(160, 14, 152, 20, DARKGREY);
  for (int k; k<5; k++){
    tft.fillCircle(170+34*k, 27, 10, WHITE);
  }
  tft.fillCircle(170+34*cpt, 27, 7, BLACK);
  tft.drawFastHLine(0, 50 , 500, BLACK);
  tft.drawFastHLine(0, 53 , 500, BLACK);
}

void displayDate(void){
  tft.fillRect(330, 12, 145, 26, BLACK);
  // tft.setCursor(330,5);
  tft.setCursor(355,12);
  tft.setTextColor(WHITE);
  tft.setTextSize(3);
  tft.print(values[0]);
}
void displayTemp(void){
  tft.fillRect(5, 12, 145, 26, BLACK);
  tft.setCursor(20,12);
  tft.setTextColor(WHITE);
  tft.setTextSize(3);
  tft.print(values[4]);
}

void describeMenu(String txt){
  tft.fillRect(5, 60, 470, 255, BLACK);
  tft.setCursor(20, 70);
  tft.setTextColor(YELLOW);
  tft.setTextSize(3);
  tft.print(txt);
}

void cleanBar(){
  tft.fillRect(-35, 0, 500, 49, BKGCOLOR);
  displayDate();
  displayTemp();
  barMenu();
  tft.drawFastHLine(0, 40 , 500, BLACK);
}


bool checkValues(String values[],String memvalues[],int tocheck[],int size){
  bool res = true;
  for(int i = 0; i < size; i++){
    if(memvalues[tocheck[i]] != values[tocheck[i]]){
      return true;
    }
  }
  return false;
}


void sameValues(String values[],String memvalues[],int tocheck[],int size){
  bool res = true;
  for(int i = 0; i < size; i++){
    memvalues[tocheck[i]] = values[tocheck[i]];
  }
}

void swiping(){
  while (Touch_getXY()){
    if(memSwipe == -1){
      memSwipe = pixel_x;
    }
    swipeCpt++;
  }
  if (memSwipe != -1){
    if(swipeCpt > 15){
      if( memSwipe + 100 >  pixel_x){
        if(cpt == 0){
          resSwipe =0;
          cpt = 4;
        }
        else{
          cpt--; 
          resSwipe =0;
        }
        barMenu();
      }
      if( memSwipe - 100 < pixel_x){
        if(cpt == 4){
          resSwipe =0;
          cpt = 0;
          }
          else{
            cpt++; 
            resSwipe = 0;
          }
        barMenu();
        }
      swipeCpt = 0;
      memSwipe = -1;
    }
  }
}


void setup() {
    Serial.begin(9600);
    uint16_t ID = tft.readID();
    if (ID == 0xD3D3) ID = 0x9486;
    tft.begin(ID);
    tft.setRotation(1);            
    tft.fillScreen(WHITE);
    barMenu();
    tft.fillRect(5, 5, 470, 40, BLACK);
    values[0] = "heure";
    values[1] = "jour";
    values[2] = "mois";
    values[3] = "annee";
    values[4] = "temp";
    values[5] = "netT";
    values[6] = "humid";
    values[7] = "dtJ";
    values[8] = "Presence";
    values[9] = "description";
}

void loop() {
  readSerialPort(&var_id,&var_content,values);
  swiping();
  if(values[0]!= memvalues[0]){
    displayDate();
    memvalues[0]= values[0];
  }
  if(values[4]!= memvalues[4]){
    displayTemp();
    memvalues[4]= values[4];
  }

 
  // Defilement du menu
  if(cpt == 0 ){
    int myCheck[] = {1,2,3,5,7,9};
    if(memcpt != cpt || checkValues(values,memvalues,myCheck,6)){
      tft.fillRect(5, 60, 470, 255, BLACK);
      delay(10);
      tft.setTextColor(ORANGE);
      tft.setTextSize(5);
      tft.setCursor(40,80);
      tft.print(values[1]); //jour
      tft.print(" - ");
      tft.print(values[7]); // date du jour
      tft.setTextColor(WHITE);
      tft.setCursor(40,150);
      tft.print(values[2]); // mois
      tft.setCursor(40, 230);
      tft.print(values[3]); // annee 
      tft.setCursor(260,150);
      tft.setTextSize(3);
      tft.setTextColor(CYAN);
      tft.print("T.xt: "); 
      tft.print(values[5]); // temperature externe
      tft.setCursor(220,200);
      tft.print(values[9]);
      // Serial.println(dayOfW[3]);
      sameValues(values,memvalues,myCheck,6);
      memcpt = cpt;
    }
  }

  if(cpt == 1 ){// MENU TEMPERATURE
  int myCheck1[] = {4,5,6};
    if(memcpt != cpt || checkValues(values,memvalues,myCheck1,3)){
      tft.fillRect(5, 60, 470, 255, BLACK);
      tft.setTextColor(WHITE);
      tft.setTextSize(4);
      tft.setCursor(40,80);
      tft.print("temperature int: "); 
      tft.setCursor(150,130);
      tft.setTextColor(CYAN);
      tft.println(values[4]);
      tft.setTextColor(WHITE);
      tft.setCursor(40,180);
      tft.print("humidite: "); 
      tft.setCursor(150,230);
      tft.setTextColor(CYAN);
      tft.println(values[6]);
      sameValues(values,memvalues,myCheck1,3);
      memcpt = cpt;
    }
  }

  if (cpt >= 2 && memcpt != cpt){
    describeMenu("En cours de developpement mon reuf");
    memcpt = cpt;
  }
}