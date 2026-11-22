---
name: polish
description: Audit the UI and UX of what we are working on at a chosen level of polish, open the proposed changes as a report the owner answers in their browser, then build what the owner approves. Product code stays untouched until approval. For a site whose code is not in the repo, the approved changes become a report to share. Use when the user invokes /vstack:polish or $vstack:polish, or the older /vstack:design-review, asks for a design review, design audit, UI or UX review, or another review round, or wants a screen or app to look more polished, premium or consistent, even if they do not say "review". To comment on a wireframe, page or running app with no audit, use vstack:review.
---

# Polish

Audit first, propose second, build after the owner approves. The owner answers the proposal in a report page, in their own browser tab, before any product code changes.

Read `lenses.md` before Step 3 and `report.md` before Step 4. Both sit beside this file.

## Host

Follow §0 of `../review/SKILL.md` to load the adapter for your host. This skill uses the Host ops `run`, `edit`, `background`, `watch_stream` or `watch_next`, `stop`, `browser_capture`, `user_browser` and `subagent`, defined in `contracts/host.md`. Where the adapter says an op is not available, follow what this file says to do without it.

## Step 1: Set the scope and open the review

The skill runs inside a conversation, so take the target and any focus areas from the current work. Ask only if the conversation leaves the target unclear.

The owner picks the level of polish in the review page, not in chat:

| Level | 中文 | Aim |
|---|---|---|
| **Clean** | 简洁 | Looks right. Clear hierarchy, consistent spacing, an aligned grid, and consistent type, colour, components and copy at every width. No new effects. |
| **Refined** | 精致 | Clean, plus works right. Links, forms, loading and controls behave as users expect, and nothing loads in a jarring way. No new effects. |
| **Showcase** | 惊艳 | Refined, plus the finishing touches that make it stand out: animation, parallax, smooth transitions, scroll interactions and playful details, built on one brand idea. |

The level decides which part of `lenses.md` applies. Clean and Refined find defects and add no new effects. Showcase proposes the effects.

The mode decides which checks apply within each level: **Website**, **Web app**, or both for a product that has both. Pick it for each flow, as in *Modes* in `lenses.md`.

The delivery decides what happens to the approved changes:

| Delivery | When | Step 5 |
|---|---|---|
| **Build in this repo** (`build`) | This repo holds the code for the screens in scope. | Build the approved changes. |
| **Report only** (`report`) | The code is elsewhere, such as a live site or someone else's product. | Write a report of the approved changes to share. |

Pick the default from the repo. The page shows both, and the owner may change it before picking a level.

The owner also sets these in the page. Each is saved with the pick:

| Setting | Key | Default | What it changes |
|---|---|---|---|
| **Effort**: Low, Medium or High | `effort` | `medium` | The model and reasoning effort the work runs at. See *Run at the chosen effort* below. |
| **Proofread** (experimental) | `proofread` | `false` | The report's words and new UI copy go through `vstack:proofread`, in Step 4 and Step 5. |
| **Trim AI filler** (experimental) | `trimCopy` | `false` | The review adds check CX1 in `lenses.md`. |

If `.vstack/local/polish/` holds an earlier round for this target, also follow **Later rounds** below. Rounds from before the rename sit in `.vstack/local/design-review/`; read them there and save the next round under `polish/`.

Open the review before you audit:

1. Write the answers file, `.vstack/local/polish/<target>-round-<n>.json` from the project root:

   ```json
   {"stage": "choose", "delivery": "build", "canBuild": true, "decisions": {}, "overall": "", "revised": {}}
   ```

   Write `"delivery": "report"` and `"canBuild": false` when the code is not in this repo. If the owner already named a level in chat, or this is a later round, write `"stage": "audit"` and `"level"` instead. The page then skips the choice.
