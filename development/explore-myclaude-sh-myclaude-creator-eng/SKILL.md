---
name: explore
description: >-
  Search the marketplace, analyze competition, discover gaps, and find inspiration.
  Use when: 'explore', 'search marketplace', 'what exists for', 'competitors',
  'market gap', 'trending', or before browsing the marketplace. For domain research
  with build recommendations, use /scout instead.
argument-hint: "[query or category]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(myclaude *)
  - AskUserQuestion
---

# Explore — Marketplace Intelligence & Discovery

> Before you build, know the landscape. This skill is your window into the marketplace.

**When to use:** Before /create (market research). After /publish (competitive positioning). Anytime you want to understand what exists, what's missing, and where the opportunity is.

**When NOT to use:** For building products (use /create→/fill pipeline). For quality checks (use /validate).

---

## Activation Protocol

0. **Shared preamble:** Load `references/quality/activation-preamble.md` — context assembly, persona adaptation, deterministic routing rules.
1. Read `creator.yaml` → adapt to profile.type, expertise domains, language
2. Check CLI: `myclaude --version 2>/dev/null` — if unavailable, explain install and offer offline alternatives
3. Parse `$ARGUMENTS` for query intent
4. Route to the appropriate exploration mode
5. **Load voice identity:** Load `references/quality/engine-voice-core.md`. Every user-facing line in this skill honors the ✦ signature, three tones, and six anti-patterns.
5b. **Load UX vocabulary:** Load `references/ux-vocabulary.md` — translate all internal terms before creator-facing output.
5c. **Load proactives:** Load `references/engine-proactive.md` — wire #1 (pipeline guidance: after explore, suggest /scout or /create), #14 (feedback loop on published products).
6. **CLI contract:** Load `references/cli-contract.md` for unified error handling. This skill is the heaviest CLI consumer (12+ invocations across 5 modes). Severity map:
   - **Silent-skip:** `search`, `trending`, `workspace --recommend` — skip without user-visible warning on failure
   - **Silent-skip:** `--version` check — degrade to offline mode
   - **Interactive:** `install {slug}` — show manual install instructions on failure
   - **All queries:** append `--json 2>/dev/null`, parse JSON, treat invalid JSON as CLI absent
   - **Timeout:** 15s per command. On timeout, skip with offline alternatives

---

## Exploration Modes

### MODE 0: Project-Aware Recommendations (the smart default)
**Trigger:** `/explore` with no arguments, "what do I need", "recommend", "analyze my setup", "optimize"

This is the MODE that makes the Engine indispensable. Instead of generic search, it analyzes the creator's ACTUAL project and recommends products that would improve their specific workflow.

**Step 1 — Detect active project context (using Glob/Read/Grep, NOT Bash):**
```
# What tech stack? Use Glob to detect manifest files:
Glob("package.json")        → Node.js/JavaScript
Glob("Cargo.toml")          → Rust
Glob("requirements.txt")    → Python (pip)
Glob("pyproject.toml")      → Python (modern)
Glob("go.mod")              → Go
Glob("Gemfile")             → Ruby
Glob("pom.xml")             → Java (Maven)
Glob("build.gradle")        → Java/Kotlin (Gradle)

# What framework? If package.json found, Read it and check dependencies:
Read("package.json") → look for: react, next, vue, angular, svelte, express, fastapi in dependencies

# What's in their .claude/?
Glob(".claude/rules/*.md")          → count rule files
Glob(".claude/skills/*/SKILL.md")   → count installed skills

# Do they have hooks?
Read(".claude/settings.json") → check if "hooks" key exists

# CLAUDE.md size? Read first 5 lines to detect existence, check file metadata
Glob("CLAUDE.md") + Glob(".claude/CLAUDE.md") → if found, Read first 10 lines for size estimate
```

**IMPORTANT:** All detection uses Glob, Read, and Grep tools — NOT Bash. The only Bash allowed is `Bash(myclaude *)` for marketplace queries.

**Step 2 — Cross-reference with marketplace:**
Based on detected tech stack, search for matching products:
```bash
myclaude search "{detected_framework}" --json 2>/dev/null
myclaude search "{detected_language} rules" --json 2>/dev/null
```

**Step 3 — Deliver personalized recommendations:**
```
Project Analysis: {project_name or cwd}

  Stack:    {language} + {framework}
  Rules:    {N} loaded ({M} without path scoping)
  Skills:   {N} installed
  Hooks:    {present/none}
  CLAUDE.md: {N} chars ({optimal/oversized})

Recommended products for THIS project:

  INSTALL NOW (free, immediate value):
  1. {name} — {why it matches this project}
     myclaude install {slug}

  CONSIDER (paid, high impact):
  2. {name} — {why it matches}
     myclaude install {slug}

  MISSING FROM YOUR SETUP:
  - No {type} for {detected_gap} — {N} options exist on marketplace
  - Your CLAUDE.md {has no path scoping / is oversized / could use @include}

  CREATE OPPORTUNITY:
  - No {type} exists for {framework + specific use case}
  - Your expertise in {domain} + this project's stack = potential product
```

