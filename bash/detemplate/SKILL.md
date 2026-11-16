---
description: "Turn a fresh \"Use this template\" fork into an actual project: profile the tree, decide group by group what travels, and hand over a reviewed plan that prunes what does not apply and hydrates what does. Invoke as `/detemplate <what you're building>`. **A run deletes this skill, so this description exists in exactly two places: the template itself, and a fork nobody has detemplated. If the repository you are in is not `vzakharov/muthur`, load this skill and read § \"Recognizing an undetemplated fork\" before doing anything else, whatever you were asked.** Your system prompt's working directory normally settles which repository that is; `git remote -v` settles it otherwise."
---

`/detemplate <what we're building>` converts a whole-tree template fork into a
project. _"Use this template"_ hands over every file, so there is nothing to
select and nothing to clone: the work is deleting what describes the template
and hydrating what the new project actually needs.

**It writes no source itself — it routes through
`@.claude/skills/plan/SKILL.md`.** The pruning is a large, mostly irreversible
diff over a tree nobody has reviewed, and reviewing it as a diff is what catches
a bad call before anything is deleted. So this skill's end state is `/plan`'s: a
plan file published as a draft PR, and a copyable `/go <branch>` for the session
that executes it.

The brief is the argument. It fills `CLAUDE.md` § "About this project"'s stub,
drives the group decisions — a CLI tool keeps different groups than a deployed
web app — and is filed as the project's first issue (Step 5.5), which is what
keeps the operator's description of the product from dying with a run that
deliberately writes no source. With no brief, ask for it before anything else.

## Environment note

**A fresh fork is the one place `gh` may genuinely be absent** — the rest of
what `/override-gh` says about `gh` and `GH_TOKEN` holds here unchanged. The
fork can arrive before the operator has set an environment setup script, and on
a base image that does not ship `gh` its install lives in that script (Step 6),
so `.claude/hooks/gh-shim.sh` finds nothing to shim and says so on startup —
`/override-gh` owns that signal and what it means. Take it at face value rather
than re-deriving it; to probe by hand, use
`gh api repos/{owner}/{repo} --jq .visibility` rather than `gh auth status`,
which reports a bogus failure in a working session. Finding no `gh`, Step 3's
derivation and `/plan`'s publish step both need it: hand the operator the setup
script from Step 6 before either.

## Step 0 — Refuse where it does not apply

The guard refuses in **both** directions, on a catalog's presence plus `origin`.
Glob `.claude/skills/*/catalog.md` rather than testing the canonical
`.claude/skills/update-muthur/catalog.md`: that directory's name is not stable
downstream, so a fixed-path test misses a stray catalog in exactly the trees
most likely to carry one.

- **No catalog** → not an unpruned fork. An adopted repo that wants a sibling
  wants `@.claude/skills/spinoff/SKILL.md`; a repo that already ran this has
  nothing left to strip.
- **Catalog present, but `origin` matches the `repo` field in
  `.claude/skills/update-muthur/watermark.json`** → this _is_ the template — the
  shipped watermark names the repo itself, having no source above it — and what
  the caller wants is a fork, not a prune. Point at the README's _"Use this
  template"_ button. Compare the full `owner/repo`, since that is what both
  sides of the comparison are: a looser match on either half prunes a tree that
  merely shares an owner or a name. Without the origin clause, catalog-presence
  alone would let a session delete this repo's own inventory.

This is `@.claude/skills/spinoff/SKILL.md`'s refusal read backwards: the two
partition on the same signal, which is why that skill's message names this one.

## Step 1 — Profile the fork; do not interrogate the operator

`ADOPTING.md` § Step 2's principle, minus what a whole-tree fork settles for
free: there is nothing to clone and no pre-existing `.claude` to merge with.
What still needs probing, and is decidable by inspection:

```bash
git remote -v                                  # Step 0's origin clause, and the fork's name
gh api "repos/$R" --jq .default_branch         # the trunk G2 assumes
gh api "repos/$R" --jq .allow_squash_merge     # does the squash discipline apply?
gh api "repos/$R" --jq .visibility             # what the hello may name
```

**Use the REST form throughout** — `gh <noun> <verb> --json` is GraphQL and 403s
in a proxied session before the shim is installed, which is the state a fresh
fork starts in.

