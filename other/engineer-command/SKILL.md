---
name: engineer-command
description: >-
  Guide for authoring an IDE slash command - one Markdown file the user runs as
  /name in Cursor, Claude Code or OpenCode. Use when users want to create or
  update such a command. Not for model-discovered skills.
license: 'Based on https://github.com/anthropics/skills'
---

# Command Creator

This skill guides writing a slash command: ONE Markdown file in an IDE's commands directory that the user runs by typing `/<name>`. The file is the prompt the agent receives when the command runs.

## Question Format (FR-UNIVERSAL.QA-FORMAT)

When asking the user a choice (IDE, scope, examples to cover):

- **Numbered** — each question is a numbered list item (`1.`, `2.`, …), not a heading, a bold-only line, or a paragraph.
- **Self-contained** — the question is answerable from itself and its options alone. Name what is being decided and what the answer changes, inside the question. "Which of the above?", a bare "Your choice?", and "Which variant do you prefer?" with nothing restated are defects: they send the reader back up the transcript to reconstruct the question.
- **Each option stands on its own** — a reader often jumps straight to the options, so an option's title and the lines under it must be enough to choose without the text above the question or the earlier turns. The title is a short name after the option's letter or number, and the reader answers with that letter or number; the `**Essence:**` line under it says what would be done, to what, and what the reader gets. A short reply option with no analysis of its own (Apply / Skip / Edit) has no Essence line, and its title says it alone. **Inside an option, name things in words, never by a report's ids.** Every line of the option — title, Essence, Pros, Cons, Risks, Best for — is read without the report, and ids slip in most often in Pros, Cons and Risks. Write what the thing is instead of its label: "the checkout errand on the shop site", not `E4`; "the search box ignoring the first keystroke", not `N3`. A label in parentheses after a general phrase — "the two most expensive errands (E4, E3)" — is still a bare label: name each item. A number taken from a report keeps what it measures in the same sentence: a percentage names the whole it is a share of ("page text takes about 40% of the cost", not "a 40% share"), and a sum says whose cost it is. **Any phrase that stands for a group is a pointer**: a count ("the four slow pages", "the same three errands"), a category ("the anomalies", "the issues found"), a rank or superlative ("the costliest runs"), "these", "as above", "the current round" — and so is a partial list, a count followed by a few examples or a "such as". Replace it with every member of the group, named in words, in that option — even when the list is long, even when the report above already lists them; if the whole set does not fit, drop the group from the option. Test: with the report deleted, could the reader name every member from this option alone? A word coined in this session gets a short explanation in the option. An explanation elsewhere in the reply does not count — not in the report above the question, not in another option. Before sending, read each option alone, line by line, and list every label (letters plus digits such as `E4` or `N3`), number, group phrase (a count, a category, a superlative, "the same", "these") and coined term in it; replace each with words or remove it.
- **No catch-all option** — never add an option whose only content is an invitation to answer freely ("Other", "Something else", "Your own variant", "Tell me what you need"). The user can always type a free-form reply instead of a letter or number, and an IDE's question tool (`AskUserQuestion` and the like) already offers a free-text answer of its own, so such an option adds a line and no choice. An option that names a concrete alternative is a real option, even when its title starts with "Other".
- **`agent's choice`** — on a multi-select where the user delegates with `agent's choice` (or its language equivalent), pick the subset yourself, justify the pick in one line, and proceed without re-asking for confirmation.
- When the choices are mutually exclusive alternatives with their own analysis, that analysis is nested under the option inside the question — never repeated as a separate block before it. It opens with the `**Essence:**` line, then `**Pros:**`, `**Cons:**`, `**Risks:**` and `**Best for:**`, each on its own labelled line.

## What a Command Is, and What It Is Not

- A command is a single file, `<commands-dir>/<name>.md`. The user starts it by name; the model does not pick it up on its own.
- It is NOT a `SKILL.md` directory. When the user wants a capability the model loads by itself from its description, or one that needs bundled scripts, references or assets, that is a skill: hand over to `engineer-skill` and say why.
- One command, one job. Keep supporting detail inside the file; if it outgrows one file, it is a skill.

## Command Paths and Formats by IDE

