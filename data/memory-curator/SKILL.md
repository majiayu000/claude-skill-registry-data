---
name: memory-curator
description: Manage architectural decisions and insights in memory.jsonl. Use when you need to document strategic decisions, lessons learned, fixed problems, or architectural insights. Append-only audit trail for project knowledge.
---
<memory_curator>
# Memory Curator Skill

`memory.jsonl` is an **append-only** audit trail of durable engineering knowledge:
- **Never** edit or delete existing lines.
- **Never** write to the file manually—always use the script.
- Add a new entry to correct or supersede an older one.

---

## When to Use (Triage Test — all three are quick yes/no)
Create a memory entry **only if at least one** is true:

1) Will this decision meaningfully affect **how we build other features**?  
2) Is this a **pattern** we’ll want to **repeat** across the codebase?  
3) Does this **prevent a category of future mistakes**?

If **no** to all three → do **not** create an entry. Put implementation detail into the task context instead.

---

## Workflow (Authoritative)

**Always use the helper script** and never edit the file by hand.

```bash
python3 $CLAUDE_PROJECT_DIR/.claude/skills/memory-curator/scripts/add_memory_entry.py \
  --summary "<see Summary Format below>" \
  --tags architecture,api,lessons-learned \
  --links "TASK-090 services/backend-api/src/plaid/plaid-service.ts"
```

**The script will:**

* Compute the next sequential ID (`mem-0001`, `mem-0002`, …)
* Add a UTC timestamp (`YYYY-MM-DDTHH:MM:SSZ`)
* Append a single JSON object as one line to `.meridian/memory.jsonl`
* Echo the written entry for confirmation

---

## Summary Format (consistent & skimmable)

Write `--summary` as concise Markdown using these bolded labels in this order (one paragraph per label, short bullets allowed). This gives structure **without** changing the JSON schema.

```
**Decision:** <The decision or principle in a single sentence.>
**Problem:** <What made this necessary; symptoms, constraints, or failure mode.>
**Alternatives:** <Narrow list of serious options considered and why rejected.>
**Trade-offs:** <What we accept (complexity, perf, coupling) and why it’s OK.>
**Impact/Scope:** <Which services/modules/patterns this affects now and later.>
**Pattern:** <If reusable, name it; 1–2 rules of thumb to apply next time.>
```

> Keep to ~6–10 lines total. If it doesn’t fit, it’s probably a design doc, not a memory entry—link to that doc and keep the summary short.

---

## Tags (small, useful taxonomy)

Use **kebab‑case** tags. Prefer a few broad tags over many hyper‑specific ones.

* Core: `architecture`, `data-model`, `api`, `contracts`, `security`, `performance`, `reliability`, `observability`, `testing`, `tooling`, `build`, `release`, `i18n`, `a11y`, `cost`
* Nature: `decision`, `pattern`, `lesson`, `tradeoff`, `deprecation`, `migration`
* Stack (when relevant): `nextjs`, `react`, `node`, `prisma`, `postgres`, `redis`, `s3`, `graphql`, `openapi`

Examples:

```
--tags architecture,pattern,nextjs
--tags api,contracts,lesson
```

---

## Links (make future retrieval easy)

Use `--links` for **TASK IDs, critical file paths, PR URLs, or design docs**. Examples:

```
--links "TASK-091 services/web/app/(auth)/route.ts https://github.com/org/repo/pull/1234"
```

* Prefer **relative repo paths** over vague descriptions.
* It’s fine to include multiple `--links` flags or a space/comma‑separated list.
* Do **not** put secrets or tokens in links.

---

## JSON Shape (what the script writes)

Typical entry:

```json
{"id":"mem-0038","timestamp":"2025-11-12T05:55:31Z",
 "summary":"**Decision:** ...","tags":["architecture","pattern","nextjs"],
 "links":["TASK-090","services/backend-api/src/plaid/plaid-service.ts"]}
```

Your script may include additional fields; never rely on field order.

---

## Corrections, Supersession, and Deprecation

* **Never edit** old lines. Add a **new** entry that references the old one by ID in `--summary` or `--links`.
* Use tags like `deprecation` or `lesson` to signal context.
* Recommended summary line when superseding:

  * `**Decision:** Supersedes mem-0021 — <new decision>. Why: <reason>.`

---

## Good vs Bad Examples

**Bad (too tactical):**
“Add a scroll indicator with 15 segments using requestAnimationFrame.”
*Why it’s bad*: UI detail, not a reusable principle.

**Good (durable pattern):**

```
**Decision:** Collocate request orchestration in Next.js Route Handlers; keep helpers file‑local.
**Problem:** 3‑layer service indirection slowed iteration and hid data contracts.
**Alternatives:** Keep services layer (rejected: redundancy, test friction); global helpers (rejected: coupling).
**Trade-offs:** Slight duplication accepted to gain locality; extraction only after 3+ call sites.
**Impact/Scope:** All new routes in /app/*; refactors opportunistically in legacy pages.
**Pattern:** Orchestrator <120 LOC; helpers <30 LOC; schema at boundary.
```

---

## Common Queries (jq snippets)

```bash
# All architecture decisions
jq -s '.[] | select(.tags != null and (.tags | index("architecture"))) ' .meridian/memory.jsonl

# Entries mentioning a task
jq -s '.[] | select(.links != null and (.links | index("TASK-090")))' .meridian/memory.jsonl

# Most recent 5 entries
tail -5 .meridian/memory.jsonl | jq -s '.'

# Security-related
jq -s '.[] | select(.tags != null and (.tags | index("security")))' .meridian/memory.jsonl
```

---

## Guardrails

* No secrets/PII—ever.
* Keep entries **short** and **pattern/decision oriented**.
* Prefer one strong entry over several fragmented ones.
* If you’re unsure whether it belongs, add the insight to `TASK-###-context.md` and revisit later.
</memory_curator>