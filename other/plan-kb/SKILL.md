---
name: plan-kb
description: Create or evolve a durable Markdown plan inside a hraness/wordcell vault. Use when a user asks for an implementation plan, proposal, RFC, migration plan, execution audit, phased checklist, or an update to an existing plan's decisions, progress, review findings, verification evidence, or final result.
---

# Write a durable plan

Keep the plan useful before, during, and after execution. It is the coordination
record, not a disposable answer or a duplicate task tracker.

## Find the plan's owner

1. Resolve `<vault>` to the directory containing its authored or managed
   `index.md` front door, then
   set the shell-local `KB_ROOT` to that path (`KB_ROOT=kb` from a typical
   repository root, or `KB_ROOT=.` from inside the vault). Read the vault's
   `AGENTS.md` and the nearest guide under `<vault>/plans/`. Pass that resolved
   root to every command; do not assume the starting directory is the vault.
2. When the plan owns a repository path, resolve the repository root as
   `KB_REPO` and load that path's current memory before a whole-vault search:

```sh
wordcell context "<repository-path>" --root "$KB_ROOT" --repo "$KB_REPO"
```

Use `--kind file` or `--kind directory` when an absent future path cannot be
classified from the filesystem. Read the inherited guides first, then the
applicable maintained knowledge, active plans, dated research, reports, and
separate historical-plan group.

3. Search existing plans before creating one:

```sh
wordcell list --root "$KB_ROOT" --where type=plan --sort area --json
wordcell search "the intended outcome" --root "$KB_ROOT" --json
```

If `wordcell` is not installed, do not let retrieval tooling block the plan: use
`rg` or the available file search over `<vault>/plans/`, titles, aliases, and relevant
terms. If the directory is not an initialized hraness/wordcell vault, follow the
repository's existing planning convention instead of initializing one without
being asked. Semantic search writes only a derived local cache; when that cache
location is not writable, use exact search or point `XDG_CACHE_HOME` at a
writable cache directory.

4. Update an existing plan when it already owns the outcome. Create a new file
   only for independently executable work.
5. Use `<vault>/plans/<descriptive-kebab-name>.md` unless the local guide already groups
   plans by area. Do not reorganize older plans merely to impose a new tree.

## Write from evidence

Read [the plan structure reference](references/structure.md), then tailor it to
the work. Preserve these invariants:

- State one concrete outcome and the current status.
- Record what is known, what is assumed, and what remains to discover.
- Separate in-scope work from non-goals.
- Put constraints and decisions before the steps they shape.
- Make dependencies and ordering visible.
- Give each acceptance claim a verification method.
- Include rollback or recovery when a change can leave durable state behind.

Turn a missing implementation detail into an ordered discovery gate when the
outcome and authorization are already clear and the decision can be made from
in-scope evidence. Stop and request direction when the unknown would change the
intended outcome, expand authority or external coordination, or choose between
materially different products.

Use small frontmatter. Start with `type: plan`, a descriptive title and
one-sentence description, a kebab-case `area`, and one of `proposed`,
`accepted`, `in-progress`, `blocked`, `completed`, `superseded`, or `cancelled`.
When the plan owns work in a code repository, add `repository_scopes` with the
few exact canonical repository-relative files or directories it explains. Use
no globs. A future path is valid; update an active plan deliberately when code
moves instead of relying on inferred Git renames. Add aliases or tags only when
they help humans or structured queries.

## Grow the same file during execution

- Change status when reality changes, not in anticipation.
- Check off completed work without deleting the original intent.
- Incorporate decisions, review findings, deviations, and command or test
  evidence where a future reader can understand their consequence.
- When blocked, name the exact missing condition and the safe work already
  completed.
- When a plan becomes `completed`, `superseded`, or `cancelled`, write a
  non-empty `## Result` and `## Durable memory`. State what shipped or why work
  stopped in Result. In Durable memory, link each reusable conclusion to the
  maintained note, guide, documentation, or checked code contract that now owns
  it. When nothing warrants promotion, say so explicitly and give the reason.
  Retain the terminal plan as history.
- Do not create separate progress, review, or completion files for the same
  plan.

## Connect and verify

Add wikilinks or typed relationships only where the prose and evidence explain
a useful connection. Review the changed plan for reusable concepts before
refreshing:

```sh
wordcell percolate "<plan-note-id>" --root "$KB_ROOT" --limit 25 --json
wordcell refresh --root "$KB_ROOT"
wordcell check --root "$KB_ROOT"
```

Run those commands when the plan lives in an initialized hraness/wordcell vault. In a
repository-native planning directory, use that repository's own validation
instead. Review broken links first, then inspect orphan and mention advisories
in context. Promote only concepts likely to be reused, and ground every typed
relationship in the plan's prose. An independently useful plan may legitimately
remain an orphan in a new or sparse vault. Record that disposition mentally or
in the task handoff; do not manufacture links or relations merely to improve
graph counts.

In an authored-catalog vault, refresh leaves the front door unchanged and `wordcell
catalog --root "$KB_ROOT"` renders an exhaustive disposable inventory. In a
managed vault, independent edit lanes use `wordcell check --root "$KB_ROOT"
--no-catalog`; the integrating lane performs the single catalog refresh.
