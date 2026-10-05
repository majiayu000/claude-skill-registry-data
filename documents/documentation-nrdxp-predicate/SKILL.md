---
name: documentation
description: |
  Writing quality guidelines, formatting conventions, and styling constraints for documentation.
  Trigger when:
  - Writing, editing, or auditing documentation files, READMEs, markdown files, or guides.
  - Modifying files with suffixes like: *.md, *.qmd, *.txt, *.rst.
  - Prompt contains keywords: doc, documentation, spelling, grammar, headers, links, table alignment, Divio, tone, voice, clarity.
---

# Documentation

This skill governs how you write. Section 1 applies to **all text you produce** — code comments, chat responses, documentation. (Commit messages are governed by [commit-hygiene](../commit-hygiene/SKILL.md), which owns that jurisdiction in the §5 routing table.) Section 2 applies when you are **producing or editing a standalone document** (README, guide, reference page, explanation, specification).

---

## Section 1: Core Writing Principles

These rules are always active. They are non-negotiable.

### 1. Answer First

Lead with the conclusion, not the context. The reader's question should be answered in the first sentence or heading — background, caveats, and methodology come after. If someone stops reading after one paragraph, they should still have the answer.

### 2. Active Voice

Default to active voice. Use passive only when the actor is genuinely irrelevant or unknown. "The function returns an error" — not "An error is returned by the function."

### 3. Sentence Economy

One idea per sentence. Delete words that don't earn their place. If a sentence works without a word, remove that word. Prefer concrete language over abstract hedging.

### 4. Terminology Lock

Once you name a concept, use that name everywhere. Do not swap synonyms for variety — consistency beats prose elegance. If the codebase calls it a "store," never call it a "repository" or "database" in documentation. Terminological inconsistency is a documentation bug.

### 5. Scannable Structure

Readers scan before they read. Support this:

- Use meaningful headings (not "Overview" or "Introduction" — say what the section _contains_)
- Use bullet points for lists of 3+
- Bold key terms on first use
- Front-load important words in headings and list items

### 6. No Filler

Do not pad text with words that add no information.

> [!CAUTION]
> **Anti-Patterns (FORBIDDEN):**
>
> - ❌ Preamble walls: "In this section, we will discuss the various aspects of..."
> - ❌ Restating the question: "You asked about X. X is an important topic. Let me explain X."
> - ❌ Hedge-word padding: "It's worth noting that perhaps it might be considered..."
> - ❌ Empty transitions: "Now let's move on to the next topic."
> - ❌ Compliment-before-content: "Great question! That's a really interesting point."
> - ❌ Metatext about your own process: "I'll analyze this step by step."
>
> ✅ **Correct behavior:** Start with the substance. If a paragraph's first sentence could be deleted without losing information, delete it.

---

## Section 2: Documentation Production

> **Activation scope:** Apply this section when producing or editing a **standalone document** — any file whose primary purpose is to communicate information to a reader (README, guide, reference, spec, tutorial, explanation). Code comments are governed by Section 1. Commit messages defer to [commit-hygiene](../commit-hygiene/SKILL.md).

### 7. Document Classification (Divio Model)

Before drafting, identify which type of document you are writing. Each type has a distinct purpose, tone, and structure — mixing them produces documents that serve no audience well.

| Type            | Purpose              | Tone                 | Structure                      |
| :-------------- | :------------------- | :------------------- | :----------------------------- |
| **Tutorial**    | Learning by doing    | Guiding, encouraging | Step-by-step, linear, no forks |
| **How-To**      | Solve a problem      | Practical, direct    | Numbered steps to a result     |
| **Reference**   | Describe the machine | Austere, precise     | Tables, lists, type signatures |
| **Explanation** | Build understanding  | Discursive, honest   | Prose, diagrams, "why" chains  |

A document should be **one type**. If you need to explain _and_ provide reference, write two documents (or two clearly separated sections). A tutorial that drifts into reference material fails at both.

### 8. Audience Declaration

State who the reader is, either explicitly ("This guide is for developers integrating the X API") or implicitly through level of assumed knowledge. Do not write for everyone — writing for everyone serves no one. Key dimensions:

- **Domain familiarity** — do they know the problem space?
- **Tool familiarity** — have they used this software before?
- **Goal** — learning, reference-checking, or troubleshooting?

### 9. Self-Consistency

A document must not contradict itself. Before finalizing:

- Verify terminology is consistent throughout (see Terminology Lock, §4)
- Check that claims in the introduction match the body
- Confirm cross-references point to content that exists and says what you claim it says

### 10. Scope Economy

Write the minimum documentation that eliminates the maximum confusion. Every sentence must address the reader's **information need**, not the general topic. Ask: "If I remove this paragraph, does the reader lose something they need?" If not, remove it.

> [!IMPORTANT]
> Over-documentation is itself a maintenance burden. Stale, verbose docs are worse than concise, current ones. Prefer a short document you will maintain over a comprehensive one you won't.

### 11. Progressive Disclosure

Present the simple, common path first. Link to edge cases, advanced configuration, and error recovery rather than interleaving them with the main flow. The reader who needs exceptions will follow the link; the reader who doesn't will thank you for not burying them.

### 12. Documentation Debt

Documentation debt is a first-class concept, parallel to technical debt:

- **Missing docs** — a feature exists but has no documentation
- **Stale docs** — documentation describes a previous version of the code
- **Misleading docs** — documentation is factually wrong or implies incorrect usage
- **Orphaned docs** — documentation references concepts, files, or APIs that no longer exist

When you encounter documentation debt, flag it explicitly. Do not silently work around it.

### 13. Markdown Audit: Links, Headers, and Linting

When editing or auditing markdown files, enforce the following structural rules. They keep documents portable across host environments and consistent in formatting.

**Link integrity and portability** — all markdown file cross-references must resolve from any host environment or mounting context:
- **Use standard Markdown link format:** All links must follow `[text](url)`.
- **Use relative paths:** Link between files using relative markdown paths (e.g. `[constitution](../constitution/SKILL.md)`).
- **Forbid machine-specific absolute paths:** Never use absolute file URIs (e.g., `file:///var/home/...` or `file:///absolute/path/...`) in any documentation, comments, or plans. They are host-specific and fail to resolve when skills or projects are copied, symlinked, or cloned.
- **Verify:** Proactively audit link targets to confirm that the relative references resolve correctly from the directory of the file containing the link.

**Header hierarchy** — use a single `<h1>` (one `#`) per page, then nest header levels sequentially (`##`, `###`, ...) without skipping a level.

**Linting standards:**
- Align table columns.
- Use a consistent list symbol (`-`).
- Leave no trailing spaces.

To check link integrity automatically, run the script at [`doc-audit/scripts/check_docs.py`](../doc-audit/scripts/check_docs.py): it scans markdown files for broken local and external links.