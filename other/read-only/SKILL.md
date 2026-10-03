---
name: read-only
description: Add a curated set of read-only permission rules -- file reads, directory listings, content search (grep/glob), git inspection, and system checks -- to a Claude Code settings.json allowlist so safe reads stop triggering permission prompts. Local read-only by default; outbound reads (WebFetch, WebSearch, registry lookups) and secret-bearing reads (env dumps) are offered only as explicit opt-ins. Trigger when the user says "read-only", "/read-only", "pre-approve read operations", "allow all read-only commands", "stop asking me about ls/cat/grep", or asks to add safe read permissions to a settings file. Do not use for write or install permissions, or for mining transcripts to find which commands actually prompt most -- route those to a dedicated settings or transcript-analysis skill (e.g. update-config, fewer-permission-prompts) when one is installed.
---

# Read-Only

Add a known-safe catalog of read-only permission rules to a Claude Code settings file in one pass: merge into the existing JSON, never clobber, never touch `deny` or `ask`, and confirm exactly what was added.

## Step 1 -- Pick the target file

If the user named a scope, use it. Otherwise ask once, recommending the first option:

1. **User global** `~/.claude/settings.json` (Recommended) -- approve once, benefit in every project. Broadest convenience, broadest blast radius: the catalog is low-risk, not zero-risk (see the redirection caveat in Step 4), so users who work in sensitive repos may prefer option 3.
2. **Project shared** `.claude/settings.json` -- committed; teammates inherit it.
3. **Project personal** `.claude/settings.local.json` -- this machine, this repo only; smallest blast radius.

In a non-interactive context (no user available to answer), default to `.claude/settings.local.json` -- smallest blast radius.

## Step 2 -- The catalog

Rule syntax: bare `Tool` allows the whole tool; `Bash(cmd:*)` is a prefix match; `Bash(cmd)` is an exact match. Exact matches are used below wherever the command's *flags* can mutate (e.g. `git branch -d`).

### Core native tools (always add)

```
"Read", "Glob", "Grep"
```

These cover file reads, directory/pattern listings, and content search natively. If the user wants reads scoped (e.g. exclude secrets), offer path forms like `"Read(./src/**)"` instead of bare `"Read"`, and remind them `deny` rules such as `"Read(./.env)"` always win over `allow`.

### File and directory inspection (always add)

```
"Bash(ls:*)", "Bash(cat:*)", "Bash(head:*)", "Bash(tail:*)",
"Bash(wc:*)", "Bash(file:*)", "Bash(stat:*)", "Bash(tree:*)",
"Bash(du:*)", "Bash(df:*)", "Bash(diff:*)", "Bash(realpath:*)",
"Bash(dirname:*)", "Bash(basename:*)", "Bash(pwd)",
"Bash(shasum:*)", "Bash(md5:*)"
```

### Search (always add; `find` is opt-in)

```
"Bash(grep:*)", "Bash(rg:*)", "Bash(fd:*)", "Bash(ag:*)"
```

`Bash(find:*)` is **opt-in with a stated caveat**: `find` supports `-delete` and `-exec`, which mutate. A prefix rule cannot see mid-command flags, so allowing `find:*` allows those too. Offer it, name the risk in one line, and add it only if the user accepts.

### Git inspection (always add)

```
"Bash(git status:*)", "Bash(git log:*)", "Bash(git diff:*)",
"Bash(git show:*)", "Bash(git blame:*)", "Bash(git shortlog:*)",
"Bash(git describe:*)", "Bash(git ls-files:*)", "Bash(git rev-parse:*)",
"Bash(git grep:*)", "Bash(git reflog:*)", "Bash(git ls-tree:*)",
"Bash(git rev-list:*)", "Bash(git diff-tree:*)", "Bash(git merge-base:*)",
"Bash(git cat-file:*)", "Bash(git config --list)", "Bash(git config --get:*)",
"Bash(git config --global --get:*)", "Bash(git remote -v)",
"Bash(git stash list)", "Bash(git branch)", "Bash(git branch -a)",
"Bash(git branch -vv)", "Bash(git tag)", "Bash(git tag --list:*)",
"Bash(git worktree list)"
```

Deliberately exact (not `:*`) for `branch`, `tag`, `stash`, `remote`, `config`: their prefix forms reach mutating subcommands (`git branch -d`, `git tag v1`, `git stash pop`, `git remote add`, `git config user.name x`).

