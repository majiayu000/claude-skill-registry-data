---
name: marketing-email
description: >
  Use this skill when the owner wants to write, draft, or generate a marketing or
  sales email — a campaign email, newsletter, nurture-sequence email, or cold/warm
  sales outreach. Invoke when the user says "write a marketing email", "draft a sales
  outreach email", "create a newsletter email", "write a cold email", "draft a nurture
  email", or "generate an email campaign". Not for everyday personal or internal
  professional correspondence.
allowed-tools: Read, Write, Bash
argument-hint: "[optional: path to campaign briefing file]"
---

@./format-guidelines.md **Read when:** starting this skill
@../\_shared/storytelling-frameworks.md **Read when:** selecting a narrative framework in Step 5
@../\_shared/persuasion-principles.md **Read when:** selecting persuasion principles in Step 6

# Email Skill

You are helping the owner produce a complete, publishable marketing or sales email.
The email must comply with the format guidelines in this skill folder, reflect the
company's brand voice, and — if a campaign briefing is present — serve the briefing's
goals.

This skill covers **marketing email** (bulk campaigns, newsletters, nurture
sequences) and **sales email** (cold or warm 1:1 outreach) as two flavors of the same
discipline. It does not cover everyday personal or internal professional
correspondence. This skill is **language-, industry-, and audience-neutral**. It works
for any output language and any B2B or B2C context. Calibration happens through the
loaded context files, the campaign briefing (if any), and the owner's topic input.

## Step 0: Recall learnings

If `.claude/learnings.md` exists, read it silently. Apply all relevant entries to
inform this run. Do not announce this step. If the file is absent, continue normally.

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

| Need                    | What to look for in the Summary                                     |
| ----------------------- | ------------------------------------------------------------------- |
| Brand voice             | Writing style, tone, vocabulary, phrasing rules, things to avoid    |
| Organization background | Who the company/author is, products, positioning, mission           |
| Target audience         | Reader personas, goals, challenges, job titles, B2B/B2C signals     |
| Output language         | Default language, locale, or region                                 |
| Email-specific rules    | Signature/legal-footer requirements, send-cadence policy, CTA rules |

Where multiple files plausibly cover the same need, pick the one whose Summary best
fits the task at hand and note the choice.

Warn on **semantic absence, not label absence** — "No brand voice context found",
never "no `writing-style` row". Gate on two needs only: if no loaded file plausibly
covers **brand voice**, or none covers **organization background**, ask once whether
this is intentional or whether the user should pause and run `/content-onboarding`.

> "I don't see any [writing style / organization background] context. Is this
> intentional, or should I pause while you run `/content-onboarding`?"
>
> - **Intentional**: note the gap; label the final output
>   `⚠ DEGRADED OUTPUT — no [brand voice / organization background] context`
> - **Pause**: direct the owner to onboarding and stop.

For absent audience, language, or email-specific rules: note silently and continue —
never ask.

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

## Step 3: Infer and confirm email type, audience, and goal

This is the content-production-specific step for email.

1. Use the loaded audience context and campaign brief (if any) to infer:
   - **Email type**: marketing (campaign/newsletter/nurture) or sales (cold/warm
     outreach)
   - **Audience**: B2B or B2C
   - **Content goal**: thought leadership, awareness, lead generation, nurturing,
     conversion, or retention/win-back
   - **Funnel stage**: TOFU, MOFU, or BOFU
   - **Audience expertise level**: novice, familiar, or expert

   If the loaded context genuinely does not support a confident inference on any of
   these, ask the owner the missing question directly rather than guessing.

2. Present a one-line inference summary to the user, for example:
   "Type: Sales outreach · Audience: B2B (mid-market) · Goal: lead generation ·
   Stage: MOFU · Expertise: familiar"

3. Ask the user to confirm or correct before generating. Do not silently apply
   assumptions.

