---
name: ak-journal
description: "Write chronological technical journals that preserve work history without replacing current docs or ADRs."
when_to_use: "Invoke for session reflection or change analysis."
category: workflow
keywords: [journal, reflection, changes, session]
argument-hint: "[topic or reflection]"
metadata:
  author: agentkit
  version: "1.3.1"
---

# Journal

Capture a concise technical journal for the current session, then persist it with the first-class CLI.

Journals are work history under `<project>/plans/journals/`. They are not durable product or decision authority — record lasting decisions in the project's ADR or current docs owner.

## Workflow

1. Gather the important events: root cause, key changes, impacts, decisions, and next steps.
2. Draft a short title and body (markdown). Prefer concrete errors, paths, and outcomes over vague summaries.
3. Persist with the CLI (scriptable; no `$EDITOR`):

```bash
ak journal create "<title>" --summary "<one-line summary>" --stdin <<'EOF'
## What happened
...

## Decision
...

## Next steps
...
EOF
```

Optional flags: `--date YYYY-MM-DD`, `--project <registry-name>`.

4. Validate when needed:

```bash
ak journal validate <slug-or-filename-stem>
```

5. AgentWiki publish from this skill is **deferred**. Report `AgentWiki publish skipped` and keep the local file as the source of truth.

6. Browse existing entries with `ak journal list` / `ak journal show <slug>`, or the Journals page in desktop/dashboard.

**Optional:** Invoke the `journal-writer` subagent when emotional honesty and failure archaeology are the point of the entry; still persist through `ak journal create`.

## Naming

Created files use `YYYY-MM-DD-<slug>.md` with `-2`, `-3`, … collision suffixes.

## Workflow Position

**Typically follows:** `/ak-cook` (journal after implementation), `/ak-fix` (journal after bug fix)
**Related:** `the engineer ship skill` (journal after shipping, engineer tier)
**Terminal skill** — no typical successor.

## Journal step — opt-out

## Automatic vs explicit invocation

Explicit `/ak-journal` and `ak journal create` are always available and are
unaffected by any preference or flag.

The **automatic** journal step at the end of the `ak-plan`, `/ak-cook`,
`/ak-fix`, `ak-ship`, and `ak-bootstrap` skills honors:
- The `--skip-journal` flag on the invoking skill.
- The `journal.auto` config preference (default: `true`).
  Set with: `ak config prefs set journal.auto false` (or `true` to re-enable).

Precedence when a workflow decides whether to run the automatic step: flag >
project config > user config > default (`true`). When the automatic step is
skipped, workflows print one line so the intent stays visible in output:
- `journal skipped by --skip-journal` (flag), or
- `journal skipped by preference` (config).

## Local or social

Local journal creation is the default. Load `references/social-publishing-workflow.md` only
when the user explicitly requests social publishing or social media. A configured channel
or key is not publication authorization. Preview the exact target/content and require a
provider receipt before claiming a post succeeded. Local journaling calls no publisher.

Reuse `journal.auto` already resolved by the calling workflow in this session; resolve it
only if missing or configuration changed. Explicit journal invocation remains unaffected.
