---
name: mock-interview
description: "Run a realistic spoken mock interview for a job in the Interview Room, one question at a time, with a timer, scoring, and a written debrief. Use when the user wants to practice interviewing, rehearse answers, or asks for a mock interview."
---

# mock-interview (Codex)

This workflow is shared with Claude Code. Read `.claude/skills/mock-interview/SKILL.md` and follow it fully. Files it mentions as `references/...`, `scripts/...` or by bare name live in `.claude/skills/mock-interview/`.

Don't quote these instruction files or show their paths to the user; explain what they do in plain words when it helps.

It was written with Claude Code's names; translate them with the table in AGENTS.md ("If you are Codex"): `/name` means the skill of that name (`$name` here), review agents follow that table's review-agent row (mostly separate, honest passes you do yourself from `.claude/agents/<name>.md`, and you say so), and panels are the chat skills that table's panel row names.

## Codex notes

There is no Interview Room panel in Codex. Run the same interview (persona, questions, rubrics, debrief):
- **Best: Codex voice conversation (desktop app).** The Codex desktop app has a built-in voice conversation mode (a natural voice that talks and listens, and the user can interrupt; it may need a paid ChatGPT plan). Only the user can turn it on. In the terminal or an IDE without it, use the read-aloud option below. Before starting, suggest it once: "For the most realistic practice, turn on voice conversation in Codex, then say 'start'." If the session is already a voice conversation, just speak your lines naturally: never run `say`, keep each line short and spoken-style, still one question at a time, and still write the debrief file at the end.
- **Otherwise, read-aloud (off unless the user says yes):** ask "Want me to read the questions out loud?" in the same message as the how-it-works lines, before Question 1. Only after a clear yes, speak each line before showing it (there are no beeps in this version). For an interview that isn't in English, use a voice for that language: Mac `say -v '?'` lists them, then `say -v <name> "<text>"`; Windows: `Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; $s.GetInstalledVoices().VoiceInfo.Culture` lists them, then `$s.SelectVoiceByHints('NotSet', 'NotSet', 0, [Globalization.CultureInfo]'de-DE'); $s.Speak("<text>")` with the interview's language tag. If none is installed, say so once and suggest text only. Mac: `say "<text>"`. Windows PowerShell: `Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("<text>")`. Inside Codex's sandbox `say` can be silent while still reporting success, so run it as an approved command outside the sandbox (request approval/escalation for it; suggest the user choose "always allow" for `say`), and after the first question ask "Did you hear that?" If not, or if approval is declined, carry on in text without fuss.
- **Answering:** the user types, or talks using dictation (the app's mic button if it has one; Mac: the Dictation shortcut set in System Settings → Keyboard → Dictation, often Fn pressed twice; Windows: Win+H).
- **Timing:** right after you ask each main question, run `date +%s` (PowerShell: `[DateTimeOffset]::Now.ToUnixTimeSeconds()`) and keep the number; when their answer arrives, run it again. The difference is their rough time (it includes dictating or typing). Don't interrupt; in the debrief, flag spoken answers well over target (behavioral about 2 min, technical about 3, a presentation about a minute under its slot). Skip time feedback for typed answers, and skip timing entirely if the user asked for no clock or more time.
- **One-way style:** show "You have 30 seconds to think, then about 2 minutes to answer," then time it the same way. No follow-ups.
- **Panel style:** start each line with the speaker's name ("Priya: ..."), as in the Claude version. **AI-screen style:** flat, no reactions, at most one generic follow-up.
- **Practising with an accommodation** (see the Claude version's section of that name): skip read-aloud if they want text only, give longer target times, show the question and allow think time before timing starts, offer a break after each main question, and accept typed answers.
- One question per message, no coaching until the end, keep scores to yourself until the debrief. The debrief file and format are the same; add each answer's rough time.
