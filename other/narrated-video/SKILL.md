---
name: narrated-video
description: Turns a slide deck, exported as a PDF, into a short narrated MP4 video with captions, read by a Google Gemini text-to-speech voice. Speaker notes, an outline, or a transcript of the talk improve the script but are optional. Writes a script of one scene per slide, stops for the user's approval, records one audio clip per sentence, times captions from the script's own words, and assembles the video with ffmpeg. Fires on "make a video from my slides", "narrated video from this deck", "turn my presentation into a video", "add a voiceover to my slides", and "captioned video of my talk".
when_to_use: Use when the user wants a narrated, captioned video of a slide presentation, built from the deck alone or with speaker notes, an outline, or a transcript of the talk. Not for a screen recording of software in use or a video of a person on camera.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
argument-hint: [path to the deck's PDF, or to the video's folder]
---

# Narrated Video

Turns a slide deck into a short video: each slide on screen while a stock AI voice reads a script written for it, with the script's words as captions.

**Produces**, in one folder per video: `script.md` (the approved narration), `video.mp4` (1920 by 1080, plays on phones and in browsers), and `captions.srt` and `captions.vtt` (caption files for sites that accept one). **Does not produce:** an upload, or a slide or sentence announcing that the narration is AI-generated; how to label the video is the user's decision.

## Rules

- Send nothing to the voice service until the user has approved the script, and then send only the script's words: never the slides, notes, outline, or transcript.
- Never ask for the API key, display it, or write it to a file. The user stores it in Step 1, in their own terminal window.
- Never open a raw transcript. Run `clean_transcript.py` on it, and read only `transcript-clean.txt`, after the user has checked it.
- Put nothing in the script that the slides and the user's material do not support.
- Use Gemini's stock voices only. Never clone or imitate a real person's voice.
- Hidden or backup slides never appear in the video.

## Running the commands

- `SCRIPTS` below means the `scripts` folder beside this SKILL.md. Write it out as a full path in double quotes, with forward slashes, in every command (for example `"C:/Users/name/.claude/skills/narrated-video/scripts/voice.py"`).
- `PY` means the Python command Step 1 finds: `python3` on a Mac, `python` or `py -3` on Windows.
- Run each command from inside the video's folder, one command at a time. The commands use only double quotes and plain arguments, so they run unchanged in Terminal, PowerShell, and Git Bash. Do not join commands with `&&`, which Windows PowerShell 5.1 rejects.
- Allow up to 10 minutes for `check_setup.py --install`, `voice.py script`, and `build_video.py`, or run them in the background; a long script takes several minutes to record. A recording that stops partway keeps every clip already made, and the same command resumes it.
- **Codex.** Codex opens an ordinary folder (one not tracked by Git) as read-only, so the user starts it in Auto mode: `codex --sandbox workspace-write --ask-for-approval on-request`. Codex then asks before any command that reaches the internet or writes outside the video's folder: the package and ffmpeg installs, the skill's own copy of its Python packages (Step 1), and every voice request. The user approves each request when Codex asks. Where the setup check reports the key missing under Codex, look at `[shell_environment_policy]` in `~/.codex/config.toml`: an `exclude` or `include_only` list there, or an `inherit` value other than `"all"`, can keep `GEMINI_API_KEY` from Codex's commands.
- The scripts print counts, lengths, costs, and file names, never the key and never transcript text. Relay their reports to the user in plain words.

## Step 1: Check the computer

**The video's folder.** Everything for one video lives in one folder, and every command runs from inside it. Where the current folder holds other work, ask the user for a name, create the folder inside it, and work there.

**Windows.** Where you are running inside WSL (the Windows Subsystem for Linux), tell the user to start the agent again from PowerShell or Git Bash in Windows itself; inside WSL, the Windows steps below (winget, python.org, and the key in the Windows account settings) do not apply.

**Find Python.** Run `python3 --version` on a Mac; on Windows run `python --version`, then `py -3 --version` if that fails. Python 3.9 or later is needed. Where none answers:

- **Mac:** `brew install python ffmpeg`. Where `brew` is not found, the user installs Homebrew in their own Terminal window, because the installer asks for their Mac password: the command is on https://brew.sh, and the user runs the lines it prints at the end, after which `brew` works.
- **Windows:** the user installs the Python install manager from https://www.python.org/downloads, accepts the offer to add Python to the PATH (the list of folders Windows searches for commands), then closes the agent and its terminal and starts them again (where the agent runs inside VS Code or a desktop app, the user quits that application and reopens it). A `python` command that opens the Microsoft Store means Python is not yet installed.

**Run the check:**

