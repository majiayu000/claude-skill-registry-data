---
name: braindump
description: Fast capture of unstructured, stream-of-consciousness thoughts. Classifies the domain, extracts entities (people/projects), and writes an AI-first note to 00-inbox/. Use when the user says "braindump", "I have an idea", "note this", "capture this", or shares a stream of thoughts with no clear structure.
---

# Skill: Braindump

## When to activate

- The user explicitly says: "braindump", "brain dump", "capture", "note this".
- The user shares an unstructured stream of thought (>2 ideas in one message).
- The user explicitly wants to "get this out of my head".
- At the start of a morning session: "here's what's on my mind today".

**Do NOT use braindump when:**
- It's a meeting or a transcript → use `meeting-ingest`.
- It's a question or a request for analysis → just answer normally.
- It's a decision to make → use `challenge-decision`, then log in `05-decisions/`.

## Preflight

1. **Read `_CLAUDE.md`** at the vault root (AI-first rules, structure, conventions) and
   `00-inbox/MY-PROFILE.md` (working language, active domains, knowledge domains).
2. **Get the real timestamp** from an available tool, or ask the user the time if unavailable.
3. **List existing notes** in `02-people/` and `03-projects/` so you can detect references.

## Process

### Step 1 — Collect

If the user hasn't given the content yet, ask: "What's on your mind?" Accept any
format (short, long, raw voice-to-text, any language, mixed). **No judgment, no
filtering at this stage.**

### Step 2 — Domain classification

Detect the domain automatically. Confirm with the user if ambiguous:

- **professional**: work, team, processes, organizational change.
- **personal**: family, health, side projects, personal life.
- **project-specific**: if you identify an existing project in `03-projects/`.
- **mixed**: cross-cutting.

### Step 3 — Entity extraction

Parse the braindump to identify:

- **People mentioned**: proper names, role descriptions ("the PM in Spain").
  - For each, fuzzy-match against `02-people/*.md`.
  - Match → wikilink `[[02-people/First Last]]`.
  - No match but a clear name → offer to create a stub.
  - Vague description → flag for clarification.

- **Projects mentioned**: project names, initiatives.
  - Fuzzy-match against `03-projects/*.md`.
  - Same logic: wikilink or stub.

- **Concepts / entities / tools / teams / jargon**: any *thing* mentioned in the braindump
  that warrants its own page in your personal wiki — wikilink to `06-knowledge/<slug>.md`.
  If the page doesn't exist, **create a wiki stub** following the Wiki stub protocol in
  `.claude/skills/knowledge-build/SKILL.md` (Mode A.2): `type: wiki`, `needs-review: true`,
  `domain: <inferred>` (from braindump domain / tags / MY-PROFILE knowledge-domains; else
  `unsorted`), `created-from` set to this braindump, with a 1-line snippet from the
  braindump in the `## Sources` section. No recurrence threshold — first mention is enough.
  After creating, **call curator incremental** (Mode C.1) to route the new page into its
  domain hub.

### Step 4 — Light analysis (do NOT over-analyze)

Generate at most ONE paragraph:
- **Main insight**: one sentence capturing the essence.
- **Tension / open question**: what's unresolved.
- **Suggested follow-up**: one concrete action if obvious (else skip).

⚠️ **Anti-pattern to avoid**: don't overload the braindump with analysis. This is
a capture, not an essay.

### Step 5 — Generate the note

**Path**: `00-inbox/YYYY-MM-DD-HHMM-<slug>.md`

The `<slug>` is 3–5 kebab-case words summarizing the content (e.g.
`onboarding-script-friction`).

**Required format:**

```markdown
---
date: YYYY-MM-DD
type: braindump
tags: [braindump, <domain-tag>, <topic-tags>]
domain: professional|personal|project-specific|mixed
energy: low|medium|high
related-people: ["[[02-people/...]]"]
related-projects: ["[[03-projects/...]]"]
ai-first: true
---

## For future Claude

[2-3 sentences: what was captured, why it was noted, temporal context. English.]

## Raw content

[The user's braindump, cleaned for spelling/punctuation BUT not rewritten. Keep
the tone, the hesitations, the "not sure if...". This is raw material.]

## Insight

[One sentence max — the essence of what was said.]

## Tension / Open question

[What's unresolved, if applicable. Otherwise skip this section.]

## Links

- People: [[02-people/...]], [[02-people/...]]
- Projects: [[03-projects/...]]
- Concepts: [[06-knowledge/...]]

## Suggested follow-up

- [ ] [Concrete action if obvious; task-roundup will add a ^t-id and pull it into TODO.md]
```

