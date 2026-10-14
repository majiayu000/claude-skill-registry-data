---
name: instagram-post
description: >
  Use this skill when the owner wants to write, draft, or generate an Instagram post or caption.
  Invoke when the user says "write an Instagram post", "create an Instagram caption", "draft for Instagram",
  "write for Instagram", "design an Instagram carousel", or "generate an Instagram Reel caption".
allowed-tools: Read, Write, Bash
argument-hint: "[optional: path to campaign briefing file]"
---

@./format-guidelines.md **Read when:** starting this skill
@../\_shared/storytelling-frameworks.md **Read when:** selecting a narrative framework in Step 5
@../\_shared/persuasion-principles.md **Read when:** selecting persuasion principles in Step 6

# Instagram Post Skill

You are helping the owner produce a complete, publishable Instagram post (feed caption,
carousel, Reel, or Story) that complies with the format guidelines in this skill folder,
reflects the company's brand voice, and — if a campaign briefing is present — serves the briefing's goals.

This skill is **language-, industry-, and audience-neutral**. It works for any output language and
any B2B or B2C context. Calibration happens through the loaded context files and the owner's topic
input.

## Step 0: Recall learnings

If `.claude/learnings.md` exists, read it silently. Apply all entries relevant to this run —
both `[cc-content:*]`-tagged entries and entries from other plugins that inform content quality or
project constraints. Do not announce this step. If the file is absent, continue normally.

## Step 1: Load context

Read the context table from all loaded CLAUDE.md files:

```bash
grep -A 200 '## Context files' CLAUDE.md 2>/dev/null || echo "(no context table)"
```

CLAUDE.md files may exist at multiple hierarchy levels (workspace root, project root, sub-directory).
The harness already loads all applicable ones into your context window. If multiple `## Context
files` tables exist, rows from more specific CLAUDE.md files take precedence over less specific ones.

**If no context table is found** in any loaded CLAUDE.md, ask once:

> "I don't see any context files registered. Would you like to:
> (a) Pause and run `/content-onboarding` to set up context
> (b) Continue without project context (output will be generic)"

Stop if (a); note "generating without project context" and continue if (b).

**If a context table exists**, read every file listed in the **File** column.

After loading, assess what each file covers by reading its **Summary** entry. Map the loaded files
to these content needs:

| Need                     | What to look for in the Summary                                  |
| ------------------------ | ---------------------------------------------------------------- |
| Brand voice              | Writing style, tone, vocabulary, phrasing rules, things to avoid |
| Organization background  | Who the company/author is, products, positioning, mission        |
| Target audience          | Reader personas, goals, challenges, job titles                   |
| Output language          | Default language, locale, or region                              |
| Instagram-specific rules | Content strategy, posting frequency, hashtag policies            |

**When multiple files plausibly cover the same need**, pick the one whose Summary best fits this
specific post. For example: if one file's Summary says "casual, behind-the-scenes personality" and
another says "formal, thought leadership only", and this post targets community building, load the
casual one and note the choice.

**Coverage gaps — flag these two:**

If no loaded file plausibly covers **brand voice**, ask once:

> "I don't see any writing style or brand voice context. Is this intentional, or should I pause
> while you run `/content-onboarding`?"
>
> - **Intentional**: note the gap; label the final output `⚠ DEGRADED OUTPUT — no brand voice context`
> - **Pause**: direct the owner to onboarding and stop.

Apply the same ask for **organization background** if no loaded file covers it.

For absent audience, language, or Instagram-specific rules: note silently and continue.

After loading and assessing, note which files were loaded and which needs each covers. Proceed to
Step 2.

## Step 2: Check for campaign briefing

Determine the briefing path:

1. If the owner passed a file path as an argument (`$ARGUMENTS`), use that path.
2. Otherwise, check for `brief.md` in the current working directory:

```bash
ls brief.md 2>/dev/null && echo "found" || echo "missing"
```

- **Found** (either via argument or `brief.md`): read the file and note its key messages, goals,
  and constraints. Confirm: "✓ Campaign briefing loaded from `<path>`."
- **Missing**: note "No campaign briefing found — generating from company context only." and
  continue.

## Step 3: Infer and confirm audience, goal, and post format

This is the content-production-specific step.

1. Use the loaded audience context and campaign brief (if any) to infer:
   - **Audience type**: B2B or B2C (or multi-audience)
   - **Content goal**: awareness, consideration, conversion, retention, advocacy, or education
     (from the goal variations in format-guidelines.md)
   - **Funnel stage**: TOFU, MOFU, or BOFU (if applicable)
   - **Audience expertise level**: novice, familiar, or expert
   - **Post format**: single-image (feed), carousel, Reels, or Stories (per Layer 1 post-format section)

2. If the loaded context genuinely does not support a confident inference, ask the owner the
   missing question directly rather than guessing.

3. Present a one-line inference summary to the user, for example:
   "Audience: B2B (SaaS) · Goal: lead generation · Stage: MOFU · Expertise: familiar · Format: carousel"

4. Ask the user to confirm or correct before generating. Do not silently apply assumptions.

5. Based on confirmed values, explicitly state which Layer 2 and Layer 3 variations from
   `format-guidelines.md` are being applied and why. For example:
   "Applying B2B expertise-signaling tone (Layer 2), consideration-goal carousel + problem hook structure (Layer 3),
   and middle-funnel sustained-engagement strategy (Layer 3)."

