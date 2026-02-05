---
name: spellbook-auditing
description: "Meta-audit skill for spellbook development. Spawns parallel subagents to factcheck docs, optimize instructions, find token savings, and identify MCP candidates. Produces actionable report."
---

# Audit Spellbook

<analysis>
Crystallized principles enabling comprehensive spellbook auditing through parallel subagent orchestration.
</analysis>

## Invariant Principles

1. **Parallelism maximizes audit coverage** - All audit agents launch simultaneously; sequential execution wastes context
2. **Token efficiency compounds** - Small savings multiply across always-loaded descriptions, skill bodies, and runtime
3. **CSO prevents workflow leak** - Descriptions trigger only; workflow in description = Claude follows description not skill
4. **Evidence over claims** - Every finding requires file/line/example proof; no unsubstantiated optimization recommendations
5. **Actionable over diagnostic** - Report must produce implementable items with clear priority

## Trigger Conditions

Use when: "audit spellbook", "optimize skills", pre-release quality check, token usage concern, periodic maintenance.

## Execution Model

<reflection>
Single-message parallel launch of ALL audit agents. Each agent: focused scope, JSON output, thorough within domain. Report compiles after all complete.
</reflection>

### Phase 1: Parallel Audit Subagents (Launch ALL in ONE message)

| Agent | Scope | Output Format |
|-------|-------|---------------|
| **Factcheck** | README, docs/**/*.md, CHANGELOG, claims | `{file, line, claim, status, evidence}[]` |
| **Instruction Engineering** | skills/*/SKILL.md, commands/*.md, templates | `{file, issues: [{principle, violation, suggestion}], score}[]` |
| **CSO Compliance** | Skill/command descriptions | `{file, current_desc, cso_status, issues, proposed_desc, rationale}[]` |
| **Instruction Optimizer** | All instruction content | `{file, optimizations: [{section, issue, before_tokens, after_tokens, proposed}], savings}[]` |
| **MCP Candidate** | Tool call patterns | `{pattern, occurrences, proposed_mcp_name, signature, savings}[]` |
| **YAGNI** | Entire spellbook | `{item, type, concern, recommendation, confidence}[]` |
| **Persona Quality** | fun-mode assets (if exists) | `{personas, contexts, undertows, synthesis_issues}` |
| **Consistency** | All skills/commands | `{inconsistency_type, examples, suggested_standard}[]` |
| **Dependency** | Skill/command/MCP relationships | `{graph, orphans, circular_deps, hotspots}` |
| **Test Coverage** | MCP tools, workflows | `{component, type, has_tests, quality, gaps}[]` |
| **Token Counting** | All files | `{total, always_loaded, deferred, by_file, rankings}` |
| **Conditional Extraction** | Templates, commands | `{file, line_start, line_end, trigger, tokens, proposed_skill, difficulty}[]` |
| **Tables-Over-Prose** | All prose sections | `{file, section, current_tokens, proposed_tokens, savings_pct, example}[]` |
| **Glossary Opportunity** | Repeated definitions | `{term, occurrences, canonical_definition, savings}[]` |
| **Naming Consistency** | All names | `{name, type, current_pattern, expected_pattern, compliant, suggested_rename}[]` |
| **Reference Validation** | All skill/command refs | `{file, line, reference, exists, type_mismatch, suggestion}[]` |
| **Orphaned Docs** | docs/ vs source alignment | `{file, issue, expected_source, recommendation}[]` |

### CSO Status Categories

| Status | Meaning |
|--------|---------|
| CSO_COMPLIANT | Follows all principles |
| WORKFLOW_LEAK | Contains process Claude might follow instead of skill |
| MISSING_TRIGGERS | No "Use when..." or symptoms |
| TOO_BROAD | Triggers for unrelated tasks |
| TOO_NARROW | Missing natural keywords |
| AMBIGUOUS_TRIGGERS | Multiple conditions need numbered enumeration |

### Phase 2: Compile Report

Save to: `~/.local/spellbook/docs/<project-encoded>/audits/spellbook-audit-YYYY-MM-DD-HHMMSS.md`

Structure: Executive Summary (savings, critical issues, MCP candidates) -> Per-agent results -> Prioritized actionable items.

### Phase 3: Implementation Prompt

Present options via AskUserQuestion:
1. Implement high-priority items now
2. Implement all items
3. Review report first
4. Skip implementation

If implementing: invoke `writing-plans` skill, gather clarifying questions upfront, execute with appropriate skills.

## Helper Skills

| Skill | Use For |
|-------|---------|
| `writing-skills` | **AUTHORITATIVE** CSO/description guidance |
| `instruction-engineering` | Restructuring instructions |
| `instruction-optimizer` | Compressing verbose content |
| `writing-plans` | Implementation planning |
| `fact-checking` | Deep claim verification |
| `finding-dead-code` | Unused MCP tool code |
| `green-mirage-audit` | Test quality |

## Naming Convention Reference

| Type | Pattern | Examples |
|------|---------|----------|
| Commands | Imperative verb(-noun) | execute-plan, verify, handoff |
| Skills | Gerund/Noun-phrase | debugging, test-driven-development |
| Agents | Noun-agent (role) | code-reviewer, fact-checker |

## Critical: Workflow Leak Bug

Description summarizes workflow -> Claude follows description, ignores skill body. Real failure: "code review between tasks" in description caused ONE review instead of TWO specified in skill.

**Formula:** `"Use when [triggering conditions/symptoms]"` - NEVER `"Use when X - does Y then Z"`

**Verify:** After fixing descriptions, confirm Claude reads full skill content.
