---
description: Write code_tour.md, a leveled checklist to understand the code, docs, and tests of a dir
model: sonnet
---

# Goal

- Given a dir, write `code_tour.md`: a markdown checklist that guides a human
  through the code, docs, and tests of that dir
- Split it into exactly three levels:
  - **Level 1**: "Understand in 15 mins"
  - **Level 2**: "Understand in 1 hour"
  - **Level 3**: "Understand in full"
  - Do not add or rename a level. Each level adds items to the levels before it
  - A reader can stop after any level and still know the dir at that depth
- Give the time of every item, so the reader can plan the work
- Include examples and tests to run, so the reader sees how the code behaves
- Include the end-to-end demo in Level 3, from `code_demo.md` of the dir
  - The skill `.claude/skills/review.create_demo/SKILL.md` writes this file
  - The tour does not explain the output: it points to the file
- Take files, kinds, reading times, and code order from the `# Review roadmap`
  section of the dir `README.md`
  - The skill `.claude/skills/readme_dir.create/SKILL.md` writes this section
  - The checklist does not repeat the map or the file table

# Conventions

- Follow the template `.claude/templates/review_create_code_tour.template.md`
  - It has no `# Map of the Dir`: the map is in the README
- Write the text following `.claude/skills/text.rules.md` and
  `.claude/skills/markdown.rules.md`
  - Use `- [ ]` for every checkbox, never a bare `[ ]`
- In Level 3 items, refer to `.claude/skills/coding.rules.md` (Python) and
  `.claude/skills/testing.rules.md` (tests)
- Take how to run the tests from the `## Testing` subsection of the roadmap

# Workflow

## Get the Input

- Take the dir from the arguments, or the current dir if none is given
  - If the dir does not exist, report the error and stop
- Compute the dir path from the repo root:
  ```bash
  > git rev-parse --show-toplevel
  ```
- Write the output as `code_tour.md` in the dir. The name is fixed: it does not
  follow `## Generated File Naming` of `.claude/skills/skill.rules.md`
  - If the file exists, read it, then overwrite it. Keep the ticked items that
    are still in the new checklist
- Take the dir `README.md`
  - If it is missing or has no `# Review roadmap` section, report the error and
    stop. Tell the user to run `.claude/skills/readme_dir.create/SKILL.md` on the
    dir first
- Take the dir `code_demo.md`
  - If it is missing, report the error and stop. Tell the user to run
    `.claude/skills/review.create_demo/SKILL.md` on the dir first

## Read the Roadmap

- From the `# Review roadmap` section of `<DIR>/README.md`, take:
  - The entry points, in run order
  - The layers, bottom first, and the import-graph cycles
  - The test command, for the dev env and for Docker
  - The reading speeds, in lines per min
  - The "Skipped" line and the other notes on the table
- From the table, take each file's kind, lines, `Mins`, `Changed` flag, doc, and
  test
  - The `code` rows are in bottom-up import order
  - A raw export has no time, so give it no read item
  - A Level 3 item may list the header of a raw export
- Check that the roadmap is current:
  ```bash
  > git ls-files --cached --others --exclude-standard <DIR>
  > wc -l <FILES>
  ```
  - If a file is missing from the table, or a `Lines` value differs, report it and
    stop. Tell the user to run `.claude/skills/readme_dir.create/SKILL.md` on the
    dir again
- Mark files with uncommitted changes, since the `Changed` flag goes stale first:
  ```bash
  > git status --short <DIR>
  ```

## Set the Reading Time

- Use the skim speed for `Skim` items, and the speed of the file's kind for
  `Read` items
- Compute an item's minutes as `ceil(lines / speed)`, with 1 as the minimum
- Estimate the other items by hand, in whole mins:
  - Run `--help` or a dry run: 2
  - Run `pytest` on one test file: 1
  - Run `pytest` on the whole dir: 2, or the measured time rounded up
  - Run a command that needs the internet, an LLM, or a browser: 5 to 30, and
    say what it needs
  - Check a claim of the docs against the code: 5
  - Run the coverage: 5
  - Check a file against a rules file: 2 per file
- Show each item's time at its start: `(<N> mins)`, or `(1 min)` for one min
- Sum each level's item times, and print the sum in the level's `Time` line
  - For Level 2 and Level 3, also print the sum up to that level
  - Use these fixed titles, and never compute a title from the sums:
    - `# Level 1: Understand in 15 Mins`
    - `# Level 2: Understand in 1 Hour`
    - `# Level 3: Understand in Full`
  - The `Time` line holds the real sum, so the reader sees any gap with the title

## Understand Enough to Write Items

