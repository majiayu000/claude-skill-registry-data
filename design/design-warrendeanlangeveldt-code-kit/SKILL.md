---
name: design
description: Design a design story's screens with the person before any of them is built, and record each approved design so its screen can be coded. Reads the screens the specs list, designs them in the project's design tool (Paper, Figma, Pencil) or as design files under design/, shows them, iterates on the person's feedback, exports each approved screen's states into design/ as files a lane can read, and adds them to the design register the design gate reads. --hand-over exports designs approved before that are still only in the tool. Use when code-kit next or the loop gives the design step, when a lane was refused for a screen whose design isn't approved, or runs /code-kit:design [story IDs].
---

# Design before code

A screen is designed and approved before anyone builds it. The design gate refuses a lane writing a screen file until the design register holds its exported design (an entry naming only an artboard in the tool doesn't count), and the plan's screen stories depend on their design story, so nothing is dispatched early. Designing is the lead's work with the person: you propose, they decide.

The CLI is `node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs"`.

## 1. What to design

For each story given (`**Lane:** design` in the plan):

- read the requirements it cites and the `## Screens` section of their specs: each screen, what it shows, what the person can do there, and its empty, loading and error states. A screen is a `###` or `####` heading, a `- **Name** (…)` bullet or a table row, by its exact name, with a `**States:**` line or a States column. If the story designs only some of a spec's screens, name them in the plan with a `**Screens:**` line under the story;
- read the architecture for the design tool and the folders screens live in, and the principles for the brand, theme and accessibility targets;
- look at the designs already approved (`design/register.json` and what it links to), so the new screens match them.

If the specs don't list the screens, or leave a state out, ask the person now rather than inventing it.

## 2. Design

Use the project's design tool:

- **A design tool connected to this session** (Paper, Figma, Pencil, whichever the architecture names, or the one the person uses): design each screen there, one artboard per screen and state, with the project's tokens.
- **None:** write each screen as a static HTML and CSS file under `design/<area>/<screen>.html`, at the sizes the product targets (phone, desktop), opened in the browser to check it.

Use the spec's own content: the real labels, fields, messages and limits from its requirements, never lorem ipsum or placeholder screens. Every state the spec lists gets a design. Follow the principles for theme (light and dark, if both), type, spacing and accessibility.

## 3. Show it and iterate

**Under vibe** (`harness.autonomy` is `vibe`), you approve each screen yourself: check every state against the spec's Screens section, the principles and the project's tokens, fix what falls short, and approve it with `code-kit approve design --delegated --story ST-n --reason "…"` when the register is written. Skip the showing below; the person isn't asked.

Show the person each screen (a screenshot, or the file to open) with one line on what it does and which requirements it serves. Ask what to change. Make the changes and show them again until they say a screen is approved. A screen they want rethought goes back to step 2; one that needs the spec changed goes to `/code-kit:spec-design` first.

## 4. Export what's approved

A lane agent has no connection to the design tool: it builds from files in the repository. So when the person approves a screen, export every state they approved into `design/<area>/<screen>/<state>.<ext>` (`design/bookings/list/empty.png`, `design/bookings/list/empty.jsx`) before you record it, as it was approved: an artboard changed afterwards is a new approval. For each state, its code where the tool gives code, and a PNG at the size the product targets; once per project, the design tokens as JSON (`design/tokens.json`).

- **Paper:** `get_jsx` and `get_computed_styles` for each artboard, `export` for its PNG, `get_tokens` for the tokens.
- **Figma:** its MCP server's code and screenshot tools for each frame, and its variables for the tokens.
- **Claude Design and artifacts:** the page's HTML, read through the artifact; a headless browser's screenshot of each state for the PNG.
- **Pencil, or HTML files under `design/`:** the HTML is already the code; a headless browser's screenshot gives the PNG.
- **Anything else:** whatever code it gives, and the PNG. A tool that gives no code has an image only, and the state says why.

The export is the target the lane matches, not code to paste: it builds the screen from the project's design system and components.

## 5. Record the approved designs

For each approved screen, add an entry to the register, naming the code file the lane will write (from the architecture's folders and the project's routing), the screen as the spec's `## Screens` section names it, and every state with its files, the viewport it was drawn at and the sha256 of each file (`shasum -a 256 <file>`):

```json
{
  "screens": [
    {
      "file": "apps/web/app/bookings/page.tsx",
      "screen": "Bookings list",
      "story": "ST-1",
      "approved": "2026-10-11",
      "source": { "tool": "paper", "ref": "<file id> — Bookings list" },
      "tokens": "design/tokens.json",
      "states": [
        {
          "name": "default",
          "code": "design/bookings/list/default.jsx",
          "image": "design/bookings/list/default.png",
          "viewport": "390x844",
          "sha256": { "code": "<sha256>", "image": "<sha256>" }
        }
      ]
    }
  ]
}
```

`story` is this design story. One design can serve several code files, such as the web and the mobile screen: each has its own entry, naming the same states. Committing the register is refused while an entry names a file that isn't there, a hash that isn't the file's, a state with no image, or leaves out a state the spec lists for the screen; `code-kit designs` lists every entry and what's wrong with it.

The register is protected by the `design` approval, which is the person's: writing it is refused until they approve, and in a session with the code-kit mod the write waits in the band for their Approve. Give the approval a reason in their words ("bookings list and detail, as shown"). Then commit the designs and the register on `design/st-<n>`. Commit each screen as the person approves it: the story reads as in progress until every screen it designs is in the branch's register (or you set its `**Status:**` to `review` in the plan), and then `code-kit next` sends it to review. Review and merge it like the lead's own story. Once it's merged, `code-kit next` dispatches the screen stories that waited on it.

## Handing over designs approved before (`--hand-over`)

`code-kit next` names register entries whose design is only in a design tool ("6 approved screens are only in paper"), and holds every story that builds one of those screens, giving the `design` step with `handOver: true` and the design stories to hand over; a lane's write to such a screen is refused until it's handed over. For each, find the artboard the entry names, and ask the person whether it's still the design they approved: the tool's copy may have changed since. Once they confirm, export it as in step 4 and rewrite its entry as in step 5. Then, for each of those screens that's already built, compare the build with the export as the review does (each state's screenshot beside its PNG), and add a fix story to the plan for each difference, citing the screen's requirements.

## 6. Report

Say which screens were approved, which are still open and why, and what's dispatched next.
