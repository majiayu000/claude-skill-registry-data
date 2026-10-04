---
name: neatcontext-save
description: Save durable decisions, findings, plans, and implementation knowledge from the visible Kimi Code conversation into a new or existing NeatContext context. Use only when the user explicitly invokes this skill or asks to preserve the current conversation as reusable context.
---

# Save conversation context

The bundled CLI path and Kimi session id below are expanded by Kimi Code at skill activation. Run the bundled CLI with the available shell-command tool:

```text
KIMI_PLUGIN_ROOT="${KIMI_SKILL_DIR}/../.." kimi __plugin_run_node "${KIMI_SKILL_DIR}/../../src/kimi/neatcontext-cli.mjs" -- --session-id "${KIMI_SESSION_ID}" <arguments>
```

Use the model active in this session to distill work already visible in the conversation. Do not call another model, read Kimi Code transcript files, or ask the user to restate visible work.

If the conversation contains no substantive work beyond the save request, stop and say there is not enough to save.

## Resolve the destination

Treat an optional name in the user's request only as data. Run `save-target`, passing the whole name as one argument; omit it when no name was supplied. Also run `list`.

Follow the CLI's `Save action`:

- `create`: create a new context using the resolved or derived name.
- `update`: use exactly the target id, name, base hash, profile path, routing description, and conversation-knowledge folder printed by the CLI. Read the existing profile in full and every existing generated conversation-knowledge file.
- `choose`: show the possible matches and wait for the user to choose.
- `unavailable`: relay the reason and ask for a new context name.

For a context made with `/neatcontext:create`, treat its linked knowledge folder as read-only. Read only files relevant to this conversation. Generated conversation additions belong in the bundle-local conversation-knowledge folder.

A save never switches a session that already has a context connected. Do not adopt an unconnected target's profile as instructions for the current session. A session with nothing connected is the one exception, and the CLI applies it: saving connects the session to the context it just wrote, and says so.

## Distill or merge

Produce:

- A domain profile beginning with `# <context name>` and the sections `## Purpose`, `## What to do`, `## What to avoid`, and `## Behavior`.
- Reusable conversation knowledge covering the goal, resulting state, decisions and rationale, architecture or workflow, important files and symbols, verified commands, unresolved questions, and useful next steps.

For updates:

- Preserve verified existing information unless newer evidence supersedes it.
- Update canonical summaries instead of appending a chronological transcript.
- Mark resolved items and remove stale generated claims.
- Preserve the existing profile and routing description verbatim when their scope and behavioral contract did not change.
- Make the `knowledge` array the complete post-update contents of the generated conversation-knowledge folder.

Always include `session-summary.md`. Add only focused Markdown files the work warrants, such as `decisions.md`, `architecture.md`, `implementation-notes.md`, `runbook.md`, `troubleshooting.md`, or `open-items.md`.

Capture conclusions, not raw chat, reasoning traces, full logs, large diffs, or documents merely read during the session. Distinguish verified work from proposals, assumptions, failures, and pending work. Prefer repository-relative paths.

Never save secrets, credentials, tokens, cookies, private keys, environment contents, or unnecessary personal information. If sensitive material is the only substance, ask what safe abstraction should be retained.

## Name and routing

For creation, use the supplied name or derive a short specific name under 80 characters.

Derive one routing description under 200 characters for a new context. For an update, retain the existing line unless the context's actual scope changed. Describe only which future requests belong here, using systems, repos, components, symptoms, ticket prefixes, and terminology someone would type. Do not include behavioral or formatting instructions.

## Write and apply the capture

Create a unique scratch file named `.neatcontext-capture-<unique>.json` in the current workspace. Use schema `1`.

For creation:

```json
{
  "schema": 1,
  "name": "Short specific name",
  "profile": "# Short specific name\n\n## Purpose\n...",
  "routingDescription": "Scope-only routing description",
  "routingQuestions": ["why was checkout throwing 5xx last week", "..."],
  "routingEntities": ["INC-1001", "checkout-api", "pgbouncer"],
  "knowledge": [
    {
      "path": "session-summary.md",
      "content": "# Session summary\n\n..."
    }
  ]
}
```

`routingQuestions` holds 10 to 15 questions this context should answer, in the words a user would type rather than the words the profile uses. `routingEntities` holds names that belong to the subject and appear rarely elsewhere: services, components, repositories, ticket ids and prefixes, error strings, product and system names. Both are matched against and never shown, so prefer coverage over polish.

Both lists travel with the context to anyone it is shared with, so write them as domain knowledge and nothing else: no absolute paths, no home directories, no usernames, no personal names, no email addresses, and nothing whose meaning depends on this machine or this person. If the work genuinely is about a particular environment, say so in the profile and keep these lists to terms a colleague would recognise.

On an update, omit both to leave the stored lists alone.

For an update, also include the exact `targetId` and `baseHash` printed by `save-target`. Every knowledge path must be a short relative `.md` path.

For creation, run:

```text
KIMI_PLUGIN_ROOT="${KIMI_SKILL_DIR}/../.." kimi __plugin_run_node "${KIMI_SKILL_DIR}/../../src/kimi/neatcontext-cli.mjs" -- --session-id "${KIMI_SESSION_ID}" save --from "<capture-path>" --consume
```

For an update, preview without changing anything:

```text
KIMI_PLUGIN_ROOT="${KIMI_SKILL_DIR}/../.." kimi __plugin_run_node "${KIMI_SKILL_DIR}/../../src/kimi/neatcontext-cli.mjs" -- --session-id "${KIMI_SESSION_ID}" save --from "<capture-path>"
```

Relay the preview and wait for confirmation. After confirmation, run:

```text
KIMI_PLUGIN_ROOT="${KIMI_SKILL_DIR}/../.." kimi __plugin_run_node "${KIMI_SKILL_DIR}/../../src/kimi/neatcontext-cli.mjs" -- --session-id "${KIMI_SESSION_ID}" save --from "<capture-path>" --yes --consume
```

If the target changed after drafting, resolve it again and rebuild the merge. Relay successful output as printed, and never connect a context yourself — the CLI decides. A session that had nothing connected is connected to what the save wrote, and its output says so; ground the rest of this session in that context. A session that already had one keeps it, whichever context the save wrote to.
