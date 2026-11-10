---
name: create-diagram
description: Create or edit a standalone Mermaid diagram (a .mermaid or .mmd file) inside a prototype. Only while the Diagrams module is on; a diagram that belongs with an explanation is a mermaid fence in a document instead.
---

# Create a diagram

The [Diagrams README](../../README.md) is the contract; read it for how diagrams render, update and embed.

## Before you start

1. Find the prototype's folder, `src/prototypes/<contributor>/<folder>/`. Work only in your own prototypes unless you are an Admin: `yarn studio context src/prototypes/<contributor>/<folder> --json` says whether you may (`canEdit`).
2. Choose the form. A diagram that belongs with an explanation is a `mermaid` fence inside a document (see the write-document skill). A diagram that needs its own page in the prototype's navigation, or a preview in documents and canvases, is a standalone file.

## Write

3. A standalone diagram is a `.mermaid` file (`.mmd` works too) anywhere in the prototype outside helper folders (names starting with `_`). Nothing registers it; its file name is its title ("sign-in-flow.mermaid" → "Sign In Flow").
4. Write plain Mermaid: no Markdown fences, one diagram per file. Choose the diagram type that fits the relationship and the audience; any standard Mermaid type works.
5. Give it an `accTitle` and an `accDescr` (where the diagram type has them), so screen readers can describe it:

   ```mermaid
   flowchart LR
     accTitle: Sign-in flow
     accDescr: A returning member signs in, then lands on Home.
     start[Sign in] --> home[Home]
   ```

6. Leave colours and fonts to the studio: diagrams follow its light theme. Set a colour only when it carries meaning, and check its contrast.
7. To show the diagram in a document, link it with image syntax on its own line: `![Sign-in flow](./sign-in-flow.mermaid)`. Keep the path relative, with its extension, and the file in the same prototype. The preview's header opens the diagram.
8. Excalidraw can import Mermaid into a canvas. That copy is a separate drawing: later edits to the `.mermaid` file don't reach it.

## Identity

9. Leave the leading `%% @studio-id` comment to the studio. While the dev server runs, a new diagram in your own prototype gets one within a second. Otherwise run `yarn studio identify src/prototypes/<contributor>/<folder> --json`, then `--yes`. Never change or copy an existing ID, and keep it the first line when you edit.

## Check

10. Open the diagram in the studio (`/prototypes/<prototype-id>/artifacts/<diagram-id>`). Invalid Mermaid shows "Unable to render Mermaid diagram." with Mermaid's message: fix the source (the file's actions, Edit source, locally) and it draws again by itself.
11. Look at every document that embeds it, then report the diagram's address and anything you couldn't resolve.