```
PY "SCRIPTS/check_setup.py"
```

It reports Python, the four Python packages (PyMuPDF, Pillow, python-pptx, and certifi), ffmpeg, and whether it can find the key. The voice step itself needs no package beyond Python. Fix what it lists:

- **Packages missing:** `PY "SCRIPTS/check_setup.py" --install`. Where the computer's Python refuses new packages (Homebrew's does), the script creates a private environment in `~/.narrated-video/venv`, and every other script finds it on its own.
- **ffmpeg missing:** on a Mac, `brew install ffmpeg`; on Windows, `winget install --id Gyan.FFmpeg -e --accept-source-agreements --accept-package-agreements`. A new install on Windows reaches the PATH only in a new terminal; the scripts find it before that.
- **Key not found:** give the user the steps below. They run them in their own terminal window, not through you, so the key never enters this conversation.

**Storing the key.** The user signs in at https://aistudio.google.com/apikey with a personal Google account (a university or employer account may block AI Studio), accepts the terms, and copies the key AI Studio creates.

Recommend that the user link a billing account to the key in AI Studio. A three-minute video then costs $0.04 to $0.08 at Google's published prices, and Google does not use what it receives to improve its products. The free tier is the fallback: it costs nothing and needs no billing account, but Google may use what it receives, and its daily cap on requests, shown in AI Studio, can stop a recording partway, since a three-minute video sends about 34 requests (one per sentence, plus the voice samples and the setup test). The recording resumes where it stopped the next day, or as soon as billing is linked.

On a Mac, in Terminal (the first command asks for the key twice and shows nothing while it is pasted; the second also gives each new Terminal window the key as `GEMINI_API_KEY`):

```
security add-generic-password -U -a "$USER" -s GEMINI_API_KEY -w
echo 'export GEMINI_API_KEY="$(security find-generic-password -a "$USER" -s GEMINI_API_KEY -w 2>/dev/null)"' >> ~/.zshrc
```

(A Mac whose Terminal runs bash rather than the default zsh takes `~/.bash_profile` in place of `~/.zshrc`.)

On Windows, in PowerShell (the first line asks for the key and hides it; the second stores it in the Windows account settings):

```
$k = Read-Host "Paste your Gemini API key" -AsSecureString
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", [System.Net.NetworkCredential]::new("", $k).Password, "User")
```

Either way the key sits in the Mac Keychain or the Windows account settings, never in a file the user might share. The scripts read it from there when `GEMINI_API_KEY` is not set, so run the check again after the user stores it. Where it still reports the key missing, the user closes the agent and its terminal and starts them again (where the agent runs inside VS Code or a desktop app, the user quits that application and reopens it).

**Test the voice:**

```
PY "SCRIPTS/check_setup.py" --test-voice
```

It saves one spoken sentence as `voice-test.wav` in the video's folder and prints its full path. Ask the user to play it. Where the script reports that Google does not recognize the model name, tell the user; do not try other model names. The current name is on https://ai.google.dev/gemini-api/docs/speech-generation, and every voice command takes it with `--model`.

## Step 2: Prepare the inputs

**The deck, as a PDF.** The user makes a copy of the deck and removes from the copy anything the video should not show: hidden and backup slides, other people's names, photos, or contact details without their agreement, and client names or figures not theirs to share. They export the copy as a PDF into the video's folder. The PDF is the only required input.

**Optional material.** Each improves the script. The deck alone also works, and the script then follows what the slides say; tell the user so.

- **Speaker notes.** Where the user has the deck as a `.pptx` (Keynote and Google Slides can export one), copy it into the folder and run:

  ```
  PY "SCRIPTS/deck_notes.py" "deck.pptx" --pdf "deck.pdf"
  ```

  It writes `notes.md`, one entry per shown slide, numbered to match the PDF, with hidden slides' notes left out, and stops where the PDF's page count differs from the shown slides.

- **An outline** of what the user would say. Save it in the folder as `outline.md`, or take it from the conversation.

