---
name: long-tail-copy
description: >
  Use this skill to draft a finished marketing or PR text for an output format
  that does NOT have its own dedicated skill — for example a newsletter,
  whitepaper, landing-page copy, product description, email, webinar
  abstract, or ad copy. Invoke when the user says
  "draft a newsletter", "write the copy for this landing page", "turn this idea
  into a <format>", or names any text deliverable without a dedicated skill. This
  is the general-purpose writer for the long tail of formats. It deliberately
  defers: if a dedicated skill exists for the requested format (such as a blog
  article or LinkedIn post, or a project-specific skill), it points the owner
  there first. Do NOT use it for formats that already have a dedicated skill.
allowed-tools: Read, Write, Bash
argument-hint: "[optional: path to campaign briefing or inspiration file]"
---

@../\_shared/storytelling-frameworks.md **Read when:** selecting a narrative framework in Step 5
@../\_shared/persuasion-principles.md **Read when:** selecting persuasion principles in Step 6

# General Text Skill

You are helping the owner produce a **complete, ready-to-use text** for a content
format that does not have its own dedicated skill. The text must reflect the
company's brand voice, speak to the right audience, follow any format rules the
project has registered, and — if a campaign briefing is present — serve its goals.

This skill is **format-, language-, industry-, and audience-neutral**. It carries
the _craft_ (a two-pass draft-then-self-edit process, framework and persuasion
selection) but holds **no built-in rules for any specific format**. Format rules
come from the project's own context files when they exist, and otherwise from your
own knowledge of best practices for the requested format.

Because it is general, this skill must be careful **not to do work a dedicated skill
would do better**. Step 2 is where it checks for that and, if needed, routes the
owner away.

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
| Format rules            | Best practices / structure / length for a specific output format |

**When multiple files plausibly cover the same need**, pick the one whose Summary
best fits this specific task. For example, if one brand-voice file is "casual —
employer branding" and another is "formal — corporate communications", and this is
a press release, load the formal one and note the choice.

**Coverage gaps — flag these two:**

If no loaded file plausibly covers **brand voice**, ask once:

> "I don't see any writing style or brand voice context. Is this intentional, or
> should I pause while you run `/content-onboarding`?"
>
> - **Intentional**: note the gap; label the output `⚠ DEGRADED OUTPUT — no brand voice context`
> - **Pause**: direct the owner to onboarding and stop.

Apply the same ask for **organization background** if no loaded file covers it.

For absent audience or language: note silently and continue. Format rules are handled
explicitly in Step 2.

## Step 1.5: Detect multi-format requests

If the owner's request names 2 or more target formats, or explicitly asks to
"repurpose," "atomize," or "turn this into multiple formats," stop and say:
"That's a multi-format request — `/atomize` handles fan-out across
formats from one core message. Switching you there." Do not continue this skill's
own drafting steps for a multi-format request.

## Step 2: Identify the format and route correctly

This is the step that keeps the general skill in its lane. First, settle on the
**requested output format**. If the owner has not named one clearly, ask:
_"What format is this for — e.g. press release, newsletter, landing page, whitepaper,
email, product description?"_

Once you know the format, work through three tiers **in order**:

### Tier A — A dedicated skill exists for this format → offer to route

Some formats have their own dedicated skill that applies format-specific best
practices this general skill does not. Using the general skill for them produces
weaker results, so check first.

**How to check:** look at the skills available in this session (your available-skills
list). The cc-content plugin ships dedicated skills for some formats — for example
blog articles (`blog-article`) and LinkedIn posts (`linkedin-post`)
— and **the project may have added its own** dedicated skills for other formats. Do
**not** rely on a hardcoded list; judge from the skills actually available whether any
one's purpose squarely covers the requested format.

**If a dedicated skill covers the format**, stop and tell the owner:

> "There's a dedicated skill — `/<skill-name>` — for <format>. It applies
> format-specific best practices that this general skill doesn't, so it will usually
> give you a better result. Do you want to:
> (a) Switch to `/<skill-name>` (recommended)
> (b) Continue here with the general text skill?"

