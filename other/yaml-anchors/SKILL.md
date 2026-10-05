---
name: yaml-anchors
description:
  Replace repeated configuration in a GitHub Actions workflow with YAML anchors
  and aliases. Use when the user wants a shorter workflow, mentions YAML anchors,
  or writes the same env, services, permissions, or path filter in more than one
  job of the same file.
version: 0.1.0
---

# YAML Anchors

GitHub Actions parses workflow YAML with anchors and aliases since
[18 September 2025](https://github.blog/changelog/2025-09-18-actions-yaml-anchors-and-non-public-workflow-templates/).
GitHub rejects the merge key (`<<`), so an alias overrides nothing: a copy that
differs by one key is out of an anchor's reach.

## Procedure

### 1. Inventory the repeated blocks

Read every workflow in `.github/workflows/`. Find the configuration written more
than once in the same file and record each copy's file, job, and key. These keys
hold most of the duplication.

- `env` maps shared by jobs
- `services` containers, such as a database or a cache
- `permissions`
- `paths`, `paths-ignore`, and `branches` filters under `on.push` and
  `on.pull_request`
- `runs-on`, when it names a set of self-hosted labels

Compare the copies of each block key by key and mark them identical or
different. Done when every repeated block has a site list and that verdict.

### 2. Identify anchor candidates

Anchor a block of three lines or more that is identical across two or more sites
in the same file.

Done when each candidate has a verdict: anchor or leave.

### 3. Anchor the identical blocks

Copy each workflow before you change it, so step 4 compares against the file as
it stood. `git show HEAD:<file>` returns the committed file, which is a
different document whenever the working tree already carries an edit.

```bash
cp .github/workflows/ci.yml /tmp/before.yml
```

- **Define on the first copy.** Put `&name` on the first copy in document order
  and `*name` on each later copy.
- **Anchor configuration that is already doing a job.** A workflow accepts eight
  top-level keys - `name`, `run-name`, `on`, `permissions`, `env`, `defaults`,
  `concurrency`, and `jobs` - so a workflow has nowhere to park a block of
  definitions.
- **Name the anchor after its content**, such as `&env_vars` or `&code_paths`.
- **Alias whole nodes.** An alias replaces a node. It appends to no list and
  overrides no key.
- **Keep the anchored expressions context-free.** An alias copies `${{ ... }}`
  as text, and the expression evaluates against the job that holds the alias, so
  `${{ matrix.node }}` inside an anchor expands to nothing in a job that has no
  matrix.

Done when each anchor has at least one alias, and each alias resolves to an
anchor written earlier in the file.

### 4. Verify

Run `actionlint` on each changed workflow.

```bash
actionlint .github/workflows/ci.yml
```

It reads anchors and aliases, and it reports a merge key by name:
`GitHub Actions does not support YAML merge key "<<"`. A YAML library reports
nothing there, because PyYAML follows YAML 1.1 and expands `<<` in silence.

Then prove the rewrite didn't change behavior.

```bash
python3 -c '
import sys, yaml
before, after = (yaml.safe_load(open(p)) for p in sys.argv[1:])
sys.exit(0 if before == after else "workflows differ")
' /tmp/before.yml .github/workflows/ci.yml
```

Where `import yaml` raises `ModuleNotFoundError`, run the same script through
`uv run --with pyyaml python -c` instead.

`zizmor` 1.29 audits every alias site and prints each finding at the anchor's
line. A finding repeated on one line describes a different job each time.

Report the blocks that an anchor cannot reach and the reason for each.

## Example

```yaml
on:
  push:
    paths: &code_paths
      - "src/**"
      - "package.json"
  pull_request:
    paths: *code_paths

jobs:
  test:
    runs-on: ubuntu-latest
    services: &postgres
      db:
        image: postgres:18
        env:
          POSTGRES_PASSWORD: postgres
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v6
      - run: npm test

  integration:
    runs-on: ubuntu-latest
    services: *postgres
    steps:
      - uses: actions/checkout@v6
      - run: npm run test:integration
```

[Reusing workflow configurations](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations)
is the source of truth for anchors. If a rule here disagrees with that page,
obey the page.
