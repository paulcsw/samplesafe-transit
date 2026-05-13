# GPT-First Mini Orchestration Pipeline

## Principle

The human is the PM. GPT Pro and Codex produce bounded artifacts. Claude is optional and only used for a final independent red-team review.

## P0 - Repo And Control Plane

Owner: Codex + Human

Outputs:

- `.orchestrator/`
- `samplesafe-transit.md`
- `scripts/check_submission.py`
- `firmware/samplesafe_transit.ino`

Pass condition:

- file structure exists
- initial commit is pushed

## P1 - Source Facts

Owner: GPT Pro + Human

Outputs:

- `.orchestrator/source_facts.md`

Pass condition:

- implemented, not implemented, and fallback claims are separated
- human hardware truth is recorded after tests

## P2 - Blog Skeleton

Owner: GPT Pro

Outputs:

- `samplesafe-transit.md`

Pass condition:

- official sections exist: Overview, Images, Videos, Features, Usage, Tech Stack, Installation
- only local image and video references are used

## P3 - Firmware MVP

Owner: Codex

Outputs:

- `firmware/samplesafe_transit.ino`

Pass condition:

- SAFE, WATCH, RISK, INSPECT_NEEDED state machine exists
- APDS9960, MPU6050, SI7021 read sections exist
- serial event timeline fallback exists

## P4 - Hardware Test Loop

Owner: Human + GPT Pro

Outputs:

- updated `.orchestrator/source_facts.md`
- updated `.orchestrator/handoff.md`

Pass condition:

- boot, sensors, display, latch, and serial/BLE timeline are marked PASS, FAIL, or NOT READY

## P5 - Media Capture

Owner: Human + GPT Pro

Outputs:

- `samplesafe-cover.jpg`
- `samplesafe-prototype.jpg`
- `samplesafe-internal-sensors.jpg`
- `samplesafe-lid-open-watch.jpg`
- `samplesafe-rough-handling-risk.jpg`
- `samplesafe-dashboard.jpg`
- `samplesafe-demo.mp4`

Pass condition:

- all media files exist at repo root
- filenames are lowercase and have no spaces

## P6 - Blog Completion

Owner: GPT Pro

Outputs:

- final English `samplesafe-transit.md`

Pass condition:

- claims match `source_facts.md`
- limitations and non-diagnostic wording are included

## P7 - Compliance Gate

Owner: Codex + GPT Pro

Outputs:

- validator output
- final checklist update

Pass condition:

- `python scripts/check_submission.py samplesafe-transit.md` passes
- no rejection blockers remain

## P8 - Optional Red-Team

Owner: Claude Opus or fresh GPT Pro thread

Outputs:

- `.orchestrator/redteam_review.md`

Pass condition:

- final verdict is submit or do not submit yet
- any accepted risk is explicitly noted by the human

## P9 - Submission

Owner: Human

Outputs:

- public GitHub repository link
- form submission

Pass condition:

- GitHub rendering is checked
- final validator passes