- **(a)** → direct the owner to the dedicated skill and stop.
- **(b)** → note "owner chose the general skill over `<skill-name>`" and continue.

If unsure whether a skill truly covers the format, surface the option rather than
guessing silently — let the owner decide.

### Tier B — No dedicated skill, but a format-guideline file is registered → load it

From the context files you loaded in Step 1, check whether any file's Summary covers
**best practices, structure, or length for the requested format** (e.g. a whitepaper
guideline, e-mail best-practices, landing-page guideline, webinar guideline). If one
exists, treat it as **authoritative** for this format: load it, and follow its rules
on length, structure, mandatory sections, and conventions. Note: "Format rules loaded
from `<file>`."

### Tier C — Neither → use your own best practices

If no dedicated skill and no registered guideline cover the format, draft using your
own knowledge of current best practices for that format — appropriate length,
structure, and conventions for the channel. Note: "No project guideline for <format>;
using general best practices."

## Step 3: Check for campaign briefing and inspiration input

1. **Campaign briefing.** If the owner passed a file path as an argument
   (`$ARGUMENTS`), use it; otherwise check for `brief.md` in the working directory:

   ```bash
   ls brief.md 2>/dev/null && echo "found" || echo "missing"
   ```

   - **Found**: read it; note key messages, goals, and constraints. Confirm:
     "✓ Campaign briefing loaded from `<path>`."
   - **Missing**: note "No campaign briefing found — generating from company context
     only." and continue.

2. **Inspiration input.** If the owner referenced or pasted an article, briefing, or
   notes as the seed for the text, note its substance. If it is an **article with a
   URL**, plan to weave a brief mention of the inspiration and its **full URL** into
   the finished text (unless the format or brand voice makes that inappropriate).

## Step 4: Get the content idea, audience, and length target

If the owner has not said what the text should be about, ask:

> "What should this text say? Describe the content idea or key message, or paste raw
> notes and I'll shape them into the finished <format>."

Then settle anything still open that materially shapes the draft:

