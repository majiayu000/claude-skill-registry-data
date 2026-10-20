---
name: chore
owner: baseline
description: Workflow track for tasks that need no TDD — documentation edits, governance count bumps, vendored-skill content updates, configuration tweaks, formatting, typo fixes, dependency bumps where no project code changes. Skips `/scenario` and `/implement` (no failing test to drive) and runs the work directly. `archive`, `memory-sync`, `/grant-commit`, and `/commit` remain mandatory. `verify`, `simplify`, `integrate`, and `document` are conditional — required when the diff hits one of the listed triggers, optional otherwise. `verify` is skipped only when the diff is pure-docs/prose AND `project.json → test.kind` is `behavior` (absent/invalid `test.kind` → `structural` → verify runs). Chore is a stripped-down pipeline, not a bypass; never silently skip a conditional phase whose triggers apply.
argument-hint: "<one-line description of the chore>"
---

# chore — workflow for tasks that don't need TDD

This skill runs a stripped-down workflow for tasks where nothing is meaningfully driven by a failing test. The full `/tdd` RALPH cycle is theatre when the change is "fix a typo", "update a count", "remap a vendored path", or "tighten a description" — there is no test that catches a typo, and the project audit (or a downstream lint) serves as the regression check.

The chore workflow exists so this class of work can move with the **right** ceremony — real verification of "did I break anything" without the scenario+implement loop, and conditional simplify/integrate/document passes when the diff actually warrants them.

## Definition: when is a task a chore?

A task is a **chore** if and only if **it has no code changes that need TDD**. Concretely, a chore is anything from this list:

- Documentation edits — `README.md`, `CLAUDE.md` prose, `docs/init/seed.md` prose, governance count refreshes, skill SKILL.md descriptions, reference docs.
- Vendored-skill content updates — path remaps (e.g. `.agents/` → `.claude/skills/`), count refreshes, "Related Skills" annotations, license-required modification notices.
- Configuration tweaks — `project.json`, `.mcp.json`, `settings.json` edits whose behavioural effect is config-driven (a new declaration, a flipped flag) rather than code-driven.
- Formatting / typo fixes anywhere in the repo.
- Dependency bumps where no project code changes alongside.
- Skill consolidation moves — collapsing a single-consumer skill into its consumer's `references/` directory.
- File renames or path remaps with no behavioural change.

A task is **not a chore** if any of:

- New runtime behaviour is being added — the failing test is the only way to drive it correctly.
- A bug is being fixed and regressing to that bug would be undetectable without a test — the fix SHALL come with a test.
- A refactor changes behaviour under specific inputs — TDD captures the boundary.

The classification rule is: *if there is no failing test that should exist for this work, it is a chore. Otherwise it is `/tdd` (or higher).*

`/triage` decides the classification; this skill confirms it on entry.

## Prereq

`.claude/state/workflow.json` exists with `track_id == "chore"` (post-§18; legacy `entry_phase == "chore"` accepted for pre-§18 in-flight workflows). If the prereq is not met, refuse and surface the mismatch.

## Phase shape

### Mandatory phases (always run)

1. **Edit** — apply the change directly. No `/scenario`, no `/implement` — there is no failing test to drive.
2. **`archive`** — empty bundle is fine; `/commit`'s prereq requires `archive` in `completed`.
3. **`memory-sync`** — Phase 10.6. Empty pending is fine (fast-path runs Step 0 sweeps and short-circuits). `/commit`'s prereq requires `memory-sync` in `completed`.
4. **`/grant-commit` then `/commit`** — user-required consent + commit. Same as every other workflow.

### Resolving the track's `internal_phases[]` (MANDATORY — read before the triggers)

The `chore` track declares `internal_phases: ["verify", "simplify", "security", "integrate", "document"]` in `.claude/workflows.jsonl`. Those are the phases this skill may run **without a DAG node**. `/triage`'s `deriveExceptions` deliberately does **not** except them: at triage time the diff does not exist, so a conditional cannot be pre-judged.

That makes **you** the resolver. By the end of this skill, every phase in `internal_phases[]` SHALL sit in exactly ONE of:

- **`completed`** — its trigger fired and the phase ran; or
- **`exceptions`** — its trigger did not fire, plus an `auto_skipped[]` provenance row: `{phase, reason, oracle: "chore-conditional"}`.

