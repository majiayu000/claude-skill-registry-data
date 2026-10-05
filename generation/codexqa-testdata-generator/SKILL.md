---
name: codexqa-testdata-generator
description: >-
  Constructs test data against real backends and writes it back into test cases
  as executable preconditions. Use whenever the user wants test data built, case
  materials or preconditions prepared, a data-build skill or tool reused, an API
  discovered, a construction script written, or a proven method recorded —
  including Chinese phrasings such as 构造测试数据, 准备测试数据, 造数据, 用例数据,
  用例物料, 用例数据准备, 用例前置数据, 测试数据回写, 测试物料清单, 数据需求分析.
  Also use it for concrete requests that never say "test data", like "create this
  account from the OpenAPI", "build a script from these change APIs", "publish
  that script as a tool", or "scaffold a new domain from this OpenAPI directory".
  Not for authoring test cases from a PRD (that is
  codexqa-testcase-generator) or finding defects in code (that is codexqa-defect-analyzer).
  Bundled slots and sub-skills here are internal; reach them through this skill.
  Former skill name: testdata-generation.
license: Apache-2.0
compatibility: >-
  Requires Node 22+ on PATH; scripts run on the Node standard library with no
  runtime npm dependencies. Works fully offline against local files and the
  bundled mock server; enterprise platforms are opt-in HTTP adapters.
metadata:
  author: codexqa-testdata-generator contributors
  version: "1.0"
  open-standard: agentskills
---

# Test Data Generation

This directory is the skill. It has no baked-in company knowledge.
Platforms are adapters; local files work with zero extra infrastructure.

**This skill never invents business data.** It decides which path to take and
extracts parameters the user already supplied; an executor, a published tool, or
a generated script is what actually calls the backend. "Construct succeeded"
means the backend returned a business ID, not that an ID appeared in the reply.

`SKILL_DIR` is the folder that contains this `SKILL.md`. Every command below
uses it, so resolve it once:

```bash
SKILL_DIR="<directory of this SKILL.md>"
```

Config lookup: `$DATA_BUILD_CONFIG` → `./testdata/config.yaml` → `~/.testdata/config.yaml`.

Four fallback paths, in this order, after the case-material check below:

1. **Domain skill** — search for a matching data-build skill, install or load it, and delegate
2. **Existing tool** — reuse a published tool from the tool registry
3. **API catalog** — discover the APIs that can build the data
4. **Generated script** — write a construction script from those APIs and run it

## Documents (load on demand)

Read this file first; it is the routing contract. Load anything else only when
the row below applies, so a single-step construct does not drag the whole tree
into context.

| File | Load when |
|---|---|
| `SKILL.md` (this file) | always: routing, priorities, guardrails |
| [references/case-data-material-planner/SKILL.md](references/case-data-material-planner/SKILL.md) | the request is a case-material job (see the next section) |
| [references/workflow.md](references/workflow.md) | you need the full command syntax, experience-report payloads, or the FAQ for steps 1–4 |
| [references/adapters.md](references/adapters.md) | wiring an enterprise platform, or an adapter behaves unexpectedly |
| [references/script-template.ts](references/script-template.ts) | writing a step-4 construction script |
| [slot-scaffolder/SKILL.md](slot-scaffolder/SKILL.md) | building a reusable domain pack from OpenAPI |
| [slots/SLOT_SPEC.md](slots/SLOT_SPEC.md) | authoring or reviewing a slot contract by hand |
| `README.md` / `README.zh-CN.md`, [HOW_IT_WORKS.md](HOW_IT_WORKS.md), [INSTALL.md](INSTALL.md), [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md) (and `.zh-CN.md`) | human-facing: install, operations, method, and known gaps. Not needed by the agent |

---

## Case-material route (check first)

After receiving a data-construction request, **first** decide whether it is a case-material job.

**Trigger phrases** (any match enters the sub-skill and **stops** the generic flow):

- English: case data, case materials, test-data preparation, write back test data,
  data requirements, data inventory, prepare test data, test material list
- Chinese: 用例数据, 用例物料, 用例数据准备, 为用例准备数据, 用例前置数据,
  测试数据回写, 用例数据构造, 测试数据分析, 测试物料, 数据需求分析,
  测试数据准备, 数据物料, 需求测试数据, 准备测试数据, 测试物料清单, 数据诉求

**On hit**: load and follow [references/case-data-material-planner/SKILL.md](references/case-data-material-planner/SKILL.md). Run `references/case-data-material-planner/scripts/pipeline.ts` as the orchestrator (paths below are relative to that sub-skill root) — construction, binding, and writeback are stages inside that script, so do not spawn Agents to do them.