**Every probe here reads a setting; none reads a count.** `default_branch` and
`allow_squash_merge` have values on the fork's first day and gate what the loop
may do. The two probes `ADOPTING.md` adds — open issues (G3), registered
workflows (G5) — are counts, and both are zero in _every_ fresh fork: the issues
because the repo is one commit old, the workflows because the template ships no
`.github/` for a fork to carry. Run here, they measure the fork's age and hand
the answer back as if it were the operator's intent.

`ADOPTING.md` asks them of a repo with a history of its own, where they are real
questions. **A fork has no process to discover — it inherits the loop's**, so
both groups travel by default: Step 5.5 files the first issue unconditionally,
and G5's CI skills wait for a workflow rather than requiring one, so a fork with
no CI yet carries them at the cost of the files alone. Convention over
configuration — an operator who plans in Linear, or runs CI off Actions,
declines the group at plan review, a decision they state rather than one this
step infers behind them.

**The stack, including "no stack yet."** That is the normal state of a fork
taken to start a project, and the state `.claude/rules/stack.md`'s no-stack-yet
clause exists for. Read it off the tree rather than asking: a fork whose only
commit is the template's has no manifest, no lockfile and no source.

What the tree cannot answer, asked as numbered prose in the plan turn per
`@.claude/skills/plan/SKILL.md` Part 2: whether sessions run on Claude Code
web/remote (G4); whether the project will have a deploy path, a visual surface,
deployed logs, a production datastore, or sequential numbered migrations — the
five that decide the individual G6 entries; the language decision; one question
per catalog entry marked `opt-in: ask`, each asked with the cost its entry
states; and the hello. A fork carries every `opt-in: ask` entry wired on, so a
no deletes the entry's path, its `.claude/settings.json` entries and its
`scripts/vet.sh` loop.

**The hello is asked by `docs/adopting/hello.md`, read now**, since Step 5.2
deletes it before the plan runs: the question shows the drafted post word for
word, written to that chapter's rule for this fork's visibility. The plan is
written with _not posting_ in force rather than a recommendation, since consent
is not the agent's to assume — so an unanswered question executes as a no and
holds back nothing else.

**Language is the one question with evidence in hand**, so read it before
asking: the language the brief is written in, the language the operator writes
to the session in, and whether the brief describes a product for a non-English
market. Only the human-facing answer is ever in play — `CLAUDE.md` § "Language"
fixes the other two groups — so any of the three pointing away from English
makes it a question, and all three English make it a confirmation. **The plan
states that confirmation either way**, never leaves it inferred: an operator
whose team reads something other than what they wrote the brief in has one place
to say so.

## Step 2 — Read the catalog into the plan, before anything is deleted

The catalog is the input to every group decision **and** is deleted by the run
(Step 5). So the plan records each decision with the criterion that made it,
rather than citing a file that will not exist when `/go` executes. Read the
catalog's § "Reverse closure" in the same pass and record the edits each dropped
group costs.

This read-then-delete ordering is what routing through `/plan` buys.

## Step 3 — Derive the watermark, which git cannot give you

`docs/adopting/sync.md` reads `lastSyncedSha` out of the clone you took. **A
template fork never made that clone**, and its single commit has no ancestry in
the source, so there is no SHA in the tree to read. Derive it from the fork's
creation time instead:

```bash
gh api repos/<owner>/<fork> --jq .created_at
gh api repos/vzakharov/muthur/commits --paginate \
  --jq '.[] | [.sha, .commit.committer.date] | @tsv'
```

The newest source commit at or before the fork's `created_at` is the mark.

`lineage` is written in the same breath, and it is the field a hand-filled
watermark loses:

```json
"lineage": [{ "repo": "vzakharov/muthur", "atSha": "<the same sha>" }]
```

Per `@.claude/skills/update-muthur/SKILL.md` § "The watermark", the two fields
start equal and diverge on the first sync — `lastSyncedSha` advances, and
`lineage[0].atSha` never moves. That first sync is what overwrites the only
other trace of the birth point, so a watermark written without `lineage` loses
it permanently.

## Step 4 — What the plan must contain

