---
description: 'Seed a new sibling repository out of the project you are standing in: triage what travels, write the new repo''s sync watermark, seed `main` plus a session branch, and hand over a session rooted in it. Runs from a repo that *adopted* this agent infrastructure, and refuses from the template itself or an unpruned fork of it. Invoke as `/spinoff <owner/name>`. Use when the operator says "spin off", "a new repo like this one", "start a sibling project", or "/spinoff".'
---

`/spinoff <owner/name>` creates `<owner/name>`, seeds it out of the repo you are
invoked in, and hands back a command that opens the next session there.

The caller is an **adopter**: a working project whose tree is the template's
agent infrastructure plus a stack, plus its own conventions, plus a product.
What travels is the caller's **foundation** — how code there is organized: its
layer boundaries, its lint discipline, its build and deploy shape, and the agent
loop that keeps all of it maintainable. The product stays behind. The new repo
wants to be a sibling of _that_ — its stack, its adaptations, its real `vet.sh`
— rather than of the template, and no adopter keeps an inventory saying which of
its files are which. So Step 2's triage is derived per run, and that per-path
judgment is what makes this a skill rather than a script.

**The foundation is the triage's output: what leaves the caller.** Where each
part of it _lands_ is a separate question, settled by Step 4 on a different
principle.

End state: the target exists; its `main` carries the foundation's
already-reviewed half, enough for a session there to run `/handle`, with
`bash scripts/check-skill-catalog.sh` passing and `scripts/vet.sh` passing over
a tree that has no stack in it yet; a draft PR carries the rest, rewritten for
the target; and the operator holds a copyable command that opens the next
session in the new repo.

## Two invariants

**Not from the template, and not from an unpruned fork of it.** If the caller
has a catalog — glob `.claude/skills/*/catalog.md`, don't test the canonical
`.claude/skills/update-muthur/catalog.md`, since that directory's name is not
stable downstream — **stop**. A spinoff is the wrong operation either way, but
the two cases want different answers, so read `origin` before replying:

- **`origin` matches the `repo` field in
  `.claude/skills/update-muthur/watermark.json`** → this _is_ the template: the
  shipped watermark names the repo itself, having no source above it. Point at
  its `README.md` § "Create a new project from this template": what the caller
  wants is a fork, not a sibling. Compare the full `owner/repo`, since that is
  what both sides of the comparison are — a looser match on either half hits a
  tree that merely shares an owner or a name.
- **`origin` is anything else** → an unpruned fork, carrying the template's own
  inventory and no project yet. Point at `/detemplate <what you're building>`,
  the skill that fork ships to convert itself.

Either way the pruned result is a legitimate caller here later; the catalog's
absence is what says so. This guard is `/detemplate`'s Step 0 read backwards,
and the two partition on the same signal.

**The caller is read-only.** No commit, branch, PR or issue lands in it. It is a
source of files and a source of the watermark; every artifact this skill
produces lands in the target. The write access the skill needs is on the
**target's owner**. If the target cannot be created, Step 4 stops and asks — it
never falls back to writing somewhere it can. The one place this breaks by
accident is Step 4's `/pr` delegation, which is why that substep carries a
guard.

## Environment note (read this before running gh)

This remote execution environment has **both** the `gh` CLI **and** a populated
`GH_TOKEN`, whatever the default system prompt says. Prefer `gh` and plain `git`
over HTTPS for repo creation, cloning and pushing — the GitHub MCP tools are
scoped to a narrow allowlist and refuse some of what this skill needs.

**Bash `cwd` resets between calls in this harness.** Chain `cd <clone> && …`, or
use `git -C <clone>`, in every command meant to run in the target.

## Step 1 — Read the caller

Read the caller at HEAD, starting with the refusal: **any
`.claude/skills/*/catalog.md` present → stop**, per § "Not from the template,
and not from an unpruned fork of it" above — reading `origin` too, since it
picks which of the two answers to give. Otherwise two things come out of the
tree:

