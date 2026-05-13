# Current Task - SampleSafe Transit MYOSA 5.0

## Deadline

Submit final GitHub repository link before 17 May 2026 23:59:59 AoE.

## Objective

Run a GPT-first mini orchestration for a MYOSA-compliant SampleSafe Transit submission package:

- single markdown file
- official Markdown sections
- real images
- local mp4 demo video
- working prototype evidence
- firmware/code where possible

## Non-Negotiable Submission Rules

- Markdown file: `samplesafe-transit.md`
- Required structure:
  - one-line project tagline after frontmatter
  - `## Acknowledgements`
  - `## Overview`
  - `## Demo / Examples`
  - `### Images`
  - `### Videos`
  - `## Features (Detailed)`
  - `## Usage Instructions`
  - `## Tech Stack`
  - `## Requirements / Installation`
- All submission media filenames lowercase, no spaces
- Cover image required: `samplesafe-cover.jpg`
- Local video required: `samplesafe-demo.mp4`
- No YouTube links
- Do not claim unimplemented features
- Do not publish phone numbers or private contact details

## MVP Demo Target

Show:

1. Safe baseline
2. Lid open / light ingress -> Watch
3. Warm exposure or temp/humidity drift
4. Shake/tilt -> Risk
5. Close lid -> Inspect Needed remains latched
6. Event timeline or serial/BLE log

## Owners

- Human PM: hardware truth, photos, videos, final submit
- GPT Pro: blog producer, claim checker, demo script writer, compliance reviewer
- Codex: firmware MVP, validator script, small repo patches
- Claude or fresh GPT Pro thread: optional final red-team review only

## Operating Rules

- One model writes files at a time.
- `source_facts.md` is updated by the human after real hardware tests.
- Codex owns code and validator work.
- GPT Pro owns final prose and claim policy.
- Run the validator every day and before submission.
