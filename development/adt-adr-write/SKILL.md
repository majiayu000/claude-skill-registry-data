---
name: adr-write
description: Capture an Architecture Decision Record — what was decided, why, what alternatives were considered, and when to revisit. Writes a numbered ADR file to docs/adr/ in the active repo, with consistent formatting that downstream skills (improve-codebase-architecture, refactor-plan) can read. Use right after deciding something non-obvious so the reasoning isn't lost.
triggers:
  - adr-write
  - capture
  - refactor
---

# ADR Write

Architecture Decision Records preserve the *why* behind a decision so future maintainers
(including future-you) don't undo the work to rediscover the same reasoning. Most
codebases lose this context within 6 months of the decision.

This skill captures one decision quickly, in a consistent format that is grep-able,
RAG-indexable, and readable by `improve-codebase-architecture` and `refactor-plan`.

## Use When

- You just made a non-obvious technical decision (library choice, schema design,
  pattern selection, sequencing, tradeoff between two valid approaches)
- A reviewer asks "why didn't you do X instead?" and the answer isn't already written
  somewhere
- You're about to undo a previous decision — capture both why the old one is being
  replaced and the new direction
- You're starting a refactor and want the rationale on record before the diff lands

## Do Not Use When

- The decision is obvious from the code (e.g., used the standard library function)
- The decision is captured in an existing PR description, design doc, or skill — link
  to it instead of duplicating
- The work is throwaway (spike, prototype, experiment that won't ship)

## Inputs / Prereqs

- Active repo with write access
- A clear statement of what was decided (you, the operator, must already know this —
  the skill records, it does not decide)
- Optional `<short title>` arg; otherwise the skill will ask

---

## Workflow

### 1. Find or create the ADR directory

```bash
# Conventional locations, in order of preference
for d in docs/adr docs/architecture/decisions docs/decisions adr architecture/decisions; do
  [ -d "$d" ] && ADR_DIR="$d" && break
done

# If none exist, create docs/adr (most common convention)
[ -z "$ADR_DIR" ] && ADR_DIR="docs/adr" && mkdir -p "$ADR_DIR"
```

### 2. Compute the next number

```bash
# Find highest existing ADR number, default to 0001
LAST=$(ls "$ADR_DIR" 2>/dev/null | grep -E '^[0-9]{4}-' | sort | tail -1)
if [ -n "$LAST" ]; then
  N=$(echo "$LAST" | grep -oE '^[0-9]{4}')
  NEXT=$(printf "%04d" $((10#$N + 1)))
else
  NEXT="0001"
fi
```

### 3. Gather the decision content

If the user did not provide all of these in the prompt, ask once (one combined
question, not one at a time):

- **Title** — short, imperative ("Use Drizzle instead of Prisma")
- **Context** — what situation forced this decision (1–3 sentences)
- **Decision** — what was decided (1–2 sentences, declarative)
- **Alternatives considered** — at least one, with one-line reason rejected
- **Consequences** — what changes because of this (positive and negative)
- **Revisit when** — concrete trigger that would re-open this decision

If the user gave a free-form statement, extract these fields from it; only ask for
fields that are genuinely missing. Do not interrogate them with one question per field.

### 4. Detect related context

Pull related signals to enrich the ADR without manual lookup:

```bash
# Recent commits on the area being decided
git log --oneline -10 --diff-filter=AM -- '<relevant path or glob>' 2>/dev/null

# Open PRs touching the area
gh pr list --search "<relevant keyword>" --state open --limit 5 2>/dev/null

# Existing ADRs that may be superseded
grep -lE "Drizzle|Prisma" "$ADR_DIR"/*.md 2>/dev/null
```

If an existing ADR addresses the same area, mark this new ADR as `Supersedes: NNNN`
and add `Superseded by: <new>` to the older one in the same skill run.

### 5. Write the file

```bash
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g')
FILE="$ADR_DIR/${NEXT}-${SLUG}.md"
DATE=$(date -u +%Y-%m-%d)
```

Write this template (one per ADR, no skipped sections):

```markdown
# ADR-NNNN: <Title>

- **Status:** Accepted
- **Date:** YYYY-MM-DD
- **Deciders:** <names or roles>
- **Supersedes:** ADR-NNNN  (omit if none)
- **Superseded by:**         (filled in later if/when replaced)

## Context

<1–3 sentences. What problem or pressure forced a choice. Include any constraints
the reader needs to know — performance budget, team size, deadline, vendor lock-in
risk, prior art in the codebase.>

## Decision

<1–2 sentences, declarative. "We will use X to do Y." Specific enough that someone
unfamiliar with the project can act on it.>

## Alternatives considered

- **<Alternative A>** — <one-line reason rejected>
- **<Alternative B>** — <one-line reason rejected>
- (At least one alternative; preferably 2–3.)

## Consequences

**Positive:**
- <What gets easier, faster, safer, cheaper>

**Negative:**
- <What gets harder, more expensive, more constrained>

**Neutral:**
- <Things that change but aren't strictly better or worse>

## Revisit when

- <Concrete trigger 1 — e.g., "Drizzle drops support for PostgreSQL JSON ops">
- <Concrete trigger 2 — e.g., "Team grows past 8 backend devs and migration friction
  becomes the bottleneck">
- (Without a revisit trigger, the ADR becomes permanent law it shouldn't be.)

## References

- <Link to PR, design doc, benchmark, RFC, library docs>
```

### 6. Update the ADR index (if present)

```bash
INDEX="$ADR_DIR/README.md"
if [ -f "$INDEX" ]; then
  # Append a new row to the index table; do not rewrite the whole file
  echo "| ADR-${NEXT} | [${TITLE}](./${NEXT}-${SLUG}.md) | ${DATE} | Accepted |" >> "$INDEX"
fi
```

If no index exists and there are now ≥3 ADRs, prompt to generate one.

### 7. Mark superseded ADRs

If the new ADR replaces a previous one:

```bash
# Edit the old ADR to add "Superseded by: NNNN" line
# and change Status from "Accepted" to "Superseded"
```

### 8. Stage and report

```bash
git add "$FILE"
[ -f "$INDEX" ] && git add "$INDEX"
[ -n "$SUPERSEDED" ] && git add "$SUPERSEDED"
```

Do not auto-commit. The ADR usually accompanies the change it documents — let the
user include both in the same commit.

```
ADR-${NEXT} written: ${FILE}
Status: Accepted
Supersedes: ${SUPERSEDED:-none}
Index updated: ${INDEX:-no index found}

Staged but not committed. Suggested:
  git commit -m "Add ADR-${NEXT}: ${TITLE}"

Or include with the implementation commit:
  git add <impl files> && git commit -m "<scope>: ${TITLE} (ADR-${NEXT})"
```

---

## Outputs / Evidence

- Numbered ADR file at `$ADR_DIR/NNNN-slug.md`
- Updated index (if present)
- Updated superseded ADR (if applicable)
- Files staged for commit; not auto-committed

## Failure / Stop Conditions

- Repo has no commit yet → cannot place ADR; ask user to make initial commit first
- User cannot articulate at least one alternative considered → push back ("if there
  was no alternative, this isn't a decision worth recording") and stop
- User cannot articulate a revisit trigger → still write the ADR but flag in the
  report; permanent decisions without revisit conditions tend to outlive their value

## Memory Hooks

- Read memory for any project-specific ADR conventions (different directory, different
  template, custom fields)
- Write memory only if you established a new ADR convention this session worth reusing
  (e.g., "this repo uses MADR format, not the lightweight one above")