The sub-skill root is `<this SKILL.md directory>/references/case-data-material-planner/`.
All of its `scripts/`, `agents/`, `templates/` paths are relative to that root.

---

## Decision tree

Handle every other request **in this exact order**:

```
user data-construction request
    │
    ▼
[route] case-material scene? (phrases above)
    │
    ├─ yes → load references/case-data-material-planner/SKILL.md  ✓ stop
    │
    └─ no → generic flow
            │
            ▼
        [step 1] search_data_build.ts
                 (semantic proven methods + skill marketplace, in parallel)
            │
            ├─ pinned_matches present AND Agent judges them relevant
            │       → load skillPath (or install) → delegate → report  ✓ stop
            │
            ├─ proven_matches present AND Agent judges them applicable
            │       → run proven_invocation → feedback only  ✓ stop
            │
            ├─ skill_matches: one local clear match
            │       → load → delegate → report  ✓ stop
            │     several / weak / needs install → ask, then same
            │
            └─ none match
                    │
                    ▼
                [step 2] tool_registry.query (two query angles)
                    │
                    ├─ one clear tool (or user already gave an id)
                    │       → query_input_list → fill params → execute → report  ✓ stop
                    │     several / weak → ask, then same
                    │
                    └─ no matching tool
                            │
                            ▼
                        [step 3] api_catalog (in parallel when useful)
                            │
                            ├─ method A: plan change APIs (if planId exists)
                            └─ method B: keyword / service search
                            │
                            ▼
                        [step 4] write script from template
                            │
                            ├─ generate → run locally → report
                            └─ after a successful run, ask whether to publish
                                    ├─ yes → tool_registry.publish  ✓ stop
                                    └─ no  → return the result     ✓ stop
```

---

## Step 1 — Search matching data-build options

### Build the search input

Extract two kinds of input from the user request:

**Keywords** (skill-name match):

- Take 1–2 nouns that name the domain slot, such as the name in `slot.yaml`
- **Never** use verb phrases such as "create a" or "help me construct"
- If keywords miss, the script **falls back to a full scan**. Do not retry by hand.

**Structured query** (semantic match):

- `registry-key`: `{entity}::{action}`, e.g. `catalog-order::create`
- `query`: one natural-language sentence
- `entry-type`: `entity` or `action`
- `domain`: from workspace context `business_line`, or infer from the request

Examples and the full command: [references/workflow.md](references/workflow.md).

```bash
node "$SKILL_DIR/scripts/search_data_build.ts" \
  --keywords <nouns> \
  --query "<sentence>" \
  --registry-key "<entity>::<action>" \
  --entry-type entity \
  --domain "<domain>" \
  --json
```

The script runs proven-method search and skill-marketplace search **in parallel**,
then injects pinned favorites. JSON shape:

```text
{
  "pinned_matches": [...],
  "proven_matches": [...],
  "skill_matches": [...]
}
```

### Result priority

**Priority 0 — `pinned_matches` (highest)**

Pinned skills are returned unconditionally so retrieval noise cannot drop them.

The **Agent** judges relevance from each item's `description` (same idea as proven applicability):

- Relevant → use it first. Prefer `skillPath` when `SKILL.md` exists.
  If `available=false` or `skillPath` is missing, install then load.
- Not relevant → ignore and continue to proven / skill matches.

The script does **no** keyword filter on pinned items. A relevant pinned hit
ends step 1; do not evaluate proven/skill after that.

**Priority 1 — `proven_matches`**

Reuse only when **all three** hold:

1. **Semantic alignment**: `registry_key` describes the same operation
2. **Tool reachable**: the bound skill is installed or the bound tool can execute
3. **Params available**: required `proven_invocation.paramMapping` values exist in context

All three → execute `proven_invocation` and keep `experience_id` for feedback.
Any miss → skip that row and continue to `skill_matches`.

**Priority 2 — `skill_matches`**

Asking is for ambiguity, not ceremony. The user already asked to construct
data. Drop rows whose description does not cover the request (a catalog-product
construct is not a distributor slot, even if both appear in `skill_matches`).

- **One remaining local match** (`skillPath` already has `SKILL.md`) → load
  it, say which skill you used, and stop. Do not ask first.
- **Needs install** (`available=false` or no `skillPath`) → ask, because
  install is a side effect the user did not request.
