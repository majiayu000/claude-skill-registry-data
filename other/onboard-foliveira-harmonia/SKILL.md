---
name: onboard
description: Harmonia onboard - capture an existing repo's canonical verify commands into .harmonia/project.yaml. Use ONLY when explicitly invoked as /harmonia:onboard.
disable-model-invocation: true
---

Your working contract is the rules; their digest is injected at session start - read `${CLAUDE_PLUGIN_ROOT}/core/RULES.md` in full only if that digest is not in your context.

Attach Harmonia to a repository it did not scaffold. You capture the repo's own
verify commands into `.harmonia/project.yaml` so the scoper authors success
criteria against the repo's real commands.

This is not a lifecycle stage: it mints no task workspace and writes no marker or
receipt. It writes exactly one file - `.harmonia/project.yaml` at the repo root -
which the onboarded repo is meant to commit. On a second run it refines that file
in place; see step 3.

The interview, the run-before-record step, and the refine step are yours to carry
out honestly. They are a prose contract, on the same footing as human acceptance
today, not a technical guarantee.

## The file you write

`.harmonia/project.yaml` is flat: one scalar per line, known keys only, no nesting
and no arrays, so each value sits on a single physical line.

```yaml
# .harmonia/project.yaml - this repo's canonical verify commands. Read by the
# scoper. Written by /harmonia:onboard; safe to hand-edit; commit it.
test: <shell command>
lint: <shell command>
typecheck: <shell command>
build: <shell command>
```

Each value is a single bare command on one physical line. The scoper copies it
verbatim into a `- run:` criterion, so leave no `#` on a value line - it would
become part of the command. Typical values: `go test ./...`, `npx vitest run`, or
`bats tests/` for `test`; `golangci-lint run` or `npm run lint` for `lint`;
`tsc --noEmit` or `npm run typecheck` for `typecheck`; `go build ./...` or
`npm run build` for `build`.

## Steps

1. **Interview for the four verify commands - do not guess them.** Elicit this
   repo's canonical commands in four categories from the developer: `test`, `lint`,
   `typecheck` (or `type-check`), and `build`. Ask; do not infer them from a glance
   at the tree.

2. **Prove each verify command works before recording it.** The discipline is:
   prove it works before recording it. Run each candidate once, from the repo root,
   and record it only when it exits 0. Reject it on ANY non-zero exit - gate on
   non-zero, not on an enumerated code set. Judge it by exit status, never by
   pattern-matching its output. A command that does not run is not written as if it
   did.

3. **Refine in place on re-run.** One `.harmonia/project.yaml` per repo. If the
   file already exists, read it and update only the keys that changed, preserving
   the rest; never clobber it from scratch. A second run refines the file in place.
   Preserving a key is not certifying it: a value you did not receive from the
   developer this session stays in the file un-run, and you tell them that is what
   happened. Running it to "check it still works" is executing input you did not
   author, which is the one thing this step must not do. A repository you cloned
   can carry this file, and a scoper copies its values verbatim into `- run:`
   criteria that execute at review.

A `coverage:` key left in the file by an earlier version is no longer read by
anything. Tell the developer it is there and that they can delete it.
