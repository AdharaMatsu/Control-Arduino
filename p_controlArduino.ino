int LED = 12;

void setup() {
    pinMode(LED, OUTPUT);
  
    Serial.begin(9600);
    Serial.setTimeout(250);
}


int valor = 0;
void loop() {
  if(Serial.available()>0){
    valor = Serial.readString().toInt();
    digitalWrite(LED, valor); 

    }

  Serial.println(String(valor));
  delay(100);
}
