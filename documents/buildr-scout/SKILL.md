---
name: buildr-scout
description: |
  Extracts actionable knowledge from external sources (articles, docs, papers,
  repos, APIs) and converts findings into Buildr system artifacts: vault items,
  repo modifications, agent directives, and system evolution proposals.

  USE THIS SKILL when: the user provides an article/URL/doc and wants to
  extract value from it, when the system needs to absorb new patterns or
  practices, when existing vault items need updating based on new knowledge,
  or when research is needed to inform architectural decisions.

  Triggers on: "läs denna artikel", "analysera", "extrahera", "vad kan vi
  lära oss", "researcha", "undersök", "uppdatera systemet", "absorbera",
  "read this", "analyze", "extract", "what can we learn", "research",
  "investigate", "update the system", "absorb", "scout", or when the user
  provides a URL or document and expects actionable system improvements.

  The Smith builds tools. The Operator builds projects.
  The Scout brings in knowledge from the outside world and evolves the system.
---

# Buildr Scout

## What This Skill Does

Takes external knowledge → analyzes it → produces system-level improvements.

The Scout is the system's interface to the outside world. It reads articles,
documentation, engineering blogs, research papers, and codebases. It doesn't
just summarize — it extracts what matters for the Buildr system specifically,
then produces concrete artifacts that improve the system or enable other agents
to make changes.

## The Pipeline

```
Source material arrives (URL, article, doc, codebase reference)
    ↓
Phase 1: INTAKE (fetch, normalize, structure the source)
    ↓
Phase 2: ANALYZE (deep extraction — patterns, principles, anti-patterns)
    ↓
Phase 3: RESEARCH (proactive discovery — related concepts, cross-references)
    ↓
Phase 4: MAP (connect findings to Buildr system — gaps, upgrades, conflicts)
    ↓
Phase 5: EMIT (produce concrete outputs — vault items, repo changes, directives)
    ↓
Phase 6: VERIFY (confirm outputs are self-contained and actionable)
```

---

## Phase 1: Intake

Accept and normalize the source material.

### Source Types

| Source | How to Handle |
|--------|--------------|
| **URL** | Fetch with WebFetch. Extract full content. Preserve code blocks. |
| **Pasted text** | Accept as-is. Identify structure (article, doc, README, spec). |
| **File path** | Read the file. Detect format (markdown, code, JSON, YAML). |
| **Repo reference** | Clone/read the relevant files. Map the architecture. |
| **Multiple sources** | Process each independently, then cross-reference in Phase 3. |

### Intake Output

Produce an internal document (not shown to user unless asked):

```
SOURCE: [title or identifier]
TYPE: [article | documentation | paper | codebase | specification]
DOMAIN: [what field/technology this covers]
AUTHOR_AUTHORITY: [high | medium | low — is the source authoritative?]
RECENCY: [date if available, relevance to current practices]
LENGTH: [short < 2000 words | medium | long > 8000 words]
```

### Quality Gate

Before proceeding past intake:
- Is the source readable and complete? (No paywalls, no broken fetches)
- Is the source relevant to software engineering, agent design, or system architecture?
- If the source is low-quality or irrelevant, tell the user and suggest alternatives.

---

## Phase 2: Analyze

Deep extraction of actionable knowledge. This is NOT summarization.
The goal is to identify what can become a tool, rule, pattern, or memory.

### Extraction Dimensions

For every source, extract along these dimensions:

#### 2.1 Patterns
Reusable approaches that solve recurring problems.
```
PATTERN: [name]
CONTEXT: [when this pattern applies]
MECHANISM: [how it works — specific, not abstract]
EVIDENCE: [what result the source reports]
BUILDR_FIT: [which vault type this could become: skill | strategy | routine]
```

#### 2.2 Anti-Patterns
Things that fail and why.
```
ANTI_PATTERN: [name]
FAILURE_MODE: [what goes wrong — specific consequence]
WHY: [root cause]
ALTERNATIVE: [what to do instead]
BUILDR_FIT: [constraint | memory/scar]
```

