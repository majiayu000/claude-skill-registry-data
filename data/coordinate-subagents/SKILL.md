---
name: coordinate-subagents
description: Advanced subagent troubleshooting. Use when subagent calls fail, return bad output, or need voting for critical decisions.
tools: [ Task ]
---

# Subagent Troubleshooting & Advanced Patterns

Core coordination patterns are in CLAUDE.md `<subagent_coordination>`. This skill covers edge cases.

---

## When to Load This Skill

- Subagent returned malformed output twice
- Need voting pattern for critical/irreversible decision
- Debugging why coordination isn't working
- Learning TOON format syntax details

---

## Voting for Critical Decisions

For irreversible actions (deletions, deployments, security assessments), run same query 2-3 times in parallel:

```xml
<!-- 3 parallel agents, same question -->
<invoke name="Task">
  <parameter name="subagent_type">Explore</parameter>
  <parameter name="model">haiku</parameter>
  <parameter name="prompt">@type: AssessAction about: "safe to delete auth_old.ts" ...</parameter>
</invoke>
<invoke name="Task">
  <parameter name="subagent_type">Explore</parameter>
  <parameter name="model">haiku</parameter>
  <parameter name="prompt">@type: AssessAction about: "safe to delete auth_old.ts" ...</parameter>
</invoke>
<invoke name="Task">
  <parameter name="subagent_type">Explore</parameter>
  <parameter name="model">haiku</parameter>
  <parameter name="prompt">@type: AssessAction about: "safe to delete auth_old.ts" ...</parameter>
</invoke>
```

**Interpret results:**
- 3 agree → proceed confidently
- 2 agree → proceed with caution, note dissent
- All differ → query is ambiguous, refine and retry

---

## Red-Flag Recovery

| Symptom | Action |
|---------|--------|
| Output exceeds budget by >30% | Discard entirely, retry same prompt |
| Wrong format (expected TOON, got prose) | Discard, retry with stricter instruction |
| 2 consecutive failures | Refine query OR escalate model (haiku→sonnet) |
| Contradictory answers across retries | Query is ambiguous, decompose further |

**Never:** Try to parse/repair confused output. Discard and retry.

---

## TOON Format Reference

Token-Oriented Object Notation. Use for uniform arrays (file lists, steps, configs).

### Basic Syntax

```toon
# Array with header declaring fields
items[N]{field1,field2,field3}:
  value1,value2,value3
  value1,value2,value3
```

### Escaping

- Commas in values: wrap in quotes `"value, with comma"`
- Quotes in values: escape `\"nested quote\"`
- Newlines: use `\n`

### Examples

**File list:**
```toon
files[3]{path,purpose,lines}:
  src/auth/login.ts,Main login handler,145
  src/auth/session.ts,Session management,89
  src/auth/token.ts,JWT utilities,67
```

**Process steps:**
```toon
steps[4]{position,action,file}:
  1,Parse request body,src/middleware/parser.ts
  2,Validate auth token,src/middleware/auth.ts
  3,Check permissions,src/middleware/rbac.ts
  4,Execute handler,src/routes/api.ts
```

**Key-value config:**
```toon
config[3]{key,value}:
  maxTokens,1500
  format,toon
  itemLimit,10
```

---

## Anti-Patterns Checklist

If coordination isn't working, check for these:

| Anti-Pattern | Fix |
|--------------|-----|
| Single agent doing multiple tasks | Split: one task per agent |
| No token budget specified | Add `@constraints: maxTokens: N` |
| Using opus for simple search | Downgrade to haiku |
| Full conversation history in prompt | Strip to goal + constraints only |
| Sequential independent calls | Parallelize in one message |
| Parsing broken output | Discard and retry instead |
| Asking to "explain" or "describe" | Request structured format |
| Direct MCP/web tool calls in main context | Delegate: payloads unpredictable, request TOON summary |
| Verifying N external sources inline | Delegate: N scrapes = N×2000 tokens wasted |

---

## Decomposition Examples

**Bad: Compound task**
```
Find authentication code and analyze security vulnerabilities and suggest fixes
```

**Good: Three focused agents**
```
Agent 1: Find authentication code (haiku, 1500 tokens)
Agent 2: Analyze security of [files from agent 1] (sonnet, 2000 tokens)
Agent 3: Suggest fixes for [issues from agent 2] (sonnet, 2000 tokens)
```

Note: Agent 2 depends on Agent 1, so run sequentially. But if you had 3 independent searches, run all in parallel.

---

## Quick Diagnostics

```
Subagent returned garbage
├─ Was format specified? → Add explicit TOON/JSON instruction
├─ Was budget set? → Add @constraints maxTokens
├─ Was task atomic? → Check for "and", split if needed
├─ Right model? → Simple task shouldn't use opus
└─ Second failure? → Escalate model or refine query
```

---

## External Data Operations

MCP tools and web scrapes are **context pollution hazards**:

| Tool | Typical Payload | Risk |
|------|-----------------|------|
| `firecrawl_scrape` | 500-5000 tokens | High - full page content |
| `firecrawl_search` | 200-1000 tokens | Medium - result snippets |
| `WebFetch` | 500-3000 tokens | High - full page content |

**Rule**: Any task involving N external fetches should be delegated with:
- Token budget: `min(N × 200, 2500)` tokens for summary output
- Format: TOON for uniform results, JSON for complex analysis
- Scrape options: `onlyMainContent: true`, `formats: ["markdown"]`

**Example - URL verification:**
```
Task(Explore, sonnet):
  "Verify these 10 legislation URLs. For each, scrape with onlyMainContent:true,
   confirm HTTP 200, identify managing authority from page content.

   @return ItemList in TOON:
   results[10]{jurisdiction,url,status,authority}:
     Commonwealth,https://legislation.gov.au,valid,Office of Parliamentary Counsel
     ...

   @constraints: maxTokens: 2000"
```

---

## Reference

- Core patterns: `CLAUDE.md` `<subagent_coordination>`
- TOON format details: `references/toon-format.md`
- Source: "Solving a Million-Step LLM Task with Zero Errors" (arxiv:2511.09030)
