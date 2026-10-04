---
name: scepticagent-prompts
description: ScepticAgent AI prompt reference. Use whenever the user asks about the prompts, wants to change analysis behaviour, modify what the AI looks for, adjust highlight categories or scoring, understand what instructions are sent to the AI, or tune the output format of analysis or highlights.
---

## Prompt locations — all in `background.js`

### `buildAnalysisSystem(url, title, content)` — lines 658–705

Full page analysis system prompt. Instructs Claude to use `web_search` to verify claims, check source credibility, find supporting/opposing evidence, identify bias and emotional language. Page content truncated to 10000 chars.

Required output sections (renderer depends on these exact headings):
```
## Key Claims
## References & Sources
## Supporting Evidence
## Opposing Perspectives
## Bias & Framing
## Emotional Language
## Misinformation Risks
## Overall Assessment
```

Sources must be cited as inline markdown links e.g. `[Reuters](https://reuters.com/...)`.

---

### `buildChatSystem(url, title, content)` — lines 707–720

Chat follow-up system prompt. Instructs the agent to answer questions about the page using web search and cite sources as inline markdown links. Page content truncated to 10000 chars.

---

### `buildHighlightsPrompt(withSearch)` — lines 108–140

Extracts verbatim phrases from the page. Two modes:

- `withSearch: true` — includes STEP 1 (web_search for real URLs) / STEP 2 (output JSON). Used in manual "Highlight Page" after analysis is complete.
- `withSearch: false` — JSON output only, `source_url` left empty. Used in the auto fast scan on page open.

**Output JSON schema:**
```json
{
  "summary": "two sentences — what the article is about, then how emotional/factual/biased it is",
  "category_summaries": {
    "misinformation": "one sentence",
    "emotional": "one sentence",
    "bias": "one sentence",
    "supported": "one sentence",
    "logical": "one sentence"
  },
  "highlights": [
    {
      "phrase": "verbatim text from page (8–180 chars, no quote characters)",
      "category": "misinformation|emotional|bias|supported|logical",
      "note": "max 90 chars explanation",
      "source": "publication name or empty string",
      "source_url": "full URL or empty string"
    }
  ]
}
```

Constraints: max 25 highlights, phrases must appear verbatim on the page, no markdown code fences in output, no typographic quote characters in phrases.
