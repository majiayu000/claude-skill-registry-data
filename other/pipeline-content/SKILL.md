---
name: pipeline-content
version: 1.0.0
description: "Content creation pipeline — research, strategy, create, critique, humanize, knowledge capture. Chains auto-researcher, content-strategy, content-creator/copywriting/tech-writer, content-critique, humanizer, graphify, and obsidian-vault into a quality-gated content workflow."
---

# Pipeline: Content Creation

You are orchestrating a content creation pipeline. Every piece of content goes through research, creation, critique, and humanization before delivery.

## Input Parameters

Collect these before starting (use AskUserQuestion for any missing):

- **topic**: What the content is about
- **type**: `blog` | `social` | `email` | `docs` | `landing` | `ad` | `video-script`
- **platform** (for social): `tiktok` | `instagram` | `facebook` | `linkedin` | `youtube` | `x` | `threads`
- **audience**: Who is this for?
- **brand/slug** (optional): Brand identity to use
- **language** (optional): `en` | `vi` (default: `en`)

## Pipeline State

Create a tracker at `.gstack/pipeline-content-{date}.md`.

```markdown
## Pipeline: Content Creation
Started: {timestamp}
Topic: {topic}
Type: {type}
Platform: {platform}

| # | Stage | Status | Gate | Notes |
|---|-------|--------|------|-------|
| 1 | RESEARCH | pending | — | — |
| 2 | STRATEGY | pending | — | — |
| 3 | CREATE | pending | — | — |
| 4 | CRITIQUE | pending | — | — |
| 5 | HUMANIZE | pending | — | — |
| 6 | KNOWLEDGE | pending | — | — |
```

---

## Stage 1: RESEARCH

Invoke `/auto-researcher` with the topic.

The researcher will search, synthesize, and produce a structured report with:
- Key findings with confidence levels
- Supporting evidence with source quality tiers
- Conflicting views
- Limitations

Save the research output — it feeds into Stages 2 and 3.

**Gate:** Research report must have at least 3 data points with High or Medium confidence. If all sources are Low confidence, warn the user and ask whether to proceed.

**On pass:** Update tracker → PASS, proceed.

---

## Stage 2: STRATEGY (conditional)

**Skip if:** type is `social`, `ad`, or `email` AND user didn't request a campaign.

**Run if:** type is `blog`, `landing`, `docs`, or user explicitly requests strategy.

Invoke `/content-strategy` with:
- The research findings from Stage 1
- The target audience
- The content type and platform

Output: content brief with angle, outline, keyword targets, CTA, and distribution plan.

**Gate:** User reviews and approves the brief. If skipped, the research report serves as the brief.

---

## Stage 3: CREATE

Select the creation skill based on content type:

| Type | Skill | Why |
|---|---|---|
| `social`, `ad`, `email`, `landing` | `/content-creator` | Conversion-focused with formulas, psychology effects, platform constraints |
| `blog`, `video-script` | `/copywriting` | Long-form persuasive writing with AIDA/PAS frameworks |
| `docs` | `/tech-writer` | Developer documentation with Diataxis framework |

Pass to the selected skill:
- The research findings from Stage 1
- The content brief from Stage 2 (if available)
- All input parameters (audience, platform, language, brand)

**Gate:** Draft content produced. Present to user for initial review before critique.

---

## Stage 3.5: COMPLIANCE (fintech only)

**Trigger condition:** Run this stage ONLY when ANY of these are true:
- `preset=banking-finance` or `preset=crypto` is active
- Content type involves financial products or services
- Product type is `neobank`, `payments`, `lending`, `insurance`, `wealthtech`, or `crypto`
- Target audience is in a regulated financial jurisdiction

**Skip if:** Content is general business/tech content with no financial product claims.

Invoke `/fintech-compliance-gate` with:
- The draft content from Stage 3
- Product type (infer from preset or ask user)
- Target jurisdiction(s)
- Distribution platform

The compliance gate runs a 20-item checklist and produces RED/AMBER/GREEN findings.

