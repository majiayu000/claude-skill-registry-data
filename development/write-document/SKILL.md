---
name: write-document
description: Create or edit a Markdown document inside a prototype, with its title, Mermaid diagrams, links and embedded views. Only while the Documents module is on; shared system context and the Manual have their own owners.
---

# Write a document

The [Documents README](../../README.md) is the contract; read the sections you need (frontmatter, links, embeds).

## Before you start

1. Find the prototype's folder, `src/prototypes/<contributor>/<folder>/`. Work only in your own prototypes unless you are an Admin: `yarn studio context src/prototypes/<contributor>/<folder> --json` says whether you may (`canEdit`).
2. Keep context that more than one prototype needs in the system's own context, not in a prototype document.

## Write

3. A document is a `.md` file anywhere in the prototype outside helper folders (names starting with `_`). Nothing registers it.
4. Write plain Markdown: no HTML, no components. HTML you type shows as text; an HTML comment stays hidden and can hold a note for the next editor.
5. Give it a title: `title` in the frontmatter, or an opening `# Heading`. Add `description` for a line under it and `toc: true` for "On this page" in a long document.
6. Draw diagrams with a `mermaid` fence, never an image file, and give each an `accTitle` and `accDescr` so screen readers can describe it:

   ````md
   ```mermaid
   flowchart LR
     accTitle: Sign-in flow
     accDescr: A returning member signs in, then lands on Home.
     Start --> Home
   ```
   ````

7. Link to the prototype's files with paths relative to the document, with their extension so other Markdown readers follow them too: `[the brief](./notes/Brief.md)`.
8. To show a view next to the text, link it with image syntax on its own line: `![Sign-in screen](./flows/Sign-in.vue)` (wrap a path with spaces in angle brackets: `![Sign-in screen](<./flows/Sign in.vue>)`). A named state is embedded by its permanent address, `![Signed in](/prototypes/<prototype-id>/artifacts/<state-id>)`. A standalone diagram (`![Sign-in flow](./sign-in-flow.mermaid)`) shows as a compact drawing; documents embedded this way show as cards. Only files of the same prototype can be embedded; refer to the original view instead of copying its code into the document.

## Identity

9. Leave `studioId` to the studio. While the dev server runs, a new document in your own prototype gets one in its frontmatter within a second. Otherwise run `yarn studio identify src/prototypes/<contributor>/<folder> --json`, then `--yes`. Never change or copy an existing `studioId`.

## Check

10. Open the document in the studio (its address is `/prototypes/<prototype-id>/artifacts/<document-id>`) and look at its links, diagrams and embeds. A card saying "Not found" names what to fix. A document that can't be read shows its error; fix the file and it reads again by itself.
11. Run `yarn studio identity-audit`; it reports frontmatter that is never closed and a `toc` that isn't `true` or `false`, as the build does.
12. Report the document's address and anything you couldn't resolve.