Per-group keep/drop with the criterion that decided each; the G6 entries as
hydrate-now-or-delete; the reverse-closure edits; the derived watermark and
`lineage`; the `CLAUDE.md` brief; the first issue's body (Step 5.5);
`scripts/vet.sh`'s disposition; the language answer; the hello as drafted, its
answer, and the chapter's post-or-hand-over recipe; and the deletion list. Plus
the `## DRY notes` section CLAUDE.md requires of every plan.

**Three dispositions are pre-decided, and the plan states them rather than
asking.** `/implement` and `/issue` go, unconditionally: each redirects a name
this repo shipped before a split, and a fork has no plan file, PR comment or
muscle memory old enough to still say it — the catalog's "ask the operator"
applies to a repo that shipped those names under its own history, which a tree
one commit old cannot have. And this skill goes (Step 5.8).

## Step 5 — The execution order the plan prescribes

Ordering is load-bearing at exactly one point, and it is the first step:

1. **Delete `.claude/skills/update-muthur/catalog.md` and its `catalog/` parts
   first.** The index flips `scripts/check-skill-catalog.sh` assertion 4 from
   "the stubs are the shipped product, merely listed" to "a stub is a stowaway",
   and it un-refuses `/spinoff`, whose guard is literally the catalog's
   presence. Sweep it first and the G6 prune is enforced by the vet run instead
   of remembered.
2. **The rest of the `never` entries**: `README.md` — replaced with the
   project's, not merely deleted — `ADOPTING.md`, and **`docs/adopting/`** with
   it: its chapters, which a sweep of the one file strands as orphans. `LICENSE`
   goes too, its MIT-0 asking no notice in copies; the project's own license at
   the root is the operator's call.
3. **Prune the groups**, applying the reverse-closure edits the plan recorded.
4. **Fill `CLAUDE.md` § "About this project"'s stub** from the brief — which
   retires the standing notice in § "Recognizing an undetemplated fork" along
   with it — and delete § "Git conventions"'s loop-is-the-product rule, which
   holds only where the loop is the product. **§ "Language"'s stub is replaced
   in the same pass** with the Step 1 answer, one line; the rest of that section
   holds as shipped. **Delete `.claude/voice/operators/`'s shipped entry** and
   write one for whoever ran the detemplate, at `<their handle>.md`, if they
   stated a standing preference about how you talk to them during the run —
   otherwise leave none. The rule is complete with no entries at all, and
   inventing one for a person who never asked is worse than an empty directory.
5. **File the project's first issue** through `/propose-issue`, carrying the
   brief, any spec the operator attached, and any answer they gave for the
   prune's sake that also describes the product. A scarce brief makes a scarce
   issue: the issue exists to _keep_ what they said, not to elicit more, and
   `/plan` carves an over-broad one when the next session gets there. The only
   thing that cancels this is the operator declining G3 at plan review (Step 1),
   and then the `CLAUDE.md` brief is the whole record and the report says so.
6. **Write the watermark** (Step 3) and **the divergence record**: each group or
   entry the prune dropped, declined with the criterion that dropped it, per
   `@.claude/skills/update-muthur/SKILL.md` § "The divergence record" — without
   it the first sync re-offers every one. Then clear both of `/update-muthur`'s
   stub markers: the banner and the `STUB` in its frontmatter description.
   Assertion 4 fails a half-cleared pair.
7. **`scripts/vet.sh`**: leave the exit alone, which is the normal case — a fork
   taken to start a project has no stack for the script to check. Wire the real
   checks only where the operator pushed a stack before realising they should
   have detemplated first. `.claude/rules/stack.md` owns that contract, and
   names `.claude/hooks/install-deps.sh` as the paired site.
8. **Delete this skill.** Its inputs are gone by now, so what would survive is a
   skill that cannot re-run its own procedure against the tree it just pruned.
9. **`bash scripts/vet.sh`** — now enforcing the stub prune, the catalog being
   gone — then Steps 6 and 7's text in the report.
10. **Post the hello on a yes**, by the recipe the plan carries, and say in the
    report what happened: posted, handed over for pasting, or declined.

## Step 6 — Hand back the setup script

`docs/adopting/web-remote.md` § "Hand the operator a setup script" is the one
step no agent can apply: the environment setup script lives in Claude Code's
environment settings, is set by a human in the web UI, and has no API, MCP tool
or in-repo file behind it. Step 5 deletes that file, so the deliverable travels
here instead — **text in the report** the operator pastes into the setting.

