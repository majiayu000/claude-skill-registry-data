---
name: documentation
description: Write and maintain the /docs knowledge base. Apply when adding or changing a page under /docs, or when a code change makes existing documentation wrong.
---

<!--
This file is part of Agentprise
Copyright © 2026 The Regents of the University of Michigan
Licensed under the GNU Free Documentation License v1.3 or later.
See <https://www.gnu.org/licenses/fdl-1.3.html>. See README for full license information.
-->

# Agentprise

## Documentation and the /docs knowledge base

This skill expands section 16 of [AGENTS.md](../../AGENTS.md). Read that section
and the [project-preferences skill](../project-preferences/SKILL.md) first. Follow
the wording rules in the [response-style skill](../response-style/SKILL.md) and the
reading level in section 12 of `AGENTS.md`. The README stays short, per section 15;
detail belongs here.

`/docs` is a small curated knowledge base for humans and for agents arriving with
no context. It is not generated API reference, so no autodoc dumps, no per-function
pages, and no restated docstrings. Section 5 of `AGENTS.md` covers documenting
interfaces in the code itself.

### Pages

Create the pages that apply and skip the rest. An empty stub is worse than a
missing page.

    /docs
    README.md           Index of this folder: one linked line per page
    architecture.md     Components, what each does, how they connect, key decisions and why
    data-flow.md        Where data enters, how it changes, where it lands; formats, schemas, time zones; where PHI could appear and how it is protected
    usage.md            Common operations beyond the README quick start
    how-to/             One file per goal, such as how-to/add-a-data-source.md
    troubleshooting.md  Known failure modes: symptom, cause, fix
    faq.md              Questions people actually asked, with answers
    compliance.md       Security and accessibility posture: controls in place, WCAG target and evidence, data retention, known gaps, review status

### Page structure

Every page uses this order.

1. The hidden license header, an HTML comment at the very top that is present in
   the source and invisible when rendered:

       <!--
       This file is part of Agentprise
       Copyright © YYYY The Regents of the University of Michigan
       Licensed under the GNU Free Documentation License v1.3 or later.
       See <https://www.gnu.org/licenses/fdl-1.3.html>. See README for full license information.
       -->

2. The project title as H1.
3. The page subtitle as H2.
4. A link back to the project README, directly under the subtitle, relative to this
   page's depth: `../README.md` from `/docs`, `../../README.md` from `/docs/how-to/`.
5. A summary of two to four plain-language sentences covering what the page holds
   and who it is for. Someone who stops reading here still knows whether they are
   in the right place.
6. The body, as sections, numbered steps, or both.
7. A short conclusion saying what the reader can now do and where to go next.
8. Additional resources: every link used in the page, plus related EFDC knowledge
   base articles and outside references, all with descriptive link text.
9. The same relative link back to the project README as the last line.

### Content rules

- Write for a capable maintainer, researcher, or auditor who has never seen the
  project.
- Document only behavior that exists and can be checked against the current code or
  configuration. Put anything planned under a clearly labeled "Planned" note.
- Use synthetic examples for all sample data, identifiers, credentials, and paths,
  per sections 6 through 8 of `AGENTS.md`.
- Prefer Mermaid for architecture and data-flow diagrams so diffs stay reviewable,
  and always pair a diagram with an equivalent text description. See the
  [accessibility skill](../accessibility/SKILL.md).
- Earn troubleshooting and FAQ entries. Add one when a real failure or question
  happens, or when the design makes it clearly predictable. Never pad with invented
  hypotheticals.
- Keep `compliance.md` to evidence rather than aspiration. "Inputs validated via
  allowlist in `config/validation.js`; axe-core scan clean as of <date>" is
  acceptable. "Fully HIPAA compliant" is not.

### Changes that need a documentation update

Update `/docs` in the same change set whenever any of these happen:

- Functionality is added or removed.
- User-visible behavior changes: inputs, outputs, defaults, error messages, steps,
  or interface.
- Configuration, dependencies, permissions, or the run or deploy procedure changes.
- Data structures change: schema, grain, field meaning, units, time zone, or
  retention.
- Security or accessibility posture changes, which also means `compliance.md`.
- The changes have piled up enough that a new hire reading only the old pages would
  be misled.

A small internal refactor with no user-visible or structural effect needs no
documentation update. When you do update pages, name them in the Summary of your
response. Stale documentation is a defect.

### Additional resources

- [Project instructions](../../AGENTS.md)
- [Response style skill](../response-style/SKILL.md)
- [Accessibility skill](../accessibility/SKILL.md)
- [Skills index](../../SKILLS.md)
