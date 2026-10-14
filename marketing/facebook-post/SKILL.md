---
name: facebook-post
description: >
  Use this skill when the owner wants to write, draft, or generate a Facebook post.
  Invoke when the user says "write a Facebook post", "create a Facebook post", "draft for Facebook",
  "write for Facebook", or "generate a Facebook post".
allowed-tools: Read, Write, Bash
argument-hint: "[optional: path to campaign briefing file]"
---

@./format-guidelines.md **Read when:** starting this skill
@../\_shared/storytelling-frameworks.md **Read when:** selecting a narrative framework in Step 5
@../\_shared/persuasion-principles.md **Read when:** selecting persuasion principles in Step 6

# Facebook Post Skill

You are helping the owner produce a complete, publishable Facebook post for either a Page or a Group.
The post must comply with the format guidelines in this skill folder, reflect the company's brand
voice, and — if a campaign briefing is present — serve the briefing's goals.

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

| Need                    | What to look for in the Summary                                    |
| ----------------------- | ------------------------------------------------------------------ |
| Brand voice             | Writing style, tone, vocabulary, phrasing rules, things to avoid   |
| Organization background | Who the company/author is, products, positioning, mission          |
| Target audience         | Reader personas, goals, challenges, job titles                     |
| Output language         | Default language, locale, or region                                |
| Facebook-specific rules | Page vs. Group posting strategy, hashtag policies, CTA constraints |

**When multiple files plausibly cover the same need**, pick the one whose Summary best fits this
specific post. For example: if one file's Summary says "casual, fun — community content" and
another says "formal — thought leadership only", and this post targets a Group, load the casual
one and note the choice.

**Coverage gaps — flag these two:**

If no loaded file plausibly covers **brand voice**, ask once:

> "I don't see any writing style or brand voice context. Is this intentional, or should I pause
> while you run `/content-onboarding`?"
>
> - **Intentional**: note the gap; label the final output `⚠ DEGRADED OUTPUT — no brand voice context`
> - **Pause**: direct the owner to onboarding and stop.

Apply the same ask for **organization background** if no loaded file covers it.

For absent audience, language, or Facebook-specific rules: note silently and continue.

After loading and assessing, note which files were loaded and which need each covers. Proceed to
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

## Step 3: Infer and confirm audience and goal

This is the content-production-specific step.

1. Use the loaded audience context and campaign brief (if any) to infer:
   - **Audience type**: B2B or B2C (or multi-audience)
   - **Content goal**: awareness, consideration, conversion, retention, advocacy, or education
     (from the goal variations in format-guidelines.md)
   - **Funnel stage**: TOFU, MOFU, or BOFU (if applicable)
   - **Audience expertise level**: novice, familiar, or expert
   - **Platform channel**: Personal Profile, Professional Mode, Business Page, or Group —
     confirm this explicitly; format-guidelines.md now shows reach differs by an order of
     magnitude between these (Page ~1–6% vs. Group ~20–60% vs. Personal, highest)

2. If the loaded context genuinely does not support a confident inference, ask the owner the
   missing question directly rather than guessing.

3. Present a one-line inference summary to the user, for example:
   "Audience: B2B (SaaS) · Goal: lead generation · Stage: MOFU · Expertise: familiar · Channel: Business Page"

4. Ask the user to confirm or correct before generating. Do not silently apply assumptions.

5. Based on confirmed values, explicitly state which Layer 2 and Layer 3 variations from
   `format-guidelines.md` are being applied and why. For example:
   "Applying B2B expertise-signaling tone (Layer 2), consideration-goal educational structure (Layer 3), and Page-focused organic strategy (Layer 3)."

## Step 4: Ask for the post topic (if not provided)

If the owner has not specified a topic or goal for the post, ask:

> "What should this Facebook post be about? You can describe the topic, share a key message you
> want to convey, paste a rough note, or link to content you'd like promoted."

Wait for the answer, then proceed.

## Step 5: Select storytelling framework

Read `../_shared/storytelling-frameworks.md` and follow the selection process described there.
Apply the chosen framework as the structural spine of the post.

## Step 6: Select persuasion principles

Read `../_shared/persuasion-principles.md` and follow its selection process. Pick 1–3 principles
that fit the post's goal and the reader's state, plus a pre-suasive opener strategy. Note the
choice in working notes (e.g., "Using **Problem-agitation + Specificity**, opener leads with a
concrete pain point").

## Step 7: Generate the Facebook post

Produce a complete Facebook post that:

- **Opens with a strong hook** that stands alone within ~125–140 characters (mobile truncation)
- **Fits the length target** for its goal (under ~150 chars for awareness/conversion; 150–300 for
  consideration/education)
- **Contains one clear idea or call-to-action**
- **Uses 0–2 emojis** at natural pauses (if brand voice permits) and 0–3 hashtags only if they
  serve a specific campaign/event/location purpose (never as a discovery tactic)
- **Includes a singular CTA** if the goal is conversion or consideration (e.g., "Leave your answer
  below", "Watch the demo") — never an engagement-bait phrase ("Like if you agree", "Comment YES",
  "Tag a friend", "Share to win")
- **Applies selected storytelling framework and persuasion principles**
- **Reflects tone and vocabulary** from loaded brand voice context and audience context
- **Acknowledges channel reach dynamics:** Page posts reach ~1–6% of followers organically;
  Groups reach ~20–60% of members; Personal/Professional posts reach highest. Note this to the
  owner and, for Page posts with a conversion goal, suggest paid amplification or a
  founder/employee personal-profile share — not a Group cross-post, since Groups need
  community-appropriate framing decided at the channel-selection stage (Step 3), not a reach
  patch applied here
- **If the post includes a link**, place it directly in the post body (never hidden in the first
  comment as a reach workaround) and note the reach trade-off
- **If the post includes an image or video**, flag that alt text / captions should be added
- **If briefing is present**, the post must serve its stated goals and key messages

Internal verification checklist from `format-guidelines.md`:

- Hook grabs attention in first line and stands alone within ~125–140 characters
- Length appropriate for goal (under ~150 chars for awareness/conversion; 150–300 for
  consideration/education)
- One idea per post
- CTA is singular, easy to answer, and free of engagement-bait phrasing
- Emojis: 0–2 max; hashtags: 0–3 max and only if purposeful
- Tone matches audience (B2B vs. B2C calibration)
- Channel confirmed (Personal Profile / Professional Mode / Page / Group) and reach
  expectations set accordingly
- If Page post: note lower organic reach; recommend paid boost or a founder/employee
  personal-profile share if low reach is a risk for the stated goal
- If Group post: adjusted for community tone (peer-to-peer, less promotional)
- If link included: placed in the post body, not hidden in the first comment
- Conversation-inviting element present (question or call for input)

For every unmet item, revise the draft and re-check — do not present until
every item is satisfied or the failure genuinely cannot be fixed (e.g. missing
context), in which case surface it in the output rather than hiding it.

Present the post in a clear block:

```
─────────────────────────────────────────────
Facebook post draft
─────────────────────────────────────────────
<post content>
─────────────────────────────────────────────
Character count: <N> / 63,206 max
Platform: [Page / Group]
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
[cc-content:facebook-post] <concise observation> — <YYYY-MM-DD>
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
  publish. Copy it above and paste directly into Facebook." and exit. If nothing was stored, skip
  the confirmation and exit directly.
