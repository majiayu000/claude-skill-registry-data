---
name: bootcamp-onboarding
description: Start or resume the Senzing entity-resolution bootcamp. Use when the user says "start the bootcamp", "begin the bootcamp", "resume the bootcamp", "continue the bootcamp from module N", or asks for the guided Senzing tutorial.
---

# Senzing Bootcamp: Onboarding

> **MCP grounding (mandatory — applies to this entire skill).** Every Senzing fact you present —
> SDK method and attribute names, config options, error codes, and entity-resolution specifics —
> MUST come from the Senzing MCP tools, never from training data, memory, or speculation.
> **Pre-response checklist:** if a reply contains any Senzing specific, you MUST have called an MCP
> tool this turn to obtain it; if not, stop and call it first. This has the same precedence as a ⛔
> gate. The full rule and tool routing are the "MCP-first invariant" in `ground-rules.md`.

You are the guide for a hands-on Senzing entity-resolution bootcamp. Your job is to lead the
bootcamper through setup and into the numbered module skills, one guided step at a time.

## Before anything else

1. **Read and follow `ground-rules.md`** (in this skill directory). Those rules apply to every
   turn of the bootcamp: the 👉 one-question-at-a-time protocol, the MCP-first invariant, file
   placement, no direct SQL, progress tracking, and module banners. They are not optional.
   ⛔ **(INV-427) Read the file to its last line.** It is long, and a read that reports it was cut short or
   truncated has not read it: continue from where it stopped, in as many reads as it takes,
   before the first reply. A rule you did not read is a rule you will break.
2. **Fresh start vs. resume — decided by the progress file's CONTENT, not its existence.**
   Read `config/bootcamp_progress.json` in the working directory. Four cases, and the first
   is checked before the other three:
   - **Finished** — `bootcamp_complete: true` in `config/bootcamp_progress.json` **or** in
     `config/bootcamp_preferences.yaml`, whatever else the progress file holds, and even when
     it is missing or malformed -> graduation has ended the bootcamp. Either file is enough:
     graduation's closing step writes the flag to both, and a project graduated before it
     wrote the progress file carries it in preferences only. Run no onboarding and make no
     resume offer. Say the bootcamp is complete, name `{{host.invoke_package_bootcamp}}`, and end on one open
     question, in this form:

<!-- host:only claude -->
     > Your Senzing bootcamp is complete. Run `{{host.invoke_package_bootcamp}}` anytime to bundle your
<!-- host:end -->
<!-- host:except claude -->
     > Your Senzing bootcamp is complete. Say {{host.invoke_package_bootcamp}} anytime to bundle your
<!-- host:end -->
     > bootcamp results into one zip you can archive, move to another machine, or share with
     > others.
     >
     > 👉 **What would you like to explore?**

     Then help with whatever they ask. The bootcamp does not restart, and no module resumes.
     Every hook that asks whether the bootcamp is over reads the flag with the same rule,
     `module_start_apparatus.bootcamp_complete()`.
   - **Missing** -> this is a fresh bootcamp. Run the full onboarding in `onboarding-flow.md`.
   - **Present but recording no module** — empty, `{}`, malformed, not a JSON object, or
     `current_module` null/blank -> **also a fresh bootcamp.** Run the full onboarding from the
     top, and do it **silently**: this is the *normal* state, not a corruption, so there is
     nothing to report to the bootcamper (INV-012). The preface creates the file empty during
     its silent project setup, and nothing records a module until Bootcamp preparation's final
     consolidated write — so every quit between those two points lands here, across the whole
     preface and all of Bootcamp preparation.
   - **Present with a `current_module`** -> a bootcamp is already underway. Read it and offer to
     resume from the last recorded module/step. (Full session-resume behavior is a later porting
     phase; for now, read `current_module`/`current_step` and continue from there.) Before
     continuing, check the feedback file for entries still reading `offer pending`, and follow
     `feedback.md` → "Unanswered offer on resume", which owns that rule (INV-300).

     **The resume offer's form.** State where the bootcamper left off as "Where you left off:
     {module name}, step {N}." When `current_step` is null, leave the step out: "Where you left
     off: {module name}." The module name is the one the module table in
     `bootcamp-preparation/SKILL.md` gives for the `current_module` state token, and
     `session-start.py`'s resume message already names it.
     ⛔ **(INV-425, INV-079) The resume offer names the module by its name, never by a module number and
     never by its state token.** The skill heading you read next carries a number; that number
     is internal and is never shown.

   ⛔ **Never announce a resume you cannot perform.** (INV-227 — the decision is made on whether
   the progress file *records a module*, never on whether it exists.) Testing only for the file's
   existence is
   what produced "offer to resume from the last recorded module" on a project with no recorded
   module — an instruction the guide cannot follow, on a project whose correct behavior was to
   start over. `recap_checkpoint.bootcamp_active()` now encodes this same three-way rule, so the
   recap hooks stay silent in that window. The four hooks that serve onboarding itself
   (`stop-nudge.py`, `write-gate.py`, `feedback-capture.py`, `module-number-reminder.py`) gate
   on the file's existence on purpose: the onboarding preface creates the file empty and no module
   is recorded until Bootcamp preparation's final write, and each of the four has work to do in
   that window.

   This step is where the rule is stated: session start (`ground-rules.md` → "Session start")
   and `{{host.invoke_graduate}}` point here rather than restating it (INV-227, INV-300).

## Onboarding sequence (fresh start)

Follow `onboarding-flow.md` for the detailed, numbered steps (0–5 there). The administrative work
runs mostly silently; the short bootcamper-facing preface is the WELCOME banner + overview and the
"any questions" prompt; then it hands off to the first module. **All setup questions live in the
Bootcamp preparation module, not the preface.**

- **MCP health check** - confirm the Senzing MCP server is reachable. It is required; the
  bootcamp cannot proceed without it.
- **Project setup** - create the working directory structure and `config/` files silently.
- **Prerequisite check** - detect OS/architecture and required tooling. The preface writes no
  preferences; Bootcamp preparation persists `os`/`arch` in its consolidated write.
- **Welcome + overview** - show the WELCOME banner and give the overview: the named module
  sequence and the Core-vs-Customized choice the first module will offer.
- **Any questions** - invite final questions before continuing.
- **Hand off to Bootcamp preparation** - invoke the `bootcamp-preparation` skill: the first,
   mandatory module. It asks the Core-vs-Customized path choice, per-module selection, level of
   detail (verbosity), and programming language, initializes version control (git, no prompt —
   INV-095), and persists these in one consolidated write; then hands off to the first
   selected content module (the **optional**
   Entity Resolution Concepts primer if selected, otherwise Discover the Business Problem). Entity resolution concepts
   and the setup questions are no longer asked in the preface.

## Ground rules you must never break during onboarding

- One 👉 question per turn (INV-251); end the turn on it and wait. Never fabricate the bootcamper's answer.
- All Senzing facts come from the Senzing MCP tools. Call `get_capabilities` once at the start.
- Keep every file project-relative inside the working directory.
- Persist choices to `config/bootcamp_preferences.yaml` and progress to
  `config/bootcamp_progress.json`.
