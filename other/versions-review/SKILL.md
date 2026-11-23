---
name: versions-review
description: "Versions and review rounds for Claude: runs client notes rounds like a post house: numbered versions (v001, v002...) that are never overwritten, A/B contact sheets comparing two versions frame by frame, notes grouped by type and traced to the note behind the note, a plan diff of what changed, a CHANGELOG, and QC re-run after every round. Use when the user says 'here are the client notes', 'make v2', 'revision round', 'compare the two versions', 'what changed since last time', 'go back to the version they approved', 'A/B these', 'keep track of versions'. Runs on video-studio-core (plan.json, render --frames, editor review, finish, qc)."
license: MIT
---

# Versions and Review

Every round gets a number, a diff, a side-by-side and a clean QC, and the approved cut is never touched.

- **Best for:** any edit with feedback rounds: client work, brand, weddings, courses, team reviews
- **Inputs:** a Video Studio work folder `W` with `plan.json`, and the notes (text, timestamps, voice memo transcript)
- **Outputs:** `W/plan_v00N.json`, `W/final_v00N.mp4`, `W/contact_v00N.png`, `W/ab_v00N_v00M.png`,
  `W/review_v00N.md`, `W/CHANGELOG.md`

## Before you start

- This skill needs **video-studio-core** in the same skills folder. `CORE` = that folder.
- First run on a machine: `python CORE/scripts/check_env.py`.
- Agree the number of rounds up front (two is common for weddings and social) and who gives the final approval.
- Keep every version's plan **in the same work folder** as the original: plan paths (`source`, `matte`, clips, music)
  are relative to the plan file, so a copy in another folder breaks them.
- `render.py --frames` always writes `W/contact_sheet.png` and `render.py` writes `W/composite.mp4`: both are
  overwritten each time, so copy or name them per version as shown below.

## Version naming

| file | rule |
| --- | --- |
| `plan_v001.json` | first cut sent to the client. Copy of `plan.json` at that moment |
| `"outputFile": "final_v001.mp4"` | set inside each version's plan so `finish.py` never overwrites another version |
| `contact_v001.png` | the contact sheet for that version (same frame times every round) |
| `client_project_v001_16x9.mp4` | the name the client sees (copy of `final_v001.mp4`) |
| `APPROVED` | when a version is approved, write it in `CHANGELOG.md`; never edit that plan again (new work = new number) |

## Run a round

```bash
# 0. first time: freeze v001
python CORE/scripts/render.py W/plan_v001.json --frames 2,8,15,30,45
python CORE/scripts/render.py W/plan_v001.json --out W/composite_v001.mp4
python CORE/scripts/finish.py W/plan_v001.json --in W/composite_v001.mp4
python CORE/scripts/editor.py review W/plan_v001.json --out W/review_v001.md
```

Copy `W/contact_sheet.png` to `W/contact_v001.png` straight after the `--frames` render.

For the next round: copy `plan_v001.json` to `plan_v002.json`, set `"outputFile": "final_v002.mp4"`, apply the notes
to `plan_v002.json` only, then the same four commands with `v002` (and copy the sheet to `contact_v002.png`).
If a note changes the cut itself (timing, order, a removed sentence), redo that step first: `autocut.py --work W --cut "..."`
or a new timeline spec writes a new `cut.mp4`, which changes **every** plan in the folder. In that case work in a new
folder `W_v002/` (re-run `run.py` there) and say so in the changelog.

## Read the notes like an editor

1. Read all notes before touching anything. Group them: **story, timing, graphics/text, sound, colour, spelling/facts**.
2. Find the note behind the note: "slow at 0:40" often means the promise at 0:05 is unclear; "music too loud" may
   mean one line is unintelligible. Fix the cause.
3. Do what was asked. If you disagree, also make your alternative as a separate version (`v002b`) and show both.
4. Map each note to the plan field it touches: text/spelling in `elements[].text`/`title`/`name` and `words[].w`;
   timing in `start`/`end`; zooms in `speaker.zooms`; music in `music` (`under`, `duck`, `fitTo`); colour in
   `color.look`/`intensity`; loudness in `audio`. Picture order or length changes go back to the timeline / autocut.
5. Answer every note in the changelog: done / done differently (why) / not done (why).

## Compare versions

A/B contact sheet (same frame times, v001 on top, v002 below), Pillow only:

```bash
python -c "from PIL import Image; a,b=Image.open('W/contact_v001.png'),Image.open('W/contact_v002.png'); o=Image.new('RGB',(max(a.width,b.width),a.height+b.height),'white'); o.paste(a,(0,0)); o.paste(b,(0,a.height)); o.save('W/ab_v001_v002.png')"
```

Open `ab_v001_v002.png` with the Read tool and look at it before sending. Single-frame A/B of a colour note:
`python CORE/scripts/color.py preview W/source.mp4 --look portra --intensity 0.6 --correct --t 12 --out W/look_a.png`
and again with the other look to `look_b.png`.

What changed in the plan (paste into the changelog):

```bash
python -c "import difflib,sys; a=open('W/plan_v001.json',encoding='utf-8').read().splitlines(); b=open('W/plan_v002.json',encoding='utf-8').read().splitlines(); sys.stdout.writelines(l+'\n' for l in difflib.unified_diff(a,b,'v001','v002',lineterm='',n=1))"
```

Skip the `words` array noise by reading only the hunks under `elements`, `music`, `color`, `speaker`.

## CHANGELOG.md (in the work folder)

```text
## v002  2026-11-18  (round 1 of 2)
Notes from: Priya (email 17 Nov)
- [story]    "hook is weak"            -> new hook text 0:00-0:02, kept the first line   DONE
- [spelling] "Rao not Rau"             -> lowerthird + words fixed                        DONE
- [sound]    "music too loud at 0:40"  -> music under 18 -> 22, speech-aware duck         DONE
- [colour]   "warmer"                  -> portra 0.6 (v002b keeps cool-corporate)         DONE, alt in v002b
- [timing]   "cut the second example"  -> needs re-cut: done in W_v002/                   DONE
QC: qc.py pass, review 92/100, loudness -14.1 LUFS / -1.2 dBTP
Files: client_project_v002_16x9.mp4, ab_v001_v002.png
```

## Check before delivering

- After every round, re-run QC on the new file: `python CORE/scripts/qc.py W/final_v002.mp4 --plan W/plan_v002.json --platform youtube --strict`
  (notes fixes break things: orphan captions, text pushed out of the safe zone, a zoom left on a deleted word).
- Re-read `review_v002.md` for new high-severity items.
- The A/B sheet shows only the intended changes; spelling of every name checked again.
- The approved version's plan, final file and contact sheet are untouched (compare file dates).
- Send the client: the new file, the A/B sheet, and the changelog entry. State how many rounds remain.

## Example requests

- "Here are the client's notes on v1, make v2 and tell me what you changed."
- "Show me v2 and v3 side by side."
- "They approved v2 but now want a shorter version: don't touch v2."
