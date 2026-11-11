---
name: auto-improve-database-guard-install
description: "Tell the database guard of the agentic-auto-improve plugin which databases in this project are protected: finds the database names this project's tracked configuration files use, shows each with the file and line that names it, asks which to protect (and whether a Testing-environment database exists), and appends only those names to the project's rules file. Appends only, never removes a name; on a first install it says plainly that the guard then stops writes only to the listed databases and asks a separate yes or no. Prints the server-trigger line and its install command for a person to run. The name carries the plugin name because you may have several plugins installed. Use when: user says /auto-improve-database-guard-install, 'protect my databases', 'tell the database guard my database names', 'the database guard has no list', or 'add a database to the protected list'. Never edits a .sql file, never runs a database command, never removes a name."
user_invocable: true
---

# /auto-improve-database-guard-install — name the databases the guard protects

The database guard refuses destructive or writing commands aimed at the databases listed under
`protected_databases` in **this project's** `.claude/hooks/db-destructive-guard.rules.json`. No copy of
the guard names a database. This skill puts your project's real database names into that file.

```
/auto-improve-database-guard-install
   propose -> one confirmation of the names -> (first install only: one yes or no on the narrowing)
           -> append the names -> print the server-trigger line for a person to run
```

It reads and touches only `agentic-auto-improve`'s rules file in this project.

## The rule that shapes everything here

**The skill carries the conversation. The script carries every rule.**

What counts as a valid name, which names are disposable, how the file is appended to, and what
changes between the preview and the apply all live in `auto_improve_finish_install.py protect-databases`,
which has its own test suite. Read its answer. Do not work any of it out yourself.

The script **only appends**. It never removes, reorders or respells a name, never reads or writes
`production_path_allowlist` or `human_only_commands`, never edits a `.sql` file and never runs a
database command. Only a person removes a protected name, by merging a pull request by hand.

## Step 0: Find the script

Test these places **in this order** and keep the first hit (do not `ls` all three: `ls` sorts its operands).

```bash
FI=
S=.claude/scripts/auto_improve_finish_install.py
if [ -f "$S" ]; then FI=$S
elif [ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -f "$CLAUDE_PLUGIN_ROOT/$S" ]; then FI=$CLAUDE_PLUGIN_ROOT/$S
else
  # What Claude Code recorded for this plugin (this project's entry, then the user entry), then the newest cache folder by version number.
  CFG=${CLAUDE_CONFIG_DIR:-$HOME/.claude}
  ME=$(printf %s "$CLAUDE_PROJECT_DIR" | tr 'A-Z\134' 'a-z/' | tr -s /)
  REC=$(tr -d '\r\n' 2>/dev/null < "$CFG/plugins/installed_plugins.json" | grep -o '"agentic-auto-improve@[^"]*" *: *\[[^]]*]' | grep -o '{[^{}]*}' | tr '\134' / | tr -s /)
  MINE=$(printf '%s\n' "$REC" | grep '"scope" *: *"project"' | while IFS= read -r O; do
    P=$(printf %s "$O" | sed -n 's/.*"projectPath" *: *"\([^"]*\)".*/\1/p' | tr 'A-Z' 'a-z' | tr -s /)
    [ -n "$ME" ] && [ "${P%/}" = "${ME%/}" ] && printf '%s\n' "$O"
  done)
  NEWEST=$(ls -d "$CFG"/plugins/cache/*/agentic-auto-improve/*/ 2>/dev/null | sed -n 's|^\(.*/\([0-9][0-9.]*\)/\)$|\2 \1|p' | sort -rV | cut -d' ' -f2-)
  FI=$({ printf '%s\n' "$MINE"; printf '%s\n' "$REC" | grep '"scope" *: *"user"'; } | sed -n 's/.*"installPath" *: *"\([^"]*\)".*/\1/p' | { cat; printf '%s\n' "$NEWEST"; } | while IFS= read -r D; do
    [ -n "$D" ] && [ -f "${D%/}/$S" ] && { printf '%s\n' "${D%/}/$S"; break; }
  done)
fi
py -3 "$FI" --help   # macOS and Linux: python3 "$FI" --help
```

**If `FI` is empty, stop and say so.** Say the script was not found in the project, in `$CLAUDE_PLUGIN_ROOT` or in the
plugin cache, then stop. Pick the launcher once: `py -3` on Windows, `python3` on macOS and Linux. Below it is `PY`.

**Exit codes.** `0` is a plan, an apply or nothing to do. `2` is a refusal you can correct. `3` is an environment
problem (the guard file cannot be loaded, the project is unreadable). On `2` or `3`, read `code` and `message`, tell the
user the reason in one plain sentence, and stop. A refusal always means nothing was changed.

## Step 1: Preview

```bash
$PY "$FI" protect-databases --project . --json
```

Read the JSON. Show the user:

