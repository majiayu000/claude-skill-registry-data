---
name: match-the-design
description: Every UI change your agent makes is built from your shared component library and design doc, by reusing or extending a primitive instead of inventing a one-off component. Use for any UI, UX, layout, navigation, loading, empty or error state, styling or frontend component change, or when you say "use our components", "reuse the design system" or "don't make a new component".
---

# Build UI from the shared system

Build each UI change from the shared visual system. Treat the design guidance and the component library as source
code dependencies, not inspiration.

## Resolve the sources

1. Find the product repository root and read its agent instructions (`AGENTS.md`, `CLAUDE.md` or similar)
   completely.
2. Find the **design source of truth**: a design philosophy, design system doc, brand guide or style guide. Look in
   the repo root, `docs/`, `design/`, a sibling `brand` or `design-system` repo, or wherever the instructions
   point. Read it completely for every UI task. When the change touches visible copy, also read the tone of voice
   guide if there is one; read other copy guides only when the task needs them.
3. Find the **component library** the product builds from. It may be a separate repo checked out beside the
   product, an installed package (look in the package manifest for a `ui`, `design-system` or `components`
   package), or a folder inside the product such as `src/components/ui`. Prefer a local checkout; fetch its remote
   first when network access is allowed, and record the commit you inspected.
4. Run the inventory from this skill's folder:

   ```bash
   node scripts/inventory-ui-sources.mjs --product <repo-root> --summary \
     [--brand <folder with the design doc>] [--library <library root>] [--components-dir src/components]
   ```

   It finds the design doc and library on its own when they sit in the usual places (or set `UI_BRAND_DIR` and
   `UI_LIBRARY_DIR`). Narrow with `--family <folder name>` or `--behavior <term>` before opening source. Use
   `--output <path>` only when a durable full inventory is needed. It reads `.tsx`, `.jsx`, `.vue` and `.svelte`
   files; change that with `--ext`.

If the design source or the component library cannot be found, stop and ask the user where they are. Do not
silently replace them with remembered conventions. If the project truly has neither, say so, and propose starting
a small library folder before building new UI.

## Select before implementing

1. Name the user job, host surface, interaction state, data density, and the existing local owner of this UI.
2. Search the complete inventory by behavior, not only by the requested visual name. Inspect the source of every
   plausible primitive, including its dependencies, keyboard, focus, ARIA, responsive, animation and
   `prefers-reduced-motion` behavior.
3. Shortlist the best two to four candidates. Score them against:
   - functional fit and complete state coverage;
   - fit with the design doc's look and density;
   - use of the design tokens (type, color, spacing, motion) the design doc names;
   - accessibility and reduced motion;
   - framework constraints (for example server and client boundaries) and bundle cost;
   - maintainability, and removal of the local primitive it replaces.
4. Reject effects that conflict with the design doc for this surface, even when the library contains them. For
   example, a quiet tool or dashboard surface does not get decorative gradients, 3D, ornamental motion, heavy
   shadows or color-coded meaning.
5. Record the selected primitive and why it beats the alternatives before editing.

## Reuse or extend

- Some libraries are catalogues of hard-coded previews rather than consumable packages. Treat a catalogue entry
  as a concept until its source exposes real props, tests, accessibility, reduced motion, correct dependencies
  and a package export that works in your framework. Never weaken an existing product implementation by importing
  a preview.
- Import the selected primitive through a stable package or export boundary. Do not paste or fork its source
  into the product repository.
- If the library is not consumable as a package, first add the export and build boundary to the library, then
  consume it as a dependency.
- This applies to reusable visual and interaction primitives. Product and domain components still own business
  data, routes, actions and feature composition, but compose their visual controls from the library.
- A product-specific wrapper is allowed only as a thin adapter over a named library primitive. It may supply
  product data, tokens, labels or composition. It must not recreate the primitive's visuals or interaction state.
- If no primitive can be adapted, add the reusable primitive to the component library first, with its tests and
  catalogue entry, then consume it. A standalone custom product component is not an acceptable fallback.
- Use the design tokens package or variables. Do not hardcode brand colors, spacing, typography or motion values.
- Finish the migration: replace usages, remove the superseded local implementation, and remove dead styles and
  exports. One visual behavior has one owner.

## Verify the whole state space

Apply the repository's own quality and test standards (`code-check` and `bug-trap` if
you use them). At minimum verify:

- unit behavior for the shared primitive or adapter;
- real integration and navigation behavior in the host product;
- keyboard order, focus visibility, ARIA semantics, contrast and reduced motion;
- loading, empty, error, populated, disabled, hover and focus, and destructive states that apply;
- light and dark themes at narrow and wide target viewports;
- no clipping, horizontal page overflow, duplicate controls or wasted desktop space;
- typecheck, tests, coverage, production build, and dependency and duplication checks;
- rendered screenshots after fonts, data and animation settle.

End with evidence: design constraints applied, library commit, candidates considered, selected primitive,
extension seam if any, local component removed, checks run, and live verification state.
