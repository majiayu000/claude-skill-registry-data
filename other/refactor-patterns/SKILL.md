---
name: refactor-patterns
description: Apply design-pattern thinking to AICP refactoring — recognize when ad-hoc code is (or should be) an instance of a documented pattern, consolidate duplicate pattern-instances into a shared implementation, or contribute a new pattern to `wiki/patterns/` when one emerges organically. AICP has 5 documented patterns today (profile-as-coordination-bundle, single-active-backend-with-lru-eviction, three-permission-modes, per-backend-circuit-breaker-with-failover-chain, per-day-jsonl-dlq-with-retry-budget). Distinct from the other refactor skills (extract / split / rename / architecture) — this skill is about the PATTERN layer. Loads when the operator says "apply pattern X to Y" / "this looks like pattern X but isn't using it" / "extract a pattern from these three similar modules" / "document this as a new pattern" / "pattern-ize the circuit breaker".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# refactor-patterns

Apply pattern-thinking to a refactor — either apply an existing documented
AICP pattern to new code, consolidate several ad-hoc instances into a
shared pattern-based implementation, or promote an organically-emerged
solution into a named pattern in the wiki.

Distinct from the other refactor skills:

| Skill | Scope |
|-------|-------|
| `refactor-extract` | Pull one definition from inline code |
| `refactor-rename` | Rename a symbol consistently |
| `refactor-split` | Split one overlarge module into several |
| `refactor-architecture` | Restructure at the package level |
| `refactor-patterns` (this) | Apply or extract a design pattern across code |

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Apply existing pattern**: "apply circuit breaker pattern to backend X",
  "this should use the profile pattern", "make Y follow the single-active
  pattern"
- **Consolidate pattern instances**: "these three modules all do X the
  same ad-hoc way — extract the pattern", "DRY this up as a pattern"
- **Promote a new pattern**: "this worked well, document it as a pattern",
  "is this recurring shape worth naming?"
- **Apply pattern from second brain**: "the brain has a pattern Z — apply
  it to AICP", "how does pattern Z from the wiki map to our code?"

Do NOT load when:

- The concern is naming one function — load `refactor-extract`
- The concern is splitting a file — load `refactor-split`
- The concern is a single-module restructure without pattern content —
  load `refactor-architecture`
- The concern is adopting a library — that's `evolve-integrate`, not
  pattern-refactoring

## Operations

### Operation 1 — Identify the pattern candidate

**When**: operator raises a pattern-refactor opportunity; ground in
specifics before touching code.

**Process**:

1. Classify the situation:
   - **Case A — Apply existing pattern**: a pattern is already documented
     in `wiki/patterns/` (check via `ls wiki/patterns/01_drafts/` and
     `ls wiki/patterns/02_reviewed/`); code has an opportunity to use it
   - **Case B — Consolidate pattern instances**: multiple code sites do
     the same thing differently; time to name + unify
   - **Case C — Promote emergent pattern**: a solution that worked well
     deserves to be documented for reuse
2. List concrete code sites (file paths + line numbers). "This project
   has a pattern opportunity" is not enough — name the call sites.
3. Distinguish pattern-refactor from architectural-refactor:
   - Pattern = reusable shape of code inside a problem domain
   - Architecture = layering of modules across the package

**Quality bar**: never pattern-refactor without naming ≥2 concrete code
sites (Case A), ≥2 existing instances (Case B), or ≥1 instance that
worked well (Case C). Knowledge Evolution Standards require
≥2 instances to promote a pattern from draft to reviewed.

### Operation 2 — Case A: Apply an existing pattern

**When**: pattern doc exists; code should use it.

**Process**:

1. Read the canonical pattern doc in `wiki/patterns/01_drafts/` or
   `wiki/patterns/02_reviewed/`:
   - Note the "Implementation" section's canonical shape
   - Note the "Gotchas" section's known failure modes
   - Note the "Instances" section for existing uses
2. Compare the target code against the pattern:
   - What's ALREADY the same? (likely most of it)
   - What diverges? (the actual refactor surface)
3. Refactor the target code to conform:
   - Re-use helper functions/classes from existing pattern instances
   - Add the new instance to the pattern doc's Instances section
