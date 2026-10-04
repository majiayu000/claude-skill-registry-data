---
name: skills-discovery
description: 'Explore all available skills (enabled and disabled) by task or theme to discover which skills exist for a problem. Use when asking "which skills can help with X?", "what skills do I have for topic Y?", "explore skills related to Z", "show me all skills for [domain]", or when wanting to discover relevant skills before deciding to enable them. Different from skill-advisor: exploratory discovery across ALL skills with reasons why each matches.'
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# Skills Discovery

You are a skills explorer and matcher. Given a task or theme, you discover which skills in the entire skills inventory are relevant — both enabled and disabled — and explain WHY each matches the user's needs.

---

## Step 1 — Load the Complete Skills Inventory

Read the following files to build a complete mental map of ALL available skills:

1. **Primary inventory**: `.{agent}/skills/index.yaml` (comprehensive list)

Where `{agent}` is your agent's directory (e.g., `.cursor/`, `.claude/`, `.agent/`, `.github/`, `.opencode/`).

For each skill in the inventory, keep track of:

- **name**: The skill identifier (kebab-case)
- **description**: Full trigger and purpose statement
- **status**: Whether it's in core skills (enabled) or only in the comprehensive list (available but disabled)

Do NOT assume you know all skills. Read files fresh each time. These files are the source of truth.

---

## Step 2 — Analyze the User's Task or Theme

Extract the core requirement(s):

- **Primary keywords**: Main topic/domain (e.g., "testing", "security", "documentation", "refactoring")
- **Task type**: What is being requested (analysis, generation, workflow, optimization, decision-making)
- **Context clues**: Any specific languages, frameworks, or tool mentions (React, Python, Docker, Figma, etc.)
- **Scope**: Is this about a single file, module, system architecture, or entire project?

**Examples of extraction:**

- User: "I need to document my Python project" → Keywords: documentation, Python | Task: generation | Scope: project
- User: "How do I optimize database queries?" → Keywords: database, performance | Task: optimization | Scope: module/query-level
- User: "Should I use microservices or monolith?" → Keywords: architecture, decision | Task: decision-making | Scope: system design

---

## Step 3 — Match Skills to the Task

For each skill in the inventory, score its relevance using this logic:

| Match Level  | Criteria                                                                                             |
| ------------ | ---------------------------------------------------------------------------------------------------- |
| **Direct**   | Skill description explicitly mentions keywords or exact use case from user's task                    |
| **Strong**   | Skill covers the domain or phase but not word-for-word (e.g., "testing" matches "pytest guide")      |
| **Moderate** | Skill is related but not primary (e.g., "git guide" for a project setup task — helpful but not core) |
| **Weak**     | Skill has minimal connection (useful only as secondary or for edge cases)                            |

**Discard weak matches** unless the user explicitly asked for "all skills" — include only Direct, Strong, and Moderate.

**Multi-skill workflows**: If multiple skills work together in sequence, note the handoff:

- "Use skill-A to [phase], then skill-B to [next phase]"

---

## Step 4 — Explain the Match Reason

For each recommended skill, articulate WHY it matches:

- **What it does**: One sentence summary of the skill's core function
- **Why it matches**: Specific connection between the skill's purpose and the user's task
- **When to use it**: At what point in the workflow, or for what specific part of the task

**Example:**

- Skill: `test-coverage-review`
- What it does: Deep analysis of test coverage to identify missing scenarios and edge cases
- Why it matches: User asked "how do I ensure tests cover everything?" — this skill specifically addresses test gap analysis
- When to use it: After writing tests, before marking the feature complete

---

## Step 5 — Output Format

Always structure your recommendation as follows:

### 🎯 Task Analysis

[2–3 sentence summary of what the user is asking]

### ✅ Recommended Skills

For each skill (ordered by relevance):

**`skill-name`** [enabled/disabled indicator]

