---
model_tier: high
name: adr-create
description: "Use when capturing an architectural decision — file naming, next ADR number, Status / Context / Decision / Consequences, index regen; fires even without saying 'ADR'."
domain: process
scope:
  write:
    - pattern: "docs/decisions/ADR-*.md"
      access: "create"
    - pattern: "docs/decisions/INDEX.md"
      access: "write"
  verification_command: "./scripts-run src/scripts/adr/regenerate_index --dir docs/decisions"
execution:
  type: assisted
  handler: shell
  timeout_seconds: 30
  allowed_tools: []
  command:
    - ./scripts-run
    - src/scripts/adr/regenerate_index
    - --dir
    - docs/decisions
runtime_requires:
  bins:
    - bash
    - node
  network: []
workspaces:
  - agent-config-maintainer
packs:
  - meta
---

# adr-create

## When to use

Use this skill when:

- A non-trivial architectural choice needs a written record (kernel
  membership, cap raises, contract changes, library swap, deprecation).
- A decision overrides a previous one and needs `supersedes:` linkage.
- A roadmap phase closes and the chosen variant must be cited.
- The user says "write an ADR for X", "decision log this", "we need
  a record of why we picked Y".

Do NOT use when:

- The change is reversible without governance impact (typo, lint
  fix, refactor that stays inside one module).
- The decision is already covered by an existing ADR — extend or
  supersede it instead of duplicating.
- A skill, rule, or guideline is the better home (use those skills).

## Admission gate — classify before you create

Run this **before** picking a surface or a number. An ADR is warranted only
when the decision is architecturally significant on at least one axis:

1. **Hard or costly to reverse** — a one-way door: public API shape, DB
   schema, wire format, published identifier, migration.
2. **Broadly constraining** — it binds work outside the module that made it.
3. **Crosses a governed surface** — consumer contract, API, security or
   privacy floor, package structure.

None of the three holds → it is **not** an ADR. Route it to its real home: a
decision note in `agents/decisions/`, a config value, a measurement record in
`docs/CLAIMS.md`, an experiment, or a roadmap item.

Explicitly **not** ADRs: a temporary numeric threshold · a benchmark value ·
a model mapping · one-off release sequencing · a reversible local
implementation detail.

**The tree's own reference case.** ADR-002 encodes `25 000 → 26 000` and a
`4.0k` override ceiling as architecture law (`ADR-002:55`, `:62`), and
ADR-114 then had to add another override while recording that 7 of 9 kernel
rules already carry them (`ADR-114:74`). The *principle* — a kernel budget
exists, is measured, and is capped — is the ADR. The numbers belong in a
versioned budget contract with a regression gate, so a recalibration stops
needing an architecture supersession.

## Goal

- Sequential `ADR-NNN-<slug>.md` numbering with no gaps.
- Standard template: Status, Context, Decision, Consequences,
  Alternatives, References.
- Regenerated index so readers find the ADR by topic, not by ls.
- Zero MCP-tool dependency — pure filesystem + TypeScript tooling (run via ./scripts-run).

## Preconditions

- An ADR directory exists. Two layouts coexist (see
  [`docs/contracts/adr-layout.md`](../../../docs/contracts/adr-layout.md)):
  - **Flat** — `docs/decisions/` (or `docs/adr/` alias): cross-cutting
    governance ADRs, 3-digit numbering (`ADR-NNN-<slug>.md`).
  - **Per-area** — `docs/adrs/<area>/`: sub-area ADRs, 4-digit
    numbering (`NNNN-<slug>.md`); `<area>` must match the canonical
    inventory in `src/scripts/audit_adr_coverage.ts` (`AREAS`). Deliberately not
    a link: this skill is projected into `dist/agent-src/skills/`, whose sibling
    `scripts/` directory carries six curated files and not this one, so any
    relative href that resolves in `src/` is broken in the projection.
- The decision is **already made** — ADRs record outcomes, they do
  not run the decision process. For unresolved trade-offs, run the
  council or consult `adversarial-review` first.

## Procedure

### 1. Inspect and pick the surface

Ask one question only if both are plausible:

1. **Flat surface** — chosen when the decision constrains the
   package's contract with consumers (kernel composition, rule
   taxonomy, package-wide architecture). Directory: `docs/decisions/`
   (fallback `docs/adr/`). Filename: `ADR-NNN-<slug>.md`.
