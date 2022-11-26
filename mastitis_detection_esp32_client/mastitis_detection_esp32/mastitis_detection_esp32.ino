// Import required libraries
#include <WiFi.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <Adafruit_MLX90614.h>

const int buzzer = 18; //buzzer
Adafruit_MLX90614 mlx = Adafruit_MLX90614();
const int buttonPin = 13; // push button
int buttonState = 0;   // button state
double temp = 0; // body tempreture
const double bodyTempThreshold = 29.5;
const double mastitisBeepDuration = 1000; // 1 second
const double tempDetectionBeepDuration = 100; // 100 milliseconds
const double getTempDelay = 500;
// setup AP Wifi station credentials
const char* ssid = "KZFarm";
const char* password = "12345678";
// led state
bool mastitisState = 0;
// ledpin
const int ledPin = 26; // Beep threshold

// Create AsyncWebServer object on port 80
AsyncWebServer server(80);
AsyncWebSocket ws("/ws");

const char index_html[] PROGMEM = R"rawliteral(
<!DOCTYPE HTML><html>
<head>
  <title>Dashboard - AI Based Mastits Detecting System</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,">
  <style>
  html {
    font-family: Arial, Helvetica, sans-serif;
    text-align: center;
  }
  h1 {
    font-size: 1.8rem;
    color: white;
  }
  h2{
    font-size: 1.5rem;
    font-weight: bold;
    color: #143642;
  }
  .topnav {
    overflow: hidden;
    background-color: #143642;
  }
  body {
    margin: 0;
  }
  .content {
    padding: 30px;
    max-width: 600px;
    margin: 0 auto;
  }
  .card {
    background-color: #F8F7F9;;
    box-shadow: 2px 2px 12px 1px rgba(140,140,140,.5);
    padding-top:10px;
    padding-bottom:20px;
  }
  .button {
    padding: 15px 50px;
    font-size: 24px;
    text-align: center;
    outline: none;
    color: #fff;
    background-color: #0f8b8d;
    border: none;
    border-radius: 5px;
    -webkit-touch-callout: none;
    -webkit-user-select: none;
    -khtml-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    -webkit-tap-highlight-color: rgba(0,0,0,0);
   }
   /*.button:hover {background-color: #0f8b8d}*/
   .button:active {
     background-color: #0f8b8d;
     box-shadow: 2 2px #CDCDCD;
     transform: translateY(2px);
   }

   .martitis-btn{
    padding: 15px 50px;
    font-size: 24px;
    text-align: center;
    outline: none;
    color: #fff;
    background-color: #04831f;
    border: none;
    border-radius: 5px;
    -webkit-touch-callout: none;
    -webkit-user-select: none;
    -khtml-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    -webkit-tap-highlight-color: rgba(0,0,0,0);
   }
   .martitis-detected{
    background-color: #cf2008;
   }

   .no-martitis-detected{
    background-color: #04831f;
   }

   .sub-martitis-detected{
     background-color: #FFCA2C;
   }
   .state {
     font-size: 1.6rem;
     color:#8c8c8c;
     font-weight: bold;
   }
  </style>
<title>AI Based Mastits Detecting System</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:,">
</head>
<body>
  <div class="topnav">
    <h1>AI Based Mastits Detecting System</h1>
  </div>
  <div class="content">
    <div class="card">
      <h2>Detected Tempreture:</h2>
      <p class="state"><span id="tempreture">0<sup><small>o</small></sup>C</span></p>
      <h2>Current Tempreture:</h2>
      <p class="state current-temp"><span id="current-tempreture">0<sup><small>o</small></sup>C</span></p>
      <p><button id="mastits-detection" class="martitis-btn no-martitis-detected">NO MASTITIS DETECTED</button></p>
    </div>
  </div>
<script>
  var gateway = `ws://192.168.4.1/ws`;
  var websocket;
  window.addEventListener('load', onLoad);
  function initWebSocket() {
    console.log('Trying to open a WebSocket connection...');
    websocket = new WebSocket(gateway);
    websocket.onopen    = onOpen;
    websocket.onclose   = onClose;
    websocket.onmessage = onMessage; // <-- add this line
  }
  function onOpen(event) {
    console.log('Connection opened');
  }
  function onClose(event) {
    console.log('Connection closed');
    setTimeout(initWebSocket, 2000);
  }
  function onMessage(event) {
    var state = event.data.split(":");
    console.log(state);
    var cmd = state[0];
    var value = state[1];    
    if (cmd == "DT"){
      document.getElementById('tempreture').innerHTML = value + "<sup><small>o</small></sup>C";
    }else if(cmd == "CT"){
      document.getElementById('current-tempreture').innerHTML = value + "<sup><small>o</small></sup>C";
    }else{
    if (cmd == "CM"){
       document.querySelector("#mastits-detection").classList.add("martitis-detected");
        document.querySelector("#mastits-detection").innerHTML=value;
        //////////////////////////
        document.querySelector("#mastits-detection").classList.remove("sub-martitis-detected");
        document.querySelector("#mastits-detection").classList.remove("no-martitis-detected");
    }else if(cmd == "SCM"){
      document.querySelector("#mastits-detection").classList.add("sub-martitis-detected");
        document.querySelector("#mastits-detection").innerHTML=value;
        /////////////////////////
        document.querySelector("#mastits-detection").classList.remove("martitis-detected");
        document.querySelector("#mastits-detection").classList.remove("no-martitis-detected");
    }else{
        document.querySelector("#mastits-detection").classList.add("no-martitis-detected");
        document.querySelector("#mastits-detection").innerHTML=value;
        ///////////////////////
        document.querySelector("#mastits-detection").classList.remove("martitis-detected");
        document.querySelector("#mastits-detection").classList.remove("sub-martitis-detected");
      }
    }
  }
  function onLoad(event) {
    initWebSocket();
  }
