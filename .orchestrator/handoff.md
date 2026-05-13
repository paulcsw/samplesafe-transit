# Handoff

## 2026-05-13 - Codex Scaffold Pass

Files created:

- `samplesafe-transit.md`
- `firmware/samplesafe_transit.ino`
- `scripts/check_submission.py`
- `.orchestrator/current_task.md`
- `.orchestrator/source_facts.md`
- `.orchestrator/task_board.md`
- `.orchestrator/final_gate.md`
- `.orchestrator/prompts/*.md`

Commands run:

- `git init`

Known assumptions:

- Real images and demo video are intentionally not fabricated.
- The validator is expected to fail until the human adds the real media files at repo root.
- Firmware defaults to serial dry-run mode with `ENABLE_SENSOR_LIBS` set to `0`.
- Set `ENABLE_SENSOR_LIBS` to `1` after installing and verifying the hardware libraries.

Next handoff for Codex:

- Run `python scripts/check_submission.py samplesafe-transit.md`.
- Keep expected missing-media failures until real assets are captured.
- Check Arduino syntax if the build environment is available.
- Patch only path, syntax, and small robustness issues.

## 2026-05-13 - GPT-First Pipeline Update

Changes:

- Reframed the control plane around Human PM, GPT Pro, Codex, and optional final red-team review.
- Added `.orchestrator/pipeline.md`.
- Updated submission sections to the simplified GPT-first structure.
- Removed Claude Code as a normal patching lane.

Expected validator status:

- The markdown structure should pass.
- The validator should still fail until real local media files are added at repo root.

## 2026-05-13 - Official Format Patch

Changes:

- Applied the patch-only zip for `samplesafe-transit.md`, `scripts/check_submission.py`, and `firmware/samplesafe_transit.ino`.
- Aligned the control plane with the stricter official MYOSA structure:
  - one-line tagline
  - Acknowledgements
  - Overview
  - Demo / Examples with Images and Videos
  - Features (Detailed)
  - Usage Instructions
  - Tech Stack
  - Requirements / Installation
- Firmware now shows `RISK` briefly before latching into `INSPECT_NEEDED`.

Expected validator status:

- The official heading structure should pass.
- Validator should still fail until the required real JPG/PNG images and local MP4 are added.

## 2026-05-13 - Demo Firmware Risk Fixes

Changes:

- Increased `RISK_LATCH_MS` from 1500 ms to 5000 ms so the Risk state is easier to capture on video.
- Changed WATCH alert output from blue to amber-style red+green to match the green/amber/red demo narrative.
- Kept RISK and INSPECT_NEEDED red-centered with buzzer output.
- Guarded APDS9960 `sampleMissing` so a simple lid-open/light event stays Watch until closed-box sample-presence thresholds are calibrated.
- Replaced acceleration-magnitude tilt detection with a baseline-vector angle check for more reliable tilt behavior.
- Added shock, tilt, and sample_missing fields to serial sample output for easier demo evidence.

Expected validator status:

- Validator should still fail only because real media files are missing.
