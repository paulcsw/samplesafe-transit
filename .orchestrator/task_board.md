# Task Board

## P0 - Submission Compliance

Owner: GPT Pro + Codex

Outputs:

- `samplesafe-transit.md` with required headings
- `scripts/check_submission.py` validator

Done when:

- validator passes
- no YouTube links
- local mp4 referenced
- required headings present

## P0 - Firmware Demo MVP

Owner: Codex, then Claude Code

Outputs:

- `firmware/samplesafe_transit.ino`

Done when:

- compiles or has clear hardware-specific TODOs
- reads or stubs APDS9960, MPU6050, SI7021 safely
- displays Safe / Watch / Risk / Inspect Needed
- serial event log exists even if BLE is incomplete

## P0 - Real Media Capture

Owner: Human

Outputs:

- `samplesafe-cover.jpg`
- `samplesafe-prototype.jpg`
- `samplesafe-internal-sensors.jpg`
- `samplesafe-lid-open-watch.jpg`
- `samplesafe-rough-handling-risk.jpg`
- `samplesafe-dashboard.jpg`
- `samplesafe-demo.mp4`

Done when:

- all files exist at repo root
- filenames lowercase, no spaces
- demo mp4 plays locally

## P1 - Blog Polish

Owner: GPT Pro

Outputs:

- final English blog

Done when:

- overview, demo, features, usage, tech stack, installation all filled
- no false implementation claims
- limitations included

## P1 - Independent Red-Team

Owner: Claude Opus 4.7

Outputs:

- `.orchestrator/opus_review.md`

Done when:

- blockers listed
- must-fix items under 10
- human resolves or explicitly accepts risks
