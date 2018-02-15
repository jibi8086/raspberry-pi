
/* Author:Jibin Joseph
   Create date: 09-02-2018
   Description:	Buzzer*/


//Declare PinNumber
const int buzzer1 = 2;
const int buzzer2 = 3;      
const int buzzer3 = 4;   
const int buzzer4 = 5; 
const int buzzer5 = 8;  
const int ledPinBuzzer=9;
//Declare Button state set as zero
int buttonState1 = 0;         
int buttonState2 = 0;
int buttonState3 = 0;
int buttonState4 = 0;
int buttonState5 = 0;
// pinMode set as input
void setup()
	 {
		Serial.begin(9800);
		pinMode(buzzer1, INPUT);
		pinMode(buzzer2, INPUT);
		pinMode(buzzer3, INPUT);
		pinMode(buzzer4, INPUT);
	    pinMode(buzzer5, INPUT);
        pinMode(ledPinBuzzer, OUTPUT);
	}

void loop()
    {  
        //Read Buzzer 
   		buttonState1 = digitalRead(buzzer1);
   		buttonState2= digitalRead(buzzer2);
   		buttonState3 = digitalRead(buzzer3);
 		buttonState4 = digitalRead(buzzer4);
		buttonState5 = digitalRead(buzzer5);
        Serial.print("TEAM C =");
		Serial.println(buttonState1);
		Serial.print("TEAM B =");
		Serial.println(buttonState2);
		Serial.print("TEAM D =");
		Serial.println(buttonState3);
		Serial.print("TEAM A =");
		Serial.println(buttonState4);
		Serial.print("TEAM E =");
		Serial.println(buttonState5);
        //Check buzzer switch is active or not
  		if (buttonState1 == HIGH)
			  {
                Serial.print("********** TEAM C **********");
                digitalWrite(ledPinBuzzer, HIGH); 
                delay(1000);
                digitalWrite(ledPinBuzzer, LOW);
			    delay(4000);
			  }
         else if(buttonState5 == HIGH)
             {
                digitalWrite(ledPinBuzzer, HIGH);
                Serial.print("********** TEAM E **********");
                digitalWrite(ledPinBuzzer, HIGH); 
                delay(1000);
                digitalWrite(ledPinBuzzer, LOW);
			    delay(4000);        
             }
		 else if(buttonState2 == HIGH)
			  {
                digitalWrite(ledPinBuzzer, HIGH);
                Serial.print("********** TEAM B **********");
    			digitalWrite(ledPinBuzzer, HIGH); 
                delay(1000);
                digitalWrite(ledPinBuzzer, LOW);
			    delay(4000);
  			  }
		else if(buttonState3 == HIGH)
    			{
               	  digitalWrite(ledPinBuzzer, HIGH);
              	  Serial.print("********** TEAM D **********");
      			  digitalWrite(ledPinBuzzer, HIGH); 
             	  delay(1000);
            	  digitalWrite(ledPinBuzzer, LOW);
				  delay(4000);
    			}
 		else if(buttonState4 == HIGH)
			    {
                    digitalWrite(ledPinBuzzer, HIGH);
                    Serial.print("********** TEAM A **********");
			        digitalWrite(ledPinBuzzer, HIGH); 
                    delay(1000);
                    digitalWrite(ledPinBuzzer, LOW);
			        delay(4000);
			    }   
		/*else if(buttonState5 == HIGH)
			    {
			        delay(4000);
			    }*/
    }