**No internal phase may be left in neither set.** That limbo state is not cosmetic: `integrate`'s prereq requires `security` in `completed` OR `exceptions`, so an unresolved `security` makes `integrate` structurally unrunnable — and it fails on the *common* case (a chore with no sensitive surface), while a chore that happens to touch `.claude/hooks/**` passes. Resolve every one, every time.

Writing a runtime-skipped conditional into `exceptions` is **recording a decision this track was already authorised to make** (Art. IV sanctions chore's conditional routing), not a new bypass power. The `auto_skipped[]` row is what makes it auditable.

### Conditional phases (required when triggers apply, optional otherwise)

5. **`verify`** — run the project test command and stamp `.claude/state/last_test_result` (the verdict is binding; `verify_pass_guard` reads this file). **Skipped only** when **both** hold:
   - The diff is **pure-docs/prose only** — every changed path is documentation/prose (e.g. `**/*.md`, `docs/**`) and **no** path is code/config/script (`**/*.{mjs,js,cjs,ts,tsx,json,sh,py,yml,yaml}`, hook scripts, `settings.json`, `project.json`, etc.). Reuse the same diff inspection the triggers below use.
   - `project.json → test.kind` is `behavior` — a code-only suite (e.g. a unit-test runner) that cannot exercise documentation.

   Otherwise **run verify**. Specifically: any code/config/script path in the diff runs verify **regardless of `test.kind`**; and when `test.kind` is absent, invalid, or `structural` it resolves to `structural`, so verify runs even for a pure-docs diff (a structural/whole-repo check — e.g. the baseline audit — genuinely verifies docs). A `FAIL` from a verify that ran means stop, surface, and route the user to `/triage` for a proper bugfix track — chore does not loop. When verify is skipped, record the skip and its reason (pure-docs diff + `test.kind: behavior`) in the end-of-chore summary.
6. **`simplify`** — required when **any** of:
   - Diff exceeds ~30 lines OR touches more than 3 files.
   - The change includes refactor-like moves (renames, restructuring, file relocations).
   - The chore creates duplication that future cleanup will need to consolidate.
   - More than one file in the diff would benefit from a reuse / structure pass.
   Otherwise skip — and say so in your end-of-chore summary so the choice is auditable.

7. **`integrate`** — required when **any** of:
   - The diff touches the test surface — test command, fixtures, hook scripts, `settings.json` hook wiring, `project.json → test/lint` keys.
   - The diff alters MCP server declarations or runtime config that affects how the harness behaves.
   - The diff could plausibly break unrelated downstream phases (e.g. editing an audit script's `EXPECTED_*` set).
   Otherwise the `verify` stamp (when verify ran) is sufficient — note the skip in the summary.

7.5. **`security`** — required when the diff intersects `project.json → security.sensitive_globs` (`.claude/hooks/**`, `.claude/commands/**`, `src/cli/**`, `bin/**`, `**/auth/**`, `**/*.env*`). Decide it mechanically, not by eye:

   ```
   node .claude/skills/chore/sensitive-surface.mjs
   ```

   It prints `{sensitive, matched}` and always exits 0 (advisory — a helper that can block a commit will eventually block the wrong one). `sensitive: true` → run `Skill(security)` and append `security` to `completed`. `sensitive: false` → skip it, append `security` to `exceptions`, and record the `auto_skipped[]` row.

   Chore previously had no security node and no security trigger, so a chore touching `.claude/hooks/**` shipped with **no security review by construction** — while the `rightsize-gate` was deliberately built to never skip security. This trigger closes that gap. A sensitive-surface chore is not a bypass lane.

8. **`document`** — required when **any** of:
   - User-facing prose changes — `README.md`, `CLAUDE.md` prose, `docs/init/seed.md` prose, skill `SKILL.md` `description:` lines, public-facing reference docs.
   - Counts or inventories change — skill count, hook count, command count, MCP server count, alternate-track count.
   - New conventions are introduced — a new helper file, a new reference doc, a new directory.
   - The `seed.md §16` follow-ups list needs an entry resolved or added.
   - The chore touches `src/` templates (the templates are user-facing once `npx @friedbotstudio/create-baseline` runs).
   Otherwise skip — note in the summary.

If a conditional phase is required, run it **before** `/grant-commit`. If you skip one, the end-of-chore summary SHALL state which conditional phases were skipped and why. Silent skips are not allowed.

## Steps

1. Read `.claude/state/workflow.json`. Confirm `track_id == "chore"` (post-§18) OR `entry_phase == "chore"` (legacy pre-§18). If neither, stop and surface the mismatch — the user reached this skill without the correct triage classification.
2. Restate the intended edits inline: file paths, brief description per file, estimated total diff size. Confirm with the user if anything is ambiguous.
3. Apply the edits via `Edit` / `MultiEdit` / `Write`. Honour the engineering rules from CLAUDE.md Article VI (no stubs, no commented-out code, no `TODO` / `FIXME` / `HACK` / `XXX`).
4. **Apply the conditional `verify` trigger, and run + stamp the binding verdict when it fires (inlined verify).** Classify the diff (pure-docs/prose vs touches code/config/script) and read `.claude/project.json → test.kind` (absent or invalid → `structural`). **Skip verify** only when the diff is pure-docs/prose only **and** `test.kind` is `behavior`; in that case do **not** write `.claude/state/last_test_result`, and record the skip + reason in the end-of-chore summary. **Otherwise run verify**: per `.claude/skills/verify/SKILL.md` (the contract doc) read `.claude/project.json → test.cmd`; run via Bash from project root (capture stdout, stderr, exit code; no retry); apply verdict rules (`PASS` iff exit 0 AND at least one test executed AND no failed/errored test; otherwise `FAIL`); atomically write `.claude/state/last_test_result` with the canonical four-line format. The `verify_pass_guard` hook reads line 1 as the binding verdict. If the verdict is `FAIL`, stop — the user investigates; chore does not loop. Write `.claude/state/harness_state` with `state: "yielded"` and `reason: "chore verify FAIL"` so the Stop hook stays silent.
5. Walk the remaining conditional triggers (`simplify` / `integrate` / `document`) in order. For each:
   - **Required** → invoke the phase skill and append it to `workflow.json → completed`.
   - **Skipped** → record the rationale in your end-of-chore summary; do not append to `completed`.
6. Invoke `Skill(archive)` — mandatory.
6.5. Invoke `Skill(memory-sync)` — mandatory (Phase 10.6). Runs Step 0 canonical sweeps and, if `_pending.md` is non-empty, full triage. On empty pending the fast-path returns success in ≤ 3 sweep.mjs invocations.
7. Append `"chore"`, `"archive"`, `"memory-sync"`, and any conditional phases that ran to `workflow.json → completed`. Update `updated_at` to the current epoch.
8. **Marker op FIRST, then write `harness_state`, then emit end-of-chore summary.** On `state: "continue"` (more phases follow, e.g. archive is still pending): `echo "<slug>" > .claude/state/.harness_active` to refresh the active marker, then write `.claude/state/harness_state` with `{state: "continue", slug, reason}`. On `state: "done"` (archive just appended and no further phases remain): `rm -f .claude/state/.harness_active`, then write `harness_state` with `{state: "done", slug, reason}`. The state file carries exactly three keys; no `written_at`, no `tick_count`. Then tell the user:
   - "Chore green."
   - Files changed.
   - Conditional phases run (and why).
   - Conditional phases skipped (and why).
   - "Run `/grant-commit`, then `/commit` to finalize." *(omit this line on non-git projects where commit is excepted; instead say "Workflow ends after `/archive` on this non-git project.")*

## Constraints

- The `verify` stamp is binding **when verify runs**. `verify_pass_guard` reads `.claude/state/last_test_result`; that file is the truth. `verify` is skipped only when the diff is pure-docs/prose **and** `project.json → test.kind` is `behavior` (absent/invalid `test.kind` → `structural` → verify runs); a skipped verify writes no stamp and is recorded in the end-of-chore summary.
- No subagent delegation — Article II applies to chore the same as every other phase skill.
- A `FAIL` from `verify` is non-recoverable inside this skill — chore does not loop. If the audit reveals a real bug, the user runs `/triage` for a proper bugfix track.
- Conditional phases are *conditional*, not *forbidden*. **If in doubt, run them.** The cost of running a `simplify` or `document` pass that turned out unnecessary is small; the cost of skipping one whose triggers actually applied is shipping drift.
- The end-of-chore summary SHALL document every conditional-phase skip. Silent skips defeat the auditability the chore workflow is designed for.
- Chore is **not** a bypass for the canonical workflow's quality gates. It is a stripped-down ordering of the same gates, with the test-first phases removed because there is nothing to test-first.
