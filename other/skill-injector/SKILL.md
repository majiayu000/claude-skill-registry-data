---
name: skill-injector
description: Auto-selects and injects relevant skills from the 125+ ECC catalog into agent prompts based on task type, project stack, and agent role. Prevents skill overload by loading only what's needed.
---

# Skill Injector - Smart Skill Selection

Maps task signals to skills from the everything-claude-code catalog and injects only the relevant ones into each agent's prompt. Prevents context bloat by being selective.

## When to Activate

- During task routing (called by task-router skill)
- When an agent needs additional skill guidance mid-task

## Skill Selection Algorithm

### Input
- Task classification (type + complexity) from task-router
- Agent role being dispatched
- Project stack from crew-profile.md
- Skill catalog from crew-skills.json

### Selection Rules

**Rule 1: Always-Active Skills (injected into every agent)**
These are universal best practices (kept minimal for token efficiency):
- `context-budget` — monitor token consumption (subsumes strategic-compact)
- `verification-loop` — verify before claiming done
- `coding-standards` — follow project conventions

Note: `iterative-retrieval` moved to bug-fix task-type skills. `search-first` moved to feature task-type skills. `strategic-compact` dropped (redundant with context-budget).

**Rule 2: Stack-Specific Skills (based on detected languages)**

| Stack | Skills |
|-------|--------|
| JavaScript/TypeScript | typescript-patterns, backend-patterns |
| React | react-patterns, react-testing |
| Next.js | nextjs-patterns |
| Vue | vue-patterns, nuxt4-patterns |
| Python | python-patterns |
| Django | django-patterns, django-security, django-tdd |
| Flask | python-patterns |
| Go | golang-patterns |
| Rust | rust-patterns |
| Java | java-patterns, springboot-patterns |
| Kotlin | kotlin-patterns, kotlin-testing |
| C++ | cpp-coding-standards, cpp-testing |
| C# | csharp-testing, dotnet-patterns |
| Flutter/Dart | dart-flutter-patterns |
| Swift | swiftui-patterns, swift-concurrency-6-2 |
| PHP/Laravel | php-patterns, laravel-patterns |

**Rule 3: Task-Type Skills (based on classified task type)**

| Task Type | Skills |
|-----------|--------|
| bug-fix | iterative-retrieval, deep-research, codebase-onboarding |
| feature | architecture-decision-records, agentic-engineering, blueprint, search-first |
| refactor | architecture-decision-records, backend-patterns |
| test | tdd-workflow, e2e-testing, ai-regression-testing |
| security | security-scanning |
| docs | article-writing, documentation-lookup |
| devops | deployment-patterns, docker-patterns, database-migrations, git-workflow |
| review | verification-loop |
| performance | cost-aware-llm-pipeline |

**Rule 4: Agent-Role Skills (specific to the dispatched agent)**

| Agent | Additional Skills |
|-------|------------------|
| ceo | agentic-engineering, architecture-decision-records |
| vp-engineering | architecture-decision-records, hexagonal-architecture |
| vp-quality | verification-loop, tdd-workflow |
| senior-dev | (stack skills + task skills) |
| junior-dev | coding-standards only (keep prompt small for Haiku) |
| code-reviewer | verification-loop, security-scanning |
| debugger | iterative-retrieval, deep-research |
| security-analyst | security-scanning |
| devops-engineer | deployment-patterns, docker-patterns |
| doc-writer | article-writing |
| test-engineer | tdd-workflow, e2e-testing |

### Output: Skill Injection Payload

For each agent being dispatched, generate a skills section:

```markdown
## Injected Skills for this Task

### From: {skill-name}
{Condensed key guidance from the skill - NOT the full SKILL.md, just the most relevant rules and patterns for this specific subtask}

### From: {skill-name-2}
{Condensed guidance}
```

### Token Budget per Agent

To prevent context bloat from too many skills:

| Agent Model | Max Skill Tokens | Max Skills |
|-------------|-----------------|------------|
| Opus (CEO) | 3000 tokens | 6 skills |
| Sonnet (leads/senior) | 2000 tokens | 4 skills |
| Sonnet (planner in lite mode) | 2500 tokens | 5 skills |
| Haiku (junior/devops/docs) | 800 tokens | 2 skills |

**Lite mode note**: When `--lite` flag is used, no Opus agents are dispatched. The vp-engineering agent takes over planning duties and gets an expanded budget (2500 tokens, 5 skills) to compensate for the extra architectural context it needs.

If selected skills exceed the budget:
1. Prioritize: always-active > task-type > stack > agent-role
2. Truncate to key rules only (skip examples, anti-patterns)
3. Drop lowest-priority skills

## Skill Content Condensation

When injecting a skill, don't paste the entire SKILL.md. Extract only:
1. The core rules/principles (2-5 bullet points)
2. The most relevant pattern for this specific task
3. Any critical anti-patterns to avoid

Example condensation:
```
Full SKILL.md: 200 lines, ~2000 tokens
Condensed injection: 15 lines, ~150 tokens
```

This keeps agent prompts focused and within token budget.
