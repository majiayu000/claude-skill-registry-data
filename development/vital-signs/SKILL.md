---
name: vital-signs
description: Katara checks the vital signs so she knows the patient is really well, not just quiet. Use for create-verification-skill, /create-verification-skill, "make a control skill for this repo", "make a driver skill for this repo", or when a project has no scripted way to prove UI, CLI, or service behavior. Generates a project-local verify skill that drives the app the way a user does, in any language, framework, or platform, and proves it end to end.
---

# Katara's vital signs

A healer does not take the patient's word that they feel fine. She checks the pulse, the breath, and the color, and she knows what healthy looks like for this patient. A verification skill is that check for an app. It launches the real thing, drives it the way a user does, and captures evidence that the feature is alive.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

Every serious project needs a scripted way to drive the real app and prove behavior. It launches the app, exercises a feature the way a user would, and captures evidence. This skill generates that as a project-local skill tailored to the repo, named `verify`.

- **Claude Code.** Write it at `.claude/skills/verify/` in the repo root. A project skill by that name replaces Claude Code's bundled `/verify`, which only the user can invoke, so every skill that names the driver skill (for example `healing-water`) can call the project one ([Claude Code 2.1.200 or later](https://code.claude.com/docs/en/skills#run-and-verify-your-app)).
- **Codex.** Write it where Codex discovers repo skills, `.agents/skills/verify/` in the repo root.
- **Monorepo.** Write it in the touched package directory instead.

You write the output for the next agent, not for a human. It will be read cold, mid-task, by an agent that has never seen the app.

## 1. Interview the repo, not the user

Answer these from the codebase. Ask the user only what you cannot observe.

- **Surface.** What does a user actually touch? A web UI, a CLI or TUI, a desktop app, an API, a mobile app, a library? A repo can have several. Pick the primary one and note the rest.
- **Run.** How does the app start locally? Prefer the repo's own documented dev command (package scripts, Makefile, README quickstart). Note ports, env vars, seed data, and auth.
- **Drive.** How can an agent interact with it programmatically? Existing harnesses first: Playwright or Cypress specs, expect scripts, PTY helpers, curl-able endpoints, a debug port. Only then pick a generic recipe. Use browser automation or CDP for web and Electron, a tmux or PTY harness for a CLI or TUI, and plain HTTP for services.
- **Observe.** What evidence can be captured? Screenshots, terminal transcripts, response bodies, logs, exit codes, database state.
- **Isolate.** Can two instances run side by side (ports, data dirs, profiles)? If not, say so in the generated skill. Refusing to double-drive a shared instance beats corrupting the user's session.

If the checkout does not build or start as-is, fix that first, or report it precisely, before you generate anything. A skill written against a broken base teaches wrong steps. When an irrelevant missing asset blocks startup (a static dir the API never serves, a sample config), the generated skill may create it, clearly marked as verification scaffolding, and remove it in cleanup.

## 2. Generate the skill

Write `SKILL.md` in the verify directory with YAML frontmatter. It needs `name: verify` and a `description` that names the app, the surface, and when to reach for it. Without frontmatter the skill never registers. With `disable-model-invocation` the model cannot call it. Then write these sections, each grounded in what the interview actually found, with no placeholders left.

- **Launch.** The exact command that starts the app for verification, and how to tell it is ready (a log line, a prompt). Launch must reach a usable state from an empty data dir, including any migrations and seed data. Ready means usable, not just that a process answers. A database health check can pass while its init scripts are still running. Include teardown. A short-lived CLI or TUI has no server to keep alive. There, launch means build the binary (or install deps) once, then start each drive in its own isolated PTY or tmux session.
- **Doctor.** One read-only check that answers "is this instance worth driving?" Process up, the right version or build, the port owned by us, auth valid. An agent runs this first whenever anything looks off.
- **Drive.** The harness recipe with real selectors and commands from this repo, not examples. Prefer stable handles (ARIA labels, data attributes, prompt strings, route paths) over coordinates and tab order.
- **Evidence.** What to capture for a proof and where it goes. State the proof standards.
  - Exercise the real user path, not internal setters or test-only endpoints.
  - Capture the action and the resulting state, not just the final screen.
  - Verify side effects (files written, rows inserted, messages sent) alongside what is visible.
  - Use mocks only where a production boundary already isolates the external system.
  - When the safe path is a dry run or test mode, observe what it actually skips (files, network, git refs) rather than trusting its name. Some dry runs still touch the network or open a browser.
- **Cleanup.** How to tear down the instances the run created. Never kill by process name. Kill what you started. Cleanup removes instances and scratch state, never the evidence. Proof artifacts survive the teardown, in a location the skill names.
- **Helpers.** Any script the skill ships is executable, and the skill body shows its invocation. A helper the reader has to reverse-engineer is not a helper.

## 3. Seed the feature map

Create `features/README.md` in the verify directory, plus one file per user-facing feature you can identify. Aim for the top three to five to start, drawn from routes, commands, menus, or docs. Follow the shape in [references/feature-map-example/](references/feature-map-example/README.md), with a README index and one file per feature.

Each feature file answers, from the user's point of view, what the feature is, how to reach it, how to drive it with the harness, and what observable end state proves it works. Its four H2s are `Sub-features`, `How to get to it (user POV)`, `Driving it with <harness>`, and `Gotchas`.

If the seed data lacks a precondition a journey needs, the journey reports a failure and the reason goes in that feature's `Gotchas`. Never weaken the journey to make it pass. The map is the repo's maintained verification source. A proof that drives one convenient entry point is incomplete when the map lists others.

## 4. Prove the generated skill before handing it over

Run its own instructions end to end once. Launch, doctor, drive one mapped feature (one is enough, since the map exists so later runs can cover the rest), capture evidence, and clean up. After cleanup, confirm the evidence still exists at the named location. A cleanup that eats the proof fails this step.

Fix what fails. Run the generated cleanup after every failed iteration too, so broken attempts do not strand processes and ports. A generated skill that was never executed is a draft, not a deliverable.

If you proved it in a stand-in for the real target (a container in place of a fresh VM, a local stack in place of a remote one), list every setup step the stand-in did that the target will not. Those steps stay unverified until a run on the real target covers them.

## 5. Offer the upkeep loop

Point the user at `checkup` to keep the map honest as the app changes. Suggest a cadence only if they ask.