### Step 6 — Propagation

1. **Daily note**: append a link to this braindump in `01-daily/YYYY-MM-DD.md`
   under the `## Braindumps of the day` section. Create the daily note if missing
   (with `type: daily` frontmatter).

2. **Stubs**: for each wikilink to a non-existent note, create the stub:
   - Persons → offer (then `people-update`).
   - Projects → simple stub.
   - `06-knowledge/<slug>` → **wiki stub** per the protocol above (created silently with
     `needs-review: true` — no need to ask).

3. **People updates**: if a person note exists and the interaction is
   significant, offer to invoke `people-update` to log it.

### Step 7 — Report

End with a short recap:

```
✓ Braindump captured: 00-inbox/2026-05-20-1432-onboarding-script-friction.md
✓ Daily note updated
→ 2 references detected: [[02-people/Alex Rivera]] (exists), [[03-projects/Onboarding Refresh]] (new, stub created)
→ Suggestion: invoke people-update for Alex? (significant interaction)
```

## Anti-patterns to avoid

❌ **Over-analyzing** — a braindump is not an essay. Stay light.
❌ **Rewriting the raw content** — keep the raw material, it's precious for future-you.
❌ **Creating people without confirmation** — always ask before a new person note.
❌ **Skipping wikilinks** — every referenced entity MUST be a wikilink, even a stub.
❌ **Orphan note** — today's daily note MUST link the braindump.
❌ **More than 5 tags** — be minimal.
❌ **Fabricating dates** — always use the real timestamp from preflight.

## Full example

**User input:**
> "saw the onboarding team is struggling with the new tier-1 qualification script,
> Alex flagged that agents make mistakes on edge cases, maybe we need to revisit
> the training. We touched on it in standup but nobody really dug in. I wonder if
> it's because we accelerated the rollout without enough piloting."

**Output (note created):**

```markdown
---
date: 2026-05-20
type: braindump
tags: [braindump, professional, training, qualification-script]
domain: project-specific
energy: medium
related-people: ["[[02-people/Alex Rivera]]"]
related-projects: ["[[03-projects/Qualification Script V2]]", "[[03-projects/Onboarding Refresh]]"]
ai-first: true
---

## For future Claude

This braindump captures a concern (2026-05-20) about training gaps in the
onboarding team following the rollout of the new tier-1 qualification script.
Alex Rivera flagged edge-case errors. The user suspects insufficient piloting
during an accelerated rollout. No formal action yet — raised informally in standup.

## Raw content

Saw the onboarding team is struggling with the new tier-1 qualification script,
Alex flagged that agents make mistakes on edge cases, maybe we need to revisit the
training. We touched on it in standup but nobody really dug in. I wonder if it's
because we accelerated the rollout without enough piloting.

## Insight

Accelerated rollout of the qualification script V2 + training not adapted to edge
cases → field friction not formally surfaced.

## Tension / Open question

Is this a training problem or a script-design problem? Hypothesis to challenge
before investing in a training redesign.

## Links

- People: [[02-people/Alex Rivera]]
- Projects: [[03-projects/Qualification Script V2]], [[03-projects/Onboarding Refresh]]

## Suggested follow-up

- [ ] Targeted 1-1 with Alex to dig into the concrete edge cases
- [ ] Check whether the pattern shows up in other teams too
```

## User preferences

Adapt to the preferences in `00-inbox/MY-PROFILE.md` and `_CLAUDE.md`. Typical defaults:

- **Concise and direct** — no introductory fluff.
- **No corporate-speak.**
- **MVP 98%** — if info is missing, ask ONE question max, otherwise proceed.
- Accept any working language, but the "For future Claude" preamble is always English.
