---
name: doc-investigation
description: Capture the current session's code investigation or improvement plan into a structured document and store it in the central investigation registry (default ~/.claude/investigation-registry/<service>/, override with $CLAUDE_DOC_HOME). Asks which shape to use (inferring a recommended default) — bug (Problem → Symptoms → Root Cause → Fix), exploration (Question → Map → How It Works → Future Signals), or improvements (Goal → Gap Analysis → Plan → Out of Scope), a forward-looking remediation plan. Use after researching code, or after designing a plan to change something, in any repo — yours or someone else's — when the reasoning is worth keeping. `/sdd:doc-investigation list` lists the investigations already registered for the current repo's service.
argument-hint: "[list] | [optional title] [bug | explore | improvements to force the type]"
allowed-tools: Read, Write, Bash(cat ${CLAUDE_PLUGIN_ROOT}/templates/investigation-*.md), Bash(git rev-parse:*), Bash(git branch:*), Bash(mkdir:*), Bash(ls:*), Bash(find:*), Bash(cat application*), Bash(date:*), Bash(basename:*), Bash(grep:*), Bash(sed:*), Bash(tr:*), Bash(test:*)
---

# Investigation Capture


---

## Description

Turns the **current session's investigation** into a durable, structured document.

While researching code — often in a repo that is not your own — you uncover *why*
something behaves the way it does. That knowledge normally evaporates when the
session ends. This skill freezes it into a fixed template and files it in the
central **investigation registry**, so it survives and can later be searched with
`/sdd:doc-investigation-query`.

The conversation **is** the source. The skill reads what has been discussed so far
in this session and synthesizes it — it does not re-investigate the code. Anything
not actually discussed is marked `[TBD]` (unknown) or `[INFERRED]` (deduced) so you
can confirm before it is written.

---

## Core Rule

There are **three fixed templates**, and the skill picks one by **type**:

| Type | Template | Shape | Use when the session was… |
|------|----------|-------|---------------------------|
| `bug` | `templates/investigation-bug.md` | Problem → Symptoms → Reproduction → Investigation → Findings → Root Cause → Fix (Status/Where/Change/Verify) → Related Classes → Future Signals | …diagnosing something broken or wrong |
| `exploration` | `templates/investigation-explore.md` | Question → Context → Map → How It Works → Key Findings → Caveats & Gotchas → Open Questions → Future Signals | …understanding how/where something works, with no bug |
| `improvements` | `templates/investigation-improvements.md` | Goal → Current State → Gap Analysis → Plan → Out of Scope → Open Decisions → Future Signals | …deciding *what to change*: a remediation / improvement plan against a requirement or standard |

All three live under `${CLAUDE_PLUGIN_ROOT}/templates/`. **Read the chosen one at the start
of the run and fill its placeholders — never hand-write the structure from memory.**
Never rename, reorder, add, or drop a section. If a section has no content from the
session, keep the heading and write `[TBD]` under it. The `type` frontmatter field is
set to the chosen type so `/sdd:doc-investigation-query` can filter on it.

---

## Use Cases

```bash
/sdd:doc-investigation                                  # asks which template (bug / exploration / improvements), inferred one recommended
/sdd:doc-investigation "Vehicle lookup returns stale rows"   # seed the title; still asks which template
/sdd:doc-investigation explore "How a lead reaches the cache"  # force the exploration template
/sdd:doc-investigation bug                               # force the bug template
/sdd:doc-investigation improvements "Meet the CLAUDE.md gist"  # force the improvement-plan template
/sdd:doc-investigation list                             # list investigations already registered for this repo's service
```

Run it at **any point** in a session — the moment the investigation feels "figured
out." You can run it again later in the same session to capture a fuller picture;
each run writes a new dated file.

---

## List Mode

When `$ARGUMENTS` is exactly `list`, this is a **read-only listing** — print the
investigations already registered for the **current repo's service** and exit before
any capture logic runs. (`list` is reserved; to capture an investigation whose title is
literally "list", pass it differently, e.g. `/sdd:doc-investigation bug list`.)

Unlike `/sdd:doc-investigation-query`, which spans the whole registry, `list` is scoped
to one service — the repo you are in.

1. Detect the target service exactly as Step 2 does (`spring.application.name` →
   git repo basename → `unscoped`), lowercased.
2. List that service's investigations, newest first:

```bash
SERVICE="<detected-service>"
REGISTRY="${CLAUDE_DOC_HOME:-$HOME/.claude}/investigation-registry"
DIR="$REGISTRY/$SERVICE"

if [ ! -d "$DIR" ] || ! ls "$DIR"/*.md >/dev/null 2>&1; then
  echo "No investigations registered for $SERVICE."
  echo "Run /sdd:doc-investigation after researching code to capture one."
  exit 0
fi

echo "Investigations for $SERVICE in $DIR:"
ls -1t "$DIR"/*.md 2>/dev/null | while read -r f; do
  title="$(grep -m1 '^title:' "$f" | sed 's/^title:[[:space:]]*//')"
  type="$(grep -m1 '^type:' "$f" | sed 's/^type:[[:space:]]*//')"
  printf "  %-40s  [%s]  %s\n" "$(basename "$f")" "${type:-?}" "$title"
done
```