#### 2.3 Principles
High-level truths that inform decision-making.
```
PRINCIPLE: [statement]
SCOPE: [always | conditional on X]
IMPLICATION: [what this means for how agents should behave]
BUILDR_FIT: [strategy | constraint | memory/insight]
```

#### 2.4 Technical Details
Specific implementation knowledge.
```
DETAIL: [what]
APPLICABILITY: [which tech stack / context]
GOTCHA: [non-obvious caveat]
BUILDR_FIT: [skill step | constraint | memory/scar]
```

#### 2.5 Architecture Decisions
Design choices with trade-offs.
```
DECISION: [what was chosen]
ALTERNATIVES: [what was rejected]
RATIONALE: [why this choice]
TRADE_OFFS: [what you give up]
BUILDR_FIT: [strategy | decision record | memory/insight]
```

### Minimum Extraction

Every source must yield AT LEAST:
- 2 patterns or principles
- 1 anti-pattern
- 1 concrete technical detail

If a source yields fewer, it's either not valuable enough or the analysis
isn't deep enough. Dig deeper before proceeding.

---

## Phase 3: Research

**This is what separates Scout from a summarizer.**

After analyzing the source, proactively investigate:

### 3.1 Cross-Reference with Existing System

```
For each finding:
  1. Read vault/INDEX.md — does an existing vault item cover this?
  2. If YES → is the existing item weaker than the new finding?
     → Flag for upgrade
  3. If NO → is this finding important enough for a new vault item?
     → Flag for creation
  4. Does this finding CONFLICT with an existing vault item?
     → Flag as conflict — requires human decision
```

### 3.2 Gap Detection

Look for what the source implies but doesn't state:

- If the source describes a generator-evaluator pattern, check if the Buildr
  system has vault items for QA feedback loops. If not → gap.
- If the source discusses context window management, check if existing
  strategies cover this. If not → gap.
- If the source mentions a tool or technique, check the catalog/index.json
  for related tools.

### 3.3 Lateral Discovery

Search for related concepts the user didn't ask about:

```
Source discusses "harness design"
  → Related: circuit breakers (templates/circuit-breaker.md exists — good)
  → Related: sprint contracts (not in vault — potential new strategy)
  → Related: evaluator tuning (not in vault — potential new skill)
  → Related: context window degradation (memory-system handles this — verify)
```

### 3.4 Impact Assessment

For each finding, assess:

```
IMPACT: [high | medium | low]
  high = changes how agents work across all projects
  medium = adds capability or prevents known failure mode
  low = nice-to-have, edge case, or already partially covered

EFFORT: [trivial | moderate | significant]
  trivial = add a few lines to existing vault item
  moderate = new vault item or modify an engine
  significant = new system component or architectural change

PRIORITY: IMPACT / EFFORT (high impact + trivial effort = do immediately)
```

---

## Phase 4: Map

Connect findings to specific Buildr system locations.

### 4.1 Vault Item Mapping

For each finding flagged as a potential vault item:

| Finding | Vault Type | Target Path | Action |
|---------|-----------|-------------|--------|
| [pattern name] | skill | `vault/skills/[name].md` | CREATE / UPDATE |
| [anti-pattern] | constraint | `vault/constraints/[name].md` | CREATE / UPDATE |
| [principle] | strategy | `vault/strategies/[name].md` | CREATE / UPDATE |
| [verification] | routine | `vault/routines/[name].md` | CREATE / UPDATE |
| [experience] | memory | `vault/memories/[scope]/[name].md` | CREATE / UPDATE |

### 4.2 Repo Modification Mapping

For findings that require changes to existing system files:

| Finding | Target File | Change Type | Description |
|---------|------------|-------------|-------------|
| [finding] | `engines/bridge.py` | MODIFY | [what to change] |
| [finding] | `CLAUDE.md` | APPEND | [what to add to guardrails] |
| [finding] | `templates/AGENT.md` | MODIFY | [behavioral update] |

### 4.3 Agent Directive Mapping

For findings too complex for direct changes — generate material that tells
another agent what to do:

```markdown
# Agent Directive: [Title]

## Source
[Where this knowledge came from]

## What Needs to Happen
[Clear description of the change]

## Why
[The finding that motivates this]

## Affected Files
[List of files that need modification]

## Constraints
[What must NOT change]

## Verification
[How to confirm the change worked]
```

