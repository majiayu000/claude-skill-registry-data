---
name: guide
description: Walk the user through a multi-step task (e.g. cloud console / permission / dashboard setup) with a live step tracker that is re-printed at the bottom of every reply so they never scroll up. Use when the user asks to "guide me through", "walk me through", "give me step by step" instructions, "how do I set up ..." for a UI/console task, or invokes guide. Also use when, mid-guide, they say a step "isn't working", "the menu isn't there", or ask a clarifying question about a step.
effort: medium
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Guide

Build instructions from evidence for the task's current flow, then keep the user oriented by
**re-printing a live step tracker at the very bottom of every reply**. This solves the core
annoyance: when the user asks a follow-up, the instructions scroll out of view and they have
to scroll up and down. With this skill, the next steps are always the last thing on screen.

## The tracker block (the key mechanic)

Every reply while a guide is active **ends** with a tracker block — it must be the last thing
in the message, so it stays pinned to the bottom. Format:

```
---
✓ Steps 1–4 done
▶ 5. Open the Roles list  ← you are here
    On the open IAM page, click Roles in the left sidebar.
    You should see a list of roles.
  6. Open the role's details
    In the Roles list, click site-reader.
    You should see that role's permissions.
```

Rules for the block:
- **Render it as a fenced code block** (triple backticks), exactly like the example above.
  This preserves the indentation and the `▶`/`✓` markers in a terminal. **Never** use HTML
  entities like `&nbsp;` or markdown list syntax to indent — they render literally as text in
  many clients. Plain spaces inside the code fence are all you need.
- **Collapse done steps to one line**: `✓ Steps 1–N done` (omit the line if none are done).
- Mark the current step with `▶` and `← you are here`.
- List every remaining step in full after the current one, indented two spaces.
- **Keep the instructions, not just their titles.** Include the navigation, action, and
  expected result needed to carry out each remaining step. Use continuation lines indented
  four spaces; there is no one-line limit. The user must not need to scroll up to recover
  a URL, click path, value, or command. Put clickable links in the prose too, since links
  inside the code block render as plain text.
- If the user is stuck on the current step, append `(stuck)` to it: `▶ 5. … (stuck)`.
- Nothing comes after the block — no sign-off, no extra prose.

## Instructions

### Step 1: Verify against current docs before planning
If the task touches a **third-party console, dashboard, or API that changes** (cloud
providers, app stores, SaaS settings pages), look up the current official docs *before*
producing the plan. Cover the full known flow, including prerequisites, required permissions,
and whether actions belong to an account, project, or individual app. **A plan naming several
consoles needs a verified navigation source for each** — one vendor's integration guide does
not license another vendor's clicks, and the part you feel unsure about is not the only part
that needs checking. Skip this check only for stable/local tasks with no changing external
workflow.

**Fetching a page verifies only what its contents support.** Check each menu path, button,
prerequisite, and role claim against the relevant passage or an observed live UI, and ask
lookup tools what the documented flow is without naming the menu or role you expect. A
summary, example URL, or search snippet does not establish a current menu; inspect the
underlying passage when one is ambiguous or conflicts with another source. Quote sources by
the global rule: paste the line, and read a canonical list in full instead of grepping for
the items you expect to find.

**Any path not traceable to a fetched passage is unverified.** Mark it `(unverified)` in the
plan and the tracker and keep it a pending verification step, never a confident click path.
Resolve it from the user's visible screen before sending them through it; independent
verified steps may proceed. Link the official sources beside the steps they support, and say
which details remain uncertain.

**A contradicted memory invalidates the domain.** A lookup that corrects your memory of one
part of a product makes every remembered path for that product stale; re-verify each before
use rather than treating the correction as isolated.

Apply this check to each new phase or branch before adding its instructions — a check of one
phase does not verify later phases, and the user need not request another lookup. **Re-run it
for the remaining phases before advancing the tracker if the plan is more than a day old.**