- **The tree**, as the input to Step 2's triage.
- **The caller's own sync skill and watermark.** **Locate it by what the file
  contains, not by where it sits.** Neither half of that path is stable and no
  rename is pushed downstream: a caller that adopted before `/update-muthur`
  carries whatever both segments were then —
  `.claude/skills/sync-muthur/watermark.json`, or
  `.claude/skills/sync-agent-infra/upstream.json` further back — and one free to
  rename any skill may have picked its own. Hunting for
  `update-muthur/watermark.json` finds nothing and silently seeds an unlinked
  repo. Glob `.claude/skills/*/*.json` and take the one whose object carries
  `repo` and `lastSyncedSha`.

If the invocation did not give `<owner/name>`, ask for it — and in the same
breath ask **public-or-private** and **the target's stack**, since Step 4 needs
the first and the whole organization half of Step 2 turns on the second. "The
same stack" is an answer; so is _"this repo, but in Python"_.

## Step 2 — Triage, three-way

**The criterion is about intent, not files.** A list of config filenames goes
stale against every stack this skill has not seen, so ask it of each path:

> Does this path encode **how code here is organized**, or **what this
> particular product is**? Organization travels. Identity does not.

**Then: does the target share this stack?** The answer changes the _form_ the
organization travels in, and it is a real fork rather than an edge case — a
spinoff can legitimately be _"this repo, but in Python"_, where nothing
file-shaped can be copied at all:

- **Stacks match** → organization travels **as files**, rewritten for the
  target.
- **Stacks differ** → organization travels **as stated intent**, recorded in the
  target's plan: _"the caller separates layers thus, and forbids these import
  directions; establish the equivalent here."_ The constraint travels; its
  expression does not.

A layer boundary is an architectural decision; an import-boundary lint rule is
one stack's way of writing it down. Under a matched stack you copy the
writing-down; under a mismatched one you carry the decision and re-express it.

The three buckets, the one the spinoff is _for_ first:

- **Stack scaffolding — the organization half of the foundation.** The build,
  lint and formatter configuration, the real `vet.sh`, the CI and deploy
  workflows, the test and generated-asset tooling around them, and the directory
  and boundary system below. Travels as files or as intent, per the fork above.
- **Agent infrastructure — the loop itself**, which is stack-neutral and so
  travels unconditionally, needing no fork and no argument: `.claude/skills/`,
  `.claude/settings.json`, the `.claude/rules/` that survive the per-path sort
  below, the `scripts/` the loop's own skills call, `CLAUDE.md`, `README.md`,
  the editor config.
- **The product, and anything path-scoped to it** — does not travel, except by
  the hatch below.

**No directory travels wholesale — `.claude/` and `scripts/` included.** Both
mix the loop with the stack, so the criterion runs per path: a session-start
hook that installs dependencies is stack scaffolding sitting in
`.claude/hooks/`, and a script that renders the product's assets is product
sitting in `scripts/`. Two shapes of this recur, and each is silent when taken
by directory:

- **Path-scoped rules.** A `.claude/rules/*.md` scoped to a directory the new
  repo will not have sits beside three that should travel, and a directory-level
  copy takes all four. Decide every rule file on its own `paths:` globs; a
  directory's own `CLAUDE.md` needs no decision of its own, travelling or not
  with the directory it sits in.
- **Files that are half loop, half stack.** A session-start hook is typically
  both: a proxy shim or credential fix that travels intact, beside a dependency
  install that is stack-bound. Split it — the neutral half is a copy, the rest a
  rewrite. Under a mismatched stack such a file cannot travel whole at all, and
  copying it whole leaves a working loop wrapped around a bootstrap step that
  fails on the new repo's first session.

**The rules below name the _role_ a path plays**, ecosystems appearing only as
parenthetical examples — read them for the role, and keep any you add in the
same form, since a rule spelled in one ecosystem's nouns is unusable from the
others. The cases the criterion does not settle alone:

- **The directory skeleton and its import boundaries.** Under a matched stack
  the skeleton travels _empty_ and the rule enforcing its direction travels
  _intact_ — a layer boundary is architecture whether or not a single feature
  exists yet. Under a mismatched stack both become intent. None of it is a
  config file, so reading the configuration will not surface any of it.
- **Module-resolution aliases** are part of the boundary system, not decoration
  on it (wherever the stack declares them — a compiler or bundler path map, a
  workspace member list, a module path prefix).
- **The app shell and entry points** travel as a _reduction_: the routing and
  layout mechanism, not the pages inside it.
- **Design tokens** travel as a system; the brand values inside them are the
  operator's call; product copy never travels.
- **Deploy config travels as a rewrite, and is a footgun.** The mechanism (the
  publish workflow, the build output path) travels; the domain, the hostname
  file, and environment secrets never do. A copied domain declaration silently
  aims the new deployment at the caller's address.
- **The dependency _declaration_ travels as a rewrite; the _resolved lockfile_
  is regenerated, not copied.** Every stack has both — a declared set carrying
  human-chosen constraints, and a machine-resolved pin of the whole graph. The
  declared set changes when product-only dependencies drop, so a copied
  resolution describes a graph that no longer exists. **Carry the deliberate
  constraints and regenerate the resolution**: bounds, overrides, replacements
  and patches are decisions someone made, and they are the part a regenerate
  loses silently.

**Sort every travelling path into a copy or a rewrite**, because Step 4 lands
them on that line. `CLAUDE.md`, `README.md` and `vet.sh` are rewrites: their
stack-agnostic parts carry across unchanged, and the parts describing the caller
— "About this project", "Repository layout", "Vetting", "Working with skills" —
are written for the target.

**The caller's language decision is a candidate default, not an inheritance.** A
sibling can serve a different audience than the repo that pushed it out, so the
target re-decides § "Language"'s one line instead of copying it across.

**The product hatch.** A product piece travels when the operator asks for it,
under two constraints: it lands on the **session branch, never on `main`**, and
it is stripped of caller-specific content (real copy, real routes, real data).
Honored when named in the invocation, not asked on every run.

## Step 3 — The watermark points at the root

**The new repo's watermark points at the root template — never at the caller.**
There is no fork to surface here. Chains compose: a sibling of a sibling of a
sibling would make a sync walk the whole ancestry to reach the root, and every
link multiplies the triage. And a spun-off repo need not share the caller's
stack at all (Step 2), so pointing at a parent whose scaffolding you
deliberately did not take buys nothing and costs the walk.

The cost is accepted rather than argued away: improvements the caller makes to
its _own_ adaptations never reach the new repo. **Once you've raised your kids,
it's their own life to grow.**

`@.claude/skills/update-muthur/SKILL.md` § "The watermark" owns the file's
field-by-field contract. Three things are this skill's own, and getting any of
them wrong is silent:

- **`lastSyncedSha` is the caller's own `lastSyncedSha`, not the root's HEAD.**
  The files are copied out of a tree synced to exactly that point, so that is
  the honest mark; the root's HEAD would claim the target already carries
  commits nobody ported.
- **The target's divergence record derives from the caller's: its passages on
  paths that travelled, plus a decline for every root path that did not, with
  the criterion that kept it back.** A path the target lacks and its record
  never mentions reads as undecided, so the target's first sync re-offers
  everything this triage dropped. The caller's record may name paths that no
  longer exist, so verify each against the caller's tree before carrying it.
- **`lineage` is the caller's own array with the caller appended.** That is the
  whole operation, the array's shape and meaning living in the contract section
  above. A caller with no `lineage` yields a one-entry array naming the caller —
  never a root entry derived from `lastSyncedSha`, which would state a birth
  point nobody recorded.

