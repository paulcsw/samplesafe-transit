---
publishDate: 2026-05-13
title: SampleSafe Transit
excerpt: A MYOSA-based biosample transport integrity monitor that detects lid exposure, rough handling, and microclimate drift during transit.
image: samplesafe-cover.jpg
tags:
  - myosa
  - biosample-transport
  - integrity-monitoring
  - esp32
---
> Turning biosample transport from a single temperature number into a root-cause timeline: exposure, warming, and rough handling.
---

## Acknowledgements

We thank the MYOSA Sensors team for providing the modular MYOSA platform and the MYOSA 5.0 event structure. This prototype was developed as a student project by Yoonho Lee and Seungwoo Choi at the National University of Singapore.

---

## Overview

SampleSafe Transit is a MYOSA-based biosample transport integrity monitoring prototype. It is designed for short-distance laboratory, hospital, and teaching-lab transport workflows where a handler needs to know not only whether a sample box warmed up, but also whether it was opened, exposed to ambient light, shaken, tilted, or subjected to microclimate drift.

The prototype is not a diagnostic device. It does not determine clinical sample validity. Instead, it records transport integrity signals that can help a handler decide whether a box should be inspected, re-stabilized, or reviewed before continued use.

**Key features:**

* Lid-opening and light-ingress detection using APDS9960 proximity and ambient-light readings.
* Rough-handling detection using MPU6050 acceleration and orientation changes.
* Temperature and humidity drift monitoring using the SI7021 sensor.
* A judge-readable state machine: **Safe → Watch → Risk → Inspect Needed**.
* Local OLED/LED/buzzer feedback plus serial event logging as a fallback for the BLE dashboard.

---

## Demo / Examples

### Images

Place the following real project images in the same folder as this markdown file before final submission.

<p align="center">
<img src="/samplesafe-cover.jpg" width="800"><br/>
<i>SampleSafe Transit cover photo showing the assembled prototype.</i>
</p>

<p align="center">
<img src="/samplesafe-prototype.jpg" width="800"><br/>
<i>Prototype enclosure and visible MYOSA hardware.</i>
</p>

<p align="center">
<img src="/samplesafe-internal-sensors.jpg" width="800"><br/>
<i>Internal APDS9960, MPU6050, SI7021, OLED, and wiring layout.</i>
</p>

<p align="center">
<img src="/samplesafe-lid-open-watch.jpg" width="800"><br/>
<i>Lid-open or light-ingress event causing the Watch state.</i>
</p>

<p align="center">
<img src="/samplesafe-rough-handling-risk.jpg" width="800"><br/>
<i>Shake or tilt test causing the Risk or Inspect Needed state.</i>
</p>

<p align="center">
<img src="/samplesafe-dashboard.jpg" width="800"><br/>
<i>Serial event timeline or BLE dashboard showing transport events.</i>
</p>

### Videos

The final local MP4 demo should show Safe baseline, lid-open Watch, warm exposure or drift, shake/tilt Risk, the Inspect Needed latch, and the event timeline.

<video controls width="100%">
<source src="/samplesafe-demo.mp4" type="video/mp4">
</video>

---

## Features (Detailed)

### 1. Multi-sensor transport integrity detection

SampleSafe Transit combines three sensing modalities. The APDS9960 is used for lid-opening, light-ingress, and sample-presence cues. The MPU6050 is used for shock, tilt, inversion, and rough-handling cues. The SI7021 is used for internal temperature and humidity drift. This makes the system more informative than a temperature-only logger because it can explain the likely reason behind a transport issue.

### 2. Conservative state machine

The firmware follows a simple state machine: **Safe → Watch → Risk → Inspect Needed**. A short exposure or microclimate event moves the system into Watch. A stronger handling or sample-removal event moves it into Risk, and then into Inspect Needed so the event history is not hidden just because the lid is closed again.

### 3. Local and logged feedback

The OLED is intended to show the current state and the event reason, while the RGB LED and buzzer provide local alerts. Serial event logging is included as the current fallback evidence path. BLE dashboard output should only be claimed as implemented after hardware testing confirms it.

### 4. Honest prototype scope

The repository currently contains a firmware MVP and a deterministic submission validator. Real sensor thresholds, photos, and final local MP4 evidence must be added after hardware testing. Any feature that is not verified on hardware should remain described as a prototype limitation or fallback.

---

## Usage Instructions

1. Connect the APDS9960, MPU6050, SI7021, and OLED display over the MYOSA I2C stack or an equivalent ESP32 I2C setup.
2. Open `firmware/samplesafe_transit.ino` in the Arduino IDE or another compatible ESP32 build environment.
3. Keep `ENABLE_SENSOR_LIBS` set to `0` for a serial dry run, or set it to `1` after installing and confirming the required sensor libraries.
4. Upload the firmware and open the serial monitor at 115200 baud.
5. During startup calibration, keep the box closed and still.
6. For dry-run testing, send the following serial commands:

```plaintext
l = toggle lid/light exposure
s = trigger shock/tilt event
w = toggle warm/humidity drift
c = close lid while keeping the inspection latch
r = manual reset after inspection
```

7. For final hardware testing, capture photos and video only after confirming the real sensor behavior in `.orchestrator/source_facts.md`.

---

## Tech Stack

* **MYOSA / ESP32-class controller** for sensor reading, state evaluation, and serial logging.
* **APDS9960** for proximity, ambient light, color, and optional gesture input.
* **MPU6050** for accelerometer/gyroscope-based handling detection.
* **SI7021** for temperature and humidity tracking.
* **OLED display, RGB LED, and buzzer** for local feedback.
* **Arduino-style C/C++ firmware** in `firmware/samplesafe_transit.ino`.
* **Python 3** validator in `scripts/check_submission.py`.

---

## Requirements / Installation

Install an ESP32-compatible Arduino environment. For dry-run validation, no sensor libraries are required because `ENABLE_SENSOR_LIBS` defaults to `0`.

For hardware mode, install or confirm equivalent sensor/display libraries:

```bash
# Install through Arduino Library Manager where possible:
# - Adafruit APDS9960
# - Adafruit MPU6050
# - Adafruit Si7021
# - Adafruit GFX
# - Adafruit SSD1306
```

Validate the submission package before uploading:

```bash
python scripts/check_submission.py samplesafe-transit.md
```

---

## File Structure (Optional)

```plaintext
samplesafe-transit/
├─ samplesafe-transit.md
├─ samplesafe-cover.jpg
├─ samplesafe-prototype.jpg
├─ samplesafe-internal-sensors.jpg
├─ samplesafe-lid-open-watch.jpg
├─ samplesafe-rough-handling-risk.jpg
├─ samplesafe-dashboard.jpg
├─ samplesafe-demo.mp4
├─ firmware/
│  └─ samplesafe_transit.ino
├─ scripts/
│  └─ check_submission.py
└─ .orchestrator/
   ├─ current_task.md
   ├─ source_facts.md
   ├─ task_board.md
   ├─ pipeline.md
   └─ final_gate.md
```

---

## License (Optional)

License to be added by the team before final publication.

---

## Contribution Notes (Optional)

This repository is currently a deadline-focused MYOSA 5.0 submission package. Future contributors can improve calibrated thresholds, BLE dashboard output, enclosure design, and long-duration transport testing.
