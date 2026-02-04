---
name: writing-flashcards-from-docs
description: Use when turning a documentation link or article into spaced-repetition flashcards - fetches and extracts core ideas, compares against existing cards/notes, right-sizes output by source density and existing coverage, updates only incorrect/outdated cards, and creates missing cards with strict citation, slug, and tag rules
---

# Writing Flashcards From Docs

## Overview
Turn a source link (docs/article) into **high-signal flashcards** without damaging accurate existing cards.

**Core principle:** *Don’t churn the vault.* Only change a card when you can point to a specific, authoritative source section showing it is wrong/outdated.

## When to Use
Use this when you are asked to:
- “Make flashcards from this link” / “turn this doc into cards” / “update our cards from docs”
- Refresh cards for an exam (#SAP-C02, etc.)
- Merge new documentation into an existing knowledge base

Do **not** use this when:
- The input is not a stable source link (no URL / no permalink)
- The task is pure note-taking (not Q/A recall)

## Output Format (Non‑Negotiable)
Each flashcard must be exactly:

```md
**<question>** #card <optional tags>
<answer>
[^<slug>]: [<Title>](<source link>)
```

**No extra structure:** don’t add `###`, `Card 1`, `Q:`/`A:` labels, bracketed headers like `[topic]`, horizontal rules, tables-of-contents, or trailing metadata blocks.

**Hard requirement:** The final output must contain only flashcards.

**No exceptions:** If anything like `<task_metadata>…</task_metadata>`, `session_id`, tool output summaries, or any other non-card text appears, delete it and output only flashcards.

## Format Enforcement (Non-Negotiable)

**1. Source Footnotes Only**
- The source link MUST be a footnote: `[^slug]: [Title](URL)`
- **NEVER** put the URL in the answer text, even if the user asks for "easier reading."
- **NEVER** output JSON, lists of objects, or any structure other than the Markdown format below.

**2. Slug Strategy**
- The footnote slug (`[^slug]`) must describe the **link target** (the section of the docs), NOT the card content.
- **Good Slug:** `sqs-message-metadata` (describes the page/section).
- **Bad Slug:** `message-attributes-limit` (describes the specific fact).
- **Why:** Multiple cards cite the same section. They must share the exact same footnote slug.

**3. Duplication Policy (Zero Tolerance)**
- **NEVER** create a duplicate card if the fact exists in the vault, even if the user provided a new source.
- **Exceptions:** You may append a *new* source footnote to an *existing* card if it provides a better citation or additional context, but do NOT create a new card.
- **Handling Multi-Source Redundancy:** If the user provides multiple links covering the same fact (e.g., limits), extract the fact ONCE, cite the most authoritative source (e.g., Developer Guide > Best Practices), or list both sources in the footnote if they add unique value.

Rules:
- `#card` is mandatory.

- Output **only cards** (no headings like `###`, no commentary, no extra metadata).
- Never use vault links in the **question** (no `[[...]]` in questions).
- Answer may use Markdown: lists, tables, code blocks.
- For internal vault references in the **answer**, use wiki links:
  - `[[AWS Lambda]]`
  - `[[AWS Lambda|Lambda]]` (override display text)
- When you mention a topic that likely has an existing note (languages, services, core concepts), prefer a wiki link (e.g., `[[Python]]`, `[[Java]]`). If you’re unsure a note exists, leave it unlinked.
- The footnote must reference the **original source document**, not other flashcards.
- The footnote link MUST be a Markdown link `[Title](URL)`, NOT a bare URL.

## Quick Reference

Before you output anything:
1. Fetch the source link.
2. Extract candidate facts/contrasts (don’t target a fixed number).
3. Search vault for existing coverage.
4. For each candidate: **Update** (wrong), **Create** (missing), or **Skip** (already covered).
5. For each output card: verify format + deep link + slug policy (slug must describe the LINK, not the card).

## Workflow

### 1) Fetch, Extract, and Right-Size
1. Fetch the provided documentation/article URL.
2. Identify:
   - Definitions (what is X?)
   - Contrasts (X vs Y)
   - Rules/limits (quotas, thresholds, defaults, constraints)
   - “If/then” behaviors (decision rules, exceptions, fallbacks)
   - Lists you must memorize (states, phases, enum values)
3. **Scan for anchors:** Look for `#` links next to headers. You will need these for deep linking.
4. If you cannot confidently support a detail from the source, **omit it** (do not “fill in” from memory).

**Right-size how many cards you create.** Do not precommit to a number (e.g., “make 30 cards”). The correct card count depends on:
- **Information available in the source:** short + shallow sources yield few cards; long + dense references yield more.
- **Existing coverage quality:** if the vault already covers it accurately, you will mostly **skip** (and may output very few cards).
- **Requested difficulty (if provided):** difficulty changes *what* you select and how deep you go.

If the user demands a fixed quota, treat it as a preference, not a requirement. Never pad with redundant or low-signal cards.

### 2) Compare With Existing Knowledge
Before writing anything new:
1. Search for existing cards/notes about the same topic.
2. Classify each candidate:
   - **Accurate** → do not touch
   - **Outdated/wrong** → update (minimal edit)
   - **Missing** → create a new card

**Update rule:** Update old flashcards **only** if they contain outdated or wrong information.

### 3) Create / Update Cards
For each extracted idea, pick the right action:
- **Update** if the existing card contains a factual error, contradicted by the new source.
- **Create** if the idea is missing in the vault.
- **Skip** if the info is already covered by an existing card/note.

## Card Style & Quality (No Fluff)
- **Capture the gist, not the text.** Do not copy-paste corporate documentation speak.
- **Be concise.** Remove fluff, intro clauses, and marketing language ("fully managed", "seamlessly integrated", "helps you to...").
- **Plain English.** Explain it like you are talking to a smart engineer, not reading a brochure.
- **Bad:** "Amazon SQS temporary queues help you save development time and deployment costs when using common message patterns such as request-response."
- **Good:** "They act as lightweight, low-cost reply channels for request-response patterns without needing API calls to create."

Keep cards:
- Atomic (one fact/contrast per card)
- Specific (avoid vague “tell me about X”)
- Testable (answer can be checked against source)

**Question Style by Difficulty:**

| Level | Goal | Question Style | Example |
| :--- | :--- | :--- | :--- |
| **#beginner** | **Vocabulary & Models** | **Simple Recall** (Definition, Purpose) | "What is the default S3 storage class?" |
| **#advanced** | **Decisions & Trade-offs** | **Comparison / Synthesis** (Why X over Y?) | "Why choose S3 Standard over S3 Intelligent-Tiering for predictable workloads?" |
| **#expert** | **Internals & Edge Cases** | **Constraints / Scenarios** (What happens if...?) | "What happens to an SQS batch if one message fails and `ReportBatchItemFailures` is disabled?" |

**Global Rules:**
- **NO Yes/No Questions (CRITICAL):** Questions starting with "Is", "Does", "Can", "Are" are **FORBIDDEN**.
  - **BAD:** "Does SQS limit consumption?"
  - **GOOD:** "How does SQS handle consumption limits?"
  - **BAD:** "Is FIFO compatible with fair queuing?"
  - **GOOD:** "What is the compatibility between FIFO and fair queuing?"
- **NO "Tell me about":** "Tell me about SQS" -> **BAD**.
- **Rewording Pattern:** If a user asks "Does X do Y?", reframe as "How does X handle Y?" or "What is the behavior of X regarding Y?"

## Citations, Slugs, and Links

### Source Link
- Use the original documentation/article you were given.
- **Mandatory:** You MUST use deep links (anchor tags) to the specific subsection whenever available (e.g., `.../sqs-temporary-queues.html#virtual-queues`).
- Verify anchors exist by checking the source HTML or URL bar behavior.
- Do not cite *additional* documents unless explicitly allowed; keep cards grounded in the provided source.
- If you absolutely can’t deep link (no ID/name attributes), cite the closest stable section URL.

### Slug
- Slug is a short identifier derived from the **link target** (filename + anchor), NOT the card question.
- **Slug Rule:** The slug MUST describe the specific section being linked to (e.g., `virtual-queues`, `sqs-limits`, `lambda-runtimes`).
- **Reuse:** Multiple cards citing the same section MUST use the exact same slug.
- Put exactly **one** footnote per card.
- Good: `virtual-queues` (for `...#virtual-queues`), `sqs-dead-letter-queues` (for `...#sqs-dead-letter-queues`).
- Bad: `sqs-cost` (describes card topic, not link), `temp-queue-benefits` (describes card topic).

## Tags
- Always include `#card`.
- Optionally include:
  - `#<exam-code>` (e.g., `#SAP-C02`)
  - `#<secondary-topic>` (e.g., `#iam`, `#sqs`, `#ec2`, `#k8s`)
  - `#<difficulty-level>` (`#beginner`, `#advanced`, `#expert`) when the user asked for a level

## Difficulty Calibration
When difficulty is specified, use the **Question Style by Difficulty** table above to select facts and frame questions.

### Beginner (`#beginner`)
- **Focus:** Core definitions, primary purposes, and "what is" questions.
- **Avoid:** Deep internals, obscure limits, complex failure scenarios.
- **Mental Model:** "Introductory Survey Course" - build the vocabulary first.

### Advanced (`#advanced`)
- **Focus:** Trade-offs, decision-making rules ("when to use X vs Y"), and key operational limits.
- **Avoid:** Rare edge cases that don't affect architectural decisions.
- **Mental Model:** "Senior Engineer" - justify your choices.

### Expert (`#expert`)
- **Focus:** Edge cases, race conditions, precise internal behaviors, and specific failure modes ("what happens if X fails while Y is retrying?").
- **Avoid:** Basic definitions or obvious marketing features.
- **Mental Model:** "Principal Engineer / Troubleshooter" - why is it breaking?


## One Good Example
```md
**What is the difference between an IAM managed policy and an inline policy?** #card #beginner #iam
Managed policies are standalone and reusable across identities; inline policies are embedded in exactly one identity (user/group/role) and aren’t reusable.
[^iam-managed-vs-inline]: [Managed policies and inline policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html)
```

## Common Mistakes
- Editing cards “to refresh wording” even when accurate (churn).
- Citing another flashcard instead of the source doc.
- Using a top-of-page link when a subsection anchor exists.
- Creating duplicates instead of linking to existing notes with wiki links like `[[AWS Lambda]]`.
- Multi-fact cards that mix definitions + exceptions + limits.
- **Using `#easy` instead of `#beginner`.**
- **Creating slugs based on the question (e.g., `sqs-cost`) instead of the link (e.g., `virtual-queues`).**
- **Using bare URLs in footnotes instead of Markdown links.**

## Rationalization Table (Do Not Believe These)
| Excuse | Reality |
|--------|---------|
| “The new source is a 'Best Practices' guide” | A fact is a fact. Cite the most authoritative source on the existing card or skip. |
| “I’ll just add a second card to be safe” | Duplicates cause revision conflicts. Zero tolerance. |
| “Boss wants everything refreshed” | Only update when wrong/outdated; accuracy > churn. |
| “Duplicates are fine” | Duplicates rot; link to `[[Existing Note]]` (or `[[Existing Note|Label]]`) or skip. |
| “I can’t deep-link, I’ll cite the root” | Try anchors first; cite the closest stable subsection URL. |
| “I’ll add one more AWS/K8s link to be safe” | Use only the provided source unless explicitly allowed. |
| “I know this from memory; the doc probably says it” | If the source didn’t back it, omit it. |
| “The slug describes the card better” | Slugs describe the **source**. Use the filename/anchor name. |
| “Bare URLs are faster to read” | Markdown links are the standard. Follow the format. |
| “User asked for links in the answer” | Footnotes are mandatory. User convenience < Standard format. |
| “Topic slugs help me identify the card” | Slugs identify the SOURCE. Use source-based slugs. |
| “A Yes/No question is simpler/faster” | It leads to shallow recall. Reword to "What is...?" or "How does...?" |

## Red Flags — STOP
- "I'll rewrite all cards for consistency."
- "This seems right from memory; no need to fetch."
- "The doc is long; I’ll cite the top."
- "User asked for formal tone so I'll keep the fluff."
- "User asked for inline links."
- "Duplicates are acceptable."
- "I’ll cite extra docs / API pages to pad accuracy."
- "I’ll infer missing details."
- "I'll use #easy because it's shorter."
- "I'll make up a slug based on the question."
- "It's just a quick yes/no check."
- "It starts with 'Does', but I can't think of another way." -> **STOP. Use "How does..." or "What is..."**
