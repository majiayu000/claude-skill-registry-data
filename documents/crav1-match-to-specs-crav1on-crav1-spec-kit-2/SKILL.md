---
name: crav1-match-to-specs
description: >-
  Match one or more repos that already make up a system, plus a dump of
  notes, tickets, old docs, diagrams, or screenshots, to docs/system/
  (including glossary.md) and one spec per confirmed slice. When that folder
  exists, write glossary.md if it is missing, or append only words that are
  not already rows. Do not rewrite existing glossary rows. A meaning the
  source does not state is `to be researched`. Repos are evidence of what
  exists. The dump is what to match, not a brief for a new product. Do not
  write application code.
disable-model-invocation: true
icon: search
color: yellow
---

# Match to specs

You are the **parent**. Match existing repos to a dump. Do not implement. Do not plan. Do not commit.

This is not a mode of `/crav1-intake-to-specs`, `/crav1-spark-to-spec`, or `/crav1-ideas-to-spec`. It is not a system-to-architecture pass. Do not send this job to those commands, and do not absorb theirs.

Slice protocol: [references/slice.md](references/slice.md). Landscape diagrams: [references/diagrams.md](references/diagrams.md).

## Inputs

Everything after `/crav1-match-to-specs`, and every `@`, is input.

| Kind | Role |
| --- | --- |
| **Repos** | Evidence of what exists. One or more repos that already make up the system |
| **Dump** | Notes, tickets, old docs, diagrams, screenshots. What to match. Not a brief for a new product |

A one-liner with no repos and no dump: tell them `/crav1-spark-to-spec`. A pile of ideas for a product that is not built yet: `/crav1-ideas-to-spec` or `/crav1-intake-to-specs`. Do not match a greenfield brief against empty code and call the slices done.

## Where the specs go (first response, no map, no files)

Before any map and before any file, ask where the spec files go. Use the questions tool when it is available. Options only. Do not ask them to type a path.

Repos already in front of you are the repos they `@`-mentioned. Include the current checkout when it is one of those repos, or when they `@`-mentioned no repo and this checkout is the system. Do not offer a repo that is only named inside the dump. Do not offer this kit repo unless they `@`-mentioned it as one of the system repos.

1. One option per repo already in front of you, labeled with that repo’s name.
2. Last option: **A new clean repo**.

Stop. Do not read the dump for slices yet. Do not write files.

**Existing repo.** That repo is the only spec tree. Other repos stay evidence. They are listed in `repos.md` and are not given their own `docs/specs/` trees.

**A new clean repo.** Create it only after they pick this option, and only when you are about to write (after the map is confirmed). `git init` a new directory. No remote. No application code. Name it with a short kebab from the system in the dump, or `system` if the dump has no name. Put it next to the other repos when those paths share a parent directory. Otherwise create it in the current workspace. Tell them the path you used. Specs and `docs/system/` go there. The evidence repos are still not spec trees.

## Read and map (no files yet)

Read the repos and the dump. Then propose a map. Do not write files.

For each slice:

- Slug (`docs/specs/<slug>/`) and a short title
- Which repo the slice belongs to (behavior lives there, or would live there)
- First match: **done**, **partial**, or **not in the code**
- Evidence: paths, or none
- Facts you read from the code, and facts that are only in the dump

**Done:** the dump’s claim for this slice is in that repo. Cite paths.

**Partial:** part of the claim is in the code and part is not. Cite the paths that exist. The missing part is the dump’s words.

**Not in the code:** the dump describes it and the repos do not contain it. This slice is not started. Still list it. Do not drop it because it has no code.

On the side, list code no slice covers: repo, path, one line about what it is. Major areas you actually read, not every file. That list is not a guessed spec.

Put every fact you will treat as accepted on the map. A fact you leave off stays inferred.

Stop. They confirm or edit the map. Do not write files. That confirmation is the only product stop before writing. Do not open a mushy interview, an architecture interview, or an export-format question. If they edit the map, the edit is the confirmation. Do not ask again. Use their slugs, repos, and match statuses. A fact they struck, or that you never put on the map, stays labeled inferred if it appears later. Confirming the map confirms the facts they left on it.

## Branch (one for the dump)

If they picked a new clean repo, create it now, before the branch prompt. No commit yet. A repo with no commits skips the prompt.

Follow `/crav1-feature-branch` (drop-in: `.cursor/skills/crav1/crav1-feature-branch/SKILL.md`; plugin: sibling `skills/crav1-feature-branch/SKILL.md`) in the **destination** repo. One branch for the whole dump. Not one branch per slice.