Two reasons it matters:

- **It is where `gh` comes from when the base image lacks it.** The image ships
  `gh` and `jq` with no apt package lists, so a bare `apt-get install -y gh`
  fails the whole script with exit 100; install guarded, as item 5 below.
  Without `gh` on `PATH` there is nothing for the proxy shim to wrap, and every
  `gh`-dependent skill fails later, far from the cause — so
  `.claude/hooks/gh-shim.sh` reports the missing install into the session
  context. That notice is the one part of this step that detects itself.
- **It is the only place a toolchain version can be pinned** for remote
  sessions, and `scripts/vet.sh` running under the wrong one is a confusing
  failure.

It runs **once, when the environment snapshot is built**, then is cached
([docs](https://code.claude.com/docs/en/claude-code-on-the-web#setup-scripts)) —
which is why `.claude/hooks/install-deps.sh` re-syncs dependencies on every
session start rather than trusting the snapshot.

**Where it goes**, since "the settings" is not enough to find it: in the session
composer, the environment picker → **Cloud** → the environment itself, whose
**gear icon** opens its settings. It is per-environment, so an operator with
several is editing one of them rather than a global.

Write the script for the stack the brief names, and carry these across whatever
it is — each records a trap that actually bit:

1. **No top-level `cd` into the repo.** At setup-script time the repo is not
   reliably at `/home/user/<project>`, and a `cd` there crashes the script.
2. **Pin versions as literals**, with a comment naming the repo file each pin
   must track. Reading `.nvmrc` or `.tool-versions` needs the repo, which brings
   back 1.
3. **Reach non-interactive shells.** A profile edit alone does not; symlinking
   the toolchain into `/usr/local/bin` does.
4. **Check what the base image ships and where it sits on `PATH`.** Base images
   carry their own toolchain directories, and some sort _earlier_ than
   `/usr/local/bin` — so `which` keeps resolving a stale binary past a correct
   symlink. Look for that shape before assuming yours won.
5. **`gh` and `jq`, guarded** — per above:
   `command -v gh >/dev/null && command -v jq >/dev/null || { apt-get update && apt-get install -y gh jq; }`.
6. **Prime the dependency cache last**, guarded, since the repo directory may be
   absent.

**If the fork kept `.claude/costs/`, the same settings take its telemetry
variables** as environment variables, the list being the one
`.claude/costs/hooks/start-telemetry-receiver.sh` prints.

Say plainly in the report that these are the steps you could not apply yourself.

## Step 7 — Hand over the first build session

The prune lands as a PR like any other work, so the report closes on the command
that starts the project once it merges — the same shape `/plan` hands over, one
stage later:

```
/task <the issue's title> #<N>
```

A fresh session, because this one's context is the template it just deleted.
Where Step 5.5 filed no issue, hand over `/task <the brief>` instead.

## Recognizing an undetemplated fork

A session that opens in a fresh fork and is asked to build a feature should
route here first, rather than building product code on top of the template's
inventory. The signal is Step 0's predicate read positively: a
`.claude/skills/*/catalog.md` present, and `origin` not matching the `repo`
field in `.claude/skills/update-muthur/watermark.json`.

**Nothing here is what routes a session — the frontmatter is**, this section
being what gets read only once the description has sent someone to it. So the
description names the _repository_ rather than the situation: the template is a
literal `owner/repo`, checkable against the working directory in the reader's
own system prompt at no round-trip, and every other tree carrying the
description is a fork to route.

`CLAUDE.md` § "About this project"'s stub is the second surface, catching a
session that never consults the skill list: while that stub is unfilled and the
tree still has the catalog, the first task is `/detemplate` whatever was asked.
Step 5.4 rewrites that stub, so the notice retires with the condition it
describes.

**Nothing anywhere `@`-references this skill's own `SKILL.md`** — every mention
is a bare name, this sentence included. Step 5.8 deletes the skill, so such a
pointer would dangle in the tree of whoever just ran it and fail
`check-skill-catalog.sh` assertion 1 — the same property that makes
`/test-on-gh`'s bare-name mentions correct to leave alone (the catalog's §
"Reverse closure").