- For each file, read the docstring or first lines, and its paired doc
- Write each file's purpose in one short line
  - Take the purpose of entry points and layers from the roadmap
  - If the purpose is unclear, write only the file name and `purpose unknown`.
    Do not guess
- Find the docs with a diagram, e.g., mermaid, PlantUML, C4, Graphviz, or TikZ:
  ```bash
  > grep -rlE '```(mermaid|plantuml|dot|graphviz|tikz)|C4Context|C4Container|C4Component|@startuml' <DIR> --include='*.md'
  ```
  - Note each file's diagram kind, e.g., `C4 diagram (PlantUML)`
- Find the examples to run
  - Take example commands from the dir README and the scripts
  - Take flags from `--help`, e.g., `--dry_run` and `-v DEBUG`
  - Run each command that needs no internet, LLM, or browser, and check it works
  - Do not invent a command or a flag

## Write the Levels

- Write all three levels of the template
  - **Level 1**: what the dir does and how to run it
  - **Level 2**: components and data flow
  - **Level 3**: every file, its test, the checks, and the end-to-end demo
- Fill each level with the groups `Docs`, `Code`, `Tests`, and `Examples`
  - In Level 3, use the group `Code and Tests, Bottom Layer First` instead of
    `Code` and `Tests`, and add the groups `Checks` and `End-to-End Demo`
  - Drop a group that has no item in a level. Do not write filler
- Read or skim whole files only
  - Start each reading item with `Read all of` or `Skim all of`
  - Do not limit an item to a section, a function, or a line range
  - Do not use `Look at`, section names, or function names as an item's scope
  - The only exception is the header of a raw export
- Use `Skim all of` to map a file, and `Read all of` to understand it
  - A file may appear in two levels only if the second item goes deeper, from
    `Skim all of` to `Read all of`
  - Level 3 reads every file in full, once, with `Read all of`. Do not skim a
    file and then read it in Level 3
- Level 1 items
  - Skim the dir README, which holds the `# Review roadmap`, and its docs' READMEs
  - Skim the small example input
  - Run `--help` of the entry points
  - Run the dry run of the runner and of the first stage
  - List the test files, matching each with its code using the roadmap table
  - Do not open a code file or a test file
  - Keep the level under 20 mins
- Level 2 items
  - Read the architecture doc, and skim the flow doc
  - Skim the types file and each stage
  - Run all the tests with `pytest`, and in Docker
  - Run the end-to-end test with the live log
  - Read the end-to-end test, and skim the test helpers
  - Keep the level under 90 mins
- Level 3 items
  - In `Docs`, read the flow doc, the PRD, the decisions, the progress doc, and
    the plan
  - In `Docs`, read each design doc and script README right before the code it
    describes, in code order
  - In `Docs`, read the logs, todos, background notes, and the `data` files the
    code uses, e.g., config, prompt, and example input
  - In `Code and Tests`, for each `code` file in roadmap order (bottom up):
    - `Read all of` the file
    - `Read all of` its test file, if any
    - `Run pytest` on the test file, and match each test name with the code
  - If the test helpers were not read in Level 2, or only skimmed, `Read all of`
    them before the first test that uses them
  - In `Checks`, add:
    - Three items that check a claim of the docs against the code
    - An item to mark each doc line that disagrees with the code with
      `// TODO(gp): Check ...`
    - The `git diff` of changed files when `git status` shows uncommitted
      changes. Skip it when the dir is clean
    - The check against the coding and testing rules
    - The coverage run
  - In `Examples`:
    - Run the dry run again with `-v DEBUG`
    - Run the first stage on the example input, and the dry run of the next
      stages on its output. Say what it needs, e.g., `needs internet`
    - Trace one input through all stages with the end-to-end test
  - In `End-to-End Demo`, add these items, in this order:
    - `Read all of` the file `code_demo.md`
    - Run the demo with the command of `code_demo.md`. Say what it needs and
      costs, copying the command, needs, and cost from the file
    - List the output dir, and match each file with the section
      `# What Is Generated` of `code_demo.md`
    - Read each summary file, and check that each failed item is in the issues file
    - Compare two report values with the value in the file of one item
    - Run the same command again, and check that finished work is skipped

## Write the Items

- Start each item with its time, then the checkbox: `- [ ] (<N> mins) ...`
- Keep each item to at most 4 lines of at most 85 characters. Indent continuation
  lines by 6 spaces
  - Split an item that needs more lines into two items
  - A line that holds only one path may pass 85 characters
- Start each action with a verb: `Read all of`, `Skim all of`, `Run`, `List`,
  `Check`
