---
name: feature-announcement-writer
description: "Generate a multi-format feature announcement pack from a single product description — no copywriting experience needed. Produces 4 ready-to-use formats: changelog entry, email, in-app push, and social post. Use when launching a new feature, announcing a beta, or preparing a communication pack for multiple channels. Triggers: 'write feature announcement', 'feature announcement writer', 'generate announcement for my feature', 'напиши анонс фичи', 'создай пакет анонса', 'генератор анонса фичи'."
version: 1.0.0
---

# Feature Announcement Writer

This skill generates a ready-to-use multi-format announcement pack from a single product feature description. Designed for product managers, product owners, and content marketers who need to distribute a feature announcement across 4 channels (changelog, email, in-app push, social) without manually rewriting the same information for each format.

**Input:**
- Feature description (plain text, pasted inline or as `.md` file — min 1 paragraph)
- Optional: product name, feature name, target audience (users / customers / internal / developers), launch type (GA / beta / soft launch)

**Output:**
- Markdown document with 4 labeled, copy-ready sections: Changelog Entry, Email Announcement, In-App Push, Social Post (LinkedIn/X)

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Accept and Validate Input

1. Check if the user provided a feature description (inline text or file)
   - If no description provided: Stop — "Please describe the feature you want to announce. Paste a 1–2 paragraph description and I'll generate the announcement pack."
   - If description is a `.docx` or `.pdf` file: Stop — "feature-announcement-writer works with plain text or .md files. Export your document to text format and try again."

2. Check description length
   - If fewer than 1 paragraph (less than 3 meaningful sentences): ask one clarifying question — "What's the main benefit for users?" — then continue with available info

3. Check if this is a sprint summary with multiple features
   - If input contains 5+ distinct feature bullet points or explicit sprint/release framing: Flag — "This looks like a sprint summary with multiple features. For multi-feature release notes, use `release-notes-generator` instead."

### Step 2: Extract Context

1. Scan description for:
   - **Product name** — the product or app this feature belongs to
   - **Feature name/title** — what this specific feature is called
   - **Target audience** — signals like "for users", "for developers", "internal team", "enterprise customers"
   - **Launch type** — signals like "beta", "soft launch", "GA", "early access", "limited release"

2. If product name or feature name cannot be inferred:
   - Ask in **one consolidated question**: "A few quick details: What's the product name? What should I call this feature? (Skip anything you don't need.)"
   - Do not ask multiple separate questions

3. Apply defaults silently (state them in the output header):
   - Audience not specified → default to `users`
   - Launch type not specified → default to `GA`

4. Check if description is entirely technical (API changes, schema updates, dev tooling):
   - If yes: Flag — "Description appears technical — generating developer-facing copy. Say 'user-facing' to switch."

### Step 3: Identify Value Proposition

1. Extract the core user benefit (what the user can now do that they couldn't before)
2. Identify 2–3 supporting benefits or use cases
3. Note tone signals from the description (exciting launch vs. incremental improvement vs. critical fix)

### Step 4: Generate All 4 Formats

Generate all formats in one response. Use clearly delimited sections.

**Format 1 — Changelog Entry**
- Markdown one-liner format: `- [Feature name]: [user benefit description]`
- Plain language; no jargon; no commit hashes
- If launch type is beta: prefix with `[Beta]`

**Format 2 — Email Announcement**
- Subject line: benefit-first; specific (e.g., "New: Export reports as PDF — available today")
  - Do NOT use: "Newsletter", "Update", "We're excited to announce", "We are pleased to"
- Body structure:
  - Opening sentence: lead with biggest user benefit ("Starting today, you can...")
  - Paragraph 1: explain the feature and its 2–3 key benefits in plain language
  - Paragraph 2: mention audience or access details (who gets it, how to find it)
  - Closing: 1 CTA sentence or brief thank-you — no fluff
- Length: 150–250 words
- Tone: professional, direct, benefit-first

**Format 3 — In-App / Push Notification**
- Exactly 1–2 sentences
- Maximum 160 characters (count carefully)
- Structure: verb-first + specific benefit + optional CTA
- Example: "Export reports as PDF — save time on formatting. Try it now."
- If character limit is exceeded: trim to single most impactful sentence

**Format 4 — Social Post (LinkedIn / X)**
- 3–5 sentences
- Conversational tone (not a press release)
- Opens with a hook (question, surprising stat, or direct statement of value)
- Names the feature and 1–2 key benefits
- Ends with one CTA or question to audience
- No emojis unless explicitly requested

### Step 5: Offer Blog Intro

After the 4 formats, add one line:
> "Want me to add a blog intro paragraph? Just say so."

Do not generate it unless requested.

---

## Negative Cases

- **No description provided:** Stop — "Please describe the feature you want to announce. Paste a 1–2 paragraph description and I'll generate the announcement pack."
- **Sprint summary with multiple features:** Flag — "This looks like a sprint summary with multiple features. For multi-feature release notes, use `release-notes-generator` instead."
- **File is .docx or .pdf:** Stop — "feature-announcement-writer works with plain text or .md files. Export your document to text format and try again."
- **Description too sparse:** Ask one question ("What's the main benefit for users?"), then generate.
- **User requests extra format (Slack, press release):** Generate the 4 standard formats first, then offer: "I can also write a [format] — want me to add it?"

---

## Output Format

```
## Feature Announcement — [Feature Name] · [Product] · [Date]
_Audience: [users/customers/internal/developers] · Launch type: [GA/beta/soft launch]_

---

### 📋 Changelog Entry

- [Feature name]: [user benefit description]

---

### 📧 Email Announcement

**Subject:** [Benefit-first subject line]

[Email body: 150–250 words]

---

### 📱 In-App / Push Notification

[1–2 sentences, ≤ 160 characters]

---

### 🔗 Social Post (LinkedIn / X)

[3–5 sentences, hook-first, ends with CTA or question]

---

> Want me to add a blog intro paragraph? Just say so.
```
