---
name: kanso-council
description: "Use when the user wants a stronger, multi-model, or cross-checked audit: \"convene the council\", \"council review\", \"audit with codex/grok/gemini too\", \"second opinion on this diff\", \"multi-engine audit\". Detects other agent CLIs, runs kanso-audit's framework on each in parallel, and merges the reports into one consensus-weighted findings list."
argument-hint: "[scope: diff|branch|module-path|all] [--fresh] [--<engine>-model=...]"
allowed-tools: Bash(git *) Bash(gh *) Bash(rg *) Bash(command *) Bash(mktemp *) Bash(codex *) Bash(cursor-agent *) Bash(claude *) Bash(gemini *)
---

# kanso-council

A stronger audit. Every capable agent CLI on the machine reviews the same scope under kanso-audit's framework, independently and in parallel, and the reports merge into one consensus-weighted findings list. Agreement between independent models is strong signal; a finding three engines converge on is rarely noise.

The council changes who reviews, never what happens next. Findings land in kanso-audit's report format, end at kanso-audit's approval gate, and route through its Phases B, C, and D unchanged. This skill owns Phase A only.

## The roster

Four engines are known. The host CLI (the one this session runs in) always sits on the council and audits inline; the others are detected with `command -v` and run headless in their own worktrees. An absent engine is skipped with a one-liner, never an error.

**Model policy: family aliases and CLI defaults only. A dated model ID in this file is a bug.** Aliases and defaults track each vendor's current flagship, so a new model generation needs zero edits here.

| Engine | Headless invocation | Model | Effort |
|---|---|---|---|
| codex | `codex exec "<prompt>"` | CLI default (current flagship) | `-c model_reasoning_effort="low"` |
| cursor-agent | `cursor-agent -p --output-format text "<prompt>"` | `--model grok` (family alias) | none available |
| claude | `claude -p "<prompt>"` | `--model opus` (family alias) | CLI default (medium) |
| gemini | `gemini -p "<prompt>"` | CLI default | none |

If an alias errors because the vendor renamed it, drop the model flag, rerun on the CLI default, and note the substitution in the roster line. Per-run overrides win over the table: `--codex-model=x` maps to that engine's model flag verbatim.

Open the report with the roster:

```
Council: host (claude) + codex + grok · gemini not found, skipped
```

## Resolve the scope

Same grammar as kanso-audit: `diff` (default), `branch`, a module path, or `all`. Resolve it once, before dispatch, and capture the concrete input (the diff text, or the file list for path and `all` scopes) so every engine reviews identical material. A council where each member reads a different tree is theatre.

`--fresh` applies to the host's own leg only, exactly as kanso-audit defines it. External engines are already fresh context by construction.

## Build the shared prompt

Read `../kanso-audit/SKILL.md` and extract the sections from "The review framework" through "The report format", including the adversarial lens and the anti-dilution pattern list. Do not paraphrase them; the framework lives in one file and the council quotes it. Wrap the extract with:

1. The resolved scope: the diff text inline for `diff` and `branch` scopes, or the file list plus "read these files" for path scopes.
2. Role framing: "You are one reviewer on a council. Audit this code against the framework below. Investigation only."
3. Hard constraints: read-only, no fixes, no questions, no commentary outside the report, emit exactly the report format with one line per finding.

Every external engine receives the same prompt. Difference in verdicts should come from the models, never from the briefing.

## Dispatch: worktrees, parallel, cleaned up

External engines get full tool access in headless mode (cursor-agent in particular has write and bash), so none of them runs in the user's working tree. Each engine audits a throwaway checkout:

```bash
WT=$(mktemp -d)/council-<engine>
cleanup() { [ -n "${CHILD:-}" ] && kill "$CHILD" 2>/dev/null
            git worktree remove --force "$WT" 2>/dev/null; git worktree prune; }
trap cleanup EXIT INT TERM
git worktree add --detach -q "$WT" HEAD
# diff scope: apply the captured uncommitted diff inside $WT first
( cd "$WT" && <engine invocation> ) > <engine>.report 2> <engine>.log & CHILD=$!
wait "$CHILD"
```

The engine runs as a background child with `wait`, never as a foreground command. Bash defers signal traps until a foreground command finishes, so a foreground engine would hold its worktree for the rest of its run after an interrupt; `wait` is interruptible and lets cleanup fire immediately on success, failure, timeout, or kill alike. Run one wrapper per engine, all in parallel, while the host performs its own kanso-audit Phase A inline.

Rules:

- **Record the baseline first.** `git worktree list` before dispatch; after all jobs finish, run it again and remove anything the council added that survived. The tree the user owns is untouched either way, and the run ends only when the two listings match.
- **Timeout: 5 minutes per engine.** A slow engine is dropped from the council with a note. The merge never waits on a straggler.
- **An engine that errors is dropped, not retried.** Include its last stderr line in the roster note. One engine plus the host is still a council; only the host alone means falling back to plain kanso-audit, and saying so.

## Merge

Normalise each report's findings to `path:line`, tier, category, pattern name, one-line description. Then:

- **Same finding:** same file, lines within ~5 of each other, same pattern or same described defect. Merge into one entry credited to all backers: `(3/3)`.
- **Consensus keeps the tier.** Two or more backers: highest tier claimed among them stands.
- **Lone Tier 1 stands.** A real bug found once is still a bug; mark it `(1/3)` so the user can weigh it.
- **Lone Tier 3 drops.** One engine's style nit is noise by definition.
- **Disagreement is surfaced, never averaged.** If one engine calls a site fine and another calls it a blocker, the finding goes under `## Disputed` with each side's one-line position. The user judges.

The signal rule from kanso-audit still governs the merged list: Tier 1 plus Tier 2 below 60% of total means cut Tier 3 until it holds.

## The report

kanso-audit's format, two additions: the roster line under the header, and a backer count on each finding.

```markdown
# Council audit: <short scope description>

Council: host (claude) + codex + grok · gemini not found, skipped
**Files:** <n> · **Findings:** <t1> blocker, <t2> important, <t3> polish

<Two lines max, as kanso-audit defines.>

## Findings

[1] `src/auth.ts:88` — defensive theatre swallows token-refresh errors (blocker, behaviour-change) (3/3)
[2] `src/auth.ts:141` — off-by-one in retry window (important, behaviour-change) (1/3)

## Disputed

[3] `src/cache.ts:52` — codex: unbounded map is a leak (important) · grok: bounded by session lifetime, fine
```

Then kanso-audit's approval gate, verbatim, and its Phases B, C, and D by reference. Behaviour changes still need explicit opt-in; refactors still route to `/kanso-refactor`; verification still pastes the exit code.

## What this skill never does

- Run an external engine in the user's working tree, or leave a worktree behind. Cleanup is trap-guaranteed and verified against the baseline listing before the report ships.
- Hardcode a dated model ID, here or in a generated command.
- Paraphrase the review framework into the prompt. It is quoted from kanso-audit's file, once.
- Apply a fix. The gate and everything after it belong to kanso-audit.
- Block the merge on a slow, missing, or broken engine.
- Average a disagreement into a middle tier. Disputes are shown, not smoothed.
- Pad the roster. If only the host is available, say so and run `/kanso-audit` instead.