## Step 4: Ask for the post topic (if not provided)

If the owner has not specified a topic or goal for the post, ask:

> "What should this Instagram post be about? You can describe the topic, share a key message you
> want to convey, paste a rough note, or link to content you'd like promoted."

Wait for the answer, then proceed.

## Step 5: Select storytelling framework

Read `../_shared/storytelling-frameworks.md` and follow the selection process described there.
Apply the chosen framework as the structural spine of the caption.

## Step 6: Select persuasion principles

Read `../_shared/persuasion-principles.md` and follow its selection process. Pick 1–3 principles
that fit the post's goal and the reader's state, plus a pre-suasive opener strategy. Note the
choice in working notes (e.g., "Using **Specificity + Problem-agitation**, hook leads with a
concrete pain point, CTA is specific call-to-action").

## Step 7: Generate the Instagram post

Produce a complete Instagram caption that:

- **Opens with a strong hook** (grabs attention within 1–3 seconds per format-guidelines.md; for Reels, the hook must also work as on-screen text)
- **Fits the length target** for its format and goal (100–220 chars for awareness/Reels; 126–800 chars for consideration/carousel; see Layer 3 tables for other goals)
- **Contains one clear idea or call-to-action**
- **Hook does NOT start with an emoji** (emojis reserved for later natural pauses, 1–5 max depending on format)
- **Includes a singular CTA** if the goal extends beyond pure reach (e.g., "Save this post", "Tap the link in bio", "Share this with someone who needs it") — avoid generic bait prompts ("Comment YES")
- **Applies selected storytelling framework and persuasion principles**
- **Reflects tone and vocabulary** from loaded brand voice context and audience context
- **For post format:** if Reels, keep caption short and let the video carry the narrative; if carousel, assume reader will swipe and can handle longer/multi-part captions; if single-image, hook must stand alone within the truncation point (~125 characters Feed)
- **Hashtags: 3–5 max** (the platform now enforces a hard cap around 5), chosen for topical relevance over volume
- **Acknowledges format implications:** note whether this is feed/carousel/Reels/Stories and how the format choice serves the goal
- **If briefing is present**, the post must serve its stated goals and key messages

Internal verification checklist from `format-guidelines.md`:

- Hook grabs attention in first line (within 1–3 seconds, ideally under 125 characters for mobile truncation, ~55 for Reels)
- Hook does NOT start with emoji; for Reels, hook also appears as on-screen text
- Length appropriate for format and goal (see Layer 3 tables in format-guidelines.md)
- One idea per caption
- CTA is singular and easy to answer
- CTA is specific and save/send-oriented, not vague or generic bait
- Emojis: 1–5 max depending on format, placed at natural pauses (not in opening hook)
- Tone matches audience (B2B vs. B2C calibration)
- Hashtag count: 3–5, topically relevant
- Post format choice aligns with goal and funnel stage (per Layer 3)
- Content is native/original — no unaltered reposts or watermarked video
- Conversation-inviting element present (question, call for saves/shares, or community hook)

For every unmet item, revise the draft and re-check — do not present until
every item is satisfied or the failure genuinely cannot be fixed (e.g. missing
context), in which case surface it in the output rather than hiding it.

Present the output in a clearly delimited block showing the content and its character/word count:

```
─────────────────────────────────────────────
Instagram post draft
─────────────────────────────────────────────
<caption content>
─────────────────────────────────────────────
Character count: <N> / 2,200 max
Format: [single-image / carousel / Reels / Stories]
Hook visible before truncation: [yes / no — first 125 chars: <snippet>]
Goal: [goal from Step 3]
```

If output is degraded (brand voice or organization context missing), prepend:

```
⚠ DEGRADED OUTPUT — generated without: <list of missing context>
```

## Step 8: Feedback

**Auto-store phase.** Before asking for feedback, review this run. For each qualifying observation,
append one tagged line to `.claude/learnings.md` (create with standard header if missing):

```text
[cc-content:instagram-post] <concise observation> — <YYYY-MM-DD>
```

Qualifies: content preferences or constraints not already in any loaded `context/` file or
`CLAUDE.md`; corrections the owner made to the output; project-specific facts that would change
future output; accepted/rejected suggestions deviating from best practices.

Does not qualify: standard behavior applied without deviation; facts already in context files or
`CLAUDE.md`; anything derivable by re-reading context files; facts semantically equivalent to an
existing `.claude/learnings.md` entry under any plugin tag — when in doubt, skip; redundancy is
worse than a missed entry.

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

> "Did this post meet expectations? If you have any corrections or notes for future posts, share
> them here — or press Enter to finish."

- If the owner **provides a correction**: append it as a tagged entry using the same format and
  qualification criteria above. Confirm total entries written across both phases:
  "✓ N learning(s) saved to `.claude/learnings.md`."
- If the owner **confirms quality or skips**: if any entries were auto-stored, confirm
  "✓ N learning(s) auto-saved to `.claude/learnings.md`." Then say "Great — the post is ready to
  publish. Copy it above and paste directly into Instagram." and exit. If nothing was stored, skip
  the confirmation and exit directly.