Directives go to `.tmp/directives/` — they are consumed by other agents
and deleted after execution.

---

## Phase 5: Emit

Produce the actual outputs. Every output must be immediately usable.

### 5.1 Vault Items

Follow the exact templates defined in `skills/buildr-smith/SKILL.md`.
The Scout does NOT invent its own formats. It uses Smith-compatible formats
so items can be reviewed and accepted into the vault.

**Before writing any vault item, run the agnosticism test:**
```
Can this item be used identically for:
  ✓ A booking site for fishing trips in Zanzibar?
  ✓ A SaaS dashboard for project management?
  ✓ A CLI tool for data processing?
  ✓ An e-commerce store for handmade crafts?

If ANY is "no" → make it agnostic or don't create it.
```

### 5.2 Repo Modifications

Apply changes directly to existing files when:
- The change is unambiguous (e.g., adding a guardrail to CLAUDE.md)
- The change is small (< 20 lines)
- The change doesn't alter system architecture

For larger changes, emit an agent directive instead.

### 5.3 Agent Directives

Write to `.tmp/directives/YYYY-MM-DD-[slug].md`.
These are fire-and-forget documents for other agents.

### 5.4 Discovery Logging

Log every significant finding using the memory system:

```bash
bash memory-system/tools/discovery-write.sh \
  --session "[current-session]" \
  --engine "scout" \
  --topic "[topic]" \
  --content "[finding]" \
  --direction "reviewing"
```

### 5.5 Evolution Proposals

For findings that suggest structural system changes:

```markdown
# Evolution Proposal: [Title]

## Source Evidence
[Article/doc that motivates this]

## Current State
[How the system works now]

## Proposed Change
[What should change]

## Migration Path
[How to get from current → proposed without breaking anything]

## Risk
[What could go wrong]

## Decision Required
[What the human needs to decide before proceeding]
```

Evolution proposals go to `docs/proposals/YYYY-MM-DD-[slug].md`.
They are NEVER auto-executed. They require human approval.

---

## Phase 6: Verify

Before delivering outputs:

- [ ] Every vault item passes the agnosticism test
- [ ] Every vault item follows Smith templates (correct type, line limits)
- [ ] Every repo modification is small and reversible
- [ ] Every agent directive is self-contained (no external dependencies)
- [ ] Every evolution proposal has a clear decision point
- [ ] Findings are logged to the discovery system
- [ ] Conflicts with existing vault items are explicitly flagged
- [ ] MANIFEST.md is updated if new files were created
- [ ] No vault item references another vault item (self-contained rule)

---

## Output Summary Format

After completing all phases, present to the user:

```markdown
## Scout Report: [Source Title]

### Extracted
- [N] patterns, [N] anti-patterns, [N] principles, [N] technical details

### Produced
- [N] new vault items (list with paths)
- [N] vault item upgrades (list with what changed)
- [N] repo modifications (list with files)
- [N] agent directives (list with titles)
- [N] evolution proposals (list with titles)

### Conflicts Found
- [List any findings that contradict existing vault items]

### Gaps Identified
- [List system gaps discovered during research phase]

### Recommended Next Steps
1. [Prioritized action]
2. [Prioritized action]
...
```

---

## Key Principles

1. **Extract, don't summarize.** The user can read the article themselves.
   The Scout's job is to turn prose into system artifacts.

2. **Proactive over reactive.** Don't just process what's asked — discover
   related gaps, conflicts, and opportunities.

3. **Smith-compatible outputs.** Every vault item the Scout produces must
   pass the Smith's quality gate. Use the same templates, same constraints.

4. **Changes are graduated.** Small changes → direct repo edits.
   Medium changes → agent directives. Large changes → evolution proposals.
   Never auto-execute architectural changes.

5. **Everything is traceable.** Every output links back to the source finding.
   Every finding links back to the source material. An auditor can trace
   any vault item back to the article that inspired it.

6. **The system gets smarter with every source.** Each article processed
   should measurably improve the vault, close a gap, or prevent a future
   failure. If processing a source didn't change anything, either the source
   was irrelevant or the Scout failed.
