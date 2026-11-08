---
name: communication-setup
description: "Set up, change or remove how Claude talks to you: a custom output style with your reply rules, a reminder of those rules on every message, and a Stop hook that quietly nudges Claude when a reply runs a little long and blocks one that runs far past your limit. Use when the user says Claude's replies are too long, exhausting, hard to skim, full of process narration or caveats, 'you make me work for the information', 'talk to me shorter', 'communication setup', 'set up how you talk to me'; when the length check or reply-length hook blocked a reply it shouldn't have, or the user wants a different limit or style; or asks to remove or undo it ('remove communication setup', 'go back to normal replies')."
---

# Communication setup

Memory notes and CLAUDE.md rules about tone fade in long sessions. This skill enforces them with three pieces, from weakest to strongest:

1. **An output style.** It goes into the system prompt and survives compaction, so it outranks CLAUDE.md. It sets the base voice.
2. **A reminder on every message** (UserPromptSubmit hook). It puts the rules next to each message the user sends, so they stay in view.
3. **A length check** (Stop hook). A block is jarring: the user sees the long reply, a hook message and then the rewrite. So it has two tiers. A reply a little over the limit (up to `hard_factor` times it, default 2) isn't blocked: the next message carries a quiet note to keep that reply shorter, and the user sees nothing. A reply far over is blocked once with a one-line reason, and the rewrite passes so it never loops. It skips `>` quoted drafts and code blocks, and allows any length when the user's message asks for depth ("explain", "details", "full").

Everything lives in `~/.claude` and applies to every project. `scripts/setup.py` (next to this file) installs and removes it. It backs up `settings.json` to `settings.json.bak` before every change, and it only touches its own entries.

## Replies from this skill

This skill is for people who find long replies tiring, so its own replies are the test. Every reply it sends is one or two lines: what happened, and at most one question. Don't explain how the hooks or tiers work, don't list what you checked, and don't offer extra changes nobody asked for (like renaming the config), unless the user asks. Two things are part of the job and always get said: offering to retire a hand-made hook or style that does the same thing, and the exact command when the sandbox blocks a write. An interview is the one reply that can run longer, because it carries the questions.

## Status

Run `python3 <skill>/scripts/setup.py status` and answer in one or two lines: whether it's on, and the line and word limit.

## Install or change

**1. Check what's there.** Run `python3 <skill>/scripts/setup.py status`. If it's installed, start from the current config at `~/.claude/communication-setup.json`.

**2. Interview, briefly.** If `~/.claude/settings.json` already has a hand-made length hook or an output style that does the same job, say so in this same message and ask whether to retire it once this is in, so the rules don't run twice. Then ask only what you can't infer from the conversation, all in one message:
- What tires them: length, process narration, caveats, too many questions, jargon, convoluted phrasing.
- The reply limit. The default is about 5 lines of prose: a quiet note past 8 lines or 120 words, and a block past twice that.
- Words that mean "go long" for them, in every language they use.
- One real reply of yours they found tiring, if there is one. It becomes the bad example.

**3. Write the config** to a temp file and show it to the user in a few lines before installing:

```json
{
  "name": "Ana",
  "style_name": "Ana",
  "description": "Short, answer-first replies in plain words for Ana, who skims.",
  "about": "Ana skims. Long replies tire her, and she ends up skipping them.",
  "rules": [
    "Answer first, in one or two lines.",
    "About 5 lines outside quoted drafts, unless she asks for depth.",
    "No narration of what you checked, ran or read. Only the result and what you need from her.",
    "No caveats she didn't ask for.",
    "Plain words, said the way you'd say them to a coworker.",
    "At most one question, at the end, yes/no when possible."
  ],
  "max_lines": 8,
  "max_words": 120,
  "hard_factor": 2,
  "depth_words": ["explain", "details", "full", "everything", "walk me through"],
  "example_bad": "a real tiring reply, trimmed",
  "example_good": "the same answer in two lines"
}
```

Only `style_name` and `rules` are required. Write the rules themselves in plain, short sentences: they are what Claude reads every turn.

**4. Install:** `python3 <skill>/scripts/setup.py install <config.json>`. Writing to `~/.claude/settings.json` from a sandboxed Bash needs the sandbox off for that one command.

**5. Tell the user** what changed, in two lines: the style name and the limit. Mention that the style applies from the next session, while the hooks apply right away. Mention that saying "remove communication setup" undoes it.

If they said yes to retiring a hand-made hook or style, remove its `settings.json` entry now (leave the file itself unless they asked), and say so in the same two lines.

## Remove

Run `python3 <skill>/scripts/setup.py remove`. It deletes its hooks, style and config, restores the output style the user had before the first install, and leaves every other hook alone. Then confirm in one line.

## Tuning

- **The hook blocks a reply that should have been long.** Add the user's word for it to `depth_words` and reinstall. Don't raise the limit for one case.
- **Replies are still long but under the limit.** Lower `max_lines` or `max_words`.
- **Blocks feel jarring.** Raise `hard_factor` (say to 3), so more overruns get the quiet note instead of a block.
- **Rewrites keep coming back long.** The Stop hook lets the second attempt through on purpose. Tighten the rules text instead of adding retries.

## Anti-patterns

- **Installing without showing the config.** The rules speak for the user, so the user approves them.
- **Long rules.** A rules list the user would find tiring to read defeats the point. Keep each rule to one plain sentence.
- **Counting drafts.** Drafts are what the user will send, so their length is the user's call. The hook already skips `>` quotes; keep drafts in them.

## Cross-references

- `/flagrare:write-docs`, "Say it plainly": the same plain-wording rule for documents.
- `/flagrare:editorial-pass`, which flags convoluted phrasing in documents.

## Evals

The cases live in `plugins/flagrare/evals/communication-setup/` (the eval runner refuses a folder inside `skills/`). Each run gets a throwaway home folder, so the install and remove cases never touch your real `~/.claude`. Run them from `plugins/flagrare`:

```bash
claude plugin eval . --tag communication-setup --scaffold --allow-tools Bash Write Edit --trust-plugin
```

Inside a run, the sandbox blocks writing `~/.claude/settings.json`, so the graders also accept a short, plain "the sandbox blocked it, run this command" reply.
