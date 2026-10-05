---
name: research-answer
description: Systematic web and codebase research workflow for information queries
  and fact verification. Gathers authoritative sources, executes query chains, evaluates
  evidence, and synthesizes grounded answers with inline citations.
argument-hint: <research question or topic>
---

<!-- Generated from workflows/research-answer.md by tools/generate_integrations.py. Edit the source file, not this one. This is an execution WORKFLOW packaged as an Agent Skill so it is discoverable and directly invocable ("/research-answer") in every compatible tool. -->

# Workflow: Research-then-Answer

## When to Use
| Criteria | Match |
|----------|-------|
| Intention | information_query, fact_check, research |
| Complexity | varies — from simple FAQ to deep research |
| Power Mode | Eco (simple) or Balanced/Deep (complex) |
| Clarity | user wants information, not code changes |

## Required Skills
- web-search-research
- browser-automation (if interactive browsing is needed)
- communication-tone
- safety-profiles (default; relaxed if OSINT/security research)

## Flow

### Step 0: Thinking Stage (Pre-Action)
- [ ] What exactly is the user asking? Factual question, comparison, deep research?
- [ ] Is this time-sensitive? (current events, recent changes = MUST search)
- [ ] What do I already know vs what do I need to verify?
- [ ] Never fabricate citations or sources — if unsure, search

### Step 1: Determine Research Depth
- **Simple fact**: single search, direct answer
- **Moderate topic**: search → read → synthesize
- **Deep research**: multi-query chain, cross-reference, evaluate sources

### Step 2: Search
- Use dedicated search tools (not google.com via browser)
- For time-sensitive queries: search before answering regardless
- For niche topics: use specific queries
- Chain searches: use findings to inform next query

```python
# Simple: one search
search_web("current CEO of OpenAI 2026")

# Deep: chain searches
search_web("transformer architecture limitations long context")
→ find "attention quadratic complexity"
search_web("sparse attention methods long context 2025 2026")
→ compare approaches
search_web("RingAttention vs sparse attention benchmarks")
→ get performance data
```

### Step 3: Read & Extract
- Use search results as starting points
- Visit authoritative sources directly
- Extract relevant facts with source attribution
- For long pages: use text extraction over scrolling

### Step 4: Synthesize
- Compare multiple sources
- Resolve contradictions (flag if can't)
- Distinguish: confirmed facts vs likely vs speculation
- Organize by relevance to user's question

### Step 5: Cite & Answer
- Every factual claim gets a citation: `[source:N]`
- Answer directly — don't start with "Great question!"
- Structure: summary first, then details
- For complex topics: use headings to organize
- Offer to go deeper if user wants more

### Step 5b: Sanity Check
- [ ] Is every factual claim supported by a real citation? *(Perplexity)*
- [ ] Are citations inline (not a bibliography at end)?
- [ ] Did I search before answering if info may have changed?
- [ ] Am I distinguishing confirmed facts from speculation or uncertainty?
- [ ] Have I presented multiple viewpoints for contested topics? *(Anthropic evenhandedness)*
- [ ] Never cite fabricated IDs — verify each citation exists

### Step 6: Final Answer
- Wrap final answer in `<answer>` tags (Perplexity pattern)
- NEVER include bibliography at end — citations are inline only
- NEVER cite fabricated information

## Token Budget
- **Simple fact**: 1K-3K tokens
- **Moderate research**: 5K-15K tokens
- **Deep research**: 20K-50K tokens
- **Warning threshold**: >50K → offer to continue in next session

## Hallucination Watchpoints
- Fabricating citations (most dangerous error)
- Overconfident claims from single source
- Confirmation bias — only citing sources that agree
- Presenting speculation as fact
- Not searching when info is time-sensitive
- Relying on training data for current events
