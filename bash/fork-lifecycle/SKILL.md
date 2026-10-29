---
name: fork-lifecycle
description: "Sync the forks package group in prateek/dotfiles packages.toml with the live state of the prateek/forks fleet: adopt a fork once it ships a release, or retire one whose upstream PRs have all landed. Reads fleet state via gh api (no clone), edits packages.toml through scripts/packages/fork-lifecycle-entry, validates the reconciler, and opens an ordinary PR. Use when a fork ships its first release, when a fork files a retire self-issue, or when asked to reconcile fork packages. Trigger on 'adopt the X fork', 'retire the X fork in dotfiles', 'sync fork packages', 'a fork filed a retire issue'."
---

# fork-lifecycle

Keeps `[packages.groups.forks].entries` in `home/.chezmoidata/packages.toml` in
sync with the fleet in `prateek/forks`. This is the **dotfiles side** of the
downstream-fork system (design: [ADR 0015](../../../docs/adr/0015-downstream-fork-daily-driver.md)).
Fleet operations — assembling, releasing, retiring the fork itself — live in the
`fork-ops` skill in `prateek/forks`. Adopt and retire here are ordinary PRs; no
automation writes `packages.toml`.

The single writer is `scripts/packages/fork-lifecycle-entry` (add/remove,
idempotent, TOML-parse-guarded). Package names are opaque tokens
`prateek/forks/<tool>-fork`.

## Read fleet state

No clone needed — `gh api` against `prateek/forks`:

```sh
# forks in the fleet
gh api repos/prateek/forks/contents --jq '.[] | select(.type=="dir") | .name'
# a fork's manifest (kind lives in [release]); the retired marker; latest release
gh api repos/prateek/forks/contents/<tool>/.fork/fork.toml --jq .content | base64 -d
gh api repos/prateek/forks/contents/<tool>/.fork/retired   # 404 = still live
gh api repos/prateek/forks/releases \
  --jq '[.[]|select(.tag_name|startswith("<tool>-v"))][0].tag_name'
# retire self-issues (they record what to flip back to)
gh issue list --repo prateek/forks --author "app/prateek-fork-automation" --state open
# fork-specific build/sync gotchas, if a fork won't adopt cleanly (404 = none yet)
gh api repos/prateek/forks/contents/<tool>/learnings.md --jq .content | base64 -d
```

Build-resolution learnings are recorded on the `prateek/forks` side (the
`fork-ops` skill writes `<tool>/learnings.md`); this skill only reads them.

A fork is **adopt-eligible** when it has a `<tool>-v*` release and no
`.fork/retired`. It is **retire-eligible** when `.fork/retired` exists (or it
filed a retire self-issue).

## Adopt

```sh
scripts/packages/fork-lifecycle-entry add \
  --file home/.chezmoidata/packages.toml \
  --name prateek/forks/<tool>-fork \
  --kind <formula|cask> \        # from the fork's fork.toml [release].kind
  --replaces <official-token>    # what the fork shadows in brew; omit if none
```

`kind` comes from the fork's `fork.toml`. `replaces` is the official brew token
the fork stands in for — you know it, or read it from the retire self-issue's
"flip back to" line.

## Retire

```sh
scripts/packages/fork-lifecycle-entry remove \
  --file home/.chezmoidata/packages.toml \
  --name prateek/forks/<tool>-fork
```

`brew bundle` reinstalls the official package once the fork entry is gone — the
apply-time reconciler runs first and uninstalls the fork.

## Validate, then PR

```sh
scripts/packages/render-brewfile --machine-type personal   # the entry renders
just test-shell tests/bats/packages/fork-reconcile.bats     # swap logic still holds
```

Then open an ordinary PR with `gh pr create`. A human
merges; `chezmoi apply` swaps the install. Close the fork's retire self-issue if
one drove the change.
