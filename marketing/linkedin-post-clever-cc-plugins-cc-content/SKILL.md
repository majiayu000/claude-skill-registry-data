---
name: linkedin-post
description: >
  Use this skill when the owner wants to write, draft, or generate a LinkedIn post.
  Invoke when the user says "write a LinkedIn post", "draft a post for LinkedIn",
  "create a LinkedIn update", "generate a LinkedIn post", or "post on LinkedIn".
allowed-tools: Read, Write, Bash
argument-hint: "[optional: path to campaign briefing file]"
---

@./format-guidelines.md **Read when:** starting this skill
@../\_shared/storytelling-frameworks.md **Read when:** selecting a narrative framework in Step 3b
@../\_shared/persuasion-principles.md **Read when:** selecting persuasion principles in Step 3c

# LinkedIn Post Skill

You are helping the owner produce a complete, publishable LinkedIn post. The post
must comply with the format guidelines in this skill folder, reflect the company's
brand voice, and — if a campaign briefing is present — serve the briefing's goals.

This skill is **language-, industry-, and audience-neutral**. It works for any
output language and any B2B or B2C context. Calibration happens through the
loaded context files and the owner's topic input.

## Step 0: Recall learnings

If `.claude/learnings.md` exists, read it silently. Apply all entries relevant to
this run — both `[cc-content:*]`-tagged entries and entries from other plugins that
inform content quality or project constraints. Do not announce this step. If the file
is absent, continue normally.

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

| Need                    | What to look for in the Summary                                  |
| ----------------------- | ---------------------------------------------------------------- |
| Brand voice             | Writing style, tone, vocabulary, phrasing rules, things to avoid |
| Organization background | Who the company/author is, products, positioning, mission        |
| Target audience         | Reader personas, goals, challenges, job titles                   |
| Output language         | Default language, locale, or region                              |
| LinkedIn-specific rules | Hashtag policies, disclaimers, link policies, CTA constraints    |

**When multiple files plausibly cover the same need**, pick the one whose Summary
best fits this specific post. For example: if one file's Summary says "casual, inclusive —
job ads and employer branding" and another says "formal — corporate communications",
and this post is a recruiting post, load the casual one and note the choice.

**Coverage gaps — flag these two:**

If no loaded file plausibly covers **brand voice**, ask once:

> "I don't see any writing style or brand voice context. Is this intentional, or should
> I pause while you run `/content-onboarding`?"
>
> - **Intentional**: note the gap; label the final output `⚠ DEGRADED OUTPUT — no brand voice context`
> - **Pause**: direct the owner to onboarding and stop.

Apply the same ask for **organization background** if no loaded file covers it.

For absent audience, language, or LinkedIn-specific rules: note silently and continue.

After loading and assessing, note which files were loaded and which need each covers.
Proceed to Step 2.

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

## Step 3: Ask for the post topic (if not already provided)

If the owner has not specified a topic or goal for the post, ask:

> "What should this post be about? You can describe the topic, share a key message
> you want to convey, or paste raw notes and I'll turn them into a post."

Wait for the answer, then proceed.

## Step 3a: Determine account type (personal profile vs. company page)

Format guidance in `format-guidelines.md` now diverges meaningfully between personal
profiles and company pages — voice, length, CTA style, and tone all differ (see
"Personal Profile vs. Company Page" in that file). Infer the account type from the
campaign briefing or loaded context if it's stated there. If it isn't, ask once:

> "Is this post for a personal profile (first-person, founder/employee voice) or a
> company page (brand voice)?"

Note the answer — it drives length target, voice, and CTA style in Step 4.

## Step 3b: Select a storytelling framework

Read `../_shared/storytelling-frameworks.md` and follow the selection process described
there. Apply the chosen framework as the structural spine of the post.

## Step 3c: Select persuasion principles

Read `../_shared/persuasion-principles.md` and follow its selection process. Pick 1–3
principles that fit the post's goal and the reader's state, plus a pre-suasive opener
strategy. Note the choice in working notes (e.g., "Using **Authority + Social Proof**,
opener primes credibility").

## Step 4: Generate the post

Produce a complete LinkedIn post that:

- Opens with a tight, unbroken hook within ~140 characters (mobile fold), no blank
  line before the fold, starting with one structural emoji
- Is calibrated to the account type from Step 3a — voice, length target, and CTA
  style per the "Personal Profile vs. Company Page" table in `format-guidelines.md`
- Is structured according to the framework chosen in Step 3b (if applicable)
- Includes a body delivering the substance the hook promises
- Ends with a specific, singular CTA that invites a substantive reply — never an
  engagement-bait phrase ("Comment YES", "Agree?", "Tag someone who needs this")
- Uses 0–3 emojis placed structurally, not decoratively (omit if brand voice prohibits)
- Hashtags are optional — if used, 3–5 relevant tags at the end; omitting them is a
  fine default, not a compromise
- Stays within the recommended character target for the account type (1,300–2,500
  for personal profiles, ≤700–800 for company pages)
- Reflects tone and vocabulary from loaded brand voice context
- Addresses the audience from loaded audience context
- Avoids AI-slop clichés and uniform sentence rhythm; anchors every claim with a
  specific number, name, or outcome
- Includes a link directly in the post body if a link adds real value to the post —
  never hides it in the first comment as a reach workaround

Internally verify against the quality checklist in `format-guidelines.md`. For
every unchecked gate, revise the draft and re-check — do not present until
every gate passes or the failure genuinely cannot be fixed (e.g. missing
context), in which case surface it in the output rather than hiding it.

If the briefing is present, the post must serve its stated goals and key messages.

Present the post in a clear block:

```
─────────────────────────────────────────────
LinkedIn post draft
─────────────────────────────────────────────
<post content>
─────────────────────────────────────────────
Character count: <N> / 3,000
```

If the output is degraded (brand voice or organization context missing), prepend:

```
⚠ DEGRADED OUTPUT — generated without: <list of missing context>
```

## Step 5: Feedback

**Auto-store phase.** Before asking for feedback, review this run. For each qualifying
observation, append one tagged line to `.claude/learnings.md` (create with standard
header if missing):

```text
[cc-content:linkedin-post] <concise observation> — <YYYY-MM-DD>
```

Qualifies: content preferences or constraints not already in any loaded `context/` file
or `CLAUDE.md`; corrections the owner made to the output; project-specific facts that
would change future output; accepted/rejected suggestions deviating from best practices.

Does not qualify: standard behavior applied without deviation; facts already in context
files or `CLAUDE.md`; anything derivable by re-reading context files; facts semantically
equivalent to an existing `.claude/learnings.md` entry under any plugin tag — when in
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

**Explicit feedback.** After the auto-store phase, ask:

> "Did this post meet expectations? If you have any corrections or notes for
> future posts, share them here — or press Enter to finish."

- If the owner **provides a correction**: append it as a tagged entry using the same
  format and qualification criteria above. Confirm total entries written across both
  phases: "✓ N learning(s) saved to `.claude/learnings.md`."
- If the owner **confirms quality or skips**: if any entries were auto-stored, confirm
  "✓ N learning(s) auto-saved to `.claude/learnings.md`." Then say "Great — the post
  is ready to publish. Copy it above and paste directly into LinkedIn." and exit. If
  nothing was stored, skip the confirmation and exit directly.
