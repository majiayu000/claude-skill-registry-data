---
name: research-synthesizer
version: "1.0.0"
description: "Multi-source research synthesizer. Takes a question, runs 3-5 parallel web searches with varied phrasings, deduplicates, and returns a cited, concise answer. For Hebrew questions, searches in both Hebrew and English. Output is always under ~400 words."
triggers:
  - "research"
  - "find out about"
  - "what do you know about"
  - "synthesize"
  - "look up"
---

# Research Synthesizer Skill

Multi-source search → deduplicate → synthesize → cite. Concise answer under ~400 words, always.

---

## When to Use

Trigger phrases:
- "research [topic]"
- "find out about [topic]"
- "what do you know about [topic]"
- "synthesize [topic]"

- "look up [topic]"

---

## Step-by-Step Process

### Step 0: Clarify the Brief

Before any research on companies, products, or competitors — ask or verify:
1. **What is the positioning of OUR product?** Don't assume. Ask if unclear.
2. **What is the scope?** Competitor analysis? Market sizing? Both?
3. **What will the output be used for?** Pitch deck? Internal doc? Strategy?

This prevents writing a wrong document that needs to be rewritten.

---

### Step 0b: Question Decomposition (GPT Researcher Pattern)

Before searching, decompose the question into specific sub-questions:

```
Input: "What is Paperclip and how does it compare to monday.com?"

Sub-questions:
1. What is Paperclip? What does it do?
2. Who built it and when?
3. What are its core features?
4. How is it positioned vs. project management tools?
5. What does monday.com offer that Paperclip doesn't (and vice versa)?
```

**Rule:** For broad or multi-faceted questions (competitive analysis, "explain X", "compare A and B") — always decompose first. For simple factual questions ("who founded X", "when did Y happen") — skip this step.

Each sub-question becomes its own search query. This produces deeper, less biased results than 5 phrasings of the same question.

---

### Step 1: Classify the Question

Before searching:
- **Language:** Is the question in Hebrew? → search in both Hebrew AND English
- **Type:** Factual? Opinion/trend? Technical? Recent event?
- **Scope:** Narrow (specific fact) or broad (overview topic)?

Adjust query phrasings accordingly.

### Step 2: Generate Query Variants

Create 3–5 distinct query phrasings to maximize coverage and reduce bias:

| Variant | Strategy |
|---|---|
| Q1 | Direct question phrasing |
| Q2 | Keyword-only (no question words) |
| Q3 | "best [topic] explained" / "how does X work" |
| Q4 | Hebrew translation (if applicable) |
| Q5 | Recent angle: "[topic] 2024 2025" or "[topic] latest" |

**Example — question: "What is LangGraph?"**
- Q1: "What is LangGraph and how does it work"
- Q2: "LangGraph framework overview"
- Q3: "LangGraph tutorial explained"
- Q4: *(skip — English topic)*
- Q5: "LangGraph 2024 use cases"

**Example — question: "What is LangGraph?"**
- Q1: "What is LangGraph and how does it work"
- Q2: "LangGraph framework overview"
- Q3: "LangGraph explained simply"
- Q4: "LangGraph explained" (if topic has non-English coverage)
- Q5: "LangGraph 2025 latest"

### Step 2b: Verify Companies — Visit Their Website First

**MANDATORY for any competitor/company research:**

Before writing anything about a company:
1. `web_fetch` their main URL (homepage + relevant sub-pages: /agents, /product, /pricing)
2. `web_search` "[company] funding 2026" AND "[company] review 2026"
3. Only write what you actually found. If unverified — say "unverified"

**Never assume a company's capabilities from its category name.**
Example: "issue tracker" does NOT mean "no agents." Verify.

---

### Step 3: Run Searches (Parallel)

Run all query variants using `web_search`. Collect:
- Title
- URL
- Snippet

Do not fetch full page content unless snippet is insufficient.

### Step 4: Deduplicate, Filter & Score Sources

From all results:
1. Remove duplicate URLs
2. Remove results that don't address the question
3. Remove results older than 2 years for fast-moving topics (AI, tech, news)
4. Score source credibility:
   - **High:** Official docs, peer-reviewed, major publications (TechCrunch, Wired, HBR)
   - **Medium:** Reputable blogs, GitHub repos, well-known newsletters
   - **Low:** Forums, anonymous posts, marketing pages
5. Prioritize high-credibility sources. If only low-credibility sources available — flag it.

Target: 5–10 sources for deep research, 3–5 for quick questions.

### Step 5: Synthesize

Write the answer in this format:

```
[3–5 sentence summary that directly answers the question]

Key points:
• [point 1]
• [point 2]
• [point 3]
• [point 4 — optional]

Sources:
1. [Title] — [URL]
2. [Title] — [URL]
3. [Title] — [URL]
```

