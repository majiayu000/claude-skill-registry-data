---
name: skill-improve
description: Read accumulated session logs for a skill, synthesize numbered improvement proposals with rationale and session evidence, collect conversational HITL approval, apply accepted changes to the SKILL.md, bump the patch version, and write a changelog entry. Use when you have enough session logs and are ready to improve a skill. Triggers on "/skill-improve", "improve the skill", "evolve the skill", "apply session learnings", "update the skill from session logs", or any phrase asking to apply accumulated friction logs to a SKILL.md.
version: 0.1.1
---

# Skill Improve

You are the evolver. Your job is to read what friction sessions have accumulated for a skill, synthesize that signal into concrete numbered proposals, get the author's approval on each one, and apply the accepted changes — updating the SKILL.md, bumping the version, and writing a changelog entry. Nothing is written until the author explicitly approves.

---

## Phase 1: Resolve the skill

The user invokes this as `/skill-improve <skill-name>` (e.g., `/skill-improve qa`). If they didn't provide a skill name, ask: "Which skill should I improve?"

This skill must be run from the skills repo — it edits SKILL.md files and writes changelogs that live there. Find the owning plugin:

```bash
ls plugins/*/skills/<skill-name>/ 2>/dev/null
```

- **One match** — record the plugin name.
- **No match** — you're not in the skills repo, or the skill name is wrong. Tell the user: "skill-improve must be run from your skills repo checkout — switch to it and try again. Available skills: `ls plugins/*/skills/`." Then stop.
- **Multiple matches** — ask the user to qualify: "Found `<skill-name>` in both `<plugin-a>` and `<plugin-b>` — which one?"

---

## Phase 2: Gather evidence

Read three things in parallel:

**1. Session logs**
```bash
ls ~/.claude/skill-sessions/<plugin>/sessions/<skill-name>/ 2>/dev/null
```
Read every file in that directory. If the directory doesn't exist or is empty — **check whether the user has referenced an alternative evidence file in the conversation** (e.g., a dev notes file, an ENHANCEMENTS.md, a one-off markdown document). If so, read from that path instead and state: "No standard session logs found — reading evidence from `<path>`." Apply the same synthesis and dedup logic. If no alternative source was mentioned either, tell the user: "No session logs found for `<skill-name>`. Run `/skill-reflect <skill-name>` after a few sessions first." Then stop.

After reading, print a one-line inventory before proceeding:
> "Found N session log(s) for `<skill-name>`: `<date-1>`, `<date-2>`, … Synthesizing proposals."
> (Or, if using an alternative source: "Reading evidence from `<path>`. Synthesizing proposals.")

**2. Current SKILL.md**
```bash
cat plugins/<plugin>/skills/<skill-name>/SKILL.md
```
Note the current `version:` value from the frontmatter.

**3. Existing CHANGELOG.md** (if present)
```bash
cat plugins/<plugin>/skills/<skill-name>/CHANGELOG.md 2>/dev/null
```
Read it to understand what has already been improved. Do not re-propose changes that were addressed in a prior improvement cycle.

---

## Phase 3: Synthesize proposals

Identify patterns across all session logs. A single log noting an edge case is weak signal; the same gap appearing across multiple sessions is strong signal. Weight your proposals accordingly.

For each distinct improvement opportunity, write a numbered proposal in this format:

```
**Proposal N: <short title>**
What to change: <specific section or instruction in the SKILL.md, described precisely>
Why: <rationale — what friction this addresses>
Evidence: <cite the session log(s) by date/filename that surfaced this>
```

Ground rules:
- Be specific. "Improve the instructions in Phase 2" is not a proposal. "Add a fallback step to Phase 2 that asks the user for the issue ID if it can't be inferred from the branch name" is.
- Don't pad. If only one improvement is clearly warranted, produce one proposal. Quantity is not a virtue.
- Cross-reference logs against the changelog. For each session log, check its "Proposed improvements" section against the CHANGELOG entries. If a specific proposal from that log was already addressed in a prior improvement cycle, skip that proposal — but still read the rest of the log for unresolved friction. Skip the proposal, not the log.
- If no CHANGELOG exists, read the current SKILL.md directly and filter any proposals whose substance is already present in the current text. Don't assume all proposals are new just because there is no changelog — the skill may have been improved informally before the evolver loop existed.
- Don't re-propose. If the CHANGELOG.md shows a previous cycle already addressed something, skip it even if a session log mentions it again.
- Separate concerns. If two distinct parts of the skill need fixing, make two proposals — don't bundle them. The author needs to be able to accept one and reject the other.

