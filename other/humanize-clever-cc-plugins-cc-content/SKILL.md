---
name: humanize
description: >
  Use this skill to remove AI "tells" from an existing draft and make it read as
  human-written, calibrated to the project's brand voice. Invoke when the user says
  "humanize this", "make this sound less AI", "remove AI tells from this", "this
  reads like ChatGPT wrote it", "polish this draft to sound human", or pastes a
  draft and asks for a more authentic-sounding version. Works on drafts from any
  source — the owner's own writing, another tool's output, or a previous cc-content
  skill's draft. Do NOT use it to generate new content from scratch; it only revises
  an existing draft.
allowed-tools: Read, Write, Bash
argument-hint: "[optional: path to the draft to humanize]"
---

# Humanize Skill

You are helping the owner remove AI "tells" from an existing draft and produce a
version that reads as genuinely human-written, calibrated to the company's brand
voice. This skill takes **any** draft regardless of origin — it is not limited to
drafts produced by other `cc-content` skills.

This skill is **format-, language-, industry-, and audience-neutral**. It carries the
detection and rewrite craft below but calibrates every stylistic choice to the loaded
brand voice — a formal-voice project and a casual-voice project get different
rewrites of the same input.

## Step 0: Recall learnings

If `.claude/learnings.md` exists, read it silently. Apply all entries relevant to
this run — both `[cc-content:*]`-tagged entries and entries from other plugins that
inform content quality or project constraints. Do not announce this step. If the
file is absent, continue normally.

## Step 1: Load context

Read the context table from all loaded CLAUDE.md files:

```bash
grep -A 200 '## Context files' CLAUDE.md 2>/dev/null || echo "(no context table)"
```

CLAUDE.md files may exist at multiple hierarchy levels (workspace root, project root,
sub-directory). The harness already loads all applicable ones into your context window.
If multiple `## Context files` tables exist, rows from more specific CLAUDE.md files
take precedence over less specific ones.

**If no context table is found** in any loaded CLAUDE.md, ask once:

> "I don't see any context files registered. Would you like to:
> (a) Pause and run `/content-onboarding` to set up context
> (b) Continue without project context (humanization will use generic style choices)"

Stop if (a); note "generating without project context" and continue if (b).

**If a context table exists**, read every file listed in the **File** column, and
identify which one covers **brand voice** (writing style, tone, vocabulary, phrasing
rules, things to avoid) by matching against each file's **Summary** entry — this is
the **only** need this skill gates on. Organization background, audience, and output
language are noted silently if present and **never block** — humanization revises
style, not substance, so it doesn't need them to do its job.

**Coverage gap — brand voice:**

If no loaded file plausibly covers brand voice, ask once:

> "I don't see any writing style or brand voice context. Is this intentional, or
> should I pause while you run `/content-onboarding`?"
>
> - **Intentional**: note the gap; label the output `⚠ DEGRADED OUTPUT — no brand voice context` and fall back to generic human-writing conventions (varied rhythm, contractions, concrete detail) without a specific tone target.
> - **Pause**: direct the owner to onboarding and stop.

## Step 2: Get the draft

Resolve the draft to humanize, in this order:

1. If the owner passed a file path as an argument (`$ARGUMENTS`), read it.
2. If the owner pasted text in the request, use that.
3. If neither, ask: _"Paste the draft you want humanized, or give me a file path."_

## Step 3: Detect AI markers (Pass 1)

Scan the draft for these markers and count each type:

- **Em-dash parentheticals** — insertions set off by "–" or "—".
- **Overused transitions** — "Moreover," "Furthermore," "In today's world," and
  similar formulaic connectors.
- **Formulaic structure** — a rigid intro–3 points–conclusion shape with no
  variation.
- **Generic AI phrases** — "dive into," "unlock," "elevate," "transform," unless the
  loaded brand voice explicitly uses these terms as part of its established
  vocabulary.
- **Excessive colons/semicolons** — used as a crutch for list-like sentences instead
  of natural prose.
- **Too-perfect parallel structure** — this marker has two cases; scan for both:
  - _Within-passage:_ every sentence in a single passage sharing the exact same
    grammatical shape.
  - _Cross-section template repetition:_ the same sentence-opening template — same
    opening words, same clause shape, but not necessarily identical wording after
    that (e.g. "delivers"/"scales"/"provides" filling the same slot still counts)
    — reused across multiple otherwise-unrelated parallel sections (sibling
    subsections, comparison blocks, FAQ answers). This case is invisible when scanning any one paragraph in isolation —
    it only surfaces by comparing sentence openers across the whole document. After
    the within-passage scan, run a second, document-wide pass in two stages:
    1. **Candidate grouping:** group sentences by their opening span — the first
       2–3 words for whitespace-delimited languages, or the comparable
       clause-initial unit (e.g. the first few characters or morphemes) for
       languages without whitespace word boundaries such as Chinese, Japanese, or
       Thai. This is a structural check, not a vocabulary list — it applies the
       same way regardless of language.
    2. **Confirmation:** within each candidate group, compare clause shape (same
       grammatical construction following the opener, not just the same opening
       words) and discard groups that only share a prefix by coincidence (e.g.
       "The report describes…" next to "The report is…"). A confirmed group needs
       2 or more sentences sharing the same clause shape — a single matching
       sentence is not repetition. Count a confirmed group under this marker only
       when those 2+ sentences also sit in _separate_ structurally parallel
       sections — sibling subsections, rows, or list items that are themselves
       distinct passages, each playing the same repeated structural role. Heading
       level is one signal for this but not a requirement: unheaded rows or list
       items count too if they share the role, as long as they're separate
       passages. Repeated list items or table rows sitting inside one single
       passage are within-passage, not cross-section, regardless of this wording.
       Favor _distinctive_
       templates: a short, generic opener with an equally generic continuation
       (e.g. "This means…" followed by an unremarkable clause) can recur by
       coincidence in genuine human writing and isn't on its own a strong signal —
       only count it when the full template (opener plus clause shape together) is
       specific enough that independent drafting would be unlikely to reproduce it
       verbatim. Each confirmed group counts as one cross-section hit, regardless of
       how many sentences or sections it spans — that detail belongs in the Step 5
       example, not in the count itself. A sentence already counted toward a
       within-passage hit doesn't also count toward a cross-section group, so the
       two counts never overlap.

    This cross-section pass matters most on documents with multiple sibling
    sections (subsections, comparison blocks, FAQ entries): a low per-passage
    marker count can still hide a document that reads as "too polished" once
    repeated section templates are counted.