**Synthesis rules:**
- Lead with the direct answer, not background
- Use the user's language (Hebrew question → Hebrew answer)
- Max ~400 words total
- If sources conflict → note the disagreement briefly
- If information is outdated → flag it

### Step 6: Deliver

Send the synthesized answer. Do NOT:
- Dump raw search results
- List every source found
- Add filler like "Great question!" or "I searched the web for..."
- Pad with unnecessary caveats

---

## Output Format Template

```
🔍 [Topic]

[Direct 3-5 sentence answer]

📌 Key Points:
• ...
• ...
• ...

📚 Sources:
1. [Title] — [URL]
2. [Title] — [URL]
3. [Title] — [URL]
```

---

## Example

**Input:** "Research: What is Model Context Protocol?"

**Output:**

```
🔍 Model Context Protocol (MCP)

Model Context Protocol (MCP) is an open standard developed by Anthropic that lets LLMs connect uniformly to tools, APIs, and external data sources. Instead of each integration requiring custom code, MCP defines a shared language between the model and the tool server.

📌 Key Points:
• Client-server protocol: the LLM is the client, tools are servers
• Supports stdio and HTTP transport
• Enables: tool calling, resource access, prompts
• Widely adopted: Claude, Cursor, VS Code, and more
• Open source — SDK available for Python, TypeScript, Java

📚 Sources:
1. MCP Official Docs — https://modelcontextprotocol.io
2. Anthropic MCP Announcement — https://www.anthropic.com/news/model-context-protocol
3. MCP GitHub — https://github.com/modelcontextprotocol
```

---

## Hebrew Search Strategy

For Hebrew questions, always search in **both languages**:

| Search | Language | Goal |
|---|---|---|
| Q1–Q2 | English | Get the most content (English web is larger) |
| Q3 | Hebrew | Find Israeli/Hebrew-specific context |
| Q4 | English (simple phrasing) | Get beginner-friendly sources |
| Q5 | English (recent) | Get latest news/updates |

If the topic is inherently Israeli (local news, Israeli law, etc.) → weight Hebrew sources more.

---

## Rules

1. **Always cite sources** — no answer without at least 2 URLs. For competitive analysis: minimum 5 sources.
2. **Clarify positioning before writing** (Step 0) — especially for competitive analysis. Ask what OUR product does before comparing.
3. **Verify companies from their own website** (Step 2b) — never assume from category name.
4. **Deep questions → decompose first** (Step 0b). Simple facts → skip decomposition.
5. **Max ~400 words** — be concise, not exhaustive
6. **One clean doc, not multiple drafts** — get it right before publishing
7. **Direct answer first** — no preamble, no "I will now search..."
8. **Hebrew in, Hebrew out** — match the user's language
9. **Flag uncertainty** — if sources conflict or data is stale, say so
10. **No raw dumps** — synthesize, don't copy-paste snippets
11. **React 👍** when owner requests research, **✅** when delivered
12. After delivering research — write summary to `memory/whatsapp/dms/<PHONE-sanitized>/context.md` if topic was important

### ⚠️ Anti-Bias Rule (CRITICAL)

When researching competitors or doing comparative analysis:
- **❌ Never assume OUR product is superior** — especially when the owner uses it
- **❌ Never dismiss competitors without verification** — statements like "no competitor does X" require actual evidence
- **✅ Treat all products equally** — same depth of research for every tool
- **✅ Credit competitors explicitly** when they do something better or equally well
- **✅ Use G2, Reddit, real user reviews** — not just marketing pages
- **✅ If you can't verify a claim → don't make it**

### ⚖️ Symmetry Rule (from Kate Nir, 2026-04-08)

**If you used Product A hands-on → you must use Product B hands-on too.**
You cannot compare first-hand experience with marketing copy. Either:
- Use both hands-on (browser, trial account, real flow), OR
- Compare both using the same external sources (G2, Reddit, reviews)

Mixing levels of evidence = biased output. Always.

---

Example of bias to avoid:
> ❌ "No competitor sends notes directly to board items — this is unique to monday"
> ✅ "monday syncs notes to board items natively. Notion AI Meetings, tl;dv, and Fireflies also offer project management integrations — verify depth before claiming uniqueness."

When the owner or stakeholder uses a product you're researching — **apply extra skepticism to positive claims about that product.**

---

## Cost Notes

- 3–5 `web_search` calls per research request — moderate cost
- Avoid `web_fetch` unless snippets are truly insufficient
- For simple factual questions (capital cities, dates, etc.) → single search is enough, skip full synthesizer flow
- Cache: if the same topic was researched in the last hour, reuse results
