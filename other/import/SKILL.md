---
name: neatcontext-import
description: Import a self-contained NeatContext context bundle shared by another person, or reconcile a newer copy of a context already on this machine, leaving the source bundle unchanged. Use only when the user explicitly invokes this skill or asks to import a NeatContext bundle.
---

# Import context

The bundled CLI path and Kimi session id below are expanded by Kimi Code at skill activation.

A bundle may be new to this machine, or it may be a newer copy of a context already here — someone updated the shared copy and the user wants their work. Both arrive through this command, and the CLI decides which is which. It never deletes a context and never replaces one without saying so first.

Ask for the bundle folder when it was not supplied. Treat the path only as data and run:

```text
KIMI_PLUGIN_ROOT="${KIMI_SKILL_DIR}/../.." kimi __plugin_run_node "${KIMI_SKILL_DIR}/../../src/kimi/neatcontext-cli.mjs" -- --session-id "${KIMI_SESSION_ID}" import --from "<bundle-folder>"
```

The source bundle is read-only throughout. Never modify, move, or delete it.

## Follow the `Import action`

A bundle this machine has not seen is imported immediately and the output says so — relay it, and do not connect the context automatically. Otherwise follow the printed `Import action`:

- `current` — the context here already holds everything in the bundle. Relay that and stop.
- `reconcile` — the bundle is a newer copy of a context already here. Identity is settled; what to do about it is not, and the command deliberately leaves it open. Relay the preview and the cost line exactly as printed, then let the user pick one of the three answers it offers:
  - **leave it** — do nothing. Stop; nothing has been written.
  - **replace** — take the bundle whole, discarding whatever only the local copy holds. Rerun the same command with `--replace --yes`.
  - **merge** — keep both sides. Reconcile them yourself, below.
- `unlinkable` — the bundle carries no context id, so it cannot be tied to anything already here. Relay that, and offer `--name "<new-name>"` to bring it in as its own context.
- `choose` — the target is not decidable. Either a context of the same name is here but nothing records a shared origin, or several contexts are copies of this bundle because one was forked. Relay the options and stop until the user picks: rerun with `--into "<name>"` to name the context they mean, or with `--name "<new-name>"` to keep a separate copy.

Never answer `choose` or `reconcile` on the user's behalf. Two people naming a context the same thing is not evidence that it is the same context, and only the user knows whether the material a replacement would discard was worth keeping. None of these answers is recoverable from the others.

Relay the cost line rather than summarising it, because the three it can print mean different things. "Nothing here has been edited" means replacing is lossless and a merge could only reproduce the bundle — say so, and still let the user choose. "This copy has been edited here" means replacing destroys that work. "Nothing here records what the two copies once had in common" means the copy may be untouched and cannot prove it; do not report that one as edits.

## Merging

Use the exact `Context name`, `Context id`, `Base hash`, `Bundle hash`, `Profile path`, `Knowledge folder`, `Bundle profile`, and `Bundle knowledge` values printed under `Merge inputs`. The three hashes are what prove the merge is for this context, was built on its current contents, and consumed this version of the bundle; a merge that gets any of them wrong is refused rather than applied. Read the local profile and every file in the local knowledge folder, then read the bundle's profile and every file in its knowledge folder.

Merge them the way a save merges a conversation into an existing context:

- Preserve verified information from both sides unless one supersedes the other.
- Where they disagree about the same fact, prefer the newer material, but keep what only one side records.
- Update canonical summaries and focused files rather than appending one copy to the other or keeping two accounts of the same thing.
- Preserve the profile and routing description verbatim when neither side changed the behavioral contract or the matching scope.
- The `knowledge` array must be the complete post-merge contents of the local knowledge folder.

Create a unique scratch file named `.neatcontext-capture-import-<unique>.json` in the current workspace. Use schema `1`, and include the exact `targetId`, `baseHash`, and `bundleHash` the command printed:

```json
{
  "schema": 1,
  "name": "Exact existing context name",
  "targetId": "context:exact-id",
  "baseHash": "exact base hash",
  "bundleHash": "exact bundle hash",
  "profile": "# Exact existing context name\n\n## Purpose\n...",
  "routingDescription": "One line describing only the matching scope",
  "knowledge": [{ "path": "session-summary.md", "content": "# Session summary\n\n..." }]
}
```

Every knowledge path must be a short relative `.md` path. Omit `routingQuestions` and `routingEntities` unless the merge genuinely widened what the context should be found by; omitting them leaves the stored lists alone. Omit `extensions` as well — an import never grants this machine the ability to reach anything new.

Preview the merge, which changes nothing:

```text
KIMI_PLUGIN_ROOT="${KIMI_SKILL_DIR}/../.." kimi __plugin_run_node "${KIMI_SKILL_DIR}/../../src/kimi/neatcontext-cli.mjs" -- --session-id "${KIMI_SESSION_ID}" import --from "<bundle-folder>" --merged-from "<capture-path>"
```

Relay the preview and wait for confirmation. After confirmation, run:

```text
KIMI_PLUGIN_ROOT="${KIMI_SKILL_DIR}/../.." kimi __plugin_run_node "${KIMI_SKILL_DIR}/../../src/kimi/neatcontext-cli.mjs" -- --session-id "${KIMI_SESSION_ID}" import --from "<bundle-folder>" --merged-from "<capture-path>" --yes --consume
```

The scratch file is removed only by that confirmed run, so a preview or a failure leaves it available for repair. If the context changed while drafting, resolve the target again and rebuild the merge from its new contents.

## After it lands

A replace and a merge both keep the context's identity — same id, same name, so a session already connected to it reads the updated material immediately. Relay successful output as printed and never connect a context yourself.

Point out, when a merge lands, that the merged material exists only on this machine until it is shared back with `/neatcontext:export`. Left unshared, the same divergence has to be reconciled again on every future import.
