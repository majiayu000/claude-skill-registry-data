---
name: adr-gate
description: Pre-review/pre-commit gate that enforces ADR and spec linkage for non-trivial changes — a change that makes an architectural decision must leave a decision record
when-to-use: Automatically before code review and before committing non-trivial changes; when a change introduces a new pattern, service, schema, or security surface
user-invocable: false
effort: low
---

# ADR Gate — Pre-Review / Pre-Commit Decision-Record Enforcement

**Every non-trivial change must trace to a decision.** This gate runs *before* a code review (native `/code-review` or otherwise) and before committing architectural work. It links changes to an ADR (Architecture Decision Record) or spec, and — when a change makes a decision that no ADR captures — it drafts one so the decision is not lost in a diff.

This is the reactive counterpart to `framework-evaluation` / `/evaluate-framework`: that skill produces ADRs *proactively* when evaluating an external tool; this gate catches decisions made *implicitly*, in code, that were never written down. It is the same discipline as `doccheck` (docs must stay honest) applied to *why the code exists*, not *what the docs claim*.

**Harvested from `code-review`'s former `adr-gate.md` sub-file (deleted in the same change, per ADR-0008) and corrected to Tessera's real ADR machinery.**

---

## Tessera's ADR machinery (what this gate is grounded in — not generic)

- **`docs/adr/`** — numbered `NNNN-<slug>.md`, sequential, never reused.
- **`docs/adr/README.md`** — the index. **Every on-disk ADR MUST appear here** — `scripts/doccheck.py`'s `adr-index-complete` asserts it, and the **pre-commit hook blocks the commit** if an ADR is missing from the index. *So: any ADR this gate creates or drafts must be added to the index in the same change, or the commit fails.*
- **`docs/adr/_template.md`** — the structure for eval ADRs. Internal-decision ADRs (0005–0008) follow a prose style instead; match the closest existing ADR.
- **Statuses:** `Proposed | Accepted | Watching | Superseded by ADR-NNNN | Deprecated`.
- **Never edit an Accepted ADR.** If a decision changes, write a new numbered ADR that supersedes it (CLAUDE.md, README convention). The original stays as the historical record.
- **Other decision homes:** `docs/design-principles.md` (compounding principles — never reorder/renumber) and `docs/observatory.md` (on-the-radar, not yet ADR-weight). Not every decision is an ADR; a small one may belong in the observatory.

Downstream (Tessera-scaffolded projects): `bin/tessera-new-project` should seed `docs/adr/` and `docs/adr/0001-*.md`. Decisions there land in the project's own `docs/adr/`, not in Tessera's.

> Correction from the harvested version: the old sub-file logged decisions to `_project_specs/session/decisions.md` and initialized ADRs via "claude-bootstrap". **Neither exists in Tessera** — session memory is Mnemos; scaffolding is `bin/tessera-new-project`. Both are fixed here.

---

## Gate Protocol

```
Changed files detected
      |
      v
[1. Classify change scope] ── trivial? ──YES──> skip gate, proceed
      |
      NO
      v
[2. Discover linked ADRs + specs] ── found? ──YES──> inject into review context
      |
      NO
      v
[3. Reverse-engineer an ADR draft from git history + the diff]
      |
      v
[4. Present draft to user (interactive) OR write as Proposed (unattended)]
      |
      v
[5. Inject architectural context into the review]
```

---

## Step 1: Classify change scope

**Trivial — skip the gate:**
- Typo/comment/whitespace edits, `.md` docs, CHANGELOG/README
- Dependency patch/minor bumps, lockfiles
- Test-only changes that don't alter behavior
- Config *value* changes (not structural)

```bash
# Skip only if ALL changed files match trivial patterns
TRIVIAL='CHANGELOG|README|\.lock$|\.md$|__snapshots__|\.test\.|\.spec\.'
```

**Non-trivial — the gate applies:**
- New or deleted files; new services or patterns
- API routes, models, schemas, database migrations
- Security surface (auth, crypto, permissions, secrets handling)
- Hook lifecycle / gate / spend / verification changes (Tessera-specific: these are the mechanism layer — they almost always warrant an ADR or observatory entry)

---

## Step 2: Discover ADRs + specs

Search in order; stop when context is sufficient.

