---
name: continuous-learning
description: Stop-hook session-end pattern extractor (v1) — flags sessions worth mining and saves reusable patterns as one-file learned skills under ~/.claude/skills/learned/. Use when wiring, testing, or debugging the Stop-hook extractor, tuning its config.json thresholds, or extracting a session's patterns manually via /learn. Superseded by continuous-learning-v2 (deterministic PreToolUse/PostToolUse instinct learning with confidence scoring and project scoping) for ongoing automatic capture — do NOT use this skill for instinct/confidence-scored learning, project-scoped instincts, or guaranteed per-tool-call observation; that is continuous-learning-v2.
---

# Continuous Learning Skill (v1 — Stop-hook extractor)

Runs as a **Stop hook** (`evaluate-session.sh`) that fires once at session end. The script counts
user messages in the transcript, skips short sessions (below `min_session_length`, default 10), and
emits a stderr signal telling Claude to mine the session for extractable patterns and where to save
them.

**Relationship to continuous-learning-v2:** v2 (`~/.claude/skills/continuous-learning-v2/`, also
shipped as the `skyyrose-core:continuous-learning-v2` plugin skill) supersedes this skill as the
primary learning path — deterministic PreToolUse/PostToolUse observation hooks, atomic instincts,
confidence scoring, project-scoped storage. v2's own Backward Compatibility section keeps this v1
Stop hook running in parallel as the lightweight session-end extractor, feeding
`~/.claude/skills/learned/`. Use v1 for that narrow job only; everything else belongs to v2.

## When to use

- Installing the Stop hook into `~/.claude/settings.json`, or diagnosing why it never fires.
- Tuning `config.json` (`min_session_length`, `patterns_to_detect`, `ignore_patterns`,
  `learned_skills_path`).
- Responding to the hook's end-of-session signal by extracting patterns from the just-finished
  session.
- Manual extraction mid-session via the `/learn` command
  (`~/.claude/commands/learn.md`, also present in this worktree at `.claude/commands/learn.md`).

**When NOT to use:**

- Instinct-based learning, confidence scoring, project-scoped instincts, `/evolve`, `/promote` —
  that is `continuous-learning-v2`.
- Repo engineering lessons and behavioral corrections — those go to
  `docs/engineering-learnings.md` / `tasks/lessons.md` / `.wolf/buglog.json` per CLAUDE.md §8, not
  to a learned skill file.
- One-time fixes, simple typos, external-API flakes — explicitly listed in `ignore_patterns`.

## Inputs

| Input | Required state | If absent |
|---|---|---|
| `evaluate-session.sh` + `config.json` in this skill's directory | Present, script executable | **Stop.** Nothing to wire; re-fetch the skill files |
| `jq` on `PATH` | Installed | **Stop and install.** With `config.json` present, the script calls `jq` under `set -e` — a missing `jq` kills the hook with a non-zero exit, not a graceful default |
| `CLAUDE_TRANSCRIPT_PATH` env var | Set by Claude Code when the hook fires | Manual runs without it exit `0` silently **by design** (hook no-op). For a manual test you MUST point it at a transcript fixture — never read a silent no-op as a passing test |
| Hook entry in `~/.claude/settings.json` | `Stop` hook pointing at `evaluate-session.sh` | Skill is inactive — no signal will ever appear. Wire it first (Procedure step 1) |

`config.json` knobs: `min_session_length` (default 10), `extraction_threshold`, `auto_approve`,
`learned_skills_path` (default `~/.claude/skills/learned/`), `patterns_to_detect`,
`ignore_patterns`.

## What gets extracted

- Error resolution patterns
- User correction patterns
- Framework workarounds
- Debugging techniques
- Project-specific conventions

Ignored (per `ignore_patterns`): simple typos, one-time fixes, external API issues.

## Procedure

1. Wire the Stop hook in `~/.claude/settings.json` (path adjusted to where this skill lives):

   ```json
   {
     "hooks": {
       "Stop": [{
         "matcher": "*",
         "hooks": [{
           "type": "command",
           "command": "~/.claude/skills/continuous-learning/evaluate-session.sh"
         }]
       }]
     }
   }
   ```

2. Verify the wiring exists (see Verification check 4) before trusting any "no patterns this
   session" outcome — an unwired hook is silent, and silence reads as success (fail-open,
   bug-230 pattern).

3. At session end the hook prints to stderr either
   `[ContinuousLearning] Session too short (N messages), skipping` or
   `[ContinuousLearning] Session has N messages - evaluate for extractable patterns` plus the
   save path. On the second signal, review the session against `patterns_to_detect` and drop
   anything matching `ignore_patterns`.