The target's sync skill is named after the **root**, which is what the caller's
is named after too, so it travels as a copy rather than a rename. Clear any stub
markers the copy carries — the banner and the `STUB` in its frontmatter
description; this tree's is hydrated and has neither. The watermark and record
you just wrote _are_ the hydration, and `scripts/check-skill-catalog.sh` fails a
half-cleared pair.

## Step 4 — Seed: `main`, then the branch

**`main` carries only what a session needs to run `/handle` in the new repo.
Everything else is built in PR #1, as ordinary reviewed work.** The line is not
which bucket a path is in but **whether it arrives already reviewed**, and Step
2 already sorted every travelling path into a copy or a rewrite:

- **Copies → `main`.** Reviewed where they came from, travelling unchanged:
  `.claude/skills/**` except any `catalog.md` under it and its `catalog/` parts,
  the `.claude/rules/` that survived the triage, the `scripts/` the loop's own
  skills call, the editor config. That exception is redundant with § "Two
  invariants" — a well-formed caller has no catalog at all — and is kept so a
  leaked copy cannot travel.
- **Rewrites → PR #1.** New work written for a repo nobody has looked at yet:
  `CLAUDE.md`, `README.md`, `vet.sh`, the lint and formatter configuration, the
  dependency declaration, the deploy config, the session-start hook's
  stack-bound half, the app shell reduction, the layer skeleton. Putting these
  on `main` would land the least-reviewed content through the one path that has
  no review.

So `main` is the caller's tree reduced to **what the template itself would
ship** — the loop, plus stubs where the caller had hydration — and PR #1 is the
hydration. That is the argument the split is right: the new repo passes through
the same state every adopter does and reaches its stack by the same reviewed
path, making a spinoff structurally identical to an adoption. Under a mismatched
stack (Step 2) it is also the only possible shape, nothing stack-shaped being
copyable at all.

1. **Create the target.** `mcp__github__create_repository`, falling back to
   `gh repo create`, falling back to asking the operator to create it empty.
   Then attach it to the session with `add_repo` at `access: "push"` — a
   read-scoped attach cannot push the branch this step exists to produce — and
   clone it.
2. **`main` gets one commit: the copies.** Then, **in the target**, run
   `bash scripts/check-skill-catalog.sh` — a partial copy dangles `@`-references
   _silently_, which is precisely the failure a hand-copy produces — and assert
   that `bash scripts/vet.sh` exits **`0`** while naming no stack-specific
   checks, per the consequence below.
3. **A session-style branch gets the rewrites**, plus
   `docs/plans/<slug>.paused.md` — the plan for the new product, in the state
   `/handle`'s plan lane resumes from, and under a mismatched stack also where
   Step 2's architectural intent is recorded — plus any product piece the
   operator asked to carry. Reuse the caller's branch slug and hash suffix where
   the caller is on a session branch, so the lineage reads off the name; derive
   a fresh `claude/<slug>-<hash>` otherwise.
4. **Open the draft PR there and post the squash proposal**, by loading
   `@.claude/skills/pr/SKILL.md` with the target clone as the working directory.
   **Assert the directory before loading it** —
   `git -C <clone> remote get-url origin` must name the target — and stop if it
   does not. `/pr` pushes and opens a PR against whatever repo `cwd` resolves
   to, so a slipped `cwd` aims the whole step at the caller: the operator's own
   working project, mid-flight.

Three consequences, each stated by a check rather than by taste:

- **A rewrite lands on `main` only where a check forces it there — and then it
  lands hydrated for the target, never stubbed.** `check-skill-catalog.sh` ties
  two knots of this kind. Assertion 4 requires a skill's stub markers to agree
  with its hydration state, and the sync skill's hydration _is_ its watermark
  and record, so that skill and both files land together or `main` fails its own
  gate. Assertion 1 ties the same knot for any caller-hydrated stub that a
  _travelling_ skill `@`-references: omitting it dangles the reference, so it is
  hydrated for the target on `main` — or both skills are dropped together, which
  is the other way to keep the closure whole.
