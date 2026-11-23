---
name: course-module
description: "Online course lesson editor for Claude: turns a teacher's recording (talking head, slides or screen) into a clean 3-10 min lesson with one learning objective, numbered steps, callouts, quiz cards, a recap, accessible captions (WCAG) and a transcript, consistent across every module. Use when the user says 'edit my course video', 'make a lesson', 'e-learning module', 'Udemy / Teachable lecture', 'training video for staff', 'add quiz cards and captions', or hands over lecture recordings. Runs on video-studio-core (transcribe, retakes, autocut, chapters, captions, deliver, QC)."
license: MIT
---

# Course Module

One lesson, one objective, nothing the learner has to rewind to understand.

- **Best for:** online courses, corporate training, onboarding lessons, university lectures, coaching programmes
- **Inputs:** lesson recording (face, slides, screen or all three), slide deck export or screen capture, course name
- **Default skin:** `whiteboard-host` · alternatives `tutorial-steps`, `highlighter-study`, `chapter-pro`
- **Formats:** 16:9 lesson; optional 9:16 promo clip per module
- **Durations:** 3-10 min per lesson (split longer recordings)
- **Genre preset:** `--genre course-module`

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = that folder, `SKILLS` = the skills folder.
- First run: `python CORE/scripts/check_env.py`.
- Ask for: the learning objective of this lesson (one sentence), terms and names to spell (`--prompt`), the course
  template (intro card, colours) so every module looks the same, and whether an LMS needs SCORM.
- SCORM packaging is not done by the engine: deliver MP4 + VTT + transcript and let the LMS wrap them.
- Accessibility is part of the job: captions on every lesson, transcript text, nothing conveyed by colour alone.

## How a pro cuts this

**Structure (% of lesson)**

| beat | % | what goes here |
| --- | --- | --- |
| objective | 8 | "By the end of this lesson you can..." on screen and said |
| why it matters | 10 | the problem this solves for the learner |
| teach | 55 | concept in 2-4 numbered steps, one idea per step |
| example / practice | 17 | worked example, then a quiz card or exercise prompt |
| recap + next lesson | 10 | 3 bullet recap, what comes next |

**Pacing.** ASL 4-10 s; visual change every 8 s (callout, step card, slide change). Slower than YouTube: learners
need time to read. Hold slides with text >= 1.5 s per line of text.

**Cut rules.**
- Keep the last good take (`--retakes`); remove fillers and long pauses but keep the teacher's rhythm.
- Jump cuts are acceptable in lessons; hide the obvious ones with a slide or a punch-in.
- Cut repetition and tangents; move asides to a "notes" document, not the video.
- Split recordings at topic shifts into separate lessons (`story.py outline` shows topic shifts).

**Transition grammar.** Cuts; a dissolve only at a scene change (talking head to slides). Same intro and outro card on
every module.

**Music and sound.** No music under teaching (bed at -32 dB only on the intro/outro card). Clear voice:
`"eq": "clear"`, de-ess, -16 LUFS for LMS/web. No SFX except a soft tick on a quiz reveal.

**Colour.** No look (accurate). Fix white balance and exposure only (auto correction).

**Captions.** Accessible subtitles, sentence case, <= 15 cps, 2 lines max, high contrast (`"preset": "clean"`);
always also deliver `.vtt`/`.srt` sidecars and a transcript.

**What the client judges.** Clarity, consistency across modules, accessibility.

**Common mistakes.** No stated objective; 25-minute lessons; reading slides aloud; music under explanation;
captions too fast; every module with a different look; missing transcript.

## Make the edit

```bash
python CORE/scripts/run.py lesson03.mp4 --style SKILLS/whiteboard-host --genre course-module --format 16:9 --smart-cuts --retakes --prompt "Kubernetes, kubectl, YAML" --title "Lesson 3: Deployments" --work m03 --stop-after plan
python CORE/scripts/story.py outline --work m03 --genre course-module    # topic shifts -> split long recordings
python CORE/scripts/render.py m03/plan.json --frames 2,30,90,180,280
python CORE/scripts/render.py m03/plan.json
python CORE/scripts/finish.py m03/plan.json --platform podcast
```

`--platform podcast` gives -16 LUFS (LMS/web target). Slides or screen as a separate file: add `--clip slides.mp4`
and place it with `clip` elements or full-frame `cutaways`. Split a long recording into lessons with `--cut` ranges
or `story.py reorder --work m03 --order "s1-s24"` per lesson, then `run.py - --timeline ...` per lesson.

## Refine the plan

- **Objective card:** `{"type": "titlecard", "kicker": "Lesson 3 of 8", "title": "Deployments", "subtitle": "Roll out a new version with zero downtime", "start": 0, "end": 4}`.
- **Steps:** `{"type": "steps", "steps": [{"label": "Write the YAML", "at": 31}, {"label": "Apply", "at": 74}, {"label": "Verify", "at": 120}]}`
  or a `checklist` with `items[].at` when the teacher lists things.
- **Callouts and highlights:** `{"type": "callout", "point": [880, 420], "x": 1450, "y": 220, "title": "replicas: 3"}`,
  `{"type": "text", "text": "rolling update", "fx": {"name": "highlight", "target": "rolling"}}`.
- **Quiz card:** `{"type": "poll", "question": "Which command applies a manifest?", "options": [{"label": "kubectl apply", "pct": 100}, {"label": "kubectl run", "pct": 0}], "revealAt": 3}`
  (pause cue: hold 4-5 s), or a `card` with `title` and `items`.
- **Recap:** `card` with 3 `items` timed to the teacher's recap words.
- **Captions:** `{"type": "captions", "preset": "clean", "cpsMax": 15}`; fix terms in `words`.
- **Audio:** `"audio": {"platform": "podcast", "voice": {"denoise": "light", "eq": "clear", "deess": true}}`; no `music`
  (or only on the intro card with `"fadeOut": 1`). Remove `sfx` the skin added.
- **Colour:** `"color": {"auto": true}` only; no `look`.
- Keep a `course_template.json` of the intro card, colours (`theme.vars`) and caption settings; paste it into every module.
- `python CORE/scripts/editor.py review m03/plan.json --genre course-module`.

## Deliver

```bash
python CORE/scripts/deliver.py m03/plan.json --to youtube,web-h265 --out-dir m03/deliver --burn no --cps 15 --chapters "0:00 Objective; 0:40 Why; 1:30 Steps; 5:10 Practice; 6:40 Recap"
python CORE/scripts/qc.py m03/deliver/final_youtube.mp4 --plan m03/plan.json --platform youtube --strict
```

Hand over per lesson: MP4, `captions.vtt` + `.srt`, a transcript (the caption text from `post.md` or the words),
chapters. Name files `course_m03_deployments_v002.mp4`. SCORM: give the LMS these files; the engine makes no package.

## Check before delivering

- Objective said and shown in the first 30 s; recap matches the objective.
- Every technical term spelled right in captions; captions <= 15 cps, never over code or the key part of a slide.
- Same intro, colours and caption style as the previous modules.
- `qc.py` passes; loudness consistent across modules (all at the same target).

## Example requests

- "Edit lesson 3 of my course: cut the mistakes, add step cards and captions."
- "Split this 40-minute lecture into 5 lessons of about 8 minutes."
- "Add a quiz question after the example and a recap card at the end."