---

## Phase 4: Present and collect approval

Print all proposals clearly, then ask:

> "I found N proposals based on M session logs. Reply with which to accept, reject, or edit — e.g., 'accept all', 'accept 1 and 3, reject 2', or 'accept 1 but change the wording to…'"

Wait for the author's reply. Handle the full range of responses:

- **"Accept all"** — apply every proposal.
- **"Accept N and M, reject K"** — apply only the accepted ones.
- **"Accept N but change it to…"** — apply with the author's inline edit, not the original wording.
- **"Reject all" / "Cancel"** — stop. Print: "No changes made."

If the author's reply is ambiguous (e.g., "the first two look good"), confirm before writing: "To confirm: I'll apply proposals 1 and 2 and skip 3. Proceed?"

**Do not write anything to disk until you have explicit approval.**

---

## Phase 5: Apply accepted changes

Edit the SKILL.md to incorporate each accepted proposal. Apply them one at a time, in proposal order. Use the Edit tool — do not rewrite the whole file unless the changes require structural reorganization, in which case use Write and explain why.

---

## Phase 6: Bump the version

Read the current `version:` from the SKILL.md frontmatter (e.g., `0.3.0`).

- **Default: patch bump** (`0.3.0 → 0.3.1`) — for refinements, clarifications, added fallbacks, and new edge case handling that doesn't change the skill's overall shape.
- **Minor bump** (`0.3.0 → 0.4.0`) — for behavioral changes: new phases, removed phases, changed output format, different trigger conditions. Before applying a minor bump, ask: "This feels like a minor version bump (`0.3.0 → 0.4.0`) rather than a patch — the changes alter how the skill behaves, not just sharpen existing instructions. Agree?" Note: "Accept all" approves the *proposals*, not the *version category* — ask the minor-bump question separately even when the author already said "accept all."

Update the `version:` field in the SKILL.md frontmatter.

---

## Phase 7: Update the changelog

Write to `plugins/<plugin>/skills/<skill-name>/CHANGELOG.md`.

**If the file doesn't exist**, create it and seed it with two entries — one for the original version and one for the new version:

```markdown
# Changelog

## v<new-version> — <today's date>
**Sessions:** <N> (<comma-separated dates of logs that informed this cycle>)
**Changes:**
- <accepted change 1>
- <accepted change 2>

## v<original-version> — (initial release)
Initial version.
```

**If the file exists**, prepend the new entry above the first existing `## v` heading:

```markdown
## v<new-version> — <today's date>
**Sessions:** <N> (<comma-separated dates of logs that informed this cycle>)
**Changes:**
- <accepted change 1>
- <accepted change 2>

```

The "Sessions" line lists how many session logs were read and their dates — this is the audit trail connecting the changelog entry to the raw evidence.

---

## Phase 8: Confirm

Tell the author:

1. New version (e.g., `qa: 0.3.0 → 0.3.1`).
2. How many proposals were applied vs. total proposed (e.g., "2 of 3 applied").
3. Path to the changelog (e.g., `plugins/delivery/skills/qa/CHANGELOG.md`).

---

## What to skip

- Don't commit — the author commits when they're ready.
- Don't delete or archive **standard session logs** from `~/.claude/skill-sessions/` — they remain as raw evidence for future cycles. Non-standard evidence sources (dev notes, ENHANCEMENTS files, one-off markdown documents) are not subject to this rule; follow the user's instructions about those.
- Don't propose stylistic rewrites of sections that aren't broken — only fix what the sessions showed was broken.
- Don't update `plugin.json` version — that's a plugin-level release concern, not a per-skill improvement.
