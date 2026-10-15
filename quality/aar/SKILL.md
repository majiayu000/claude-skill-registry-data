---
name: aar
description: Generate an After Action Report with Base120 references and receipts.
version: 0.1.2
execution-mode: advisory
argument-hint: "\"<OPERATION>\" [classification]"
category: fleet-ops
status: candidate
---

> **Finalize shortcut**: After writing the AAR file, run
> `aar-finalize <aar-file.md>` to validate required sections and post the
> mandatory SITREP to the bus in one command. Add `--dry-run` to validate
> without posting. Skips posting if 0 Improves and 0 Recommendations
> (per the Bus: N exception rule). Guards against re-posting if footer
> already says `Bus: Y`.
# AAR Command

Generate a standardized After Action Report for a completed operation, session, or incident.

## Working Directory

Run all `git`, `gh`, `pytest`, and `rg` commands from the fleet repo root (`~/.agents` or the active worktree equivalent). Never assume a package-relative CWD. (The prior canonical repo `hummbl-governance` is archived; `~/.agents` is the live fleet repo on agent-node.)

## Usage

```bash
[aar]                           # AAR for current session activity
[aar] "<OPERATION>"             # AAR for a named operation
[aar] "<OPERATION>" "INTERNAL"  # AAR with classification label
```

## AAR vs SITREP

| | SITREP | AAR |
|---|--------|-----|
| **When** | During or at checkpoint | After completion |
| **Focus** | Current state + next steps | What happened + lessons |
| **Tone** | Forward-looking | Retrospective |
| **Audience** | Operational (what do we do next?) | Institutional (what did we learn?) |

Use SITREP during operations. Use AAR after.

## Required Sections

1. **Mission & Intent** (P6: Point-of-View Anchoring) -- What were we trying to do?
2. **Chronology** (RE17: Versioning & Diff) -- What actually happened, in order?
3. **Outcome vs Plan** (IN17: Counterfactual Negation) -- How did results compare to intent?
4. **Root Causes** (DE1: Root Cause Analysis) -- Why did deviations occur?
5. **Sustains** (RE16: Retrospective -> Prospective Loop) -- What worked well? Keep doing it.
6. **Improves** (IN20: Antigoals & Anti-Patterns Catalog) -- What failed or was suboptimal?
7. **Recommendations** (DE7: Pareto Decomposition) -- Prioritized changes for next time.

## Constraints

