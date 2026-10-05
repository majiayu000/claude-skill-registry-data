---
name: handoff
description: Compact the current conversation into a handoff document another session or agent can resume from. Use when wrapping up with unfinished work, when context is getting long, or when the user says "hand this off", "write a handoff", or "save state for the next session". Produces a single Markdown file at a durable, harness-agnostic path and reports it. Does NOT continue the work itself; it only captures state so a fresh session can.
argument-hint: "What will the next session be used for?"
---

# Handoff

A handoff is a single Markdown document that lets a fresh session, on any agent or
harness, resume this work without re-reading the whole conversation.
Capture the current *state* and the *next move*, not a transcript.

## What to capture

Keep it short and skimmable.
Include only what the next session actually needs:

- **Goal** — what we are trying to achieve, in a sentence or two.
- **State** — what is done, what is in progress, what has not been started.
- **Next step** — the single most concrete thing to do next.
- **Key decisions** — choices already made and *why*, so they are not relitigated.
  Attribute each one: confirmed by the user, an agent assumption (say so), or
  recorded elsewhere (link the PR/ADR/doc). Ideas only discussed are not
  decisions; they belong under open questions.
- **Open questions and gotchas** — blockers, risks, and anything surprising.
- **Where to resume** — the exact files, paths, commands, or URLs to pick up from.
- **Previous handoff** — if this session resumed from one, link it rather than
  re-summarising it; each re-synthesis loses fidelity and provenance.
- **Suggested skills** — the skills the next session should invoke, by name.

Do not duplicate content already captured in other artefacts (PRDs, plans, ADRs,
issues, commits, diffs).
Reference them by path or URL instead.

Redact secrets and personal data — API keys, tokens, passwords, PII. The
document lands in a durable, greppable directory and outlives the session, so
anything leaked into it persists.

If the invocation included a focus (arguments or an accompanying instruction),
tailor the document to it.

## Saving the document

Save to a durable, harness-agnostic location, then report the full path back to the
user so both they and the next session can open it:

```sh
dir="${HANDOFF_DIR:-$HOME/handoffs}"
mkdir -p "$dir"
path="$dir/handoff-$(date +%Y%m%d-%H%M%S).md"
echo "$path"
```

If the goal or the invocation arguments suggest a short topic slug, insert it
before the timestamp — `handoff-<slug>-YYYYMMDD-HHMMSS.md`; the plain timestamp
form is the fallback.
Write the document to that path and print it as the final step.

`$HANDOFF_DIR` lets any environment redirect handoffs without editing the skill.
The default keeps them out of your project repos, survives reboots and temp-directory
cleanup, and names them so they sort chronologically and are easy to find and grep.

## Credits

Derived from Matt Pocock's MIT-licensed `handoff` skill
([github.com/mattpocock/skills](https://github.com/mattpocock/skills)); upstream
licence in [LICENSE-upstream](./LICENSE-upstream).
