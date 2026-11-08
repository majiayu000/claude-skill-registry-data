---
name: start
description: "Use when profile/preferences.md says \"SETUP: not done\", or the user is new, wants to set things up or redo their preferences. First-time setup interview (15-20 minutes): master resume from their resume file, career stage, field, target roles, preferences, field pack. Picks up where it left off."
---

# start (Codex)

This workflow is shared with Claude Code. Read `.claude/skills/start/SKILL.md` and follow it fully. Files it mentions as `references/...`, `scripts/...` or by bare name live in `.claude/skills/start/`.

Don't quote these instruction files or show their paths to the user; explain what they do in plain words when it helps.

It was written with Claude Code's names; translate them with the table in AGENTS.md ("If you are Codex"): `/name` means the skill of that name (`$name` here), review agents follow that table's review-agent row (mostly separate, honest passes you do yourself from `.claude/agents/<name>.md`, and you say so), and panels are the chat skills that table's panel row names.

## Codex notes

- Choice questions: Codex has no clickable multiple-choice tool here, so show each option set as a short numbered list (several related ones in one message is fine) and ask them to reply with the numbers. Open questions stay one per message.
- Saving to their profile: there's no edit popup in Codex, so skip the note about it. As in Claude, show the user the exact lines you'll save and ask "OK to save?" before every save to their master resume or preferences, and keep to the same saves (master resume once; preferences at the end of section 3 and of section 6). Make each save one `apply_patch` (several hunks in it are fine).
- Section 4 (field pack): there are no background research agents here; build it yourself after the conversation, and tell the user it will take a few minutes. Add `field-pack` to the setup checklist (`profile/setup-progress.md`) only when all five files say `STATUS: generated`; if the chat ends first, the next `$start` (or the session's welcome note) picks up the files still marked `not generated`.
- Section 6 (Gmail): always ask question 15, even if Gmail isn't connected yet (connecting is something the user does in settings, not a tool call). In Codex, Gmail (and Google Calendar, where offered) is a plugin: the **Plugins** tab in the ChatGPT desktop app, or `/plugins` in the terminal (the user signs in to Google there), then they start a new chat. Give the same warning about Google's permission screen. For a work or school Microsoft 365 account or any other mail, follow the Codex notes in `.claude/skills/sync-inbox/references/other-inboxes.md` (pasting or saving emails into imports always works).
- Section 7 (panels): skip the panel check. Say instead: "In this app everything happens right here in the chat. Say **show my board** for your job list, **show my outbox** for drafts, **show my contacts** for your network, and **job inbox** for new openings; when you fill in an application form, ask for your **apply kit**. Type **$today** at the start of each session to see what's due. For mock interviews, start a voice chat in the ChatGPT desktop app, or type your answers."
- Section 7a (your look): there is no Claude design system route here (no Artifact tool); offer the website, brand-file and presets routes. For "show me the looks", describe the presets in one line each rather than opening previews. If `node` isn't available, follow "Without Node" in the page-design skill.
- Section 7b (folder safety check): same as Claude; run the `git config` command only with the user's OK.
- Section 8: write the commands Codex-style: `$find-jobs`, `$mock-interview`, `$today`, `$tour` (or just ask in plain English).
