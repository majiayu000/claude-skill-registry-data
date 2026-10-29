---
name: claude-code-basics
description: Interactive beginner walkthrough for learning the physical mechanics of VS Code and Claude Code, including folders, Explorer, paths, panels, commands, prompts, terminal output, tool results, and edit approvals.
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash(pwd), Bash(ls *), Bash(git status), Bash(git branch --show-current), Bash(git log *)
---

## What This Skill Does

A hands-on, one-topic-at-a-time lesson in the *physical mechanics* of using VS Code and Claude Code — opening a folder, the Explorer, paths, the chat panel, slash commands, writing prompts, the terminal, reading tool results, and the real permission/edit-approval UI. Assumes zero prior technical knowledge.

This is **not** `start` or `new-joinee` — those teach the conceptual MCP/Skills architecture (the "four/seven-layer model"). This teaches the literal buttons, panels, and prompts a beginner is looking at right now. The two are complementary; point a learner here for "how do I actually use this thing," and to `start`/`new-joinee` for "how does this AI system work."

## Hard Rules (never break these)

- `Write` and `Edit` are **deliberately not** in `allowed-tools`. Every file creation or edit in this lesson happens as a genuinely unapproved tool call, so the learner sees the real permission/diff prompt — never add these tools to `allowed-tools`.
- Before every such attempt, confirm conversationally first ("Ready for me to try creating/changing X? You'll see a real approval prompt.") — this is separate from, and in addition to, the tool's own permission prompt.
- `Write`/`Edit` may only ever target exactly one of these three paths, never anything else:
  - `onboarding-output/claude-code-basics-practice.txt`
  - `onboarding-output/claude-code-basics-progress.md`
  - `onboarding-output/claude-code-basics-cheat-sheet.md`
- Never claim to delete the practice file — no delete capability exists in `allowed-tools`. Explain manual removal instead (see Topic 9).
- Terminal commands are limited to exactly the patterns in `allowed-tools`. If a git command fails because the folder isn't a Git repository (or Git is unavailable), explain that plainly as a normal, unremarkable state — never as an error.
- Button labels, icons, and panel positions vary between VS Code/Claude Code versions and themes. Describe things generally ("look for something like…") and ask the learner to confirm what they actually see rather than asserting an exact label or position.
- Do not mark a topic's comprehension check passed until the learner actually passes it. One wrong answer gets supportive corrective guidance and a rephrased retry — never the identical question twice, never marked complete regardless.
- `context: fork` is intentionally not used — this lesson requires continuous conversation and real learner responses.

## Step 0: Check for Prior Progress

Before Step 1, check whether `onboarding-output/claude-code-basics-progress.md` exists (Read). If it does and shows `Status: IN PROGRESS`, ask via AskUserQuestion: **Resume from the next incomplete topic** / **Restart from the beginning** / **View saved progress** (show its contents, then ask again). Otherwise proceed to Step 1.

## Step 1: Welcome and Starting Assessment

Briefly list the topics (Step 2 table). Then, for each topic, ask one quick self-assessment question via AskUserQuestion: **I already know this** / **Not sure** / **Never used this**. Topics marked "I already know this" are recorded as **Skipped (learner self-assessed)** — distinct from **Passed**, and never presented as if their comprehension was actually checked. Everything else proceeds through the full Topic Template below.

## Topic Template (applies to every topic in Step 2)

