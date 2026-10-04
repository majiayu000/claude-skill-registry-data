---
name: spec
description: Own the feature spec.md — draft it the first time from the source captured by /sdd:start, or refine an existing spec by feeding additional context (files, Jira tickets, pasted text, free text). Draft mode runs when no spec.md exists yet; refine mode integrates new context into an existing spec and is append-only on Open Questions. Refine with no arguments is a strict no-op. Runs triage on the first draft. Detects downstream staleness (plan.md, uncommitted changes) and only warns — never deletes downstream artifacts.
argument-hint: "<files> | jira <ticket> | paste | <free text>"
allowed-tools: Read, Write, Edit, Bash(cat .specwork/_spec/*), Bash(cat .specwork/_state/*), Bash(cat ${CLAUDE_PLUGIN_ROOT}/templates/spec.md), Bash(cat ${CLAUDE_PLUGIN_ROOT}/templates/spec-frontend.md), Bash(cat ${CLAUDE_PLUGIN_ROOT}/lib/jira.sh), Bash(ls .specwork:*), Bash(git rev-parse:*), Bash(git status:*), Bash(test:*), Bash(python3:*), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py:*), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/lib/triage.py:*), Bash(curl:*), Bash(printenv:*)
---

# Spec

Own `.specwork/_spec/<slug>-spec.md`. `/sdd:start` captures the raw source and
state; `/sdd:spec` turns that into the canonical spec and keeps it current.

`/sdd:spec` has two modes, chosen by whether the spec file already exists:

- **Draft mode** (no spec.md yet): generate the first spec from `source.md` and
  the spec template, fold in any context passed as arguments, then run triage.
- **Refine mode** (spec.md exists): integrate new context in place — resolve
  Open Questions, expand sections, record constraints. Append-only; never
  deletes user-authored content.

Refine mode with **no arguments** is a strict no-op: nothing to integrate, no
write, no mtime bump.

---

## When to use

- **Right after `/sdd:start`** — draft the spec from the captured source.
- **Resolve Open Questions** once you have the answer (a file, a Jira ticket, a
  paste, or free text).
- **Add scope** you forgot at `/sdd:start` — a specific endpoint, class, service.
- **Record constraints** that surfaced later (a PII rule, retry policy, SLA).

When **not** to use:
- The pipeline hasn't started — `.specwork/` is missing. Run `/sdd:start` first.
- You need to change the branch, ticket, or rules — those belong to
  `/sdd:start` / `/sdd:resync`.

---

## Prerequisites

Required artifacts (created by `/sdd:start`):

```text
.specwork/_state/<slug>-state.json
.specwork/_state/<slug>-rules.json
.specwork/_state/<slug>-implementation-cache.json
.specwork/_spec/<slug>-source.md
```

`spec.md` is **not** required — its absence is what selects draft mode. If any
of the artifacts above are missing, abort with no writes.

---

## Execution

| Step | Action |
|------|--------|
| 0  | Pipeline precondition — abort if `.specwork/` is missing or uninitialized via `gates.py precheck` |
| 1  | Resolve the slug from `.specwork/_state/` |
| 2  | Detect mode: draft (no spec.md) vs refine (spec.md exists) |
| 2.5| No-op gate: refine mode **and** zero arguments → print no-op notice and exit, no write |
| 3  | Verify required artifacts exist; abort with no writes if any are missing |
| 4  | Parse `$ARGUMENTS` into input items (files, jira ticket, paste, free text) |
| 5  | Fetch each input — read files, curl Jira via `lib/jira.sh`, capture pasted text |
| 6  | **Draft:** write the first spec from source + template + context. **Refine:** integrate context into the current spec. |
| 7  | Write the spec to `.specwork/_spec/<slug>-spec.md` (this bumps its mtime — downstream staleness is mtime-based) |
| 8  | Append newly confirmed classes/repos/tests to `implementation-cache.json` (dedupe, append-only) |
| 9  | **Draft only:** run `triage.py <slug>` now that the spec body has real content |
| 10 | **Refine only:** check downstream staleness — `plan.md` mtime, uncommitted git changes |
| 11 | Print result (draft summary + triage, or categorized refine diff + warnings) |

---

## Non-Interactive Behavior (STRICT)

If `SDD_NON_INTERACTIVE=1`, `/sdd:spec` must continue automatically and must not ask
for conversational confirmations between steps.

Allowed stops in this skill are only technical blockers:

- No active pipeline (`gates.py precheck` fails)
- Missing required artifacts
- Input fetch failure that prevents completing the action

`/sdd:spec` may print warnings (for example downstream staleness), but warnings are
not a pause condition in non-interactive mode.

### Post-write continuation (non-interactive only)

After writing the spec (Step 7), immediately run:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py check-oqs <slug>
```

- **Unresolved OQs remain** → print them with their line numbers and stop. The
  pipeline stays paused until `/sdd:spec` is called again with the answers.
- **No unresolved OQs** → continue the pipeline in this order, without pausing:
  1. Invoke `/sdd:plan`
  2. Invoke `/sdd:implement`
  3. Set `auto_open_mr_after_commit: true` in `.specwork/_state/<slug>-state.json`
  4. Invoke `/sdd:commit` — it runs the coverage gate, commits, and (with that
     flag set) continues automatically to `/sdd:mr`. **Stop at the open MR**;
     never invoke `/sdd:close` or `/sdd:mr-address`.

In non-interactive mode the pipeline runs straight through to the MR — the only
hard stop is unresolved Open Questions (above).

This is the mechanism that lets `/sdd:spec` resume a pipeline interrupted at the OQ
gate: the user resolves the questions, calls `/sdd:spec`, and the pipeline continues
automatically without having to re-run `/sdd:auto`.

---

## Step 0 — Pipeline Precondition Gate (STRICT)

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py precheck
```

If the exit code is non-zero, abort with no writes:

```text
✗ Cannot run /sdd:spec.
No active pipeline (.specwork/ missing or uninitialized). Run /sdd:start first.
```

---

## Step 1 — Resolve Slug

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py resolve-slug "$(git rev-parse --abbrev-ref HEAD)"
```

`resolve-slug` already handles the multiple-state-file case in code: given the
current branch, it returns the slug whose `state.json` `branch` field matches
(falling back to the first state file). If it prints nothing, no pipeline is
initialized — abort and tell the user to run `/sdd:start`.

---

## Step 2 — Detect Mode

```bash
test -f ".specwork/_spec/${SLUG}-spec.md" && echo "refine" || echo "draft"
```

- **draft** — spec.md does not exist. Generate it from source + template.
- **refine** — spec.md exists. Integrate new context in place.

To reset a spec from scratch, delete the file and re-run `/sdd:spec` (it will
re-enter draft mode).

---

## Step 2.5 — No-op Gate (refine + zero args)

If mode is **refine** and `$ARGUMENTS` is empty, there is nothing to integrate.
Exit cleanly without writing the spec (preserving its mtime) and without
printing integration instructions:

```text
Spec is already drafted (.specwork/_spec/<slug>-spec.md).
No arguments passed — nothing to refine, nothing changed.

To refine, pass additional context:
  /sdd:spec <file> [<file> ...]        — add file context
  /sdd:spec jira <TICKET>              — add Jira ticket context
  /sdd:spec "free text"                — add free text
  /sdd:spec <file> jira <TICKET> "..." — combine sources

Next:
  /sdd:plan        (discover target files)
  /sdd:implement   (start implementing — inline discovery if no plan)
```

`/sdd:spec` called twice in a row with no args is a no-op the second time. This is
what keeps `/sdd:plan` from seeing a spurious staleness bump.

---

## Step 3 — Verify Required Artifacts

```bash
for f in \
  ".specwork/_state/${SLUG}-state.json" \
  ".specwork/_state/${SLUG}-rules.json" \
  ".specwork/_state/${SLUG}-implementation-cache.json" \
  ".specwork/_spec/${SLUG}-source.md"; do
  [ -f "$f" ] || { echo "Missing: $f"; exit 1; }
done
```

`spec.md` is intentionally **not** in this list. If anything above is missing,
print the missing paths and abort with no writes.

---

## Step 4 — Parse Input

Inspect `$ARGUMENTS`. Arguments can mix multiple input types — process each
item independently:

| Pattern | Type | Action |
|---------|------|--------|
| Starts with `jira ` followed by a ticket key (e.g. `PROJ-1234`, `IR-122`) | jira | Fetch in Step 5 |
| Equals `paste` (or starts with `paste:`) | paste | Read pasted text |
| Contains `/` or ends in `.java`/`.kt`/`.ts`/`.tsx`/`.js`/`.py`/`.yaml`/`.yml`/`.json` | file | Read the file in Step 5 |
| Anything else | free text | Treat as inline guidance |

In **draft mode**, zero arguments is valid — the spec is drafted from
`source.md` alone. In **refine mode**, zero arguments was already handled by the
no-op gate in Step 2.5.

---

## Step 5 — Fetch Inputs

For each parsed item, fetch its content and remember its provenance label.

**File:**

```bash
[ -f "$PATH_TO_READ" ] && cat "$PATH_TO_READ"
```

If the path does not exist, note it as `[NOT FOUND: <path>]` later — do **not**
abort the whole skill for a missing file.

**Jira:**

```bash
source ${CLAUDE_PLUGIN_ROOT}/lib/jira.sh

if jira_is_ticket_key "$TICKET" && jira_is_configured; then
  jira_write_issue_markdown "$TICKET" "/tmp/spec-${TICKET}.md"
  cat "/tmp/spec-${TICKET}.md"
else
  echo "Jira not configured or invalid ticket key: $TICKET"
  echo "Set JIRA_BASE_URL + JIRA_USER + JIRA_TOKEN, or paste the ticket body instead."
fi
```

**Paste:** capture the pasted text from the conversation.

**Free text:** the inline argument is the content.

Concatenate everything into a single `CONTEXT` buffer, preserving provenance per
item — "from: `OrderController.java`", "from: jira IR-122", "from: paste", or
"from: inline".

---

## Step 6 — Build the Spec

The canonical section structure (both modes preserve it exactly — downstream
skills `/sdd:plan`, `/sdd:handoff`, `/sdd:whatnext`, `/sdd:state` parse by heading):

1. `## Summary`
2. `## Scope` (with `### In scope` / `### Out of scope`)
3. `## Behavior`
4. `## Implementation Context`
5. `## Expected Change Scope`
6. `## Safe Constraints` (with `**Safe**` / `**Unsafe**`)
7. `## Open Questions`

**Frontend variant**: when the project is a frontend stack (see *Template
selection* below), the spec also carries UI-specific sections inserted after
`## Behavior`: `## Components`, `## Props & State`, `## Routes`,
`## Design Reference`, `## Accessibility Requirements`. The seven canonical
headings above are still present and unchanged, so downstream parsing is
unaffected.

### Template selection (draft mode)

Pick the template that matches the project stack:

```bash
STACK="$(python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py detect-stack 2>/dev/null || echo unknown)"
case "$STACK" in
  frontend) TEMPLATE=${CLAUDE_PLUGIN_ROOT}/templates/spec-frontend.md ;;
  *)        TEMPLATE=${CLAUDE_PLUGIN_ROOT}/templates/spec.md ;;
esac
```

`java`, `node`, and `unknown` use the default `spec.md`. Only `frontend`
(a JS/TS project shipping a UI framework) uses `spec-frontend.md`.

### Draft mode

Read the source and the selected template:

```bash
cat ".specwork/_spec/${SLUG}-source.md"
cat "$TEMPLATE"
```

Write the first version of the spec, using the **source as the authoritative
input** and the template as the section structure. Rules:

1. Use the title from the source (slug + summary).
2. Fill every section the source supports with concrete content. For any
   section you cannot fill from source/context, leave a single Open Question
   rather than inventing detail.
3. Preserve the section order and headings from the template.
4. Open Questions are numbered (`#1`, `#2`, …) and use the format
   `- [ ] **#N** <question>`. List every unresolved ambiguity you would
   otherwise have to guess.
5. NEVER touch `.specwork/_spec/<slug>-source.md` — it is immutable.

If context (files, jira, free text) was supplied, fold it into the relevant
sections as you draft.

### Refine mode

Read the current spec, keep the previous content in memory (Step 11 needs it for
the diff), then integrate the new `CONTEXT`:

| If the input is... | Then... |
|--------------------|---------|
| A file referencing a class / endpoint / service relevant to the feature | Add the symbol to `## Implementation Context` with a one-line note. If the file's signature answers an open OQ, mark that OQ resolved. |
| A Jira ticket body / comments | Authoritative. Behaviors → `## Behavior`. Constraints → `## Safe Constraints`. Scope hints → `## Expected Change Scope`. Cite the ticket in the diff. |
| Text that answers an existing OQ (`#N`) | Flip `- [ ] **#N**` → `- [x] **#N**` and append ` — resolved: <answer>`. Preserve the question text. |
| Text introducing a new rule (PII, SLA, retry, idempotency) | Add to `## Safe Constraints` under `**Safe**` or `**Unsafe**`. |
| Text expanding scope | Add to `## Implementation Context` and adjust `## Expected Change Scope`. |
| Anything ambiguous | Append a **new** Open Question with the next `#N`. Do not guess. |

Hard preservation rules (refine):
- **Never delete user-authored content.** OQ resolutions append `— resolved:`;
  they never remove the question text.
- **Never invent class names.** Use the symbol verbatim, or write `[UNKNOWN]`.
- **Never modify `## Summary` or the title** unless the input explicitly
  contradicts them — if it does, surface the conflict as a new Open Question
  instead of silently rewriting.
- **Never touch `source.md`** (immutable) or regenerate `rules.json`
  (that's `/sdd:start`'s job).

---

## Step 7 — Write the Spec

Write the spec to `.specwork/_spec/${SLUG}-spec.md`. Every write bumps the file
mtime — that is the signal `/sdd:plan` and `/sdd:implement` use to detect a stale
plan. There is **no separate timestamp bump**; the mtime is the source of truth.

In refine mode, if integration produced **no actual change** (no OQ resolved, no
scope addition, no constraint, no warning), do **not** rewrite the file —
preserving the original mtime is what tells `/sdd:plan` there is nothing to
regenerate. Print the "No changes to the spec" notice from Step 11 instead.

---

## Step 8 — Update Implementation Cache

If Step 6 confirmed any new classes, repositories, or tests, append them
(append-only, deduped — never remove prior entries):

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py merge-cache <slug> '{"similar_classes":[],"related_tests":[],"repositories":[]}'
```

---

## Step 9 — Triage (draft mode only)

On the first draft, run triage now that the spec body has real content. Triage
classifies on `## Summary` + `## Behavior`; until `/sdd:spec` draft writes the
spec, triage has nothing to classify — which is why it lives here, not in
`/sdd:start`.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/triage.py <slug>
```

This writes `.specwork/_state/<slug>-path.json` with one of four advisory
classifications (`trivial` / `focused` / `standard` / `high-risk`) and the
recommended pipeline path. Print the result (type, complexity, path, reason).
The path is advisory — the developer can override at any step.

---

## Step 10 — Staleness Detection (refine mode only)

**plan.md staleness (by mtime):**

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py check-staleness <slug> && echo "PLAN_FRESH" || echo "PLAN_STALE"
```

**Uncommitted changes:**

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/worktree.py is-clean || echo "DIRTY_WORKTREE"
```

If either fires, surface it in Step 11. **Never delete or rename downstream
artifacts** — the user runs `/sdd:plan` themselves to regenerate.

---

## Step 11 — Print Result

### Clickable paths

Whenever output references the spec or its Open Questions, use the canonical
format documented across `/sdd:whatnext`, `/sdd:plan`, `/sdd:start`, `/sdd:state`: an
**absolute path with the line number of the `## Open Questions` heading**,
wrapped in single backticks so Claude Code renders it as a clickable token.

```bash
SPEC=".specwork/_spec/${SLUG}-spec.md"
ABS_SPEC="$(cd "$(dirname "$SPEC")" && pwd)/$(basename "$SPEC")"
OQ_LINE="$(grep -n "^## Open Questions" "$SPEC" | head -1 | cut -d: -f1)"
# Use `${ABS_SPEC}:${OQ_LINE}` (wrapped in backticks) wherever output references OQs.
```

Do **not** wrap the whole output block in a fenced code block — fenced blocks
suppress inline-code coloring on the path. Emit it as plain markdown text.

### Draft mode output

```text
Spec drafted: `/abs/path/repo/.specwork/_spec/<slug>-spec.md:42`  ← Open Questions

Triage:  standard (MEDIUM)
Path:    /sdd:plan → /sdd:implement → /sdd:commit → /sdd:mr
Why:     3 layers (controller, service, repository), no high-risk signals.

Open Questions: 3 open
  Resolve them in `/abs/path/repo/.specwork/_spec/<slug>-spec.md:42` before /sdd:plan
  (re-run /sdd:spec with the answers as context).

Next:
  /sdd:plan        (recommended for 3+ files)
  /sdd:implement   (small / obvious changes — inline discovery)
```

When the draft has zero Open Questions, drop the OQ lines and shorten `Next:`.

### Refine mode output

Emit only sections that actually changed; omit empty ones.

```text
Spec refined: `/abs/path/repo/.specwork/_spec/<slug>-spec.md:42`  ← Open Questions

Open Questions:    5 → 3
  ✓ Resolved #1 — Use UUID for personId        (from: OrderController.java)
  ✓ Resolved #3 — Notifications are fire-and-forget, no retry   (from: paste)
  ⚠ Still open:  #2, #4, #5
      `/abs/path/repo/.specwork/_spec/<slug>-spec.md:42`  ← Open Questions

Implementation Context:
  + OrderController.createOrder()        (from: OrderController.java)
  + PaymentClient (Feign)                (from: paste)

Safe Constraints:
  + Unsafe: Logging unmasked PII fields  (from: jira IR-122)

Downstream artifacts (now potentially stale):
  ⚠ .specwork/_plan/<slug>-plan.md is older than the spec
    Run /sdd:plan to regenerate (it is idempotent — overwrites in place).
  ⚠ Working tree has uncommitted changes
    Review them against the new spec before committing.

Next:
  Resolve Open Questions in `/abs/path/repo/.specwork/_spec/<slug>-spec.md:42` (3 open).
  Then /sdd:plan (recommended — plan is stale).
  Or /sdd:implement if no plan exists / plan is still valid.
```

When **all** OQs are resolved, drop the OQ-related lines and shorten `Next:` to
the pipeline-step commands.

If refine produced no change, print:

```text
No changes to the spec.

The input did not produce any updates — either the spec was already up to date,
or the input didn't match any actionable category. The file mtime was not
modified.
```

---

## Hard Rules

- Never delete user-authored content in the spec. Resolutions append; they do
  not remove.
- Never modify `.specwork/_spec/<slug>-source.md`. The original source is
  immutable.
- Never regenerate `.specwork/_state/<slug>-rules.json`. That belongs to
  `/sdd:start`.
- Append-only on `implementation-cache.json` — never remove prior entries.
- Never delete, rename, or modify `.specwork/_plan/<slug>-plan.md`. Only warn
  that it's stale.
- Never modify git state — no commits, no branches. Read-only `git status` only.
- Refine + zero args is a strict no-op — no write, no mtime bump.
- If required artifacts are missing, exit cleanly with no writes.
- Preserve the spec template's section order and headings exactly.

---

## Related Skills

- `start` — captures the source and state that `/sdd:spec` turns into the spec;
  it does **not** create spec.md.
- `plan` — idempotent re-run absorbs spec updates; the staleness warning here
  recommends running it.
- `implement` — blocks on unresolved Open Questions; refining the spec to
  close OQs unblocks it.
- `handoff` — reads the latest spec; running `/sdd:spec` before `/sdd:handoff`
  ensures the execution pack is current.
- the old `spec-refine` alias has been removed — use `/sdd:spec` (refine mode) instead.
