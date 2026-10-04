---
name: release-template
description: Safely release the canonical Copier template by inspecting changes since the latest SemVer tag, proposing the next version, validating the template, requesting explicit approval, and then creating and pushing the exact tag. Use when the user invokes `/release-template` or asks to version, tag, publish, or release `Llamitai/wise` to `Llamitai/saas-bootstrap-template`.
disable-model-invocation: true
---

# Release Template

Release only the canonical `Llamitai/wise` template. Deduce a SemVer bump from
the delivered changes, but treat it as a proposal that requires explicit user
approval.

## Safety contract

- Never create or push a tag before the approval gate below.
- Never push `main`, use `--tags`, force, delete, move, or recreate a tag.
- Never edit or push the generated mirror directly.
- Stop on every failed guard or validation. Do not work around the script.
- A push rejected by a tag protection rule or ruleset is a stop condition;
  report it and never bypass it.
- Do not interpret prior approval, silence, or an ambiguous response as approval
  for the current tag and SHA.

## Locate the bundled script

Resolve the absolute directory containing this loaded `SKILL.md`. Use
`<skill-dir>/scripts/release_template.py` regardless of whether this skill was
loaded from `.claude` or `.agents`. Do not assume the
script is under the repository's top-level `scripts/` directory.

## 1. Inspect without mutation

From anywhere inside the target repository, run:

```bash
python3 <skill-dir>/scripts/release_template.py inspect
```

The command emits one JSON object. If it exits non-zero, report its `message`
and `action`, then stop. In particular, do not create a new release while the
previous canonical tag is absent from the template mirror.

Keep the returned `previousTag`, `previousSha`, `headSha`, `headSubject`, and
`candidates`. Treat them as one proposal snapshot.

## 2. Assess the changes

Use the exact SHAs from `inspect`:

```bash
git log --format='%h %s%n%b' <previousSha>..<headSha>
git diff --stat <previousSha> <headSha>
git diff --name-status <previousSha> <headSha>
```

Inspect the relevant full diff before classifying it. The tree diff is the
authoritative release delta even when `previousTagIsAncestor` is false; show a
warning in that case. Use Conventional Commits only as supporting evidence.

Choose the highest applicable impact:

- `major`: incompatible generated-project behavior, mandatory manual migration,
  or a broken contract used by generated projects.
- `minor`: a backward-compatible capability, option, or module added to the
  generated template.
- `patch`: fixes, documentation, refactors, dependency maintenance, or release
  tooling without an incompatible new capability.

For ambiguous breaking changes during `0.x`, explain the ambiguity. Select
only the immediate `patch`, `minor`, or `major` value returned in `candidates`.
Do not invent prereleases, skip versions, or accept a version at or below the
previous tag.

## 3. Validate before asking

Run the repository's template preflight. `check` compares the built template;
`preflight` mirrors the publication workflow locally (render a project, run its
backend and frontend suites, smoke `copier update` from the latest tag) without
pushing anything:

```bash
just template check
just template preflight
```

If it fails, summarize the failure and stop. Do not ask for release approval.

## 4. Present the proposal and stop

Show all of the following:

- previous tag;
- suggested tag and bump level;
- evidence for that classification;
- exact `headSha` and `headSubject`;
- destination `origin` (`Llamitai/wise`);
- warning that pushing the tag triggers template publication.

Ask exactly one explicit question equivalent to:

> Confirm creating and publishing `<tag>` from `<headSha>`?

End the turn and wait. Do not invoke `publish` in the same turn as the question.

If the user selects another candidate, update the explanation and repeat the
full summary and approval gate. If repository state changes, start again with
`inspect` and obtain fresh approval.

## 5. Publish only after approval

After an unambiguous approval of the displayed tag and SHA, run:

```bash
python3 <skill-dir>/scripts/release_template.py publish \
  --expected-previous-tag <previousTag> \
  --tag <approvedTag> \
  --expected-head <approvedHeadSha> \
  --confirm-tag <approvedTag>
```

The script repeats the guards, validates every effective `origin` push URL,
validates the immediate SemVer candidates, creates a lightweight tag, pushes
the approved SHA only to the tag's exact destination ref, and verifies the
remote.

On `pushed: true`, report that the push triggered `publish-template.yml`. On
`alreadyOnOrigin: true`, report that no new push occurred and that the existing
workflow run may still be pending or failed.

## Failure handling

- Preserve a local tag left by a failed push. Never delete it automatically.
- Retry only after a fresh inspection, the same complete summary, and new user
  confirmation. The script may reuse the local tag only when its SHA matches.
- If the approved tag already exists on `origin` at the approved SHA, treat the
  push as idempotently complete; do not claim a new workflow was triggered.
- If any tag points to an unexpected SHA or origin and mirror disagree, stop and
  report the inconsistency.
