---
name: landing-page
description: >
  Use this skill when the owner wants to write, draft, or generate a landing page.
  Invoke when the user says "write a landing page", "draft a registration page",
  "create a webinar landing page".
allowed-tools: Read, Write, Bash
argument-hint: "[optional: path to campaign briefing file]"
---

@./format-guidelines.md **Read when:** starting this skill
@../\_shared/storytelling-frameworks.md **Read when:** selecting a narrative framework
@../\_shared/persuasion-principles.md **Read when:** selecting persuasion principles

# Landing Page Skill

You are helping the owner produce a complete, publishable landing page. The page
must comply with the format guidelines in this skill folder, reflect the company's
brand voice, and — if a campaign briefing is present — serve the briefing's goals.

This skill is **language-, industry-, and audience-neutral**. It works for any
output language and any B2B or B2C context. Calibration happens through the
loaded context files, the campaign briefing, and the owner's topic input.

`format-guidelines.md` covers the full page-length spectrum — from short single-CTA
inbound registration pages (gated content / webinar sign-up) to longer direct-sales
pages — and gives extra depth to the short-form case. This skill does not assume
which one a given project needs; Step 3 infers the funnel stage (and therefore page
length, form friction, and CTA directness) from loaded context and the campaign
brief, and asks the owner directly whenever that inference isn't confident.

## Step 0: Recall learnings

If `.claude/learnings.md` exists, read it silently. Apply all entries relevant to
this run — both `[cc-content:landing-page]`-tagged entries and entries from other
plugins that inform content quality or project constraints. Do not announce this
step. If the file is absent, continue normally.

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
work out what it covers, and map the loaded files to the skill's content needs:

| Need                    | What to look for in the Summary                                                                                         |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Brand voice             | Writing style, tone, vocabulary, phrasing rules, things to avoid                                                        |
| Organization background | Who the company/author is, products, positioning, mission                                                               |
| Target audience         | Reader personas, goals, challenges, job titles                                                                          |
| Output language         | Default language, locale, or region                                                                                     |
| Format-specific rules   | Rules governing landing pages specifically (e.g. legal disclaimers, domain/hosting constraints, approved form-provider) |

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

## Step 3: Infer and confirm audience, goal, and funnel stage

1. Use the loaded audience context and campaign brief (if any) to infer: B2B or
   B2C, content goal (see the goal table in `format-guidelines.md` — most landing
   pages are lead generation or conversion), funnel stage (TOFU/MOFU/BOFU — gated
   content, webinar registration, or direct sale), and audience expertise level. If
   the loaded context genuinely does not support a confident inference, ask the
   owner the missing question directly rather than guessing.
2. Present a one-line inference summary to the user, for example:
   "Audience: B2B (mid-market) · Goal: lead generation · Stage: TOFU (gated content) ·
   Expertise: familiar"
3. Ask the user to confirm or correct before generating. Do not silently apply
   assumptions.
4. Based on confirmed values, explicitly state which Layer 2 (B2B/B2C, persuasion
   principles) and Layer 3 (goal, funnel stage, audience expertise) variations from
   `format-guidelines.md` are being applied and why — including page length target,
   form field count, and CTA directness for the confirmed funnel stage.

## Step 4: Ask for the content topic (if not provided)

Ask: "What should this landing page be about? What's the offer — a gated asset, a
webinar, a demo, or a direct purchase?" and wait.

## Step 5: Select storytelling framework

Read `../_shared/storytelling-frameworks.md` and follow its selection process. Apply
the chosen framework as the structural spine — for short registration pages this
mainly shapes the hero/value section; for longer direct-sales pages it shapes the
full page arc.

## Step 6: Select persuasion principles

Read `../_shared/persuasion-principles.md` and follow its selection process. Pick
1–3 principles plus a pre-suasive opener strategy, informed by the B2B/B2C guidance
in the "Persuasion principles" table of `format-guidelines.md`. Note the choices in
working notes.

## Step 7: Generate the landing page

Produce a complete landing page that applies the confirmed format-guidelines
variant (funnel stage, B2B/B2C, audience expertise), the chosen storytelling
framework, the selected persuasion principles, and any loaded brand-voice and
audience context. Structure the output using the required sections from
`format-guidelines.md` Layer 1 (header zone, hero/above-the-fold, value/proof
section, social proof, closing CTA), and include:

- Headline and subheadline (message-matched to the campaign brief/ad copy if one
  was loaded)
- Primary CTA copy, stated once and repeated identically at each section break
- Form field list, sized to the confirmed funnel stage and goal — state which
  fields were included and why
- Social proof placement and content (specific, attributed, recent — per
  guidelines)
- Any mandatory elements surfaced by the **format-specific rules** context loaded
  in Step 1 — legal disclaimers, jurisdiction-specific consent-checkbox wording,
  brand-mandated footer content, or a specific form/CRM provider's field names.
  If Step 1 found no format-specific rules context and the confirmed audience is
  EU/German (see Privacy, Consent, and Compliance in `format-guidelines.md`), ask
  the owner once for the required consent wording rather than inventing it.

Internally verify against the quality checklist in `format-guidelines.md`. For
every unchecked gate, revise the draft and re-check — do not present until
every gate passes or the failure genuinely cannot be fixed (e.g. missing
context), in which case surface it in the output rather than hiding it.

If, after applying the above, a mandatory element is still unresolved — no context
covers it and the owner hasn't stated it — mark it inline with `[TODO: ...]` in the
generated page rather than guessing, and call it out in the closing summary.

Present the output in a clearly delimited block showing the content and its word
count, organized by section (Header / Hero / Value / Social proof / CTA).

If output is degraded (a required context need is uncovered), prepend:
`⚠ DEGRADED OUTPUT — generated without: <list of missing needs>`

## Step 8: Feedback

This step has two phases:

**Auto-store phase.** Before asking the user for feedback, review the run for
qualifying observations. For each, append one tagged line to `.claude/learnings.md`
(create with standard header if missing), tagged `[cc-content:landing-page]`.
Qualifies: content preferences or constraints not already in any loaded context file
or `CLAUDE.md`; corrections the user made; project-specific facts that would change
future output; accepted/rejected suggestions deviating from best practices. Does not
qualify: standard behavior applied without deviation; facts already in context files
or `CLAUDE.md`; anything derivable by re-reading context files; facts semantically
equivalent to any existing `.claude/learnings.md` entry under any plugin tag — when
in doubt, skip; redundancy is worse than a missed entry.

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
"✓ N learning(s) auto-saved to `.claude/learnings.md`." Then deliver a closing line
and exit. Tailor the closing delivery note to what was actually produced rather than
a fixed phrase: if the confirmed audience was EU/German, remind the owner to have the
consent-checkbox wording reviewed before publishing; if format-specific rules context
named a page builder, CMS, or form/CRM provider, reference handing the copy off there;
otherwise default to a generic "ready to hand off to your web developer or landing-page
builder."