2. **Per-area surface** — chosen when the decision constrains code
   inside one area folder (one runtime module, one contract group,
   one CLI surface). Directory: `docs/adrs/<area>/`. Filename:
   `NNNN-<slug>.md` (4-digit, no `ADR-` prefix).
3. **Unknown area** — `<area>` not in the inventory: refuse with a
   hint to add the area to `AREAS` in
   `src/scripts/audit_adr_coverage.ts` in the same PR. Do not invent.
4. **In doubt** → per-area (cheaper to surface, easier to relocate).

### 2. Pick the next ADR number

- **Flat surface** — scan `docs/decisions/` (or `docs/adr/`) for
  `ADR-*.md`, parse the leading 3-digit number, take `max + 1`
  (zero-padded to 3). For an empty directory, start at `001`.
- **Per-area surface** — scan `docs/adrs/<area>/` for
  `[0-9][0-9][0-9][0-9]-*.md`, parse the leading 4-digit number,
  take `max + 1` (zero-padded to 4). For an empty area, start at
  `0001`. `README.md` is **not** an ADR — skip it.

Reject re-use of an existing number — index regeneration treats
duplicates as a hard failure on both surfaces.

### 3. Pick a slug

Short, hyphen-lowercase, scope-revealing. Match peer ADRs in the
directory. Examples: `kernel-swap-deferred`, `flat-cluster-subs`,
`http-bridge-deferred-with-trigger`,
`per-tier-smoke-scripts`. Reject slugs longer than 60 chars.

### 4. Author the ADR

Use the surface-specific template. All sections are required; "—"
is acceptable for genuinely empty Alternatives or References blocks
but never for Status, Context, Decision, or Consequences.

`## Evidence` and `## Assumptions` are required headings too, with one
carve-out each: `## Evidence` may be empty only when the record grades itself
`E0` and says so in the section, and `## Assumptions` may be "—" only when
every load-bearing claim in the rationale carries a basis ref.

**`review_trigger` is required and it names a CONDITION, not a date.** A
decision is a call made under conditions that held at the time; the trigger
records which change would make it worth re-deciding. "Review annually" is
ignored by everyone and rots into ceremony —
`check_adr_frontmatter.ts` rejects bare cadences for exactly that reason. Write
the event: *"when a second consumer reports the same preservation surprise"*,
*"when a host ships a native primitive for this"*, *"if the measured lift drops
below the pre-registered threshold"*. Enforced from 2026-07-25 forward; earlier
ADRs are grandfathered by date.

**Staged — and `terminal` is not one of the stages.** A new or materially
amended accepted ADR needs a substantive trigger now. An *existing* accepted
record may carry `review_trigger: unclassified` while the migration runs, and
that exception count only ever decreases. `terminal`, `none`, an empty value
and permanence phrasing ("forever", "never revisit", "settled forever") are
invalid at **every** stage — `check_adr_frontmatter.ts` rejects them, because
"no trigger — terminal decision" is permanence with softer wording. `terminal`
is not a migration state; it is the thing the staging exists to stop becoming
permanent. Superseded, rejected and deprecated records are historical and need
no active trigger.

When you later reopen one, say which **premise moved** and what evidences the
move — not "we were wrong". If the original was right under its own conditions,
record that too. A premise that turns out false while the decision stays correct
gets a logged correction block, never a silent edit.

**Three descriptive axes ship on a new record** — `provenance`, `evidence`,
`authority_basis`. Vocabulary, defaults and the mutation policy are owned by
[`adr-layout § Provenance and evidence`](../../../docs/contracts/adr-layout.md);
`check_adr_frontmatter.ts` validates the shape. What the author has to get
right while drafting:

- Every load-bearing factual claim in the rationale either **points at a basis
  ref** — `file:line`, a URL, a `docs/CLAIMS.md` claim id, a benchmark id — or
  is **labelled an assumption** under `## Assumptions`. There is no third
  state, and an unlabelled guess reads as a finding to the next reader.
- **An empty `## Evidence` section means `E0` by construction, and the record
  says so.** An honest E0 is publishable, exactly as an honest null is; a
  confident grade over an empty section is not.
- `discovery: incomplete` is the honest default on E0 and stays that value
  until a defined evidence search has run and found nothing. `complete`
  asserts absence — a claim the author owns.
