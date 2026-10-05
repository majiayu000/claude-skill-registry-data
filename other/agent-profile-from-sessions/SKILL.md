---
name: agent-profile-from-sessions
description: Use when the user keeps re-explaining the same preferences to a coding agent across chats (design taste, video style, review rules, how work should be verified, "as I said", "I told you"), or asks how to make Claude Code, Codex, Copilot CLI or OpenCode stop forgetting how they work. Runs the free local emulo --coach report over their own past sessions to show what they repeat, with dated receipts, then offers to build a reviewed you.md profile. Not for shared team memory, project documentation, or a single forgotten fact.
---

# Stop repeating yourself to your coding agent

This skill turns a complaint like "I keep telling you the same thing" into evidence from the user's own history, and then into something the agent can load next time.

## Phases

1. **Confirm the pattern.** Ask one question: which kind of instruction keeps coming back (design, video, writing, verification, code style)? Then continue. Do not mine anything yet.
2. **Run the free report.** It is local and makes no model call:
   ```bash
   uvx emulo@0.6.7 --coach
   ```
   Add `--source claude` (or `codex`, `copilot`, `opencode`) to read one tool only. On a large history it takes about a minute.
3. **Show the evidence.** Quote the repeated asks it found, with their dates, grouped by theme. Say plainly that a text match cannot tell why something was repeated or whether the agent forgot it. The findings are possibilities, not a diagnosis.
4. **Decide the cheapest fix with the user:**
   - one or two rules: suggest adding them to `CLAUDE.md` or `AGENTS.md`, or to the host's own memory, which may be enough;
   - a recurring style across many chats (for example how they want designs or films): offer a full Emulo profile.
5. **Only with an explicit yes,** hand over to the `emulo` skill (`npx skills add ohad6k/emulo@emulo`). It mines the full history into a you.md after showing the planned model calls and getting cost approval.
6. **Review and install.** The user reads every quote in the profile and removes anything they don't want. Then install it for the current host and verify it loads in a fresh task. In Claude Code the user types `/you`; in Codex, `--target agents` writes it into the project's `AGENTS.md`.

## Do not

- Do not claim the agent will "understand" the user or follow the profile. A profile improves context; it is not a guarantee.
- Do not upload, paste or summarize session logs anywhere outside the user's machine.
- Do not run the mining step without showing its planned model calls and getting a yes.
- Do not write the profile into a committed file without naming the file and warning that it contains quotes from the user's sessions.
- Do not use this for team-wide or shared memory. Emulo profiles are personal.

## What it reads

Only the messages the user typed in supported local session logs (Claude Code, Codex, Copilot CLI, OpenCode, Google Antigravity). It does not read rules files, memory files or typed self-descriptions as evidence. Details: https://github.com/ohad6k/emulo and https://emulo.vercel.app/agent-profile
