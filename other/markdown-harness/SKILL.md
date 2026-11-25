---
name: markdown-harness
description: Govern a folder of markdown with markdown-harness — set it up in a repository, author or change a
  markdown-harness.config.yaml, put `mh check` in the gate, or wire the Claude Code hook that reads a freshness
  sentence back to an agent. Use when installing or setting up markdown-harness, deciding what a document must declare
  about its provenance or freshness, adding or changing a rule, converting a document template into a rule over its
  headings, applying or updating a preset such as Keep a Changelog or Archgate ADRs, migrating an existing setup off the
  `--check` flag forms or an old config grammar, working out why a rule governs nothing, or demonstrating what the tool
  does.
compatibility: Requires @hancrafted/markdown-harness >= 0.0.2, as `mh` or `npx mh`. Confirm with `mh --help`.
---

**Being handed this skill is a request to act.** Run the probes, say where the repository stands, and
offer the numbered options for that state — all three in your first reply. A slash command or a file
read putting this in front of you _is_ the request; act on it directly.

Keep the offer to the work in step 3's table. Other governance systems in the repository are a
separate conversation, and listing them alongside turns an answer into a menu.

## 1. Probe

Five reads, one pass, and they settle the corpus between them. Each reads the artifact itself rather
than a record of it, so none can go stale.

| Probe                                            | Absent means   |
| ------------------------------------------------ | -------------- |
| `markdown-harness.config.yaml` at the repo root  | not configured |
| `docs/markdown-harness/`                         | init never ran |
| `@hancrafted/markdown-harness` in `package.json` | not installed  |
| the gate script contains `mh check`              | not gated      |
| a `PostToolUse` entry in `.claude/settings.json` | not hooked     |

A sixth read works the other way round: if a **retired form** is present, the setup needs migrating.
A retired form is `mh --check`, `--query`, `--audit` or `--assess` in a script or workflow, or a
`path:`, `fileName:` or `vocabulary:` key in the config.

## 2. Say where the repository stands

One line, from what the probes found — not a report of five probes. "You have a config and the gate
runs `mh check`, but nothing is hooked" is the whole of step 2.

A one-line welcome explaining what the tool is belongs **only** in the never-set-up state. Anywhere
else the repository has already answered that question and the user is mid-task.

## 3. Offer the numbered options for that state

| Config  | `docs/markdown-harness/` | State              | Offer                                                                                                                                                |
| ------- | ------------------------ | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| absent  | absent                   | not set up         | 1. set it up · 2. see it work on throwaway files first                                                                                               |
| absent  | present                  | set up, ungoverned | 1. author the first config · 2. apply a preset · 3. convert a document template · 4. see the demo · 5. finish setup                                  |
| present | either                   | governed           | 1. add or change a rule · 2. apply or update a preset · 3. convert a document template · 4. why a rule governs nothing · 5. gate · 6. hook · 7. demo |

**When a retired form is present, option 1 is `migrate to the current commands and config`**, ahead
of the state's own list. Until the migration is done the gate exits 2 on every run, and every other
option works on a config the CLI refuses.

**Options are numbered, never bulleted.** That is a house rule for this skill and it holds in
`init.md`, `demo.md`, `authoring-a-config.md`, `authoring-body-structure.md` and `applying-a-preset.md` too: a user answering a menu should be able to type
one digit.

## 4. Read the file for the option they picked

| To do this                                                   | Read this                                                                  |
| ------------------------------------------------------------ | -------------------------------------------------------------------------- |
| Set it up — install, gate and hook in one pass               | [`assets/init.md`](assets/init.md)                                         |
| See it work on throwaway files before committing to rules    | [`assets/demo.md`](assets/demo.md)                                         |
| Author the first config, or add, change or debug one rule    | [`assets/authoring-a-config.md`](assets/authoring-a-config.md)             |
| Apply or update a preset: Keep a Changelog, Archgate ADRs    | [`assets/applying-a-preset.md`](assets/applying-a-preset.md)               |
| Convert a document template into a rule over its headings    | [`assets/authoring-body-structure.md`](assets/authoring-body-structure.md) |
| Migrate an existing setup to the current commands and config | [`assets/migrating.md`](assets/migrating.md)                               |
| Put `mh check` in the gate on its own                        | [`assets/wiring-the-gate.md`](assets/wiring-the-gate.md)                   |
| Wire the freshness hook on its own, on Claude Code           | [`assets/wiring-the-hook.md`](assets/wiring-the-hook.md)                   |

`init.md` covers the last two through a script; reach for them directly when init has already run, or
when the repository needs one without the other. Read the file you picked before acting — each
carries its own steps and its own completion criterion.

## What holds throughout

One config file declares what each path must carry. Rules are an ordered list, the first match is the
complete set of constraints, and a file no rule names is invisible to the tool.

**Governance is opt-in** — a rule that matches nothing governs nothing, and the tool stays silent.
**The tool reports; the user decides.** Propose frontmatter edits, and write what they approve.

**Treat a script's exit 0 as evidence about the script alone.** Where a step claims the freshness
hook works, the evidence is a row in `docs/markdown-harness/activity.csv`. `demo.md` step 4 is the
worked example.

`mh --help` lists the commands and the exit codes. Ask the tool rather than trusting a restatement.
