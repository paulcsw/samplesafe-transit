# Source Facts - Do Not Invent Beyond This

## Project

SampleSafe Transit is a MYOSA-based biosample transport integrity monitor.

## Problem

Affordable transport monitors often record only temperature, without explaining whether an issue came from lid opening, exposure, shock, tilt, or microclimate drift.

## Sensors

- APDS9960: lid-open, light ingress, sample presence/removal, optional gesture acknowledge
- MPU6050: shock peak, tilt hold, inversion, rough-handling score
- SI7021: temperature, humidity, microclimate drift, warm-exposure timer
- OLED: Safe / Watch / Risk / Inspect Needed status and event reason
- RGB LED + buzzer: local visual/audio alert
- ESP32 BLE: event timeline, if implemented

## Firmware Concept

Startup calibration -> sensor read loop -> smoothing -> event detectors -> state machine -> OLED/LED/buzzer/log output.

## State Machine

Safe -> Watch -> Risk -> Inspect Needed.

Inspect Needed should not automatically clear just because the lid is closed.

## Safety Wording

This is not a diagnostic device. It is a biosample transport integrity monitoring and early-warning assistance prototype.

## Claim Policy

Use "implemented" only for features actually tested.

Use "prototype limitation" for features not fully working.

Use "fallback" when the serial log replaces an unfinished BLE dashboard.

## Hardware Truth Log

Update this section by hand after each real hardware test.

## Hardware Truth Checklist

- [ ] APDS9960 tested
- [ ] MPU6050 tested
- [ ] SI7021 tested
- [ ] OLED state display tested
- [ ] RGB LED/buzzer tested
- [ ] BLE dashboard tested
- [ ] serial log fallback tested

| Date | Item | Status | Evidence |
| ---- | ---- | ------ | -------- |
| 2026-05-13 | Repo scaffold | Created | Initial commit |
| 2026-05-13 | Real photos/video | Not yet captured | Pending human capture |
| 2026-05-13 | Sensor thresholds | Not yet calibrated | Pending hardware test |
