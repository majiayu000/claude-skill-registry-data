---
name: app-configuration
description: "Use when configuring an app, CLI, or skill stack."
version: 1.0.0
author: Charles Ponti
license: MIT
metadata:
  author: ponti-studios
  category: Software Development
  tags:
    - configuration
    - secrets
    - cli
  hermes:
    tags: [configuration, secrets, cli]
    related_skills: [subsystem-removal, kernel-dev-build]
---

# Application configuration

One precedence rule, one parser, one file. Configuration that works "somehow" is the same
configuration that fails on the next machine and cannot be explained.

## When to use

- Adding or changing how an app, CLI, script, or skill reads its settings.
- A value is found in more than one place, or the code "negotiates" where to look.
- Secrets are being added to a project (API keys, tokens, license keys).
- An agent's skill stack is installed, updated, or found drifting from the repo it came from.

Not for: build tooling flags, or library options passed as function arguments.

## The rule

```
explicit flag  >  environment variable  >  one user config file  >  built-in default
```

Nothing else is consulted. No `.env`, no per-tool config file, no chain of candidate paths, no
"if not found, try the old location". Each added source is a question a future reader has to ask.

## Procedure

1. **Pick one file and one location.** `~/.<product>.yml` or `$XDG_CONFIG_HOME/<product>/config.yml`,
   overridable by a single variable (`STUDIO_CONFIG`), and nothing else. Print the resolved path in
   the error message when a value is missing, so the answer to "where do I set this?" is one line.
2. **Write one parser, and import it.** Put it in the module every consumer already imports. If a
   consumer cannot import it (a skill with no `node_modules`, a preload that runs before the app),
   move the parser to the shared library that consumer _can_ import — do not copy it into the consumer.
   Two copies diverge silently: the day one grows a fix, the other keeps the old behaviour and the
   difference only shows up on the machine that took the other branch.
3. **Validate at load, once.** A schema (zod or hand-written) at the parse boundary, with the same
   error shape everywhere, so a bad value fails at boot rather than at the call site.
4. **Expand `~` wherever a path starts**, including after a scheme prefix — `file:~/x` is a path.
5. **Resolve secrets lazily.** A command that only prints configuration, or a `--dry-run`, must not
   require a key. Resolve at first use, not at module scope.
6. **Delete dead keys everywhere, not just in code.** Schema key, env mapping, test fixture, the
   user's own config file, and the docs. A key nothing reads still looks supported, so the next
   person sets it and wonders why nothing happens.

## Secrets

- The environment first, then the config file. If the key lives in the file, ship it `0600` and warn
  on load when it is group- or world-readable.
- Never echo a key in a log, an error, or a test fixture; read it once and pass it down.
- **Match the credential shape the protocol expects before debugging the endpoint.** SigV4 storage
  wants a 32-character Access Key ID plus a 64-character secret; a dashboard "API token", or a
  token's ~34-character `ID…` identifier, fails on the first request with a length error that reads
  like a server fault. Read the length in the message as a shape problem, not a connectivity problem.
- A checked-in `.env` is a secret leak waiting for a `git add -A`. An env file that only exists on one
  machine is worse: it makes "works for me" the normal state.

## The skill stack is a copy, not a source

An installed skill follows the same rule as a config value: one source, one installer, and no second copy that can drift. Six failures, all silent, all found by diffing rather than by anything going red:

