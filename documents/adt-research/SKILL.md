---
name: research
description: Deep research on a topic using web search, docs, and codebase analysis
triggers:
  - research
  - investigate
  - what does X do
  - how does X work
  - find information about
  - ultraresearch
---

# Research

Exhaust all available sources before concluding. Don't stop at the first result.

## Sources (in order)

1. **Codebase** — search existing code first; answer may already be there
2. **Library docs** — use context7 or equivalent for up-to-date package docs
3. **Web search** — use for current state, comparisons, best practices
4. **GitHub** — search issues/PRs for known bugs and workarounds

## Rules

- Verify claims against primary sources — don't trust summaries of summaries
- Note the date of sources; docs for old versions mislead
- When sources contradict, report the contradiction — don't pick one silently
- If uncertain after exhausting sources, say so explicitly

## Output

```markdown
## Finding: <topic>

### Summary
<2-3 sentences>

### Key Facts
- <fact with source>
- <fact with source>

### Uncertainties
- <what is unclear or unverified>

### Recommendation
<what to do based on findings>
```