- **Output language:** write the finished text in the language specified by loaded
  context — **even when an inspiration article is in another language** (an English
  source does not make a German-default project's text English). Only if no output
  language is in context, fall back to the language of the owner's request.
- **Audience:** if the loaded audience context has more than one persona, infer which
  one(s) this text targets and confirm in one line. If audience context is absent and
  the owner hasn't said, ask only if it would change the draft meaningfully.
- **Length target:** use the Tier-B guideline's length if one was loaded; otherwise
  use a sensible target for the format and state it. If a guideline specifies an
  optimal length, use the full range to give the reader substance rather than
  underfilling it.

## Step 5: Select a storytelling framework

Read `../_shared/storytelling-frameworks.md` and follow its selection process. Apply
the chosen framework as the **structural spine** of the text, where it fits the
format (a press release and a webinar abstract use structure differently than a
narrative email). Where the SPIN logic (Situation → Problem → Implication →
Need-Payoff) fits the task, let it shape the argument's progression. Note the choice
in working notes — e.g. "Using **PAS** as the spine; SPIN progression for the body."

## Step 6: Select persuasion principles

Read `../_shared/persuasion-principles.md` and follow its selection process. Pick
**1–3 principles** that fit the goal and the reader's state, plus a pre-suasive opener
strategy. Layer them naturally into the prose — not as labeled callouts. Note the
choice — e.g. "Using **Authority + Social Proof**; opener primes credibility."

## Step 7: Draft (pass 1)

Write the text in the output language as a **creative, expressive** finished piece for
the requested format. Hold to these rules:

1. **Connect to the organization.** Tie the content idea (and any inspiration input)
   to the organization's products, services, and experience — but keep it subtle.
   Avoid overt self-promotion like "based on our X years of experience as …"; the
   connection should read as relevance, not advertising.
2. **Offer original value.** Go beyond the facts of any inspiration input — add a
   framing, application, or insight the source itself doesn't provide.
3. **Use the brand voice.** Follow the loaded brand-voice context closely; you are
   writing _as_ the organization.
4. **Apply SPIN where it fits.** Let Situation → Problem → Implication → Need-Payoff
   shape the structure when the task suits it.
5. **Honor format best practices.** Apply the Tier-B guideline (if loaded) or your own
   best practices for the format's length, structure, and conventions.
6. **Cite the inspiration** if an article was provided: mention it and include its
   full URL in the text (unless format/brand voice says otherwise).
7. **Aim at the audience.** Shape content, structure, and tone for the confirmed
   persona(s).

## Step 8: Self-edit (pass 2)

Now read your pass-1 draft **sentence by sentence** and revise it. Intervene **as
much as necessary but as little as possible** — preserve what works.

Check and fix:

1. **Factual errors and ambiguous phrasing.** Correct statements that are wrong or
   that a reader could reasonably misread. If a fix would require heavy rewriting,
   cut the passage instead — as long as removing it doesn't break what follows.
2. **Unsupported claims about the organization.** Every reference to the org's
   products, services, or experience must be traceable to the loaded context. If a
   claim isn't adequately supported, soften it, rephrase it, or remove it.
3. **Hype and over-dramatization.** The text should be opinionated and confident, but
   not sensational. Defuse exaggeration, clickbait phrasing, and manufactured drama.
4. **Style drift.** Bring any passage that drifts from the brand voice or the format
   guideline back into line — including new sentences you add while editing.
5. **AI tells — em-dash insertions.** Find parenthetical insertions set off by dashes
   ("–" or "—") and rewrite them as clean sentences so none of those enclosing dashes
   remain. This is a frequent, recognizable tell; removing it makes the text read as
   human-written.

If a Tier-B guideline specifies an optimal length, make sure the edited text uses the
full range rather than coming in thin.

## Step 9: Present the text

Present the finished text in a clearly delimited block so the owner can copy it
cleanly:

```
─────────────────────────────────────────────
<format> draft
─────────────────────────────────────────────
<the finished text only — no preamble, no commentary inside the block>
─────────────────────────────────────────────
Format rules: <Tier-B file name | "general best practices">
Framework: <name> · Persuasion: <list>
Length: <count> <unit> (target: <range or "n/a">)
─────────────────────────────────────────────
```

The block must contain **only the deliverable text** — the German source prompt was
explicit that the asset itself carries no introduction or explanation. Put any notes
in the footer rows, not inside the text.

**Channel formatting:** if the text is for a **social-media post or any channel that
strips formatting**, do not use bold, italics, or their Markdown equivalents. Replace
bullet points with fitting emojis, and keep the body plain.

If the output is degraded (brand voice or organization context missing), prepend:

```
⚠ DEGRADED OUTPUT — generated without: <list of missing context>
```

## Step 10: Feedback

**Auto-store phase.** Before asking for feedback, review this run. For each qualifying
observation, append one tagged line to `.claude/learnings.md` (create with the
standard header if missing):

```text
[cc-content:long-tail-copy] <concise observation> — <YYYY-MM-DD>
```

Qualifies: content preferences or constraints not already in any loaded context file
or `CLAUDE.md`; corrections the owner made to the output; project-specific facts that
would change future output (e.g. "press releases here always end with a boilerplate
paragraph"); accepted/rejected deviations from best practices.

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

> "Did this text meet expectations? Any corrections or notes for future texts —
> or press Enter to finish."

- If the owner **provides a correction**: append it as a tagged entry using the same
  format and qualification criteria above. Confirm: "✓ N learning(s) saved to
  `.claude/learnings.md`."
- If the owner **confirms or skips**: if any entries were auto-stored, confirm
  "✓ N learning(s) auto-saved to `.claude/learnings.md`." Then exit. If nothing was
  stored, exit directly.
