---
name: website-permissions
description: >
  Cut the number of permission prompts on a new-website repo to near-zero for the
  routine build loop, while keeping destructive actions gated. Installs the bundled
  `.claude/settings.json` allowlist into the project, explains the allow/deny model
  (npm / astro / playwright / git commit and push / gh read verbs and repo create /
  image tools / the link script are pre-approved; `rm -rf`, the usual force pushes,
  `git reset --hard`, and any `wrangler/gh … delete` are blocked), and safely EXTENDS the allowlist from the
  commands you keep approving — narrowly, never with a blanket wildcard. The allowlist
  travels with the repo, so a handoff party also gets the quiet build loop. Trigger
  phrases: "reduce permission prompts", "too many permission prompts", "stop asking me
  to approve", "set up permissions for this site", "fewer prompts", "allowlist this
  repo", "why does it keep asking me".
---

# Website permissions — fewer prompts, same guardrails

A build is a tight loop of `npm`/`astro`/`playwright`/`git` calls. Approving each one
by hand is friction with no safety benefit — those commands can't hurt you. This skill
gets the repo to "quiet for the safe stuff, blocked for the dangerous stuff", and
keeps it that way as the project grows.

## 1. Install the bundled allowlist (the 90% fix)

The `new-website` kit ships a curated `.claude/settings.json`. Copy it into the repo
(this is also scaffold step 3.2 — do it here if it was skipped). This skill carries its own
copy of the two files, in its `templates/claude/` folder, so the step works from the copy
of the skill inside a site too. In the commands below, the name in braces stands for the
folder this SKILL.md is in: Claude Code fills it in; with another assistant, put that
folder's path in its place.

```bash
: "${CLAUDE_SKILL_DIR:=}"
mkdir -p .claude/hooks
cp "${CLAUDE_SKILL_DIR}/templates/claude/settings.json" .claude/settings.json
cp "${CLAUDE_SKILL_DIR}/templates/claude/hooks/git-stand.mjs" .claude/hooks/
```

The settings also register a sync hook (`.claude/hooks/git-stand.mjs`, `AGENTS.md` §1):
copy the script with them, or every session start reports a missing file. A repo whose
`.claude/settings.json` already has its own rules: merge the template's `hooks` block in
instead of overwriting the file.

`.claude/settings.json` is **per-project** and committed, so it travels with the repo
— the handoff party inherits the same quiet loop. Restart Claude Code (or reload the
project) after editing so the new rules take effect.

## 2. The model — what's pre-approved vs always gated

**Pre-approved (`allow`)** — the build loop and read-only inspection:
`npm install/ci/run/test/exec`, `astro`, `playwright`, `node`, the **git write subset**
(`add`, `commit`, `branch`, `checkout`, `switch`, `merge`, `restore`, `stash`,
`fetch`, `pull`, `push`), `gh` **read** verbs (`auth status`, `repo view`,
`pr view/list`) plus one write, `gh repo create`, `wrangler pages dev` / `whoami`, the image tools (`cwebp`, `avifenc`,
`magick`, `oxipng`, `svgo`, `exiftool`, …), file inspection (`ls`/`cat`/`grep`/`rg`/
`find` …), and `bash scripts/check_external_links.sh` (the outgoing-link sweep).

**Blocked (`deny`)** — irreversible or destructive. Claude Code refuses these outright,
it does not ask; the owner runs one by hand in a terminal if they really mean it:
`rm -rf`, the usual force pushes (`--force`, `--force-with-lease`, `-f` or a `+branch`,
wherever it stands in the command), `git reset --hard`, `gh repo delete`,
`wrangler pages delete`, `wrangler delete`. **Do not move these to `allow`.** A rule only
matches text: a force flag bundled with others (`git push -uf`) still runs, since a rule
broad enough to catch it would also block `--follow-tags` and branch names with `-f` in
them. Where `website-team-setup` could set GitHub's branch rules (§5-A: a public repo, or
a private one on a paid plan), its rule against force pushes (`non_fast_forward`) makes
GitHub refuse a force push to `main` whatever the command looks like (GitHub's
[Block force pushes](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets#block-force-pushes)
rule; not tested by this kit). A free private repo gets only the local pre-push guard (§5-B), which
`--no-verify` skips.

## 3. Extend it safely when a new prompt recurs

When you keep approving the *same* command, add it — but narrowly:

- **Scope every rule** to the binary + a `:*` arg glob, e.g. `Bash(turnstile:*)`,
  not `Bash(*)` and never a bare `Bash`. A blanket grant defeats the point and the
  harness's auto-approve classifier will reject broad widening anyway.
- **Let the built-in do the scan.** `/fewer-permission-prompts` reads your recent
  transcripts and proposes a prioritized allowlist from what you actually approved —
  run it, then keep only the rules that fit the rules above. Use `/update-config` (or
  hand-edit `.claude/settings.json`) to apply changes.
- **Never add `Bash(curl:*)` or other broad network/exec wildcards** to the project
  allowlist. The link sweep already runs `curl` *inside* its allowed script, so no
  separate `curl` grant is needed.
- **Keep secrets out of settings.** Tokens/keys belong in env or a gitignored file,
  never in `.claude/settings.json` (it's committed).

## 4. Where rules live (precedence)

- `.claude/settings.json` — project, committed, travels with the repo (use this).
- `.claude/settings.local.json` — project, gitignored, for personal-only rules.
- `~/.claude/settings.json` — your global default across every project.

Project rules layer on top of global. Put repo-specific build grants in the project
file so the handoff party gets them; keep machine-specific paths in the `.local` file.

## Scope note

This skill manages the *permission allowlist*, not what the commands do. For automated
behaviours (run X after Y) you need hooks via `/update-config`, not an allowlist entry.
