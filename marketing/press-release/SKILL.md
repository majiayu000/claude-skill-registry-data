---
name: press-release
description: >
  Use this skill when the owner wants to write, draft, or generate a press release.
  Invoke when the user says "write a press release", "draft a press release",
  "create a press release", "generate a press release announcement", or similar
  requests for announcement-format content.
allowed-tools: Read, Write, Bash
argument-hint: "[optional: path to campaign briefing file]"
---

@./format-guidelines.md **Read when:** starting this skill
@../\_shared/storytelling-frameworks.md **Read when:** selecting a narrative framework in Step 5
@../\_shared/persuasion-principles.md **Read when:** selecting persuasion principles in Step 6

# Press Release Skill

You are helping the owner produce a complete, publishable press release. The
release must comply with the format guidelines in this skill folder, reflect
the company's brand voice, address the right audience for the right goal and
distribution channel, and — if a campaign briefing is present — serve the
briefing's goals.

This skill is **language-, industry-, and audience-neutral**. It works for any
output language and any combination of B2B / B2C, distribution channel, and
announcement focus. Calibration happens explicitly in Step 3 by inferring values
from the loaded context and confirming them with the owner.

## Step 0: Recall learnings

If `.claude/learnings.md` exists, read it silently. Apply all entries relevant
to this run — both `[cc-content:*]`-tagged entries and entries from other
plugins that inform content quality or project constraints. Do not announce
this step. If the file is absent, continue normally.

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
> (b) Continue without project context (output will be generic)"

Stop if (a); note "generating without project context" and continue if (b).

**If a context table exists**, read every file listed in the **File** column.

After loading, assess what each file covers by reading its **Summary** entry.
Map the loaded files to these content needs:

| Need                         | What to look for in the Summary                                          |
| ---------------------------- | ------------------------------------------------------------------------ |
| Brand voice                  | Writing style, tone, vocabulary, phrasing rules, things to avoid         |
| Organization background      | Who the company/author is, products, positioning, mission                |
| Target audience              | Reader personas, goals, challenges, job titles                           |
| Output language              | Default language, locale, or region                                      |
| Press-release-specific rules | Mandatory sections, distribution channels, legal/compliance requirements |

**When multiple files plausibly cover the same need**, pick the one whose Summary
best fits this specific task.

**Coverage gaps — flag these two:**

If no loaded file plausibly covers **brand voice**, ask once:

> "I don't see any writing style or brand voice context. Is this intentional, or should
> I pause while you run `/content-onboarding`?"
>
> - **Intentional**: note the gap; label the final output `⚠ DEGRADED OUTPUT — no brand voice context`
> - **Pause**: direct the owner to onboarding and stop.

Apply the same ask for **organization background** if no loaded file covers it.

For absent audience, language, or press-release-specific rules: note silently and continue.

After loading and assessing, note which files were loaded and which need each covers.
Proceed to Step 2.

## Step 2: Check for campaign briefing

Determine the briefing path:

1. If the owner passed a file path as an argument (`$ARGUMENTS`), use that path.
2. Otherwise, check for `brief.md` in the current working directory:

```bash
ls brief.md 2>/dev/null || echo "not found"
```

**If found**, read it. Confirm the briefing scope with the owner:

> "Found briefing: [BRIEFING TITLE]. Does this cover the announcement(s) you want
> to draft? Or should I use a different briefing?"

**If not found**, note "No campaign briefing found — generating from company context only."
and continue.

Proceed to Step 3.

## Step 3: Infer and confirm audience and goal

Use the loaded audience and organization context and campaign brief (if any) to infer:

1. **Audience type:** B2B or B2C (or mixed)
2. **Primary distribution goal:** direct-to-journalist pickup, SEO/backlink/brand-entity
   via wire placement, or owned record-of-announcement
3. **Audience expertise level:** novice, familiar, or expert in the topic domain

If the loaded context does not support a confident inference, ask the owner the
missing question directly rather than guessing.

Present a one-line inference summary, for example:

> "Audience: B2B (mid-market) · Distribution goal: direct-to-journalist pickup ·
> Expertise: familiar"

Ask the owner to confirm or correct before generating:

> "Does this match what you need? Confirm or correct before I proceed."

Do not silently apply assumptions.

Based on confirmed values, explicitly state which Layer 2 and Layer 3 variations
from `format-guidelines.md` are being applied and why.

Proceed to Step 4.

## Step 4: Ask for the announcement topic and key details (if not provided)

Ask:

> "What is the announcement? Provide as much or as little detail as you like —
> for example: 'We shipped a dark mode feature', 'We raised $5M Series A',
> 'We hired a new CTO', 'We launched a partnership with [Company]'. I'll ask
> follow-up questions if I need more."

