---
name: rseng-ux-accessibility
description: >-
  Covers user experience and accessibility for research software: UX
  disciplines, accessibility practice, Design Thinking, scoping a Minimum
  Viable Product versus a Minimum Loveable Product, Nielsen's usability
  heuristics, and prototyping with tools like Figma and Miro. Also covers WCAG
  conformance for web-facing tools, accessibility testing, CLI usability
  guidelines and inclusive defaults. Use PROACTIVELY when creating or
  reshaping a user-facing interface (CLI, GUI, web), and when the user designs
  a research tool's interface (web, GUI or CLI), asks how to make research
  software usable or accessible, plans user testing or prototyping, or
  mentions usability heuristics, WCAG, UX or a11y in a research software
  context.
license: CC-BY-4.0
metadata:
  version: 0.2.0
---

# UX and accessibility for research software

Research software succeeds when researchers can actually use it; UX is
not cosmetic polish but part of software quality. This skill treats
usability as an engineering practice, not cosmetic polish.

## Practice

- Know the disciplines: UX research (understanding users and tasks),
  interaction design, visual design and accessibility are different
  jobs - be explicit about which one a request needs.
- Start from users and tasks, not features: apply Design Thinking -
  empathize with the target researchers, define the task, ideate,
  prototype cheaply (Figma or Miro before code), test with real users.
- Scope deliberately: an MVP proves the workflow works; a Minimum
  Loveable Product adds the qualities that make researchers adopt it.
  Pick which one the project stage needs and say so.
- Evaluate against Nielsen's usability heuristics (visibility of
  status, match with the users' world, error prevention and recovery,
  consistency, minimalism); they apply to CLIs and notebooks as much as
  GUIs - clear --help, sane defaults and good error messages are UX.
- Accessibility is a requirement, not an extra: color-contrast, keyboard
  navigation and screen-reader support for web tools; readable output
  and terminal-friendly formats for CLIs.
- Usability findings become issues like any other defect; retest after
  fixing (pair with rseng-testing for automated regression of CLI/API
  ergonomics where possible).

## Accessibility, concretely

- Web-facing research tools target WCAG (the W3C accessibility
  standard; level AA is the common bar and often a legal one for
  publicly funded services): text alternatives for non-text content,
  sufficient contrast, full keyboard operability, labeled form
  controls, and structure a screen reader can navigate (headings,
  landmarks, table headers).
- Test it, do not assume it: automated checkers (axe-class tools in
  CI) catch the mechanical failures; a keyboard-only walk-through and
  a screen-reader pass catch the rest. Accessibility findings are
  defects with severities, tracked like any other
  (rseng-project-tracking).
- Scientific outputs have accessibility too: colorblind-safe and
  perceptually honest palettes (rseng-scientific-visualization), alt
  text that states what the figure SHOWS ("temperature rises sharply
  after 1980"), not what it is ("a line chart"), and data tables as
  alternatives to figure-only results (rseng-science-communication).
- Documentation accessibility: plain language, defined jargon,
  meaningful link text, heading hierarchy - the same qualities that
  serve newcomers and non-native speakers (rseng-documentation,
  rseng-trainer's calibration).

## CLI usability, concretely

Most research tools are CLIs, and CLI UX is a codified craft (the
Command Line Interface Guidelines distill it):

- --help that teaches: usage, an actual example, and the most-used
  flags first; man-page or docs parity (rseng-documentation).
- Errors that help recovery: say what failed, on which input, and
  what to try - "config key 'stations' missing (stations.json)" beats
  a traceback (rseng-defensive-coding's fail-loud, made humane).
- Sane defaults, explicit overrides; standard conventions respected
  (exit codes for CI - rseng-ci-cd; stdout for data, stderr for
  messages so pipes work; --version; no color when not a TTY).
- Progress for long operations (rseng-hpc-computing jobs excepted -
  log lines there), and quiet/verbose flags because both scripting
  and debugging are real uses.
- Test the ergonomics: golden-file tests on --help and error
  messages keep promised UX from rotting (rseng-testing).

## Working with this skill

The generated references.md beside this file lists the source material
and pointers:

- references.md - verified Learn more pointers


Learn more (verified):
  - https://www.w3.org/WAI/standards-guidelines/wcag/ - WCAG
  - https://www.a11yproject.com - the A11y Project
  - https://clig.dev - Command Line Interface Guidelines

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-defensive-coding - humane fail-loud error messages
- rseng-documentation - docs accessibility and help parity
- rseng-science-communication - accessible slides and figures
- rseng-scientific-visualization - colorblind-safe honest palettes
- rseng-testing - golden-file tests on CLI ergonomics
- rseng-user-support - error-message questions reveal UX gaps

<!-- related-skills:end -->
