---
name: lessons-capture
description: Internal helper invoked only by other skills in this plugin (e.g. feature-storm, feature-design, feature-plan, feature-implement, bug-fix) as their final step. Captures one skill-improvement recommendation (or "none this run") and appends a dated entry to a per-skill log under ~/.claude/dev-skills/lessons/<skill-name>.md. Takes the calling skill's slug as its only argument. Never edits any SKILL.md — the log is reviewed and applied later, either by the user or by a dedicated improver skill. Not user-facing — users should not invoke this directly.
user-invocable: false
---

# Lessons capture

Invoked as the last step of another skill in this plugin to reflect on the run that just happened and persist any improvement recommendation to a per-skill log. This skill **never edits any `SKILL.md`** — the log is the artifact, and the user (or a future improver step) applies the changes deliberately, after seeing patterns across multiple runs.

This protocol lives here alone so every calling skill reflects the same way; do not restate it inline in a caller.

## Input

The calling skill must pass its own slug as the only argument — e.g. `feature-design`, `feature-plan`, `feature-implement`. The slug is the directory name under `skills/<slug>/` and is used as the lessons-log filename.

If the invocation arrives with no argument, ask the user once for the calling skill's slug and proceed. Do not guess from conversation context — wrong attribution corrupts the log.

## Step 1 — Reflect on the run

Reflect on the run that just completed inside the calling skill. Consider both:

- **Reactive improvements** — friction observed during the run: ambiguous instructions, missing guidance, steps that turned out to be wrong, decisions you had to make that the skill should have decided for you, places where you re-did work or asked the user something the skill could have inferred.
- **Proactive improvements** — even if the run went smoothly, how could the skill be made more **efficient** or **intelligent** next time? For example:
  - Steps that could be parallelized or that re-did work unnecessarily.
  - Heuristics the skill could apply to skip or auto-resolve cases it currently asks about.
  - Better automatic detection (e.g. inferring conventions from existing project state).
  - Tighter templates — sections that are routinely "Not applicable" or routinely under-filled.
  - Better self-review lenses for failure modes that almost slipped through.
  - Output that could be more compact or more useful in chat.

**At most one recommendation per run.** A recommendation is **not** required — most runs should produce none. Only surface one if you have a genuinely valuable, specific change in mind. If you are reaching for content or padding with generic "be smarter" suggestions, produce nothing instead.

> A skill that gets one strong improvement every ten runs is far better than one that gets ten weak suggestions every run.

## Step 2 — Format the entry

If you have a recommendation, format it as three lines:

- **Observation** — what happened, or what could be better (one line).
- **Proposed change** — the specific edit you would make in `skills/<slug>/SKILL.md` (one line — name the step and the change concretely).
- **Expected benefit** — efficiency, correctness, fewer prompts, etc. (one short clause).

If nothing notable came up, the entry is a single line: `No skill-improvement recommendations from this run.`

## Step 3 — Append to the lessons log

Write the entry to:

```
~/.claude/dev-skills/lessons/<slug>.md
```

**Always append.** Never read the existing file and rewrite it — that risks overwriting prior entries. Use a single shell append (`>>`) so the operation is atomic and cannot clobber what is already there.

Concretely, run via the `Bash` tool:

```bash
mkdir -p ~/.claude/dev-skills/lessons
# Create the header only if the file does not already exist:
[ -f ~/.claude/dev-skills/lessons/<slug>.md ] || \
  printf '# Lessons captured: <slug>\n\n' > ~/.claude/dev-skills/lessons/<slug>.md
# Append the new entry:
cat <<'EOF' >> ~/.claude/dev-skills/lessons/<slug>.md
## <UTC timestamp, e.g. 2026-05-26 14:23 UTC>

**Observation:** <one line>
**Proposed change:** <one line>
**Expected benefit:** <one line>

---

EOF
```

For a no-recommendation run, the body of the heredoc is just:

```markdown
## <UTC timestamp>

No skill-improvement recommendations from this run.

---
```

Entries accumulate chronologically (oldest first, newest at the bottom). The `lessons-learn` skill can scan in either direction. Always include the trailing `---` and a blank line so the next append lands cleanly.

If the heredoc contains characters that need escaping (e.g. backticks), keep the body simple — wrap code references in plain quotes rather than backticks inside the heredoc.

## Step 4 — Return the entry to the caller

Echo the entry body (the three bullets, or the "no recommendations" line — without the `## <timestamp>` heading and without the trailing `---`) back to the user in chat exactly once, so the calling skill can paste it under its *Skill-improvement recommendations* heading in its own chat summary. Do not paste the whole log file or any prior entries.

## Constraints (non-negotiable)

- **Never edit any `SKILL.md`.** This skill only appends to the lessons log. Improvements are applied later by the user, deliberately, after reviewing patterns across runs.
- **At most one recommendation per run.** Never invent one to fill space. "No recommendations" is the common and correct answer.
- **One entry per invocation.** Even if the calling skill ran many stages, produce one entry covering the whole run.
- **Never write outside `~/.claude/dev-skills/lessons/`.** Other directories are off-limits, including the project's `docs/` and the plugin's own files.
- **Always use UTC for the timestamp** so logs collected from different machines remain sortable.
- **Trust the argument.** Do not try to "validate" the slug against the on-disk skill list — a typo there would silently misroute future entries. If the caller passed something obviously wrong (empty, contains slashes), stop and ask.
