---
name: close-out
description: Session close-out procedure (the user says "start the close-out" or /close-out) — archive NOW.md + rewrite it from scratch, verify, lessons into RULES.md, tests, commit, resume_prompt.md.
---

# /close-out — session close-out procedure

Before the context fills up, when the user triggers it. Steps IN ORDER; [script] steps are commands, [assistant] steps are you.
If a step fails, stop and write the reason in one line; don't move on.
Windows: if `python3` is missing or opens the Microsoft Store, run the same commands with `py -3` instead of `python3`.

1. **[script]** `python3 .claude/hooks/close.py archive` → copy of `NOW.md` at `evidence/now_archive/<date>_NOW.md`;
   "Dead ends" items + "Decision:" lines are appended to `evidence/DECISIONS.md` (never trimmed). Read the `decisions:` line of the output.
2. **[assistant]** Self-review (goes into NOW, not the chat). Scale it to the session: for a simple session
   one honest line ("nothing suspicious; X deferred") is enough — don't invent worries. Ask: (a) What am I least sure of?
   (b) What did I not do, skip or assume? (c) If this breaks in 3 months, what is the most likely cause?
   For every (a)/(b) item write the command that would confirm or refute it; a doubt without a command is filler.
   Findings → NOW "Pending" / "MISTAKES I MADE"; DON'T try to fix them now (it derails the close-out).
3. **[assistant]** Write `NOW.md` **from scratch** with the RULES.md §1 template: `# NOW · <date> · commit <hash|none>` +
   8 sections (Active task ≤2 · Next ONE step ≤3 · Pending ≤6 · Scheduled ≤2 `- YYYY-MM-DD: task` ·
   Background debt ≤3 · Dead ends ≤5 · MISTAKES I MADE ≤5 · Saved to memory ≤1). ≤40 lines.
   Forbidden: history, rationale paragraphs, tables, "LATEST", "(old:". History lives in `evidence/INDEX.md`.
   Write "Next ONE step" as if for someone who never saw this chat: file path + command to run +
   what counts as done. "Continue with X" is forbidden.
4. **[script]** `python3 .claude/hooks/now_check.py NOW.md` → if not `OK`, fix and rerun.
5. **[assistant]** Is every R-{{PREFIX}} receipt written this session listed in `evidence/INDEX.md`? (`grep -n "R-{{PREFIX}}-NN" evidence/INDEX.md`)
6. **[assistant]** Lasting lesson (a recurring CLASS of mistake) → `RULES.md §6 MISTAKES I MADE` (date + R-{{PREFIX}} pointer).
   First ask: where did the user correct me this session? Every correction becomes a lesson or a memory line, or the reason it doesn't is known.
   Machine/person specific things (file location, account, preference) → `~/.claude/projects/.../memory/` + a `MEMORY.md` line.
   DON'T copy project facts into MEMORY.md (they live in the repo).
   Then `python3 .claude/hooks/memory_audit.py` (read-only). If it says `MEMORY <N> warning(s)`, fix each one
   (update a dead path, merge duplicate notes, add the missing index line) or write in NOW "Pending" why it stays.
7. **[script]** If `tests/run.py` exists, run it (`.venv/bin/python` or `python3`). If it fails, the close-out STOPS; fix it first.
   If there is no test folder, mark this step "no tests".
8. **[assistant]** Commit (if it's a git repo): only this session's files. `git add <files>` and `git commit` as SEPARATE commands;
   read `git diff --cached --stat` before committing — if `data/`, `.xlsx`, `.pdf`, `.env` or a token shows up, STOP.
   `--no-verify` is forbidden. Push: only if the user asks.
9. **[script]** `python3 .claude/hooks/close.py finish --session "${CLAUDE_SESSION_ID}"` → verifies, writes `resume_prompt.md`, marks this session closed, prints a summary.
10. **[assistant]** One line to the user: `NOW.md <N> lines · commit <hash> · tests <result>` + BELOW it the FULL contents of
   `resume_prompt.md` in a code block (so it can be copied). Saying "ready" without giving it is FORBIDDEN. No narration.