4. Based on confirmed values, explicitly state which Layer 2 and Layer 3 variations
   from `format-guidelines.md` are being applied and why (e.g., "Applying the B2B
   sales-outreach variant — staged CTA, account-specific social proof, no scarcity
   framing — and the MOFU funnel profile — comparative proof, medium CTA
   directness").

## Step 4: Ask for the content topic (if not provided)

If the owner has not specified a topic, offer, or key message, ask:

> "What should this email be about? You can describe the offer, key message, or
> paste raw notes and I'll turn them into a draft."

Wait for the answer, then proceed.

## Step 5: Select storytelling framework

Read `../_shared/storytelling-frameworks.md` and follow its selection process. For
**marketing** email, AIDA (Attention – Interest – Desire – Action) or the Inverted
Pyramid are typically strong fits. For **sales** outreach, a tighter spine usually
works better: reason for contact → relevant problem or goal → proof → low-friction
next step. Apply the chosen framework as the structural spine.

## Step 6: Select persuasion principles

Read `../_shared/persuasion-principles.md` and follow its selection process. Pick 1–3
principles that fit the confirmed email type, B2B/B2C audience, and funnel stage —
per `format-guidelines.md`, avoid scarcity/loss framing in B2B contexts unless the
deadline is genuinely real, and prefer account-specific social proof over generic
claims in sales outreach. Note the choices in working notes.

## Step 7: Generate the email

Produce a complete email that:

- Includes a subject line and preheader (mobile-safe length, no spam-trigger
  language)
- Opens with a hook that states relevance immediately — no pleasantries or
  self-introduction first
- Applies the confirmed email-type, B2B/B2C, goal, funnel-stage, and expertise-level
  variant from `format-guidelines.md`
- Uses the framework chosen in Step 5 as its structural spine
- Weaves in the persuasion principles chosen in Step 6
- Has exactly one primary CTA, phrased as a specific, low-friction action
- Reflects tone and vocabulary from loaded brand voice context
- Ends with a brief, in-voice sign-off (thanks + sender name) — do not draft a full
  signature block, legal footer, Impressum, or unsubscribe link

Legal footers, Impressum, and unsubscribe links are fixed parts of the sending
template (email marketing tool, CRM "send email" feature, or email client) rather
than per-email content. Append this fixed note after the draft, not a `[TODO: ...]`
placeholder:

> "Footer/legal compliance (Impressum, unsubscribe link, required disclosures) is
> not included above — that lives in your sending tool's template. Confirm it meets
> current legal requirements and your company's policy before sending."

Internally verify against the quality checklist in `format-guidelines.md`. For
every unchecked gate, revise the draft and re-check — do not present until
every gate passes or the failure genuinely cannot be fixed (e.g. missing
context), in which case surface it in the output rather than hiding it.

Present the output in a clearly delimited block:

```
─────────────────────────────────────────────
Email draft — <email type>
─────────────────────────────────────────────
Subject: <subject line>
Preheader: <preheader text>

<email body>
─────────────────────────────────────────────
Word count: <N> | Subject length: <N> characters
```

If output is degraded (a required context need is uncovered), prepend:

```
⚠ DEGRADED OUTPUT — generated without: <list of missing needs>
```

## Step 8: Feedback

This step has two phases:

**Auto-store phase.** Before asking the user for feedback, review the run for
qualifying observations. For each, append one tagged line to `.claude/learnings.md`
(create with standard header if missing), tagged `[cc-content:marketing-email]`.
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

**Explicit feedback.** Ask whether the output met expectations. If the user provides a
correction, append it as a tagged entry using the same criteria. Confirm total entries
written across both phases: "✓ N learning(s) saved to `.claude/learnings.md`." If the
user confirms quality or skips: if any entries were auto-stored, confirm
"✓ N learning(s) auto-saved to `.claude/learnings.md`." Then deliver a closing line —
`Paste into your email marketing tool.` — and exit.
