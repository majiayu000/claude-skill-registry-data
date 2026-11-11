---
name: obsidian-brain
description: "Lets Claude think with your business notes: sets up a free Obsidian vault of plain-text markdown notes, points Claude Code at the vault folder, then turns raw thoughts into clear ideas with next actions and finishes half-finished notes, writing new notes beside your originals instead of overwriting them. Use when someone keeps notes in Obsidian (or wants to), asks Claude to go through their notes, says \"obsidian\", \"my notes\", \"second brain\", \"finish my ideas\" or \"what's in my inbox\"."
---

# Obsidian Brain

Obsidian is a free notes app. Every note is a plain `.md` file in a normal folder on your computer, so Claude Code can open the folder and read, search and write notes like any other files. No plugin or API is needed.

This skill sets up the vault so Claude knows where things go, then does three jobs: tidy raw thoughts into clear ideas, finish the half-finished ones, and tell you what is stuck.

## What you need

- **Obsidian**, free from obsidian.md (Mac, Windows, Linux, mobile). Sync and Publish are optional paid add-ons; you do not need either.
- **Claude Code**, started inside the vault folder. Claude.ai chats cannot open a folder on your computer; there you can only paste or upload notes one at a time.
- A backup before Claude edits anything: Obsidian's built-in File recovery plugin (on by default), or `git init` in the vault (add `Private/` to `.gitignore` first if those notes should not be in the history).

## Setup (`set up my vault`)

1. Ask where the vault is. New vault: in Obsidian, "Create new vault", e.g. `~/Obsidian/Business`. Existing vault: use it as it is; do not move the owner's notes.
2. Create only the folders that are missing:

   ```
   Inbox/          quick thoughts, voice-memo transcripts, anything unsorted
   Ideas/          one idea per note
   Meetings/       one note per call or meeting
   Projects/       things with a finish line
   Reference/      facts you look up: prices, processes, contacts by role
   Private/        Claude is blocked from reading this (see step 4)
   Claude/         everything Claude writes goes here first
   ```

3. Copy `templates/CLAUDE.md` to the vault root and fill the two `<...>` lines with the owner. Claude Code reads it every time it starts in the vault. Obsidian shows it as a normal note.
4. Copy `templates/.claude/settings.json` to `<vault>/.claude/settings.json`. It blocks Claude's file tools from reading or editing `Private/` and blocks `rm`. Obsidian ignores folders that start with a dot. This is a guard rail, not a vault lock: anything that must never be read by an AI belongs outside the vault folder.
5. Start it: `cd ~/Obsidian/Business` then `claude`. Test with "How many notes are in Inbox/ and Ideas/, and which three are the most recent?"

## What to ask

Plain requests, not special commands. Each one writes into `Claude/` and links back to the source notes with `[[Note name]]`, so in Obsidian you click straight from the result to your original.

| Ask | Claude does | Writes |
|---|---|---|
| "Go through my inbox" | Reads every note in `Inbox/`. For each: one-line summary, what kind of thing it is (idea, task, reference, meeting), one next action, which folder it belongs in | `Claude/Inbox review YYYY-MM-DD.md` with a move list. Moves notes only after you say "move them" |
| "Turn my raw thoughts into clear ideas" | Groups related notes, writes each group as one clear idea: the problem, the idea in two sentences, who it is for, first step, open questions | One note per idea in `Claude/Ideas/`, each linking its sources |
| "Finish my half-finished ideas" | Finds unfinished notes (see below), picks the 3 with the most to work with, writes a finished version: what the note was going for, the missing pieces filled in, first three steps | `Claude/Finished/<original name> (finished).md`. The original is untouched |
| "What's stuck?" | Lists ideas and projects with no change in 30+ days, notes that end in a question, and tasks with no owner or date | `Claude/Stuck YYYY-MM-DD.md` |
| "Connect my notes about <topic>" | Finds notes on the topic and proposes `[[links]]` between them | A list of proposed links. Adds them to your notes only after you approve |

A note counts as half-finished if it has `status: draft` in its frontmatter, ends mid-sentence or with a question, has headings with nothing under them, has a `TODO`, or is under about 60 words in `Ideas/` or `Projects/`.

## Rules

- Write new notes in `Claude/`. Edit or move the owner's notes only when asked, and say exactly which files changed.
- Never delete a note. If something looks like a duplicate, list it.
- Never invent a fact, number, name or decision. When finishing an idea, anything Claude adds that was not in the notes is marked `(suggestion)`; a gap it cannot fill is a question under "Open questions".
- Every note Claude writes starts with frontmatter: `source: [[...]]`, `created: YYYY-MM-DD`, `by: claude`. That way you can always tell your notes from Claude's.
- Use Obsidian's own syntax: `[[Note name]]` links, `#tags`, `- [ ]` tasks. Note names stay readable and never repeat an existing note's name: two files called `Morning class.md` make `[[Morning class]]` point at the wrong one.
- Do not read `Private/`. The settings file enforces this in Claude Code; do not work around it.

## End of every run

1. Notes read (count and folders).
2. Notes written, as `[[links]]`.
3. Changes to the owner's own notes (should be "none" unless asked).
4. Questions only the owner can answer.