- **A transcript** of a time the user gave the talk (a Zoom, Teams, or Otter export in `.vtt`, `.srt`, or `.txt` form). It holds other people's names and words, so a script cleans it before you read any of it. Ask the user to keep the raw file outside the video's folder (their Downloads folder, for example), and for their name exactly as the transcript labels them. Then run:

  ```
  PY "SCRIPTS/clean_transcript.py" "<path to the raw transcript>" --me "<their label>"
  ```

  It writes `transcript-clean.txt` with time stamps removed, the user's lines labeled `Me:`, everyone else's labeled `Other:`, and every other speaker's name replaced with `[name]`. It recognizes Zoom, Teams, and Otter labels, including pronouns in parentheses and "Last, First" names; `--me` matches with or without pronouns, in either name order. Add `--only-me` to keep only the user's lines. Where the user wants other names removed too (people mentioned in passing), they list them, one per line, in a text file outside the folder, and the command takes `--names "<path to that file>"`.

  **Check the speaker count.** Ask the user how many people spoke. Where the script's "Speakers found" count is lower, it missed someone (most often a person who spoke once under a label written in lowercase), and that person's name and words may sit inside a `Me:` paragraph, where `--only-me` keeps them. The user then lists the missed names in the `--names` file, you run the command again, and the user checks every `Me:` paragraph for someone else's words. A nonzero count on the script's line "Lines that open with words and a colon but were kept as speech" points to the same problem.

  The user then opens `transcript-clean.txt`, removes anything left that should not reach an AI (a name, a client, a figure not theirs to share, or a personal detail), saves it, and tells you it is ready. Read it only then.

## Step 3: Turn each slide into an image

```
PY "SCRIPTS/slides_to_images.py" "deck.pdf"
```

It writes `slides/slide-01.png`, `slide-02.png`, and so on, and `slides/slides-text.md` with each slide's text. Tell the user the count and ask them to confirm it matches the slides meant for the video. A higher count means hidden or backup slides reached the PDF: the user removes them from the copy, exports the PDF again, and you run this step again.

Read `slides/slides-text.md`. Where a slide's text alone does not say what the slide shows (a chart, a diagram, or a photo), view its image.

## Step 4: Write the script, then stop for the user's approval

**Length.** Ask the user how long the video should run. Where they have no target, propose about half a minute a slide and confirm it. The budget is 150 words a minute: a three-minute video is about 450 words.

**Format.** Write `script.md` in the video's folder:

```
# Script: <title of the talk>

Status: draft

## Slide 1

<the words the voice reads while slide 1 is on screen>

## Slide 2

<...>
```

Every slide gets one scene, in order, its heading number matching its image number. A scene left empty shows its slide silently for three seconds; use that rarely.

**Writing it.**

- Open with what the video covers. Open each section's first slide with that section's main point.
- Write for the ear: short sentences, one idea each. Write numbers as they are said ("forty-two percent", "three point five million dollars", "twenty twenty-six"), and spell out symbols. Expand an acronym the audience may not know on first use.
- Use only facts in the slides, `notes.md`, the outline, and `transcript-clean.txt`, never general knowledge. Where a slide shows a figure, the script uses that figure.
- From a transcript, keep the user's own wording from the `Me:` lines where it reads well, and drop filler, false starts, repeats, and asides. Carry another speaker's point only where the talk needs it, in the user's words, never quoted and never named.
- Add no sentence about the narration being AI-generated.

**Check it.**

1. Run `PY "SCRIPTS/check_script.py" --minutes <planned length>`. Fix every `ERROR` line, and rewrite each digit and symbol it flags as spoken words.
2. Have the script checked by an agent that did not write it. Where you can start a separate agent, give it `script.md`, `slides/slides-text.md`, the slide images, and the user's material, and this brief: "List every number, name, or claim in script.md that the slides and the user's material do not support, every number that differs from its slide, and every sentence that would be hard to say aloud. Report each by slide number. Change nothing." Where you cannot start one, make the same check yourself as a separate pass, reading the sources again rather than relying on your memory of them. Fix each finding, or bring it to the user where it needs their judgment.

**Stop for approval.** Show the user the whole script, its word count and planned length, what the check changed, and anything you were unsure of. Tell them two facts before they approve: only the script's words go to Google; and on the free tier Google may use what it receives to improve its products, so a script holding anything confidential needs the paid tier, which they set up by linking a billing account to their key in AI Studio. Then stop and wait. Apply the user's edits as they write them and run `check_script.py` again. Change the line to `Status: approved` only on the user's explicit approval. `voice.py` refuses a script that is not marked approved.

## Step 5: Record the voice

**Compare voices on one scene:**

```
PY "SCRIPTS/voice.py" samples
```

It reads the longest scene in three voices, Charon, Kore, and Puck (Google describes them as Informative, Firm, and Upbeat), into the `samples` folder, with each reading's length and pace. `--voices "Achird,Sulafat,Iapetus"` tries others (Friendly, Warm, and Clear); Google's speech page lists all 30. `--style "at a calm, measured pace"` adds a reading direction, which then goes on every later voice command too. The user plays the samples and chooses.

**Price it, then record it**, with the chosen voice:

```
PY "SCRIPTS/voice.py" script --voice Charon --dry-run
PY "SCRIPTS/voice.py" script --voice Charon
```

The dry run sends nothing and reports what the recording will cost. The recording makes one clip per sentence in the `audio` folder and reports each scene's length, the video's planned length, and the pace. Where the length is far from the plan, propose cuts to the user; their approved change goes into `script.md`, and the same command records only the sentences that changed.

Where Google reports a usage limit, the clips recorded so far are kept: the user waits (AI Studio shows the free tier's limits) or links billing, and the same command continues where it stopped. `--pause 10` spaces the requests ten seconds apart.

## Step 6: Build the captions and the video

```
PY "SCRIPTS/build_video.py"
```

It writes `captions.srt` and `captions.vtt` from the script's own words (each sentence on screen while its clip plays, at most two lines of 42 characters, long sentences split at a natural break) and `video.mp4`, with the captions on a band below each slide so they never cover it.

**Check the result before reporting it.** Confirm three things yourself: the words in `captions.vtt`, read in order, match `script.md`; the length `build_video.py` reports is close to the planned length; and one frame from the middle of each scene shows that scene's slide (extract it with `ffmpeg -ss <seconds> -i "video.mp4" -frames:v 1 "check-<slide>.png"`, taking the time from `captions.vtt`, view it, then delete the frame files). Fix what differs, then report the video's length and the files.

For a site that takes a separate captions file, `PY "SCRIPTS/build_video.py" --no-burn` makes a version with full-frame slides and the captions as a track the viewer switches on; upload `captions.srt` or `captions.vtt` with it. It replaces `video.mp4`, so rename the first version before running it where the user wants both.

## Step 7: Change one scene

Where the user asks for a change, make it in the scene it affects; the skill re-records nothing else:

- **A wrong word or figure:** change the sentence in `script.md` with the user's approval, then run `voice.py script` (with the same `--voice`) and `build_video.py`. Only changed sentences go to Google.
- **A mispronounced word:** add a line to `pronounce.txt` in the video's folder in the form `written = spoken` (for example `SaaS = sass`), then run `voice.py script` and `build_video.py`. The voice hears the respelling; the captions keep the written word.
- **A sentence read badly though its text is right:** `voice.py script --voice <voice> --redo <slide number>`, then `build_video.py`.
- **A slide to correct:** edit the deck, export the PDF again, run `slides_to_images.py`, then `build_video.py`. No new recording is needed while the slide count stays the same.

## Files in the video's folder

| File | Made by | Holds |
|---|---|---|
| `voice-test.wav` | `check_setup.py --test-voice` | one test sentence |
| `deck.pdf` | the user | the deck, without hidden slides |
| `notes.md` | `deck_notes.py` | speaker notes, optional |
| `outline.md` | the user | an outline, optional |
| `transcript-clean.txt` | `clean_transcript.py`, then the user | a cleaned transcript, optional |
| `slides/` | `slides_to_images.py` | one image per slide, and the slides' text |
| `script.md` | you, approved by the user | the narration, one scene per slide |
| `pronounce.txt` | the user or you | respellings for the voice, optional |
| `samples/` | `voice.py samples` | voice comparisons |
| `audio/` | `voice.py script` | one clip per sentence, and `clips.json` |
| `captions.srt`, `captions.vtt` | `build_video.py` | the captions |
| `video.mp4` | `build_video.py` | the finished video |

## Errors and fixes

| What happens | Cause and fix |
|---|---|
| `python` opens the Microsoft Store, or is not found | Python is not installed: Step 1. |
| `brew: command not found` | Homebrew is not installed, or the lines its installer printed were not run. |
| pip reports an "externally managed environment" | Run `check_setup.py --install`, which uses a private environment instead. |
| The check reports the key not found after the user stored it | The user stored it under another name, or the agent's sandbox stops the scripts from reading it. The user stores it again with Step 1's commands; under Codex, check `[shell_environment_policy]` as "Running the commands" describes; under Claude Code, the user restarts the agent. |
| Google refuses the key (401 or 403) | The key was copied incompletely or with extra characters: the user stores it again. |
| Google does not recognize the model (404) | Google renamed the model: the user finds the current name on the speech page, and the commands take it with `--model`. |
| Google reports a usage limit (429) | Wait, link billing, or add `--pause 10`; the same command resumes. |
| `build_video.py` says a scene differs from what was recorded | The script or `pronounce.txt` changed after recording: run `voice.py script` again. |
| `video.mp4 is open in another program` | Close the video player and run `build_video.py` again. |
| Captions appear in a small font | No standard font was found: run `build_video.py --font "<path to a .ttf file>"`. |