</script>
</body>
</html>
)rawliteral";

void notifyClients(String &mtemp) {
  // notify other clients that mastitcs is detected
  // String mtemp = "MT:MD";
  ws.textAll(String(mtemp));
}

void handleWebSocketMessage(void *arg, uint8_t *data, size_t len) {
  AwsFrameInfo *info = (AwsFrameInfo*)arg;
  if (info->final && info->index == 0 && info->len == len && info->opcode == WS_TEXT) {
    data[len] = 0;
      String text = (char*)data;
      Serial.println(text);
    if(text != ""){
    ////////myString.indexOf("Arduino");
    if(text.indexOf("CM:") > 0){
     // contains mastitis
        mastitisState = 1;
    }else if(text.indexOf("SCM:") > 0){
        mastitisState = 1;
    }else{
      mastitisState = 0;      
    }
    notifyClients(text);
    }
  }
}

void onEvent(AsyncWebSocket *server, AsyncWebSocketClient *client, AwsEventType type,
             void *arg, uint8_t *data, size_t len) {
  switch (type) {
    case WS_EVT_CONNECT:
      Serial.printf("WebSocket client #%u connected from %s\n", client->id(), client->remoteIP().toString().c_str());
      break;
    case WS_EVT_DISCONNECT:
      Serial.printf("WebSocket client #%u disconnected\n", client->id());
      break;
    case WS_EVT_DATA:
      handleWebSocketMessage(arg, data, len);
      break;
    case WS_EVT_PONG:
    case WS_EVT_ERROR:
      break;
  }
}

void initWebSocket() {
  ws.onEvent(onEvent);
  server.addHandler(&ws);
}

String processor(const String& var){
  Serial.println(var);
  if(var == "STATE"){
    if (mastitisState){
      return "ON";
    }
    else{
      return "OFF";
    }
  }
  return String();
}

void setup(){
  // Serial port for debugging purposes
  Serial.begin(115200);
    /////// setup led
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
  /////////////  setup buzzer
  pinMode(buzzer, OUTPUT); // Set buzzer - pin 9 as an output
  //////// setup button
  pinMode(buttonPin, INPUT);
  ////// setup buzzer
  digitalWrite(buzzer, LOW);
  ////////
  Serial.print("Setting AP (Access Point)…");
  // Remove the password parameter, if you want the AP (Access Point) to be open
  WiFi.softAP(ssid, password);
  //////
  IPAddress IP = WiFi.softAPIP();
  ////////
  Serial.print("AP IP address: ");
  Serial.println(IP);
  initWebSocket();
  // Route for root / web page
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/html", index_html, processor);
  });
  // start server
   // Start server
  Serial.print("Sarting server.....");
  server.begin();
  Serial.print("Sarting mxl sensor…");  
  while (!Serial);
  if (!mlx.begin()) {
    Serial.println("Error connecting to MLX sensor.");
    while (1);
  };
}
///loop
void loop() {
  ws.cleanupClients();
  // read object tempreture
  temp = mlx.readObjectTempC();
  // read button state
  buttonState = digitalRead(buttonPin);
  // if button is high proceed and check current tempreture from sensor
  if(buttonState == HIGH){
  Serial.println("TEMP: ");
  Serial.println(temp);
  // notify all the clients about the current tempreture
  // detected tempreture
  String stemp = "DT:" + String(temp);
  ws.textAll(stemp);
  //////////////////////
  if(temp > bodyTempThreshold){
    digitalWrite(buzzer, HIGH);
    delay(tempDetectionBeepDuration);
    digitalWrite(buzzer, LOW);
  }else{
  digitalWrite(buzzer, LOW);
  }    
  }else{
    // current tempreture
    String ctemp = "CT:" + String(temp);
    ws.textAll(ctemp);   
  }
  // if mastitis has been detected in a cow 
  // TO DO: Make a long beep
  if(mastitisState){ 
    // open states
  digitalWrite(buzzer, LOW);
    // turn on the LED
    digitalWrite(ledPin, mastitisState);
    // turn on the buzzer
    digitalWrite(buzzer, mastitisState);
    delay(mastitisBeepDuration);
    // reset all states after beep delay is timed out
    mastitisState = LOW;
    digitalWrite(buzzer, LOW);
    digitalWrite(ledPin, LOW);
    // resent mastits state on all clients
    //  String mtemp = "MT:MN";
    //  ws.textAll(String(mtemp));
  }
  delay(getTempDelay);
}


