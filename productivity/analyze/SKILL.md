---
name: analyze
description: Risk analysis and approach selection before planning. Use when requirements are ambiguous, approaches vary, or work touches hub/bridge nodes. Skip for typo fixes.
mcp: codebase-memory-mcp
---

# /supergraph:analyze

Analyze first, implement never. No code until approach is approved.

Announce: "🔍 /supergraph:analyze — framing problem, checking graph risk..."

## When

- Ambiguous requirements
- Multiple valid approaches
- Task spans modules
- Graph shows high blast-risk (hub/bridge nodes)
- User says "how should I..." or "what's the best way..."

Skip for: typo fixes, config changes, clear mechanical edits.

## Workflow

**0. Read CONTEXT.md (if exists):**
```bash
cat CONTEXT.md 2>/dev/null | head -60
```
Use existing domain vocabulary in all analysis — never invent new terms for concepts already named.

**1. Frame the problem:**
- Goal: [one sentence]
- Known constraints
- Open questions

## Ceremony Router

For work that enters analyze, classify the uncertainty before choosing an approach:

- **spike:** the approach or feasibility is unknown. Produce a bounded experiment, define what evidence would invalidate it, and exit with a decision or an explicit escalation.
- **bounded:** the behavior and boundary are known but implementation choices remain. Compare the smallest viable approaches, identify affected paths, and exit with an approved implementation shape.
- **architectural:** the change crosses contracts, hubs, bridges, persistence, or multiple platforms. Produce the full graph-informed analysis and required SDD inputs before planning.

Approval required before implementation on every path. The router may skip unnecessary ceremony, but it may not skip approval, RED-before-production TDD, verification, or review. If hidden complexity appears, upgrade one-way from `spike` to `bounded` to `architectural`; never downshift after evidence has expanded the scope.

**1b. Score ambiguity (before grilling):**

| Signal | +1 if... |
|---|---|
| Ambiguous scope | touches multiple modules without naming one |
| No explicit path | no file/package/feature named |
| Multiple intents | could be bug fix, feature, refactor, or question |
| First interaction | no established context this session |

| Score | Action |
|---|---|
| 0–1 | Skip grilling — proceed with best available info |
| 2 | Show 1-line routing summary, wait for confirm |
| 3–4 | Grill: ask focused questions with recommended options |

**Auto-skip grilling entirely if:** user said "go"/"just do it", trivial fix (<15 lines, 1 file), explicit mode command, or active plan already exists.

**Grilling rules:** ONE question at a time, offer recommended answer, max 3 questions. Stop when goal + constraints are clear enough that approach won't reverse on new info.

**2. Check graph risk:** Reuse `/supergraph:scan` context (`CBM_PROJECT`, `codebase-memory-mcp`, see `references/codebase-memory-contract.md`). If targets identified, call `detect_changes`, `search_graph`, `trace_path`, `get_architecture`, recipes `hubs/bridges/cross-boundary`. Empty = evidence. >20 files STOP.

**2b. Serena (optional):** See `serena/SKILL.md:Setup`. If scan not run, call `initial_instructions` first, then `find_referencing_symbols`/`find_implementations` per target. Skip if unavailable.

**3. Propose 2-3 approaches + persona debate:**
For each approach: pros, cons, risk level, effort. Prefer minimal viable.

Then run 5 quick persona checks on the **recommended** approach:

| Persona | Question |
|---|---|
| Architect | Does this fit the architecture? New coupling? |
| Security | What can be abused? Auth/data boundaries respected? |
| Performance | Latency impact? N+1 queries? Memory leaks? |
| UX | Error states handled? Intuitive? |
| Devil's Advocate | Simpler alternative? Which assumption could be wrong? |

Emit verdict: **GO** (no blockers) / **CAUTION** (manageable risks, note mitigations) / **STOP** (critical issue — redesign needed before planning).

STOP triggers: auth bypass with no mitigation, fundamental design incompatibility, N+1 with no workaround, false core assumption.

**4. Ask focused questions (one at a time):**
Only if the answer changes direction.

**5. Recommend and hand off:**
Present recommendation. Once approved, summarize decisions into an analysis block in the plan file or prompt context:
```markdown
## Analysis Decisions
- Approach: [chosen] | Why: [reason]
- Alternatives considered: [list] | Risks: [list]
```

Update CONTEXT.md if analysis crystallized new domain terms:
```bash
printf '\n## <term>\n[definition]\n' >> CONTEXT.md
```

→ invoke `/supergraph:plan`

## Rules
- No implementation during analyze
- Don't over-analyze for hypothetical futures
- Ask ONE question at a time during grill — never dump multiple questions
- Always end with: "Shall I create the plan?" → invoke `/supergraph:plan`
