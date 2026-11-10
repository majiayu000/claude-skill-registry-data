---
name: build-prototype
description: Create a prototype, or create or edit a prototype view, a Vue file that renders in its assigned system's preview document, with its named states, system options, links to other views and lo-fi marker.
---

# Build a prototype view

The [prototypes README](../../README.md) is the contract; read the sections you need (views, named states, system options, navigation, lo-fi, permanent identities).

## Before you start

1. Find the prototype's folder, `src/prototypes/<contributor>/<folder>/`, and inspect it with `yarn studio context src/prototypes/<contributor>/<folder> --json`: it reports the owner, the system, a pending rebuild and whether you may change it, without writing. Read its `meta.json`. `systemId` names its system, or `null` for no system; `order`, when present, is the navigation's order (paths inside the prototype), and its first artifact is the one the prototype opens with. Work only in your own prototypes unless you are an Admin.
2. For a system, read that system's `AGENTS.md` and follow it: it says which components, stand-ins and strings views use.
3. To start a new prototype, run `yarn new "Prototype Name"` as the person. It uses the studio's default system; add `--system <folder name or ID>` for another, or `--no-system` for none, as they asked. It creates `src/prototypes/<their key>/<slug>/` with `meta.json` (the README lists its fields), your contributor ID as owner, and an empty starting view, `Prototype.vue`, and prints the address to open. Pass its refusals on as they are (someone who isn't a contributor yet must be added first). Build the first view in `Prototype.vue`, or rename it. A prototype folder written by hand instead needs `yarn studio identify src/prototypes/<contributor>/<folder> --json`, then `--yes`, to get its IDs and owner.

## Write views

4. A view is a `.vue` file in the prototype; its path inside the prototype, without `.vue`, is how other views link to it (`flows/Sign in`). Put helpers that are not artifacts (components, data) in a folder whose name starts with `_`, such as `_parts/`.
5. Use `<script setup lang="ts">` and a `<template>`. In a system's prototype, Vue, the system's components and its stand-ins are auto-imported. In a prototype with no system, import from `vue` and style the view yourself; it starts from browser defaults and always renders light.
6. An empty view is a `.vue` file holding only comments. The studio shows "This view is empty" with a prompt to copy until you write it. To add a view someone will fill in later, write the file with nothing but a comment, such as `<!-- Sign in, for returning members -->`.
7. Leave the permanent identity to the studio. While `yarn dev` runs, a new view in your own prototype gets its `<!-- @studio-id <id> -->` comment at the top within a second. Without the dev server, run `yarn studio identify src/prototypes/<contributor>/<folder> --json` to preview and then `--yes`. Never write, change or copy an ID by hand: keep the comment when you edit, rename or move the file, and give a copied file no ID so it gets its own. `yarn studio identity-audit` reports missing and duplicate IDs; the build fails on them.

## Named states

8. For variations of one screen (a member, a new user, an error, an empty list), declare named states in the view instead of copying the file. Export a plain list from the regular `<script>` block, next to `<script setup>`; each state renders the view with its `props`:

   ```vue
   <script setup lang="ts">
   defineProps<{ name: string }>()
   </script>

   <script lang="ts">
   export const states = [
     { title: 'Member', props: { name: 'Ana' } },
     { title: 'New user', props: { name: '' } },
   ]
   </script>
   ```

   Titles are plain text in quotes, written in place, each different, on one line and without `-->`. The studio reads them without running the view, so never compute a title or build the list elsewhere. A view whose only script is the regular `<script>` must also export its component as `default`; with `<script setup>` beside it, it needn't.

9. Each state gets its own permanent ID as a comment at the top, `<!-- @studio-state <id> <title> -->`, matched by title. The dev server or `yarn studio identify` writes it; never write it yourself. Each state is listed under its view in the navigation and opens at its own address. To rename a state, change its title in the code and in its comment together: the comment keeps its link. A comment that names no state, a repeated title or one that isn't plain text stops the build, naming the file and title. Remove a state's comment only when removing the state.

