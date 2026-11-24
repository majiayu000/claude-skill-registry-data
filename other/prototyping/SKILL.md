---
name: prototyping
description: "Clickable flows that test tasks before building them."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, prototype]
    category: web
    related_skills: [web-design, wireframing, usability-testing]
    web_designer_stages: [preview]
---

# Prototyping Skill

Link screens into a clickable prototype that simulates real use without working code, built only for the paths to be tested. This skill covers low-fidelity prototypes from wireframes and high-fidelity prototypes from finished designs. It does not cover the final build, and it does not cover usability testing itself — the prototype is the thing tested, not the test. Load-on-demand only, loaded by the web-designer coordinator for its stages; never auto-loads; never contacts the user directly — the coordinator is the only router.

## When to Use

- To test a flow with users or stakeholders before building, and to validate interactions that a static mock cannot show.
- When a flow must be walked end to end before the build commits to it.
- When the wireframe is agreed and the key paths need a clickable form.
- When a finished design must be walked as a user would walk it, before the build.
- When a broken path must be found cheaply, in the prototype, rather than after launch.
- Not as a presentation: the prototype is a learning tool, and a path that breaks in it has done its job.
- Not for every path: built only for the paths to be tested, not for the whole site at once.

## Prerequisites

- The run is active and the coordinator loaded this skill for its stage or stages.
- The wireframe is agreed, so the prototype links screens whose structure is already settled.
- The key paths to test are named, so the prototype covers them and no more.
- The flows are known, so the prototype can include the happy path, the error path and the exit for each one.

## How to Run

1. Name the paths to test, from the task flows — one path per top task.
   - A path names its task, its start screen and its end state.
   - Paths not named are not built; the prototype stays small and testable.
2. Build the site itself as the prototype where possible, in real HTML, CSS and JavaScript; otherwise build a clickable flow of the key paths.
   - The real site as prototype tests the real interactions, not a picture of them.
   - A clickable flow links the key screens in order, with the interactions that matter.
3. Link the screens so a user can complete a real task by tapping through, including the error path and the exit.
   - Every tap on the path leads somewhere; no tap is a dead end.
   - The error path and the exit are linked, not left as notes.
4. Walk each path end to end and note where it breaks, before the build begins.
   - Walk the happy path, then the error path, then the exit, for each task.
   - Note the exact screen and tap where a path breaks.
5. Treat every broken path as a finding, not a failure: fix the flow, not the prototype's polish.
   - A broken path found now is a launch bug avoided.
6. Record the prototype location, its screenshots and the walkthrough notes in the stage record.
   - Screenshots cover 1440, 768 and 375, so the prototype is checked at every preview width.
7. Re-check after any fix, and record what changed.
   - A fixed path is walked again end to end before the stage closes.
   - The prototype recorded is the one the walkthrough tested, not an earlier draft.

## Quick Reference

- Forms: low-fidelity from wireframes, or high-fidelity from finished designs.
- Build: the site itself as the prototype where possible (real HTML/CSS/JS), otherwise a clickable flow of the key paths.
- Scope: only the paths to be tested.
- Purpose: a learning tool, not a presentation.
- Test: a user can complete a real task by tapping through.
- Screenshots: 1440, 768 and 375.
- Paths: one per top task, named before building.
- Links: every tap on a tested path leads somewhere.
- Error path and exit: linked, not left as notes.
- Findings: broken paths recorded with the exact screen and tap.
- Result: a user can complete a real task by tapping through.

## Procedure

### 1. What it is

Linking screens into a clickable prototype — low-fidelity from wireframes or high-fidelity from finished designs — that simulates real use without working code, built only for the paths to be tested.

### 2. How Hermes applies it

Hermes builds the site itself as the prototype where possible (real HTML/CSS/JS), otherwise a clickable flow of the key paths, and treats the prototype as a learning tool, not a presentation.

### 3. What it returns to the stage

- `preview` stage record: `url_or_path` names the prototype location; `screenshots` maps the 1440, 768 and 375 viewports to captures of the prototype; `console_log` carries the walkthrough notes, including every broken path found.

### 4. Good looks like

A user can complete a real task by tapping through; broken paths are found in the prototype, not after launch.

## Pitfalls

- A prototype built as a presentation: polished screens that cannot be walked, so the paths are never tested.
- Every path prototyped: the whole site built twice, with the tested paths lost among the untested ones.
- A prototype with no error path and no exit: the happy path works and everything else is untested.
- A broken path polished over: the finding is hidden instead of fixed, and the same break ships in the build.
- A static mock called a prototype: no tapping through, no task completed, no interaction validated.
- Testing the prototype with the people who built it: the walkthrough confirms what the builders already believe, instead of what a user does.
- A tap that leads nowhere: a linked screen missing from the prototype, so the path ends mid-task.
- A high-fidelity prototype built from an unagreed wireframe: the structure underneath is still undecided, so the prototype tests the wrong screens.
- Walkthrough notes never recorded: the broken paths are noticed, discussed, and then lost before the build.

## Verification

- A user can complete a real task by tapping through the prototype, on each key path.
- The happy path, the error path and the exit all work in the prototype.
- Broken paths were found in the prototype and recorded, not discovered after launch.
- Screenshots exist at 1440, 768 and 375 for the prototype.
- Every tap on a tested path leads somewhere; no tap is a dead end.
- Walkthrough notes name the exact screen and tap where each path broke.
- Every tap on a tested path leads somewhere; no tap is a dead end.
- The prototype covers only the paths named for testing, not the whole site at once.
- Walkthrough notes name the exact screen and tap where each path broke.
- Broken paths were fixed in the flow, not polished over in the prototype.
- The stage record carries the prototype the walkthrough tested, with its screenshots and notes.
- The responsive judger checks the prototype across viewports; the visual and content judgers check the paths it shows. The skill does the work and the judgers check it; the skill never grades its own output.
- A simulated review is not a substitute for real users: audit 3.25 says so plainly, and a prototype walkthrough by the builders does not claim otherwise. Five real users per round remain the test that counts.

## Coordinator wiring

Loaded by stages: preview. Returns: `preview.url_or_path` (prototype location); `preview.screenshots` (1440, 768 and 375 captures); `preview.console_log` (walkthrough notes, broken paths found). Judger boundary: responsive judger checks the prototype across viewports; visual and content judgers check the paths it shows.
