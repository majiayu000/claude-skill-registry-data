---
name: new-content-skill
description: >
  Use this skill when building a new content-production skill for a specific output format.
  Invoke when the user says "create a new content skill", "build a skill for [format]",
  "new content skill", "synthesize research into a skill", or "create a [format] skill".
allowed-tools: Read, Write, Bash
argument-hint: "<format-name> [--plugin] (e.g., blog-article, marketing-email --plugin)"
---

# New Content Skill

This meta-skill turns external research reports into a fully structured content-production
skill. It reads research files from the staging folder, assesses coverage across all content
axes, synthesizes a three-layer `format-guidelines.md`, and generates a `SKILL.md` skeleton
ready for customization.

## Step 0: Recall learnings

If `.claude/learnings.md` exists, read it silently. Apply relevant entries — such as
prior skill-creation observations or project-level defaults that would affect how this
skill is structured. Do not announce this step. If the file is absent, continue normally.

## Step 1: Determine the format name and mode

If the user passed a format name as `$ARGUMENTS`, use it. Normalize to kebab-case
(e.g., "Blog Article" → `blog-article`, "Marketing Email" → `marketing-email`).
Strip the `--plugin` flag from `$ARGUMENTS` before deriving the format name — it is not
part of the name.

If no argument was passed, ask:

> "What content format is this skill for? Provide a short kebab-case name — for example:
> `blog-article`, `marketing-email`, `whitepaper`, `video-script`, `case-study`."

Wait for the answer before proceeding.

**Determine the mode.** After resolving the format name, check whether `$ARGUMENTS`
contains the flag `--plugin`.

- If `--plugin` is present: you are in **plugin-dev mode**. The output will go into the
  `cc-content` plugin repository at `plugins/cc-content/skills/<format-name>/`.
- If `--plugin` is absent: ask once:

  > "Where should this skill be created? Reply `project` for a project-local custom skill,
  > or `plugin` to contribute it to the cc-content plugin."

  Wait for the answer. `project` → **end-user mode**; `plugin` → **plugin-dev mode**.

Store the mode — it controls output paths, shared-file handling, and @-imports in all
subsequent steps.

## Step 2: Find research files

Check whether the staging folder exists and contains `.md` files:

```bash
ls .claude/skill-drafts/<format-name>/ 2>/dev/null && echo "found" || echo "missing"
```

**If missing or empty:** respond with the following and stop:

> "No research files found at `.claude/skill-drafts/<format-name>/` (your consuming project's
> local `.claude/` folder, not a folder inside the plugin repository).
>
> To get started, open `${CLAUDE_SKILL_DIR}/../_shared/content-skill-research-brief.md` — it
> contains six copy-paste research prompts and a combined mega-prompt for your preferred
> AI tool (Perplexity, Claude.ai, ChatGPT).
>
> Save each research response as a `.md` file under `.claude/skill-drafts/<format-name>/`,
> then invoke this skill again. If you were running in plugin-dev mode, remember to include
> `--plugin` again."

**If found:** list the files and read all of them:

```bash
ls .claude/skill-drafts/<format-name>/*.md 2>/dev/null
```

Read every file listed. Note which files appear to cover which research areas (by content,
not filename).

## Step 3: Assess research coverage

Semantically assess the research files across six coverage areas. Match on meaning, not
filenames — a single file from the combined mega-prompt may cover all six areas at once.

| #   | Coverage area                             | Maps to layer                               |
| --- | ----------------------------------------- | ------------------------------------------- |
| 1   | Universal structure                       | Layer 1 — hook, body, CTA, length, format   |
| 2   | B2B vs. B2C differences                   | Layer 2 — audience-specific variations      |
| 3   | Content goal variations                   | Layer 3 — goal axis                         |
| 4   | Funnel stage adaptations (TOFU/MOFU/BOFU) | Layer 3 — funnel axis                       |
| 5   | Audience expertise adaptations            | Layer 3 — expertise axis                    |
| 6   | Psychological / persuasion principles     | Layer 2 + 3 — Cialdini, biases, pre-suasion |

Present a coverage summary like:

```
Coverage assessment for [FORMAT]:

✓ 1. Universal structure — hook, CTA, and length guidelines found
✓ 2. B2B vs. B2C differences — covered
✗ 3. Content goal variations — not found
✓ 4. Funnel stage adaptations — TOFU/MOFU/BOFU covered
✗ 5. Audience expertise adaptations — not found
✓ 6. Persuasion principles — Cialdini principles present

Gaps: areas 3 and 5.
```

