---
name: gated-long-form-content
description: >
  Use this skill when the owner wants to write, draft, or generate gated long-form
  lead-generation content such as a whitepaper, guide, ebook, or research report.
  Invoke when the user says "write a whitepaper", "draft a lead-gen guide", "create an
  ebook", "draft a gated whitepaper", "generate a research report for lead gen".
allowed-tools: Read, Write, Bash
argument-hint: "[optional: path to campaign briefing file]"
---

@./format-guidelines.md **Read when:** starting this skill
@../\_shared/storytelling-frameworks.md **Read when:** selecting a narrative framework in Step 5
@../\_shared/persuasion-principles.md **Read when:** selecting persuasion principles in Step 6

# Gated Long-Form Content Skill

You are helping the owner produce a complete, publishable gated long-form asset
(whitepaper, guide, ebook, or research report). The asset must comply with the
format guidelines in this skill folder, reflect the company's brand voice, serve the
confirmed audience/goal/funnel combination, and — if a campaign briefing is present —
serve the briefing's goals.

This skill is **language-, industry-, and audience-neutral**. It works for any output
language and any B2B or B2C context. Calibration happens through the loaded context
files, the confirmed inferences in Step 3, and the owner's topic input.

## Step 0: Recall learnings

If `.claude/learnings.md` exists, read it silently. Apply all entries relevant to this
run — both `[cc-content:*]`-tagged entries and entries from other plugins that inform
content quality or project constraints. Do not announce this step. If the file is
absent, continue normally.

## Step 1: Load context

Check for a `## Context files` table in CLAUDE.md via:

```bash
grep -A 200 '## Context files' CLAUDE.md 2>/dev/null || echo "(no context table)"
```

CLAUDE.md files may exist at multiple hierarchy levels (workspace root, project root,
sub-directory) and the harness loads all applicable ones. Where multiple tables exist,
rows from more specific CLAUDE.md files take precedence.

**Do not enumerate required categories by name.** Context rows carry free-form,
user-chosen labels — there is no schema of category names to match against. Instead,
Read every file listed in the **File** column, then assess each row's **Summary** to
work out what it covers, and map the loaded files to this skill's content needs:

| Need                    | What to look for in the Summary                                  |
| ----------------------- | ---------------------------------------------------------------- |
| Brand voice             | Writing style, tone, vocabulary, phrasing rules, things to avoid |
| Organization background | Who the company/author is, products, positioning, mission        |
| Target audience         | Reader personas, goals, challenges, job titles                   |
| Output language         | Default language, locale, or region                              |
| Format-specific rules   | Rules governing whitepapers, guides, or ebooks specifically      |

Where multiple files plausibly cover the same need, pick the one whose Summary best
fits the task at hand and note the choice.

Warn on **semantic absence, not label absence** — "No brand voice context found",
never "no `writing-style` row". Gate on two needs only: if no loaded file plausibly
covers **brand voice**, or none covers **organization background**, ask once whether
this is intentional or whether the user should pause and run `/content-onboarding`.
Same pause / DEGRADED OUTPUT pattern as all output-format skills. For absent audience,
language, or format-specific rules: note silently and continue — never ask.

See `../_shared/context-categories.md` for the full guide to common context patterns
and the authoring rules this step follows.

## Step 2: Check for campaign briefing

Determine the briefing path:

1. If the owner passed a file path as an argument (`$ARGUMENTS`), use that path.
2. Otherwise, check for `brief.md` in the current working directory:

```bash
ls brief.md 2>/dev/null && echo "found" || echo "missing"
```

- **Found** (either via argument or `brief.md`): read the file and note its key
  messages, goals, and constraints. Confirm: "✓ Campaign briefing loaded from
  `<path>`."
- **Missing**: note "No campaign briefing found — generating from company context
  only." and continue.

## Step 3: Infer and confirm audience and goal

This is the most consequential step for this skill, since `format-guidelines.md`
varies substantially by audience, goal, funnel stage, and expertise level.

1. Use the loaded audience context and campaign brief (if any) to infer: B2B or
   B2C, content goal (thought leadership / awareness / lead generation / nurturing /
   conversion / retention), funnel stage (TOFU / MOFU / BOFU), and audience
   expertise level (novice / familiar / expert). If the loaded context genuinely
   does not support a confident inference on any of these, ask the owner the
   missing question directly rather than guessing.
