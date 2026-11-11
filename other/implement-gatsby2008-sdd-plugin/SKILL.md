---
name: implement
description: Implement focused changes inline using spec + rules state, with strict Open Questions gate.
allowed-tools: Read, Edit, Write, Bash(cat .specwork/_spec/*), Bash(cat .specwork/_state/*), Bash(cat .specwork/_plan/*), Bash(cat .specwork/_progress/*), Bash(find src:*), Bash(grep:*), Bash(git rev-parse:*), Bash(git diff:*), Bash(git status:*), Bash(python3:*), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py:*), Bash(date:*), Bash(mkdir .specwork/_progress:*)
---

# Implement

Implement the next focused change from the spec using bounded context and minimal diffs.

`REF` below means `${CLAUDE_PLUGIN_ROOT}/skills/implement/REFERENCE.md`. Read a `REF §` section only when its step needs it — abort messages only when a gate fails.

---

## Central Rules

1. Never silently guess business behavior; business ambiguity becomes an Open Question.
2. Unresolved Open Questions block implementation.
3. Missing `spec.md` blocks implementation completely.
4. A stale plan (built against an older spec) blocks implementation — re-run `/sdd:plan` to regenerate, or delete the plan file to fall back to discovery.
5. Read `rules.json` when available and apply it.
6. Read `implementation-cache.json` when available, reuse it before discovery, and update it at the end.
7. Avoid broad repository scans; no repo-wide scan by default.
8. Load only spec + rules + cache + targeted files. Target files must be known or confirmed before editing.
9. Use bounded retries when fixing implementation or test failures.
10. Escalate persistent failures instead of retrying indefinitely; infrastructure/environment failures never trigger broad speculative rewrites.
11. If `SDD_NON_INTERACTIVE=1`, do not ask for conversational confirmations; continue automatically between steps.

---

## Execution Modes

Only lightweight modes are supported — no full mode:

- `focused`: localized change, usually <= 3 files
- `batch`: several sequential focused steps with shared context reuse

---

## Step 0 — Pipeline Precondition Gate (STRICT)

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py precheck
```

Then rehydrate non-interactive mode from pipeline state:

```bash
if [ "${SDD_NON_INTERACTIVE:-0}" != "1" ]; then
  SLUG="$(python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py resolve-slug)"
  SDD_MODE="$(python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py non-interactive "$SLUG" 2>/dev/null || echo 0)"
  [ "$SDD_MODE" = "1" ] && export SDD_NON_INTERACTIVE=1
fi
```

If `precheck` exits non-zero, abort with no writes (REF § Abort messages).

In non-interactive mode the only allowed pauses are: the Open Questions gate, the plan gates (Steps 3.4 and 3.5), and a command/runtime failure that prevents safe continuation.

---

## Step 1 — Detect Branch

```bash
git rev-parse --abbrev-ref HEAD
```

Derive `slug` from the branch with `python3 ${CLAUDE_PLUGIN_ROOT}/lib/slug.py` (field `slug`) — the same helper `/sdd:start` and `/sdd:resync` use; never hand-craft it. It must equal the file prefix under `.specwork/_state/` (REF § Slug examples).

---

## Step 2 — Load Spec, Rules, and Implementation Cache

```bash
cat .specwork/_spec/<slug>-spec.md
cat .specwork/_state/<slug>-rules.json
cat .specwork/_state/<slug>-implementation-cache.json
```

If the canonical `spec.md` drafted by `/sdd:spec` is missing, abort (REF § Abort messages). Do not continue from `rules.json` or the cache alone, do not reconstruct the spec from prior conversation or code, and do not proceed on context remembered from an earlier run.

- `rules.json` missing → continue spec-only and ask for clarification on ambiguous business rules.
- Cache missing → continue and create it at the end of this run.

Extract from the spec: summary, scope, behavior (with its `B<n>` ids, when present), implementation context, expected change scope, safe constraints.

Apply `rules.json` as hard constraints — it is the compact, feature-scoped checklist for this run. It is distilled (no tables, lifecycles, or other context): the project rule files under `.claude/rules/` (and any `.claude/service-rules.md`) are already loaded in session context — consult them for detail the checklist cannot carry. Do not go hunting other docs beyond these.

Treat the cache as a fast index for this feature (fields: REF § Cache fields). It is supplemental only and never replaces the spec as the canonical implementation contract.

---

## Step 3 — Validate Open Questions (STRICT GATE)

Do not re-implement this check inline — call the shared gate. It checks the `## Open Questions` section of the spec and, when it exists, the plan:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py check-oqs "$SLUG"
```

It prints each blocking file (`--- <path>`) with its unresolved `- [ ]` items. On non-zero exit, abort with no writes, naming which file blocks (REF § Abort messages).

- A single unresolved item in either file blocks; spec OQs are resolved in the spec, plan OQs in the plan (REF § Gate rationale).
- Do not implement while Open Questions are unresolved, do not infer answers, do not "pick the most reasonable option", do not partially implement around unresolved business behavior.

---

## Step 3.4 — Plan Required Gate (STRICT, high-risk only)

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py check-plan-required <slug>
```

On non-zero exit, abort with no writes (REF § Abort messages).

- Fires only when `.specwork/_state/<slug>-path.json` marks the tier **high-risk** (`plan_required`) and the plan is **absent**. A tier forced with `/sdd:spec --tier` wins over the automatic one, in both directions. No `path.json`, or any other tier → passes silently (REF § Gate rationale).
- Once the plan exists, this gate passes and Step 3.5 takes over.
- The gate never writes and never runs `/sdd:plan` for the user; it only blocks and instructs.

---

## Step 3.5 — Plan Staleness Gate (STRICT, only when plan exists)

Skip when `.specwork/_plan/<slug>-plan.md` does not exist (Step 4 falls back to discovery).

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py check-staleness <slug>
```

On non-zero exit, abort with no writes (REF § Abort messages).

- Strict: never silently fall back to discovery when a stale plan exists — the user must re-plan or remove the plan.
- Fires when the spec content changed since `/sdd:plan` stamped its fingerprint, whoever edited it; a `touch` or whitespace-only save does not fire. Legacy plans without a fingerprint fall back to mtime (REF § Gate rationale).
- The gate never deletes or modifies `plan.md`.

---

## Step 4 — Identify Target Files

**Plan-first path** (plan exists): the plan's `## Target Files` table is the source of truth. Treat the plan as **binding but living**:

- Use the listed files as the primary target set for this pass.
- If you confirm during Step 5 that a file **not** in the plan must change, append a row to `## Target Files` and to the matching cache arrays before editing it, and log "Plan updated: +<N> file(s)" in the Step 8 summary.
- Never silently touch a file that is not in the plan **and** belongs on its `## Out-of-Plan Files` list. Stop and report instead.

**Discovery-fallback path** (no plan): use spec context first, then the cache, before any discovery command. Prefer explicit file paths over package-level discovery; use only targeted `find`/`grep`, never whole-repo scans unless the user explicitly approves (REF § Discovery guidance). If targets are still unclear, ask exactly one focused question:

```text
Which files should this step modify?
```

---

## Step 5 — Implement (Bounded)

- read only required files/sections; for large files, use targeted reads (`grep`, line ranges) before editing
- apply the minimal focused change; prefer small diffs over architectural rewrites
- avoid unrelated refactors, unrelated directories, and speculative fixes outside the spec
- do not modify unrelated production code to satisfy tests
- do not introduce new dependencies unless explicitly requested
- preserve existing patterns and naming conventions

If the implementation reveals ambiguity: append it to the spec as `- [ ] <question>`, **stop immediately** (do not guess, do not partially implement), and print the notice from REF § Abort messages. The spec is the persistent record — do not rely on conversation context to carry the answer.

If a required change conflicts with `rules.json`, stop and report the conflict.

---

## Step 6 — Test Coverage

Create or update tests for every changed behavior — focused on the spec's behavior, not excessive:

- **New classes, enums, or DTOs**: a dedicated unit test when there is testable behavior
- **Changed logic**: a focused regression test close to the modified behavior
- **New endpoints**: add or update an integration test when appropriate
- **Bug fixes**: a regression test that fails before the fix and passes after
- No testable surface → state the reason explicitly before proceeding

**Tag tests with the Behavior they cover.** When `## Behavior` items carry ids (`**B1**`, …), mark each test you write or change with the id(s) it verifies, qualified by the slug, in a comment or display name: `// spec: <slug>#B2`, `# spec: <slug>#B1, B3` (the slug carries to the ids after it), `@DisplayName("spec: <slug>#B2 - rejects null applicationId")`. Ids are only unique within one spec; the slug keeps the tag meaningful after `.specwork/` is gone. `/sdd:commit` reads these tags from the lines added on this branch and reports any Behavior without one — a token-free conformance check. Skip tagging when the spec has no ids.

### Run individual tests

Optionally run only the tests you created or modified (commands: REF § Running individual tests).

- Pass → continue. Fail → classify before any fix. Build tooling unavailable → skip silently and note it in the summary.
- Never run the full test suite unless explicitly requested.
- Never rewrite unrelated infrastructure or modify unrelated production code to make a test pass.
- Never change expected assertions unless the spec explicitly requires the behavior change.

### Failure decision matrix

Classify every failure with REF § Failure decision matrix before attempting a fix. Fix only direct or clearly related failures; escalate immediately for infrastructure, environmental, unrelated, or ambiguous ones.

### Retry tracking

Only direct or related failures are eligible for retry. Maximum attempts per failing area:

- Direct implementation error: 2
- Related test setup error: 1
- Infrastructure/environmental/unrelated/ambiguous: 0 — escalate immediately

Count a retry only when the same failing area persists after a fix attempt; report unrelated new failures separately (REF § Retry and escalation detail).

### Escalation policy

When the same failing area persists past its budget: **STOP**, keep the working tree as-is, and print the escalation report (six fields and the do-not list: REF § Retry and escalation detail). Human escalation is a valid and preferred outcome.

**Persisting the escalation is mandatory.** Every time this policy triggers, append a dated entry to `.specwork/_progress/escalations.md` (REF § Escalation entry format):

- `mkdir -p .specwork/_progress`; create the file if missing.
- Append, separated by a blank line. Never overwrite or delete prior entries — the file is append-only within the feature.
- Date prefix from `date +%Y-%m-%d`.

---

## Step 7 — Update Implementation Cache

Add facts discovered in this run to `.specwork/_state/<slug>-implementation-cache.json` (shape: REF § Cache fields): validated facts only, deduplicated, short and searchable; never remove prior entries unless clearly invalid. Best-effort — never blocks implementation. One call:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py merge-cache <slug> '{"repositories":["LeadsRequestRepository"],"patterns":["fallback lookup uses person + collateral identity"]}'
```

---

## Step 7.5 — Simplicity Checkpoint (advisory, non-mutating)

Skip for trivial changes (a rename, a copy, a one-line config tweak); run it when the change carried real logic (`focused` tier and above). Take one non-mutating pass over the diff and ask *is there a simpler way?* (REF § Simplicity checklist).

- Found one → one advisory line in the Step 8 summary (`Simpler alternative: …`). Never apply it silently; the developer decides.
- Nothing stands out → say so in one line. Do not manufacture a suggestion.
- Never change observed behavior; never reopen a resolved Open Question. No artifacts, no gate.

---

## Step 8 — Ready for Next Step

Assign a final risk level from the observed signals (REF § Risk classification table) — not from file count alone — and print the next phase from REF § Recommendation logic using REF § Output templates (or the escalation block if Step 6 escalated).

- The printed phase must match the risk level, never a lower one. **HIGH always surfaces `/sdd:test-design`**, even when inline tests exist — it designs only the missing cases.
- The recommendation is advisory to the developer. Apply contextual judgment only *within* the matched phase. When more implementation steps remain, recommend `/sdd:implement`.
- Do not hide failed tests behind a normal "done" message.

Related skills: REF § Related skills.