- DO NOT fabricate metrics, counts, commit hashes, or file paths. Verify before citing.
- DO NOT include Base120 codes unless that transformation was actually applied in the analysis.
- DO NOT write an AAR if no operation occurred -- report "no activity to review" instead.
- DO NOT editorialize or soften failures. AARs are blame-free but fact-strict.
- Mark inferred or estimated information with `[inferred]`.
- **Causal claims especially**: any statement of the form "A caused B", "hook X did Y", "the push triggered Z" MUST be verified against source (config file, hook body, git reflog) OR marked `[unverified]`. If you cannot verify within the AAR turn, write the observation without a cause: "HEAD changed between push and log; cause unknown — investigate next op." An unverified cause propagates as false fact to the next session. (Origin: PR #498 AAR claimed a branch-switch hook that did not exist; falsified in PR #499.)
- Every claim in Chronology and Outcome must have a receipt: command output, commit hash, file path, or log line.
- Sustains and Improves MUST be roughly balanced. If everything went well, dig harder for improves. If everything failed, find what sustained.
- **Review requests**: If the AAR covers a code review, the review request MUST include a non-empty diff. A review with an empty `<diff></diff>` forces the reviewer to reverse-engineer changes from git history, which is slow and error-prone. Flag this as an `Improves` if encountered. (Origin: principal-engineer review, 2026-06-15 — empty diff forced manual archaeology of commits `3152df7` and `f01804b`.)
- **Failed-lane incident check**: If the AAR covers a BETS run or any multi-lane evaluation where a lane failed before a re-run, the AAR MUST verify whether the failed lane caused real side-effects on the target system. A re-run that passes does not undo damage from the first run. Check the target system state explicitly and report any incidents. (Origin: 2026-09-14 — first BETS run sent `taskkill /f /im explorer.exe` to agent-node via SSH and killed `explorer.exe`; the re-run passed but the AAR reported "BETS 7/7 pass" without catching the incident.)

## Evidence Gathering

Before writing the AAR, gather receipts:

1. **Git log**: `git log --oneline -20` for commits in the operation window
2. **Bus entries**: Use `bus-global.py` to read the canonical global hub — NOT the local `_state/coordination/messages.tsv` file. The local file is not synced to the hub and reading it produces false findings (e.g., missing posts that are visible fleet-wide).
   - Recent entries: `python ~/bin/bus-global.py tail 50`
   - Search for specific terms: `python ~/bin/bus-global.py search "<term>"`
   - The canonical bus lives on hummbl-vps and is accessed exclusively through `bus-global.py`. Never `cat`, `tail`, or `Add-Content` the local `messages.tsv` as an evidence source.
3. **CI status**: `gh run list --limit 5` if CI was involved
4. **File changes**: collect both tracked and untracked scope receipts:
   - tracked committed range: `git diff --stat <before>..<after>`
   - current worktree: `git status --short --untracked-files=all`
   - unstaged tracked diff: `git diff --stat`
   - staged diff: `git diff --cached --stat`
   - untracked artifact sizes/counts: `git status --short --untracked-files=all | grep '^??'` plus `wc -l <file>` or `find <dir> -type f | wc -l` for material new files/dirs
5. **Test results**: Any test runs during the operation

DO NOT skip evidence gathering. An AAR without receipts is fiction.

## Output Format

```
AAR: <operation> | <classification> | <YYYYMMDD-HHMMZ> | <author>
═══════════════════════════════════════════════════════════════════

## 1. Mission & Intent (P6: Point-of-View Anchoring)
- **Objective**: <what we set out to do>
- **Success criteria**: <how we would know it worked>
- **Constraints**: <time, scope, resource limits>

## 2. Chronology (RE17: Versioning & Diff)
| Time/Commit | Action | Result |
|-------------|--------|--------|
| <hash/time> | <what was done> | <outcome> |

## 3. Outcome vs Plan (IN17: Counterfactual Negation)
- **Planned**: <what should have happened>
- **Actual**: <what did happen>
- **Delta**: <specific deviations with receipts>

## 4. Root Causes (DE1: Root Cause Analysis)
For each deviation:
- Deviation: <what>
- Why 1: <surface cause>
- Why 2: <deeper cause>
- Why N: <root cause>

## 5. Sustains (RE16: Retrospective -> Prospective Loop)
- <thing that worked> -- evidence: <receipt>
- <thing that worked> -- evidence: <receipt>

## 6. Improves (IN20: Antigoals & Anti-Patterns Catalog)
- <thing that failed or was slow> -- evidence: <receipt>
- <thing that failed or was slow> -- evidence: <receipt>

## 7. Recommendations (DE7: Pareto Decomposition)
1. **[HIGH]** <action> -- addresses: <which improve>
2. **[MED]** <action> -- addresses: <which improve>
3. **[LOW]** <action> -- addresses: <which improve>

---
Base120 Applied: <comma-separated codes actually used>
Evidence: <artifact paths, commit ranges, or [none]>
Bus: <bus entry posted? Y/N>
```

## Bus Integration (mandatory unless purely advisory)

Every AAR with actionable findings (Improves >0 or Recommendations >0) **MUST** post a SITREP summary to the coordination bus before the run completes. The footer line `Bus: Y/N` is not optional for these AARs — it must be `Y`.

The reason is fleet visibility: most of an AAR's value is in the lessons-learned, and lessons-learned that don't reach the other agents teach no one. An AAR with Improves but `Bus: N` keeps the operator informed and leaves the fleet blind to a known failure mode.

Exception — `Bus: N` is acceptable only when ALL of:
- the AAR has zero Improves and zero Recommendations (purely a "what worked" record), AND
- the operation is fully internal to the operator's scope (no other agent or human depends on the receipts)

Posting form (canonical identity, no parenthetical, host tag first in message):

```
<timestamp_utc>	<canonical-identity>	all	SITREP	host=<machine> AAR: <operation> -- <1-line key finding> + <1-line top recommendation>
```

`<machine>` MUST be one of `workstation`, `delta`, `remote-node`, `remote-node`, `hummbl-vps`, `huxley`, `remote-node`, or `unknown`. Before
posting, validate that the message body begins with:

```text
host=(workstation|delta|remote-node|remote-node|hummbl-vps|huxley|remote-node|unknown)
```

If the bus accepts a post but emits a host-tag warning, post one corrected
SITREP immediately and reference the malformed entry in the AAR evidence.
Do not claim `Bus: Y` from a receipt that failed machine-tag validation.

If the AAR's STATUS for the operation has already been posted earlier in the session and contains the same lessons-learned content, the AAR may reference that timestamp in `Bus: Y (covered by STATUS at <ts>)` instead of duplicating. This is the only legitimate way to claim `Y` without a fresh post.

Origin: 2026-04-30 — codex AAR on bus tooling chose `Bus: N`; the 4 actionable recommendations (hummbl-governance/bus scope) were not visible to fleet until a different session surfaced them. Operator agreed convention should be mandatory.

## Related

- SITREP: `[sitrep]` (during operations)
- CAES: `[caes]` (compliance auditing)
- Vernacular: `docs/VERNACULAR_QUICK_REFERENCE.md`
- Base120 Reference: `memory/base120-reference.md`