4. Save each extracted pattern to `learned_skills_path` as `[pattern-name].md` — kebab-case name,
   **one pattern per file**:

   ```markdown
   # [Pattern Name]
   **Context:** [When this applies]
   ## Problem - Solution - When to Use
   ```

5. For mid-session extraction without waiting for the Stop hook, run `/learn`.

## Verification

Run from the skill directory (`SKILL=/Users/theceo/DevSkyy/.claude/worktrees/glimmering-crafting-shannon/.claude/skills/continuous-learning`).
Each check can return "no":

```bash
bash -n "$SKILL/evaluate-session.sh"        # 1. PASS: exits 0 (script parses)
jq empty "$SKILL/config.json"               # 2. PASS: exits 0 (config parses)
T=$(mktemp -d)                              # 3. prove the length gate can fail BOTH ways
printf '{"type":"user"}\n{"type":"user"}\n{"type":"user"}\n' > "$T/short.jsonl"
CLAUDE_TRANSCRIPT_PATH="$T/short.jsonl" bash "$SKILL/evaluate-session.sh"
                                            #    PASS: stderr "Session too short (3 messages), skipping", exits 0
for i in $(seq 1 12); do printf '{"type":"user"}\n'; done > "$T/long.jsonl"
CLAUDE_TRANSCRIPT_PATH="$T/long.jsonl" bash "$SKILL/evaluate-session.sh"
                                            #    PASS: stderr "evaluate for extractable patterns" + save path
grep -c 'continuous-learning/evaluate-session.sh' ~/.claude/settings.json
                                            # 4. PASS: prints >= 1. 0 = hook INACTIVE (unwired)
```

Checks 1–3 earn `[repro]` (ran and observed); check 4 earns `[repo]` (reads the settings file, not
live hook execution). A run where check 3's short fixture does not print the skip line, or the long
fixture does not print the evaluate line, is a broken gate — do not proceed to extraction.

## Worked example

Real run, 2026-07-29, this worktree (`$SCRATCH` = the session scratchpad dir; fixtures were
synthetic transcripts):

```bash
$ bash -n "$SKILL/evaluate-session.sh"; echo "syntax-check exit:$?"
syntax-check exit:0
$ jq empty "$SKILL/config.json"; echo "config-parse exit:$?"
config-parse exit:0
$ printf '{"type":"user"}\n{"type":"user"}\n{"type":"user"}\n' > "$SCRATCH/short-transcript.jsonl"
$ CLAUDE_TRANSCRIPT_PATH="$SCRATCH/short-transcript.jsonl" bash "$SKILL/evaluate-session.sh"
[ContinuousLearning] Session too short (3 messages), skipping
$ for i in $(seq 1 12); do printf '{"type":"user"}\n'; done > "$SCRATCH/long-transcript.jsonl"
$ CLAUDE_TRANSCRIPT_PATH="$SCRATCH/long-transcript.jsonl" bash "$SKILL/evaluate-session.sh"
[ContinuousLearning] Session has 12 messages - evaluate for extractable patterns
[ContinuousLearning] Save learned skills to: /Users/theceo/.claude/skills/learned/
```

Both branches of the length gate observed firing — the 3-message fixture was skipped, the
12-message fixture triggered extraction with the save path. `[repro]`

## Failure modes

- **Hook never wired → silent inactivity.** No error, no signal, and "no learned skills" looks
  identical to "nothing worth learning". This is the fail-open pattern (bug-230): absence of the
  gate reads as a pass. Verification check 4 exists for exactly this.
- **`jq` missing → hook dies.** `set -e` + command substitution means a missing `jq` exits the
  script non-zero when `config.json` is present. Symptom: Stop-hook error at session end.
- **Manual run without `CLAUDE_TRANSCRIPT_PATH` → deceptive green.** The script exits 0 having
  done nothing. Only a run against a fixture (Verification check 3) proves behavior.
- **Extracting noise.** One-time fixes, typos, and external-API flakes are in `ignore_patterns`
  for a reason — a learned-skills directory full of noise buries the real patterns.
- **Multiple patterns in one file.** Keep skills focused — one pattern per file, kebab-case
  filename, or downstream reuse and pruning both degrade.
- **Expecting guaranteed capture from v1.** Skill/Stop-hook-based observation is session-end-only
  and coarse; v2 moved to PreToolUse/PostToolUse hooks precisely because per-tool-call capture
  must be deterministic. Needing that guarantee here means you are in the wrong skill — use
  `continuous-learning-v2`.