2. Present a one-line inference summary to the user, for example:
   "Audience: B2B (enterprise) · Goal: lead generation · Stage: MOFU · Expertise:
   familiar"
3. Ask the user to confirm or correct before generating. Do not silently apply
   assumptions.
4. Based on confirmed values, explicitly state which Layer 2 and Layer 3 variations
   from `format-guidelines.md` are being applied and why — e.g., "Applying the B2B
   committee-structure guidance (executive summary + technical appendix) and the
   MOFU proof-type guidance (original research, comparative data)."

## Step 4: Ask for the content topic (if not provided)

Ask: "What should this whitepaper/guide/ebook be about?" and wait.

## Step 5: Select storytelling framework

Read `../_shared/storytelling-frameworks.md` and follow its selection process. Apply
the chosen framework as the structural spine — typically a problem → insight →
solution arc for this format, per `format-guidelines.md`.

## Step 6: Select persuasion principles

Read `../_shared/persuasion-principles.md` and follow its selection process. Pick 1–3
principles plus a pre-suasive opener strategy, favoring the mechanisms called out as
strongest for this format in `format-guidelines.md` (central-route argument quality,
narrative transportation via case studies, source credibility, reciprocity). Note the
choices in working notes.

## Step 7: Generate the asset

Produce a complete whitepaper/guide/ebook that:

- Follows the required structure from `format-guidelines.md` Layer 1 (executive
  summary, problem definition, body/evidence, recommendations, conclusion, CTA)
- Applies the confirmed B2B/B2C variant from Layer 2, including the confirmed
  sub-variation (e.g., SMB vs. enterprise) where relevant
- Applies the confirmed content-goal and funnel-stage variant from Layer 3
- Pairs major claims with both data and an illustrative case where the input
  material supports it
- Uses the storytelling framework and persuasion principles selected in Steps 5–6
- Reflects tone and vocabulary from loaded brand-voice context
- Matches length to the format label and audience per the Layer 1 length table —
  no padding to hit a word count
- States an explicit, justified gating recommendation per the "Gating Decision"
  section of `format-guidelines.md`, including a recommended form-field count

Include a `[TODO: ...]` placeholder for any format-specific mandatory elements — for
example, a required word count, mandatory legal/compliance sections, or a specific
design template — that the user must specify for their use case.

Internally verify against the quality checklist in `format-guidelines.md`. For
every unchecked gate, revise the draft and re-check — do not present until
every gate passes or the failure genuinely cannot be fixed (e.g. missing
context), in which case surface it in the output rather than hiding it.

Present the output in a clearly delimited block showing the content and its word
count:

```
─────────────────────────────────────────────
<FORMAT LABEL> draft
─────────────────────────────────────────────
<content>
─────────────────────────────────────────────
Word count: <N>
```

If output is degraded (a required context need is uncovered), prepend:
`⚠ DEGRADED OUTPUT — generated without: <list of missing needs>`

## Step 8: Feedback

This step has two phases:

**Auto-store phase.** Before asking the user for feedback, review the run for
qualifying observations. For each, append one tagged line to `.claude/learnings.md`
(create with standard header if missing), tagged `[cc-content:gated-long-form-content]`.
Qualifies: content preferences or constraints not already in any loaded context file
or `CLAUDE.md`; corrections the user made; project-specific facts that would change
future output; accepted/rejected suggestions deviating from best practices. Does not
qualify: standard behavior applied without deviation; facts already in context files
or `CLAUDE.md`; anything derivable by re-reading context files; facts semantically
equivalent to any existing `.claude/learnings.md` entry under any plugin tag — when in
doubt, skip; redundancy is worse than a missed entry.

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

**Explicit feedback.** Ask whether the output met expectations. If the user provides
a correction, append it as a tagged entry using the same criteria. Confirm total
entries written across both phases: "✓ N learning(s) saved to `.claude/learnings.md`."
If the user confirms quality or skips: if any entries were auto-stored, confirm
"✓ N learning(s) auto-saved to `.claude/learnings.md`." Then deliver a closing line:
"✓ Draft ready. Move it into your design template for layout, then route it through
legal/compliance review (if applicable) before publishing behind the gate." and exit.