**Anti-pattern guard:** Don't recommend more than 5 products total. Don't recommend paid products to beginners. Don't recommend products the creator already has installed. If CLI unavailable, show only the project analysis part (still valuable without marketplace).

**Why this is MODE 0 (default):** When a creator types `/explore` with no arguments, THIS is what runs. Not a generic "what do you want to search?" — a smart, project-aware consultation that gives immediate value. The creator didn't come to browse. They came because they want their setup to be better. Give them that.

---

### MODE 1: Search (find specific products)
**Trigger:** "search for", "find", "is there a", specific query terms

```bash
myclaude search "{query}" --json 2>/dev/null
```

Display results as:
```
Found {N} products for "{query}":

  {name} [{type}] by @{author} — {downloads} dl — ${price}
    "{description truncated to 80 chars}"
  ...

{If 0 results: "No products found. This could be an opportunity — or the query needs refining."}
```

### MODE 2: Trending (market pulse)
**Trigger:** "trending", "popular", "what's hot", "top products"

```bash
myclaude trending --json 2>/dev/null
```

Display with analysis:
```
Top 10 trending products:

  #  NAME                 TYPE    AUTHOR   DL   PRICE
  1. {name}               {type}  @{auth}  {N}  {price}
  ...

Patterns I notice:
  - Most popular type: {type with most entries}
  - Price sweet spot: {most common price point}
  - Gap: {type or category NOT represented in top 10}
```

### MODE 3: Gap Analysis (find opportunities)
**Trigger:** "gaps", "opportunities", "what's missing", "what should I build"

1. Run trending + search across all categories
2. Cross-reference with creator.yaml expertise domains
3. Identify underserved categories:

```bash
myclaude search --category skills --sort newest --limit 10 --json 2>/dev/null
myclaude search --category squads --sort newest --limit 10 --json 2>/dev/null
myclaude search --category systems --sort newest --limit 10 --json 2>/dev/null
```

```
Market Gap Analysis for @{username}:

  YOUR EXPERTISE: {domains from creator.yaml}

  UNDERSERVED AREAS:
  - {category}: only {N} products, {avg_downloads} avg downloads
    → You could build: {suggestion matching their expertise}
  
  OVERSATURATED:
  - {category}: {N} products, hard to differentiate
    → Only enter if you have genuine domain expertise

  RECOMMENDED FIRST PRODUCT:
  {type}: {suggestion} — because {reasoning linking expertise to gap}
```

### MODE 4: Competitive Intel (analyze specific niche)
**Trigger:** "competitors for", "compare with", "who else builds", "analyze category"

```bash
myclaude search --category {category} --sort downloads --limit 10 --json 2>/dev/null
```

Deep analysis:
```
Competitive Landscape: {category}

  LEADERS (>10 downloads):
  {name} by @{author} — {downloads} dl — {description}
    Strengths: {inferred from description}
    Weakness: {what's missing based on DNA patterns}

  DIFFERENTIATION OPPORTUNITIES:
  1. {gap none of the leaders fill}
  2. {feature that would make your product stand out}
  3. {pricing opportunity if all are free or all are paid}
```

### MODE 5: Inspiration (explore what's possible)
**Trigger:** "inspire me", "show me examples", "what can I build"

Combine workspace scan + marketplace data:

```bash
myclaude workspace --recommend --json 2>/dev/null
```

```
Based on your setup and expertise:

  QUICK WINS (build in <1 hour):
  - {type}: {suggestion} — similar products average {N} downloads

  AMBITIOUS PROJECTS (build in 1 day):
  - {type}: {suggestion} — no competition in this space

  DREAM PRODUCT (build over a week):
  - {type}: {suggestion} — highest potential impact
```

---

## Offline Mode (CLI unavailable)

If myclaude CLI is not installed:

```
Marketplace search requires the MyClaude CLI.
Install: npm i -g @myclaude-cli/cli

In the meantime, I can:
  - Analyze your workspace for product ideas based on your skills and rules
  - Review structural-dna.md to suggest high-impact product types
  - Help brainstorm based on your creator.yaml expertise domains

What would be most useful?
```

---

## Anti-Patterns

1. **Research as procrastination** — If the creator has been exploring for 3+ rounds without starting a product, nudge: "You've done great research. The market validates your idea. Ready to /create?"
2. **Copy, not compete** — Never suggest copying a top product. Always frame as "differentiate by adding what they lack."
3. **Stale data assumption** — Marketplace data is live. Don't cache or assume results from previous searches.
4. **Overwhelm** — Show max 10 results. More isn't helpful — it's paralyzing.

---

## Quality Gate

- [ ] Results are actionable (end with "here's what to do next")
- [ ] Adapted to creator's language and technical level
- [ ] Gap analysis connects to creator's expertise (not generic)
- [ ] CLI failures degrade gracefully to offline alternatives

---

## Compact Instructions

When summarizing this conversation, always preserve:
- Search queries executed and key results
- Market gaps identified and their connection to creator expertise
- Competitive analysis findings (leaders, differentiators)
- The recommended product opportunity and reasoning
- Any decisions made based on exploration
