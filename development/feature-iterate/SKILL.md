---
name: feature-iterate
description: Iterate on a shipped AICP feature — refine based on operator feedback, observed runtime behavior, or gaps discovered in use. Distinct from feature-implement (first-pass build) and feature-review (final sign-off); this skill is the post-ship refinement lifecycle. Every iteration is scoped, tested, and documented as a distinct delta, not a quiet patch. Loads when the operator says "iterate on X" / "refine the X feature" / "X needs tuning based on how it's actually used" / "feedback on feature X suggests Y" / "follow-up on the X that shipped".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# feature-iterate

Execute the ITERATE stage of a feature-development task — refine a
shipped feature based on post-ship signal (operator feedback, telemetry,
bug reports, observed workflow friction). Distinct from the first-pass
build (`feature-implement`) and from bug-fixes (handle inline); iteration
is a deliberate refinement cycle.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: "iterate on X", "refine X", "tune X", "follow-up on X"
- **Post-ship signal**: "feedback on X suggests Y", "metrics show X is
  slow / wrong / confusing", "operator reports X doesn't cover Z"
- **Scope expansion**: "X mostly works but doesn't handle <edge case>",
  "X should also support <extension>"
- **UX refinement**: "the X output is hard to read", "X error messages
  aren't actionable"

Do NOT load when:

- The feature is a first-pass build — load `feature-implement`
- The feature is pre-ship / being designed — load `feature-plan`
- The concern is a bug (incorrect behavior, not refinement) — fix inline
  or load `ops-incident`
- The concern is rewriting the feature — that's closer to `evolve-migrate`
  or `refactor-architecture`

## Operations

### Operation 1 — Capture the iteration trigger

**When**: operator raises an iteration need; ground the work before
touching code.

**Process**:

1. Name the trigger in one sentence — WHO reported WHAT, or WHICH metric
   showed WHAT. Write it down (in the task file, in a comment, in the
   commit message draft).
2. Distinguish iteration from bug fix:
   - **Iteration**: feature works correctly but could be better
     (faster / clearer / broader scope)
   - **Bug**: feature works incorrectly against its own spec — handle
     with `ops-incident` or inline fix, not this skill
3. Locate the original feature's design artifact (task file, decision
   page, commit message) if one exists — anchor the iteration against
   documented intent

**Quality bar**: every iteration has an explicit trigger sentence. "It
felt off" is not a trigger; "operator reported `--metrics --show-cost`
didn't include cache-hit cost breakdown" is.

### Operation 2 — Scope the iteration delta

**When**: trigger is captured; decide what this iteration covers and
what it doesn't.

**Process**:

1. Write a 3-5 bullet delta description:
   - What the current feature does
   - What the iteration adds / changes / removes
   - What's explicitly OUT of scope for this iteration
2. If the iteration touches more than ~3 files or adds a new config key,
   author a small decision page (`wiki/decisions/00_inbox/iterate-<feature>-
   <aspect>.md`) — iterations accumulate invisible complexity without
   documentation
3. Get operator confirmation on the scope before implementing

**Quality bar**: NEVER expand scope mid-iteration. If a second concern
surfaces, write it down as a follow-up iteration; don't bundle.

### Operation 3 — Implement the iteration

**When**: scope confirmed.

**Process**:

1. Locate the feature surface:
   - CLI flag → `aicp/cli/main.py` or subcommand module
   - Router change → `aicp/core/router.py`
   - Backend change → `aicp/backends/<name>.py`
   - Hook change → `tools/hooks/`
   - Skill change → `.claude/skills/<name>/SKILL.md`
2. Preserve current behavior for operators who don't opt into the change
   (default-off for new toggles; existing invocations produce same output
   unless opted in)
3. Extend tests in `tests/test_<feature>.py` — the iteration's test
   ADDS cases, does not replace them (regression guard)
4. Update the feature's documentation (CLAUDE.md section, skill reference,
   `--help` text) — iterations that ship with stale docs rot fastest

**Quality bar**: regression tests for the original behavior MUST stay
green. An iteration that changes N cases should have N new tests AND
pass all pre-iteration tests unchanged.

### Operation 4 — Apply Gateway Output Contract if output changed

**When**: the iteration modifies CLI output or MCP tool return shape.

**Process**:

1. Verify the 5 contract rules apply
   (`wiki/decisions/00_inbox/aicp-cli-mcp-outputs-adopt-gateway-output-contract.md`):
   - Rule 1: Single responsibility (no bundled unrelated data)
   - Rule 2: Context branches (different paths produce different output
     with clear headers, not undifferentiated blobs)
   - Rule 3: Size ceiling (≤60 lines for CLI; trim large sub-outputs
     with `... see --detail` pointers)
   - Rule 4: Read-whole marker (explicit delimiters when output is
     long enough to risk paging truncation)
   - Rule 5: Closing NEXT line (every CLI subcommand + MCP tool return
     ends with `NEXT:` hint pointing to next action or related flag)