For each gap, ask once:

> "Area [N] — [name] — is not covered by the research files. Choose:
> a) I synthesize this section from general knowledge (flag it for review)
> b) Pause — you run the research prompt from `content-skill-research-brief.md` and we resume
>
> Reply with the area numbers you want me to synthesize (e.g., `3 5`), or `pause` to stop."

- If the user replies `pause`: stop and remind them to save the research under
  `.claude/skill-drafts/<format-name>/` before invoking the skill again.
- If the user accepts knowledge-based synthesis for any gaps: note which areas will be
  marked `⚠ KNOWLEDGE-BASED` in the output and proceed.

## Step 4: Synthesize format-guidelines.md

Create the skill folder and — in end-user mode only — copy shared reference files into
the project if not already present.

**End-user mode:**

```bash
mkdir -p .claude/skills/<format-name>
mkdir -p .claude/skills/_shared
cp -n "${CLAUDE_SKILL_DIR}/../_shared/storytelling-frameworks.md" ".claude/skills/_shared/" 2>/dev/null
cp -n "${CLAUDE_SKILL_DIR}/../_shared/persuasion-principles.md" ".claude/skills/_shared/" 2>/dev/null
```

**Plugin-dev mode:** do not copy shared files — they already exist in the repo at
`plugins/cc-content/skills/_shared/`. Only create the new skill folder:

```bash
mkdir -p plugins/cc-content/skills/<format-name>
```

Write the `format-guidelines.md` to:

- **End-user mode:** `.claude/skills/<format-name>/format-guidelines.md`
- **Plugin-dev mode:** `plugins/cc-content/skills/<format-name>/format-guidelines.md`

Base every claim on the research files; use knowledge-based synthesis only for
user-approved gaps, and mark those sections with
`⚠ KNOWLEDGE-BASED — verify before treating this skill as production-ready`.

**Filter out algorithm-gaming tactics.** Research files sourced from tutorials,
"growth hacker" coaches, and marketing blogs often carry tactics whose sole purpose
is manipulating a ranking algorithm rather than serving the reader (e.g., hiding a
useful link in the first comment to dodge a suspected reach penalty, engagement-bait
CTAs, keyword-stuffed profiles). Do not carry these into `format-guidelines.md` as
recommended practice, even when a research file presents them as current best
practice — platforms iterate to detect and penalize exactly these tricks, so they
have a short shelf life by design (the same dynamic as black-hat SEO: keyword
stuffing and link farms didn't survive Google's algorithm updates, while genuine
value — useful content, real backlinks, good UX — did, because it was never a trick
in the first place, just what the algorithm was a proxy for). When a research file
surfaces a tactic like this, either omit it or, if it's worth flagging as a
documented trend, present it under "Common Mistakes / Outdated Tactics" rather than
as guidance to follow. Genuine platform mechanics that happen to also serve the
reader (e.g., short paragraphs for scannability, a real hook because attention is
finite) are not gaming tactics and belong in the guidelines normally.

The file must follow this three-layer structure:

---

### Layer 1 — Universal Best Practices