The date prefix in each filename sorts naturally; `-1t` also surfaces the most recent
first. After listing, exit — do not proceed to capture. To search **across** services
or by content, use `/sdd:doc-investigation-query`.

---

## What It Does

| Step | Action |
|------|--------|
| 1 | Reads the session, **suggests a type** (`bug`/`exploration`/`improvements`) and **asks the user to pick it** (unless forced via args), loads the matching template, and maps the narrative onto it |
| 2 | Detects the target service (the repo being investigated) for the registry key |
| 3 | Fills the template; marks gaps `[TBD]` / inferences `[INFERRED]` |
| 4 | Prints the full draft (with the chosen type) and the destination path |
| 5 | Writes it to `investigation-registry/<service>/<date>-<slug>.md` and reports the path |
| 6 | Confirms and lists what is now registered for that service |

---

## Step 1 — Classify, Load Template, Synthesize

### 1a — Classify the investigation type

Read the session and decide whether it was a **bug**, an **exploration**, or an
**improvements** plan:

- **`bug`** — there was a symptom: something broke, returned wrong data, threw, or
  behaved unexpectedly, and the session chased *why* and *how to fix it*.
- **`exploration`** — no defect; the session set out to *understand* a mechanism,
  flow, or feasibility ("how does X work?", "where would Y hook in?", "can we Z?").
- **`improvements`** — the session produced a **forward-looking plan**: it measured
  something against a requirement/standard, found gaps, and decided what to change
  ("does X meet Y?", "what should we fix?", a remediation/improvement plan). This is
  the only forward-looking type — bug and exploration are backward-looking.

Rules for choosing:
- If `$ARGUMENTS` contains `bug`, `explore`/`exploration`, or `improve`/`improvements`,
  that **forces** the type — use it and do **not** ask.
- Otherwise infer a *suggested* type from the session — a plan with proposed changes →
  `improvements`; understanding with no plan → `exploration`; a chased defect → `bug`;
  when genuinely mixed or ambiguous, suggest `exploration`. Then **ask the user to pick
  the type before drafting**, offering all three with the inferred one as the
  recommended default:

  ```
  Which template? (bug / exploration / improvements)  [recommended: <inferred>]
  ```

  Draft only once the type is chosen. Do **not** ask when the type was forced via
  `$ARGUMENTS`.

### 1b — Load the matching template

```bash
cat ${CLAUDE_PLUGIN_ROOT}/templates/investigation-bug.md           # type = bug
cat ${CLAUDE_PLUGIN_ROOT}/templates/investigation-explore.md       # type = exploration
cat ${CLAUDE_PLUGIN_ROOT}/templates/investigation-improvements.md  # type = improvements
```

### 1c — Map the session onto the template's placeholders

**bug** → Problem (one-line) · Symptoms (bullets) · Reproduction (how to trigger it;
`[TBD]` if not reproducible) · Investigation (what was checked + verbatim SQL/code) ·
Findings (facts) · Root Cause · Fix (fill the four fields: **Status**
applied/proposed/none-yet · **Where** `file` → symbol · **Change** the concrete edit ·
**Verify** how to confirm; mark any unknown field `[TBD]`) · Related Classes (bullets) ·
Future Signals (the "if you see X, check Y first" heuristic).

**exploration** → Question (what you set out to understand) · Context (why) · Map
(components/files/services and how they connect) · How It Works (the flow, step by step,
with verbatim traces) · Key Findings (the non-obvious) · Caveats & Gotchas · Open
Questions · Future Signals (where to start next time).

**improvements** → Goal (the requirement/standard and the bar for "done") · Current
State (the honest baseline) · Gap Analysis (one row per gap, each with an ADOPT /
PARTIAL / REJECT verdict + one-line rationale) · Plan (per ADOPT/PARTIAL item: the
concrete change, files/skills touched, effort; ordered cheapest/lowest-risk first —
written as a `- [ ]` **checklist** so a later agent sees what remains; a fresh capture
leaves every box unchecked and `status: proposed`) · Out of Scope (what is
*deliberately* rejected and why — as important as the Plan) · Open Decisions (calls a
human must make first) · Future Signals (where to pick it up).

Rules (all types):
- Pull **only** from what was discussed. Do not invent file names, classes, or SQL.
- Quote code and queries verbatim as they appeared in the session.
- Mark anything you deduce but wasn't stated outright as `[INFERRED]`.
- Mark any section with no session material as `[TBD]`.
- If `$ARGUMENTS` carries a title, use it to seed the first section (`# Problem` for
  bug, `# Question` for exploration, `# Goal` for improvements).