2. Use `_print_next()` helper (already in `aicp/cli/main.py`) for CLI
   NEXT lines; add `next:` field to MCP tool return dict

**Quality bar**: iterations that change output without honoring the
contract regress AICP's CLI/MCP hygiene.

### Operation 5 — Verify and document the iteration

**When**: implementation complete; pre-commit.

**Process**:

1. Run relevant tests: `pytest tests/test_<feature>.py -v`
2. Run ruff: `ruff check aicp/`
3. Live-verify the changed code path with a real operator-like invocation
   (NOT just passing tests — see `superpowers:verification-before-completion`)
4. Update CHANGELOG or `wiki/log/` entry with the iteration
5. Craft a conventional commit: `refactor(<area>):` or `feat(<area>):`
   with the trigger sentence as rationale

**Quality bar**: iterations without live verification ship regressions.
Passing tests confirm code correctness; operator-like invocation confirms
feature correctness.

## Gotchas

- **Detection**: agent iterates without a captured trigger sentence.
  **Rule**: always write the trigger before touching code (who / what /
  why).
  **Reasoning**: trigger-less iteration drifts into speculative scope
  creep; the trigger anchors what "done" looks like.

- **Detection**: agent bundles two unrelated iterations into one commit.
  **Rule**: one iteration = one commit (or tightly-related commit series).
  If two triggers surfaced, make two iterations.
  **Reasoning**: bundled iterations are hard to revert, hard to review,
  and hide accumulating scope.

- **Detection**: agent changes feature behavior without adding regression
  tests for the ORIGINAL behavior.
  **Rule**: the pre-iteration tests must keep passing unchanged; NEW
  tests cover the iteration delta.
  **Reasoning**: replacing tests to match new behavior loses the
  regression guard; the feature can silently regress on the old path.

- **Detection**: agent iterates on CLI output without honoring Gateway
  Output Contract.
  **Rule**: output changes trigger the 5-rule check in Operation 4.
  **Reasoning**: AICP has an adopted contract; iterations that ignore
  it reintroduce the drift the contract was meant to fix.

- **Detection**: agent iterates without updating `--help` / CLAUDE.md /
  skill doc.
  **Rule**: iteration includes documentation update in the same commit.
  **Reasoning**: documentation-lag is how features rot; operators can't
  use what they don't know exists.

- **Detection**: agent treats a bug as an iteration (or vice versa).
  **Rule**: bugs violate the feature's own spec; iterations refine a
  feature that meets its spec. Classify the work correctly before
  choosing the skill.
  **Reasoning**: treating bugs as iterations delays urgent fixes;
  treating iterations as bugs skips the scope-definition step.

## Reference exemplars

- `aicp/cli/main.py` — canonical pattern for iterating on CLI flag
  handlers (see the `_print_next` helper introduced in the Gateway
  Output Contract iteration)
- `aicp/core/router.py` — canonical pattern for iterating on routing
  logic (thresholds, failover chains)
- `wiki/decisions/00_inbox/aicp-cli-mcp-outputs-adopt-gateway-output-contract.md` —
  example of a scoped iteration decision (rules, phased rollout, evidence)
- `tests/test_*.py` — regression-plus-delta test pattern
- `wiki/log/` — iteration trail for AICP features

## Domain context

AICP features tend to have long post-ship tails — router thresholds get
tuned, profile defaults get rebalanced, MCP tool deprecation markers get
extended, hook rules get refined based on operator near-misses. Iteration
is the expected normal lifecycle, not an exception. The iteration velocity
is constrained by: (1) regression-test discipline, (2) the single-
operator reality (no second operator to catch missed cases), (3)
documentation drift.

## Related skills

| Skill | When to use |
|-------|-------------|
| `feature-document` | For SCOPING a feature before first implementation |
| `feature-plan` | For DESIGNING a feature before first implementation |
| `feature-implement` | For FIRST-PASS implementation |
| `feature-test` | For authoring tests (complements this skill's test-update step) |
| `feature-review` | For final sign-off once iteration feels complete |
| `ops-incident` | If the "iteration" is actually a bug fix |
| `evolve-migrate` | If the "iteration" is actually a rewrite |
| `quality-lint` | For style hygiene of changed files |
| `quality-debt` | For capturing deferred iteration ideas |