**Gate logic:**
- **All RED items resolved** → must return to Stage 3 CREATE with compliance requirements attached
- **AMBER items** → add required disclosures to the draft, then proceed
- **All GREEN** → proceed to Stage 4

Update tracker:

```markdown
| 3.5 | COMPLIANCE | fintech-compliance-gate | {PASS/FAIL/PASS_WITH_DISCLOSURES} | {RED count}/{AMBER count}/{GREEN count} | {notes} |
```

---

## Stage 4: CRITIQUE

Invoke `/content-critique` on the draft.

The critique skill:
- Grades A-F across 6 dimensions (Clarity, Accuracy, Tone, Structure, SEO/Value, Consistency)
- Runs `/stop-slop` internally for AI pattern detection
- Produces severity-tiered findings with exact locations

**Gate:** Grade **B or above** → proceed to Stage 5.

If grade C or below:
1. Report the critique findings to the user
2. Apply the Top 3 fixes recommended by the critique
3. Re-run the creation skill with the fixes applied
4. Re-run critique on the revised draft
5. If still C after 2 revision cycles → present to user with the critique report and ask whether to proceed

---

## Stage 5: POLISH

Invoke `/content-polish` on the critique-approved draft.

The content-polish skill orchestrates three passes in sequence (language-branched: English → humanizer/proofreader, Vietnamese → humanizer-vi/grammar-checker-vi with optional translationese-cleaner-vi pre-pass):
1. **Humanizer** (format-calibrated) — removes AI patterns, calibrated to the document type
2. **Anti-fragmentation pass** — catches over-fragmentation, restores connective tissue, preserves parallelism
3. **Proofreader / grammar check** (post-humanizer mode) — catches typos, grammar, lost specifics, broken flow

This stage is MANDATORY per CLAUDE.md rules. Never skip.

**Gate:** Content-polish delivers a final "Version C" that passes:
- Humanizer's two-pass self-audit (30 AI-pattern categories)
- Anti-fragmentation check (no 3-short-sentences-in-a-row)
- Proofreader's format-calibrated review (spelling, grammar, clarity, flow)

---

## Stage 6: KNOWLEDGE (parallel, fire-and-forget)

Run these as background tasks after delivering the final content to the user:

### 6a: Knowledge graph
Invoke `/graphify` with the final content to capture entities, relationships, and topics in the knowledge graph.

### 6b: Obsidian vault
Invoke `/obsidian-vault` to persist the content metadata:
- Topic, type, platform, audience
- Research sources used
- Critique grade achieved
- Final content location

These are fire-and-forget — don't block the pipeline report on them.

---

## Final Report

```markdown
## Pipeline Report: Content Creation
Topic: {topic}
Type: {type} | Platform: {platform}
Audience: {audience}
Run: {timestamp}

| # | Stage | Skill | Result | Gate | Notes |
|---|-------|-------|--------|------|-------|
| 1 | RESEARCH | auto-researcher | {result} | {N} data points | {sources used} |
| 2 | STRATEGY | content-strategy | {result/SKIPPED} | {brief approved} | — |
| 3 | CREATE | {skill used} | {result} | Draft produced | {angle/formula used} |
| 4 | CRITIQUE | content-critique | {result} | Grade: {letter} | {revision cycles} |
| 5 | HUMANIZE | humanizer | {result} | Self-audit: PASS | — |
| 6 | KNOWLEDGE | graphify, obsidian | {result} | — | background |

Overall: {PASS / PASS_WITH_REVISIONS}
Final content: {delivered inline or file path}
```

## Vietnamese Content Pipeline

When target is Vietnamese (`language=vi`), load matching files from `skills/vietnamese-language/` at each stage: STRATEGY loads `seo-content-marketing.md` or `viral-content.md`; CREATE loads the relevant platform file and `gen-z-slang.md` if targeting under-25; CRITIQUE checks register consistency and AI-tells; HUMANIZE applies Vietnamese AI-tell patterns.
