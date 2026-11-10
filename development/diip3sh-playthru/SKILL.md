---
name: playthru
description: Add a scripted, looping product demo to a website using the playthru library. A fake cursor glides over the real UI, clicks, types and zooms the camera in, with no video file. Use when the user wants a hero demo, product walkthrough, animated "how it works" section, or a self-playing demo of their app on a landing page, or mentions playthru.
---

# playthru

playthru plays a scripted demo on the site's **real UI**. A fake cursor glides, clicks real elements, types into real inputs, and a camera zooms in on what matters, then it loops. It has no dependencies, is about 5 KB, and there's no stylesheet to import. Every timing is fixed by the library: there is no speed, easing or duration option, so don't look for one.

The user may not know npm or JavaScript tooling. Do the setup for them, choosing from the paths below, and explain in plain words what you changed.

## 1. Pick the setup path

Look at the project first:

| Project | Path |
| --- | --- |
| Has `package.json` and a bundler (Vite, Next, Astro, etc.) | **A. npm** |
| Plain HTML files, no `package.json`, or the user doesn't want tooling | **B. CDN** |
| React (any framework) | **A** with `playthru/react` (section 4) |

**A. npm.** Run the install with the project's package manager (look for `pnpm-lock.yaml`, `yarn.lock` or `bun.lock`, and use npm if there's none):

```sh
npm i playthru
```

```js
import { playthru } from "playthru";
```

**B. CDN, no install.** This works in any `.html` file. The script tag must have `type="module"`:

```html
<script type="module">
  import { playthru } from "https://esm.sh/playthru";
  // script goes here, see section 3
</script>
```

Put this script after the stage markup, or at the end of `<body>`.

## 2. Make the stage

The **stage** is the element the demo plays inside. Usually it's a box on the landing page holding the app's UI (or a static copy of it).

- Give it a **fixed height** (e.g. `height: 520px`). The camera scales the content inside it, and playthru sets `overflow: hidden` on it.
- It should have **one child**, which becomes the "scene" the camera moves. If there are several, playthru wraps them for you.
- Everything the script touches must be **inside the stage**. Selectors are scoped to it.
- The UI must actually work: playthru fires real events, so the app's own click and input handlers do the work. If the "app" is a static mockup, add small handlers so clicks have a visible effect (open a modal, add a row).
- Give the targets **stable selectors**. Add `id`s or `data-*` attributes rather than relying on fragile class chains.

```html
<div id="hero" style="height: 520px">
  <div class="app"><!-- the real UI --></div>
</div>
```

## 3. Write the script

Chain steps. They run in order, and the chain is the whole demo:

```js
playthru("#hero")
  .click("#new-issue")                 // glide over and click
  .zoom("#composer")                   // camera pushes in
  .type("#title", "Fix onboarding flicker on Safari")
  .click('[data-label="Bug"]')
  .click("#create")
  .zoomOut()
  .zoom(".row.is-new")                 // targets resolve when the step runs,
  .reset(() => app.reset());           // so elements created earlier work
```

By default it starts the first time the stage is 30% in view and loops forever.

| Step | Does |
| --- | --- |
| `move(target)` | Glide the cursor to an element. |
| `click(target?)` | Glide there and click, firing real `pointerdown`, `mousedown`, `pointerup`, `mouseup` and `click`. With no target it clicks the last one. |
| `type(target, text)` / `type(text)` | Click the field, then type with human timing. Works with React and Vue controlled inputs. Without a target it types into the last one. |
| `key(key)` | `keydown` and `keyup` on the last target, e.g. `key("Enter")`. |
| `zoom(target?)` | Camera in on an element, or on the last target. |
| `zoomOut()` | Camera back out. |
| `wait(ms)` | Pause. |
| `run(fn)` | Run custom code as a step (may be async), e.g. to flip app state. |
| `reset(fn)` | Restore app state between loops. Typed-into fields restore themselves; everything else (opened modals, added rows) goes here. |

A target is a CSS selector (scoped to the stage) or a DOM element.

Options are the second argument: `playthru("#hero", { loop, autoplay, pauseOnHover })`. All three default to `true`. `pauseOnHover` freezes the demo and hides the fake cursor while a real mouse is over the stage, so visitors can try the UI.

Controls on the returned object: `.play()`, `.pause()`, `.destroy()`, `.playing`. Set `autoplay: false` and call `.play()` to start it from a button.

**Good demo shape:** 4 to 8 steps that tell one story (open something, fill it in, see the result). Zoom on the part being worked on, then `zoomOut()` before showing the result. Always write a `reset` that undoes everything the script changed, or the second loop will start from the wrong state.

## 4. React

```jsx
import { Playthru } from "playthru/react";

<Playthru
  className="hero"
  style={{ height: 520 }}
  script={(d) => d.type("#todo", "Record the launch video").click("#add").zoom("li:first-child")}
>
  <TodoApp />
</Playthru>
```

Or attach to an element the app already renders: `usePlaythru(ref, script, options)`. It creates the demo once per mount and destroys it on unmount.

- In **Next.js App Router**, the file using `Playthru` or `usePlaythru` needs `"use client"` at the top.
- To reset React state between loops, call the component's own setters inside `reset`, e.g. `d.reset(() => setTodos(initial))`.
- In other frameworks (Vue, Svelte, Astro islands), call `playthru(el)` after mount and `.destroy()` on unmount.

## 5. Hover and focus styles

The fake cursor can't trigger CSS `:hover`, and playthru never moves real focus, so it can't trigger `:focus` either. Instead it marks elements with attributes. Mirror the existing styles onto them:

```css
.btn:hover, .btn[data-playthru-hover] { background: var(--btn-hover); }
input:focus, input[data-playthru-focus] { outline: 2px solid var(--accent); }
```

In Tailwind, use them as variants: `hover:bg-gray-200 data-playthru-hover:bg-gray-200`.

## 6. Gotchas

- **A selector that matches nothing stops the demo** with `playthru: nothing matches "…" inside the stage` in the console. Check that each target exists inside the stage at the moment its step runs.
- **Links and submit buttons don't navigate.** Their default action is prevented. If a click should do something, it needs a JS click handler.
- **Menus outside the stage.** The demo's events reach the whole page. While a menu or popover outside the stage is open, the demo pauses. It detects this through `aria-expanded="true"` (with `aria-haspopup` or a combobox) or `:popover-open`. A hand-rolled popup with neither should ignore events where `event.isTrusted === false`.
- **Can't target** elements inside iframes, `<canvas>` or WebGL.
- The drawn text caret only appears in single-line inputs. Textareas and contenteditable get typed into without one.
- With `prefers-reduced-motion` the cursor jumps, the camera stays still, and loops cut without fades. This is intended.
- On small screens, if the zoom target can't fit at 1.3×, the camera stays out. This is intended.

## 7. Check it

Open the page: start the project's dev server, or for plain HTML serve the folder with `npx serve` or any static server, because ES modules don't load from `file://`. Scroll the stage into view and watch one full loop, then a second to confirm `reset` restores the start state. Check the browser console for `playthru:` errors.

Docs: https://playthrou.diip3sh.xyz
