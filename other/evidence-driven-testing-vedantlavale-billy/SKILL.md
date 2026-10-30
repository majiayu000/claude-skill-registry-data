---
name: evidence-driven-testing
description: Prove a change works by driving the running app and capturing what happened, before the fix and after. Screenshots and probes by default, a screen recording when a flow only makes sense over time. Use whenever a change needs evidence instead of a claim that it works.
allowed-tools:
  - Bash(npx playwright *)
  - Bash(npx @vercel/before-and-after *)
  - Bash(curl *)
  - Bash(lsof -i:*)
  - Bash(npm run *)
  - Bash(python3 *)
  - Bash(gh pr:*)
  - Read
  - Write
  - Grep
  - Glob
  - TodoWrite
---

# Prove it

An agent saying the fix works is not evidence. Capture what the app actually did.

Adapted from michaelshimeles/skills. The upstream skill leads with a screen
recorder; this version leads with the headless path, because the recorder needs
ffmpeg built with `libx264` and the `ass` filter plus macOS Screen Recording
permission granted to the terminal, and that is usually not set up here. Check
before promising a video.

## A bug? Diagnose it first

If the task is a bug, run `/diagnosing-bugs` before anything here. It will not
let you fix what you have not reproduced, and its outputs slot straight in:

- its **red-capable command** and output are your before evidence
- its **regression test** going green is part of your after evidence
- the **hypothesis that proved correct** goes in the PR's `What changed`

Then use this skill for the visible proof, the screenshots or numbers a
reviewer can see without running anything.

## Capture the before state first

The before state is cheapest while the bug is still there. Capture it **before**
you fix anything:

- the broken page, the error, the empty state, the slow number
- the exact steps that produce it

Once you fix it, the before state is gone and you are reconstructing it from
memory. Do not skip this.

## Pick the path

### Default: drive it headless

Works everywhere, no permissions needed.

```bash
lsof -i :<port>   # confirm your dev server, not another session's
npx playwright screenshot --viewport-size=1280,800 \
  "http://localhost:<port>/<route>" before.png
```

For a flow, write a short Playwright script that logs in as the seeded test
user, walks the steps, and screenshots each one. Keep it in `$TMPDIR`, it is a
probe, not a test to commit.

For backend behavior, a curl pair is evidence:

```bash
curl -s -i -b cookies.txt http://localhost:<api-port>/<endpoint> | head -20
```

### When a flow only makes sense over time

Streaming chat, transcription, a progress state. Try a recording:

```bash
python3 <path-to>/evidence.py doctor
```

Read `capture_ready` in the output, not just the exit code. It exits zero when
the toolchain is present even if no capture source works. On macOS it also needs
Screen Recording permission granted to the terminal, which a human has to click.

If it is not ready, do not stall. Take a sequence of stills at the interesting
moments and say in the PR that a recording was not available.

### When there is no surface at all

Measure. Same conditions before and after, and state the conditions.

```markdown
| Metric | Before | After |
|---|---:|---:|
| `/api/items` p95 | 815 ms | 61 ms |
| DB queries per request | 43 | 2 |

Seeded test account, 20 records, 10 runs, same machine.
```

Query counts, token counts, row counts, test output. A number with no conditions
attached is not proof.

## Data rule

Matters more here than for a screenshot, because a recording catches everything
on screen.

Billy has no login and no database. The only data it shows is the invoice draft
in the browser's `localStorage` (`billy_invoice_data`). Drive the app with a
made-up invoice (fake names, addresses, GSTIN, bank details) or a profession
preset, and never with a profile that holds a real invoice. Clear
`billy_invoice_data` or use a fresh profile when unsure.

For anything touching layout, templates or export, the evidence is the exported
PDF next to the on-screen canvas, not the canvas alone. For a change to the
invoice data shape, also load the editor with a draft saved by the *old* code
present, since that is what returning users have.

## Read your own evidence before you post it

Look at the after capture. If it does not show the thing working, the change is
not finished. Go back and build, then capture again.

This is the loop that makes the whole thing work. The after shot failing is not a
failure of the evidence step, it is the evidence step doing its job.

## Deliver

Put the pair in the PR body under `## Before and after`, via `/before-and-after`.
Drag images into the PR on github.com rather than uploading to a public paste
host.
