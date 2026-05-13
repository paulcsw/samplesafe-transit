/*
  SampleSafe Transit firmware MVP

  Default mode is a serial dry run so the state machine can be tested before
  exact board libraries and wiring are confirmed. Set ENABLE_SENSOR_LIBS to 1
  after installing the listed Adafruit libraries and verifying the I2C wiring.
*/

#define ENABLE_SENSOR_LIBS 0

#include <Arduino.h>
#include <math.h>

#if ENABLE_SENSOR_LIBS
#include <Wire.h>
#include <Adafruit_APDS9960.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_Si7021.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#endif

enum TransportState {
  SAFE,
  WATCH,
  RISK,
  INSPECT_NEEDED
};

struct SensorFrame {
  bool lidOpen;
  bool lightIngress;
  bool sampleMissing;
  bool shock;
  bool tiltHold;
  bool warmDrift;
  float temperatureC;
  float humidityPct;
  float accelMagnitude;
};

const uint32_t CALIBRATION_MS = 5000;
const uint32_t SAMPLE_INTERVAL_MS = 250;
const float WARM_DRIFT_C = 4.0;
const float HUMIDITY_DRIFT_PCT = 12.0;
const float SHOCK_G = 2.2;
const float TILT_G_DELTA = 0.45;

const int RGB_RED_PIN = 25;
const int RGB_GREEN_PIN = 26;
const int RGB_BLUE_PIN = 27;
const int BUZZER_PIN = 14;

TransportState state = SAFE;
String latestReason = "baseline";
uint32_t bootMs = 0;
uint32_t lastSampleMs = 0;
float baselineTempC = 25.0;
float baselineHumidityPct = 50.0;
float baselineAccelMagnitude = 1.0;

bool dryLidOpen = false;
bool dryShock = false;
bool dryWarmDrift = false;

#if ENABLE_SENSOR_LIBS
Adafruit_APDS9960 apds;
Adafruit_MPU6050 mpu;
Adafruit_Si7021 si7021;
Adafruit_SSD1306 display(128, 64, &Wire, -1);
bool apdsReady = false;
bool mpuReady = false;
bool si7021Ready = false;
bool displayReady = false;
#endif

const char *stateName(TransportState value) {
  switch (value) {
    case SAFE:
      return "SAFE";
    case WATCH:
      return "WATCH";
    case RISK:
      return "RISK";
    case INSPECT_NEEDED:
      return "INSPECT_NEEDED";
  }
  return "UNKNOWN";
}

void logEvent(const char *eventName, const String &reason) {
  Serial.print("event_ms=");
  Serial.print(millis());
  Serial.print(",state=");
  Serial.print(stateName(state));
  Serial.print(",event=");
  Serial.print(eventName);
  Serial.print(",reason=");
  Serial.println(reason);
}

void setState(TransportState nextState, const String &reason) {
  if (state == INSPECT_NEEDED && nextState != SAFE) {
    latestReason = reason;
    return;
  }

  if (state != nextState || latestReason != reason) {
    state = nextState;
    latestReason = reason;
    logEvent("state_change", reason);
  }
}

void clearInspectionLatch() {
  state = SAFE;
  latestReason = "manual reset after inspection";
  logEvent("manual_reset", latestReason);
}

void updateAlertOutputs() {
  int red = LOW;
  int green = LOW;
  int blue = LOW;
  int buzzer = LOW;

  if (state == SAFE) {
    green = HIGH;
  } else if (state == WATCH) {
    blue = HIGH;
  } else if (state == RISK) {
    red = HIGH;
    blue = HIGH;
    buzzer = HIGH;
  } else if (state == INSPECT_NEEDED) {
    red = HIGH;
    buzzer = HIGH;
  }

  digitalWrite(RGB_RED_PIN, red);
  digitalWrite(RGB_GREEN_PIN, green);
  digitalWrite(RGB_BLUE_PIN, blue);
  digitalWrite(BUZZER_PIN, buzzer);
}

void updateDisplay() {
#if ENABLE_SENSOR_LIBS
  if (displayReady) {
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 0);
    display.print("SampleSafe Transit");
    display.setCursor(0, 18);
    display.print("State: ");
    display.print(stateName(state));
    display.setCursor(0, 36);
    display.print("Reason: ");
    display.print(latestReason);
    display.display();
  }
#endif
}

void printDryRunHelp() {
  Serial.println("SampleSafe Transit dry-run commands:");
  Serial.println("  l = toggle lid/light exposure");
  Serial.println("  s = trigger shock/tilt event");
  Serial.println("  w = toggle warm/humidity drift");
  Serial.println("  c = close lid and keep Inspect Needed latched");
  Serial.println("  r = manual reset after inspection");
}

void handleSerialCommands() {
  while (Serial.available() > 0) {
    char command = Serial.read();
    if (command == 'l') {
      dryLidOpen = !dryLidOpen;
      logEvent("dry_lid_toggle", dryLidOpen ? "lid/light exposure active" : "lid closed");
    } else if (command == 's') {
      dryShock = true;
      logEvent("dry_shock", "shock/tilt injected");
    } else if (command == 'w') {
      dryWarmDrift = !dryWarmDrift;
      logEvent("dry_warm_toggle", dryWarmDrift ? "warm drift active" : "warm drift cleared");
    } else if (command == 'c') {
      dryLidOpen = false;
      logEvent("dry_close_lid", "lid closed; inspection latch remains if already set");
    } else if (command == 'r') {
      dryLidOpen = false;
      dryShock = false;
      dryWarmDrift = false;
      clearInspectionLatch();
    } else if (command == 'h' || command == '?') {
      printDryRunHelp();
    }
  }
}

