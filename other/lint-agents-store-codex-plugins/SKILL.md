---
name: lint
description: This skill should be used when the user asks to "validate macstack.json", "lint macstack", "check the stack spec", "verify macstack.json integrity", "check the documents", "where are we", "what should I do next", "project status" — and after any skill of this plugin writes or edits macstack.json or a document under macstack/. Validates the spec against the JSON Schema and the referential-integrity rules, checks the document folder, and reports the same findings read-only as a status dashboard.
---

# Check the spec, the folder, and where the project stands

Three passes over the spec and the folder, and one read-only view of the result.

A file that fails lint must not be scaffolded from.

Resolve the path first: `macstack/macstack.json` (canonical) → `./macstack.json`
(legacy fallback). Both present is a setup error — stop instead of picking one
silently.

**Prefer the reference linter** — it implements passes 1 and 2 and is maintained with
the standard:

```bash
MACSTACK_JSON="macstack/macstack.json"; [ -f "$MACSTACK_JSON" ] || MACSTACK_JSON="macstack.json"
curl -fsSL https://raw.githubusercontent.com/macstacks/macstack/main/scripts/lint.py \
  -o "${CLAUDE_PLUGIN_DATA}/lint.py" 2>/dev/null || true   # cache; keep the old copy offline
python3 "${CLAUDE_PLUGIN_DATA}/lint.py" "$MACSTACK_JSON" \
  --schema https://raw.githubusercontent.com/macstacks/macstack/main/schema/macstack.schema.json \
  --categories https://raw.githubusercontent.com/macstacks/registry/main/software-categories.json \
  --coverage-areas https://raw.githubusercontent.com/macstacks/registry/main/coverage-areas.json
```

Pass 3 is this plugin's own and has no upstream equivalent — run it either way.

Offline fallback: run all three passes manually with the bundled copies.

## Pass 1 — JSON Schema

Fetch the live schema first (it may be newer than the bundled copy); cache it in
`${CLAUDE_PLUGIN_DATA}`; offline → bundled
`${CLAUDE_PLUGIN_ROOT}/skills/lint/references/macstack.schema.json`.

```bash
python3 - <<'PY'
import json, jsonschema, urllib.request, os
URL = "https://raw.githubusercontent.com/macstacks/macstack/main/schema/macstack.schema.json"
try:
    schema = json.load(urllib.request.urlopen(URL, timeout=15))
except Exception:
    schema = json.load(open("<PLUGIN_ROOT>/skills/lint/references/macstack.schema.json"))
path = "macstack/macstack.json" if os.path.exists("macstack/macstack.json") else "macstack.json"
jsonschema.validate(json.load(open(path)), schema)
print("schema: VALID")
PY
```

**Compare revisions before trusting a difference.** Both copies carry a `$comment`
starting `rev <n>`. If the fetched one is older than the bundled one, the bundled copy
is ahead of the canon on purpose and must not be overwritten — and a `curl` against
`raw.githubusercontent.com` immediately after a push serves the PREVIOUS revision from
the CDN, which prints a full, entirely false diff. Use
`gh api repos/macstacks/macstack/contents/<path>?ref=main` when the answer matters.

No `jsonschema` lib → fall back to structural checks (required: macstack, name,
version, description; the known enums) — and tell the user that full validation was
skipped.

## Pass 2 — Referential integrity (errors)

1. `results[].produced_by[*]` ∈ processes; `processes[].produces[*]` ∈ results —
   result-first: a process with no result is "coding for coding's sake".
2. `results[].goal` ∈ goals.
3. `tasks[].workflow`, `workflows[].software`, `entities[].stores[].software`,
   `interfaces[].software|related[*]`, `connections.mcp[].software` resolve
   (own ids, ids inherited from the prototype, or cross-stack).
4. `entities[].master` appears in stores exactly once with the master role.
5. **Triggers**: `workflows[].triggers[*]` ∈ triggers; `triggers[].software` ∈
   software, `instance` ∈ its instances.
