---
name: parallel-steps
description:
  Make GitHub Actions steps run in parallel with the background, wait, wait-all,
  cancel, and parallel keywords. Use when the user wants a faster job, starts a
  service in a job, or asks for background or parallel steps.
version: 0.2.0
---

# Parallel Steps

GitHub Actions runs the steps of a job in sequence. The `background` keywords
change this. The model is the shell: `background: true` is `&`, and `wait` is
`wait`.

This document obeys ASD-STE100 Simplified Technical English. Write all prose
that you add to it in the same style.

## Procedure

### 1. Map the dependencies

Read the workflow file. For each step, find the steps that must complete before
it. A step depends on a different step when it reads that step's files, outputs,
or services. Done when each step has a list of the steps it depends on. An empty
list is permitted.

### 2. Apply the keywords

Change the steps by their role:

- **Independent group.** Put steps with no dependencies between them in one
  `parallel` block.
- **Service.** A server, a database, or an emulator: give the step an `id` and
  set `background: true`. Add a `cancel: <id>` step after the last step that
  uses the service.
- **Side task.** A step that no different step reads, such as a telemetry
  upload: set `background: true`. Do not add `wait`.
- **Reader.** A step that reads the result of a background step: add a
  `wait: <id>` step before it. To wait for all the background steps that came
  before, use `wait-all` in place of `wait`.

Done when each background step has a `wait` or `cancel` reference. A side task
with no reader needs neither.

### 3. Verify the workflow

Run `actionlint` on the file if the tool is installed. `actionlint` does not
support these keywords yet
([rhysd/actionlint#693](https://github.com/rhysd/actionlint/issues/693)), so it
can report an error or a warning on a `background`, `wait`, `wait-all`,
`cancel`, or `parallel` step that agrees with the reference. Ignore those
messages. Read the changed workflow again. Make sure that no step reads data
from a background step without a `wait` between them. Report the steps that stay
in sequence and the reason for each.

## Keywords

| Keyword            | Effect                                                                      |
| ------------------ | --------------------------------------------------------------------------- |
| `background: true` | Starts the step and continues to the next step immediately.                 |
| `wait: <id>`       | Stops until the referenced steps complete. Accepts one id or a list of ids. |
| `wait-all:`        | Stops until all the background steps before this point complete.            |
| `cancel: <id>`     | Stops the named background step without an error.                           |
| `parallel:`        | Runs a group of steps as background steps, then waits for all of them.      |

For the full behavior of each keyword - concurrency limits, output availability,
failure rules, and composite-action restrictions - see
[references/keywords.md](references/keywords.md).

## Example: service

```yaml
steps:
  - name: Start test server
    id: server
    run: npm run start
    background: true
  - name: Run E2E tests
    run: npm run e2e
  - name: Stop server
    cancel: server
```

## Example: independent group

```yaml
steps:
  - parallel:
      - name: Build the app
        run: npm run build
      - name: Build the docs
        run: npm run docs
  - name: Package
    run: npm run package
```

<!-- vale ai-tells.ParallelStaccato = NO -->
<!-- The rule reads the conditional below as the second half of a staccato
     pair. This document also obeys ASD-STE100, which mandates the short
     sentences the rule flags. -->

The
[workflow syntax reference](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
is the source of truth for these keywords. If a keyword does not agree with this
document, obey the reference.

<!-- vale ai-tells.ParallelStaccato = YES -->
