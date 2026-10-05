---
name: workflow-names
description:
  Check that every GitHub Actions workflow, job, and step has a name, and write
  the missing ones in imperative, sentence-case style. Use when the user wants
  workflow names added, reviewed, or tidied, when a run log shows raw run
  commands or job ids, or when writing a new workflow.
version: 0.1.0
---

# Workflow Names

GitHub Actions shows a fallback wherever a name is missing:

- a workflow falls back to its file path
- a job falls back to its job id
- a step falls back to its `run` command or action reference

A name turns the log line into documentation, while the fallback leaves it as
source code.

## Procedure

### 1. Inventory the nameable nodes

Find every workflow file under `.github/workflows/` and every composite action
file (`action.yml` or `action.yaml`). In each file, list the nodes that take a
name:

- the workflow `name`
- each job's `name`
- each step's `name`, in jobs and in a composite action's `runs.steps`
- a composite action's own `name` and `description`

Mark each node named or unnamed. Done when every node in every file is on the
list.

### 2. Write the names

Add a name to every node that lacks one, and rewrite every name that breaks a
rule below. Done when each name on the list follows the rules below.

### 3. Verify

Run `actionlint` on the changed files if the tool is installed. Read the changed
files again and check each name against the rules. Report each file with the
names you added, and quote the old and new name for each rewrite.

## Rules

### Names by node

- **Workflow** - a short noun phrase for the pipeline's purpose: `CI`,
  `Release`, `Deploy documentation`.
- **Job** - what the job checks or produces: `Build`, `Lint`,
  `Test on ${{ matrix.os }}`. Interpolate matrix values so parallel jobs are
  distinguishable in the run list.
- **Step** - what the step does, written like a commit subject:
  `Check out the repository`, `Run the unit tests`,
  `Upload the coverage report`.

### Style

- **Active voice, imperative present tense.** Start step names with a verb:
  `Install`, `Build`, `Publish`. Name the outcome, not the tool:
  `Check out the repository`, not `actions/checkout` or `Uses checkout`.
- **Sentence case.** Capitalize only the first word and names that are always
  capitalized, such as GitHub or Docker. No trailing period.
- **Concise.** A name fits on one line of the run log; past about 50
  characters, cut words. Drop filler the context already carries: `step`,
  `job`, `workflow`, `this`, `action`.
- **Unique within its scope.** Jobs or steps that share a name produce
  ambiguous log lines. Distinguish them by their object (`Build the app`,
  `Build the docs`).

Identifiers are not names. Job ids, step `id` values, and `concurrency` groups
are keys that expressions reference; keep them lowercase kebab-case and leave
them out of this review.

`run-name` is optional. Add it only when run context distinguishes runs, as in
`run-name: Deploy ${{ inputs.environment }}`. A static `run-name` only repeats
the workflow name, so omit it.
