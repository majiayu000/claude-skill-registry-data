---
name: timeline-site-build
description: "Use when the site build fails, or a built page must be proven."
version: 1.0.0
author: TimeLine
license: MIT
platforms: [macos, linux]
metadata:
    hermes:
        tags: [astro, solid, postcss, vite, sass, islands, hydration, build, cdp]
---

# Timeline Site Build

The site is two layers that fail differently. The config layer decides whether a page compiles at
all

- PostCSS loading, CSS alias resolution, the Node floor, the dependency policy. The island layer
  decides whether the compiled page is the page: hydration, one shared store, a measured
  composition. A green `astro build` proves only the first.

## When to Use

- `pnpm run build` exits non-zero before compiling a page: `Failed to load PostCSS config`,
  `require(...) is not a function`, `Unable to resolve @import`,
  `ENOENT ... open '@Stylesheet/...'`.
- A build "passes" but the output is empty, unstyled, or missing a route.
- A build fails only in CI, or only after a clean install.
- A page needs interaction, and a design has to become components under `Source/Component/`.
- A built page has to be proven rather than eyeballed.

## Read the innermost error first

Astro nests the same message once per resolution attempt:
`Failed to load PostCSS config (searchPath: <root>): [Failed to load ...]: ... [TypeError] require(...) is not a function`.
The load-bearing part is the LAST bracket plus the `postcss.config.js:LINE:COL` frame; everything
before it is repetition. Fix that and re-run - the config loads before CSS resolution, so a broken
config hides an alias problem behind it. Expect two rounds, not one.

The four config-layer failures, with their probes and their exact messages, are
`Reference/Build-Repair.md`:

- **An ESM-first PostCSS plugin needs `.default`.** A v11-era plugin's `require()` returns
  `{ __esModule, default }`, so calling the module object throws `require(...) is not a function`
  while PostCSS loads the config and the build never starts. Probe every plugin in one pass and
  print only the non-functions.
- **tsconfig `paths` do not reach a CSS `@import`.** `@playform/build` defines `@Stylesheet/*` for
  TypeScript and Vite; a CSS `@import` inside `<style is:global>` goes through Vite's STYLESHEET
  pipeline, which does not read them. `astro.config.ts` therefore registers an `Aliases` table with
  absolute paths as `vite.resolve.alias`. Adding only the `postcss-import` `resolve` option is NOT
  sufficient - keep both.
- **In a `lang="scss"` global block, use `@use … as *`, not `@import`.** `@import` emits a Dart Sass
  deprecation per file on every build, and `@use` must precede every other rule in the block.
- **A failure that only happens in CI is dependency resolution, not config.**
  `[astro] Unable to load your Astro config` plus
  `Cannot find module '<pkg>' imported from '<root>/astro.config.ts'`, where `astro.config.ts` does
  not import that package at all - `astro/config` does. Under pnpm's strict layout a transitive
  dependency is not at the root, so an undeclared package is unresolvable no matter which Node
  version CI uses. Declare it at the version the framework declares: `pnpm add -Dw <pkg>@<version>`.

**Reproduce a CI failure in a clean tree before editing anything.** A failure that does not
reproduce locally is a resolution difference, and `Reference/CI-Reproduction.md` is the recipe that
catches it in one pass instead of by pushing fixes and waiting for a build.

## Check the Node floor before believing the site is broken

`package.json` declares `engines.node` (>= 22.23.4 today), and Astro refuses `astro sync` and
`astro build` on a lower version. The `node` first on `PATH` inside an agent terminal can be older
than the person's own shell node, so run `node --version` and compare it against the declared floor
before editing a single config file: a version refusal and a config defect both surface as "build
failed".

Put the newer interpreter on `PATH` inside the same command that runs the build. Exporting it in an
earlier call does not survive, and the bundled interpreter then fails with
`Node.js v<old> is not supported by Astro`, which looks like a config defect:

```sh
PATH="<node-bin>:$PATH" timeout 420 pnpm run build
```

## Verify against artefacts, not the log

```sh
timeout 420 pnpm run build > <log> 2>&1; echo "EXIT=$?"
```

Never `... 2>&1 | tail -n`: the pipeline's status is `tail`'s, so a failed build reports 0 and an
empty `Target/` looks like a pass. Keep the runner in the foreground - some runtimes auto-background
a bare `pnpm run …` and the tool result then carries the launcher's status instead of the build's.
The `PATH=`-prefixed form above returns the real exit code.

Then assert over ALL of `Target/`. Astro inlines a `<style is:global>` block into the emitted HTML,
so rules imported through the alias land in `Target/index.html` inside `<style>`, NOT in the emitted
`Target/_astro/*.css` - grepping only the `.css` file reports a false negative and sends you back to
re-fix a working alias. Pick two declarations unique to the imported stylesheet, grep the whole
output tree for both, and also assert no literal `@import "@Stylesheet/` survives.