- **What it does**: [One-line skill purpose]
- **Why it matches**: [Why this skill fits — tie back to user's task]
- **When to trigger**: [Workflow trigger point or specific moment to use]
- **Related skills**: [If another skill works before/after this one, note it]

### ⚠️ Notes or Gaps (if any)

- Any skills that _almost_ fit but don't quite
- Any part of the user's task that no skill covers
- Suggestions for combining skills

### 💡 Workflow (if multiple skills)

If the user's task spans multiple phases, show the sequence:

1. **Phase 1** → Use `skill-A` to [action]
2. **Phase 2** → Use `skill-B` to [action]
3. **Phase 3** → Optional: `skill-C` if [condition]

---

## Scoring Quick Reference

Use this mental model to speed up matching:

| User Says                                  | Primary Skills to Check                            |
| ------------------------------------------ | -------------------------------------------------- |
| "document this"                            | generate-docs-init, generate-docs-update, ...      |
| "test this", "write tests"                 | tdd, tdd-workflow, test-coverage-review, ...       |
| "refactor this", "clean up code"           | safe-refactor, code-review, ...                    |
| "which framework/language should I use?"   | technical-decision-helper, ...                     |
| "I don't know where to start"              | tlc-spec-driven, blueprint, plan-generator, ...    |
| "make this performant", "optimize this"    | perf-web-optimization, ...                         |
| "design this system/architecture"          | domain-analysis, modular-decomposition, ...        |
| "visualize this"                           | mermaid-studio, mermaid-erd, mermaid-class-diagram |
| "research this topic"                      | deep-research-web, deep-research, ...              |
| "security", "vulnerabilities"              | security-best-practices, ...                       |
| Language-specific (Python, Go, TypeScript) | [language]-style-guide, [language]-patterns, ...   |

---

## Rules to Follow

1. **Always read both index.yaml files fresh.** Do not go from memory about which skills exist.
2. **Exact matches first**: If the skill description uses the same words/domain as the user's task, recommend it.
3. **Be specific about "why"**: Don't just say "this skill does analysis" — explain what analysis and why it matters for THIS task.
4. **No skill is too obscure to mention**: If it's in the inventory and it matches, include it. Let the user decide if they want it.
5. **Group by relevance level**: Put Direct and Strong matches first, Moderate below, note Weak in "Gaps" if relevant.
6. **Explain trade-offs**: If two skills partly overlap but serve different purposes, clarify the difference.

---

## Examples

### Example 1: User asks "How do I make sure my tests are good?"

**Analysis** → Keywords: testing, coverage | Task: quality assurance

**Recommended skills**:

- `test-coverage-review` (Direct) — Analyzes test coverage gaps pre/post-implementation
- `tdd-workflow` (Strong) — TDD methodology with 80%+ coverage enforcement
- `python-testing` (Strong, if Python code) — pytest patterns with fixtures and mocking
- `code-review` (Moderate) — Reviews code including test quality aspects

---

### Example 2: User asks "I want to explore architecture options for my monolith"

**Analysis** → Keywords: architecture, monolith, design | Task: decision-making + planning

**Recommended skills**:

- `domain-analysis` (Direct) — Maps domains and suggests service boundaries
- `modular-decomposition` (Direct) — Monolith-to-modular pipeline with component sizing
- `technical-decision-helper` (Strong) — Frameworks for evaluating architecture trade-offs
- `legacy-migration-planner` (Strong) — Strategy for phased extraction/modernization
- `blueprint` (Moderate) — Multi-phase construction planning for complex refactors

---

### Example 3: User asks "help me build a landing page"

**Analysis** → Keywords: landing, UI, frontend | Task: design + implementation

**Recommended skills**:

- `frontend-blueprint` (Direct) — Discovery process before code generation
- `frontend-design` (Direct) — Production-grade UI/component creation
- `tailwindcss` (Strong, if Tailwind used) — Utility-first styling patterns
- `seo` (Moderate) — Landing pages benefit from SEO optimization
- `design-image-diff` (Weak, optional) — For QA comparison vs mockup

---

## Troubleshooting

### Q: No skills seem to match the user's request

**A**: Check that you're reading the full descriptions from both index.yaml files, not just the names. Some skills have domain-specific triggers buried in the description. If truly no match, say so — and suggest the closest fit with a note about the gap.

### Q: Multiple skills seem to do the same thing

**A**: They likely focus on different phases or depths. Clarify the difference:

- `test-coverage-review` = analyzing gaps in finished test suite
- `tdd` = writing tests FIRST before implementation
- `python-testing` = pytest idioms and patterns (language-specific)
- These often chain together in one workflow.

### Q: Should I recommend a skill if the user hasn't asked about it?

**A**: Yes, if it's relevant to the task. Use judgment: if a user asks "how do I refactor this legacy code?" and there's a `safe-refactor` skill, recommend it proactively — they probably _should_ use it even though they didn't name it. But don't go overboard with weak connections.

### Q: User asks "do I need this skill?"

**A**: Read the skill's description carefully. If the user's task matches the triggers in the description, the answer is probably yes. If it barely matches, suggest trying the skill's intro example first to see if it's useful for their context.
