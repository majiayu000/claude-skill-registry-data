---
name: write-manual
description: Create or revise chapters of the Endless Design Studio's Manual for people. Only while the Manual (the documentation module) is on; agent guidance stays with its owners.
---

# Write the Manual

The Manual explains the studio to the Endless team: what it does, its controls, what each action leads to, and what to do when something goes wrong. Agent requirements belong in the owners' context, READMEs and skills, which Context & Skills shows; don't copy them into chapters.

Read the [module README](../../README.md) for the chapter contract before writing.

- Chapters are `src/modules/documentation/pages/*.md`. Each needs `title` and a numeric `order` in its frontmatter; add `description`, `section` and `toc: true` when they help. The file name is the address, so renaming a chapter changes its links: update every link to it.
- A chapter about one capability declares `module: <id>` so it hides while that module is off.
- Write for designers on the Endless team: plain words, second person, short sentences, headings phrased as the question a reader has. Describe controls by their labels in bold, with both shortcuts (**Ctrl+K**, **⌘K** on a Mac), and Windows wording first (Show in Explorer, Recycle Bin).
- Keep it a reference: capabilities, controls, consequences and troubleshooting. Tutorials and exercises don't belong here. Describe the environment without prescribing a design process.
- Describe what the studio does now. Commands are `yarn …`; views are Vue files; there is one team studio.
- Link between chapters by file (`team.md#who-can-change-what`) and to guidance by its path; both open in the studio.

After a change, run `yarn test tests/unit/manual-content.test.ts` (metadata, links and anchors) and open the chapter in the studio to read it rendered. Follow the platform's working context for scope, checks and saving.
