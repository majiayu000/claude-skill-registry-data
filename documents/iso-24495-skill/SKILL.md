---
name: iso-24495
description: "Use when text must be easy for its intended reader to find, understand, and act on — reports, emails, documentation, UI text, announcements, explanations, AI output that reads as dense or bureaucratic. Applies ISO 24495-1 plain language principles with dedicated technique layers for English and Traditional Chinese. Triggers: plain language rewrite, apply ISO 24495, make this clearer for readers, de-jargon this, 淺白改寫, 白話改寫, 去公文腔, 讓讀者一次看懂. Not for creative or literary writing."
version: 0.1.0
---

# ISO 24495-1 Plain Language (English + Traditional Chinese)

ISO 24495-1:2023 is the international standard for plain language. It defines
plain language by reader outcome, not by word lists: a document is plain when
its intended readers can get what they need (relevant), find it (findable),
understand it on first reading (understandable), and act on it (usable).

This skill rewrites text so it meets those four outcomes. The principles are
language-independent — ISO states the standard "applies to most, if not all,
written languages" — so this skill ships one shared principle layer and two
language technique layers:

- **English** → apply `references/english-techniques.md`
- **Traditional Chinese（繁體中文）** → apply `references/chinese-techniques.md`

The Chinese layer is not a translation of the English layer. It is a separate
technique set for problems Chinese text actually has (歐化長句、公文腔、
成語堆疊、中英夾雜、被字句濫用). As of this skill's release, no national
standards body has published a Chinese adaptation of ISO 24495-1; this layer
is an original implementation of the principles for Chinese.

## When to Use This Skill

- A reader-facing text (report, email, doc page, UI string, announcement,
  policy, explanation) reads as dense, bureaucratic, hedged, or jargon-heavy.
- AI-generated output is technically correct but hard to read.
- Text must work for non-specialist readers, non-native readers, or busy
  readers who will scan rather than study.
- You want a before/after with the violated principle named per change —
  ask for it; the default output is the rewritten text alone.

Not for creative or literary writing, and not for agent-facing controlled
language — for text a machine must parse without ambiguity, use a controlled
language standard such as ASD-STE100 instead (see Scope Boundary below).

## Procedure

1. **Identify the reader and purpose** (Principle 1 requires it). If the user
   named an audience, use it. Otherwise assume a busy, intelligent,
   non-specialist adult reader and state that assumption in one line only
   when it changes the rewrite materially.
2. **Detect the text language.** English → English techniques file. Chinese →
   Chinese techniques file. Mixed text → the dominant language's file, and
   handle embedded foreign terms per that file's rules. Other languages →
   apply the four principles directly and say the technique layer for that
   language does not exist yet.
3. **Read the whole text for meaning before touching a sentence.**
4. **Rewrite against the four principles**, using the language file's
   techniques. Never drop a fact, condition, number, or scope qualifier.
   If plainness would cost precision, keep the precision and flag the
   trade-off in one line.
5. **Run the language file's self-check list** before returning.

## Output Format

Return the rewritten text alone — no preamble, no principle lecture, no
change summary. Append a one-line `Kept as-is:` note only when something was
deliberately left unsimplified for precision.

When the user asks to "show the diff", "explain the changes", or "which
principles", return a before/after table instead, one row per change, naming
the principle (relevant / findable / understandable / usable) and the
technique applied.

## The Four Principles (working definitions)

| Principle | The reader outcome it protects |
|---|---|
| Relevant | The text contains what this reader needs for this purpose — and nothing else. Cutting is a rewrite tool, not just rearranging. |
| Findable | The reader can locate the part they need without reading everything: informative headings, front-loaded key points, lists for parallel items, one topic per paragraph. |
| Understandable | The reader gets it on first reading: common words, short sentences, active constructions, defined terms, no unexplained jargon. |
| Usable | The reader can act: concrete instructions, explicit actors and deadlines, next steps stated as steps. |

Full interpretation, sources, and copyright boundaries:
`references/principles.md`.

## Scope Boundary: Plain Language vs Controlled Language

ISO 24495-1 optimizes text for **human readers** and permits full natural
language. Controlled-language standards such as ASD-STE100 optimize for
**zero-ambiguity parsing** (originally by maintenance technicians, now also
by AI agents) and restrict vocabulary and grammar hard. If the reader is a
machine or the cost of one misread word is high, use a controlled-language
skill. If the reader is a person who needs to find, understand, and act,
use this one.

## Copyright Note

This is an unofficial project, not affiliated with or endorsed by ISO. The
full ISO 24495-1 text is a licensed document and is not reproduced here. This
skill is built from the standard's publicly documented principles and public
plain-language practice; every quantitative rule in the technique files is
this project's own working proxy, not a clause of the standard. For certified
conformance work, buy and consult the standard itself.