6. **Instances**: `stores[].instance`, `mcp[].instance` ∈ the instances of the
   matching software; `interfaces[].instances[*]` ∈ the instances of its software.
7. `software[]`: category ∈ the registry
   (`references/software-categories.json`), type filled, layers ⊆
   {data, logic, interface, infrastructure} without duplicates, `agentic.rating`
   consistent (3×true=full, 2=good, 1=basic, only partial=partial, nothing=none).
8. **Cross-stack**: the `<stack-id>:` prefix is declared in `stacks.root.id` /
   `stacks.substacks[].id` / `stacks.links[].id`; `role: substack` → `root` present.
9. **Agents**: `stack_agents[].access[*]` ∈ mcp|software|interfaces;
   `delegates_to` only downward (control_plane → orchestrator → worker);
   `context_packs[*]` ∈ context.packs; `managed_agents[].tools.*` resolve;
   `invocations[*].interface|workflow|trigger` resolve.
10. **Env**: `resources.accesses[].env` holds NAMES, not values (a string that looks
    like a secret/token is an error); slugs are kebab-case; `prototype` has no cycles.
11. **Plugin coverage**: `context.plugins.*[].covers[*]` ∈ the coverage registry
    (`references/coverage-areas.json`); `scope[*]` resolves to a declared id in
    software / entities / workflows / triggers / interfaces / connections.mcp.

## Pass 3 — The `macstack/` folder (rule group 12)

Active only when macstack.json has a `docs` section, or a `macstack/` folder exists
on disk. Errors block scaffolding exactly like Pass 2; lint red on a document that
reads fine usually means stripped anchors (see `troubleshoot`).

**Run it — this pass is a program now:**

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/lint/references/lint_folder.py" macstack \
  [--rule 12.3 ...] [--warnings] [--json]