**Assert the emitted route set, not just the exit code.** A green build cannot distinguish "nine
pages, all correct" from "nine pages, two silently absent". A `getStaticPaths` that returns an empty
array because a library it reads changed shape produces no page and no error - the route simply is
not in `Target/`, and every other check still passes. `find Target -name index.html` is the
inventory; compare it against the routes `Source/pages/` declares.

## Islands: split by state, not by markup

The shell, the tokens and the published markup are built static; the part that depends on who is
signed in hydrates as a Solid island.

1. **One composer holds every `createSignal`**; children take props and callbacks (`OnOpen`,
   `OnPublish`) and hold none. The composer is the only place that knows how the parts fit, so a
   child can be rendered alone in review.
2. **Write the material first.** `Source/Stylesheet/Material.scss` holds the shared mixins before
   the first component sheet: a `reset` for rows that are real `<button>`s, an `inset` for tracks, a
   `label` for eyebrows, an `ellipsis`. A sheet that repeats a hex is a second place the palette
   lives.
3. **Let data drive the dimensions.** Anything that ramps - a depth ladder, a size scale, an opacity
   gradient - is a table in the component, and the sheet reads it as custom properties
   (`--band-height`, `--marker-size`). A sheet that hardcodes seven heights makes an eighth item a
   stylesheet change.
4. **Make actions buttons.** A row or band with a handler is `<button type="button">` plus the
   `reset` mixin, with `aria-pressed` when it toggles. A `div` with `onClick` is the version a
   keyboard cannot reach.
5. **Pass only serialisable props across the boundary.** Astro renders the island on the server and
   hands it a JSON payload: arrays of plain objects, strings, numbers. A function, a `Date`, a class
   instance or a collection entry object will not survive.
6. **Mount with the narrowest directive that works.** `client:visible` for a surface on screen,
   `client:load` only when the island is the page. The static parts stay static either way.
7. **A sheet that is never imported is not a styling bug - it is a missing line.** The markup
   carries the class, the sheet contains the correct rule, and the browser reports `display: block`
   for an element whose rule says `display: flex`. Nothing errors, the build is green, and the
   layout collapses. A component file opens with `import "@Stylesheet/Component/<Name>.scss";` and
   nothing else before the `solid-js` imports, so a page never lists stylesheets.

The no-script half of this contract - what the first paint must show, and the audit that proves it -
is `Documentation/Skill/Progressive-Enhancement/SKILL.md`.

## Measure the design file, never its picture

Before the first sheet is written, pull the geometry out of the design file's own layer tree and
write it down as a spec the components are checked against. A rendered export is a picture of the
result; it is not a source of values. A screenshot shows a dark rail, a dark drawer and a light
canvas, so the page ground gets painted dark - while the frame's own root fill is a light grey that
also shows through the gap between the two panels.

Write the result to `Documentation/Reference/Design-Composition.md` and have the components cite it.
A spec that lives only in a scratch directory is gone by the next session, and a worker told to
"compare against the design context" will find nothing and either guess or block. The extraction
recipe - two MCP calls, the node-id spellings, and the four values a screenshot hides - is
`Reference/Design-Intake.md`.

**A full-bleed surface inside a measure.** A page column with `max-width` silently constrains an
application surface mounted inside it: a six-track grid collapses to ~87px tracks and the layout
reads as broken while every rule is correct. Do not fight the container from the component. Add an
opt-in on the layout and have the page pass it:

```astro
interface Props { Wide?: boolean }
<main class:list={["page", "shell-main", { "page--wide": Wide }]}>
```

with `.page--wide { max-width: none; padding-inline: 0; }` in the shell sheet. The prose measure
stays the default, so the exception is stated once.

## Verify a built island, not the source

A green build proves the island compiled, not that it hydrated. Serve the output and probe it:

```sh
cd Target && python3 -m http.server 4411 --bind 127.0.0.1
node Documentation/Skill/Timeline-Site-Build/Reference/probe-built-page.js \
    "http://127.0.0.1:4411/Workspace/?v=$(date +%s)" /tmp/page.png astro-island
```

The probe asserts, in one pass: an `astro-island` element exists, the structure renders, the
computed styles carry the tokens, no console error fired, and a screenshot is written for review.
Those five together are what distinguishes "built" from "works".

- **Count `astro-island`, not `script[type=module]`.** The shell mounts `ClientRouter`, so every
  page carries a module script whether or not it has an island. Counting module scripts reports an
  island on a page that ships none and fails a page that is correctly static.
- **Cache-bust the URL.** Chromium keeps the previous document across a rebuild, so a probe run
  after a build reports the geometry of the page that used to exist - with no error, and with values
  that look like a regression you just fixed.
- **Never serve a live `Target/` while another build may be running.** `astro build` empties the
  output directory before it writes, so a probe mid-build sees zero routes and reports each as "the
  route served no document". Snapshot the directory and serve the snapshot.