- Name each file in backticks, with its path from the repo root
- For each doc with a diagram, add a render step to every item that reads or
  skims it, so the reader sees the diagram, not its source
  - Keep `Read all of` or `Skim all of` first, and add the line
    `It has a <KIND> diagram: render it first:`
  - Under it, add this command in a fenced block, with the repo-root path:
    ```bash
    > open_md.py -i <DOC_PATH>
    ```
  - Add no time for this step
  - Do not use `open_md.py -i` for a doc with no diagram
- For a reading item, add the line count, `modified` if the file has uncommitted
  changes, and the purpose
- For a `Run` item, put the command in a fenced block under the item
  - Use `pytest <PATH>` or `invoke docker_cmd --cmd "pytest <PATH>"` for tests
  - Do not use `uv` to run the tests
- Make each item checkable: the reader must know when it is done
  - **Bad** (no time, no path from the repo root, part of a file, no purpose)
    ```markdown
    - [ ] Read the functions `_parse()` and `_main()` of epq_report.py
    ```
  - **Good**
    ```markdown
    - [ ] (27 mins) Read all of `research/Estimate_academic_paper_quality/epq_report.py`
          (535 lines): writers and readers of the output files
    ```
  - **Bad** (a vague check)
    ```markdown
    - [ ] (5 mins) Understand the output dir
    ```
  - **Good** (the reader can fail it)
    ```markdown
    - [ ] (5 mins) Check claim 1: each file in the tree of "Output Dir" has a
          `get_*_path` function in `research/Estimate_academic_paper_quality/epq_paths.py`
    ```

## Report

- Print the checklist path, the item count, and the time of each level
- Print the skipped files of the roadmap, if any
- Do not commit the file

# Constraints

- Do not modify any file of the reviewed dir except the checklist file
  - Delete the `*.log` files that running the dir's scripts created
- Do not invent a command, file, or function
  - If the command is unknown, write `find the command` as the item text
- Use `:`, not `-`, to separate a file from its description
- Do not use emojis or the em-dash

# Examples

- Run on the dir `research/Estimate_academic_paper_quality`
  - Level 1 skims `research/Estimate_academic_paper_quality/README.md` and runs the
    dry run of `estimate_paper_quality.py` on `paper_list.short.csv`
  - Level 2 reads the architecture doc, skims `epq_types.py` and the four stages,
    and runs the end-to-end test with the live log
  - Level 3 reads `epq_paths.py` and `test/test_epq_paths.py`, runs it, and so on
    up to `populate_affiliation_tiers.py`, then reads the plan and the decisions
  - Level 3 ends with the end-to-end demo: it reads `code_demo.md`, runs the demo
    into `./run_demo`, matches each output file with `code_demo.md`, and checks the
    summary of each stage

# Verification

- [ ] The output file is `code_tour.md`, in the reviewed dir
- [ ] Exactly three levels are present, in order, titled `Understand in 15 Mins`,
      `Understand in 1 Hour`, and `Understand in Full`
- [ ] Every checkbox starts with `- [ ]` or `- [x]`
- [ ] Every item starts with `(<N> mins)` or `(1 min)` after the checkbox
- [ ] The `Time` line of each level equals the sum of its items' times
- [ ] `End-to-End Demo` is in Level 3, with items that read `code_demo.md`, run
      the demo, and check the output
- [ ] `End-to-End Demo` does not explain the output files: it points to
      `code_demo.md`
- [ ] The checklist has no `# Map of the Dir`, no reading speeds, and no file table
- [ ] The header says the map and the table are in the `# Review roadmap` section
      of the dir `README.md`
- [ ] Item paths are from the repo root
- [ ] Each reading item's time follows the roadmap reading speeds
- [ ] Every item that reads a file starts with `Read all of` or `Skim all of`
  - The only exceptions are the diff items and the header of a raw export
- [ ] No reading item uses `Look at`, a section name, or a function name as scope
- [ ] Every `code`, `doc`, and `test` file of the roadmap table is in an item, or
      in the "Skipped" line of the roadmap
- [ ] Every file named in the checklist exists
- [ ] Level 3 code items follow the `code` row order of the roadmap, bottom up
- [ ] No item appears twice with the same action in two levels
- [ ] No file is skimmed and then read in Level 3
- [ ] Each item that reads a doc with a diagram has the step
      `open_md.py -i <DOC_PATH>`, and no other item has it
- [ ] Every example command was run, or says what it needs
- [ ] No test command uses `uv`
- [ ] No line is over 85 characters outside code blocks, tables, and one-path lines
- [ ] No item is longer than 4 lines
- [ ] No file of the reviewed dir changed, except the checklist file
