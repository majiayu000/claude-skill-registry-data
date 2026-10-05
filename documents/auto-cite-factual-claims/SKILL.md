---
name: Auto-cite Factual Claims
description:
  Add Markdown footnote citations to the factual claims that carry supplied
  text. Use when the user asks to cite claims, add sources or references,
  fact-check and footnote a document, or support statements with web sources.
version: 0.1.0
---

# Auto-cite Factual Claims

Cite the factual claims a skeptical reader would challenge, using sources found
through web search and Markdown footnotes. The user's request sets the scope;
without one, cite the claims the argument rests on, not every fact. Preserve the
text's wording and structure apart from the citations.

## Process

### 1. Select the claims

Read the complete text, then fix the selection:

- When the user names claims, passages, or a class of claims ("cite the
  statistics"), the selection is exactly that.
- Otherwise, select the claims the argument rests on: assertions a skeptical
  reader would challenge, where an error would change the document's
  conclusion. Quantities, dates,
  attributed statements, surprising or contested assertions, and comparisons or
  causal statements that drive a conclusion usually qualify. Common knowledge,
  incidental background, opinions clearly presented as opinions, instructions,
  and the author's own stated intentions do not.

Split a compound sentence into atomic claims when one source might not support
the whole sentence.

Done when each selected claim is atomic and sits inside the user's stated
scope or, without one, is a claim the argument rests on.

### 2. Research the selected claims

Search the web for each selected claim and open the candidate source. Prefer
sources in this order:

1. Primary sources, such as official records, research papers, standards, and
   first-party documentation
2. Authoritative institutions and subject-matter publications
3. Reputable secondary reporting

Match the source to the claim's exact scope, date, geography, quantity, and
degree of certainty. The opened page must state or directly establish the
claim. A search-result snippet is not evidence. For a time-sensitive claim, use
the most recent source that covers the stated period. Record the page title and
canonical URL without tracking parameters.

Done when each selected claim has a source that supports it or is recorded as
unsupported after targeted follow-up searches.

### 3. Place markers

Put a marker immediately after the clause or sentence it supports:

```markdown
The factual claim appears here.[^1]
```

<!-- vale ai-tells.UniversalObject = NO -->
<!-- "every claim" is the condition the rule sets, not a claim about coverage. -->

Use one marker for two or more claims only when its source supports every claim.

<!-- vale ai-tells.UniversalObject = YES -->

Reuse a marker when the same source supports separate claims. Place multiple
markers together when a claim needs two or more sources.

Preserve existing footnotes. Verify any existing citation used to satisfy the
selection by opening its source. For new numeric labels, start after the highest
existing number, or at `1` when the document has none.

Done when each selected claim with a source has a marker that supports that
exact claim.

### 4. Append definitions

Append each new definition at the bottom of the document, after any existing
footnote definitions. Use the source's page title as linked text:

```markdown
[^1]: [Article Title](https://example.com/article)
```

Keep one blank line between definitions. Escape Markdown punctuation in titles
when needed.

For file input, edit the file in place. For inline input, return the complete
cited text. If a selected claim remains unsupported, name it in a brief warning
before the inline text or in the response after editing a file. Leave that
claim unmarked and reserve markers for sources that support the exact claim.

### 5. Audit

Check each selected claim against its opened source. Then check that:

- Each selected claim with a source has a marker.
- New markers sit only on selected claims.
- Each marker has one definition, and each definition is referenced.
- Each definition contains a linked source title and a working source URL.
- Marker placement makes the supported claim unambiguous.
- Footnote labels do not collide.
- The appended definitions are the final document content.

Done when all seven checks pass and each unsupported selected claim is
reported.