The frame-level verification - the geometry, the ladder, the seam's state - is
`Documentation/Skill/Design-Verification/SKILL.md`.

## Check the effect, not the string

Every string-matching check in this skill shares one failure mode: the file or the response is
correct and the pattern is wrong, so the check reports a defect that does not exist. Three shapes,
one rule - measure what the system does, not what you predicted it would look like.

- **The minifier rewrites the markup.** `@playform/compress` strips attribute quotes, so a grep for
  `class="foo"` returns nothing on a page full of `class=foo` and the page reads as empty. Match
  `class=["']?name`, or measure with `querySelector` in a browser - the DOM is immune to the
  minifier and a shell grep is not.
- **An unanchored glob matches deeper than intended.** `Target/` in `.prettierignore` matches a
  directory of that name at ANY depth, so it hid four real TypeScript files under
  `Maintain/Source/Browser/Target/` from the formatter while appearing to mean the build output.
  Anchor the pattern (`/Target/`) and verify the _resolved_ set, not the line you wrote.
- **An API rewrites a key you asked for by name.** `gh project item-list --format json` lowercases
  only the first letter of a custom field, so a field named `RFC` arrives under `rFC` and reading
  `.rfc` yields null on every item - see `Documentation/Skill/RFC-Board/SKILL.md`.

The tell is identical in all three: the code is right, the check is red, and the fix is in the
check. Confirm the measurement before reporting a defect to anyone.

## Pitfalls

- **Build only after the edit batch is complete.** The bundler can snapshot a half-applied change -
  a new function signature with the old call sites - and fail with an error that describes a bug you
  already fixed (`Read is not a function` from a helper whose parameter changed one edit earlier).
  Finish the batch, then build; do not chase the phantom.
- **`class` is a reserved word, so it cannot name a local.** In an Astro expression
  `const class: string = …` fails the compiler with
  `Identifier expected. 'class' is a reserved word that cannot be used here.` Name the local
  `Class` - which is also this repository's PascalCase rule. Read the error's `Location:` line, not
  the stack: the stack names the compiler internals and never the defect.
- **A dynamic tag name is not an element.** `const Tag = Cond ? "a" : "article"; <Tag …>` does not
  render a tag in Astro, and the compiler rejects the variable rather than the usage. Render the
  element that is always right - an `<article>` with the link inside it - instead of branching on
  the tag name.
- **`nth-child` counts every sibling, so a composed page offsets by one.** On a page built as hero +
  cards + closing band, `:nth-child(odd)` starts counting at the hero: every card is displaced one
  position and a `:last-child` rule lands on the closing band. Use `:nth-of-type` and
  `:last-of-type`.
- **A `var(--token, <literal>)` fallback is still a stray literal.** When the token exists, the
  literal is a second copy of the palette hiding inside a `var()`; nothing checks for it, so it
  survives unless the review reads the diff. Declare the missing token in
  `Source/Stylesheet/Global.css` and read it bare.
- **A required prop added to a component the runtime already renders breaks hydration, not the
  build.** Astro type-checks the page, not the island's runtime props; a missing prop surfaces as an
  undefined read inside the component.
- **A design's generated markup is a description, not the code to commit.** A design tool emits
  React with utility classes; translate into this tree's `.scss` sheets and Solid `.tsx` components,
  and never add a utility framework the project does not already use.
- **An empty archive is a normal state.** Read every collection with a default and render the
  composition with empty columns; a page that throws on zero records cannot be developed against a
  fresh clone.

## Claim → test

| Claim                            | Test                                                                           |
| -------------------------------- | ------------------------------------------------------------------------------ |
| The config loads                 | `pnpm run build` reaches page compilation, not `Failed to load PostCSS config` |
| The CSS aliases resolve          | `grep -r '@Stylesheet/' Target/` finds no literal `@import`                    |
| Every declared route is emitted  | `find Target -name index.html` matches the routes `Source/pages/` declares     |
| The Node floor is met            | `node --version` is at or above `engines.node` in `package.json`               |
| The build returns its own status | `timeout 420 pnpm run build; echo "EXIT=$?"` prints the build's code           |
| The island hydrated              | the probe reports `hydrated: true` and the island count the route expects      |
| A sheet is imported              | the probe's computed style matches the rule, not the browser default           |

## References

| File                            | Covers                                                           |
| ------------------------------- | ---------------------------------------------------------------- |
| `Reference/Index.md`            | Every archived file in this directory, with its one-line summary |
| `Reference/Build-Repair.md`     | The four config-layer failures, with probes and exact messages   |
| `Reference/CI-Reproduction.md`  | Reproducing a build that fails only in CI                        |
| `Reference/Design-Intake.md`    | Reading a design file's layer tree into a spec                   |
| `Reference/probe-built-page.js` | Serve-and-probe a built page over CDP                            |