- If that first line is still ambiguous after reading the session, ask **one** concise
  question to nail it before drafting. Otherwise do not interrogate the user.

---

## Step 2 — Detect Target Service

The registry is keyed by service, the same way `/sdd:doc-catalog`, `/sdd:doc-adr`,
and `/sdd:doc-spec` key theirs — so an investigation, its ADRs, its specs, and its
catalog all line up under one `<service>` name.

Try in order (first hit wins), run from the repo under investigation:

1. `spring.application.name` from `application.yml` / `application.yaml` /
   `application.properties` — authoritative for Spring services.
2. git repo basename:
   ```bash
   git rev-parse --show-toplevel 2>/dev/null | xargs basename
   ```
3. If not inside a git repo (e.g., reviewing pasted code), ask for a short service
   name, or fall back to `unscoped`.

Lowercase the result. This becomes the `<service>` subdir.

---

## Step 3 — Build the Filename

Investigations are time-stamped, not numbered — the registry may be shared, so a
date prefix avoids collisions and sorts naturally.

```bash
DATE="$(date +%Y-%m-%d)"
```

Slug = the title line (Problem for bug, Question for exploration, Goal for
improvements), lowercased, non-alphanumerics → `-`, trimmed, max ~6 words. Filename:
`<date>-<slug>.md` — e.g. `2026-06-10-vehicle-lookup-stale-rows.md`.

Fill the template loaded in Step 1: replace its frontmatter placeholders
(`title`, `service`, `date`, `type`, `source` — `type` is already the right value in the
template you chose) and each section's `<…>` placeholders with the synthesized content.

Every template also carries `verified_at` — the code state the document was written
against, so a future reader can weigh staleness. Populate it from the repo under
investigation:

```bash
git rev-parse --short HEAD 2>/dev/null || echo untracked
```

Use `untracked` when not inside a git repo (e.g. pasted code). The `improvements`
template additionally carries `status` (default `proposed` on a fresh capture; lifecycle
`proposed → in-progress → done`, or `superseded` / `abandoned`) and `updated` (set to
today's date) — these are meant to be revised as the plan progresses.
The frontmatter is metadata only — it lets `/sdd:doc-investigation-query` cite and filter
by type — and the H1 sections below it (nine for bug, eight for exploration, seven for
improvements) are the document. Keep every heading even when a section is `[TBD]`.

---

## Step 4 — Show the Draft

Print the **entire** draft (frontmatter + all sections), the chosen **type**, and the
destination path, so the user sees exactly what is about to land — including any `[TBD]`
or `[INFERRED]` markers:

```
Type: <bug | exploration | improvements>
Writing to ~/.claude/investigation-registry/<service>/<file>
```

There is **no yes/no write gate** — the type was already chosen in Step 1a, so proceed
straight to Step 5 and write. The user can still interrupt to edit if something is wrong.

---

## Step 5 — Write

```bash
REGISTRY="${CLAUDE_DOC_HOME:-$HOME/.claude}/investigation-registry"
mkdir -p "$REGISTRY/<service>"
# Write the file with the Write tool to "$REGISTRY/<service>/<date>-<slug>.md"
```

- **Default**: `~/.claude/investigation-registry/<service>/`.
- **Override**: `export CLAUDE_DOC_HOME=/path/to/registry-root` (e.g. a cloned
  GitLab repo for team-shared findings) — writes under
  `$CLAUDE_DOC_HOME/investigation-registry/`. Same variable as every other registry.

---

## Step 6 — Confirm Registered

List the actual files now under that service so the user sees the result:

```bash
ls -1 "${CLAUDE_DOC_HOME:-$HOME/.claude}/investigation-registry/<service>"/*.md 2>/dev/null | xargs -n1 basename | sort
```

Then print a short confirmation and remind that `/sdd:doc-investigation-query` can
search across all captured investigations.

---

## Rules

- `list` is a reserved argument — when `$ARGUMENTS` is exactly `list`, run List Mode (read-only, current service only) and exit before any capture logic.
- Three fixed templates (`bug`, `exploration`, `improvements`) — pick one by type; never alter its shape (see Core Rule).
- Source is the session only — no fresh code scanning, no invented identifiers.
- `[TBD]` for missing, `[INFERRED]` for deduced — never silently fabricate.
- Ask for the type up front (Step 1a) unless forced via args; then always print the full draft before writing — no yes/no write gate.
- Writes go to the registry, not the investigated repo — never dirty someone
  else's working tree.

---

## Requirements

- A session containing an actual investigation to capture.
- Write access to `${CLAUDE_DOC_HOME:-$HOME/.claude}/investigation-registry/`.

---

## Related Skills

- `doc-investigation-query` — searches everything this skill captures
- `doc-adr` — for capturing a *decision* (immutable, supersede-only) rather than a finding
- `spec` (sdd bundle) — for forward-looking feature specs vs. backward-looking investigations
