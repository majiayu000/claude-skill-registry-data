---
name: context-extraction
description: Distill learnings from a completed repo analysis into reusable knowledge base entries in ~/.copilot/context/. Use after finishing a repo-analysis to make the learnings persistent and searchable.
---

# Context Extraction

## Overview

After analyzing a reference repository, this skill guides you through extracting the reusable learnings into `~/.copilot/context/` — your permanent knowledge base. The goal is to transform repo-specific observations into general, domain-organized knowledge entries Copilot can draw on for any future task.

## When to Use

- You've completed a repo analysis (`~/references/{repo}/analysis.md` exists)
- You want to make learnings available beyond this one repo
- You want Copilot to be able to reference techniques without you re-specifying them
- You're building up knowledge in a specific domain (forecasting, auth, etc.)

## Preparation

Confirm before starting:
```bash
cat ~/references/{repo-name}/analysis.md  # should be complete
ls ~/.copilot/context/                     # know what domains exist
```

---

## Extraction Workflow

### Step 1 — Read the Analysis

Focus on these sections of `analysis.md`:
- **Section 4 (Strengths)** — what's genuinely good and transferable
- **Section 6 (Key Patterns)** — the concrete techniques
- **Section 8 (What to Adopt)** — the actionable list

### Step 2 — Filter for Reusability

For each item, ask:
> "Would this be useful in a **different project** with a similar tech stack?"

| Item | Reusable? | Domain | Action |
|------|-----------|--------|--------|
| "They use a feature store" | ✅ Yes | `forecasting/` | Create `feature-store-pattern.md` |
| "Their main.py imports config" | ❌ No | — | Skip |
| "JWT validation approach" | ✅ Yes | `auth/` | Create or update `jwt-validation.md` |
| "Pandas UDF for distributed scoring" | ✅ Yes | `databricks/` | Create `pandas-udf-scoring.md` |

### Step 3 — Check for Duplicates

Before creating a new file:
```bash
grep -r "{pattern keyword}" ~/.copilot/context/ -l
```
- If a file exists → **enrich** it (add new perspective/example from this repo)
- If no file exists → **create** it

### Step 4 — Write Knowledge Entries

For each new entry, use this template:

```markdown
# {Concise Pattern Name}

## What It Is
One sentence describing the pattern clearly.

## When to Use
- Situation where this applies
- NOT when: counter-case

## How It Works
Explain the mechanism — not just what it does, but why it works.

## Implementation
\`\`\`python
# Clean, minimal example adapted from the source
# NOT the raw source code — a simplified version
\`\`\`

## Variations
- **Variation A**: when to use it
- **Variation B**: trade-offs

## Adapting to My Stack
Specific notes on applying this to Databricks/Python/Azure AD environment.

## Source
- Analyzed repo: ~/references/{repo-name}
- Original: https://github.com/{owner}/{repo}
- Key file(s): {path}
```

### Step 5 — Update Context Index

If you created entries in a new domain, add a brief `AGENTS.md` in that subdirectory:

```markdown
# {Domain} Knowledge Base

Key patterns and techniques for {domain} distilled from reference repositories.

## Entries
- [{Pattern Name}](./{file}.md) — brief description
```

This lets Copilot CLI discover the context via `COPILOT_CUSTOM_INSTRUCTIONS_DIRS`.

### Step 6 — Verify

```bash
ls ~/.copilot/context/{domain}/     # new files present
cat ~/.copilot/context/{domain}/{file}.md  # content looks right
```

---

## Output Checklist

- [ ] Each transferable pattern has its own `.md` file
- [ ] Existing entries enriched (not duplicated) where applicable
- [ ] Code examples are clean and minimal (not verbatim copies)
- [ ] Each entry has "Adapting to My Stack" section
- [ ] Source attributed back to `~/references/{repo}`
- [ ] Domain `AGENTS.md` updated if new entries added

## Tips

- Aim for **3–7 entries** per analyzed repo (more = noise, fewer = waste)
- Think in **abstractions**, not implementations — the pattern, not the specific code
- If unsure whether something is reusable: ask "would I Google for this?" — if yes, it belongs
- Use `context-curator` agent to automate this workflow
