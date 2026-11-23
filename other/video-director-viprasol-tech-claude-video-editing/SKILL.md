---
name: video-director
description: "The boss of all Video Studio skills: give it any footage (one clip, a folder of clips, photos, a voice recording, a song) and it watches and listens first - speech, language, faces, music and beat, screen recordings, shot rate, light, orientation, length - then decides what the video should be (reel, podcast, tutorial, wedding film, montage, vlog, ad...), picks the right genre skill, look, format, platform and clean-up, and runs the whole professional edit through to delivery and QC. Use it whenever the user hands over footage without naming a specific style or genre: 'edit this video', 'make something good from these clips', 'turn this into content', 'what should I do with this footage', 'edit it like a pro', 'just make it', or any video file with a loose goal ('for Instagram', 'for YouTube', 'for the client'). Needs video-studio-core and the genre skills in the same skills folder."
license: MIT
---

# Video Director

Watch the footage, decide like a senior editor, then edit. The user should only have to hand over the files.

- **Best for:** any footage when the user hasn't said which skill or style to use
- **Inputs:** files or a folder (video, photos, audio), plus whatever the user said about the goal
- **Decides:** genre skill (42), skin (40), format, platform, clean-up flags, deliverables
- **Then runs:** the chosen genre skill's own workflow, end to end

## Before you start

- Needs **video-studio-core** and the genre skills in the same skills folder. `CORE` = `video-studio-core`, `SKILLS` = the skills folder.
- First run on a machine: `python CORE/scripts/check_env.py`.
- Collect the user's own words about the goal (platform, purpose, audience, length, deadline). Pass them as `--goal`: they outweigh everything the footage suggests.

## 1. Read the footage

```bash
python CORE/scripts/director.py FILES_OR_FOLDER --goal "<the user's words>" --work director
# fast first look on very long footage: add --quick (no transcription / shot detection), or --asr-seconds 300 for more speech
```

It writes `director/director.md` (read it) and `director/director.json`. Each one holds:
- **The facts:** speech coverage, words per minute, language, opening words, faces and how many, screen-recording look, beat/BPM, cuts per minute, light level, orientation, durations, photo/clip/audio counts.
- **A ranked list of genre skills** with the reasons for each.
- **A ready `run.py` command** (genre, skin, format, platform, `--smart-cuts`/`--retakes`, `--reframe`, `--denoise`, `--music`, `--clips`/`--auto`).

## 2. Decide like an editor (you make the final call)

The script is a heuristic, so check it against what a veteran would see:

- **Read the opening words.** They tell you what the video is about better than any metric. A cooking talk is `recipe-video` even if the score says `vlog`; a founder story is `brand-film`; a guest conversation is `podcast-episode`.
- **The goal beats the footage.** "For Instagram" means 9:16 and `--platform reels`. "For the client's website" means 16:9 and a brand or testimonial film. "Shorts from my podcast" means `clip-miner-pro`.
- **Length tells you the job:**

  | footage | usual job |
  | --- | --- |
  | ≤ 2 min of one person talking | `retention-reel` |
  | 3-25 min | `vlog` / `longform-retention` |
  | ≥ 25 min | `podcast-episode`, `interview-doc` or `clip-miner-pro` |

- **Many clips with little talk** is a montage: `event-recap`, `travel-cinematic`, `wedding-highlight` (vows, rings, couple), `real-estate-tour` (rooms), `sports-highlight`.
- **Photos only:**

  | photos are | genre |
  | --- | --- |
  | family, old, memorial | `memorial-tribute` |
  | property | `real-estate-tour` |
  | anything else | `event-recap` montage |

- **Audio only:** speech → `faceless-explainer` (or `podcast-episode` audio deliverables); song → `lyric-video`.
- **Picking a skin:** use the genre's first skin unless the user named a look or a brand. The alternatives are listed in `director.md`.
- **One question at most:** ask only if `director.md` has an "Ask the user" line and the user gave no goal. Otherwise decide and go.

Tell the user the decision in two lines before editing. For example: "This is a 1-minute talking clip, so I'm cutting it as a retention reel for Instagram (9:16, halo-cut look, face-follow reframe, captions, -14 LUFS)."

## 3. Edit with the chosen genre skill

1. Open `SKILLS/<chosen-skill>/SKILL.md` and follow it from "Make the edit" to the end. It holds the structure, pacing, cut rules, transitions, sound, colour and deliverables for that genre.
2. Start from the director's command and replace `CORE`/`SKILLS` with the real paths. It stops after the plan so you can refine it.
3. Refine the plan, run `editor.py review PLAN --genre <skill> --fix`, check the contact sheet (`render.py --frames`), then `render.py`, `finish.py`, `deliver.py`, `qc.py`, all as the genre skill says.
4. If the user wants every platform at once, finish with `SKILLS/platform-pack`. For accessibility (SDH captions, audio description), use `SKILLS/accessibility-pack`.

**Messy or dark footage:** add `--stabilize` (handheld), `--denoise light|strong` (low light; the director adds `light` below about 70/255 brightness) or `--deflicker` (LED or mains flicker) to the `run.py` command.

**Several kinds of footage at once** (for example a podcast plus B-roll plus a song): make the main edit from the main source with its genre, then pass the rest as `--broll DIR` and `--music`.

## 4. Report

Tell the user:
- what you decided and why, in one line per decision
- what was cut (seconds removed, retakes dropped)
- the look and loudness
- every delivered file with its path
- the QC result, including anything you could not fix

Offer one next step, such as vertical cutdowns from a long edit or a thumbnail set.

## Check before delivering

- The chosen genre fits the content and the user's goal, not just the score.
- The genre skill's own checklist passed: contact sheet viewed, `editor.py review` issues fixed, `qc.py` with 0 FAIL.
- The format matches the platform: 9:16 for Reels, TikTok and Shorts, and 16:9 for YouTube unless asked otherwise.
- Claims, names and numbers on screen come from the footage or the user. Nothing is invented.

## Example requests

- "Here's a video from my phone, edit it." (→ reads it, decides, edits)
- "Make something good for Instagram out of this folder of trip clips and this song."
- "This is our 50-minute podcast, do what you'd do with it."
