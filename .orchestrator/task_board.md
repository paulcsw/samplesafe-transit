# Task Board

## P0 - Repo And Control Plane

Owner: Codex + Human

Outputs:

- `.orchestrator/`
- `samplesafe-transit.md`
- `firmware/samplesafe_transit.ino`
- `scripts/check_submission.py`

Done when:

- repo is public on GitHub
- initial commit is pushed

## P1 - Source Facts

Owner: GPT Pro + Human

Outputs:

- `.orchestrator/source_facts.md`

Done when:

- tested / not tested / fallback status is explicit
- claim policy is up to date

## P2 - Blog Skeleton

Owner: GPT Pro

Outputs:

- `samplesafe-transit.md`

Done when:

- one-line tagline and official MYOSA sections exist
- Demo / Examples contains Images and Videos subheadings
- Features (Detailed), Usage Instructions, Tech Stack, and Requirements / Installation are filled
- local media references are used
- no completed feature is invented

## P3 - Firmware MVP

Owner: Codex

Outputs:

- `firmware/samplesafe_transit.ino`

Done when:

- SAFE / WATCH / RISK / INSPECT_NEEDED state machine exists
- APDS9960 / MPU6050 / SI7021 sections exist
- serial event log fallback exists

## P4 - Hardware Test Loop

Owner: Human + GPT Pro

Outputs:

- updated `.orchestrator/source_facts.md`
- test notes in `.orchestrator/handoff.md`

Done when:

- boot, APDS9960, MPU6050, SI7021, OLED, latch, and serial/BLE timeline are recorded as PASS, FAIL, or NOT READY

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

Done when:

- all files exist at repo root
- filenames lowercase, no spaces
- demo mp4 plays locally

## P6 - Blog Completion

Owner: GPT Pro

Outputs:

- final English blog

Done when:

- claims match `source_facts.md`
- limitations included
- non-diagnostic wording included

## P7 - Compliance Gate

Owner: Codex + GPT Pro

Outputs:

- validator result
- final checklist update

Done when:

- validator passes
- no YouTube links
- cover image and local mp4 are present
- no rejection blocker remains

## P8 - Optional Red-Team

Owner: Claude Opus or fresh GPT Pro thread

Outputs:

- `.orchestrator/redteam_review.md`

Done when:

- blockers are listed
- final verdict is submit or do not submit yet

## P9 - Submission

Owner: Human

Outputs:

- GitHub repo link
- MYOSA form submission

Done when:

- GitHub rendering is checked
- final validator passes