- **Install with the installer, never by hand.** `npx skills add <repo> --skill <name> -g --yes` writes the store (`~/.agents/skills/<name>`) and wires every agent's link itself. A hand-made symlink, or a `muse skills install` copy under `~/.config/muse/skills/`, is a second behaviour: it loads, and no update reaches it.
- **The installer's lock file is the only provenance.** `~/.agents/.skill-lock.json` records source, hash and date per skill. Installed directories minus lock keys is exactly the set `npx skills update -g` skips — silently, indefinitely. `Source: local` in `npx skills list -g` is not a location; it means _no record at all_. Re-add each from its repo to restore both the record and the update path.
- **The installed copy is a copy.** An edit there is overwritten by the next update, and a repo edit is not what loads until you reinstall. The copy can also be _ahead_ of the repo when an agent edited it mid-task — fold that edit back into the source first, commit, then reinstall, or the reinstall deletes it.
- **`skills add` overlays, it does not replace.** Files the new version dropped survive the update, so a copy can match no version that ever existed. Use `npx skills remove -g -s <name> -y` — one name per invocation, because `-s a,b` exits 0 and removes neither — then add, when an install must match the repo exactly.
- **One name, one tier.** A real directory at `<agent-home>/skills/<category>/<name>/` (`<agent-home>` = your agent runtime's home dir) plus an installed entry of the same name collide: both resolve to the same path, `skill_view` refuses the pair, and the runtime still lists the skill as available. Keep the installed copy and delete the loose directory.
- **Audit instead of trusting.** `node scripts/skills_audit.mjs` in the kernel library reports all of it — unprovenanced install, stale lock entry, name collision, installed copy ≠ repo, comparing logical trees so a vendored `references -> ../../data` symlink is not mistaken for drift — and exits non-zero on any finding. Schedule it (a launchd `StartCalendarInterval` entry running the script with `--quiet` is enough): every one of these faults is invisible until someone diffs.

**Removing one.** Uninstalling is the same inventory problem run backwards, and the binary is rarely the whole thing:

- **A runtime manager holds three parts — the installed version, the shim, and the declaration that reinstalls it.** `mise uninstall <tool>` drops only the version; the `tool = "…"` line in `~/.config/mise/config.toml` brings it back on the next `mise install`. Delete the declaration, uninstall, remove `~/.local/share/mise/shims/<tool>`, then `mise reshim`.
- **A shim that survives the uninstall is a second install, not debris.** Run it and read its own error: `… is provided by node@24.18.0, node@26.5.0` names every runtime still holding the package. npm-global packages live per node version, so delete `<runtime>/lib/node_modules/<pkg>` and `<runtime>/bin/<tool>` for each one listed — `npm ls -g` on the _active_ version reports nothing because it is not the version that has it.
- **Sweep every agent store for the skill that documents the removed tool** (`<agent-home>/skills`, `~/.claude/skills`, `~/.agents/skills`, `~/skills`, `~/.codex/skills`, `~/.gemini/skills`, `~/.gemini/config/skills`). The copies are real directories, not links, so each needs its own `rm -rf`; afterwards grep `.skill-lock.json` and the agent's config for stale entries.
- **Read each candidate before `rm -rf`.** A short tool name is a bad search term — `pi` also matches `pip`, `api` and `pipeline-*`, so a sweep returning five hits is not evidence they are all the target. Confirm from the contents and report the ones you rejected.
- **One supported path, not two switchable ones.** A second runtime, backend or parser kept behind a config flag still has to be validated, documented, tested and kept in step with the first, and the failure mode when its dependency is gone is a claim that dies at run time. When only one is used, delete the other and make validation refuse the retired value, so a stale config fails at load with a sentence instead of later with a stack trace.
- **Archive each source set to its own path.** Two `tar czf "$T"` runs sharing one `$T` leave only the second archive while both report success: give every source set its own filename, then `tar tzf` it and count entries before deleting the originals.
- **A git worktree is removed by git, not `rm -rf`.** Run `git worktree remove --force` from the parent repo; a hand delete leaves `worktrees/` metadata pointing at a path that no longer exists. Archive the worktree's untracked files first (the removal discards them) and leave the branch ref alone so unmerged commits survive.

**Merging two peers into one.** Two skills enforcing one authority is the same duplication as two parsers. Read both, pick the spine whose ordering already reflects what is most often got wrong, fold the other's rules into it merging restatements into the rule they duplicate, renumber and repair every internal cross-reference, carry the reference files across unchanged. Before deleting either name, `search_files` the whole library for both — `related_skills`, the catalog manifest, README prose and other skills' notes all break silently, and the validator only catches `related_skills`. Then one commit swaps the catalog entries, the validator proves parity, and `skills remove` (per name) plus `skills add` reinstate the survivor.

## Verification

Prove the precedence with three runs, not one:

| Setup                          | Expect                                            |
| ------------------------------ | ------------------------------------------------- |
| only the config file           | the file's value is used                          |
| file plus an exported variable | the variable wins                                 |
| neither                        | the built-in default, and the command still works |

Then delete the file and run again — a tool that cannot start without its config file has a default
problem, not a config problem.

## Pitfalls

- **A `.env` that silently shadows the file.** With both present, the env file wins and every edit to
  the YAML appears to do nothing. Remove the duplicate source rather than documenting the order.
- **Mid-string `~` is not a path expansion.** A parser that handles a leading `~` and nothing else
  produces `file:~/db.sqlite`, which the driver reads as a relative path — the app then fails with a
  database error that says nothing about configuration.
- **A second parser is a second behaviour.** Two readers of the same file will disagree on comments,
  quoting, or `~`, and the disagreement surfaces as "it works in the CLI but not the app".
- **Validation that returns defaults hides typos.** An unknown key that is quietly ignored is fine;
  a known key with an invalid value that silently falls back is not.
- **A dry run that demands a credential is a broken verification path.** It teaches everyone to skip
  the dry run, so the cheap check stops happening.