| IDE | Project command | User command | Format |
|-----|-----------------|--------------|--------|
| **Cursor** | `.cursor/commands/<name>.md` | `~/.cursor/commands/<name>.md` | Plain Markdown, no frontmatter. The text typed after `/<name>` is passed along with the file. |
| **Claude Code** | `.claude/commands/<name>.md` (or `.claude/commands/<namespace>/<name>.md`) | `~/.claude/commands/<name>.md` | YAML frontmatter (`description`, `argument-hint`, `allowed-tools`, `model`, `disable-model-invocation`) + Markdown body. `$ARGUMENTS`, `$1`…`$N` |
| **OpenCode** | `.opencode/commands/<name>.md` | `~/.config/opencode/commands/<name>.md` | YAML frontmatter (`description`, `agent`, `model`, `subtask`) + Markdown body. `$ARGUMENTS`, `$1`…`$N`, `@filepath`, bang-backtick shell output |

Claude Code also runs a bang-backtick pair (!`shell command`) that is preceded by whitespace while it expands a command, and a code span does not escape it. Use it only on purpose and with `allowed-tools`; otherwise keep the bang glued to the preceding character.

## Choosing the IDE and the Scope

1. If the user named the IDE, use it.
2. Otherwise look for markers: `.cursor/` → Cursor, `.opencode/` or `opencode.json` → OpenCode, `.claude/commands/` or `CLAUDE.md` → Claude Code. A `.claude/skills/` directory alone is NOT evidence of Claude Code: Cursor and OpenCode projects keep their skills there too.
3. If the markers disagree with what the user said, or point nowhere, ask which IDE the command is for. Ask whether it is a project command (shared through the repo) or a personal one, unless the user already said.
4. A command meant for several IDEs is one file per IDE, each in that IDE's format. Write the shared body once and adapt only the header and the argument syntax.

## Creation Process

1. Collect concrete invocations.
2. Plan the arguments and the body.
3. Write the file in the IDE's format.
4. Validate it.
5. Iterate on real use.

### Step 1: Collect Concrete Invocations

Skip this step only when real invocations are already on record — the exact words someone would type after `/<name>`. A feature list is not that: "starting/stopping services, viewing logs, rebuilding containers, checking health" is a spec, while `/docker-compose rebuild api`, "show me the logs for the db service" and "is everything up?" are invocations. Given a spec, draft the invocations yourself and have the user confirm, add or drop them before writing anything.

Invocations decide what the command must accept and what it must do with each input. Ask a few questions at a time; start with the most important ones.

### Step 2: Plan the Arguments and the Body

For each confirmed invocation, decide:

- which arguments it carries (an action, a target, a count, free text) and how the body reads them — `$ARGUMENTS` / `$1` in Claude Code and OpenCode, the trailing text in Cursor;
- what the agent must do, step by step, and what it must refuse or confirm first (destructive operations, ambiguous targets);
- what the agent reports back.

If an invocation needs a reusable script, reference material or a template, stop and propose a skill instead (see "What a Command Is").

### Step 3: Write the File

Write `<commands-dir>/<name>.md`, where `<name>` is hyphen-case and is what the user types after `/`.

Claude Code:

```markdown
---
description: <what the command does, as shown in the / menu>
argument-hint: '[action] [service]'
---
<Imperative instructions. Read the request from $ARGUMENTS.>
```

OpenCode:

```markdown
---
description: <what the command does>
---
<Imperative instructions. Read the request from $ARGUMENTS.>
```

Cursor:

```markdown
# <Command title>

<Imperative instructions. The request is the text typed after the command name.>
```

Writing rules:

- Use the imperative form. The body is a prompt for another agent, not documentation for a person.
- Quote YAML values that start with `[`, `{`, `*` or contain `: ` — an unquoted `argument-hint: [action]` parses as a list.
- Include only what the agent would not know without being told: project paths, house rules, the exact order of steps, the safety limits. No README, installation guide or changelog sections.
- For multi-step procedures and output formats, see `references/workflows.md` and `references/output-patterns.md`.

### Step 4: Validate the File

```bash
deno run -A scripts/validate_command.ts <path/to/name.md> --ide <claude|cursor|opencode>
```

The script checks the file name, the frontmatter rules of the IDE (none for Cursor, a `description` and known keys for Claude Code and OpenCode), a non-empty body, and unintended Claude Code shell expansion. Fix every error it reports and run it again. Then tell the user how to run the command (`/<name> …`) and that the IDE may need a reload to list it.

### Step 5: Iterate

After the user runs the command on real tasks, note where the agent went wrong or asked something the file should have answered, and change the body.
