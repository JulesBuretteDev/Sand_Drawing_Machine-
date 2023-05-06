
void readSerialPort(int *var_id, float *var_content,float values[]) {
    String msg = "";
    if (Serial.available() > 1) {
        delay(10);
        while (Serial.available() > 0) {
            msg += (char)Serial.read();
        }
        // Serial.println(msg);
        Serial.flush();
        int sep_index = msg.indexOf('=');
      *var_id = msg.substring(0, sep_index).toInt();
      *var_content = msg.substring(sep_index + 1, sizeof(msg) - 1).toFloat();
      updateValues(var_id,var_content,values);
      // Serial.print("var_id");
      // Serial.print(*var_id);
      // Serial.print("var_content");
      // Serial.println(*var_content);
    }  
}

void updateValues(int *var_id, float *var_content,float values[]){
    values[*var_id] = *var_content;
    showValues(values);
}

void showValues(float values[]){
  for(int i=0; i < 20; i++){
    Serial.println(values[i]);
  }
}


int var_id = 0;
float var_content = 0;
float values[20];

void setup() {
  Serial.begin(9600); // set baud rate to 9600
}

void loop() {
  readSerialPort(&var_id,&var_content,values);
}