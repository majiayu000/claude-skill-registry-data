---
name: funnel-screenshots
description: >-
  Walk a public quiz / onboarding funnel end to end in a real Chromium with iPhone emulation and capture every unique screen as a retina screenshot (1179×2556), then document the paywall, discount modals and the empty payment form — never typing payment data. Output is numbered PNGs, a step log and an INDEX.md. Use for competitor funnel teardowns, onboarding benchmarks, paywall research, or "screenshot every step of this quiz". Triggers: "screenshot this funnel", "walk this quiz", "capture the onboarding", "teardown their paywall".
---

# Funnel screenshots

Drives a marketing funnel in a real Chromium with iPhone emulation, screenshots every unique screen at 1179×2556 (DPR 3), documents the paywall and stops at the payment form. Proven on long health, diet and lifestyle app quizzes — 30 to 120 screens per funnel.

## Setup (one time)

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/setup.sh
```

Creates a venv in `~/.cache/marketing-agent-kit/funnelshot-venv` (override with `FUNNELSHOT_VENV`), installs Playwright, downloads Chromium if missing (~150 MB), and smoke-tests that screenshots really come out at DPR 3. Re-run it any time; it is idempotent and says exactly what to install if something is missing. Everything below assumes:

```bash
PY=~/.cache/marketing-agent-kit/funnelshot-venv/bin/python
SK=${CLAUDE_SKILL_DIR}/scripts
```

## Capture a funnel

```bash
$PY $SK/funnelshot.py --url https://example.com/quiz --out ~/funnels/example-quiz
```

Then the paywall (numbering continues from where the walk stopped — if it saved 53 screens, use `--prefix 54`):

```bash
$PY $SK/paywall.py --out ~/funnels/example-quiz --prefix 54
```

Then the index:

```bash
$PY $SK/makeindex.py --out ~/funnels/example-quiz --title "Example — quiz v1" \
    --notes "Female · 170 cm / 75 kg · goal 65 kg"
```

Result: `shots/*.png`, `INDEX.md`, `log.json` (every step with URL, headings, options), `state.json` + `last_url.txt` (for resuming).

`state.json` holds the funnel's cookies and localStorage, and `log.json` / `last_url.txt` can carry the email you typed. The scripts write a `.gitignore` into the output folder that keeps these three out of git. Share `shots/` and `INDEX.md`, not the folder as a whole.

### Useful flags

| Flag | Why |
|---|---|
| `--email you@example.com` | the funnel has an email gate; without it the walk stops there |
| `--units imperial` | US / UK funnels: 5 ft 7 in / 165 lb / goal 145 lb |
| `--height 170 --weight 75 --goal 65 --age 35 --name Alex` | override the answers |
| `--resume --start 68` | continue after a crash or the step cap |
| `--max-steps 260` | the default; very long funnels need it |
| `--device desktop` | 1440×900 @ DPR 2 instead of iPhone |
| `--locale en-GB` | region-specific prices and units |
| `--headed` | watch it run (uses real Chrome) |

Long funnels hit the step cap midway. The walk saves its state, so continue with the number it printed ("resume with: --resume --start 68"); numbering stays continuous and `log.json` is appended to.

## Workflow

1. **Run `funnelshot.py`.** Watch the printed steps — each line shows URL, headings and the options it saw. That log is how you spot a mishandled screen.
2. **Read the last lines.** Why did it stop? The payment form (good), an email gate (re-run with `--email`), the step cap (`--resume`), or "nothing left to click" (usually an unrecognised CTA — see troubleshooting).
3. **Run `paywall.py`.** It tiles the paywall, catches discount and gift modals, screenshots each plan selected, then opens the payment step and the empty card form.
4. **QA before reporting — not optional:**
   - every ordinary screenshot is 1179×2556; anything taller is a deliberate full-page shot (`makeindex.py` lists those separately);
   - actually *look* at three files: the first screen, one with a long option list, the last one. Nothing cut off, text crisp;
   - if options are cut off, the screen scrolls inside a container — check that a `-scrolled.png` companion exists.
5. **Run `makeindex.py`**, then report: number of unique screens, folder, the funnel structure step by step, paywall prices / trial / auto-renew / guarantee terms, and exactly where and why the capture stopped.

Report what actually happened. If a funnel has no discount modal, say so; if the card form was unreachable, say why.

## Guardrails

Allowed, because the screenshots need it:
- ticking **consent** checkboxes (health data / privacy / terms) that gate the next step;
- typing an email the user gave you into an email gate;
- claiming discounts, selecting plans, opening the payment modal, expanding the card form.

Never:
- typing card numbers, CVV, expiry or any payment data;
- clicking Pay / Continue Securely / Google Pay / Apple Pay / PayPal / Place order;
- creating an account with a password (stop and report).

The scripts enforce this: pay-button text is in the skip list, and `funnelshot.py` stops as soon as a real card field, payment iframe or password field appears. Do not remove those guards to "get further".

**Ask the user before entering their email** — it is their address and their inbox; marketing emails will follow. One approval covers the funnel you're working on, not the next one. A dedicated inbox for research is a good idea.

Capture only what any visitor sees, at a human pace, one run per funnel. Check the site's terms if you plan to publish the screenshots.

## Several funnels at once

One subagent per funnel, each with its own `--out` folder. Give each agent: the URL, the folder, the setup command, the three commands above, the guardrails and the QA checklist. They must not share a folder.

## When something misbehaves

- `references/troubleshooting.md` — every trap hit so far: blurry screenshots, bot traps that redirect to a tarpit, clicks that time out on overlays, disabled Continue buttons, imperial units, unrecognised CTAs, gift modals, loaders, inner-scroll lists.
- `references/funnel-patterns.md` — how long app funnels are usually built and where they block automation. A sanity check for what a "normal" result looks like.

## Adapt it

- New CTA wording in your market ("Let's go", "Weiter")? Add it to `CONT` in `funnelshot.py`.
- Different answers matter for your category (B2B role, company size)? Add presets next to the height / weight rules in `funnelshot.py`.