### Step 2: Do the opening agent actions, then produce the plan
Decide who can perform each action using the tools, access, and authorization already
available, and respect an explicit request to learn or do something themselves. Before
presenting the guide, complete and verify every consecutive opening action you can take
yourself; briefly report the results above the plan and omit them from its numbering. Start
step 1 at the first action requiring the user's input, access, or interaction. If you can
finish the whole task yourself, do so and report the result without starting a guide.

For an agent action that depends on earlier user progress, keep its place in both the plan
and tracker as a handoff: **"Tell me when you reach this step; I'll [specific action]."**
Make clear what you will do and what result to expect. Do not give the user manual commands
or clicks for work you can perform, or run it before its prerequisites are ready.

Give a one-line intro, then the **complete numbered list of remaining steps**, then the
tracker block with `▶ 1` as the current step. Keep steps:
- **One action each** — a single, verifiable action or check. Include the navigation needed
  to reach it as indented detail; split independently checkable actions into separate steps.
- **Executable without guessing** — name the website or app, give its URL or launch path,
  identify the relevant account/project/repository, then give the ordered clicks from the
  user's current location. Use the visible menu and control labels, their locations, the
  value to enter or inspect, and **what they should see** when done. Reuse a location already
  established by the preceding step, but spell out navigation when the location changes.
  Fill known names and URLs from context; explain any placeholders the user must replace.
  "Confirm X", "configure Y", or "enable Z" alone is a title, not an instruction.
- **In order** — number them stably; never renumber later (positions are how the user refers
  to a step).

Before sending, read the plan and tracker as someone unfamiliar with the interface: can
they tell where to go, what to do there, and how to recognize success? Add missing detail
to both. On later turns, expand an underspecified step within its existing number.

### Step 3: Advance as the user progresses
When the user signals a step is done ("done", "next", "ok", "✓"), move `▶` to the next step,
fold the finished one into the `✓ Steps 1–N done` line, and re-print the tracker. Keep any
brief acknowledgement above the block.

When the user reaches an agent handoff, perform and verify that action, then any consecutive
agent actions whose prerequisites are ready. Confirmation that the preceding user step is
done also counts as reaching the handoff; do not require another "ready" message. Mark agent
steps done only after verifying success, then resume at the next user step with the existing
numbering. If an agent action fails, keep it current and diagnose the failure before advancing.

### Step 4: Handle "this step isn't working" / clarifying questions
When the user reports trouble or asks about a step, in this order:
1. **Answer the specific problem first** — diagnose, give the fix or 1–3 things to check for
   *that* step. This goes at the top of the reply.
2. **Re-print the tracker** at the bottom with the stuck step marked `(stuck)`.

Do **not** re-list steps the user already completed (beyond the one-line summary). The whole
point is that they don't scroll — keep the answer tight and the remaining steps below it.

If the user's screen contradicts a step, treat that as evidence against the instructions.
Recheck the relevant official docs or live UI before giving another route; do not merely
offer a lookup or repeat the disputed path. Ask what they see if that is needed to identify
the page. Verify any alternate route, search bars and direct links included. **Never reverse
a claim from memory** — if you told the user X and now believe the opposite, look it up
before saying either. Explain the correction and update affected remaining steps while
preserving completion and numbering. If verification is still inconclusive, say so and keep
the step stuck. Diagnose permissions or a changed UI only when evidence supports that
explanation.

### Step 5: Re-print on every turn
Regardless of what the user says — a question, a tangent, a "wait, why?" — end the reply with
the tracker block. The next steps must always be the last thing on screen.

### Step 6: Finish
When the last step is done, confirm completion in one or two lines (and how to verify the end
result). No tracker block on the final message — the guide is over.

The guide is not a persistent mode — it ends naturally at the last step, or the moment the
user explicitly ends it ("stop", "exit guide") or moves to an unrelated topic. On exit, stop
re-printing the tracker. A bare "done" with steps remaining means the current step is done;
advance under Step 3 unless the context indicates they want to stop the guide.

## Examples

### Example 1: A fetch does not support the remembered path

The fetched setup instructions describe creating a service account in a cloud console and
inviting its email through the app provider's Users and permissions page. They contain no
project-linking step.

Build the guide from those documented actions and cite them. Do not prepend a remembered
"Setup → API access → Link project" step, and do not report the flow as checked. If the docs
do not establish the permissions needed to invite users, verify that separately before
telling the user to contact an account owner.

