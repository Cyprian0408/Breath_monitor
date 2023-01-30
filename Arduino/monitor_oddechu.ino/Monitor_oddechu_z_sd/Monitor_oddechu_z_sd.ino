#include <Wire.h>
#include <MPU6050.h>
#include <LiquidCrystal_I2C.h> 
#include <SPI.h>
#include <SD.h>
#define CSPin  4
#define buzzerPin 9
// Zmienne potrzebne do wyświetlania na ekranie LCD czasu pomiaru aktywności oddechowej.
int h = 0;
int m = 0;
int s = 0;
int flag = 0;
LiquidCrystal_I2C lcd (0x27, 16, 2);//Informacja o podłączeniu nowego wyświetlacza
template <class T>
void display (byte row, T string)
{
  delay(500);
  lcd.clear();
  lcd.setCursor(0, row);
  lcd.print(string);
 
} 
MPU6050 mpu;
File dataFile;
void setup() {
lcd.init();
lcd.backlight();
lcd.clear();

Serial.begin(9600);
while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
}
display(0,"Initializing SD");
Serial.print("Initializing SD card...\n");
if (!SD.begin(CSPin)) {
  Serial.println("initialization failed!\n");
  while (1);
}
Serial.println("initialization done.");
if(SD.exists("dataFile.txt")){
  SD.remove("dataFile.txt");
}
dataFile =SD.open("dataFile.txt",FILE_WRITE); //open file
if(!dataFile){ 
    Serial.println("Couldn't open file."); 
}
dataFile.print(" Time      "); 
dataFile.print("Xaxis         "); 
dataFile.print("Yaxis             "); 
dataFile.print("Zaxis"); dataFile.print("\n");
dataFile.flush();
display(0,"Done");
while(!mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_16G))
  {
    Serial.println("Nie mozna znalezc MPU6050 - sprawdz polaczenie!"); // Sprawdzenie czy czujnik jest podłączony.
    delay(500);
  }
// Dodatkowe opoznienie zasilania akcelerometru 3ms
mpu.setAccelPowerOnDelay(MPU6050_DELAY_3MS);
 
  // Wylaczamy sprzetowe przerwania dla wybranych zdarzen
mpu.setIntFreeFallEnabled(false);  
mpu.setIntZeroMotionEnabled(false);
mpu.setIntMotionEnabled(false);
 
  // Ustawiamy filtr gorno-przepustowy
mpu.setDHPFMode(MPU6050_DHPF_5HZ);
 
  // Ustawiamy granice wykrywania ruchu na 2mg (zadana wartosc dzielimy przez 2)
  // oraz minimalny czas trwania na 5ms
mpu.setMotionDetectionThreshold(1);
mpu.setMotionDetectionDuration(5);
 
  // Ustawiamy granice wykrywania bezruchu na 20mg (zadana wartosc dzielimy przez 2)
  // oraz minimalny czas trwania na 20ms
  //mpu.setZeroMotionDetectionThreshold(10);
  //mpu.setZeroMotionDetectionDuration(20);  
checkSettings(); 
}
void checkSettings(){
display(0,"Settings");
Serial.println();
Serial.print(" * Sleep Mode:            ");
Serial.println(mpu.getSleepEnabled() ? "Enabled" : "Disabled");

}
void loop() {
  Activites act = mpu.readActivites(); // Funkcja sprawdzająca, czy akcelerometr jest w ruchu.
  if (act.isActivity)
  {
    digitalWrite(buzzerPin, LOW);
    Serial.print("Pacjent oddycha \n");
  } else
  {
    digitalWrite(buzzerPin, HIGH);
    tone(buzzerPin, 50);
    //delay(500);
    //noTone(buzzerPin);
    //delay(500);
    Serial.print("Pacjent nie oddycha \n");
  }

  // Odczytywanie znormalizowanych zmian położenia akcelerometru w osiach X, Y, Z.
  Vector normAccel = mpu.readNormalizeAccel();
  
  Serial.print(" Xnorm = ");
  Serial.print(normAccel.XAxis);
  Serial.print(" Ynorm = ");
  Serial.print(normAccel.YAxis);
  Serial.print(" Znorm = ");
  Serial.println(normAccel.ZAxis);

  // Wyświetlanie na ekranie LCD czasu pomiaru aktywności oddechowej.
  lcd.setCursor(0, 0);
  s = s + 1;
  lcd.print("Czas:" );
  lcd.print(h);
  lcd.print("h");
  lcd.print(":");
  lcd.print(m);
  lcd.print("m");
  lcd.print(":");
  lcd.print(s);
  lcd.print("s");
  if (flag == 24) flag = 0;
  delay(1000);
  lcd.clear();
  if (s == 60)
  {
    s = 0;
    m = m + 1;
  }
  if (m == 60)
  {
    m = 0;
    h = h + 1;
    flag = flag + 1;
  }
  if (h == 13)
  {
    h = 1;
  }
  lcd.setCursor(0, 1);
  if (act.isActivity)
  {
    lcd.print("Pacjent oddycha");
  } else
  {
    lcd.print("Brak oddechu");
  }
  dataFile.print(h); dataFile.print("h"); 
  dataFile.print(m); dataFile.print("m"); 
  dataFile.print(s); dataFile.print("s"); dataFile.print("\t");
  dataFile.print(normAccel.XAxis,6); dataFile.print("\t");
  dataFile.print(normAccel.YAxis,6); dataFile.print("\t");
  dataFile.print(normAccel.ZAxis,6); dataFile.print("\t");
  dataFile.print("\n");
  Serial.println("Zapis linii do pliku");
  
  //save,  close, open file again
  dataFile.flush();
}
