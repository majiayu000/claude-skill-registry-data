---
name: 3d-brain
description: Use when someone asks to build a 3D brain, visualize their AIOS or second brain, turn their knowledge into an interactive graph, or run /3d-brain or /3D brain.
disable-model-invocation: true
argument-hint: "[brain name] [categories or existing app path]"
---

# 3D Brain

Turn the user's actual AIOS files into a personalized, local 3D knowledge globe. Use the bundled working application, not a new interpretation of its appearance. Preserve its spherical composition, colored categories, central orb, restrained connection particles, Cinema mode, and interactive growth replay.

The command is `/3d-brain` in Claude Code. In Codex, select the `3d-brain` skill or use `$3d-brain`. Interpret the natural-language phrase “3D brain” the same way. Input comes from `$ARGUMENTS` and the conversation. Work in the current assistant; no subagents, external services, API keys, paid assets, or deployment are required.

## 1. Find the AIOS and the package

Read the applicable local operating manual and relevant index. Establish the actual AIOS root; do not scan an unrelated ancestor or all of the user's home directory. Resolve this skill's own directory from the loaded `SKILL.md`; all package paths below are relative to it, regardless of whether it lives in `.claude/skills`, `.agents/skills`, or a plugin.

Read [the portable spec](references/portable-spec.md) and [the config guide](references/config.md). Check Node.js 22 or newer. Use the user's existing Node runtime. If unavailable, explain that Node is required and follow the host's installation/approval policy.

Run the path-only discovery helper:

```text
node <skill-directory>/scripts/discover.mjs --root <AIOS-root>
```

It lists candidate folders, not their contents. Also use explicit routes in the operating manual to find custom wiki, meeting, video, or project folders. Do not assume the author's folder names or accounts exist on this machine.

## 2. Ask for the name and categories

Use the host's question tool when available, otherwise ask in plain language. Reuse information already supplied; do not repeat answered questions.

1. **Name:** “What would you like to call your 3D brain?” Accept the exact display name, such as “Atlas Brain,” “Studio Mind,” or “Maya's Second Brain.” Do not silently choose the author's name or brand. A supplied argument can answer this question.
2. **Categories:** “Which main categories would you like to see?” Offer the categories actually found, each beside its proposed file/folder path. Examples are Business knowledge, Meetings, Video knowledge, Claude memory, Codex Memory, Projects, and Skills. Let the user rename, omit, or add categories. Suggest three to seven for visual clarity; support one to twelve.

The category answer also approves its listed source paths. For a custom category with an unknown path, ask where those files live. Do not guess external memory roots. Codex's curated memory store can cover multiple projects; state that scope when offering it. Include it only if chosen. Claude memory should point to this AIOS's matching memory folder, not every Claude project.

Show the compact name/category/path mapping in your progress update. Once these choices are supplied, continue building without another generic confirmation. Ask only about unresolved paths, replacing an existing app, or another material ambiguity.

## 3. Scaffold the exact experience

Default output: `<AIOS-root>/apps/3d-brain/`. If it already exists, inspect its `brain.config.json` and reuse the app. Do not overwrite it blindly. For a requested replacement, archive the existing version first within the same project. If unrelated files occupy the destination, choose a new folder or ask the user.

Create a setup JSON file in an ignored scratch folder under the user's AIOS, using the schema in [config.md](references/config.md). Do not include actual note bodies. Use relative paths for sources inside the AIOS and explicit approved paths for outside sources. Give each category a unique ID, label, color, adapter, and one or more real paths.

```text
node <skill-directory>/scripts/scaffold.mjs --root <AIOS-root> --config <setup-json> --out apps/3d-brain
```

This copies an explicit allowlist of application files and writes the personalized local config. It refuses an existing destination. The renderer is prebuilt: `node serve.mjs` works without npm installation. Do not copy `node_modules`, another user's config, a graph snapshot, screenshots, memory files, or session logs into the app or skill.

In the generated app folder:

```text
node build.mjs
node serve.mjs
```

Start the server through the host's normal background/launch mechanism. On Windows, background launches must be hidden. Default port is 4640. If occupied, pick an available port, update this app's config, and start there. Never stop an unrelated service. Keep the bind address at `127.0.0.1`.

Read the build's real counts and warnings. A missing folder is a configuration issue to resolve, not a reason to invent nodes. Empty categories are allowed and shown honestly. For an entirely empty AIOS, explain that it needs saved notes; do not inflate it with synthetic content unless the user separately asks for a labeled example.

## 4. Preserve behavior and honest connections

The supplied renderer is the visual contract. Retain:

- A stable spherical layout, distinct source colors, dark background, glowing central orb, and quiet orbital accents.
- Real explicit Markdown links and wikilinks, with exact-title mentions distinguished from explicit relationships. Ambiguous links remain unresolved.
- Search, source solo/toggle, inventory, health flags, note reading, and local file reveal.
- **Play demo:** one central idea, the first real connection, branches springing from parent nodes, accelerating growth, and the full brain after about 29 seconds. Disconnected notes join without invented edges. This is a connectivity replay, not a historical chronology.
- The central orb is visible from the first frame. Dragging, zooming, or clicking the canvas does not stop growth. Camera input takes over from automatic pullback. Replay resets cleanly.
- **Cinema:** clean presentation with the growth counter beside the scene. Pause motion, reduced-motion support, responsive source controls, and no stale labels after replay.

All name-bearing UI comes from `brain.config.json`. Do not regenerate the visuals with an image model or replace the scene with a generic force graph. If code changes are needed, use `npm ci`, edit `src/`, and run `npm run build:js`. Keep dependency license notices with the bundle.

The default adapters read Markdown/text and curated Codex memory. For Google Drive, Notion, raw meeting JSON, databases, PDFs, or another unsupported source, explain the gap and use an explicitly approved local export or build and test an adapter. Do not claim those systems are connected merely because their names appear in a category.

## 5. Verify and deliver

Follow [the acceptance checklist](references/acceptance.md). Check the actual generated app, not just the template:

1. Graph API has the requested name/categories, unique IDs, valid endpoints, and counts matching the source scan.
2. Read at least one real note from each nonempty category, including exact topic sections for Codex memory. Originals remain unchanged.
3. Confirm the personal name on the page and test search, a source solo filter, restoration, and the inventory.
4. Watch early, middle, and complete growth. Drag and zoom while the count increases. Check the initial orb, clean labels, complete final count, and replay reset. Test Cinema and pause/resume.
5. Inspect desktop and a narrow viewport. Do not manipulate the user's physical mouse; native Pointer Lock is disabled in the supplied app. Browser automation must remain virtual/headless.
6. Check console errors. If browser verification is unavailable, say exactly which checks remain unverified rather than claiming a visual pass.

Add a small route to the new app's README in the AIOS's existing project index or operating manual, following its conventions. Synchronize `AGENTS.md`/`CLAUDE.md` when required. Avoid storing private configs, graph data, or note content in a public repository. Do not deploy or push without the user's authorization.

Finish with the brain name, local link, app folder, actual note/category counts, and the shortest useful instructions: **Play demo**, **Cinema**, drag to orbit, scroll to zoom. Mention source gaps if present. Never promise virality.