Wait for the answer. Read the details and determine what additional information
is required for a complete release:

- **The news itself:** what changed, launched, or happened
- **Why it matters:** business impact, customer benefit, or market relevance
- **Timing:** when does this become public
- **Key stakeholders:** who is being quoted (ideally, multiple voices — company + customer or analyst)
- **Supporting numbers/proof:** metrics, customer count, revenue impact, etc. (if available)

Ask follow-up questions only for gaps that would materially affect the release
(e.g., missing quotes, unclear business impact). Do not ask for perfect polish
at this stage — brief notes are fine.

Proceed to Step 5.

## Step 5: Select storytelling framework

Press releases follow the **inverted pyramid** structure as their default framework —
most important information first, supporting details in descending importance.

However, if the announcement lends itself to a narrative angle (a customer problem
solved, a market trend, a company milestone), read `storytelling-frameworks.md`
and follow its selection process to see if a narrative overlay (BAB, PAS, StoryBrand,
JTBD) would strengthen the release.

Apply the chosen framework (or confirm inverted pyramid + narrative layer if applicable)
as the structural spine.

Proceed to Step 6.

## Step 6: Select persuasion principles

Read `persuasion-principles.md` and follow its selection process. For press releases,
the most effective principles are typically:

- **Specificity:** named metrics, percentages, dollar amounts, and concrete claims
  outperform generic language
- **Social proof / authority:** third-party quotes (customers, analysts, industry
  experts) carry more weight than internal quotes alone
- **Credibility via attribution:** full name + title on first mention establishes
  authority before the quote is read

Pick 1–3 principles plus a pre-suasive opener strategy (usually specificity in the
headline and lead). Note the choices in working notes.

Proceed to Step 7.

## Step 7: Generate the press release

Produce a complete press release that applies:

- The confirmed format-guidelines variant (B2B vs. B2C, distribution goal)
- The chosen framework (inverted pyramid ± narrative layer)
- The selected persuasion principles
- Any loaded brand-voice and audience context
- AP style conventions (numerals, dates, titles) per the format guidelines

**Internally verify against the quality checklist** in `format-guidelines.md`:

- [ ] Headline under 100 chars, title case, no end punctuation
- [ ] Dateline format correct (`CITY — Body text`)
- [ ] Lead paragraph covers 5 Ws in 50–75 words
- [ ] Total length 300–500 words (ideally ~400)
- [ ] AP style conventions applied throughout
- [ ] 1–2 quotes, each adding genuine insight
- [ ] Attribution format correct (full name + title first, last name after)
- [ ] Boilerplate 50–100 words, third person, covers who/what/where
- [ ] Media contact info present

For every unchecked box, revise the draft and re-check — do not present until
every gate passes or the failure genuinely cannot be fixed (e.g. missing
context), in which case surface it in the output rather than hiding it.

Present the output in a clearly delimited block showing the complete release and
its word count.

If output is degraded (a required context need is uncovered), prepend:

> `⚠ DEGRADED OUTPUT — generated without: <list of missing needs>`

Proceed to Step 8.

## Step 8: Feedback

This step has two phases:

_Auto-store phase._ Before asking the user for feedback, review the run for qualifying
observations. For each, append one tagged line to `.claude/learnings.md` (create with
standard header if missing), tagged `[cc-content:press-release]`. Qualifies:
content preferences or constraints not already in any loaded context file or `CLAUDE.md`;
corrections the user made; project-specific facts that would change future output;
accepted/rejected suggestions deviating from best practices. Does not qualify: standard
behavior applied without deviation; facts already in context files or `CLAUDE.md`;
anything derivable by re-reading context files; facts semantically equivalent to any
existing `.claude/learnings.md` entry under any plugin tag — when in doubt, skip;
redundancy is worse than a missed entry.

_Explicit feedback._ Ask whether the output met expectations:

> "Does this press release work for your needs? If you'd like changes, tell me what
> to adjust, and I'll revise."

If the user provides a correction, apply it and re-present the release. Then ask:

> "Better? Anything else?"

Repeat until the user confirms quality or explicitly says "ship it" / "that's ready"
/ "this looks good."

When the user confirms quality or skips feedback: if any entries were auto-stored,
confirm:

> "✓ N learning(s) auto-saved to `.claude/learnings.md`."

Then deliver a closing line:

> "✓ Press release ready. You can paste this into your newsroom, send it to journalists,
> or submit it to a wire service. See `format-guidelines.md` for distribution guidance."

Exit.
