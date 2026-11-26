---
name: readme
description: "Writes or reviews a repository README in one house style with a fixed section order, bullets instead of paragraphs and no badge wall. Use when a repository needs a README, an existing one has drifted from the code, or someone asks to write or review a README."
---

# Readme

Produce a short, accurate README in one house style across repositories.

## When to use

- A new repository needs a README.
- An existing README has drifted from the code.
- A change touched the install steps, configuration or commands.
- Depth beyond a README belongs in `docs/`, not inlined here.

## Steps

1. Read `AGENTS.md` for `## Deviations`. An entry about the README, for example a dropped
   section, overrides the matching rule below. Everything else still applies.
2. Read the entry point, task runner, CI workflows, config loading, chart values or
   OpenTofu variables first. Every command and option comes from there.
3. Write the sections in this order, dropping one only if it does not apply: title and
   one line, What it does, Install, Use, Configuration, Development, License.
4. What it does: one or two sentences, what it is and who it is for.
5. Install: the shortest path from clone to running, with commands actually executed.
   Name prerequisite versions if they matter.
6. Use: the two or three things people actually do, with real input and output. Link
   `docs/` for the rest.
7. Configuration: a table of name, purpose, default, required, sourced from the code.
8. Development: build, test, lint, run locally, preferring the repository task runner.
9. License: name plus link to the `LICENSE` file.
10. Verify: run the commands, open every link, diff the configuration table against
    the code.
11. Keep it one or two screens. A section that grows past that moves to `docs/` and
    gets linked.

Review pass for an existing README: stale claims (removed or renamed features, changed
flags), missing or changed configuration, dead links, template leftovers (placeholder
names, `TODO`, scaffold URLs), install steps that no longer work, sections out of order,
a release status or a count that goes stale on its own.

## Guardrails

- `## Deviations` checked before writing or reviewing.
- A change gets documentation where a reader needs it.
- Fixed section order followed, sections dropped only when they do not apply.
- No marketing filler, no emoji, no badge wall, no roadmap or changelog section.
- Only commands that exist in the repository and were run.
- Configuration table matches the code, defaults included.
- All links resolve. Depth linked to `docs/`, not inlined.
- Releases are described as driven by the repository's release tool (release-me or
  release-please). `CHANGELOG.md` is never hand edited.
- Never state a release status or an implementation count as current fact when it
  depends on something outside this file: a release being cut, a package added, a
  version tagged. Name what exists, or point at the thing that is always current,
  instead of asserting a snapshot in prose.

## References

- `adr` for decisions, `concept-doc` for designs before implementation.
