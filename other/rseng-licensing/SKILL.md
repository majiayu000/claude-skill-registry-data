---
name: rseng-licensing
description: >-
  Covers how to license research software: copyright and public-domain basics,
  choosing between permissive, copyleft, and Creative Commons licenses, basic
  compatibility with dependency licenses, and adding a LICENSE file or
  per-file SPDX/REUSE metadata. Use when the user asks which open source
  license to pick, how to add a LICENSE file, what MIT vs GPL vs Apache means,
  whether two licenses are compatible, how to license documentation or data
  alongside code, or mentions REUSE, SPDX, CC0, or public domain. Also use
  PROACTIVELY when a repository has no LICENSE file - an unlicensed repository
  legally blocks all reuse. (Full dependency-tree audits, SPDX expressions,
  dual licensing and CI license enforcement are rseng-license-compliance.)
license: CC-BY-4.0
metadata:
  version: 0.2.0
---

# Licensing research software

Use this skill when someone is choosing a license for research software,
adding a LICENSE file, reconciling the licenses of dependencies, or
deciding how to cover documentation and data that ship with code. Without
a license, others have no legal right to reuse the work, even when the
author intended them to - so a clear, accessible license is what makes the
"R" (reusability) in FAIR real.

## Ground the discussion: copyright vs license

Before recommending anything, make these distinctions explicit:

- Copyright exists automatically from the moment a work is created; it does
  not need to be asserted. It gives only the creator the right to reproduce
  and use the work.
- A license is the document that grants others permission to use, modify,
  extend, or redistribute the work, and states the conditions. It needs no
  signature - a user cannot both rely on the license and deny its terms.
- "No license" is not the same as "public domain". No license means nobody
  may legally reuse the work; public domain (or a dedication like CC0 or the
  Unlicense) means everybody may.
- Small contributions may not be copyrightable at all.

Always check ownership before advising a license:

- Employees usually do not own IP created during employment - the employer
  does. Confirm whether permission from the institution is required.
- Watch for third-party rights baked into the work.
- Grant conditions may already mandate open release; if so, that usually
  removes the need for extra institutional permission. Flag this rather
  than assume.

## Pick a license by what it must permit and require

Recommend an existing OSI-approved license; never draft or edit one unless
the user is a copyright lawyer. Remember that once granted, a license's
permissions cannot be revoked.

Decision drivers to ask about:

- What licenses do the dependencies carry, and what do they oblige? A
  copyleft dependency can force the whole combined work to be copyleft.
- Should anyone who modifies and redistributes be required to release their
  changes' source? If yes, lean copyleft; if no, lean permissive.
- Is maximum, frictionless reuse the priority - even inside closed,
  commercial products? Lean permissive.
- Does the research community have a conventional default license? Match it
  unless there is a reason not to.

### Permissive licenses

Minimal restrictions: redistributors must keep the license text and a
copyright notice. Permissively licensed code can be folded into closed
source products.

- MIT, BSD (several variants): short, simple, allow copy/modify/merge/
  sublicense/sell.
- Apache 2.0: similar, plus an explicit patent grant - contributors license
  their relevant patents to users free of charge.

### Copyleft licenses

Require derivatives, copies, and redistributions to be released under a
compatible copyleft license. This keeps downstream products open but can
block combination with code whose terms are incompatible.

- GPL: strong copyleft; a whole derivative work, including an application
  that links a GPL library, must be GPL with source provided. Long and hard
  for non-lawyers to parse.
- LGPL: lets proprietary software use/link the component without the whole
  application becoming copyleft. Dynamic linking keeps proprietary code
  proprietary; static linking obliges LGPL terms or a way to re-link.
- AGPL: closes the "software as a network service" gap - operators of AGPL
  web applications must offer users the source, even though users never
  receive a copy locally.

### Creative Commons - for non-code artifacts

Code licenses do not fit documentation, datasets, drawings, logos, music,
or maps. Use Creative Commons for those. The
baseline rights combine into six licenses:

- BY (Attribution) - required in all CC licenses; credit the creator.
- SA (Share-Alike) - derivatives must use a compatible CC license (copyleft-
  like).
- NC (Non-Commercial) - non-commercial use only.
- ND (No Derivatives) - no redistribution of modified versions.

The six: CC BY, CC BY-SA, CC BY-NC, CC BY-NC-SA, CC BY-ND, CC BY-NC-ND. For
a public-domain dedication of non-code work, use CC0. Note that NC and ND
variants are not "open" in the open source sense - flag this when a user
wants their work broadly reusable.

## Check license compatibility

When code combines multiple sources, compatibility is the trap:

- Incompatible terms between a copyleft license and another license can
  legally prevent combining the two codebases.
- Combining copyleft code generally forces the entire combined work under
  that copyleft license - confirm the user is willing to accept that before
  they add such a dependency.
- Audit every dependency's obligations before settling on the project's own
  license, not after.

## Add the license to the repository

Once chosen, apply it concretely:

- Put the full license text in a file named `LICENSE` (`LICENSE.txt` or
  `LICENSE.md` are also accepted) in the repository root.
- On GitHub, use the built-in "Add a license" flow, which drops in the exact
  text. Otherwise create the file and paste the canonical text yourself.
- A single project-wide license is recommended for small-to-moderate
  codebases. Only split licenses across parts of a large codebase when there
  is a real need.
<!-- REUSE-IgnoreStart -->
- To license per file (mixed licenses, or fine-grained provenance), adopt
  REUSE: add a short SPDX identifier header to each file
  (`SPDX-License-Identifier: MIT`) so licensing is machine-readable and
  every file is unambiguously covered. Use SPDX identifiers whenever a tool
  or metadata field asks for the license.
<!-- REUSE-IgnoreEnd -->
- For software that also ships data or documentation, consider a LICENSE
  that specifies distinct terms for software, content, and metadata (for
  example code under an OSI license, docs under CC BY).

## Agent checklist

When helping with a licensing task, work through this order:

1. Confirm ownership and any funder/employer constraints.
2. Inventory dependency licenses and their obligations.
3. Choose permissive vs copyleft from the user's reuse goals, then a
   specific license; use Creative Commons for non-code artifacts.
4. Add a root `LICENSE` file with the canonical text (GitHub flow or manual).
5. If per-file clarity is needed, add SPDX headers via REUSE.
6. Record the SPDX identifier in package metadata (for example
   `pyproject.toml`, `DESCRIPTION`, `package.json`).

## Working with this skill

The generated references.md beside this file lists the source
material and pointers:

- references.md - verified Learn more pointers

Compliance engineering - dependency license audits, compatibility
analysis, dual licensing, SPDX expressions and REUSE verification -
is rseng-license-compliance; this skill covers choosing and applying a
license.


Learn more (verified):
  - https://choosealicense.com - GitHub's open source license chooser
  - https://opensource.org/licenses - OSI-approved open source licenses
  - https://spdx.org/licenses/ - SPDX license identifier list
  - https://reuse.software - REUSE per-file licensing specification
  - https://creativecommons.org/cc-licenses/ - Creative Commons
    license overview


<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-citation-metadata - SPDX id in metadata files
- rseng-data-management - licensing datasets alongside code
- rseng-fair-ml - licensing model weights
- rseng-fair-software - license implements reusability
- rseng-license-compliance - dependency audits and enforcement
- rseng-open-source-migration - licensing freed code

<!-- related-skills:end -->