- **Two or more remaining rows that could both be right, or only a
  weak/partial match** → show them and ask:
  **"Which of these skills matches your request, if any?"**

None match → go to step 2.

If search is empty **and** the user wants a reusable domain pack (not a one-off
construct), read `$SKILL_DIR/slot-scaffolder/SKILL.md` and follow it. That is a
bundled folder in this skill, not a separately installed skill — do not go
looking for it in the host's skill list. One-off work continues at step 2.

### Install and load a confirmed skill

```bash
SKILLS_DIR="$(dirname "$SKILL_DIR")"
node "$SKILL_DIR/scripts/adapters/cli.ts" skill_marketplace.install '<name>' '$SKILLS_DIR'
```

If `skillPath` already points at a directory that contains `SKILL.md`, load it
directly and skip install. After load, follow that skill and **stop**.

### Pin favorites (personal cheat-sheet)

Pinned skills always enter the candidate set first. Relevance is Agent-judged.

| User says | Command |
|---|---|
| pin this skill | `node "$SKILL_DIR/scripts/favorites.ts" add --name "<name>" --desc "<when to use>" --path "<dir with SKILL.md>"` |
| show pinned | `node "$SKILL_DIR/scripts/favorites.ts" list` |
| unpin | `node "$SKILL_DIR/scripts/favorites.ts" rm --name "<name>"` (or `--uuid` / `--id`) |
| verify pinned | `node "$SKILL_DIR/scripts/favorites.ts" verify` |

Storage: project `./testdata/data-build-favorites.json`, user `~/.testdata/favorites.json`.
`add` writes the user file unless `--scope project`. `$DATA_BUILD_FAVORITES_PATH` overrides both.

---

## Step 2 — Tool registry (only when no skill matched)

Query with **natural-language sentences**, not space-separated keywords.

Write **at least two** angles:

| Angle | Intent | Example |
|---|---|---|
| A | construct / create | `create a catalog test product` |
| B | business flow | `customer books a standard product` |

```bash
node "$SKILL_DIR/scripts/adapters/cli.ts" tool_registry.query "create a catalog test product"
```

If the user already has a tool id, look it up exactly:

```bash
node "$SKILL_DIR/scripts/adapters/cli.ts" tool_registry.get "<resource-id>"
```

- User already named a tool id, or exactly one result clearly matches → use it.
  Tell the user which tool you picked.
- Several results or only a weak match → show them and ask:
  **"Is there a tool that matches your request?"**

Then:

1. `tool_registry.query_input_list(resource_id)`
2. Fill params. **Order IDs, user IDs, and other core business fields must be confirmed with the user. Do not invent them.** Optional fields may use sane defaults.
3. `tool_registry.execute(resource_id, params)`
4. On success → report (see below)

---

## Step 3 — API catalog

### Method A — plan change APIs (preferred when a plan exists)

Use when the request sits inside a test-plan / change scope.

Resolve `planId` from workspace context `testPlan.id` or `planId`. If missing, **ask the user**.

```bash
node "$SKILL_DIR/scripts/adapters/cli.ts" api_catalog.search_plan_changes "<planId>"
```

Then `api_catalog.detail(<operationId>)` for key operations.

### Method B — keyword / service search (fallback)

Use when there is no `planId`, or plan APIs are weakly related.

**First**: read workspace context `targetRepositories[].serviceId` or `relatedJobs[].serviceId`.
If a service id is already known, list its APIs directly:

```bash
node "$SKILL_DIR/scripts/adapters/cli.ts" api_catalog.list_by_service "<serviceId>" "<optional-name-filter>"
```

**Second**: keyword search. Use **one precise token**, not a long Chinese/English phrase.

```bash
node "$SKILL_DIR/scripts/adapters/cli.ts" api_catalog.search "create catalog product"
```

Then `api_catalog.detail(<operationId>)`.

If the workspace has no API source at all (no OpenAPI files, no `planId`, no `serviceId`), **stop and ask** for a plan, a service id, or an OpenAPI directory. That is a material gate, not a field-by-field param review. Do not invent endpoints.

### Combination

| Situation | Strategy |
|---|---|
| Has `planId`, request matches the change | **A first**: plan APIs → detail key ops |
| Has `planId`, change is weakly related | **A + B**: inspect the change, then search by request |
| No `planId` | **B**: service id if known, else keyword search |
| User already named a service / API | **B**: `list_by_service` or `search` + `detail` |

---

## Step 4 — Write and run a construction script

Write `./testdata/<name>.ts` from [references/script-template.ts](references/script-template.ts), then run it.

