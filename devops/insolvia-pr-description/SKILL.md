---
name: insolvia-pr-description
description: >-
  How to write the title and body of an Insolvia pull request. Use this BEFORE
  running `gh pr create`, `gh pr edit --body`, or `gh stack submit` — and
  whenever a task says "open a PR", "write the PR description", "update the PR
  body", "describe these changes", or asks you to summarise a branch for
  review — and whenever a PR is part of a stack, because every body in a stack
  must carry the stack tree and `gh stack submit` will have overwritten it.
  Reach for it the moment you finish the code and start composing the
  body, not after you have pasted a commit log: this repo's PRs are read long
  after merge, by people and agents with no memory of the branch, and a body
  that only lists what changed loses the reasoning that made the change
  correct. Also read it before adding a `.github/pull_request_template.md` or
  proposing a required approving review — both interact with decisions this
  repo has already made. Read it too whenever a task involves getting an
  IMAGE into GitHub from the command line — "attach a screenshot to the PR",
  "add a screenshot", "upload this image", "include a recording", "show the
  before and after" — because there is a working token-based upload for that
  and a 404 that makes a successful upload look broken.
---

# Writing an Insolvia pull request

## Who actually reads this

Insolvia is maintained by one person, and `protect-main` deliberately sets no
`required_approving_review_count` — **the merge gate is CI, not a human
reviewer** ([`docs/reference/architecture.md`](../../../docs/reference/architecture.md)).
So a PR body here is not a request for someone's attention. It is the durable
record of *why* a change is shaped the way it is, read by:

- **you and the agent doing the next task**, weeks later, from `gh pr view`;
- **whoever is bisecting** a regression back to this merge;
- a future maintainer who was never here.

That audience changes what earns space. Restating the diff is worthless — the
diff is right there. The reasoning that produced the diff exists nowhere else,
and disappears the moment the branch is deleted.

## The Big Three

Every body answers these, in this order. Use prose, not a form.

1. **Why** — the business reason, bug report, or technical motivation. State
   the **root cause**, not the symptom. If a decision could reasonably have gone
   the other way, say what you weighed and what you rejected.
2. **What** — the scope and nature of the change: which components, modules,
   endpoints, or user-facing behaviour moved. A brief summary synthesised from
   the branch, **never a pasted commit log**.
3. **How to review** — walk the reader through the files in a sensible order,
   point at the part that is subtle, and name what you deliberately left out.
   A heading like `## The part worth reviewing` or `## Two decisions worth
   disagreeing with` does more than a file list.

**Scale the text to the change.** 150–250 words for a standard feature; one
sentence for a two-line hotfix. A long body on a small PR is as much a smell as
a one-liner on a large one.

## Title

`<area>[+<area>]: <specific, lowercase phrase>` — areas are the repo's own
(`app`, `api`, `infra`, `design-system`, `api-client`, `marketing`, `docs`).

Titles are searched, so put the distinguishing words in them. `app: the case
list and the form that opens one` beats `app: add case screens`; `infra+api:
the access log's TTL broke every staging deploy — take it out` beats `fix TTL`.
Design-system PRs append the new version: `design-system: DateInput — a masked
date field, no calendar (0.5.0)`.

## What every body must carry

- **The issue link.** `Closes #N` when the PR finishes the issue, `Refs #N`
  when it is one part of it. Say which, explicitly — "the bulk of #83", "the
  second half of #84 (8.4), after #146".
- **Verification, with evidence.** Never "tested locally". Name the command,
  the environment, and the result: test counts before and after, `terraform
  validate` green on which envs, which check the axe audit runs against. A
  small table works well.
- **What could not be verified locally, and why.** The repo requires local
  testability or a written reason (root `CLAUDE.md`). If a step genuinely needs
  the OIDC deploy role, a real CloudFront distribution, or an SES production
  identity, say so in the body and give the nearest local approximation.
- **All three environments.** If the change touches infra, config, or anything
  environment-shaped, say what it does on **local (`infra/envs/dev`), staging,
  and prod** — including "prod's table has never been created, so nothing to
  migrate".
- **Deployment considerations, surfaced not buried.** New environment
  variables, migrations, IAM permission grants (those need a human-run apply —
  `insolvia-deploy-role-permissions`), destructive converge steps, data loss on
  the next deploy. Put these under an `## After merge` heading.
- **Visual evidence for any UI change.** Screenshot or a short recording for
  app or marketing changes; a code sample of the new component API for
  design-system ones. Getting an image into a body from the CLI has its own
  trap — see **Attaching a screenshot** below.