```

Exit 0 clean, 1 errors, 2 could not load. Rules live in `references/lint_folder.py`
and the `references/rules_*.py` modules beside it, which register themselves on import.

Until v3 this pass was prose and nothing executed it, which is why 12.21 demanded a
fenced `yaml` block from documents that contain none and never once said so, and why
12.18 was unsatisfiable for `README.md` across three releases with no way to tell
whether it was failing or simply not running. **A rule nobody can run is not a rule.**
If you add one here, add it there in the same change.

Read the shape from
`${CLAUDE_PLUGIN_ROOT}/skills/documents/references/doc-contracts.json` — every rule
below is checked against that file, never against memory.

### The forty-one rules

The full catalogue — what each rule checks, what it costs to ignore, and the measurement
that bought it — is in
`${CLAUDE_PLUGIN_ROOT}/skills/lint/references/rules-group-12.md`.

Read it when adding a rule, when a finding needs explaining to somebody, or when
deciding whether a red rule is worth the fix. The runner needs none of it: it prints the
rule number, the file, the line and a verbatim excerpt, because "this table is too wide"
is not actionable and "cell 4 of row 12 is 876 characters" is.

## Warnings (non-blocking)

- A goal with no result ("a goal with no path to it"); a result with no goal when
  goals are non-empty.
- A trigger referenced by no workflow and no agent.
- `TEST-CASES.md` derived from an older version of a source document than the current
  one (name both versions) — the coverage count is stale by definition.
- A `Z-` prohibition whose tests assert the refusal but not that the refusal explains
  itself.
- An `X-` cross-cutting case whose tests name no roles to run as.
- A case with no `experience` section (outside the `Z-` space) — the UX bar for that
  case was never stated, so `UX-UI.md` has nothing to answer.
- A screen in `UX-UI.md` that no case names in its `screens` key.
- Software without an agentic passport; a required key missing from `.env`.
- **Coverage gap**: a non-empty tooling-backed section — software, entities, workflows,
  triggers, interfaces, connections — that no plugin `covers`. Say which. Do NOT
  gap-check goals, results, processes, roles or integrations: those are authored by the
  architect, not taught by a plugin, and demanding a plugin for them only produces fake
  entries.
- **Plugin without `covers`** (including the legacy bare-slug form): an agent cannot
  route to it, so it will be either ignored or loaded blindly.
- **Ambiguous coverage**: an area claimed by 2+ plugins where none narrows it with
  `scope`.
- **Unprocessed source**: a file in `inbox/` with no `merge` entry naming it.
- `lifecycle.updated` older than the newest `history/ledger.jsonl` row (name the date).
- **The project has gone quiet**: a task sitting in `in_progress` while the ledger has had no
  `work` entry for 14 days. The older staleness check compares `lifecycle.updated`
  against the newest log entry, and with no client input both freeze in agreement — a
  project can run for months with a perfectly green lint and no record of the work.
  This is the rule that notices.
- An §A open item past its age budget (warn 14 days, error 45), or with no `asked_on`
  date — a question nobody has actually put to the client is not blocked, it is
  forgotten.
- An §A item that one or more tasks name in `blocked_by` — say how many. That count is
  the argument for chasing the client today rather than next month.
- A task with no `spec` pointer, or whose `acceptance` names no test. Without `spec`,
  `update` cannot tell which documents a finished task touched.
- A `BL-<n>` promoted to a task without the original being struck with a pointer.
- Legacy free-text entries in `lifecycle.next_steps`.
- A `roles[]` entry with no `cases`; a `sees`/`can` longer than one sentence.
- A `-conformance.md` review with no `-business.md` twin of the same date and slug.
- A delta aged 14–30 days with no applied banner.
- `docs.language` absent while the documents are visibly not English.
- An `inbox/` file heavier than 5 MB.

## Judgment checks (documents)

| Check | What it flags |
|---|---|
| Duplicate content | The same fact stated in both `OVERVIEW.md` and `USER-CASES.md` |
| Superseded documents | A document contradicted by a newer source with no note pointing to it |
| Cross-role contradictions | Two role sections disagreeing on the same behaviour |
| Coverage gaps | An entity or workflow in the spec that no case touches |
| Prose that wants a section | A YAML value carrying a sentence where a section exists for it |

## Output

`ERRORS` as a list (the file is not scaffold-ready) → `WARNINGS` → one
`OK: schema + N integrity rules` line. With a prototype set — resolve and merge first,
lint the merged document.

When rule group 12 is active, append a documents block:

```
Documents: 🟢 OK | 🟡 N warnings | 🔴 N errors
1. <next step>
2. <next step>
```

🔴 on any 12.x error, 🟡 on a documents warning with zero errors, 🟢 otherwise.
Number the next steps in the same order as ERRORS/WARNINGS above (fix errors first).

## Status mode — the same findings, read-only

`/macstack-dev:check` with no argument runs everything above and then renders one
screen. **It writes nothing.** Status is not a second engine with its own predicates:
v1 had `status` re-implement seven checks that rule group 12 already made, in a second
place that could disagree with the first. There is one engine now, and two ways of
printing it.

```
<project> · <stage> · spec v<version>

Spec        🟢 schema + 11 rules
Documents   🟡 3 warnings          (12.17 ×2 · 12.11 ×1)
Milestone   M11 · in_progress ▶ · 6/9 tasks · 3 of 5 done_when recorded
Client      2 open §A · oldest 21 days · 1 blocking M11-T9
Quiet for   4 days since the last `work` entry

Next
1. Chase A5 — M11-T9 is blocked on it and it was asked 21 days ago
2. UX-UI.md was last checked against the code 41 days ago — /macstack-dev:check --code
3. 4 acceptance bullets have no test — /macstack-dev:update
```

Order the attention list by cost of ignoring it, not by rule number. A blocked task
with a client dependency outranks a stale `reviewed` date, which outranks a formatting
warning.

`--docs` limits the run to pass 3 and the judgment checks. `--code` hands over to
`conformance`, which is the only mode that reads the source tree.