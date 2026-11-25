---
name: interactive-explainer
description: Builds a single self-contained, playable HTML explainer for a tool, extension, feature or system we built, with a global state switch, a live model of the system, and a "try it" lab that runs the real rules. Use when asked to explain or demo something we made, or to make an "interactive explainer". For someone else's article, use article-explainer.
metadata:
  category: visual-media
---

# Interactive explainer

Make one offline HTML file that lets the reader **play with a system** until they understand it. The reader should finish knowing what it does, when each setting matters, and what it will refuse to do.

`examples/pi-optmem.html` is the reference Iury loves. It explains the pi-optmem extension. Study it for **taste and mechanics**. Don't copy its palette, copy or section order. Derive each page from its own system.

## When to use it

| Explaining | Use |
|---|---|
| Someone else's article, paper or idea | `article-explainer` (one scroll-driven diagram, no widgets) |
| Something we built: a tool, extension, mode, pipeline, policy | **this skill** |
| A quick answer in chat | `show-me` |

The two explainer skills differ on purpose. An article has a model to *show*. A system has state to *poke*.

## The thesis

The page is a **live model of the system**. State lives in one place, and every part of the page is a view of it. The reader changes the state and watches everything respond.

Every section needs one interactive element or one diagram. Never a wall of prose. (Iury has ADHD: scannable beats dense.)

## Process

1. **Read the real code and docs.** Find the system's actual states, rules and defaults. Note the one variable that changes behaviour most (a mode, a profile, a flag, a stage).
2. **Name the problem in one sentence.** The hero headline is the pain it removes, as a plain metaphor ("a light switch for the whole house").
3. **Pick 4 to 6 components** from the menu below. Skip any that don't fit the system.
4. **Copy rules from the code, never invent them.** The lab must run the same logic as the real implementation, simplified only where marked "(simplified)".
5. **Build, then verify** (see Checks).

## Component menu

| Component | Use when | Mechanic |
|---|---|---|
| **Hero with state switch** | The system has 2 to 4 modes | Segmented control sets `body[data-mode]`. One CSS var `--mode` recolours the headline accent, panels, chips and the sliding thumb. |
| **Machine panel** | There are layers, parts or permissions | Dashed layers that become `lit` (solid, tinted) or `dim` (struck through) per mode. Chips for tools or capabilities turn `on`. |
| **Request anatomy** | You need to show what actually gets sent, stored or loaded | Dark monospace packet, one row per part. Highlight what is added, strike through what is stripped. |
| **Data-structure explorer** | The system has a tree, graph or queue | Clickable nodes expand in place, with a small SVG that mirrors the open state. Reset button. |
| **Day-in-the-life stepper** | There is a workflow over time | A segmented progress track, a terminal on one side, plain prose on the other. Prev and next buttons. Each step shows a real command and its output. |
| **Try-it lab** | There are rules that allow or refuse things | A text input, sample buttons, and one verdict card per mode (allow or block) plus a one-line reason. Highlight the current mode. |
| **Reference** | There is configuration | Precedence list: where each setting comes from, in order. |
| **Pipeline strip** | There are stages | Cards joined by arrows, with a timer cycling a `hot` highlight. |

Add a sticky nav with the section names and a status pill that mirrors the current state.

## Style

- Pale paper with a faint dot grid, one dark ink, one muted grey.
- A serif display face for headlines. Sans for body. Mono for labels, code, nav and anything the system itself prints.
- Colours carry meaning and are named by it: `--off`, `--read`, `--on`, `--block`, `--ok`. Pick the set from the system's states, not from taste.
- Dark panels only for things the machine prints (terminals, packets, wake views).
- Generous section padding, hairline dividers, rounded panels. No gradients, no stock icons.
- Respect the reader's attention: motion shows a state change, never decoration. Honour `prefers-reduced-motion`.

## Rules

- **Single file.** Inline CSS and JS. No libraries, no CDNs, no network. Use system font stacks.
- **One state object, one render function.** Components subscribe to it. Don't scatter toggles.
- **Accessible controls.** Real `<button>`s, `aria-pressed` on toggles, `aria-label` on icon-only or segment buttons, visible `:focus-visible`, and keyboard-reachable everything.
- **Plain copy.** Short sentences. Say what the system does, then what the reader can try. Use the system's real names for commands and files.
- **Honest scope.** Mark simplified logic. State what the page does not cover.
- **Defaults on first paint.** The page must look complete before any click, in the system's most common state.
- **Responsive.** Grids collapse to one column under about 800px.
- **No secrets or private paths** in samples. Use placeholders.

## Checks

1. Open the file in a browser (agent-browser). Click every control and sample button. Confirm no console errors.
2. Compare lab verdicts with the real implementation for at least five inputs, including edge cases.
3. Tab through the page with the keyboard. Every control must be reachable and visibly focused.
4. View at about 390px and 1440px wide. Nothing overflows.
5. Read the headings alone. They should tell the story.

## Output

Write to `<project>/ai-artifacts/<topic>/explainer.html` unless told otherwise, and give the user the `file://` path.
