---
name: snapshot-protocol
description: "Use when composing a restart snapshot or continuation - snapshot structure, worktree resolution, write rules."
---

# Snapshot Composition Protocol
This is the canonical source-of-truth for snapshot composition discipline.
Invoke this skill to compose a snapshot, then take the variant-specific
terminal action.

## Step 1 — Resolve identity and your worktree

```bash
# $REPO must be YOUR worktree — the directory `thrum prime` reads the restart
# snapshot back from. Resolve it ONLY via the daemon's authoritative,
# peercred-resolved identity (`thrum agent worktree --authoritative`) — NEVER
# via `thrum whoami --field worktree` (cwd-resolved) or `git rev-parse
# --show-toplevel` (also cwd-resolved). A cwd-derived pattern
# could silently resolve to a DIFFERENT agent's worktree, or the main repo,
# saving this snapshot where nothing ever reads it back. There is NO git
# fallback — if the daemon can't answer, refuse and stop rather than guess.
REPO=$(
  thrum agent worktree --authoritative 2>/dev/null
) || { echo "ERROR: cannot authoritatively resolve your worktree via the daemon. Refusing to fall back to cwd/git-toplevel — that would risk silently saving this snapshot to the wrong repo. Check daemon connectivity and retry."; exit 1; }
[ -n "$REPO" ] || { echo "ERROR: thrum agent worktree --authoritative returned empty"; exit 1; }
AGENT=$(thrum whoami --field agent_id) || { echo "ERROR: agent not registered"; exit 1; }
[ -n "$AGENT" ] || { echo "ERROR: empty agent_id"; exit 1; }
mkdir -p "${REPO}/.thrum/restart"
```

## Step 2 — Compose your continuation

### Composition discipline (always applies)

Your context is high (or you are preparing to park) and the goal is to preserve
all load-bearing decisions across the session boundary. Write a rich
continuation that future-you will read as the first action after wake.

**§1 of your snapshot is REQUIRED FIRST PROSE.** Write the "Big picture — what
shipped this session" (or, for sleep snapshots, "where work stands at park
time") section BEFORE anything else. Be specific: name the artifacts, the
decisions, the cycles closed. Examples:

> Locked the session-archive spec v2 with §1 Big picture requirement, five
> Q-Spec approvals, and Q-Spec-5 deferred to impl-time. Hand-off pending
> coordinator final review.
>
> Investigated rc.9 inbox-race against <implementer>'s hypothesis: confirmed
> the lock-substrate fence is the right fix. Filed thrum-XXX with 4 BLOCKING
> evidence points.
>
> Closed <epic> brainstormer-third pass. 2 BLOCKING + 5 IMPORTANT + 10 MINOR.
> All three load-bearing traps PASSed. Standing by for <epic> next batch.

This section becomes YOUR OWN log entry, visible in `thrum agent sessions list`
alongside the archives of every other session you've ever restarted from.
Future-you (and other agents inspecting your history) skim §1 to decide which
sessions are worth re-reading. Write it first — before the Resume Plan, before
file paths, before patterns — because composing the §1 summary forces you to
identify what was actually load-bearing about this session, and that priority
shapes everything else you write below it.

**Stamp your snapshot with the base it was authored against.**
Derive and emit the **Authored-against** stamp per
the /thrum:stamp-protocol skill and place it at the very top of your
§1 section (that protocol computes the SHA and merge_target for you — never
hand-type them). This is what lets `thrum prime` diff your snapshot at the next
wake and flag which cited files have MOVED; an unstamped snapshot reads as
"current", indistinguishable from one that never drifted.

Any commit your snapshot names as its own stamped SHA must also be readable
under `stamp-protocol.md`'s "Read-time provenance re-derivation" section
(SHA-resolves, then merge-status) — link to that section rather than restating
its checks here.

**Describe commits, don't claim them.** A snapshot's job is to describe what a
commit's content and effect ARE — that's checkable by anyone re-reading it.
Prohibit first-person narration of git actions in the body of a snapshot:
no "I pushed X", "I fixed Y and verified it", "I ran Z". Write instead:
"commit `<sha>` exists and does `<Y>`" / "`<sha>` addresses `<Y>`". Attribution
of WHO performed a git action already lives in `command.jsonl` / `hooklog.jsonl`
— restating it here would assert authorship the snapshot-writer has typically
never mechanically verified.

After the §1 block:

CRITICAL DISCIPLINE — compose from your own working context only. To preserve
the remaining runway:

- Do NOT dispatch sub-agents (Agent, Explore, etc.)
- Do NOT re-read files you've already read this session
- Do NOT spawn web fetches or external lookups
- Do NOT run lengthy investigations (git log spelunking, codebase searches,
  multi-file grep walks)

Each of those costs context you don't have to spend, and the cost compounds — a
sub-agent that returns 6K tokens of summary doesn't just cost the dispatch, it
pollutes the dying session further. If a fact isn't already in your working
context, label it "unknown" or "verify post-restart" rather than fetching it
now. Trust your in-context state.

Write for a competent stranger in your role — someone who has the runtime
briefing (`thrum prime`, role preamble, project state) but none of this
session's conversation context. Refer to the previous session in third person.

### Structure (16 sections)

Every variant uses this structure.

Numbered `§1.` through `§16.`. Each section names a concern; write as prose, a table, or omit with an explicit
"N/A: <reason>" rather than skipping silently.

```text
§1.  Header block — author / date / restart reason / restart-you mandate / context-percent at write time
§2.  Identity — agent_id / worktree path / branch / role / coordinator name / cut-point commit SHA
§3.  Big picture — what shipped this session  [REQUIRED FIRST PROSE]
§4.  Mission state — where this work currently sits in its pipeline
§5.  Locked design decisions — operator-LOCKs, design-fork resolutions, with rationale
§6.  Open L-questions parked for the operator — or "NONE: <reason>" with explicit note
§7.  Wire contracts — durable technical reference (types, signatures, file:line cites)
§8.  Capability matrix — per-surface contracts (row-by-row table for fanout work; OMIT if N/A)
§9.  Design inventory — locked taxonomy (entanglement classes, patterns, anti-patterns; OMIT if N/A)
§10. Cycle history — review cycles run, findings, fold record (OMIT if pre-review-phase)
§11. Pipeline state — DAG of artifacts (brainstorm → plan → impl → review) with current cursor
§12. Pre-restart artifacts on disk — durable handoff manifest (table: artifact / path / status)
§13. Anticipated Q&A — questions restart-you or downstream implementer will ask, pre-answered
§14. References — bd IDs, commit anchors, memories, file paths, message IDs (load-bearing for transcript recon)
§15. Honest unknowns — verify post-restart, do NOT fabricate
§16. Restart-you's immediate next actions — numbered; step 1 actionable from cold start
```

**Per-section guidance:**

- **§1 Header.** Top of file. Author (agent_id), date, restart reason (1-line
  trigger), one-sentence mandate to restart-you ("read this in full, then [N
  specific actions]"), context-% at write time. Read-first prominence.
- **§2 Identity.** `agent_id` / worktree absolute path / branch / role /
  coordinator name / cut-point commit SHA for any line cites that follow.
  Mechanical; lets a totally cold restart-you orient before reading any prose.
- **§3 Big picture.** REQUIRED FIRST PROSE. 1–3 sentences summarizing what the
  session accomplished. Specific: artifacts, decisions, cycles closed. Becomes
  the session-archive log entry. Write this BEFORE anything else (composing §3
  forces you to identify what was load-bearing, which shapes what you write
  below). **Sleep variant:** for `/thrum:sleep`, §3
  frames as "where work stands at park time" rather than "what shipped" — the
  agent is parking, not completing. Composition discipline (1–3 sentences,
  specific, load-bearing-first) is identical.
- **§4 Mission state.** Where this work sits in its pipeline. Not the pipeline
  DAG itself (that's §11) — the narrative status.
- **§5 Locked design decisions.** Each LOCK gets a line: decision + the
  operator's wording (when applicable) + rationale.
- **§6 Open L-questions.** Numbered Q-list with researcher recommendations. OR
  "NONE: all locked per <evidence>" with the evidence cited.
- **§7 Wire contracts.** Durable technical reference — types, function
  signatures, struct field lists, file:line cites. Cut from the live tree at
  §2's cut-point SHA. **Format:** use fenced code blocks for type signatures and
  struct fields; use inline `file:line` citations anchored to §2's cut-point SHA
  so future-you can `git show <SHA>:<file>` to reproduce.
- **§8 Capability matrix.** Row-by-row table when work fans out across N call
  sites / migration surfaces / per-symbol concerns. **OMIT criterion:** OMIT
  when work is single-call-site or single-surface. **REQUIRED criterion:**
  required when the session covered changes across ≥2 independent call sites /
  migration surfaces / per-symbol concerns. When in doubt, include — a one-row
  table is cheaper than a missing one.
- **§9 Design inventory.** Locked taxonomy: entanglement classes, pattern
  catalogue, anti-patterns. **OMIT criterion:** OMIT when the work hasn't yet
  developed a stable design grammar. **REQUIRED criterion:** required when ≥3
  named classes or patterns recur in the session's decisions.
- **§10 Cycle history.** Review cycles run, findings (BLOCKING / IMPORTANT /
  MINOR counts), fold record, verify-before-fold spot-checks. **OMIT
  criterion:** OMIT when the snapshot is written before any review cycle has
  run. **REQUIRED criterion:** required after the first dual-review cycle
  closes.
- **§11 Pipeline state.** DAG of artifacts (brainstorm → plan → impl → review)
  with current cursor position. ASCII tree or table.
- **§12 Pre-restart artifacts.** Manifest table: each durable artifact's path +
  status. Lets restart-you spot-check all artifacts exist before acting.
- **§13 Anticipated Q&A.** Pre-answer questions restart-you or downstream
  implementer will ask. Format: Q (bold) + A (short). Answers cite live code so
  downstream agents don't re-derive.
- **§14 References.** Load-bearing index: bd IDs (with one-line state), commit
  anchors (with SHA + one-line claim), memory keys (with rationale for
  relevance), file paths grouped by purpose, critical message IDs (for
  transcript reconstruction).
- **§15 Honest unknowns.** List facts you suspect changed during the session OR
  were never confirmed. Future-you must NOT carry these forward as truth until
  verified.
- **§16 Restart-you's immediate next actions.** Numbered. Step 1 actionable from
  cold start.

## Step 3 — Write the continuation directly to your restart file

Use your Write tool to save the composed continuation to:

```text
${REPO}/.thrum/restart/${AGENT}.md
```

`thrum prime` will auto-inject this file at next session start (whether wake
comes from `thrum tmux restart` or `thrum tmux create`). No bash heredoc or
`cat <<EOF` redirection is needed — write the file directly.

Variants that have a verify step (`/thrum:compact`, `/thrum:restart`) mint a `SNAPSHOT_PATH` and
`SNAPSHOT_NONCE` in their own Step 3 PREP block: write to exactly that path, end
the file with `<!-- snapshot-nonce: <nonce> -->`, and record both for the verify
block. The sleep variants have no verify block and need no nonce.

After writing, return control to your variant skill (`/thrum:restart` or `/thrum:sleep`) for the terminal action.
