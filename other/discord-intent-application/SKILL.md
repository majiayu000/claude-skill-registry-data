---
name: discord-intent-application
description: Helps write the justification text for Discord Developer Portal privileged intent applications (Message Content, Server Members, Presence) for a specific bot. Takes a plain-text description of the bot's functionality and/or an uploaded/local codebase, screens the bot's features against Discord's known rejection triggers, and writes one txt file per needed intent containing the exact answer to paste into the "What do you need this intent for?" field. Only use this skill when the user explicitly asks for help with a Discord privileged intent application, an intent request/justification, or filling out the Discord developer portal's intent form — do not trigger this for general Discord bot coding, feature planning, or unrelated Discord questions.
---

# Discord Privileged Intent Application Writer

Writes the justification text Discord asks for when a bot developer requests a privileged
gateway intent (Message Content, Server Members, Presence) in the Developer Portal. The goal
is an application that gets **approved**: specific, minimal, tied to real shipped features,
and written so a reviewer with zero technical Discord/bot knowledge can follow it.

## Reference files

- `references/rules.md` — the user's own compiled rules for what makes an application succeed
  or fail. Read this in full before drafting anything. This is the authoritative source for
  tone, disqualifying use cases, and wording requirements.
- `references/alternatives.md` — paraphrased summary of Discord's official guidance on
  non-privileged alternatives (slash commands, context menus, components, modals, REST
  lookups) per intent. Use this to check whether a feature genuinely needs the intent at all.

Read both files before Step 2.

## Inputs

Gather whichever of these the user provides (ask only if genuinely missing/ambiguous — don't
block on it if there's enough to work from):

1. A plain-text description of what the bot does (required in some form).
2. Optionally, a codebase — a path, repo, or uploaded files. If code is available (this is
   most useful when running inside Claude Code with direct filesystem access), scan it for
   evidence of what the bot actually does with each intent, e.g.:
   - Message Content: handlers reading `message.content`, `.attachments`, `.embeds`,
     `.components`, `.poll`, prefix-command parsing (`!`, `?`, custom prefixes).
   - Server Members: intent flags being enabled, `on_member_join`/`on_member_update`/
     `on_member_remove` handlers, bulk member fetch/caching calls.
   - Presence: intent flags being enabled, `on_presence_update` handlers, code reading
     `status`/`activities`/`client_status`.
     Use this to confirm, correct, or fill gaps in the plain-text description — code is ground
     truth over a vague description, but don't assume every enabled intent flag reflects a real
     feature (developers often over-enable "just in case," which is itself a disqualifier).
3. Which intents to write for. If not stated, infer from the description/code which of the
   three intents the bot's real features actually touch.

## Workflow

### Step 1: Build a feature inventory

For each of the three intents, list the concrete, _currently shipped_ features that appear to
depend on it. Note the specific field/event each feature needs (e.g. "reads `message.content`
to detect a file extension," "needs `on_member_join` to assign an auto-role"). Discard
anything that's roadmap/future ("we plan to," "would also let us") — only what exists now.

### Step 2: Screen out disqualifying use cases

Check every feature in the inventory against `references/rules.md` section 2.1 (things
Discord has effectively pre-decided against): prefix commands as justification, moderation
that duplicates AutoMod, message logging/archiving/starboards-by-reading-everything, XP/
leveling from message content, feeding message content to an LLM or external service, presence
used for playtime/activity tracking or "online status" info commands, caching all members
"for performance," cross-server user profiling.

If a feature matches one of these patterns:

- Do not include it in the application text.
- Tell the user plainly which feature you're dropping and why (cite the specific pattern from
  the rules), rather than silently deleting it. If the user believes there's a genuinely
  distinct angle not covered by the pattern, discuss it before including anything.

### Step 3: Strip dilution, not just disqualification

Apply `references/rules.md` section 2.2 — these aren't rejection triggers by themselves, but
they weaken an otherwise-good application, so keep them out of the intent-specific answer:

- Features that don't need the intent at all (mentioning the music player in the Message
  Content justification, etc.) — those belong in the general bot description field, if
  anywhere, never in the per-intent field.
- Roadmap language.
- Requesting an intent with no concrete feature attached, or requesting all three when only
  some are load-bearing.
- Vague quantifiers ("all messages," "everything in the server") — rephrase to the narrowest
  true scope (which channels, which trigger, what's discarded/not stored).

### Step 4: Confirm no non-privileged alternative covers it

For every feature still standing, check it against `references/alternatives.md`. If a slash
command, context-menu command, component/modal, or a REST lookup (single-member fetch, member
search, basic user info, approximate online count) would accomplish the same thing, the
feature does not justify the intent — drop it and tell the user why, same as Step 2.

### Step 5: Draft the answer, per intent

For each intent that still has at least one surviving, genuine feature, write the answer text
using `references/rules.md` section 3 as the checklist:

- State the specific feature.
- State why it can't be built with an available alternative (name the alternative and the gap
  — e.g. "a slash command can't tell us when someone leaves the server").
- Give a concrete example of the feature benefiting a user.
- No vague statements, no unrelated features, no roadmap language.

**Tone (rules.md section 1):** casual but concise, written for a reviewer who knows nothing
about how Discord or bots work internally. Don't use terms like "gateway event," "payload," or
"opcode" without plain-English framing — explain what happens in normal words first.

**Wording layer test (rules.md section 2.3):** every sentence should be able to complete the
template "we need [intent] because [specific feature], and we can't use [alternative] because
[specific gap]." If a sentence can't be traced to that template, cut it — it's diluting, not
helping.

**Length:** keep each answer at or under 2000 characters (this is an assumed limit, not
confirmed against Discord's actual field — mention this to the user once if it's the first
time running the skill in the session, so they know to double check). Count characters before
finalizing and trim if over.

### Step 6: Show drafts, then save

Show each drafted answer to the user inline first if there's any ambiguity or a judgment call
you made (e.g. a feature you excluded, a scope you narrowed). Once confirmed (or if the
description was unambiguous enough to skip that check), save one file per applicable intent,
named exactly:

- `message_content.txt`
- `guild_members.txt`
- `presence.txt`

Only create files for intents that have a surviving justification — do not create empty or
placeholder files for intents the bot doesn't need. Save to the outputs directory and present
the files to the user.

## Notes

- This is a single-bot-per-run skill — no namespacing needed on filenames unless the user is
  clearly running it back-to-back for multiple different bots in the same session, in which
  case ask whether they want the files distinguished.
- If literally every feature for an intent gets screened out in Steps 2–4, tell the user the
  bot doesn't appear to have a valid justification for that intent right now, and don't
  produce a file for it — don't force a weak answer just to have output.