- **A grade of E2 or above must name a `basis`.** The validator rejects an
  E2/E3/E4 with an empty basis list; grade it lower rather than asserting a
  source you cannot cite.
- **A council attribution never lifts a grade above E0.** N models agreeing is
  `provenance: agentic` with `agentic_mode: council` — sources and
  measurements raise `strength`, consensus does not. A council is deliberately
  not its own `kind`.
- A human product decision records `strength: E0` with
  `authority_basis: owner_intent` and does **not** fake a grade. Its authority
  comes from owning the purpose.
- **A grade prices review burden, never authority.** Nothing about writing
  `E0` makes the record cheaper to overturn *by whom* — see
  [`adr-layout § The reopen record`](../../../docs/contracts/adr-layout.md).

**Flat-surface template** (`docs/decisions/ADR-NNN-<slug>.md`):

```markdown
---
adr: NNN
status: proposed | accepted | superseded | deprecated
date: YYYY-MM-DD
decision: <slug>
supersedes: — | ADR-MMM
superseded_by: — | ADR-MMM
amends: — | ADR-MMM          # optional — this ADR amends that one (reciprocal required)
amended_by: — | ADR-MMM      # optional — reciprocal of `amends`
phase: <roadmap> · <phase-id>
review_trigger: <the CONDITION that would reopen this decision>
protected_dimensions: [...]  # optional — purpose | security_floor | privacy_floor | external_commitment | governance | none
reopen_policy: directional | owner | unclassified   # optional; absent → unclassified

provenance:
  kind: human | agentic | mixed | unknown
  decision_makers: [...]          # who actually selected it
  human_directed: true | false | unknown
  agentic_mode: single | council | delegated   # optional, descriptive only
evidence:
  strength: E0 | E1 | E2 | E3 | E4
  discovery: complete | incomplete    # required when strength is E0
  basis: [...]                        # file:line | URL | CLAIMS id | benchmark id
authority_basis: evidence | owner_intent      # optional; absent → evidence
---

# ADR-NNN — <Decision Title>

## Status

**<Proposed | Accepted | …>** · YYYY-MM-DD.

## Context / Decision / Evidence / Assumptions / Consequences / Alternatives / References
```

`## Evidence` carries one line per basis ref backing a load-bearing claim.
`## Assumptions` carries every load-bearing claim that has no basis ref — that
is what makes the grade honest rather than decorative.

**Per-area template** (`docs/adrs/<area>/NNNN-<slug>.md`):

```markdown
---
adr: NNNN
area: <area>
status: proposed | accepted | superseded | deprecated
date: YYYY-MM-DD
decision: <slug>
supersedes: —
superseded_by: —
type: retrospective | prospective
review_trigger: <the CONDITION that would reopen this decision>

provenance:
  kind: human | agentic | mixed | unknown
  decision_makers: [...]
  human_directed: true | false | unknown
  agentic_mode: single | council | delegated   # optional, descriptive only
evidence:
  strength: E0 | E1 | E2 | E3 | E4
  discovery: complete | incomplete    # required when strength is E0
  basis: [...]                        # file:line | URL | CLAIMS id | benchmark id
authority_basis: evidence | owner_intent      # optional; absent → evidence
---

# ADR NNNN — <Decision Title>

> Area: `<area>` · Status: accepted · Date: YYYY-MM-DD · Type: retrospective | new
> Roadmap: `agents/roadmaps/<file>.md` <phase-id>
> Supersedes: —

## Context / Decision / Evidence / Assumptions / Considered alternatives / Consequences / References
```

The frontmatter block is the same shape as the flat surface — the contract
says so ([`adr-layout § Frontmatter`](../../../docs/contracts/adr-layout.md):
"identical across both surfaces"), and `audit_adr_coverage.ts`'s parser reads
it when present. The quote-style header stays as the human-readable banner,
and every existing per-area record now carries frontmatter beside it, so their
generated README tables render real values — see
[`docs/adrs/telegraph/README.md`](../../../docs/adrs/telegraph/README.md),
whose rows read `accepted` / `2026-05-16`. A record carrying the banner alone
is not blank either: `parse_blockquote_meta` reads the
`> Area: … · Status: … · Date: …` line as a fallback, and only a record with
neither renders "—". Cite the area's contract from the README in
[`docs/adrs/<area>/README.md`](../../../docs/adrs/).

### 5. Regenerate the index