Open with a brief framing sentence ("These apply to every [FORMAT] regardless of audience
type, goal, or channel."), then cover each topic as a headed subsection:

- **Length and scope** — optimal length ranges, units (words / characters / pages), when
  to deviate from defaults
- **Required sections** — the structural skeleton with the purpose of each section
  (e.g., opening/hook, body sections, closing/CTA); use a numbered or bulleted list
- **Hook / opening** — what makes a strong opener for this format, high-performing
  patterns, anti-patterns to avoid; cite named frameworks where applicable (AIDA, PAS, etc.)
- **Call to action** — placement, phrasing norms, single-vs-multiple CTA rules
- **Formatting conventions** — use of headers, bullets, white space, visual rhythm;
  reading patterns for this format (e.g., F-pattern, linear reading, skimming)
- **What separates high from low performers** — distilled differentiators from research

---

### Layer 2 — Audience-Specific Variations

**B2B vs. B2C section** — a comparison table covering: optimal length, tone, evidence /
proof type, decision-maker psychology, buying cycle impact, CTA approach, reading context.
Follow the table with prose notes on significant differences. Include B2B sub-variations
where relevant (SMB vs. enterprise, technical buyer vs. executive sponsor).

**Persuasion principles section** — which Cialdini principles and cognitive biases are most
applicable to this specific format, with concrete implementation techniques. Note where
effectiveness or implementation differs between B2B and B2C. Flag overuse risks.

---

### Layer 3 — Goal and Funnel Variations

**By content goal** — a table with a row for each of the six goals (thought leadership,
awareness, lead generation, nurturing, conversion, retention) and columns for: length /
depth, proof type, CTA directness, promotional level. Supplement with prose where the
table cells cannot capture the nuance.

**By funnel stage** — a table with rows for TOFU, MOFU, BOFU and columns for: vocabulary
level, claim specificity, proof type, CTA directness, optimal length, reader mindset, and
one common mistake at each stage.

**By audience expertise** — a table with rows for novice, familiar, and expert, covering:
vocabulary, background context depth, credibility signals, content density, and tone
calibration.

---

### Quality Checklist

A `- [ ]` checklist with format-specific quality gates derived from the research, plus
these universal items:

- Audience type, goal, and funnel stage inferences confirmed with user
- Tone consistent with brand voice (if loaded)
- CTA is singular and matches the stated goal

---

Confirm when written:

- **End-user mode:** "✓ Written: `.claude/skills/<format-name>/format-guidelines.md`"
- **Plugin-dev mode:** "✓ Written: `plugins/cc-content/skills/<format-name>/format-guidelines.md`"

## Step 5: Generate SKILL.md skeleton

Write the `SKILL.md` to:

- **End-user mode:** `.claude/skills/<format-name>/SKILL.md`
- **Plugin-dev mode:** `plugins/cc-content/skills/<format-name>/SKILL.md`

The file must be a working content-production skill following the pattern established in
the content-production authoring guide. Mark every section the user must customize with
a `[TODO: ...]` tag.

**Mode-dependent TODO policy.** `[TODO: ...]` markers left in the skill's own
instructions are appropriate only in **end-user mode** — the file lives inside one
specific consuming project, and the project owner is expected to open it and fill in
project-specific specifics (their trigger phrasing, their mandatory elements, their
delivery workflow).

In **plugin-dev mode**, the generated skill ships to arbitrary downstream projects —
nothing about "the project" is known in advance, so a TODO that asks a future plugin
maintainer to hardcode a project-specific assumption (e.g., "confirm this matches your
project's typical use", "add your CMS/provider here") is a defect, not a placeholder:
no maintainer can correctly fill it in for every consumer. Every step below that would
otherwise carry such a TODO must instead be written so the skill resolves the need at
**runtime** — infer it from loaded context (Step 1) or the campaign brief (Step 2), and
if genuinely unresolvable from either, ask the owner a single targeted question during
the run. An inline `[TODO: ...]` may still appear in the _generated content itself_
(the landing page, email, etc. the skill produces for that run) when a mandatory
element is still unresolved after checking context and asking — that is a normal,
per-run gap flag, not a design-time TODO in the skill's instructions.

Required YAML frontmatter — the `name:` field is the same in both modes: `<format-name>`
(e.g., `blog-article`). Plugin skills are namespaced automatically as `cc-content:<format-name>`,
so the skill's own `name:` field must never repeat the `cc-content-` prefix.

```yaml
---
name: <format-name>
description: >
  Use this skill when the owner wants to write, draft, or generate a [FORMAT].
  Invoke when the user says "[TRIGGER PHRASES]".
allowed-tools: Read, Write, Bash
argument-hint: "[optional: path to campaign briefing file]"
---
```

**End-user mode:** leave `[TODO: add trigger phrases for this format]` in place of
`[TRIGGER PHRASES]` — the project owner may want project-specific phrasing (product
nicknames, internal terminology) that only they know.

**Plugin-dev mode:** do not leave a TODO here — write 3–5 concrete, natural-sounding
trigger phrases directly, derived from the format name itself (e.g., for
`landing-page`: "write a landing page", "draft a registration page", "create a webinar
landing page"). The format name and its research files give you everything needed to
write these; no downstream-project knowledge is required.

Required @-imports at the top of the body (after frontmatter) — paths differ by mode:

**End-user mode:**

```
@.claude/skills/<format-name>/format-guidelines.md **Read when:** starting this skill
@.claude/skills/_shared/storytelling-frameworks.md **Read when:** selecting a narrative framework
@.claude/skills/_shared/persuasion-principles.md **Read when:** selecting persuasion principles
```

**Plugin-dev mode** (relative paths, same pattern as `linkedin-post`):

```
@./format-guidelines.md **Read when:** starting this skill
@../_shared/storytelling-frameworks.md **Read when:** selecting a narrative framework
@../_shared/persuasion-principles.md **Read when:** selecting persuasion principles
```

Required skill steps — write each as a level-2 heading with full prose instructions:

**Step 0 — Recall learnings**
At the very start, if `.claude/learnings.md` exists, read it silently. Apply all
relevant entries to inform this run. Do not announce this step. If the file is absent,
continue normally.

**Step 1 — Load context**
Check for a `## Context files` table in CLAUDE.md via:
`grep -A 200 '## Context files' CLAUDE.md 2>/dev/null || echo "(no context table)"`.

CLAUDE.md files may exist at multiple hierarchy levels (workspace root, project root,
sub-directory) and the harness loads all applicable ones. Where multiple tables exist, rows
from more specific CLAUDE.md files take precedence.

**Do not enumerate required categories by name.** Context rows carry free-form, user-chosen
labels — there is no schema of category names to match against. Instead, Read every file
listed in the **File** column, then assess each row's **Summary** to work out what it covers,
and map the loaded files to the skill's content needs:

| Need                    | What to look for in the Summary                                  |
| ----------------------- | ---------------------------------------------------------------- |
| Brand voice             | Writing style, tone, vocabulary, phrasing rules, things to avoid |
| Organization background | Who the company/author is, products, positioning, mission        |
| Target audience         | Reader personas, goals, challenges, job titles                   |
| Output language         | Default language, locale, or region                              |
| Format-specific rules   | Rules governing this particular output format                    |

Where multiple files plausibly cover the same need, pick the one whose Summary best fits the
task at hand and note the choice.

Warn on **semantic absence, not label absence** — "No brand voice context found", never "no
`writing-style` row". Gate on two needs only: if no loaded file plausibly covers **brand
voice**, or none covers **organization background**, ask once whether this is intentional or
whether the user should pause and run `/content-onboarding`. Same pause / DEGRADED OUTPUT
pattern as all output-format skills. For absent audience, language, or format-specific rules:
note silently and continue — never ask.

See `../_shared/context-categories.md` for the full guide to common context patterns and the
authoring rules this step follows.

**Step 2 — Check for campaign briefing**
Check `$ARGUMENTS` first, then `ls brief.md`. If found, read and confirm. If missing,
note "No campaign briefing found — generating from company context only." and continue.

**Step 3 — Infer and confirm audience and goal**
This is the content-production-specific step. Instruct the skill to:

1. Use the loaded audience context and campaign brief (if any) to infer: B2B or B2C,
   content goal, funnel stage, and audience expertise level. If the loaded context
   genuinely does not support a confident inference, ask the owner the missing question
   directly rather than guessing.
2. Present a one-line inference summary to the user, for example:
   "Audience: B2B (mid-market) · Goal: lead generation · Stage: MOFU · Expertise: familiar"
3. Ask the user to confirm or correct before generating. Do not silently apply assumptions.
4. Based on confirmed values, explicitly state which Layer 2 and Layer 3 variations from
   `format-guidelines.md` are being applied and why.

**Step 4 — Ask for the content topic (if not provided)**
Ask: "What should this [FORMAT] be about?" and wait.

**Step 5 — Select storytelling framework**
Read `storytelling-frameworks.md` and follow its selection process. Apply the chosen
framework as the structural spine.

**Step 6 — Select persuasion principles**
Read `persuasion-principles.md` and follow its selection process. Pick 1–3 principles plus
a pre-suasive opener strategy. Note the choices in working notes.

**Step 7 — Generate the [FORMAT]**
Produce a complete [FORMAT] that applies the confirmed format-guidelines variant, the chosen
framework, the selected persuasion principles, and any loaded brand-voice and audience
context. Internally verify against the quality checklist in `format-guidelines.md`.
For every unmet gate, revise the draft and re-check — do not present until every
gate passes or the failure genuinely cannot be fixed (e.g. missing context), in
which case surface it in the output rather than hiding it.

**End-user mode:** include a `[TODO: ...]` placeholder for any format-specific mandatory
elements — for example, word count requirements, mandatory section headers, or SEO
constraints — that the project owner must specify for their use case.

**Plugin-dev mode:** do not leave a design-time `[TODO: ...]` for this — no plugin
maintainer can correctly fill in a requirement that varies per downstream project.
Instead write this step so the skill resolves mandatory elements at **runtime**: check
the **format-specific rules** context loaded in Step 1 for anything that governs this
element (legal disclaimers, provider-specific field names, jurisdiction-specific
wording, word-count constraints); if nothing loaded covers a genuinely required
element, ask the owner once rather than guessing or inventing it. Only mark an inline
`[TODO: ...]` inside the _generated output itself_ (not the skill's instructions) as a
last resort, when the element is still unresolved after checking context and asking.

Present the output in a clearly delimited block showing the content and its word / character
count.

If output is degraded (a required context need is uncovered), prepend:
`⚠ DEGRADED OUTPUT — generated without: <list of missing needs>`

**Step 8 — Feedback**
This step has two phases:

_Auto-store phase._ Before asking the user for feedback, review the run for qualifying
observations. For each, append one tagged line to `.claude/learnings.md` (create with
standard header if missing), tagged `[cc-content:<skill-name>]`. Qualifies: content
preferences or constraints not already in any loaded context file or `CLAUDE.md`;
corrections the user made; project-specific facts that would change future output;
accepted/rejected suggestions deviating from best practices. Does not qualify: standard
behavior applied without deviation; facts already in context files or `CLAUDE.md`;
anything derivable by re-reading context files; facts semantically equivalent to any
existing `.claude/learnings.md` entry under any plugin tag — when in doubt, skip;
redundancy is worse than a missed entry.

_Explicit feedback._ Ask whether the output met expectations. If the user provides a
correction, append it as a tagged entry using the same criteria. Confirm total entries
written across both phases: "✓ N learning(s) saved to `.claude/learnings.md`." If the
user confirms quality or skips: if any entries were auto-stored, confirm
"✓ N learning(s) auto-saved to `.claude/learnings.md`." Then deliver a closing line and
exit.

**End-user mode:** include a `[TODO: ...]` for a format-specific delivery note (e.g.,
"Paste into your CMS", "Send for review").

**Plugin-dev mode:** do not leave an author-facing TODO here either — no plugin
maintainer knows every downstream project's tooling. Write the closing note so it is
derived at **runtime** from what the run actually produced: reference the
format-specific rules context if it named a CMS, builder, or provider; add a
compliance reminder if the confirmed audience triggers one (e.g., a consent-wording
review for a regulated jurisdiction, if the format's guidelines include a compliance
section); and fall back to a sensible generic default (e.g., "ready to hand off to
your [developer/builder/relevant tool]") when nothing more specific is known.

---

Confirm when written:

- **End-user mode:** "✓ Written: `.claude/skills/<format-name>/SKILL.md`"
- **Plugin-dev mode:** "✓ Written: `plugins/cc-content/skills/<format-name>/SKILL.md`"

## Step 6: Report and next steps

Present a completion summary — the "Files written" section and next steps differ by mode.

**End-user mode:**

```
✓ New skill created: <format-name>

Files written:
  .claude/skills/<format-name>/format-guidelines.md
  .claude/skills/<format-name>/SKILL.md

Shared reference files (copied to project if not already present):
  .claude/skills/_shared/storytelling-frameworks.md
  .claude/skills/_shared/persuasion-principles.md
```

**Plugin-dev mode:**

```
✓ New skill created: <format-name>

Files written:
  plugins/cc-content/skills/<format-name>/format-guidelines.md
  plugins/cc-content/skills/<format-name>/SKILL.md
```

If any areas were synthesized from general knowledge (either mode):

```
⚠ Sections synthesized from general knowledge (verify before shipping):
  - [list the affected area names]
```

Then list suggested next steps:

**End-user mode next steps:**

```
Next steps:
1. Open SKILL.md and replace all [TODO: ...] markers with format-specific content.
2. Review format-guidelines.md — especially any ⚠ KNOWLEDGE-BASED sections.
3. Run /content-onboarding in this project (if you haven't already) to set up context files, then test the skill.
4. When output looks good, save strong examples with /samples-curation.
```

**Plugin-dev mode next steps:**

```
Next steps:
1. Open SKILL.md and check for any remaining [TODO: ...] markers — per the mode-dependent
   TODO policy (Step 5), plugin-dev mode should have none in the skill's own instructions;
   if any slipped through, resolve them by writing runtime resolution logic (infer from
   context, ask the owner, fall back to a generated-output TODO) instead of hardcoding a
   project-specific assumption.
2. Review format-guidelines.md — especially any ⚠ KNOWLEDGE-BASED sections.
3. Add the skill to `.claude-plugin/marketplace.json` if it's a new plugin entry.
4. Test the skill in a target project: run /content-onboarding there, then invoke your new skill.
5. When output looks good, save strong examples with /samples-curation.
```