```bash
# 2a. Existing ADRs referencing the changed area
ls docs/adr/[0-9][0-9][0-9][0-9]-*.md 2>/dev/null
grep -rl "<module_or_feature>" docs/adr/ 2>/dev/null

# 2c. Specs / active focus
grep -rl "<feature>" _project_specs/ 2>/dev/null

# 2d. Decision context from git history
git log --oneline -10 -- <changed_files>
git log --grep="decision\|chose\|instead of\|trade-off\|supersede" -5

# 2e. Ticket / PR references
git log --oneline -20 | grep -oE "(#[0-9]+|[A-Z]+-[0-9]+)"
gh pr view --json body -q .body 2>/dev/null
```

**2b. iCPG (if indexed):** match ReasonNodes to changed paths — `icpg query constraints <file>` / `icpg query prior "<goal>"`. Optional; skip if iCPG is unavailable.

Produce an **ADR context block** naming linked ADRs, specs, git-history decisions, and coverage (`N/M changed files have decision linkage`).

---

## Step 3: Reverse-engineer an ADR draft (when non-trivial changes have no ADR)

Inputs: `git log --follow -5 <file>` (intent), `git diff` (what changed), file content (pattern/imports), PR body.

Draft in **Tessera's ADR form** — number it the next free `NNNN`, `Status: Proposed`, and match the nearest existing ADR's shape (eval → `_template.md`; internal decision → 0005–0008 prose):

```markdown
# ADR-NNNN: <title inferred from the change>

- **Date:** <today>
- **Status:** Proposed
- **Decision driver:** <what prompted this — inferred from commits/PR>

## Context / Decision / Consequences
<Context from commit messages + PR; Decision inferred from the code — what
 pattern/library/approach was chosen; Consequences = inferred trade-offs.>

## Alternatives considered
<If git history shows rejected approaches, name them.>
```

```bash
# Next ADR number
LAST=$(ls docs/adr/[0-9][0-9][0-9][0-9]-*.md 2>/dev/null | grep -oE '[0-9]{4}' | sort -n | tail -1)
NEXT=$(printf "%04d" $(( ${LAST:-0} + 1 )))
```

---

## Step 4: Present or auto-tag

- **Interactive (user present, default):** show the draft, ask `Accept / edit / skip`. Only a human sets `Accepted`.
- **Unattended (CI/headless):** write `docs/adr/NNNN-<slug>.md` as `Status: Proposed`, **add its row to `docs/adr/README.md` (or the pre-commit doccheck hook blocks the commit)**, log "ADR auto-drafted as Proposed — needs human review", and proceed with it as context. Never auto-`Accept`.
- **Strict:** block review until an ADR exists; do not auto-generate.

Mode is a project choice (CLAUDE.md / settings). Default interactive.

---

## Step 5: Inject architectural context into the review

Prepend to whatever review runs:

```markdown
## Architectural Context (ADR Gate)
### Active ADRs for this change
<relevant ADRs, status + one-line summary>
### Linked specs / tickets
<specs with key requirements>
### Review against ADRs
1. Does this change conform to the linked ADRs?
2. Does it introduce a decision captured in no ADR?
3. Should any existing ADR be updated or **superseded** (never edited if Accepted)?
4. Are there spec requirements this change leaves unaddressed?
```

---

## Review dimension: ADR Compliance

| Finding | Severity |
|---------|----------|
| Change contradicts an **Accepted** ADR | Critical |
| Architectural decision in no ADR | High |
| ADR exists but is stale / should be superseded | Medium |
| Minor drift from ADR intent | Low |

---

## Post-review: decision extraction

After review, if a new architectural choice was made:
1. Prompt to create an ADR in `docs/adr/` (and index it).
2. If it's smaller than ADR-weight → `docs/observatory.md`.
3. If review found an Accepted ADR is now wrong → draft a **superseding** ADR (do not edit the original).

---

## Quick reference

```
Runs:        before code review, before committing non-trivial changes
Stores:      docs/adr/NNNN-<slug>.md   +   index row in docs/adr/README.md (enforced by doccheck)
Statuses:    Proposed → Accepted → (Superseded by ADR-NNNN | Deprecated | Watching)
Never:       edit an Accepted ADR — supersede it
Not-an-ADR:  small/uncommitted decisions → docs/observatory.md
Next number: highest NNNN in docs/adr/ + 1
```