2. Copy `assets/review-start.html` to `<target>-round-<n>.html`, unchanged.
3. Serve the page with Host op `background`. It opens in the owner's browser:

   ```bash
   LIB=<this skill dir>/../../lib
   R=.vstack/local/polish/<target>-round-<n>
   node "$LIB/json-bridge.mjs" serve --json "$R.json" --template "$R.html" --tool polish --port 0 --host <host id>
   ```

   Pass your Host profile's `id`, such as `claude` or `codex`, so the page names your agent. Give the owner the whole URL it prints, because the token is part of it.
4. Arm the watcher, passing the seq the server printed. Use the watch op your Host profile's `capabilities.watch` names:

   | `capabilities.watch` | Host op | Command |
   |---|---|---|
   | `stream` | `watch_stream` | `node "$LIB/json-bridge.mjs" watch --json "$R.json" --stream --tool polish --seq <seq>` |
   | `pull` | `watch_next` | `node "$LIB/json-bridge.mjs" watch --json "$R.json" --tool polish --next --timeout 25 --seq <seq>` |

   A bounded wait returns one event, or `IDLE`, and ends with a `WAIT` line. Run the command on that line to wait again, after you have acted on the event. Keep waiting until `APPROVED` or `CLOSED`, and do not end the turn while the owner is still answering. How the link behaves is in [`contracts/bridge-loop.md`](../../contracts/bridge-loop.md).
5. Recommend a level, as in *Recommending a level* in `lenses.md`, while the owner reads the panels. Write it to the answers file as `recommend`, with a one-sentence reason in both languages. The page marks that panel **Recommended**.
6. Wait for `SENT`. Do not start Step 2 until the answers file holds a `level`.

The pick also saves `lang`, `en` or `zh`, the language the page showed, and the `delivery`, `effort`, `proofread` and `trimCopy` the owner kept.

### Run at the chosen effort

The Host profile's `effortLevels` names a model and a reasoning effort for each of `low`, `medium` and `high`.

- If the profile has `effortLevels`, start Steps 2 to 4 with Host op `subagent`, passing the model and effort named for `effort`. Give it this file, the answers file's path and the target. Start Step 5, and each revision after `SENT`, the same way.
- Keep serving the page and answering watcher events yourself while it works.
- If the profile has no `effortLevels`, do the work yourself on the session's model.

### Show progress

Keep the page current while you work through Steps 2 to 4:

1. Once the level is known, add `tasks` to the answers file and set `stage` to `audit`. Keep every other key. Write four to seven tasks, each in both languages. Once the survey is done, name the tasks after it, such as the sections walked and the states opened:

   ```json
   {"id": "capture", "text": {"en": "Capture the screens", "zh": "截取各个页面"}, "done": false}
   ```

2. Tick each task as you finish it:

   ```bash
   node "$LIB/json-bridge.mjs" patch --json "$R.json" --id capture --set done=true
   ```

3. If you cannot finish, set `problem` to one sentence in the owner's language and say the same in chat. Say what the owner must do before pressing **Retry**, such as signing in.

## Step 2: Read the current instructions

Read the project instructions and anything design-related: the design guide, frontend contract, token file and stylesheets. Then read the code for the screens in scope. The review must fit the rules the project already has.

## Step 3: Look at the work

Open whatever we are working on, whether that is a dev server, a preview or a live site, with `browser_capture`. Use the screen sizes in `lenses.md`, and choose the themes and states from the requirements. Cover the page as in *Covering the page* in `lenses.md`: survey it first, then give every check a verdict.

If the target asks for a sign-in, such as IAP, Google sign-in or SSO, open it with `user_browser` and ask the owner to sign in there. Capture from that tab. Never type a password yourself.

If the adapter says `browser_capture` is not available, ask the owner for screenshots of each screen and take sizes from the stylesheets. Say in chat what you could not measure.

Collect evidence:

- Screenshot each screen and each opened state, and save the images a finding will need. Capture fresh in every round, and record the screen size of every picture.
- Measure with JavaScript in the page: `scrollWidth` against `clientWidth`, heights, counts, font sizes, contrast. Use numbers in findings, because "33 cards, 4,312px" can be acted on and "feels heavy" cannot.
- Stress the layout with the longest title, the largest list and an empty list. Check for sideways overflow.
- Read the console for errors, where the host's browser tools can reach it.

