---
name: doc-adr
description: Create an Architecture Decision Record (ADR) for a technical decision and store it in the central ADR registry (default ~/.claude/adr-registry/<service>/, override with $CLAUDE_DOC_HOME). Use when a significant technical choice was made — library selection, infrastructure trade-off, pattern adoption, security approach — and the reasoning should be preserved. `/sdd:doc-adr list` shows the ADRs already registered for the current repo's service.
argument-hint: "[list] | decision description | TICKET-ID | open-questions"
allowed-tools: Read, Write, Bash(find .specwork:*), Bash(cat .specwork/_spec/*), Bash(ls:*), Bash(mkdir:*), Bash(grep:*), Bash(sed:*), Bash(basename:*), Bash(git rev-parse:*), Bash(git branch:*), mcp__atlassian__getJiraIssue
---

# ADR


---

## Description

Captures a technical decision as an Architecture Decision Record (ADR) — a short,
immutable document that records the context, the decision, and the consequences — and
**stores it directly in the central ADR registry**. There is no separate publish step
and **no copy is left in the service repo**: the registry is the single home for ADRs,
exactly like `/sdd:doc-investigation`.

ADRs never get edited. If a decision changes, a new ADR supersedes the old one.
This gives the team a permanent, searchable history of *why* the system is the way it is.

---

## Modes

| Invocation | Action |
|------------|--------|
| `/sdd:doc-adr` | **Create + store (default)** — prompts for the decision interactively, then writes the ADR straight to the registry. |
| `/sdd:doc-adr "<description>"` | Start from a one-line decision description. |
| `/sdd:doc-adr TICKET-ID` | Fetch the Jira ticket and extract decisions from it (see Jira Mode). |
| `/sdd:doc-adr open-questions` | Extract resolved Open Questions from the current branch spec and generate ADRs from them. |
| `/sdd:doc-adr list` | **List mode** — print the ADRs registered for the current repo's service. Read-only; creates nothing. |

`list` is the only reserved literal argument — anything else is treated as a decision
description or ticket ID.

---

## Registry Path

All registry I/O resolves through a single environment variable, the same one every
`doc-*` command uses:

```bash
REGISTRY="${CLAUDE_DOC_HOME:-$HOME/.claude}/adr-registry"
```

- **Default** (no env var set): `~/.claude/adr-registry/`.
- **Override**: `export CLAUDE_DOC_HOME=/path/to/registry-root` — e.g. a cloned GitLab
  repo for team-shared ADRs. ADRs are written under
  `$CLAUDE_DOC_HOME/adr-registry/<service>/`.

The same variable controls `/sdd:doc-adr-query`, `/sdd:doc-catalog`, `/sdd:doc-spec`,
and `/sdd:doc-investigation`, so all doc registries move together.

---

## List Mode

Run when the argument is `list`. This is **scoped to the current repo's service** — it
prints only that service's ADRs and exits before any create logic runs. (To ask
questions across every service, use `/sdd:doc-adr-query`.)

1. Detect the service the same way create does (see Service Name): `spring.application.name`
   → git repo basename, lowercased.
2. List that service's ADRs, grouped by ticket prefix (alphabetical sort):

```bash
SERVICE="<detected-service>"
DIR="${CLAUDE_DOC_HOME:-$HOME/.claude}/adr-registry/$SERVICE"

if [ ! -d "$DIR" ] || ! ls "$DIR"/*.md >/dev/null 2>&1; then
  echo "No ADRs registered for $SERVICE."
  echo "Run /sdd:doc-adr in this repo to create and register one."
  exit 0
fi

echo "ADRs for $SERVICE in $DIR:"
for f in "$DIR"/*.md; do
  title="$(grep -m1 '^# ADR-' "$f" | sed 's/^# //')"
  printf "  %-52s  %s\n" "$(basename "$f")" "$title"
done
```

The alphabetical sort groups ADRs by ticket prefix (all `IR-*` together, `NOTICKET-*`
last). After listing, exit. Do not proceed to the create steps below.

---

## What It Does

| Step | Action |
|------|--------|
| 1 | Reads `$ARGUMENTS` — decision description, ticket ID, or nothing |
| 2 | If ticket ID → fetches via Jira MCP to extract context (see Jira Mode) |
| 3 | If missing context → asks targeted questions (see Context Gathering) |
| 4 | Resolves the service name (see Service Name) → registry subdir `adr-registry/<service>/` |
| 5 | Scans that registry subdir to determine the next ADR number |
| 6 | Generates a slug from the title |
| 7 | Prints the ADR and writes it straight to `adr-registry/<service>/<TICKET>-ADR-NNN-<slug>.md` (no in-repo copy, no confirmation prompt) |
| 8 | Prints the stored registry path |

---

## Context Gathering

Before drafting, the skill needs four things:

| What | Question asked if missing |
|------|--------------------------|
| **The decision** | "What was decided?" |
| **The context** | "What problem or constraint forced this decision?" |
| **Alternatives** | "What other options were considered and why were they ruled out?" |
| **Consequences** | "What are the trade-offs — what do you gain and what do you give up?" |

If `$ARGUMENTS` provides enough to infer some of these, do not ask — fill them in
and note any inferences as `[INFERRED]` in the draft for the user to confirm.

Ask all missing questions in a single message, not one at a time.

---

## Open Questions Mode

Triggered when `$ARGUMENTS` is `open-questions`.

1. Reads current branch → extracts ticket ID or slug
2. Locates `.specwork/_spec/<id>-spec.md` — aborts if missing
3. Scans `## Open Questions` for resolved items (`- [x]`):

```
- [x] Consent timeout duration — resolved: 30 minutes, confirmed with Legal
- [x] Retry on Access Denied — resolved: no retry, open circuit immediately
```

4. Filters out trivial resolutions (e.g. "confirmed by PM", "no change needed") —
   only surfaces decisions that have architectural consequences.

5. For each non-trivial resolved question, show:

```
Resolved Open Questions that may warrant an ADR:

  1. Consent timeout: 30 minutes confirmed with Legal
     → involves a compliance constraint and a timeout window lifecycle decision

  2. No retry on Access Denied — open circuit immediately
     → affects error handling strategy across all DataVendor callers

Generate ADRs for which? (comma-separated numbers, 'all', or 'none'):
```

6. For each selected question, run the normal ADR draft flow using the question
   text and resolution as the starting context.

---

## Jira Mode

If `$ARGUMENTS` matches `^[A-Z]+-[0-9]+$`, fetch the ticket via
`mcp__atlassian__getJiraIssue`. Extract:

- Decisions embedded in the description or comments
- Alternatives mentioned and reasons for rejection
- Risks or assumptions that represent consequences

If multiple distinct decisions are found in the ticket, list them and ask:

```
Found 3 decisions in PROJ-17097. Which should this ADR cover?

  1. Use PostgreSQL instead of Redis for circuit breaker state
  2. Pessimistic write lock on open() to prevent race conditions
  3. Singleton row pattern (id=1) instead of append-only log

Enter a number, or 'all' to create one ADR per decision:
```

If `all`: create each ADR sequentially, incrementing the number for each.

---

## Numbering and File Name

The ADR number is **service-wide and monotonic**, scoped to the service's registry
subdir. Scan `adr-registry/<service>/` for files matching `*-ADR-NNN-*.md`:

```bash
REGISTRY="${CLAUDE_DOC_HOME:-$HOME/.claude}/adr-registry"
ls "$REGISTRY/<service>"/*-ADR-[0-9][0-9][0-9]-*.md 2>/dev/null \
  | grep -oE 'ADR-[0-9]{3}' \
  | sort \
  | tail -1
```

Extract the highest number and increment by 1. If the subdir has no ADRs yet, start at `ADR-001`. Zero-padding to 3 digits means lexical sort equals numeric sort.

Zero-pad to 3 digits: `ADR-001`, `ADR-012`, `ADR-100`.

**File name format**: `<TICKET>-ADR-NNN-<slug>.md`

The ticket ID comes first, followed by `ADR-NNN`, then the kebab-case slug. Resolve the ticket from `$ARGUMENTS`, the current branch name, or context inference:

```
PROJ-17097-ADR-001-use-postgresql-circuit-breaker.md
IR-36-ADR-002-defer-pii-until-consent-accepted.md
```

If no ticket ID is available, use the literal prefix `NOTICKET`:

```
NOTICKET-ADR-003-adopt-pessimistic-write-lock-for-circuit-open.md
```

The `NOTICKET` prefix keeps `ADR-NNN` in a fixed position (always the second hyphen-separated segment), so the find/grep numbering scan above stays uniform.

The ADR counter is **service-wide and monotonic** — it does not reset per ticket. A service whose ADRs span tickets IR-64 and IR-65 still numbers them ADR-001, ADR-002, ADR-003 in the order they were created.

---

## ADR Format

```markdown
# ADR-NNN: <Title>

## Status
Accepted

## Context
<One or two paragraphs: the problem, constraint, or situation that forced a decision.
No solution language here — only the "why we had to choose something.">

## Decision
<What was decided. Include the key reason alternatives were ruled out — one sentence
per alternative is enough.>

## Consequences
<Bullet list of trade-offs — both positive and negative. Be specific.
A vague "adds complexity" is less useful than "every DataVendor call now incurs one extra DB read.">

## Related
- Jira: [TICKET-ID](url)   ← omit if none
- MR: [!NNN](url)          ← omit if none
```

---

## Title Rules

- Title Case
- Start with a verb: "Use X", "Replace X with Y", "Adopt X for Y", "Disable X"
- Max 10 words
- Never start with "We decided to" or "Decision to"

Good: `Use PostgreSQL Instead of Redis for Circuit Breaker State`
Bad: `Decision about circuit breaker persistence layer`

---

## Service Name

ADRs are keyed by service: they land in `adr-registry/<service>/`. Resolve the service
name in this order (first hit wins) — the **same order** `/sdd:doc-catalog` and
`/sdd:doc-spec` use, so the service-catalog, adr-registry, and spec-registry all agree
on one key per service:

1. `spring.application.name` from `application.yml` / `application.yaml`
   (or `application.properties`) — authoritative for Spring services.
2. git repo basename:
   ```bash
   git rev-parse --show-toplevel | xargs basename
   ```

Lowercase to kebab-case. Example: `spring.application.name: consumer-portal-service`
→ `adr-registry/consumer-portal-service/`.

---

## Write + Confirm

There is **no yes/no write gate and no commit offer** — creating the ADR stores it, the
same way `/sdd:doc-investigation` does. Print the full ADR so the user sees exactly what
landed, write it straight to the registry, then print the stored path:

```bash
REGISTRY="${CLAUDE_DOC_HOME:-$HOME/.claude}/adr-registry"
mkdir -p "$REGISTRY/<service>"
# Write the ADR with the Write tool to
#   "$REGISTRY/<service>/<TICKET>-ADR-NNN-<slug>.md"
```

After writing, list the ADRs now registered for the service:

```bash
ls -1 "${CLAUDE_DOC_HOME:-$HOME/.claude}/adr-registry/<service>"/*.md 2>/dev/null | xargs -n1 basename | sort
```

Then print the confirmation block:

```text
Stored: ~/.claude/adr-registry/<service>/PROJ-17097-ADR-003-use-postgresql-circuit-breaker.md

<service> now has:
  IR-36-ADR-002-defer-pii-until-consent-accepted.md
  PROJ-17097-ADR-001-use-postgresql-circuit-breaker.md
  PROJ-17097-ADR-003-use-postgresql-circuit-breaker.md

Run /sdd:doc-adr-query to ask questions across the registry.
```

The user can interrupt to edit if something in the ADR is wrong.

---

## Superseding an Existing ADR

If the user says "this supersedes ADR-002" (or the skill infers it from context):

1. Update the existing ADR **in the registry** (`adr-registry/<service>/`) — its
   `## Status` becomes:
   ```
   Superseded by [ADR-NNN](<TICKET>-ADR-NNN-<slug>.md)
   ```
2. Add to the new ADR's `## Status`:
   ```
   Accepted — supersedes [ADR-002](<TICKET>-ADR-002-<slug>.md)
   ```

Never delete or rewrite the old ADR's body — only update its Status line.

---

## Integration with Open Question resolution

When a workflow resolves Open Questions mid-implementation and marks a
`- [ ]` item as `- [x]`, it should check whether the resolution carries
architectural weight (a technology choice, a compliance constraint, a pattern
decision). If so, it prints:

```
⚑  "Consent timeout: 30 minutes confirmed with Legal" looks like an architectural
   decision worth preserving. Run /sdd:doc-adr open-questions to capture it.
```

This is a suggestion only — it never blocks the update flow.

---

## Independence from the SDD Pipeline

This skill has no dependency on `.specwork/` artifacts beyond the optional
Open Questions mode. It does not affect `/sdd:whatnext`, `/sdd:state`, or any other
pipeline skill. It can be run at any point: before implementation, during, or
after merging. It writes only to the registry, never to the service repo's working tree.

---

## Related Skills

- `doc-adr-query` — reads every ADR in `~/.claude/adr-registry/` and answers cross-service decision questions
- `doc-catalog` — same create-and-store pattern for the service catalog
