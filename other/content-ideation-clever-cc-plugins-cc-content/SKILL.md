---
name: content-ideation
description: >
  Use this skill when the owner wants content ideas, angles, or directions for a
  piece of content — not a finished text. Invoke when the user says "give me
  content ideas", "brainstorm angles for this article", "what could we post about
  this", "develop some directions from this briefing", "I need angles for a
  LinkedIn post / blog / newsletter", or pastes an article or notes and asks how
  the company could pick up the topic. This is the idea-generation step that
  precedes writing — it produces distinct strategic angles the owner can then hand
  to a writing skill. Do NOT use it to write the finished text itself.
allowed-tools: Read, Write, Bash
argument-hint: "[optional: path to an inspiration file or campaign briefing]"
---

@../\_shared/persuasion-principles.md **Read when:** you want to sharpen a thesis into a more compelling claim (optional)

# Content Ideation Skill

You are helping the owner generate **content ideas** — distinct strategic angles
for a piece of content, not the finished text. The owner usually arrives with an
_inspiration input_ (an article, a short briefing, raw notes, or just a topic) and
wants several different ways the organization could pick the topic up.

The value of this skill is **divergence**: producing genuinely different angles
that connect the topic to the organization and offer original value, rather than
five rephrasings of the same summary. The owner picks the angle they like and then
writes it (often with one of the dedicated writing skills).

This skill is **language-, industry-, and audience-neutral**. Calibration happens
through the loaded context files and the owner's input.

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
> (b) Continue without project context (ideas will be generic)"

Stop if (a); note "generating without project context" and continue if (b).

**If a context table exists**, read every file listed in the **File** column.

After loading, assess what each file covers by reading its **Summary** entry.
Map the loaded files to these content needs:

| Need                    | What to look for in the Summary                            |
| ----------------------- | ---------------------------------------------------------- |
| Organization background | Who the company/author is, products, services, positioning |
| Target audience         | Reader personas, goals, challenges, job titles             |
| Output language         | Default language, locale, or region                        |

**Why these three matter most for ideation:** good angles _connect the topic to the
organization_ (needs organization background) and _speak to a real reader's
situation_ (needs audience). Brand voice matters less here — it shapes the finished
text, not the strategic angle — so you do not need it to ideate well.

**Coverage gap — flag one:**

If no loaded file plausibly covers **organization background**, ask once:

> "I don't see any company or author profile in context. Without it, the angles
> can't connect the topic to your organization — they'll be generic. Is this
> intentional, or should I pause while you run `/content-onboarding`?"
>
> - **Intentional**: note the gap; label the output `⚠ DEGRADED — no organization context`
> - **Pause**: direct the owner to onboarding and stop.

For absent audience or language: note silently and continue.

## Step 2: Gather the inspiration input and target format

You need two things before ideating:

1. **The inspiration input.** Resolve it in this order:
   - If the owner passed a file path as an argument (`$ARGUMENTS`), read it.
   - If the owner pasted an article, briefing, or notes in the request, use that.
   - If the owner only named a topic, use the topic directly.
   - If nothing is provided, ask: _"What's the inspiration? Paste an article, a
     short briefing, raw notes, or just name the topic you want angles for."_

2. **The target content format.** Angles are sharper when aimed at a format
   (a LinkedIn post reads differently from a whitepaper). If the owner has not
   named one, ask: _"What format are these angles for — e.g. LinkedIn post, blog
   article, newsletter, whitepaper? Or should I keep them format-agnostic?"_
   Format-agnostic is a valid answer; proceed without a format if so.

If an inspiration **article with a URL** was provided, note the URL — the owner may
want it cited when the angle is later written up.

## Step 3: Generate 5 distinct angles

Develop **5 creative and genuinely different angles** for the chosen format. Match
each angle, where it makes sense, to the audience persona it would resonate with from
the loaded audience context — for example, an audit-pressure angle for a QA-lead
persona, a cost-and-velocity angle for an executive persona.

**Write the angle content in the project's output language.** Determine it once,
before you start: if a loaded context file specifies an output language, that language
wins — write the thesis, goal, and perspective in it **even when the inspiration input
is in another language**. (An English source article does not make the angles English;
a German-default project gets German angles.) Only if no output language is in context,
fall back to the language of the inspiration input, and if that too is unclear, English.

The angles must **not** merely restate the inspiration input. Each one should:

- **Connect to the organization.** Show concretely how the topic ties to the
  organization's products, services, or experience. Let this surface naturally —
  the goal is relevance, not a sales pitch.
- **Offer original value.** Go beyond the facts of the input: a fresh framing, a
  pointed (even contrarian) thesis, a practical application, a surprising
  connection, or a forward-looking prediction grounded in the organization's
  expertise.
- **Keep a positive underlying tone**, even when the thesis is provocative.

Aim for spread across the five: vary the _type_ of value (don't return five
predictions or five how-tos). If you can sharpen a thesis into a more compelling
claim, the persuasion-principles reference is available — but keep angles concise;
this is ideation, not drafting.

Present each angle in exactly this structure:

```
─────────────────────────────────────────────
Content angles — <format or "format-agnostic">
Topic: <one-line topic>
─────────────────────────────────────────────

Angle 1: <short label>
• Thesis:      <sharp, pointed core claim or contrarian view>
• Goal:        <what the audience should learn, realize, or discuss>
• Perspective: <the org's own angle, experience, or approach to present it>

Angle 2: …
[5 angles total]
─────────────────────────────────────────────
```

If the output is degraded (no organization context), prepend:

```
⚠ DEGRADED — generated without organization context; angles are generic
```

## Step 4: Offer to draft the chosen angle

Ideation feeds writing. After presenting the angles, offer the next step:

> "Want me to turn one of these into a finished draft? Tell me the number and the
> format. If a dedicated skill fits the format (e.g. a blog article or LinkedIn
> post), I'll route you to it for a better result; otherwise I'll use the general
> text skill (`/long-tail-copy`)."

Do not auto-draft. Wait for the owner to choose.

## Step 5: Feedback

**Auto-store phase.** Before asking for feedback, review this run. For each
qualifying observation, append one tagged line to `.claude/learnings.md` (create
with the standard header if missing):

```text
[cc-content:content-ideation] <concise observation> — <YYYY-MM-DD>
```

Qualifies: angle preferences or constraints not already in any loaded context file
or `CLAUDE.md` (e.g. "owner dislikes contrarian theses", "always wants a customer-
story angle in the mix"); corrections the owner made; project-specific facts that
would change future ideation.

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

> "Do these angles work for you? Any corrections or notes for future ideation —
> or press Enter to finish."

- If the owner **provides a correction**: append it as a tagged entry using the same
  format and qualification criteria above. Confirm: "✓ N learning(s) saved to
  `.claude/learnings.md`."
- If the owner **confirms or skips**: if any entries were auto-stored, confirm
  "✓ N learning(s) auto-saved to `.claude/learnings.md`." Then exit. If nothing was
  stored, exit directly.