4. Update tests: keep existing behavior tests green; add new tests that
   exercise the pattern's guarantees (e.g., for circuit breaker, test
   the HALF_OPEN transition)

**Quality bar**: the target code's Gotchas section alignment must be
verified. Applying a pattern without honoring its gotchas produces
broken instances that make the pattern look bad.

### Operation 3 — Case B: Consolidate pattern instances

**When**: multiple sites implement the same shape ad-hoc.

**Process**:

1. Enumerate all instances with `Grep` — find the shape (e.g., `Grep` for
   retry-loop-with-backoff idiom)
2. Compare instances side-by-side:
   - Which parts are identical? → that's the pattern core
   - Which parts vary? → that's the parameterization surface
3. Extract shared implementation to `aicp/core/<pattern_name>.py`
   (or extend an existing module if the pattern is tightly scoped)
4. Migrate instances to use the shared implementation, one at a time,
   with tests passing after each
5. Author the pattern doc at `wiki/patterns/01_drafts/<pattern-name>.md`
   per Knowledge Evolution Standards (≥2 instances, ≥2 alternatives,
   ≥6 evidence items)

**Quality bar**: consolidation MUST preserve per-instance behavior
(pattern-refactors are behavior-preserving). Regression tests per
instance MUST stay green.

### Operation 4 — Case C: Promote an emergent pattern

**When**: a solution worked well; document it for reuse.

**Process**:

1. Wait until you have ≥2 instances of the shape in AICP code (or ≥1 in
   AICP + ≥1 in the second brain / other fleet project) — Knowledge
   Evolution Standards bar
2. Author the pattern doc at `wiki/patterns/00_inbox/<pattern-name>.md`
   or `01_drafts/` per pattern template (`wiki/config/templates/`)
3. Required sections:
   - Context (when to use, when NOT to use)
   - Implementation (canonical shape — often code snippet)
   - Alternatives considered (≥2)
   - Instances (≥2 concrete uses)
   - Evidence (≥6 items — commits, tests, lessons)
   - Gotchas (known failure modes from the instances)
4. Lint the doc: `python3 -m tools.lint wiki/patterns/01_drafts/<name>.md`
5. Cross-link from CLAUDE.md or relevant skill's Reference exemplars

**Quality bar**: patterns with <2 instances are not patterns — they're
one-offs. Respect the ≥2 bar; promoting too-early creates pseudo-patterns
that mislead future refactors.

### Operation 5 — Apply a pattern from the second brain

**When**: the second brain (`wiki/patterns/` in the research wiki)
documents a pattern AICP should adopt.

**Process**:

1. Browse: `python3 -m tools.view search <pattern-keyword>` or directly
   read `raw/articles/from-<project>/patterns/` in the brain
2. Assess applicability honestly — not every brain pattern fits AICP's
   single-operator backend-AI-platform identity
3. If applicable: apply per Operation 2, but first duplicate-or-reference
   the pattern doc locally at `wiki/patterns/00_inbox/` with provenance
   (`source: second-brain / <original-path>`)
4. Contribute back via `python3 -m tools.gateway contribute` if AICP's
   instance adds new evidence to the brain's pattern

**Quality bar**: brain patterns cross project boundaries; their
applicability to AICP is not automatic. Resist adoption-for-adoption's-sake.

### Operation 6 — Verify and link

**When**: refactor complete; documentation/links need alignment.

**Process**:

1. Run all tests affected: `pytest tests/ -k <pattern_area>`
2. Run ruff: `ruff check aicp/`
3. Verify lint on the pattern doc: `python3 -m tools.lint wiki/patterns/`
4. Update CLAUDE.md if the pattern warrants top-level mention
5. Cross-link from related skill Reference exemplars sections
6. Commit with `refactor(<area>): consolidate X into <pattern> pattern`
   or `docs(patterns): promote <pattern> to draft` message

**Quality bar**: patterns without cross-links rot. Every documented
pattern must be discoverable from at least one skill's Reference
exemplars.

## Gotchas

