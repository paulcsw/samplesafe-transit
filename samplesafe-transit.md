---
title: "SampleSafe Transit"
publishDate: "2026-05-13"
excerpt: "A MYOSA-based biosample transport integrity monitor that detects lid exposure, rough handling, and microclimate drift during transit."
image: "./samplesafe-cover.jpg"
tags:
  - myosa
  - biosample-transport
  - integrity-monitoring
  - esp32
---

# SampleSafe Transit

## Overview

SampleSafe Transit is a MYOSA-based biosample transport integrity monitoring prototype. It turns biosample transport from a single temperature number into a root-cause timeline: exposure, warming, and rough handling.

This prototype is not a diagnostic device. It is an early-warning and handling-evidence tool for biosample transport workflows.

Affordable transport monitors often record only temperature. That leaves a gap when a sample arrives in questionable condition, because the receiver may not know whether the issue came from lid opening, light ingress, shock, tilt, inversion, or gradual microclimate drift.

SampleSafe Transit focuses on a simple judge-readable state machine: Safe -> Watch -> Risk -> Inspect Needed.

## Images

![SampleSafe Transit cover](./samplesafe-cover.jpg)

![Prototype enclosure and visible hardware](./samplesafe-prototype.jpg)

![Internal sensor layout](./samplesafe-internal-sensors.jpg)

The prototype target uses:

- APDS9960 for lid-open, light ingress, and sample presence/removal cues.
- MPU6050 for shock peaks, tilt hold, inversion, and rough-handling score.
- SI7021 for temperature, humidity, and microclimate drift.
- OLED display for Safe, Watch, Risk, and Inspect Needed states.
- RGB LED and buzzer for local alerts.
- ESP32 serial logging, with BLE event timeline planned or enabled when hardware testing confirms it.

## Videos

<video controls src="./samplesafe-demo.mp4"></video>

The demo evidence should show:

1. Safe baseline.
2. Lid open or light ingress causing Watch.
3. Warm exposure or temperature/humidity drift.
4. Shake or tilt causing Risk.
5. Lid closed while Inspect Needed remains latched.
6. Event timeline through serial output or BLE dashboard.

![Lid open Watch state](./samplesafe-lid-open-watch.jpg)

![Rough handling Risk state](./samplesafe-rough-handling-risk.jpg)

![Event timeline or dashboard](./samplesafe-dashboard.jpg)

## Features

At startup, the firmware performs a baseline calibration period. The main loop then reads sensor inputs, smooths noisy values, evaluates event detectors, updates the transport state machine, and writes state changes to local output.

The state machine is intentionally conservative:

- Safe means no current event has crossed a threshold.
- Watch means an exposure, drift, or handling event should be observed.
- Risk means stronger evidence of transport integrity loss has been detected.
- Inspect Needed is latched so that closing the lid after an event does not automatically hide the history.

Implemented in this repository:

- Firmware state machine and serial event logging.
- Dry-run serial commands for bench testing without sensor libraries.
- Deterministic validation script for submission-format risks.

Pending human verification:

- Real sensor calibration values.
- Final photos and local MP4 demo.
- Confirmation of OLED, RGB LED, buzzer, and BLE behavior on the actual hardware.

## Usage

1. Power the ESP32-class board and keep the prototype closed and still during startup calibration.
2. Watch the OLED state: Safe, Watch, Risk, or Inspect Needed.
3. Open the lid or introduce light ingress to verify the Watch state.
4. Shake or tilt the box to verify the Risk or Inspect Needed state.
5. Close the lid and confirm that Inspect Needed remains latched after a serious event.
6. Use the serial monitor or confirmed BLE dashboard to review the event timeline.

## Tech Stack

- MYOSA-compatible hardware prototype.
- ESP32-class microcontroller.
- APDS9960 proximity/light/gesture sensor.
- MPU6050 accelerometer/gyroscope.
- SI7021 temperature/humidity sensor.
- OLED display, RGB LED, and buzzer.
- Arduino-style firmware in `firmware/samplesafe_transit.ino`.
- Python validation script in `scripts/check_submission.py`.

## Installation

1. Connect the APDS9960, MPU6050, SI7021, and OLED display over I2C.
2. Open `firmware/samplesafe_transit.ino` in the Arduino IDE or a compatible ESP32 build environment.
3. Leave `ENABLE_SENSOR_LIBS` set to `0` for a serial dry run, or set it to `1` after installing the required Adafruit sensor libraries.
4. Upload the firmware to the ESP32-class board.
5. Open the serial monitor at 115200 baud.
6. For dry-run testing, send `l`, `s`, `w`, `c`, or `r` in the serial monitor to emulate lid, shock, warm drift, close-lid, or reset actions.
7. For hardware testing, update thresholds only after observing real baseline readings.

## Prototype Limitations

This prototype should not be used to diagnose sample quality, determine clinical validity, or replace formal cold-chain instrumentation. It records transport integrity signals that can help a handler decide whether a sample should be inspected.

BLE timeline output is treated as optional until confirmed on hardware. If BLE is not ready before submission, the serial event timeline is the honest fallback evidence.

## Repository Contents

- `samplesafe-transit.md`: MYOSA submission blog.
- `firmware/samplesafe_transit.ino`: firmware MVP.
- `scripts/check_submission.py`: deterministic submission validator.
- `.orchestrator/`: human-operated 2-pass orchestration files and prompts.

## Submission Checklist

- [ ] `samplesafe-cover.jpg` exists at repo root.
- [ ] `samplesafe-demo.mp4` exists at repo root and plays locally.
- [ ] Real prototype and sensor photos are added.
- [ ] No YouTube links are used.
- [ ] Overview, Images, Videos, Features, Usage, Tech Stack, and Installation sections are present.
- [ ] Claims match what was actually tested.
- [ ] `python scripts/check_submission.py samplesafe-transit.md` passes.