- `current-list`: the names protected today (empty means every database is protected, see Step 3).
- `proposals`: each database name found in a **tracked** configuration file with the `Database=` or `Initial Catalog=`
  connection-string form, with `evidence` (the file and line). A name with `already-protected: true` is on the list
  already (letter case ignored).
- `excluded`: names that carry a disposable suffix, or `tempdb`, each with its reason. They are never proposed: a
  disposable name is meant to be dropped, so it can never be protected.

Never guess a name. Never add a name the user did not confirm.

## Step 2: Ask for the names, and only the names

Ask **one** question that lists the proposals and asks which of them to protect. The user may also name a database you
did not find. This skill asks for database names and nothing else.

Then ask whether this project has a **Testing-environment database** (for example the database an integration test
suite runs against). Add one **only when the person names it.** Never invent a companion name such as `<Name>_Testing`.

A name must be 1 to 128 letters, digits and underscores, not starting with a digit. The script refuses anything else
(`name-invalid`) and refuses a disposable name (`name-is-disposable`).

Say this plainly, before you write anything:

> Only a database whose name carries an allow-listed disposable suffix (`_DryRun`, `_MigrationVerify`, `_Sandbox`,
> `_Scratch`, `_Throwaway`, `_Test_<hex>`, `_E2E_<hex>`, `_Temp_<hex>`), an in-memory SQLite database, or `tempdb` may be
> dropped. Nothing on the protected list can be.

## Step 3: First install: the narrowing

Run the preview again with every confirmed name, **passing the names at preview time too**, because the plan hash
covers them:

```bash
$PY "$FI" protect-databases --project . --json --name <Db1> --name <Db2>
```

If `narrows_write_protection` is `true`, the project has no list yet. Right now the guard stops writes to **every**
database, and after this change it stops writes only to the listed ones. Print `narrowing-statement` exactly as the
script gives it, then ask a **separate** yes-or-no question that names this change. Do not fold it into the question
about the names. Pass `--confirm-narrowing` to the apply **only** on a yes. On a no, stop; nothing is written.

When `narrows_write_protection` is `false` the list already protects something and the change only adds, so there is
nothing to confirm and no `--confirm-narrowing`.

## Step 4: Apply

Show the `unified-diff` and ask one confirmation of the names. On a yes:

```bash
$PY "$FI" protect-databases --project . --json --name <Db1> --name <Db2> --apply --expect-sha256 <plan-sha256> [--confirm-narrowing]
```

`plan-sha256` is the one the preview printed. `changed-since-preview` means the file or the names changed: preview
again. `nothing-to-do` means every name was already listed.

## Step 5: Print the server-trigger line and the install command

The script prints `server-trigger`: the `IN (...)` list the workstation-wide SQL Server trigger needs, and the install
command. Print both to the user. Mark the command:

> **A person runs this once per workstation, from PowerShell or cmd.**

Never run it yourself, never edit the `.sql` file, never run a database command. The trigger is the layer that refuses
database-drop events at the server, and it keeps its own list.

## Step 6: Say what happens next

Say, in one sentence each:

- The names are in the working copy of the rules file now. They become the protected **default-branch list** only once
  a pull request carrying them merges. Until then another branch does not hold them.
- From then on no branch can shorten the list: the Protected-name check compares each rules file with the default
  branch's at turn end, in `/verify-before-done` and at the contract landing. Only a person removes a name, by changing
  only the rules file in its own pull request and merging it by hand.

## Refusals

| Code | Exit | Meaning |
|---|---|---|
| `rules-unreadable` | 2 | The rules file is not strict UTF-8 JSON without a byte order mark or duplicate key, or `protected_databases` is not a list of strings. A person repairs it. |
| `name-invalid` | 2 | A name is not 1 to 128 letters, digits and underscores starting with a letter or `_`. |
| `name-is-disposable` | 2 | The guard's own disposable pattern matches the name: it can never be protected. |
| `changed-since-preview` | 2 | The file or the names changed after the preview. Preview again. |
| `narrowing-unconfirmed` | 2 | The change narrows write protection and `--confirm-narrowing` was not given. |
| `write-failed` | 2 | A symbolic-link rules file, or an operating-system error. Nothing was written. |
| `plugin-source-checkout` | 2 | This is the plugin's own checkout. |
| `project-unreadable` | 3 | The project cannot be read. |
| `guard-unreadable` | 3 | The guard file cannot be loaded to read its disposable patterns. |

## Do not

- Add a name the user did not confirm, or a Testing database the user did not name.
- Remove, reorder or respell a name, or touch `production_path_allowlist` or `human_only_commands`.
- Edit a `.sql` file or run the install command or any database command.
- Set `CLAUDE_DESTRUCTIVE_DB_OK` or any other override.
- Ask the narrowing question as part of another question.

## When NOT to use

- To finish the project profile or register hooks: use `/auto-improve-finish-install`.
- To remove a protected name. Only a person does that, in a pull request of its own that changes only the rules file.
- Inside the plugin's own checkout. The script refuses it as `plugin-source-checkout`.
