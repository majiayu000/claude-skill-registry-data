---
name: "HUD: Profiles"
description: "Show the profiles stored in the dossier and persona stores"
when_to_use: "When Jason wants to see who's recorded in the dossier or persona stores, look up a specific person or persona or check whether a real colleague has a derived persona linked to them."
model: sonnet
effort: low
metadata:
  glyph: ᛊ
  family: hud
disable-model-invocation: false # read-only viewer, no gate needed
disallowed-tools: ["Edit", "Write", "NotebookEdit"]
allowed-tools: ["Bash(python3 \"$HOME\"/.claude/library/scripts/profiles.py:*)"]
arguments: ["action", "store", "modifier"]
argument-hint: "[list [dossier|personas] [full|short] | count [dossier|personas] | show <name>] (no args = usage)"
---

# HUD: Profiles

Two stores, one schema, one viewer: `library/profiles/dossier/` (real colleagues, gitignored) and `library/profiles/personas/` (invented or persona-derived adversarial readers, tracked). See `library/profiles/README.md` for how they relate. This skill never writes to either: it prints to the terminal and stops.

## Parsing `$ARGUMENTS`

- **No arguments**: go to "No arguments" below.
- **First token is `list` or `count`**: that action. An optional second token `dossier` or `personas` scopes the store (default both). `list` takes an optional third token `full` or `short` (default `short`).
- **First token is `show`**: `show <name>` (name is the next token).
- **Anything else** (one bare token, no recognised verb, e.g. `/hud-profiles max`): treat it as `show <that token>`. A bare name defaults to showing that profile; this is the only implicit default this skill takes, and it exists because "look someone up" is the common case.

## No arguments

Do not run anything. Print tersely and stop:

```
Usage: /hud-profiles list [dossier|personas] [full|short]
       /hud-profiles count [dossier|personas]
       /hud-profiles show <name>
```

No script call, no counts, no listing. If Jason wants counts he'll ask for `count`; printing a full listing on a bare invocation spends tokens on output that might not be wanted.

## Action: `count`

```bash
python3 ~/.claude/library/scripts/profiles.py count --store <dossier|personas|both>
```

Bare `count` (no store token) requests both and is fine to run directly: it's cheap, two lines of output. Print the result as-is.

## Action: `list`

```bash
python3 ~/.claude/library/scripts/profiles.py list --store <dossier|personas|both> --format <short|full>
```

Default store is `both`, default format is `short` (slugs only, one per line, no description). `full` adds `id`, `description`, `quickFacts`, `isRealPerson`, `pronouns`, `linkedProfileIds`, `scope` per profile, never the nine stance fields (`needs` through `verdict_style`); those stay reserved for `show`. Print the output under headed sections per store when both are shown.

## Action: `show <name>`

```bash
python3 ~/.claude/library/scripts/profiles.py get <name> --store both
```

`<name>` resolves as a slug or an `id` (`profiles.py get` tries both). This call checks both stores at once, so a name present in both prints both sections it returns.

Otherwise:

- **Found in dossier only**: print the profile. If `linkedProfileIds` names a persona (by `id`), follow it: run `get <id> --store personas` and print that too, dossier first, so the source and its derived reader model sit together. Flag if the linked persona's own `updated` is newer than the timestamp recorded in the dossier's `linkedProfileIds` entry (a drift the derivation hasn't caught up with yet).
- **Found in personas only**: print the profile. If `linkedProfileIds` names a dossier entry (by `id`, e.g. `DOS005`), that id alone carries no name: do not attempt to resolve it to "complete the picture"; that is exactly the identity resolution the id and the tracked/gitignored split exist to prevent. Note the link exists (`derived from a real colleague's review pattern`) without resolving or printing the dossier side unless that same id was already the direct subject of this same `show` call.
- **Found in neither**: say so plainly. If the CLI's own "not found" message came back, relay it; do not guess at a near match: that's `/dossier-record`'s job for the dossier side, not this skill's.

## Red flags

**Never** print `linkedProfileIds` from a persona file and then separately fetch and print the dossier entry it names, unless that dossier entry was already the direct subject of this same `show` call. Chaining persona → dossier automatically is exactly the identity resolution the tracked/gitignored split exists to prevent. Chaining dossier → persona is fine and intended: the dossier already names the persona's id, nothing new is revealed by following the link forward.

**Never** write anything. If Jason wants to record a fact, that's `/dossier-record`. If a persona needs deriving, that's `red-doc`/`red-branch`'s Step 1c in `library/references/red/methodology.md`.

<raw-arguments value="$ARGUMENTS" />
