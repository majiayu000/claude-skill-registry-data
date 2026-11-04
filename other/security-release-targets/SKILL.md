---
name: security-release-targets
description: Given a Mattermost priority/severity level (Critical/High/Medium/Low), resolve the target release-X.Y branches to cherry-pick onto by parsing the Mattermost release policy (ESR/active/upcoming) and keeping only branches that exist on mattermost/mattermost. Use when you need the list of release branches a fix must be backported to for a given severity.
allowed-tools: Read, Bash(git ls-remote:*)
---

# Resolve target release branches for a severity

You take a single priority/severity level and return the set of `release-X.Y`
branches that a fix at that level must be cherry-picked onto, per the Mattermost
release policy. You do NOT look at PRs, Jira, labels, or open anything — you only
resolve branches. Ticket handling and gating live in the caller.

## Input

- `<PRIORITY>`: one of `Critical` | `High` | `Medium` | `Low`.
  - Treat `Highest` as Critical-tier and `Lowest` as Low-tier.
  - If the value is missing or unrecognised, return an empty result and report the unsupported priority.

## Step 1: Parse the release policy

Read and parse the policy once here; later steps consume the sets produced below rather than re-reading the file.

- Read `docs/main/product-overview/release-policy.mdx` from the `mattermost/mattermost` repo, which is loaded in the workspace context.
- Locate the ` ```mermaid ` fenced code block containing `gantt`.
- Parse each release row `vX.Y[ & ...] :<status>, <start>, <end>`:
  - Locate the status marker `:(crit|active|done),` and treat everything before that marker as the row label. Status markers may contain multiple flags, e.g. `:crit, :done, ...`. Parse all status flags that appear before the start/end dates, not just the first one. 
  - Do not assume the row label is only `vX.Y`. Extract the Mattermost server release version only from the start of the label using `^\s*(v\d+\.\d+)\b`. Ignore additional label text such as `& Desktop App v6.2 Extended Support`; never extract Desktop App versions as server release targets.
  - Rows tagged both `:crit` and `:active` are ESR (Extended Support) versions, even when their label contains extra descriptive text. Ignore `:crit` rows that are not also `:active` (e.g. `:crit, :done` is end-of-life). There should always be at least one ESR row.
  - Rows tagged `:active` are active versions.
  - Rows tagged `:done` are end-of-life; ignore them.
- Let `ESR` = versions tagged both `:crit` and `:active`; `ACTIVE` = all `:active` versions; `UPCOMING` = the highest ACTIVE version (the next release). Determine "highest" by comparing major and minor as integers, never by string ordering — `v11.11` outranks `v11.9`, and a lexical sort would get that backwards.

## Step 2: Map priority to candidate versions

- Critical / High / Medium  ->  `ACTIVE ∪ ESR`
- Low                       ->  `{UPCOMING} ∪ ESR`

## Step 3: Determine target release branches

Use the candidate version set from Step 2 — do not re-fetch or re-parse the release policy.

- Map each candidate version `vX.Y` to the branch `release-X.Y` (drop the leading `v`, keep major.minor only, e.g. `v11.7 -> release-11.7`).
- Keep only branches that already exist on the `mattermost/mattermost` remote. Always use the explicit URL — never bare `origin`, which may point to a different repository when this skill is invoked from a plugin checkout:

  ```bash
  git ls-remote --heads https://github.com/mattermost/mattermost.git release-X.Y
  ```

  (This enforces "upcoming version only if its branch has already been created"; ESR and shipped active branches will exist, an uncut upcoming branch will be skipped.)
- Dedupe.

## Output

Return the deduped list of existing `release-X.Y` target branches. If no branch
remains, return an empty list (the caller should take no action).