## Step 4: Write the review

1. Write the findings with the checks for the chosen level and mode:
   - Name the check that failed, with its evidence and its location in the code. See *How to report a failed check* in `lenses.md`.
   - Propose a concrete change with values, such as "13.5px, weight 600, two-line clamp".
   - Show every finding as a before and after pair of screenshots of the product, with one short title. See *Pictures* in `report.md`.
   - Report one finding per kind of defect.
   - Show two or more ways to fix one problem as variations of one section. See *Variations* in `report.md`.
   - For a change to something the owner clearly chose, offer a way to keep the idea, such as a variation.
2. Build the review as one self-contained HTML page. Copy `assets/report-template.html` and fill it, in the format in `report.md`. Save it over the start page at `$R.html`.
   - Write every word in English and in Chinese. See *Two languages* in `report.md`.
   - Write for the owner in plain words, with no ratios, pixel sizes or design terms. See *A section* in `report.md`.
   - Cut every word a picture already says. A title, a reason of one or two sentences, and one detail per picture are the whole text.
   - If `proofread` is true, run `vstack:proofread` on the titles, reasons and captions. Read `../proofread/SKILL.md` and follow it. If it stops, say why in chat and carry on.
3. Set `stage` to `report` in the answers file. Keep every other key. Write the HTML first: the open tab reloads into the report as soon as `stage` changes.
4. Reply in chat with the verdict, the top changes, what already works and what you did not test. Keep the reply short.

Product code stays unchanged until the owner chooses **Approve & finish** or says to build.

Answer each watcher event:

| Event | Action |
|---|---|
| `SENT`, while `stage` is `choose` | The owner picked. Read `level` and `lang`, start *Show progress*, and continue at Step 2. |
| `SENT`, with `retry` set | The owner pressed **Retry**. Delete `retry` and try the step that stopped again. |
| `SENT` | Read the answers file. Revise every steered section and add variations to every `vary` section, as in *How the owner answers* in `report.md`. Do not build anything yet. |
| `APPROVED` | Build the approved sections, or write the report, in Step 5. |
| `CLOSED` | Say the link is closed. The answers file keeps the last send. If it closes during the audit, finish the report, then serve the page and arm the watcher again. |

Do not build a Rejected, a steered, a `vary` or an unanswered section.

## Step 5: Build or report

If `delivery` is `report`, write the report and build nothing:

1. Copy this round's page to `<target>-report.html`.
2. Keep only the approved sections. For a section with variations, keep only the Proposed figure the owner approved.
3. Add `data-decision="approve"` to each kept section, and `data-handoff` to the `<html>` element. The page then shows every section in one read-only scroll, with no buttons.
4. Change the eyebrow to say Polish report.
5. Open the file in the owner's browser. If the adapter offers `share`, offer to publish it.

Otherwise, build what the owner approved, one slice at a time.

- Follow the target repo's own workflow for specs, branches, tests and release.
- After the tests pass, look at the slice in a browser with long content and real-sized data.
- If `proofread` is true, run `vstack:proofread` on any new UI copy, as in Step 4.
- Report after each slice: what changed, how you verified it, and what you left out.
- Ask first if a change alters what a screen is for. Moving a type of item off the main board is one example.

## Later rounds

A later round reviews what the last round built. Earlier fixes can create new problems or move an old one elsewhere. Read the last round's page, and save this round under the next number.

- Reuse the last round's level and mode, unless the owner asks for another.
- Mark each earlier area **Landed**, **Landed, broken** or **Moved**.
- List bugs the slices introduced first. Fix a bug that blocks use in its own small change.
- Look for what the fixes made louder.
- Carry forward sections the owner left unanswered.
- Say in chat where you would stop polishing.

## Notes

- **Browser pass.** Tests miss layout faults. In the first run, visual passes caught overflowing tabs and hidden filter chips. A long title that made the panel scroll sideways shipped because no test used one.
- **Louder after a fix.** In the first run, removing the empty grey cells left one 4,312px column as the heaviest thing on the board.