Slug for that prompt: a short landscape kebab, or `system` if unnamed. Specify options: `feat/<that>` first, then `spec/<that>`, stay, or other. Do not write `docs/system/` or specs until that choice is done or skipped. A new clean repo with no commits skips the prompt (feature-branch skip). Do not push. Do not open a pull request.

## Landscape

Write `docs/system/` in the destination from this skill’s `assets/` (same files as `docs/system/_template/`): `landscape.md`, `repos.md`, `diagrams.md`, `glossary.md`. An ADR file comes from `assets/adr.md` only when the table below says to write one.

When `docs/system/` is missing, seed it from the repos and the confirmed match, including `glossary.md` in that same pass. Do not run an intake interview. Do not respec a new product.

| File | Fill |
| --- | --- |
| `landscape.md` | What the repos are, in one short paragraph. Constraints only when a repo or the confirmed dump already shows them. Bulk assumptions are confirmed map facts only. Leave the feature index empty until the specs exist. Add `## Code with no slice` when the map listed uncovered code (repo, path, one line). That note is not a spec. |
| `repos.md` | Every repo in front of you, plus the destination when it is the new clean repo. Status `exists` when the checkout is a real repo; put the URL when you have one. The new clean repo stays without a remote. Boundaries only when the repos already show one. |
| `diagrams.md` | Follow [references/diagrams.md](references/diagrams.md). One context diagram of the repos as they are. Replace the sample. Do not invent services. |
| `glossary.md` | From `assets/glossary.md`, in this same pass. See the glossary rules below. |
| `adr/` | Only where there was a real choice, with real alternatives, already visible in the repos or accepted on the map. Otherwise write no ADR. Hunches are not ADRs. |

**Glossary.** `glossary.md` is part of the landscape, not a feature spec. Source is the repos plus the confirmed dump. Do not invent terms, expansions, or definitions. Do not write TBD or to be decided. A row is only a word or abbreviation that source already uses. When that same source already says the expansion or meaning, put that text in Meaning. When the source never says what it means, set Meaning to `to be researched`. Skip ordinary English. A code identifier is not a row unless the source already treats that word as a term. Write the file even when it has no rows. When `glossary.md` already exists, append only words or abbreviations that are not already rows. Do not rewrite, reorder, or edit existing rows. Do not change a Meaning cell that already has text. Do not run an extra interview.

When `docs/system/` already exists, do not rewrite `landscape.md`, `repos.md`, `diagrams.md`, or existing ADRs. Only fill gaps the match needs, the same rule as spark and ideas: a `repos.md` row for a repo that is not listed, a landscape ADR only for a real choice that is not already recorded, a context diagram only when `diagrams.md` has none of these repos, `## Code with no slice` when that note is missing and the map has uncovered code, `glossary.md` when that file is missing, and new glossary rows when the file exists. Append to `## Code with no slice` if it is already there. Do not rewrite the paragraphs around it. Write a missing `glossary.md`, or append new rows, from the same sources and the same glossary rules. Do not rewrite existing glossary rows. The feature index is filled in Index, not here.

No `tasks.md`. No application code. No `git init` except the new clean repo they picked. No remotes.

## Slice specs

One `docs/specs/<slug>/` per confirmed slice, including `not in the code`.

One slice: write it in this chat. More than one: write them in this chat, or one worker per slug. Workers may run in parallel. There is no match-slice subagent. Do not launch `crav1-intake-slice-agent`. Do not reuse that prompt. A worker’s only instructions are [references/slice.md](references/slice.md), and the handoff must include the match status and the trace. A worker that is not given those does not write. Not-started (`not in the code`) stays the thin shape in that file. Workers do not edit `docs/system/`.

Do not thicken a not-started spec in this command. A later pass may add information before planning. This command does not.

## Index

After the specs exist, add one feature-index row per slice on `docs/system/landscape.md`: slug, `docs/specs/<slug>/`, the repo the slice belongs to, and the match status in Notes (`done`, `partial`, or `not in the code`). Do not rewrite other rows. Do not add a second row for a slug that already has one.

## Stop

Do not plan. Do not implement. Do not commit. Do not run `/crav1-finalize-commit` or `/crav1-plan-from-spec`. Do not read `work-item-offer.md`. Do not write `work-item.md`.

Output only:

- Paths written (`docs/system/` and each `docs/specs/<slug>/spec.md`)
- Counts: done, partial, not in the code
- Where the uncovered-code note is, or that the map had none
- Next:
  - `/crav1-finalize-commit` for this dump (landscape and specs). No push
  - `/crav1-plan-from-spec` only for a slice they choose to start. `not in the code` is not planned by this command

If they chose `spec/<dump>`, say that branch is specify-only: no implement there.

## Style

Be concise. Quote the dump and cite paths. Prefer a smaller map to a guessed spec.
