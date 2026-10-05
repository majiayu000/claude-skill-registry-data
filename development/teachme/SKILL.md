---
name: teachme
description: Run a closing concept-retro at the end of substantive Claude Code sessions to catch concept-gaps before they become invisible black boxes. Trigger automatically near the end of any session where you introduced a protocol, library, architecture pattern, or tool the user hadn't specified or clearly already known — even if the user doesn't ask for it. Do NOT trigger for sessions that were pure syntax lookups, small tweaks, or used only concepts already logged in the Knowledge-base concepts/ dir. If unsure whether a session was "substantive," lean toward running it — a skipped trivial retro costs nothing, a missed real one lets a black box slip through.
model: claude-sonnet-4-6
---

# Concept Retro

## Why this exists

The user works fast with agents and is fine delegating implementation detail — syntax, boilerplate, exact API calls. What he is NOT fine losing track of is *concepts*: protocols, architectures, libraries, or tradeoffs that got introduced into a decision without him knowing the vocabulary existed to question it. That's the actual black-box risk, distinct from "I'd have to look up the syntax myself."

This skill is the closing checkpoint that catches the second kind before it accumulates silently.

## When to run

Automatically, near the end of a session, if — and only if — the session introduced at least one concept-level thing the user likely didn't already know: a new protocol, a new library/framework, a non-obvious architecture choice, a new tool/service, a security or infra pattern, etc.

Skip it when:
- The session was pure syntax/tedium (e.g. "fix this regex", "rename these variables")
- Every concept touched is already logged in `concepts/` (check first — see below)
- The session was trivial / very short

Don't wait to be asked. If genuinely unsure whether something counts as "new," err toward including it — better to over-log slightly than let a gap through.

## What to do

1. **Check for prior entries first.** Entries live in the `rahulc810/Knowledge-base` repo, at
   `/storage1/Documents/code/Knowledge-base/concepts/` — one file per concept, named
   `dd-mmm-day-concept-slug.md`. Skim existing entries so you don't re-log something already covered — if a
   concept reappears, that's a signal worth a short note (see step 4), not a full new entry.

   It is a git repo: run `git -C /storage1/Documents/code/Knowledge-base status --short` first, and leave the
   new entry **staged but uncommitted** unless the user says otherwise — commit strategy is theirs. Never push.

2. **Identify what's new.** Review the session and list concepts, protocols, tools, or architectural choices that:
   - Weren't specified by the user
   - Aren't things you have clear evidence the user already knows
   - Are conceptual (not just unfamiliar syntax for something the user already understands)

3. **For each one, write an entry** in this format:

   ```
   ## [YYYY-MM-DD] <Concept name> — <project/repo>
   **What it is:** one or two plain-language sentences, no jargon-on-jargon.
   **Why here:** why this session/agent chose it over alternatives.
   **Alternative:** what else could have been used and the tradeoff.
   **Related concepts and Further reading:** Where do go from here.
   ```

   Keep each entry tight — a paragraph, not a tutorial. The goal is enough to recognize and reason about the term later, not to teach it from scratch.

4. **If a concept reappears** (already in the file from a prior session), instead of a full new entry, append a one-line note under the existing entry: `- [YYYY-MM-DD] came up again in <project>` — this is the signal that it's crossed from "one-off" to "worth actually learning properly."

5. **Mention it briefly to the user** at the end of your session summary — one line, e.g. "Logged 2 new concepts to Knowledge-base/concepts/: MQTT, and the pub/sub broker pattern." Don't dump the full entries into chat; the file is the record.

## What NOT to log

- Syntax the user could look up in 10 minutes (specific function signatures, exact flag names, language features)
- Anything the user explicitly specified or clearly directed ("use MQTT" — they named it, no gap there)
- Pure implementation detail with no conceptual weight (variable naming, formatting choices)

The filter is always: *would not knowing this term stop the user from even asking the right question?* If yes, log it. If it's just "I'd have to Google the exact syntax," skip it.