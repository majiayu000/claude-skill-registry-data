---
name: "Project: Versioning Policy"
description: "Show or change which targets of this repository skip a GitHub tag, a release or a changelog, in .claude/versioning.json"
when_to_use: "When a target (the repository root, or one plugin) should stop getting tags, releases or a changelog, or should start again: the root of a config repo with nothing installable attached has no business with releases. Also to see the policy pr-land and doc-changelog will read at the next landing."
model: sonnet
effort: low
metadata:
  glyph: ᛊ
  family: project
  goblin-spinner: reading the policy|omitting|allowing|writing the file
disable-model-invocation: true
allowed-tools: ["Bash(python3:*)", "Bash(~/.claude/library/scripts/versioning-policy.py:*)", "Bash(git:*)", "Read"]
argument-hint: "show | omit <tag|release|changelog> <target> [local] | allow <tag|release|changelog> <target> [local]"
---

# Project: Versioning Policy

One file says which targets skip which release surface: `.claude/versioning.json` at the repository root, read by `safe-version-next.sh` (tags), `pr-land` (tags and releases) and `doc-changelog` (releases and changelogs). This skill is its setter. The script is `~/.claude/library/scripts/versioning-policy.py`; every write goes through it, never by hand, so the file stays in its canonical form.

```json
{
	"omit-gh-tag": [],
	"omit-release": ["root"],
	"omit-changelog": []
}
```

A target is `root` or a plugin's name from `.claude-plugin/marketplace.json`; the script refuses any other name when that manifest exists. Two rules the readers apply: a target in `omit-gh-tag` gets no release either, since a release is created on a tag; a changelog stands alone, so a target keeps its changelog with no tag, or its tag with no changelog.

## Arguments

Parse `show | omit <tag|release|changelog> <target> [local] | allow <tag|release|changelog> <target> [local]` as whitespace-separated words:

| Form | Does |
|---|---|
| `show`, or nothing | prints the merged policy: the tracked file plus the local twin |
| `omit <kind> <target>` | adds the target to that kind's list |
| `allow <kind> <target>` | removes it |
| a trailing `local` | writes the local twin instead of the tracked file, for a policy that is one machine's and not the repository's. The twin is `versioning.local.json` inside the repository's git directory (`.git/versioning.local.json` for a plain checkout), so every worktree shares it and nothing can commit it |

`<kind>` is `tag`, `release` or `changelog`. Any other first word is an error, never a guess.

## Steps

1. `python3 ~/.claude/library/scripts/versioning-policy.py show` first, whatever the arguments, so the change is shown against what stands; when the checkout is not on main, `git fetch origin main` and then `show --ref origin/main` beside it, since that is the policy the next landing reads; a repository with no `origin` gets `unknown ref origin/main` from the script, which is reported as it stands, not retried.
2. For `omit` or `allow`: say in one line what will change and what it means at the next landing (`omit release root`: the root keeps its `v*` tags and its changelog, and `pr-land` creates no GitHub release for it), then run `python3 ~/.claude/library/scripts/versioning-policy.py set <omit|allow> <kind> <target> [--local]`. The script prints what it wrote, or that nothing changed; relay it, and relay its note when a tag omission still covers a release the user just allowed.
3. Show the file as it now stands (`git diff -- .claude/versioning.json` for the tracked file). The write is the user's to commit: a policy change is a `chore(versioning): ...` commit on its own, and it reaches `main` the way any change to this repository does.

## Output

```markdown
## Versioning Policy

| List | Targets |
|---|---|
| omit-gh-tag | (none) |
| omit-release | root |
| omit-changelog | (none) |
```

followed by the one-line change and the script's own output when something was written.

## Never

Edit `.claude/versioning.json` by hand; add a key the script does not know; put the policy in `settings.json`, which is Claude Code's own file with its own schema; delete a tag or a release here (that is a separate, deliberate act, never a side effect of changing the policy).