### Example 2: The user's screen contradicts the guide

User: "I don't see the Permissions tab."

Recheck the relevant source before replying. Suppose it mentions a Permissions page but
does not establish how to reach it from the user's screen. Reply with a link to that source,
explain the limit, and keep the tracker:

> I rechecked the docs: they describe a Permissions page, but don't confirm the tab I told
> you to open. That instruction is still unverified. What page title and navigation items
> do you see?
>
> ```
> ---
> ✓ Steps 1–2 done
> ▶ 3. Identify the access-management page from your current screen  ← you are here (stuck)
>   4. Grant access using the verified controls
>   5. Confirm the account appears with the intended role
> ```

If the recheck establishes a corrected route, cite it and replace step 3 with that route.
Preserve the user's completed steps in either case.

### Example 3: A check needs a route and an observable result

The user receives "2. Confirm Pages source is GitHub Actions" and does not know where to
look. After verifying the route in the current
[GitHub Pages documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site),
expand step 2 in place. Use the actual repository URL when known; `OWNER` and `REPO` below
stand for its owner and name. Checking a value does not imply changing it.

Reply with a clickable repository link and the source above the tracker, then:
>
> ```
> ---
> ✓ Step 1 done
> ▶ 2. Confirm the GitHub Pages publishing source  ← you are here
>     Open https://github.com/OWNER/REPO in your browser.
>     Below the repository name, click Settings. If it is hidden,
>     open the … menu in that row and choose Settings.
>     In the left sidebar's Code, planning, and automation section, click Pages.
>     Under Build and deployment, read the Source dropdown's selected value.
>     It should say GitHub Actions. If it differs, tell me what it says.
> ```

### Example 4: Agent work before and during the guide

The task requires preparing a local config, having the user choose an export folder in a
desktop app, updating the config to use that folder, and having the user try an export.
You have tools and authorization to prepare and update the config. In this example, the
app is already open and its observed UI establishes the controls used below.

Prepare and verify the config first. Report that it is ready, then start the guide:

> 1. In the app, open Preferences → Export and click Choose folder. Select your export
>    folder and confirm its path is displayed beside Choose folder.
> 2. Tell me when you reach this step and which folder you chose; I'll update the config
>    and check that it points to that folder.
> 3. Close Preferences, then choose File → Export. Open your chosen folder in the file
>    manager and confirm the exported file appears there.
>
> ```
> ---
> ▶ 1. Choose the export folder in the app  ← you are here
>     Open Preferences → Export and click Choose folder.
>     Select your folder; its path should appear beside Choose folder.
>   2. Tell me when you're here and the folder path; I'll update and check the config
>   3. Try an export
>     Close Preferences, then choose File → Export.
>     Open your chosen folder in the file manager and confirm the file appears.
> ```

When the user says "folder selected: /tmp/exports", update and verify the config, mark steps
1–2 done, and resume at step 3. If the update fails, keep step 2 current until resolved.

## Troubleshooting

### The tracker keeps drifting up the screen
**Cause:** The block wasn't the last thing in a reply, or a turn skipped re-printing it.
**Solution:** End *every* reply with the tracker and put nothing after it. Even for a one-word
answer to a tangent, append the block.

### Steps are too coarse to report a precise sticking point
**Cause:** A step bundles several actions ("set up the role and assign it").
**Solution:** Split into single-action steps so the user can say "stuck on 5" precisely.
Re-derive the plan at finer granularity, but don't change earlier numbering the user already
used; continue from where they are.

### The user's menu/option doesn't match the instructions
**Cause:** The instructions may be wrong; the account context or UI may also differ.
**Solution:** Follow Step 4's recheck before giving another path. A missing control alone
does not establish a permissions problem or prove the provider changed its UI.

### The user jumps around (does step 5 before 3)
**Cause:** Non-linear progress.
**Solution:** Track actual completion, not position. Mark whichever steps are truly done in
the `✓` summary (e.g. "✓ Steps 1, 2, 5 done"), set `▶` to the step they're now working, and
list the rest.
