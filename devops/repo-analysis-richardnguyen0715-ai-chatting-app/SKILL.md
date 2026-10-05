---
name: repo-analysis
description: Systematic workflow for analyzing a cloned GitHub repository. Use when you've cloned a repo and want to extract its tech stack, architecture, key patterns, and what to adopt into your system.
---

# Repo Analysis

## Overview

A structured workflow for turning a cloned codebase into an actionable analysis. The goal is to extract *transferable* knowledge — patterns, techniques, and ideas — not just describe what the code does.

## When to Use

- You just cloned a repo from GitHub that looks interesting
- You want to understand how a project is architected before adopting its patterns
- You need to compare a reference implementation to your current approach
- You're evaluating whether to adopt a library or framework used in the repo

## Workflow

### 0. Pre-flight

Before starting, confirm:
```
- Repo is cloned to: ~/references/{repo-name}/
- analysis.md does NOT already exist (or needs refresh)
```

If not cloned yet:
```bash
git clone https://github.com/{owner}/{repo} ~/references/{repo-name}
```

---

### Step 1 — Stack Identification (5 min)

Collect the essentials without reading code yet:

```bash
# Language breakdown
find ~/references/{repo-name} -type f | grep -E "\.(py|ts|go|rs|java|rb|kt)$" | sed 's/.*\.//' | sort | uniq -c | sort -rn

# Dependency manifest
cat ~/references/{repo-name}/requirements.txt 2>/dev/null
cat ~/references/{repo-name}/pyproject.toml 2>/dev/null
cat ~/references/{repo-name}/package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print('\n'.join(list(d.get('dependencies',{}).keys())[:20]))"

# CI/CD and infra
ls ~/references/{repo-name}/.github/workflows/ 2>/dev/null
cat ~/references/{repo-name}/Dockerfile 2>/dev/null | head -20
cat ~/references/{repo-name}/docker-compose.yml 2>/dev/null | head -30
```

**Fill in**: Tech Stack table in `analysis.md`

---

### Step 2 — Architecture Overview (10 min)

Understand the shape before diving into code:

```bash
# Top-level structure
ls ~/references/{repo-name}/src/ 2>/dev/null || ls ~/references/{repo-name}/app/ 2>/dev/null || ls ~/references/{repo-name}/

# Module count and size
find ~/references/{repo-name} -name "*.py" -not -path "*/.git/*" | head -30
```

Questions to answer:
- What are the top-level modules and their single responsibility?
- Where does data enter the system? Where does it exit?
- What's the test structure? (mirrors source? separate?)
- Is there a clear separation of concerns?

**Fill in**: Architecture Overview section

---

### Step 3 — Pattern Extraction (15 min)

Read the most interesting parts — not everything. Focus on:

1. **Entry points** — main files, routers, CLI definitions
2. **Core domain logic** — the non-trivial business logic
3. **Infrastructure adapters** — how they wire up databases, APIs, external services
4. **Tests** — what the test strategy reveals about the design

For each notable pattern:
```
Name:       Short descriptive name
File:       ~/references/{repo-name}/path/to/file.py
Lines:      L{start}-{end}
What:       What problem this solves
Why novel:  Why this is worth noting
Snippet:    (paste key 5-15 lines)
Adopt?:     Yes / Adapted / No
```

**Fill in**: Key Patterns section

---

### Step 4 — Assessment (5 min)

Be opinionated. Rate each dimension:

| Dimension | Score (1-5) | Notes |
|-----------|-------------|-------|
| Code clarity | | |
| Architecture cleanliness | | |
| Test coverage/quality | | |
| Error handling | | |
| Security posture | | |
| Scalability design | | |

**Fill in**: Strengths + Weaknesses sections

---

### Step 5 — Adoption Planning (5 min)

Convert findings into concrete actions:

```
For each pattern worth adopting:
  □ WHAT to adopt (be specific — not "their architecture", but "their repository pattern")
  □ WHERE to apply it in my system
  □ HOW HARD (drop-in / light adaptation / significant rework)
  □ PRIORITY (high / medium / backlog)
```

**Fill in**: "What to Adopt" section

---

### Step 6 — Save and Extract

```bash
# Save analysis (should already be at ~/references/{repo-name}/analysis.md)
# Then extract to knowledge base:
# "Use the context-curator agent to extract ~/references/{repo-name}/analysis.md"
```

---

## Output Checklist

- [ ] Tech stack fully documented
- [ ] Architecture flow described
- [ ] ≥ 3 patterns extracted with code snippets
- [ ] Strengths and weaknesses are specific (not generic)
- [ ] Adoption items are actionable with clear "where" and "how"
- [ ] `context-curator` run to extract to KB

## Tips

- **Don't read everything** — skim for the interesting 20%
- **Focus on what's different** from your current approach
- **Patterns > implementations** — you want the idea, not the code verbatim
- Use `repo-analyst` agent for automated analysis generation