- **The footer.** End the body with:
  `🤖 Generated with [Claude Code](https://claude.com/claude-code)`

## Attaching a screenshot

GitHub publishes no API for the attachment uploads its web UI accepts by
drag-and-drop, which is why this looks impossible from a terminal and why the
visual-evidence bullet above kept going unmet. It isn't impossible: the endpoint
behind drag-and-drop takes an ordinary `gh` OAuth token, so no browser, no
extension, and no session cookie are involved.

```
POST https://uploads.github.com/user-attachments/assets
       ?name=<basename>&content_type=<mime>&repository_id=<numeric id>
  Authorization: Bearer $(gh auth token)
  Accept:        application/json
  Content-Type:  <mime>
  <raw file bytes>
→ 201  {"url": "https://github.com/user-attachments/assets/<uuid>"}
```

Paste-ready, and checked against this repo:

```bash
gh-upload-image() {                 # gh-upload-image FILE [owner/repo]
  local f="$1" repo="${2:-}" ct id url cfg name
  [ -r "$f" ] || { echo "no such file: $f" >&2; return 1; }
  name=$(basename "$f"); ct=$(file --mime-type -b "$f")
  id=$(gh api "repos/${repo:-:owner/:repo}" --jq .id) || return 1
  cfg=$(mktemp); chmod 600 "$cfg"
  printf 'header = "Authorization: Bearer %s"\n' "$(gh auth token)" > "$cfg"
  url=$(curl -sS -f -K "$cfg" -X POST \
    -H 'Accept: application/json' -H "Content-Type: $ct" --data-binary @"$f" \
    "https://uploads.github.com/user-attachments/assets?name=$(jq -rn --arg v "$name" '$v|@uri')&content_type=$(jq -rn --arg v "$ct" '$v|@uri')&repository_id=$id" \
    | jq -r .url)
  rm -f "$cfg"
  [ -n "$url" ] && [ "$url" != null ] || { echo "upload failed" >&2; return 1; }
  printf '![%s](%s)\n' "$name" "$url"
}
```

It prints a markdown line; drop that straight into the body file, then
`gh pr create --body-file`.

**The 404 is not a failure — do not go chasing it.** A freshly uploaded asset is
readable *only by the token that uploaded it*. Fetch that URL anonymously and
you get `404`, every time, on a public repo. Referencing it in a PR, issue, or
comment is what binds it to that content and makes it readable by everyone who
can read the content. So the upload is a two-step commit, and the obvious
sanity check — upload, then `curl` the URL — reports failure for something that
worked. Verify with the token instead, or just look at the rendered PR.

Four more things that cost time to rediscover:

- **`repository_id` is the REST numeric id** (`gh api repos/:owner/:repo --jq
  .id` → `1312821833`), *not* the GraphQL node id `R_kgDO…` that `gh repo view
  --json id` hands you. The node id fails.
- **`:owner/:repo` only expands inside a git checkout.** From a scratchpad
  directory it dies with `not a git repository`; pass `owner/repo` explicitly.
- **Images and video only.** The token route is scoped to image and video types
  on repos your token can push to. A PDF, zip, or log is refused, and the only
  fallback is scraping the browser's `user_session` cookie — which prompts the
  keychain. Don't. Put the log in the body as a fenced block.
- **Keep the token off the command line.** `-H "Authorization: Bearer $(gh auth
  token)"` leaks it to `ps`. Hence the mode-600 config file above, deleted
  immediately.

The `gh-image` extension wraps exactly this endpoint and is worth knowing about,
but **installing it is blocked by the permission classifier in this
environment** — two attempts, one transient and one hard refusal. The function
above needs nothing installed, so reach for it first rather than re-litigating
the install.

## Before you open it

- **Self-review the diff first** — `git diff main...HEAD`. Catch the stray
  `console.log`, the unrelated file, the debug flag. GitHub's own guidance puts
  this ahead of asking for review; here it is the only review there is.
- **One PR, one responsibility.** Unrelated fixes bundled together are harder
  to revert and harder to bisect. Split the branch instead.
- **Design-system changes are not made in this repo** — they land in
  `insolvia-ai/design-system` and arrive here as a version bump, which is
  ordinary work and needs no PR of its own (`insolvia-design-system-bump`).
- **Dependent PRs go on a stack** — see below.
- **Never push to `main`.** Branch `claude/<name>-<id>`, then PR.

## Stacked PRs: every body carries the tree