Required shape: shebang + docstring, top-level constants, `main(params) -> {success, data, error}`, CLI entry via `import.meta.url`.
Use adapter helpers only: `callHttp`, `callSql`, `getConfig`, `callFeatureFlag`.

Rules:

- Child-process calls use argument lists, never `shell: true`
- Timeouts on every network call
- Coerce `object` / `array` / `bool` / `number` with `typeof` / `Array.isArray`
- Do not invent order IDs, user IDs, or amounts

**Feature flags** (only when the user asks for experiments, drafts, or whitelists
and `feature_flags.type` is not `noop`): confirm the environment before writes;
production writes need a second confirmation; one subject per call.
`toolType` for a successful flag script is `feature_flag`.

After a **successful local run**, ask whether to publish to the tool registry.
Do not publish before a successful run.

```bash
node "$SKILL_DIR/scripts/adapters/cli.ts" tool_registry.publish '<name>' '<what the script does>' './testdata/<name>.ts' '[{"name":"<param>","type":"string","required":true}]'
```

---

## What to tell the user

Report the business outcome, because that is the only part the user can act on.
Lead with the identifiers the backend returned, then how they were produced, then
anything still needed:

```markdown
Constructed <what>: <field>=<value>, <field>=<value>
Path: <domain skill | registry tool | generated script> (<name>)
Next: <what the user can do with it, or what is still missing>
```

Keep infrastructure out of it — `skillRoot`, absolute paths, mock ports, `node …`
invoke lines, and adapter names are noise to the person who asked for data, and
in a case document they are actively wrong (see the writeback rules). Also say
which environment produced the IDs when it was the local mock, since a mock ID
looks identical to a real one but nothing landed in a real system.

If a path failed and you fell through to the next one, say so in one line rather
than narrating every attempt.

## Success follow-up (after any successful path)

Non-blocking. A report/feedback failure must not hide a successful construct.

**When to report vs feedback:**

- Step 1 proven hit that ran successfully → **feedback only, do not report again**
- Step 1 skill delegate succeeded → report
- Step 2 tool execute succeeded → report
- Step 4 script succeeded → report
- Step 4 published after a successful run → report with the published resource id

Payloads and `toolType` mapping: [references/workflow.md](references/workflow.md).

Never put tokens, cookies, personal identifiers, or local absolute `skillRoot` paths
in the experience store. Consumers locate a skill by `resourceId` (skill name).

### Pin ask (only after a step-1 skill success)

If a **skill** (not a tool or script) completed the request and is not already pinned,
ask: **"Pin `<name>` so later similar requests stay at the top?"**

On confirm:

```bash
node "$SKILL_DIR/scripts/favorites.ts" add --uuid <uuid> --name "<name>" \
  --desc "<what it does and when to use it>" --path "<local skill dir>"
```

Pinning and experience reporting are independent. A declined pin does not undo the construct.

---

## Material gates (high-level only)

Ask the user only when a **prerequisite material** is missing — a case pack, an API/OpenAPI source, a cross-domain product, or a slot spec. Do **not** stop to collect executor fields (`fulfillOn`, `quantity`, `credits`, `rate`, …). Those follow the original rules: reuse user-supplied IDs, fill optional params with defaults, do not invent core IDs.

| Scenario | Prerequisite material | If missing |
|---|---|---|
| 1. One-shot construct | None extra. Run the original 4-step fallback | — |
| 2. Multi-step scene | Upstream domain artifact the scene cannot create (e.g. `ready-to-sell` needs a catalog product) | Ask for that material or construct it first, then finish remaining scene steps |
| 3. Write a script from APIs | An API source: OpenAPI files, `planId`, or `serviceId` | Ask for one of those; then write/run the script with original param rules |
| 4. Case materials | At least one case source (file, paste, `planId`, or URL) | Ask; do not parse or construct without cases. Path A waits for cases after knowledge-build |
| 5. New domain slot | A scene skill under `slots/` (or `workspace.slot_roots`) | Ask for the skill folder or `domain` + OpenAPI to scaffold. Drop-in discover; do not invent operations |

After the user supplies the material, **resume and complete the remaining workflow**. Do not skip later high-level steps.

## Guardrails

- Do not invent business identifiers.
- Do not call organization-specific CLIs or private registries from this skill.
- SQL is SELECT-only.
- Feature-flag writes require an explicit environment and user confirmation.
- Keep this file under 500 lines; load [references/workflow.md](references/workflow.md) on demand.
