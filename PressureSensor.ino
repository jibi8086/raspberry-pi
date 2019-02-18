int GREEN = 2;
int YELLOW = 3;
int RED = 4;

 
int fsrPin = 0;     // the FSR and 10K pulldown are connected to a0
int fsrReading;     // the analog reading from the FSR resistor divider
int LEDpin = 13; 
void setup(void) {
  // We'll send debugging information via the Serial monitor
  Serial.begin(9600); 
pinMode(LEDpin, OUTPUT);  
}
 
void loop(void) {
  fsrReading = analogRead(fsrPin);  
 
  Serial.print("Analog reading = ");
  Serial.print(fsrReading);     // the raw analog reading
 
  // We'll have a few threshholds, qualitatively determined
  if (fsrReading < 10) {
    Serial.println(" - No pressure");
     digitalWrite(LEDpin, LOW);
  } else if (fsrReading < 200) {
     digitalWrite(LEDpin, LOW);
    Serial.println(" - Light touch");
  } else if (fsrReading < 500) {
    digitalWrite(LEDpin, LOW);
    Serial.println(" - Light squeeze");
  } else if (fsrReading < 800) {
    Serial.println(" - Medium squeeze");
      digitalWrite(LEDpin, HIGH);
  } else {
    Serial.println(" - Big squeeze");
  }
  //delay(1000);
} 
