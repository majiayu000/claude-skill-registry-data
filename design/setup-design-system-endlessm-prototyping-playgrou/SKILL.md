---
name: setup-design-system
description: Set up a new studio design system by bringing another Vue app in or starting from Nuxt UI, or adapt, replace or retire a system. Use document-component for one component.
---

# Set up a design system

The [systems README](../../README.md) is the contract: "System lifecycle", "Setting up a new system" and the `system.ts` fields. [Endless Studios](../../../../systems/endless-studios/README.md) is the worked example of a Vue app brought in: read how its preview document, stand-ins and copied source fit together before changing another system. Systems are Vue only; there is no React or shadcn path.

## Scope and input

- The Overview's setup prompt names the system by name and key (`system “<key>”`), the path and the person's optional details. Resolve the target with `yarn studio status` and `src/systems/<key>/system.ts`; read its `AGENTS.md`, `README.md` and any `setup` record before asking the person to repeat a decision.
- Creating, renaming, archiving, restoring and deleting systems go through `yarn studio create-system|rename-system|archive-system|restore-system|delete-system`: preview, show the person, then `--yes`. Admins only (renaming: Admins and the system's maintainers). Never move or delete a system's folder by hand.
- Preserve other systems, their prototypes and the default system unless the person asks. An assessment stays an assessment until the person authorizes the import.
- Ask only for what the next step needs: the source (repository URL or folder), what they want to prototype, and fidelity compromises. Save supplied product knowledge as Context documents; don't invent personas or context to fill folders. Add a skill only for a recurring task the person names.

## Choose the path

- **Bring in a Vue app**: follow [Bring in a Vue app](references/bring-in-vue-app.md). Inspect the source first and report a plan (what to copy, which stand-ins it needs, what is missing) before copying anything.
- **Start from Nuxt UI**: follow [Start from Nuxt UI](references/start-from-nuxt-ui.md). Start with the theme and assets, show them on the system's Theme and Assets pages, then add the first components.

## Establish the system

1. A new system comes from `yarn studio create-system <key> --label "<Name>"` (or the New system dialog): an empty Vue app (`app.ts`), an empty theme scope (`styles/theme.css`), its own workspace (`package.json`) and a permanent ID. Adapt it in place.
2. Install packages in the system's workspace (`yarn workspace @studio-system/<studioId> add <package>`), and list the meaningful ones in `libraries` in `system.ts`, with `components` and `assets` where the library supplies them.
3. Every Vue app of the system comes from the factory `app.factory` names; install plugins (Nuxt UI, icons, i18n, stores) there, never in a view. Declare `stylesheet`, `themeClass`, `nuxtUi`, `standIns`, `source` and `aliases` as the contract describes.
4. Document components with [document-component](../document-component/SKILL.md).
5. Make or reuse one prototype in the person's folder assigned to the system (`yarn new "<Title>" --system <studioId>`) and check it renders. Previews are light only, so a system's dark colours stay in its stylesheet unseen.

## Record the setup

When the agreed setup is in place, save a `setup` record in `system.ts`:

```ts
setup: {
  stage: 'components', // where setup stands
  summary: 'Started from Nuxt UI with Harbor’s colours and type.',
  next: 'Document the data table.', // optional
  sources: ['https://github.com/acme/harbor-app'], // optional
  record: 'context/setup.md', // optional: a Context document with the details
},
```

The Overview then stops offering the setup panel, for good. Write it only when the person's requested setup is done, not when they open or copy the prompt. Keep agreed direction, sources and the next step there, and in the linked Context document for detail.

## Change the default, replace or retire

- `yarn build` before switching the default; then `yarn studio configure --system <key> --yes`. Existing prototypes keep their assigned system.
- To move prototypes to another system, duplicate them for a rebuild (their menu's Duplicate with another system) and follow the rebuild instructions; don't edit `systemId` alone.
- Retire a system with `archive-system` (files stay, prototypes archived with it) or `delete-system` (files go; its prototypes keep theirs and show "Rebuild needed"). The default system can be neither: change the default first. A held folder (an editor, a terminal, a dev server on Windows) is named in the preview: close it first.
- After a rename, the Overview lists files that still name the old folder (`renameReview` in `system.ts`): repair them, run `yarn build`, then remove `renameReview`.

## Completion

Run `yarn studio status`, `yarn typecheck` and `yarn build`. Report the source and its revision, adaptations and stand-ins, the default system, the prototype you verified (its address) and what is still missing. A passing build doesn't prove fidelity to the source app: say what you compared and what differs.
