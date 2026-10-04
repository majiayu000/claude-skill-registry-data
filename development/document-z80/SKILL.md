---
name: document-z80
description: Create, restructure, synchronize, or review public GitHub documentation for Z80, ZX Spectrum, and ZX Spectrum Next repositories. Use for README authoring, documentation architecture, English/Spanish parity, and accurate installation, usage, build, release, hardware, protocol, or troubleshooting documentation. Do not use for agent-only instructions, source-code comments, generic prose, or Google Docs.
---

# Document Z80

Make repository documentation easy to enter, operate, verify, and maintain.
Preserve each project's identity while giving related projects a recognizable
structure.

## Workflow Core

Apply the sibling `$workflow` skill at `../workflow/SKILL.md` as the execution
control plane. Workflow owns effort, dispatch, verification, and integration;
this skill owns documentation architecture, evidence, bilingual parity, and
the documentation write boundary. A workflow route never widens those
permissions.

If the sibling skill is unavailable, report the exact limitation and continue
directly without claiming workflow selection or delegated execution.

## Domain Demand

After the initial documentation preflight, classify demand and pass it to
`$workflow` when it is in `auto`:

- **Focused:** one localized correction or one small verified README update.
- **Standard:** a README plus its maintained translations, or one cohesive
  documentation restructure. This is the normal demand for one repository.
- **Deep:** two or more independent repositories, each with separate fact
  sources and mutable documentation. This may justify Heavy when its dispatch
  gate also holds.

An explicit workflow level wins. It does not make coupled documents
independent or widen the write boundary. Treat every maintained language
variant and cross-linked page in the same repository as one coupled mutable
surface with one owner; never split its languages across parallel writers.

In `auto`, `Focused` uses the shared workflow's Light route with only the named
document, repository instructions, and direct fact sources needed for the
changed claim. Do not create a documentation-specific control plane or load a
repository-wide documentation map, translation set, or release history unless
the localized change depends on it.

A review request is read-only. A create, rewrite, or synchronization request
authorizes edits only to the public human-facing documentation in scope. It
does not authorize source, build configuration, release, generated-artifact,
`AGENTS.md`, or `agent_docs/` changes unless the user explicitly includes them.

## Ground Every Claim

1. Read the applicable repository instructions and existing documentation
   before drafting. Inspect only the source, build metadata, CLI definitions,
   tests, release configuration, and artifacts needed to verify documentation
   claims.
2. Identify the audience, supported machines, toolchain, canonical language,
   maintained translations, and current document ownership. Proceed without a
   ceremony when these are evident; ask only for a material missing decision.
3. Verify commands, options, paths, filenames, versions, target models, memory
   requirements, peripherals, protocols, and release artifacts against the
   current repository. Never turn an assumption or stale artifact into a fact.
4. Distinguish confirmed behavior from emulator-only or pending physical-
   hardware verification. Do not claim that a command, build, or link works
   unless evidence supports it.

## Use One Information Architecture

Treat the root README as the landing page and shortest successful path, not as
the container for every fact. Use this order when the sections are relevant;
omit empty or artificial sections:

1. Project identity, one-sentence purpose, and primary visual.
2. Features and current status.
3. Hardware, software, and compatibility requirements.
4. Installation and quick start.
5. Use, controls, and configuration.
6. Build and verification.
7. Release artifacts and where to obtain them.
8. Troubleshooting.
9. Repository map and deeper documentation.
10. Credits and license.

Keep detailed material in the smallest durable home that matches its purpose:

- tutorials teach through a complete learning path;
- how-to guides solve a concrete goal;
- reference pages define exact commands, formats, APIs, or protocols;
- explanations cover design, architecture, constraints, and trade-offs;
- the changelog owns release chronology.

Link to one canonical explanation instead of copying it. Do not create a
`docs/` tree merely to satisfy the taxonomy; one README is correct when it is
enough.

## Preserve Identity and Language Parity

- Keep useful logos, screenshots, demonstrations, acknowledgements, and the
  project's established retro voice. Do not replace strong project-specific
  material merely to match a template.
- Prefer concise active voice, present tense, sentence-case headings, and
  direct second-person instructions. Keep identifiers and commands exact.
- Use the repository's existing localized README filename convention. Do not
  rename `README.es.md`, `READMEsp.md`, or another established variant without
  an explicit migration request.
- For a broad documentation update, keep maintained language variants aligned
  in section topology, facts, commands, links, tables, and release state while
  allowing natural wording. If the user explicitly scopes one language file,
  edit only it and report any resulting parity debt.
- Use relative repository links where possible and descriptive link text. Add
  badges, compatibility claims, download links, or legal text only when their
  targets and wording are verified.

## Verify and Report

Before finishing:

1. Recheck changed claims against their repository sources.
2. Validate local links, anchors, referenced paths, commands, and artifact
   names; run an existing documentation or link check once when available.
3. Compare maintained translations for structural and factual parity when both
   are in scope.
4. Inspect the final diff for accidental rewrites, duplicated facts, and stale
   release history.

For an edit, report changed documents, checks performed, and only material
facts still requiring confirmation. For a review, return prioritized findings
with file and line evidence and do not edit.