A stacked PR's body has a job an unstacked one doesn't — telling the reader
*where in the chain they are*. GitHub renders a stack widget on the PR page,
but that widget is web UI only: it is absent from `gh pr view`, from
notification emails, and from the merged body that survives in the archive.
The tree in the body is the copy that lasts.

**Put it directly under the title line of the body, in every PR of the stack**
— bottom to top, with this PR marked:

```
**Stack** (bottom → top), trunk `main`:

└─ #143  api+api-client: case CRUD behind auth   ✓ merged
  └─ #146  design-system: Select (0.4.0)         ○ open   ← this PR
    └─ #147  design-system: DateInput (0.5.0)    ○ open
```

Generate it rather than hand-maintaining it — the numbers and states change
under you on every `sync`:

```bash
gh stack view --json | jq -r '"**Stack** (bottom → top), trunk `\(.trunk)`:", "", (.branches | to_entries[] | (("  " * .key) // "") + "└─ " + (if .value.pr then "#\(.value.pr.number)  " else "(no PR)  " end) + .value.name + (if .value.isMerged then "  ✓ merged" elif .value.isQueued then "  ◎ queued" elif .value.pr then "  ○ open" else "  · unsubmitted" end) + (if .value.needsRebase then "  ⚠ needs rebase" else "" end) + (if .value.isCurrent then "   ← this PR" else "" end))'
```

**`--json` is not optional here.** Bare `gh stack view` and `gh stack view
--short` open an interactive TUI and hang an agent forever — the `gh-stack`
skill lists both as never-do. The docs page describing them is written for a
human at a terminal.

### `submit` writes the body, so you edit it afterwards

`gh stack submit --auto` auto-generates every new PR's title *and body* from
commit messages, and **there is no flag to supply your own**. So the order is:

```bash
gh stack submit --auto                    # creates/updates the PRs
gh stack view --json                      # read back the numbers and order
gh pr edit 146 --body-file pr-146.md      # then write the real body, per PR
```

Re-run the tree generator and re-edit the bodies after anything that changes
the chain — `gh stack sync`, a merge below you, a new layer on top. A tree
that still shows a merged PR as open is worse than no tree.

### What the tree does not replace

- **Each PR still states its own dependency in prose** — "the second half of
  #84 (8.4), after `Select` in #146". The tree gives position; the sentence
  gives the reason this layer exists separately.
- **Each PR still gets its own Big Three.** A stack is not one PR split across
  five bodies; each layer is independently reviewable and independently
  reverted, so each carries its own why/what/how-to-review.
- **Scope `Closes #N` to the layer that actually finishes the issue** — the
  ones below it get `Refs #N`. Every layer claiming `Closes` closes the issue
  on the first merge, while the rest of the stack is still open.

Stack mechanics — `init`, `add`, `rebase --upstack`, and the rule that
`gh pr merge` does not work on stacks (`gh stack merge --yes` does) — belong
to the `gh-stack` skill. Read it for the branch work; this file only owns what
goes in the body.

## Writing it

Compose the body in a file and pass `--body-file` — a heredoc or `--body`
string mangles backticks, `$`, and code fences:

```bash
gh pr create --title "app: the case list and the form that opens one" --body-file pr-body.md
```

## Anti-patterns

| Don't | Instead |
|---|---|
| Paste the commit log | Synthesise one narrative |
| "Tested locally" | The command, the env, the counts |
| "Fixes bug" / "Updates code" | Name the behaviour that changed |
| Describe the diff line by line | Explain the reasoning the diff can't show |
| Bury a data-loss or IAM consequence mid-paragraph | `## After merge`, at the end |
| Add a rigid section template to a narrative body | Sections only where they earn their heading |
| Leave `submit --auto`'s generated body on a stacked PR | `gh pr edit <n> --body-file` after submitting |
| A stale stack tree, or one only on the bottom PR | Regenerate from `--json` into every body after each sync |
| "I can't attach screenshots from the CLI" | `gh-upload-image`, above — it needs nothing installed |
| Retrying an upload because the URL 404s | Expected until referenced; check with the token, not anonymously |

## On `.github/pull_request_template.md`

There isn't one, and that is a live decision rather than an oversight: every PR
here is opened non-interactively with `--body`/`--body-file`, which bypasses the
template entirely, so the file would be inert on the path that actually creates
PRs. The prompts above are the template, read where they are used. If PRs start
being opened from the GitHub web UI, add one — and keep it to **4–6 prompts**,
because a longer one gets skipped rather than filled in.