1. **Explain** — 2-4 plain-language sentences.
2. **Topic controls** — AskUserQuestion supports at most 4 options, so this is exactly 4: **Continue** / **Repeat or show another example** / **Pause here** / **Stop the lesson**. Loop back to step 1 with a fresh example if the repeat/example option is chosen. On Pause, confirm via AskUserQuestion: **Save progress and stop (Recommended)** / **Actually, don't save — just stop**, then (if saving) attempt the `Write` (real permission prompt) to `onboarding-output/claude-code-basics-progress.md` with current topic, and each topic's Passed/Skipped/Not-yet status. On Stop, end the session without forcing a save.
3. **Demonstrate** (only where a live command genuinely helps — see per-topic notes; several topics are UI-only and can't be demonstrated since Claude can't see the learner's screen).
4. **Practical exercise** — one small, concrete thing the learner does or reports back.
5. **Comprehension check** — one question via AskUserQuestion, plausible distractors, exactly one clearly correct answer as the options. Do **not** mark any option "(Recommended)" here — this is a quiz, and flagging the correct answer would defeat the check; that's the one place in this skill where the clickable-question convention's recommended-option requirement doesn't apply. Wrong → supportive correction + one rephrased retry. Right (1st or 2nd try) → mark **Passed**.
6. **Topic controls again** — same menu as step 2, offered before moving on.

## Step 2: The Nine Topics

| # | Topic | Demo | Exercise focus | Check focus |
|---|---|---|---|---|
| 1 | Opening a project folder | `pwd` (live) — this is the folder Claude is already working in | Find the open folder's name in VS Code's title bar / File menu | What opening a folder actually does (sets the workspace) vs. distractors (installs something, connects online) |
| 2 | VS Code Explorer | None (can't see their screen) — describe the sidebar file tree, ask them to describe theirs | Name one file/folder they see in their Explorer | What the Explorer is for (browsing project files) vs. distractors (running commands, chatting) |
| 3 | Files and paths | `ls` (live) — point out this is what feeds the Explorer view | Write the relative path of a file from the `ls` output | Absolute vs. relative path — pick the relative one |
| 4 | The Claude Code panel | None — describe where chat/tool-output appears, distinct from editor tabs | Where in their window this conversation appears | What the panel is for vs. distractors (terminal, settings, Explorer) |
| 5 | Slash commands | Point at `/claude-code-basics` itself as the live example | Type `/` in their own panel, report what list appears | What typing `/` does vs. distractors |
| 6 | Writing good prompts | Show one vague prompt next to one specific one | Rewrite a given vague request to be specific (what, where, constraints) | Pick the more effective of two prompts |
| 7 | Terminal basics | `pwd`, `ls`, `git status` or `git branch --show-current` (live) — if not a Git repo, explain that calmly, not as an error | Learner runs one simple command themselves in their own terminal, reports the output | Terminal vs. asking Claude — what's different |
| 8 | Interpreting tool results | Walk back through the Topic 7 output line by line | State one concrete fact the git output told them (e.g. branch name) | Read a short sample tool result, answer what it shows |
| 9 | Permission requests & accepting/rejecting edits | See Step 3 below — the one topic with real file operations | Genuinely accept or reject a real create + a real edit | Explain in their own words what Accept vs. Reject just did |

## Step 3: Topic 9 in Detail — Permission Requests and Accepting/Rejecting Edits

This topic separates **permission approval** (allowing a tool call to run at all) from **reviewing an edit** (judging a specific proposed change) — they are related but not the same, and the learner should experience both distinctly:

1. Explain what's about to happen: "I'll try to create a small practice file at `onboarding-output/claude-code-basics-practice.txt`. Since I don't have pre-approved write access, you'll see a real approval prompt." Confirm readiness via AskUserQuestion before attempting anything.
2. Attempt `Write` to exactly `onboarding-output/claude-code-basics-practice.txt` with trivial placeholder content. This triggers the real permission prompt.
3. Whatever the learner chooses, explain what just happened in plain language — approve → file created; reject → nothing was written, and that's a completely valid, safe choice. Don't treat rejection as a failure state.
4. If the file was created: explain the specific content change about to be proposed *before* attempting it ("I'll try changing line 1 from X to Y"). Confirm readiness again.
5. Attempt `Edit` on the same practice file. This triggers the real diff-review prompt — a different UI moment than step 2's create-permission prompt; name that difference explicitly.
6. Explain what the diff view showed and what their accept/reject choice did.
7. `Read` the practice file (this tool *is* pre-approved) to show the learner what's actually in it now — closing the loop between "what you approved" and "what's really there."
8. State plainly: this skill has no ability to delete the practice file automatically (no delete tool is available, by design). If the learner wants it gone, they can delete it themselves — right-click it in the Explorer and choose Delete, or run `rm onboarding-output/claude-code-basics-practice.txt` in their own terminal if they're comfortable with that.
9. Run the comprehension check per the Topic Template — asking the learner to explain, in their own words, the difference between approving permission and reviewing a diff.

## Step 4: Final Practical Check

A short integrative scenario spanning multiple topics — e.g. "Walk me through, step by step, what you'd do to ask me to summarize a file in your project." Compare their answer against the real sequence (open folder → find file via Explorer/path → use the panel to write a specific prompt → read the result). Supportive correction and one retry if key steps are missing, same as any topic check. Don't proceed to Step 5 until this passes.

## Step 5: Optional Progress / Cheat-Sheet Save

Ask via AskUserQuestion: *"Want me to save a cheat sheet to `onboarding-output/claude-code-basics-cheat-sheet.md`?"* — **Yes, save it (Recommended)** / **No thanks**. Only attempt the `Write` (real permission prompt, same as any other file operation in this skill) if they say yes. Cheat sheet covers: the nine topics in one line each, and which ones they passed vs. skipped by self-assessment.

If `onboarding-output/claude-code-basics-progress.md` exists from an earlier pause, ask via AskUserQuestion: **Update it to `Status: COMPLETE` (Recommended)** / **Leave it as-is** — rather than delete it, since this skill cannot delete files. Tell the learner they're welcome to remove the progress file themselves once finished, same guidance as the practice file.

## Notes

- Every topic offers exactly 4 controls (AskUserQuestion's max) — Continue / Repeat or show another example / Pause / Stop — never skip straight through without offering this menu.
- Self-assessed "I already know this" skips are recorded distinctly from comprehension-check Passes; never conflate the two in the final report or cheat sheet.
- Live demonstrations only happen where `allowed-tools` genuinely supports them (the five safe read-only Bash patterns, plus `Read`/`Glob`/`Grep`); several topics are necessarily descriptive since Claude cannot see the learner's actual screen.
- Keep the tone patient and encouraging — this is for someone who has never done any of this before.
- Clickable-question convention: every decision/confirmation point (resume choice, self-assessment, topic controls, pause-save, readiness confirms, cheat-sheet/progress-file offers) uses `AskUserQuestion`. The one deliberate exception is comprehension-check options never carrying a "(Recommended)" tag, since this is a quiz. Topic 9's final explain-in-your-own-words check and Step 4's integrative scenario stay free text — they require an actual explanation, not a choice among options.
