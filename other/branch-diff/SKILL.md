---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: branch-diff
description: >
  Show the full diff of the current branch against the upstream default branch
  (upstream/main if the repo is a fork, else origin/main). Covers finding the
  base ref with gh, listing commits, --stat overview, excluding lock and
  generated files with pathspecs, and paginating large diffs with sed. Load
  when asked to review a branch, PR, or "what changed on this branch".
---

# Compare Current Branch Against Upstream Default

Compare the current branch against the upstream default branch and view the full diff.

## Step 1: Determine BASE_REF

Run:
```bash
git remote -v
```

If `upstream` remote exists, run:
```bash
DEFAULT_BRANCH=$(gh repo view $(git remote get-url upstream) --json defaultBranchRef --jq '.defaultBranchRef.name') && echo "upstream/$DEFAULT_BRANCH"
```

Otherwise, run:
```bash
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name') && echo "origin/$DEFAULT_BRANCH"
```

Set `BASE_REF` to the output (e.g., `upstream/main`).

## Step 2: Fetch and View Commits

```bash
git fetch ${BASE_REF%%/*} && git log --oneline $BASE_REF...HEAD
```

## Step 3: View Diff Stats

Run `--stat` first to get an overview of changes per file:

```bash
git diff $BASE_REF...HEAD --stat
```

This shows files changed and lines added/removed. Use this to:
- Identify noisy files to exclude (lock files, generated code with 1000s of lines)
- Determine if pagination is needed (large total line count)
- Get a quick overview before diving into the full diff

## Step 4: View Full Diff

```bash
git diff $BASE_REF...HEAD -U20
```

always exclude noisy files, use pathspec excludes. Add patterns as needed based on the project:

```bash
git diff $BASE_REF...HEAD -U20 -- \
  ':!*.lock' \
  ':!package-lock.json' \
  ':!pnpm-lock.yaml'
```

### Common files to exclude

**Lock files:**
- `*.lock`, `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `bun.lockb`

**Generated code (committed but auto-generated):**
- `*/generated/*`, `*.generated.ts`, `*.gen.ts`, `*.gen.go`
- OpenAPI/Swagger generated clients
- Protobuf generated files: `*.pb.go`, `*_pb.ts`

**Snapshots (if reviewing logic, not snapshot updates):**
- `*.snap`, `__snapshots__/*`

only do this if you already know about files to exclude from your existing context

## Paginating Large Diffs

For large diffs, paginate using `sed` to view specific line ranges with no overlap:

```bash
# Page 1: lines 1-500
git diff $BASE_REF...HEAD -U20 -- ':!*.lock' | sed -n '1,500p'

# Page 2: lines 501-1000
git diff $BASE_REF...HEAD -U20 -- ':!*.lock' | sed -n '501,1000p'

# Page 3: lines 1001-1500
git diff $BASE_REF...HEAD -U20 -- ':!*.lock' | sed -n '1001,1500p'
```

Continue incrementing by 500 until output is empty.