10. When states differ in what the system's app around the screen knows (the locale, who is signed in, the sample data its stand-ins answer with, whether the app's own layout surrounds it), export the view's choices as `system` from the same regular `<script>`, and give a state its own `system` with only the options it changes:

    ```vue
    <script lang="ts">
    export const system = {
      user: 'admin',
      sample: { queries: { UpcomingEventInstances: events } },
    }

    export const states = [
      { title: 'Spanish learner', system: { locale: 'es', user: 'learner' } },
      { title: 'Signed out', system: { user: null } },
    ]
    </script>
    ```

    The system's `AGENTS.md` and README say which options it has and what its samples look like. A state's option replaces the view's whole, so to change one part of a sample, build the state's from the view's (`sample: { ...sample, queries: {} }`) with the shared parts as constants in that `<script>`. An edited option rebuilds the open screen.

## Links between views

11. Link to another artifact of the prototype by its path, never by its ID or address. Import the helpers from `#studio/prototype`:

    ```vue
    <script setup lang="ts">
    import { PrototypeLink, usePrototypeNavigate } from '#studio/prototype'
    const navigate = usePrototypeNavigate()
    </script>

    <template>
      <PrototypeLink to="flows/Details">Details</PrototypeLink>
      <UButton @click="navigate('flows/Details')">Continue</UButton>
    </template>
    ```

    `usePrototypeArtifactHref()` gives a function returning a path's address; `useIsPrototypeArtifact('Home')` says whether that view (or one of its states) is on screen. A path may keep its `?query` or `#anchor`; a target starting with `/` is a studio address. An unknown or ambiguous path stops the view with an error naming it. Links open in the studio, so Back and Forward work; `#anchors` scroll inside the view; other web addresses open in a new tab. A rename or move made in the studio, or with your own tools while `yarn dev` runs, updates the imports, paths and links that reach the file, inside the prototype; without the dev server, update them yourself. A one-segment path (`Details`) is updated only in a `to` attribute or a `navigate(…)` call.

## Lo-fi

12. A lo-fi view keeps its components and behavior and is drawn in grayscale with a handwritten font. People switch it with "Make lo-fi" and "Make hi-fi" in the view's context menu in the navigation. In code, it is a comment at the top, `<!-- @lofi -->`; add or remove only that comment.

## Check it

Run `yarn studio check`. Both Vue script blocks and TypeScript helpers must stay within this prototype, its assigned system, Vue, `#studio/prototype` and enabled `@module/<id>` libraries. Use scoped/module CSS and imported colocated assets. Files over 750 KiB block commits; prefer smaller WebP images. A missing system remains rebuild source outside the Studio's Nuxt typecheck; rebuild it before treating its preview as verified. Scope/identity checks warn locally, while CI checks pushes against the previous revision's permissions.

Use the studio's command palette (Ctrl+K, Command+K on macOS, or Search on the rail/Home) to find prototypes by title, contributor or folder. In an open prototype it also finds artifacts and named states by title or path, using their permanent addresses. The current destination is disabled. Shortcut forwarding from previews preserves typing fields; do not add a competing global handler to a view unless the prototype needs that key itself.

13. Open `/prototypes/<prototype-id>/artifacts/<artifact-id>` in the running studio, or a state's own ID. The view renders in its system's preview document; "Open in a new tab" in the view's row menu in the file tree opens that document alone. New, renamed and removed views and states appear without a restart, and edits update the open preview live.
14. Before trusting what the preview shows, check its state: in the studio, the element with `data-preview-session` has `data-preview-state` (`ready`, `error`, `empty`, `loading`) and `data-preview-freshness` (`stale` means the latest save did not render yet or failed). In a document opened alone, read `data-preview-state` on `<html>`. On an error, read the message under "This page couldn't load" or the out-of-date notice; it names the file, line and column. Fix the file; the preview recovers by itself.
15. Run `yarn studio identity-audit` after adding views or states; it must report no missing or duplicate IDs.
16. The person may be editing the same file in the studio's source mode (`?mode=source` on the artifact's address, or ⌘' / Ctrl+'). Your writes reach their editor: a clean editor reloads, and one with unsaved changes offers "Load the new version" or "Keep mine". Their save never silently overwrites yours, and the studio refuses saves that change or drop the identity comment.
