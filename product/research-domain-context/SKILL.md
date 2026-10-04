---
name: research-domain-context
description: Research vertical domain knowledge via web when LTM is insufficient
user-invocable: false
model: sonnet
allowed-tools: WebSearch, WebFetch, Read, Write
---

# research-domain-context

Model-invocable skill for researching vertical domain knowledge when Long-Term Memory has insufficient coverage.

## Purpose

Perform targeted web research to fill domain knowledge gaps identified during context loading. Produce a structured domain context artifact written to STM for use by downstream skills.

You DO the research and write the artifact. You do NOT decide what happens with it next. The calling agent receives this output and decides how to use the domain context.

**DOES:**
- Search the web for market data, competitive landscape, industry trends, regulatory context
- Synthesize findings into structured domain knowledge
- Write domain-context.md to the specified STM path

**DOES NOT:**
- Make product strategy decisions
- Evaluate or score the domain opportunity
- Generate vision, roadmap, or backlog content
- Promote STM to LTM (that's a separate lifecycle concern)

## Input

Receive from agent:
- `domain` — (required) Identified vertical domain (e.g., "BFSI", "retail SaaS", "healthcare B2B")
- `knowledge_gaps` — (required) List of what LTM didn't cover (e.g., ["competitive landscape", "market size", "regulatory requirements"])
- `problem_statement` — (required) Original problem statement for research context
- `output_base` — (required) STM path for output (e.g., `.garura/product/discovery/`)

## Process

1. **Construct search queries:** For each knowledge gap, create 1-2 targeted search queries combining domain + gap + problem context. Prefer specific queries over broad ones.

   Examples:
   - Gap: "competitive landscape" + Domain: "BFSI lending SaaS" → "B2B lending SaaS competitors market 2025 2026"
   - Gap: "regulatory requirements" + Domain: "healthcare B2B" → "healthcare SaaS regulatory compliance HIPAA requirements"

2. **Execute searches:** Run WebSearch for each query. Maximum 5 searches total per invocation. If a gap requires more than 2 searches, prioritize depth on the most critical gaps.

3. **Fetch key sources:** For the most relevant search results (top 2-3 per gap), use WebFetch to extract detailed content. Prioritize industry reports, analyst coverage, and authoritative sources over blog posts.

4. **Synthesize findings:** For each knowledge gap, synthesize research into structured sections:
   - What was found
   - Key data points (with source attribution)
   - Confidence level (high/medium/low based on source quality and consistency)

5. **Write artifact:** Write `{output_base}domain-context.md` with:

   ```markdown
   # Domain Context: {domain}

   **Problem:** {problem_statement}
   **Researched:** {date}
   **Source:** research-domain-context skill (web research)

   ## {Knowledge Gap 1}

   {Synthesized findings with data points}

   **Sources:**
   - [{source title}]({url})

   **Confidence:** {high|medium|low}

   ## {Knowledge Gap 2}
   ...

   ## Coverage Summary

   | Gap | Status | Confidence |
   |-----|--------|------------|
   | {gap} | covered|partial|not_found | high|medium|low |
   ```

6. **Return output.**

## Output

```yaml
domain_context:
  path: "{full path to domain-context.md}"
  domain: "{domain}"
  coverage:
    - gap: "{knowledge_gap}"
      status: "covered|partial|not_found"
      confidence: "high|medium|low"
  sources:
    - url: "{source_url}"
      title: "{source_title}"
      used_for: "{which gap}"
```

**IMPORTANT**: This skill produces an artifact and returns metadata. The calling agent receives this output and decides what to do next. Do NOT instruct the agent to return or stop.

## Constraints

- NEVER fabricate market data — if not found via research, report `status: not_found`
- NEVER perform more than 5 web searches per invocation
- ALWAYS include source URLs for traceability — unsourced claims are not acceptable
- ALWAYS write confidence levels — downstream consumers need to know reliability
- NEVER include product recommendations or strategic advice — this skill gathers facts, not opinions
- ALWAYS set artifact as STM (transient) — this is not LTM
- NEVER overwrite an existing domain-context.md without reading it first — append or update sections

## Version

| Field | Value |
|-------|-------|
| Version | 1.0.0 |
| Category | analysis |