- **Hedge words** — "arguably," "potentially," "seemingly," used to soften claims
  without adding information.

Present the counts and one brief example per marker type found, **before**
rewriting — the owner should see the diagnosis first, in the single-line-per-marker
format Step 5 defines. For too-perfect parallel structure: if the cross-section
count is zero, report a plain `<count>`, same as every other marker. Otherwise
keep the two cases visible instead of collapsing them into one number — report
`<count>` as `<total> (N within-passage, M cross-section)` — and use the
`<brief example>` slot for the cross-section case: the repeated opener plus the
sections it recurs in, e.g. "'A good solution' opens the closing sentence of 3
subsections: §2.1, §2.2, §2.3" (avoid an em dash inside the example itself — it
collides with Step 5's own `<count> — <brief example>` separator). That still
fits on Step 5's one line.

## Step 4: Rewrite (Pass 2)

Produce the rewritten draft. Rules:

1. **Preserve every factual claim and the original structure's intent.** This is a
   style pass, not a content rewrite — do not add, remove, or change what the draft
   asserts.
2. **Remove every marker counted in Step 3.** None should remain in the output.
3. **Calibrate reintroduced human texture to the loaded brand voice:**
   - If the brand voice allows casualness: use contractions, allow sentences to
     start with "And" or "But" where it reads naturally, vary sentence rhythm (mix
     short punchy sentences with longer natural ones), replace vague time references
     with concrete ones ("last Tuesday" instead of "recently"), and use specific
     detail in place of generic examples.
   - If the brand voice is formal: keep contractions and casual openers out, but
     still vary sentence rhythm, replace vague generalities with specific detail, and
     remove the same AI markers — formality and human-sounding prose are not
     opposites.
   - If no brand voice is loaded (degraded per Step 1): default to varied rhythm,
     concrete detail, and marker removal only — do not guess a tone.
4. **Intervene as much as necessary but as little as possible.** Preserve what
   already works in the draft; change only what a marker-removal or tone-calibration
   rule requires.

## Step 5: Delimited output

```
─────────────────────────────────────────────
AI markers detected
─────────────────────────────────────────────
<marker type>: <count> — <brief example from the draft>
[one line per marker type found; omit types with zero occurrences]
─────────────────────────────────────────────
Humanized draft
─────────────────────────────────────────────
<the rewritten text only — no preamble, no commentary inside the block>
─────────────────────────────────────────────
```

If the output is degraded (no brand voice context), prepend:

```
⚠ DEGRADED OUTPUT — generated without brand voice context; used generic
human-writing conventions only
```

## Step 6: Feedback

**Auto-store phase.** Before asking for feedback, review this run. For each
qualifying observation, append one tagged line to `.claude/learnings.md` (create with
the standard header if missing):

```text
[cc-content:humanize] <concise observation> — <YYYY-MM-DD>
```

Qualifies: humanization preferences not already in any loaded context file or
`CLAUDE.md` (e.g. "owner always wants contractions even in the formal-voice
project"); corrections the owner made to the rewritten draft; project-specific
facts that would change future humanization passes.

Does not qualify: standard behavior applied without deviation; facts already in
context files or `CLAUDE.md`; anything derivable by re-reading context files; facts
semantically equivalent to an existing `.claude/learnings.md` entry under any plugin
tag — when in doubt, skip; redundancy is worse than a missed entry.

Check for the file before appending:

```bash
ls .claude/learnings.md 2>/dev/null && echo "exists" || echo "missing"
```

Standard header when creating the file:

```markdown
# Learnings

Corrections and feedback collected during content sessions.
Entries are tagged by skill and dated.

---
```

**Explicit feedback.** After the auto-store phase, ask:

> "Did this humanized version work for you? Any corrections or notes for future
> passes — or press Enter to finish."

- If the owner **provides a correction**: append it as a tagged entry using the same
  format and qualification criteria above. Confirm: "✓ N learning(s) saved to
  `.claude/learnings.md`."
- If the owner **confirms or skips**: if any entries were auto-stored, confirm
  "✓ N learning(s) auto-saved to `.claude/learnings.md`." Then exit. If nothing was
  stored, exit directly.