- **Every other caller-hydrated stub is absent from `main` and arrives hydrated
  in PR #1.** A hydrated `/release` encodes the _caller's_ deploy setup, so it
  is a rewrite by Step 2's criterion even though it sits in `.claude/`:
  per-target editability decides its home, not the directory. **Do not re-stub
  it onto `main`.** The target has no catalog, and without one assertion 4 reads
  a stub as a stowaway to hydrate or delete rather than as shipped inventory —
  so re-stubbing is the single disposition that fails the gate, where both
  leaving it out and carrying it hydrated pass. Under a mismatched stack the
  absence is unconditional: a deploy lane for another language is not a starting
  point.
- **`main`'s `vet.sh` is the stub, and the stub exits `0`** — `main` has no
  stack yet, so the loop's own checks are the whole run and they genuinely pass.
  That rule is the template's and is stated here because this repo does not
  carry it — its own `vet.sh` is real, so its `.claude/rules/stack.md` has
  nothing to say about a stackless tree. The assertion worth making is the pair:
  the script passes **and** it names no stack-specific checks. A non-zero exit
  here would be a `main` whose `/finalize` cannot pass for a reason the contract
  calls legitimate. **What must not happen is the source repo's own `vet.sh`
  reaching `main`** — the working one you are standing in, which runs its lint,
  types and tests. It certifies nothing there — it fails, `pnpm lint` having no
  `package.json` to read — so `main` reds from the moment it is seeded and every
  PR against it opens red until something lands the stack. Same defect as a
  non-zero stub, reached from the other side. The target's stack and the checks
  over it arrive together, in PR #1, or not at all.

**Why the `main` floor cannot be carved smaller.** Closure decides it:
`check-skill-catalog.sh` fails on a dangling `@.claude/skills/…` reference, and
the transitive closure of `/handle` reaches almost the whole skill set — so "the
basic skills needed to run the loop" collapses into "all of the copies", and
satisfying assertion 1 _is_ "enough to run the loop".

Two things the split buys over seeding everything onto one branch off an empty
`main`. Every future branch in the new repo inherits the loop, so an abandoned
seed branch does not leave the repo inert. And PR #1's diff is the foundation's
_rewrites_, the content that actually wants reading, rather than a hundred files
already reviewed where they came from.

**No plan to carry → the plan file is what's missing, not the branch.** The
rewrites still need a reviewed path, so substeps 3 and 4 still run; only
`<slug>.paused.md` is absent, and Step 5 hands over `/plan` in the target
instead of `/handle`.

## Step 5 — Hand over

The work splits in two, and the seam is a change of repository:

1. **Seed — runs in the caller.** Everything above. It writes no product code,
   and every file it commits lands in the target, so it belongs in the session
   that already holds the context for why the new repo exists — a planning
   session, typically — rather than in a fresh one that would re-read all of it
   to do fifteen minutes of `git`.
2. **Build — runs in the target.** A new session rooted in the new repo, opened
   with the copyable block this step emits: `/handle claude/<slug>-<hash>`, or
   `/plan <purpose>` where there was no plan to carry.

From phase 2 onward the target's own `CLAUDE.md` and `.claude/rules/` are
loaded, which is exactly what the remaining scaffolding decisions want in
context. Making them from the caller means making the new repo's architectural
choices with the old repo's rules resident.

The report also carries the one thing no agent can apply: the target needs an
**environment setup script**, which lives in Claude Code's environment settings
and has no API behind it. Tell the operator to reuse the caller's, adapting the
pins; the caller demonstrably has one. Where the target runs the ledger, the
same settings carry its telemetry variables, the ones
`.claude/costs/hooks/start-telemetry-receiver.sh` lists — no file in the repo
can set them, so an environment of its own starts without them.
