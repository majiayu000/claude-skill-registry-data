---
name: whatsnew
owner: baseline
description: On-demand "what's new" generator. Main context (which knows the impending change) writes keepachangelog-style entries to a fragment file at `.claude/state/whatsnew/<slug>.json` (gitignored, transient). An optional per-project `project.json → whatsnew.route_workflow` names a routing workflow that consumes the fragment and renders it wherever the project wants (a site page, a release body, a docs page). Not a workflow phase — it never blocks a commit, and it never writes `CHANGELOG.md` (that file is owned solely by semantic-release in CI).
argument-hint: "--slug <slug> --entries-file <path>"
---

# whatsnew — on-demand generator

Emits a structured "what's new" fragment for a set of changes. The fragment is a gitignored handoff buffer; a per-project routing workflow turns it into whatever surface the project wants. The generator makes no assumption about the destination, and it never touches `CHANGELOG.md` — semantic-release owns that file at release time.

This skill is **not** a mandatory workflow phase. It is invoked on demand (and, when a project wires `whatsnew.route_workflow`, handed off to that routing workflow). Version is never stored in the fragment: the routing target reads the shipped version at publish time.

## Steps

1. **Build the entries (main context).** Decide the keepachangelog entries for the change — one object per user-visible change, not per file. Write a JSON array to an entries file (for example under `.claude/state/whatsnew/`), each object shaped `{ "category": "<Added|Changed|Deprecated|Removed|Fixed|Security>", "title": "<short headline>", "body": "<one or two sentences>", "highlight": <bool, optional> }`.
2. **Run the generator.** Invoke the entrypoint with `--slug <slug> --entries-file <path>` (optionally `--project-root <root>`). It validates the entries, writes the fragment to `.claude/state/whatsnew/<slug>.json`, and resolves the optional routing target.
3. **Routing (optional).** If `project.json → whatsnew.route_workflow` names a workflow, that workflow is the documented consumer of the fragment; it reads the fragment and writes its own committed output. If the knob is absent or `null`, the generator still succeeds and the fragment simply sits at the conventional path unconsumed.

## Companion files

- `whatsnew.mjs` — the generator entrypoint. Reads the entries file, writes the fragment, reports the routing target.
- `fragment-writer.mjs` — validates entries and serializes the fragment `{ slug, generated_at, entries[{category, title, body, highlight?}] }`. No version field.
- `route-resolver.mjs` — resolves `project.json → whatsnew.route_workflow` (string track id, or `null` by read-time default).
- `classifier.mjs` — defines the canonical keepachangelog category set that `fragment-writer.mjs` validates entries against.

## Constraints

- **Never writes `CHANGELOG.md`.** That file is owned by semantic-release in CI. The generator only ever writes the gitignored fragment.
- **No stored version.** The version is read at publish time by the routing target, never written into the fragment.
- **Transient fragment.** `.claude/state/whatsnew/<slug>.json` is gitignored; a routing workflow that needs persistence commits its own rendered output, not the buffer.
- **Routing is the project's concern.** The generator is generic; it makes no assumption about where the fragment ends up. Projects with no routing target simply leave `whatsnew.route_workflow` unset.