SensorFrame readSensors() {
  SensorFrame frame;
  frame.lidOpen = dryLidOpen;
  frame.lightIngress = dryLidOpen;
  frame.sampleMissing = false;
  frame.shock = dryShock;
  frame.tiltHold = dryShock;
  frame.warmDrift = dryWarmDrift;
  frame.temperatureC = baselineTempC + (dryWarmDrift ? WARM_DRIFT_C + 1.0 : 0.0);
  frame.humidityPct = baselineHumidityPct + (dryWarmDrift ? HUMIDITY_DRIFT_PCT + 2.0 : 0.0);
  frame.accelMagnitude = baselineAccelMagnitude + (dryShock ? SHOCK_G + 0.5 : 0.0);

#if ENABLE_SENSOR_LIBS
  if (si7021Ready) {
    frame.temperatureC = si7021.readTemperature();
    frame.humidityPct = si7021.readHumidity();
    frame.warmDrift = fabs(frame.temperatureC - baselineTempC) >= WARM_DRIFT_C ||
                      fabs(frame.humidityPct - baselineHumidityPct) >= HUMIDITY_DRIFT_PCT;
  }

  if (mpuReady) {
    sensors_event_t accel;
    sensors_event_t gyro;
    sensors_event_t temp;
    mpu.getEvent(&accel, &gyro, &temp);
    float ax = accel.acceleration.x / 9.80665;
    float ay = accel.acceleration.y / 9.80665;
    float az = accel.acceleration.z / 9.80665;
    frame.accelMagnitude = sqrt(ax * ax + ay * ay + az * az);
    frame.shock = frame.accelMagnitude >= SHOCK_G;
    frame.tiltHold = fabs(frame.accelMagnitude - baselineAccelMagnitude) >= TILT_G_DELTA;
  }

  if (apdsReady) {
    uint16_t red = 0;
    uint16_t green = 0;
    uint16_t blue = 0;
    uint16_t clear = 0;
    apds.getColorData(&red, &green, &blue, &clear);
    frame.lightIngress = clear > 120;

    uint8_t proximity = apds.readProximity();
    frame.lidOpen = frame.lightIngress || proximity < 20;
    frame.sampleMissing = proximity < 8;
  }
#endif

  return frame;
}

void calibrateBaseline() {
  Serial.println("Calibrating baseline. Keep the prototype closed and still.");
  uint32_t startMs = millis();
  uint16_t samples = 0;
  float tempSum = 0.0;
  float humiditySum = 0.0;
  float accelSum = 0.0;

  while (millis() - startMs < CALIBRATION_MS) {
    handleSerialCommands();
    SensorFrame frame = readSensors();
    tempSum += frame.temperatureC;
    humiditySum += frame.humidityPct;
    accelSum += frame.accelMagnitude;
    samples++;
    delay(SAMPLE_INTERVAL_MS);
  }

  if (samples > 0) {
    baselineTempC = tempSum / samples;
    baselineHumidityPct = humiditySum / samples;
    baselineAccelMagnitude = accelSum / samples;
  }

  logEvent("baseline_ready", "startup calibration complete");
}

void evaluateState(const SensorFrame &frame) {
  if (state == INSPECT_NEEDED) {
    return;
  }

  if (frame.shock || frame.tiltHold || frame.sampleMissing) {
    setState(INSPECT_NEEDED, "shock/tilt/sample removal risk");
    dryShock = false;
    return;
  }

  if (frame.lidOpen || frame.lightIngress || frame.warmDrift) {
    setState(WATCH, "exposure or microclimate drift");
    return;
  }

  setState(SAFE, "baseline within thresholds");
}

void printFrame(const SensorFrame &frame) {
  Serial.print("sample_ms=");
  Serial.print(millis());
  Serial.print(",state=");
  Serial.print(stateName(state));
  Serial.print(",temp_c=");
  Serial.print(frame.temperatureC, 2);
  Serial.print(",humidity_pct=");
  Serial.print(frame.humidityPct, 2);
  Serial.print(",accel_g=");
  Serial.print(frame.accelMagnitude, 2);
  Serial.print(",lid=");
  Serial.print(frame.lidOpen ? "open" : "closed");
  Serial.print(",light=");
  Serial.print(frame.lightIngress ? "yes" : "no");
  Serial.print(",reason=");
  Serial.println(latestReason);
}

void setupHardware() {
  pinMode(RGB_RED_PIN, OUTPUT);
  pinMode(RGB_GREEN_PIN, OUTPUT);
  pinMode(RGB_BLUE_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

#if ENABLE_SENSOR_LIBS
  Wire.begin();
  apdsReady = apds.begin();
  mpuReady = mpu.begin();
  si7021Ready = si7021.begin();
  displayReady = display.begin(SSD1306_SWITCHCAPVCC, 0x3C);

  if (apdsReady) {
    apds.enableProximity(true);
    apds.enableColor(true);
  }

  if (displayReady) {
    display.clearDisplay();
    display.display();
  }
#endif
}

void setup() {
  Serial.begin(115200);
  while (!Serial && millis() < 3000) {
    delay(10);
  }

  bootMs = millis();
  setupHardware();
  printDryRunHelp();
  calibrateBaseline();
  setState(SAFE, "startup baseline ready");
  updateAlertOutputs();
  updateDisplay();
}

void loop() {
  handleSerialCommands();

  if (millis() - lastSampleMs < SAMPLE_INTERVAL_MS) {
    return;
  }

  lastSampleMs = millis();
  SensorFrame frame = readSensors();
  evaluateState(frame);
  updateAlertOutputs();
  updateDisplay();
  printFrame(frame);
}