- **Flat surface** — `./scripts-run src/scripts/adr/regenerate_index
  --dir docs/decisions/` writes `INDEX.md` from `ADR-*.md`.
- **Per-area surface** — `./scripts-run src/scripts/audit_adr_coverage
  --regen-area-readme <area>` rewrites `docs/adrs/<area>/README.md`.
  Coverage gate: run `./scripts-run src/scripts/audit_adr_coverage` (no
  args) — exit 0 only when every canonical area has ≥ 1 ADR.

### 6. Validate

- Flat: `./scripts-run src/scripts/adr/regenerate_index --dir docs/decisions/ --check` exits 0.
- Per-area: `./scripts-run src/scripts/audit_adr_coverage --check` exits 0.
- The project's CI / quality pipeline passes — locally only when
  `quality.local_auto_run: true`; under the default (`false` / missing)
  remote CI is the gate and no local pipeline run happens.

## Rubric pass (optional, surfacing-only)

After drafting an ADR, run
[`judge-artifact-completeness`](../judge-artifact-completeness/SKILL.md)
with rubric `architecture-score` to confirm alternatives, consequences,
reversibility, and risk are present. Invoke when the user asks for a
completeness check — not on every ADR by default.

## Output format

1. Path of the new ADR file.
2. Path of the regenerated index / README.
3. One-line summary of the decision.
4. Linked roadmap or phase, if any.

## Gotchas

- **Flat default path** is `docs/decisions/` in this package; some
  projects use `docs/adr/`. Pass `--dir` when running outside the
  default.
- **Per-area numbering is 4-digit** (`NNNN-<slug>.md`); the flat
  surface stays 3-digit (`ADR-NNN-<slug>.md`). Do not mix.
- **Area inventory is closed** — `<area>` must already exist in
  `AREAS` in `src/scripts/audit_adr_coverage.ts`. Adding a new area is
  a separate PR with explicit reviewer sign-off.
- Frontmatter `adr:` (flat) is the canonical number; the filename
  prefix must match. The flat regenerator fails on mismatch.
- ADRs are append-only history. To revise a decision, write a new
  ADR with `supersedes: ADR-MMM` (flat) or a `Supersedes:` line in
  the header quote-block (per-area) and flip the old one's status
  to `superseded`.
- Never delete an ADR file — supersede it. Deletion breaks
  historical links and round-trips through git history checks.
- **Amending is the common case; wire it in both directions.** Most reopens
  correct one decision inside an otherwise sound ADR rather than replacing the
  whole record. Use `## Amendment N (YYYY-MM-DD) — <topic>` plus the reciprocal
  `amends:` / `amended_by:` pair — the validator rejects a one-sided link,
  because a one-sided link is invisible from the stale side, and the stale side
  is the one a reader lands on first. Where the amendment reverses text that is
  still asserted above it, add a one-line banner there too; the frontmatter
  alone does not stop someone quoting the reversed sentence.
- **Who may reopen it is recorded, not assumed** — `reopen_policy` /
  `protected_dimensions`, both optional, absent meaning `unclassified`
  ([`adr-layout § Reopen authority`](../../../docs/contracts/adr-layout.md)).
  Reach for `owner` only when EVERY future transition is genuinely reserved;
  `directional` is the normal answer, and no answer is a fine answer.

## Frugality Standards

Apply the [Frugality Charter](../../contexts/contracts/frugality-charter.md)
to every ADR you author.

**Examples in this artifact:**
- Per the charter's default-terse rule, `## Context` states the
  forcing function in 2–3 sentences; no historical narrative.
- Per the cite-don't-restate principle, `## Decision` links the
  rules / contracts it overrides; no rule body is quoted in full.
- Per the cheap-question check, `## Alternatives considered` lists
  genuine design alternatives, not strawmen.

**Pre-save self-check:**
1. Does `## Context` carry more than 5 sentences of setup?
2. Does `## Decision` restate rule text instead of citing the rule?
3. Are alternatives evaluated with a real consequence each, or with
   stylistic preference?
4. Does the ADR forecast consequences with hedge phrases ("might",
   "could potentially") instead of decidable claims?

## Do NOT

- Skip Context — a decision without context is folklore.
- Reuse an existing ADR number — the index regenerator hard-fails.
- Author ADRs for reversible refactors or minor cleanups.
- Cite a council session id without ensuring the file is committed
  or otherwise reachable from the repo (per `no-roadmap-references`,
  council clause).
