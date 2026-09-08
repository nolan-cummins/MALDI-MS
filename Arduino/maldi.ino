#include <AccelStepper.h>

// 104.73 - 42.33 = 62.4 mm / 100,000 steps = 1602.564103 steps/mm (Y)
// 107.42 - 44.78 = 62.64 mm / 100,000 steps = 1596.42401 steps/mm (X)
// 49.5 - 19.14 = 30.36 / 50,000 steps = 1646.903821 steps/mm (A/Z)
// Average = 1630.077217 steps/mm, 1.630077217 steps/um

// Protoneer V3 CNC Shield Pins
#define EN_PIN 8
#define X_STEP 2
#define X_DIR  5
#define Y_STEP 3
#define Y_DIR  6
#define A_STEP 12 
#define A_DIR  13 

AccelStepper stepperX(AccelStepper::DRIVER, X_STEP, X_DIR);
AccelStepper stepperY(AccelStepper::DRIVER, Y_STEP, Y_DIR);
AccelStepper stepperA(AccelStepper::DRIVER, A_STEP, A_DIR);

AccelStepper* steppers[] = {&stepperX, &stepperY, &stepperA};
char axisLabels[] = {'X', 'Y', 'A'};

// Global State
long setpoints[3] = {0, 0, 0}; 
float defaultSpeed = 1000.0;
float defaultAccel = 500.0;

// Printing State Variables
unsigned long lastPrintTime = 0;

void setup() {
  Serial.begin(115200);
  pinMode(EN_PIN, OUTPUT);
  digitalWrite(EN_PIN, LOW);

  for(int i = 0; i < 3; i++) {
    steppers[i]->setMaxSpeed(defaultSpeed);
    steppers[i]->setAcceleration(defaultAccel);
  }
}

void printPositionUpdates(bool force = false) {
  bool needsPrint = force;
  bool isMoving[3];
  bool anyMoving = false;

  // 1. Evaluate movement states
  for (int i = 0; i < 3; i++) {
    isMoving[i] = (steppers[i]->currentPosition() != setpoints[i]);
    if (isMoving[i]) anyMoving = true;
  }

  // 2. Broadcast constantly: ~30Hz while moving, ~4Hz while idle
  unsigned long currentMillis = millis();
  if (anyMoving && (currentMillis - lastPrintTime >= 33)) {
    needsPrint = true;
  } else if (!anyMoving && (currentMillis - lastPrintTime >= 250)) {
    needsPrint = true;
  }

  // 3. Fast Parsable String: P:X:Y:Z:Xs:Ys:Zs:Xspd:Yspd:Zspd:Xacc:Yacc:Zacc:Timestamp
  if (needsPrint) {
    Serial.print("P:");
    // Positions
    Serial.print(steppers[0]->currentPosition()); Serial.print(":");
    Serial.print(steppers[1]->currentPosition()); Serial.print(":");
    Serial.print(steppers[2]->currentPosition()); Serial.print(":");
    // Setpoints
    Serial.print(setpoints[0]); Serial.print(":");
    Serial.print(setpoints[1]); Serial.print(":");
    Serial.print(setpoints[2]); Serial.print(":");
    // Current Speeds (Instantaneous)
    Serial.print(steppers[0]->speed()); Serial.print(":");
    Serial.print(steppers[1]->speed()); Serial.print(":");
    Serial.print(steppers[2]->speed()); Serial.print(":");
    // Configured Accelerations
    Serial.print(currentAccels[0]); Serial.print(":");
    Serial.print(currentAccels[1]); Serial.print(":");
    Serial.print(currentAccels[2]); Serial.print(":");
    // Timestamp
    Serial.println(currentMillis);
    lastPrintTime = currentMillis;
  }
}

int getAxisIndex(char axisChar) {
  if (axisChar == 'X' || axisChar == 'x') return 0;
  if (axisChar == 'Y' || axisChar == 'y') return 1;
  if (axisChar == 'A' || axisChar == 'a') return 2;
  return -1;
}

int getAxisIndex(char axisChar) {
  if (axisChar == 'X' || axisChar == 'x') return 0;
  if (axisChar == 'Y' || axisChar == 'y') return 1;
  if (axisChar == 'A' || axisChar == 'a') return 2;
  return -1;
}

void processCommand(String cmd) {
  cmd.trim();
  if (cmd.length() == 0) return;

  if (cmd == "S" || cmd == "s") {
    for (int i = 0; i < 3; i++) {
      setpoints[i] = steppers[i]->currentPosition();
    }
    printPositionUpdates(true);
    return;
  }

  const int MAX_TOKENS = 6;
  String tokens[MAX_TOKENS];
  int tokenCount = 0;
  int startIndex = 0;

  for (int i = 0; i < cmd.length() && tokenCount < MAX_TOKENS; i++) {
    if (cmd.charAt(i) == ':') {
      tokens[tokenCount++] = cmd.substring(startIndex, i);
      startIndex = i + 1;
    }
  }
  if (tokenCount < MAX_TOKENS) {
    tokens[tokenCount++] = cmd.substring(startIndex);
  }

  char cmdType = tokens[0].charAt(0);

  if ((cmdType == 'A' || cmdType == 'a') && tokenCount >= 3) {
    int axis = getAxisIndex(tokens[1].charAt(0));
    if (axis == -1) return;
    
    setpoints[axis] = tokens[2].toInt();
    float spd = (tokenCount >= 4) ? tokens[3].toFloat() : defaultSpeed;
    float acc = (tokenCount >= 5) ? tokens[4].toFloat() : defaultAccel;
    
    steppers[axis]->setMaxSpeed(spd);
    steppers[axis]->setAcceleration(acc);
  }
  else if ((cmdType == 'C' || cmdType == 'c') && tokenCount >= 4) {
    setpoints[0] = tokens[1].toInt();
    setpoints[1] = tokens[2].toInt();
    setpoints[2] = tokens[3].toInt();
    
    float spd = (tokenCount >= 5) ? tokens[4].toFloat() : defaultSpeed;
    float acc = (tokenCount >= 6) ? tokens[5].toFloat() : defaultAccel;

    for (int i = 0; i < 3; i++) {
      steppers[i]->setMaxSpeed(spd);
      steppers[i]->setAcceleration(acc);
    }
  }
  else if ((cmdType == 'D' || cmdType == 'd') && tokenCount >= 3) {
    tokens[1].toUpperCase();
    if (tokens[1] == "SPEED") defaultSpeed = tokens[2].toFloat();
    else if (tokens[1] == "ACCEL" || tokens[1] == "ACCELERATION") defaultAccel = tokens[2].toFloat();
  }
  else if ((cmdType == 'Z' || cmdType == 'z')) {
    for (int i = 0; i < 3; i++) {
      steppers[i]->setCurrentPosition(0);
      setpoints[i] = 0;
    }
    printPositionUpdates(true); // Force broadcast
  }
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    processCommand(input);
  }

  for (int i = 0; i < 3; i++) {
    if (steppers[i]->targetPosition() != setpoints[i]) {
      steppers[i]->moveTo(setpoints[i]);
    }
    steppers[i]->run();
  }

  printPositionUpdates();
}