Prefix matching is strict about *flag order*: `Bash(git config --get:*)` does not match `git config --global --get user.name`, which is why the `--global --get` variant is its own rule. If a read-only git command still prompts later, the cause is usually a flag appearing before the matched prefix -- add that exact variant rather than widening to `git config:*`.

### System and environment inspection (always add)

```
"Bash(which:*)", "Bash(type:*)", "Bash(whoami)", "Bash(id)",
"Bash(uname:*)", "Bash(hostname)", "Bash(date)", "Bash(uptime)",
"Bash(ps:*)", "Bash(sw_vers)"
```

`date` and `hostname` are exact because their argument forms can mutate (set the clock, rename the host). `env` and `printenv` are deliberately *not* here -- they are read-only but secret-bearing; see the opt-in list below.

### Optional add-ons (offer, do not add silently)

The default catalog above is **local** read-only. Everything in this list crosses one of two extra lines -- it sends data *outbound* or it can expose *secrets* -- so each item is added only on explicit opt-in, with its risk named in one line when offered.

- **Environment variable reads**: `"Bash(env)"`, `"Bash(printenv:*)"` -- read-only but secret-bearing: the environment commonly holds API keys and credentials, and pre-approving the dump removes the permission gate that would otherwise flag an unexpected read.
- **Web reads**: `"WebFetch"`, `"WebSearch"` -- outbound: they send query/URL content to external services.
- **Package listings**: `"Bash(npm ls:*)"`, `"Bash(pip list)"`, `"Bash(pip show:*)"`, `"Bash(brew list:*)"`, `"Bash(composer show:*)"` (local); `"Bash(npm view:*)"` (outbound -- queries the npm registry).
- **Data inspection**: `"Bash(jq:*)"`, `"Bash(yq:*)"`, `"Bash(sort:*)"`, `"Bash(uniq:*)"`, `"Bash(cut:*)"`.
- **Project-specific read CLIs** the user mentions (e.g. wp-cli: `"Bash(wp post list:*)"`, `"Bash(wp option get:*)"`). Add only the read verbs (`list`, `get`), never the bare tool prefix.

Deliberately **excluded** from every tier: `echo`, `printf`, `sed`, `awk`, `tee`, `xargs`, pagers (`less`, `more` -- interactive). The first group writes trivially (redirection or `-i`); `xargs` executes arbitrary commands.

## Step 3 -- Merge and write

1. Read the target file. If it does not exist, start from `{}`. If it exists but is not valid JSON, stop and report -- do not "fix" a broken settings file as a side effect.
2. Add rules to the allowlist array the file *already uses*. The current schema is `permissions.allow`; if the file instead has a legacy or root-level allow key (e.g. `allowedTools`), append to that existing array rather than introducing a second list the harness may ignore. Only create `permissions.allow` fresh when no allowlist exists at all. Preserve every other key untouched, including `deny` and `ask`.
3. Append catalog rules **not already present**. Dedupe by exact string; also skip a rule when an existing broader rule obviously covers it (e.g. `"Bash(git:*)"` present means skip all git rules -- note this in the confirmation rather than narrowing their rule).
4. Settings files are plain JSON: no comments, no trailing commas. Validate before saving (`python3 -m json.tool` or `jq .`); write only if validation passes.

## Step 4 -- Confirm

One compact block: the file path, count added, count skipped as already covered, and any opt-in caveats accepted. Then state the one honest limitation of the whole approach:

> Prefix rules match the start of the command, so an allowed read can still write via shell redirection (`cat a > b` matches `Bash(cat:*)`). This set is low-risk, not zero-risk; keep `deny` rules on sensitive paths (e.g. `"Read(./.env)"`).

## When NOT to fire

- "Allow `npm install`" / "stop asking about `git push`" -- those are write/network permissions. Route to a general settings-configuration skill (e.g. **update-config**) if one is installed; otherwise decline and point the user at their settings file directly. Do not stretch this skill to cover them.
- "Why am I getting so many permission prompts?" with no rule list in mind -- they want their *actual* usage mined. Route to a transcript-analysis skill (e.g. **fewer-permission-prompts**) if one is installed; otherwise offer this skill's static catalog as the fallback.
- A single live permission dialog the user wants approved once -- that is the dialog's own "always allow" option, not a settings edit.

## Safety rules

- Never remove or rewrite existing rules, and never touch `deny`/`ask` -- `deny` wins over `allow` by design and may be load-bearing.
- Adding permissions is the *only* write this skill makes. No reformatting the rest of the file, no sorting their existing rules, no cleanup.
