---
name: ready-to-film
description: "Turns notes, voice-note transcripts and half ideas into Reel, TikTok and YouTube scripts in the creator's own voice: ranks an idea bank, writes ten hooks per idea, writes the script at the right length, rewrites anything that sounds like AI using transcripts of the creator's past videos, and fact-checks every claim with a source and date. Use when someone wants a video script, hooks, a ranked list of what to film, a voice pass, a claims check, or a record sheet to read from while filming."
---

# Ready to Film

Five agents turn messy notes into scripts the creator reads straight off the screen, in their voice, with every claim checked before it is said on camera.

## Where it runs and what it connects to

| Source | Works in | What it really does |
|---|---|---|
| Pasted text | Claude.ai and Claude Code | notes, voice-note transcripts, past video transcripts |
| Screenshots | both | Claude reads the text in them |
| Google Drive connector (optional) | Claude.ai | searches and reads Docs in a folder the user names |
| Web search (optional) | both | the Fact Checker's public sources |
| Local files / `whisper-cli` | Claude Code | read a notes folder; transcribe audio voice notes locally if whisper.cpp is installed |

Claude.ai cannot transcribe audio files. Ask for the phone's own transcript of a voice note, or run it through Claude Code.

### Getting transcripts of your last 10 videos
- YouTube: Studio > Subtitles > download the .srt, or in Claude Code `yt-dlp --skip-download --write-auto-subs --sub-langs en <url>`.
- Instagram / TikTok: copy the auto-captions, or paste the script you read from.
- Anything else: re-transcribe the video file with whisper.cpp in Claude Code.

## Setup (`start`)

Ask in two short rounds, accept "skip", save as `PROFILE`:

1. Who are your videos for, in one line?
2. Platforms, and your usual length on each.
3. Your 3 best videos and how they did against your usual numbers (paste numbers if you have them).
4. Anything you never say or do on camera?
5. Transcripts of 10 past videos, as spoken.
6. Your current notes or idea list, or the Drive folder name.
7. Teleprompter, phone, or memory? (sets the max line length: 12 words for phone, 18 for teleprompter)
8. Your end-of-video CTA, word for word.

Then run agent 4 once to build `VOICE`, agent 1 on the notes, and suggest `script <top idea> as a reel`.

## Commands

| Command | Runs |
|---|---|
| `start` | setup above |
| `new idea: <text>` or pasted notes | agent 1 |
| `hooks <idea #>` | agent 2 |
| `script <idea #> as a reel / tiktok / youtube` | 2, pause for the hook pick (or `auto` = top hook), then 3, 4, 5 |
| `voice <pasted script>` | agent 4 |
| `check <pasted script>` | agent 5 |
| `record sheet` | agent 3's record-sheet mode on all scripts marked `checked` |

## Agents

Read the agent file before running that step; it is the only home for that role's rules.

1. `agents/01-idea-bank.md`: splits notes into single ideas, ranks what to film first.
2. `agents/02-hook-writer.md`: ten openers, first three words checked, top three marked.
3. `agents/03-script-writer.md`: script at the platform's length, beat table, record sheet.
4. `agents/04-voice-editor.md`: builds VOICE, rewrites lines that read as AI.
5. `agents/05-fact-checker.md`: claims table, every claim verified with source and date or flagged.

## Shared files

Claude Code: files in `scripts/`. Claude.ai: print the updated tables at the end of each run for the user to save to Project knowledge.

```
PROFILE.md  setup answers
VOICE.md    agent 4's voice notes
IDEAS.md    ranked idea bank
SCRIPTS.md  each script, status: draft / voiced / checked / filmed
CLAIMS.md   every claim, source, date checked, status
```

## Safety rules (every agent)

- Never invent a number, study, quote, result or personal story. Gaps become `[NEED: what, and where it would come from]`.
- No script is marked `checked` while any claim is NEEDS SOURCE or CUT.
- Build only from the creator's own words and opinions.
- Spoken style: numbers as digits, no em or en dashes, no rhetorical-question openers.

## End-of-run output

```
READY TO FILM: idea #4 as a reel
Hooks     10 written, picked #3 "Your inbox runs your day."
Script    148 words, about 38 s at 3.9 words/s
Voice     6 lines rewritten (2 antithesis, 3 filler, 1 trailing clause)
Claims    5: 3 VERIFIED, 1 FIX applied, 1 NEEDS SOURCE ("saves 6 hours a week")
Status    not ready, 1 line flagged. Send the source or cut the line.
Next      "record sheet" once it is checked
```