- **Detection**: agent pattern-refactors based on "feels like a pattern"
  without naming instances.
  **Rule**: require ≥2 concrete code sites / instances before refactoring.
  **Reasoning**: the premature-abstraction failure mode is real; two
  instances define a pattern, one is just code.

- **Detection**: agent applies pattern without reading the pattern's
  Gotchas section.
  **Rule**: pattern docs have Gotchas for a reason — apply them AT THE
  SAME TIME as the pattern shape.
  **Reasoning**: patterns encode failure modes; ignoring the Gotchas
  produces broken instances that make the pattern look unreliable.

- **Detection**: agent promotes a pattern with <2 instances.
  **Rule**: Knowledge Evolution Standards require ≥2; enforce it.
  **Reasoning**: single-instance "patterns" mislead future refactors
  into forcing the shape onto sites where it doesn't fit.

- **Detection**: agent consolidates ad-hoc instances without preserving
  per-instance behavior.
  **Rule**: pattern-refactor is behavior-preserving by default; changes
  require a separate commit and test justification.
  **Reasoning**: bundled behavior-change + consolidation is
  unreviewable; splits the reasoning about what broke.

- **Detection**: agent adopts a second-brain pattern without AICP-fit
  check.
  **Rule**: every brain-origin pattern adoption carries an applicability
  note in the `00_inbox/` local copy.
  **Reasoning**: brain patterns emerge from other project contexts
  (fleet, OpenArms, NNRT); AICP's constraints differ and some patterns
  don't transfer cleanly.

- **Detection**: agent documents a pattern that duplicates an existing
  brain pattern without cross-reference.
  **Rule**: before authoring, `python3 -m tools.view search <pattern-keywords>`
  in the brain.
  **Reasoning**: parallel patterns create fragmentation in the
  ecosystem's knowledge graph; one pattern with evidence from multiple
  projects is stronger than several separate ones.

## Reference exemplars

- `wiki/patterns/01_drafts/profile-as-coordination-bundle.md` —
  AICP canonical pattern (profiles coordinate backends + router + RAG
  + budget + cache + timeouts via single switch)
- `wiki/patterns/01_drafts/single-active-backend-with-lru-eviction.md` —
  resource-constrained pattern (VRAM-bound single-active backend)
- `wiki/patterns/01_drafts/three-permission-modes-think-edit-act.md` —
  operator-authority tier pattern
- `wiki/patterns/01_drafts/per-backend-circuit-breaker-with-failover-chain.md` —
  reliability pattern (three-state machine per backend)
- `wiki/patterns/01_drafts/per-day-jsonl-dlq-with-retry-budget.md` —
  persistence pattern for failed tasks
- `aicp/core/circuit_breaker.py` — canonical pattern IMPLEMENTATION
  (per-backend, three-state, failover integration)
- `aicp/core/dlq.py` — canonical pattern IMPLEMENTATION (per-day JSONL)
- `wiki/config/templates/pattern.md` (if exists) — frontmatter and
  section template for new patterns
- Second brain `python3 -m tools.view patterns` — cross-project pattern
  library

## Domain context

AICP's pattern layer reflects its identity as a single-operator,
local-first backend AI platform with hard resource constraints (single
GPU, single active backend). Its patterns emphasize: coordination
(profile bundles), resource-sharing (single-active + LRU), permission
(three modes), reliability (circuit breaker + DLQ). Most applicable
new patterns sit at the intersection of "local-first constraints" +
"operator authority" + "backend pluggability". Patterns that assume
horizontal scaling, multi-tenancy, or request parallelism often DON'T
transfer from the brain — flag applicability before adopting.

## Related skills

| Skill | When to use |
|-------|-------------|
| `refactor-extract` | For extracting a single definition (below pattern level) |
| `refactor-split` | For splitting a module (below pattern level) |
| `refactor-rename` | For renaming a symbol |
| `refactor-architecture` | For package-layout restructure (above pattern level) |
| `architecture-propose` | If the pattern needs significant architectural context |
| `feature-document` | For scoping pattern-application as a task |
| `quality-lint` | For post-refactor style hygiene |
| `quality-debt` | For inventorying pattern-opportunities as deferred work |
