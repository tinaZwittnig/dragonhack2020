#include <PubSubClient.h>
#include <ESP8266WiFi.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// Definitions for OneWire sensor
#define ONE_WIRE_BUS D6
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// WiFi & MQTT settings
const char* ssid = "iot-farm";
const char* password = "wifi-pass";
const char* mqtt_server = "openfarm.v8.si";


WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
float temp = 0;

// Pin definitions
int inPin = D6;
int voltagePin = A0;


// WiFi setup function
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}


// WiFi reconnect function
void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // connect to broker client_id, user,pass
    if (client.connect("pastir","malina","Malina1234")) {
      Serial.println("connected");
      client.publish("status", "pastir is conncted",1);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}
 
void setup()
{
  // setup Serial for debug ;)
  Serial.begin(115200);
  setup_wifi(); 
  client.setServer(mqtt_server, 1883);
  pinMode(inPin, INPUT);
  sensors.begin();
}

void loop()
{
  // reconnect if necessary
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  //publish message every 1 second
  long now = millis();
  if (now - lastMsg > 1000) {
    lastMsg = now;
    // read temperature
    sensors.setResolution(12);
    sensors.requestTemperatures();
    temp = sensors.getTempCByIndex(0);
    Serial.print("Temp: ");
    Serial.println(temp);
    // read ADC and convert to voltage
    float voltage = float(analogRead(A0)) * 0.021;
    Serial.print("Voltage");
    Serial.println(voltage);
    if(temp != -127)
      {
      client.publish("pastir/temperatura", String(temp).c_str(),1);
      client.publish("pastir/napetost", String(voltage).c_str(),1);
      }
  }
}
