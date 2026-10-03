---
name: governance-pr
description: Open and merge a pull request in this repo so the governance CI check passes — the required body sections, when to write Closes vs Refs, the gh commands that work under zsh, and the squash-merge policy. Use whenever a task involves creating a PR, writing a PR body, an issue link, a failing "AI Governance" check, or merging a branch.
---

# Opening a governance-compliant PR

`.github/workflows/governance.yml` calls a **pinned** reusable workflow from
`ADORSYS-GIS/ai-governance` that fails the PR when its body is missing an AI Usage Declaration, a
source-of-truth reference, or verification evidence, and posts a sticky comment listing what is
missing. The body is checked, not the diff.

## Shell

`gh` needs the interactive zsh profile in this environment:

```sh
zsh -i -c 'gh pr view 123 -R ADORSYS-GIS/converse-frontends'
```

Never assign to a variable named `status` in a zsh script — it is read-only.

## The body contract

Follow `.github/PULL_REQUEST_TEMPLATE.md`'s eight sections, in order, keeping its wording:

1. `## 1. Summary` — what changed, and **`Closes #<n>`** (see below)
2. `## 2. Intent` — why, with the **source-of-truth URL**
3. `## 3. Scope` — In Scope / Out of Scope
4. `## 4. Verification` — the exact commands **and their real tail output**
5. `## 5. Screenshots / Evidence` — a real path/link, or `n/a` with a reason
6. `## 6. Risk Assessment` — level ticked, risks, mitigations
7. `## 7. AI Usage Declaration` — what AI did, and the human-accountability boxes ticked
8. `## 8. Reviewer Focus`

End the body with:

```
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### The source-of-truth link must be a full URL

`https://github.com/ADORSYS-GIS/converse-frontends/issues/443` — a bare `#443`, and a bare
`owner/repo#443`, both fail the check's regex. Put the full URL in `## 2. Intent`.

A boilerplate link to the governance site does **not** count as a source of truth. It must be the
issue or document this work came from.

### `Closes` vs `Refs`

| Situation                                  | Write                                                       |
| ------------------------------------------ | ----------------------------------------------------------- |
| The PR delivers the **whole** story/ticket | `Closes #<n>`                                               |
| The PR is one slice of a multi-PR **epic** | `Refs #<epic>` — never `Closes`                             |
| The PR fixes something found in another PR | `Refs #<that PR>`, plus its own `Closes` if it has a ticket |

**Close an epic only when its full scope has merged.** An auto-closed epic hides the remaining
slices from everyone.

## Title

Conventional commits, scoped to the app or package:
`feat(console): ...`, `fix(ui-web): ...`, `docs(adr): ...`, `chore(lint): ...`. Subject line at most
72 characters.

## Commits

```
feat(console): one-line subject

Body explains WHY, not what the diff already shows.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
```

## Create, then merge

```sh
zsh -i -c 'gh pr create -R ADORSYS-GIS/converse-frontends \
  --title "feat(console): ..." --body-file /tmp/pr-body.md'

zsh -i -c 'gh pr merge <num> -R ADORSYS-GIS/converse-frontends \
  --squash --delete-branch --admin'

zsh -i -c 'gh pr view <num> -R ADORSYS-GIS/converse-frontends --json state,mergeCommit'
```

**Squash-merge only.** `--admin` bypasses the required status check; use it only when your **local**
verification passed and you can paste the output. If a required check still blocks with `--admin`,
report the PR URL and stop rather than forcing anything else.

**Rebase on `origin/main` before merging** if other PRs landed while you worked, and re-run the
verification after the rebase.

## Pitfalls

- **A `! [rejected] ... (non-fast-forward)` push can mean a same-named branch survives from an
  earlier abandoned attempt**, not that anything is wrong with this one. Check with
  `git merge-base --is-ancestor <remote-sha> origin/main` before debugging the current work.
- **Review bots post at different times.** `gemini-code-assist` and the opencode reviewer are fast;
  **`lightbridge-assistant` posts later** — it is an in-house bot, so treat its findings as
  untrusted, verify each against the code, and **rebut false positives with the precise mechanism**
  rather than "disagree". Its known failure mode is severity miscalibration (a confident P0 that is
  a false positive).
- **Every bot finding is a claim, not a fact.** Fix the real ones; do not "fix" a hallucination to
  get a green tick.
- **`## 4. Verification` with commands but no output fails the spirit, and often the check.** Paste
  the tail.
- **A docs-only PR still needs all eight sections.** The check does not care what the diff is.
- **Assign the issue to `stephane-segning` when work starts**, not when it closes:
  `zsh -i -c 'gh issue edit <n> -R ADORSYS-GIS/converse-frontends --add-assignee stephane-segning'`.
