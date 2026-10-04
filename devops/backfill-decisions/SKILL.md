---
name: backfill-decisions
description: >
  Mines the git history of a repository for architecturally significant decisions taken in the past,
  and writes Decision Records for them retroactively, following the log-decision conventions. This
  skill is user-only: it runs only when the user invokes /backfill-decisions [time range, path, or
  topic]. When the user wants to document historical or undocumented decisions, reconstruct ADRs or
  DRs from git history, generate ADRs for a legacy or existing codebase, or document the history of
  an architecture, suggest this command. For a decision that someone is taking right now, use
  /log-decision instead.
argument-hint: "[time range, path, or topic: 2023..2024, src/api, \"database\"]"
allowed-tools: [Bash(git:*), Read, Glob, Grep, Write, Edit, AskUserQuestion]
disable-model-invocation: true
---

# Backfill Decisions

Reconstruct Decision Records, called DRs, for significant past decisions, by mining the git history. This skill produces *retroactive* DRs. Someone already took and adopted each decision. The goal is to capture the evidence and the reasoning that the history reveals, marked honestly as a reconstruction.

> **Taking a decision now?** Use `/log-decision` to record it while the reasoning is fresh, or `/decide` when you are still exploring options. This skill covers only decisions already buried in the repository's past.

## Execution steps

### Phase 0: Preconditions and scope

1. Run `git rev-parse --is-inside-work-tree`. When the command reports that you are outside a repository, stop and tell the user.
2. Run `git rev-parse --is-shallow-repository`. When the result is `true`, warn the user that the clone is shallow. The history is truncated, so mining it silently misses most decisions. Suggest `git fetch --unshallow` before you continue.
3. Gauge the repo. Run `git rev-list --count HEAD` for the commit count, and `git log --reverse --date=short --pretty='%ad' | head -1` for the date of the first commit.
4. Parse `$ARGUMENTS` when the user passed any. The argument holds any combination of three things:
   - A **date range**, such as `2023..2024`. Translate it to `--since` and `--until` on every `git log`.
   - A **path**, such as `src/api`. Append `-- <path>` to every `git log`.
   - A **topic keyword**, such as `"database"`. Add it to the grep patterns in Phase 2.
5. When more than roughly 1,500 commits fall in scope and the user gave no range, use `AskUserQuestion`. Offer two choices. The first is to scan the whole history **era by era**, with one calendar year per era, oldest first. Mine and triage each era before the next one. The second is to let the user pick a narrower range.

### Phase 1: Inventory the existing DRs, which is the dedup gate

1. Locate the DR directory with the same priority order that log-decision uses: `docs/decisions/`, then `adr/`, then `.decisions/`. Also Glob more broadly for reading, with `**/adr/*.md`, `**/decisions/*.md`, and the MADR-style `NNNN-*.md`, because the target repo can use a different convention. **Write** new DRs only to the priority-ordered directory, and create `docs/decisions/` when none of the three exists.
2. Read the title and the opening paragraph of every existing DR. Build a list of the covered topics, and record the highest `DR-NNNN` sequence number.
3. Exclude from triage any mined candidate that matches a covered topic, and report it as *"already recorded in DR-NNNN"*.

### Phase 2: Mine signals

A candidate decision is **architecturally significant** when it hits at least one of these signals:

| Signal class | What counts |
|---|---|
| Technology adoption or replacement | A new or removed framework, database, message broker, language, or major library in a dependency manifest |
| Infrastructure and delivery | A Dockerfile, a compose file, a k8s manifest, Terraform, Bicep, or a CI workflow introduced, replaced, or removed |
| Structural reshaping | A top-level directory added or deleted, a subsystem extracted, merged, or renamed, or a monorepo restructure |
| Cross-cutting pattern change | The auth mechanism, the persistence pattern, the API style such as REST to gRPC or GraphQL, eventing, or caching |
| Costly major upgrades | A version jump that forced widespread code changes, such as .NET 6 to 8, Python 2 to 3, or class components to hooks |

**Counter-signals, which you ignore:** a routine dependency bump, a formatting or lint commit, and a bug fix. Also ignore a feature added inside an existing pattern, and a change to a lockfile alone.

Run these sweeps. Run them per era when you work era by era.

1. **Keyword sweep of commit subjects:**
   ```
   git log --date=short --pretty='%h|%ad|%an|%s' -i -E --grep='migrat|replac|adopt|switch(ed|ing)? to|introduc|rewrit|deprecat|drop (support|the)|remove (support|the)|upgrade to|consolidat|split out|extract'
   ```
2. **Merge and PR titles.** A PR title often states the decision word for word:
   ```
   git log --merges --date=short --pretty='%h|%ad|%an|%s'
   ```
3. **Manifest archaeology.** Glob the repo root for the manifests that exist, which are `package.json`, `*.csproj` and `Directory.Packages.props`, `go.mod`, `pyproject.toml` and `requirements.txt`, `pom.xml` and `build.gradle*`, `Gemfile`, and `Cargo.toml`. For each manifest, run `git log --follow --date=short --pretty='%h|%ad|%s' -- <manifest>`. Then run `git show <hash> -- <manifest>` only for the hits that look like an add or a removal of a top-level dependency, and not for a version bump.
4. **Infra file births and deaths:**
   ```
   git log --diff-filter=AD --date=short --pretty='%h|%ad|%s' --name-status -- 'Dockerfile*' 'docker-compose*' '*.tf' '*.bicep' '.github/workflows' '.gitlab-ci.yml' 'azure-pipelines*'
   ```
5. **Structural snapshots.** Compare the top-level trees at boundary revisions with `git ls-tree --name-only <rev>`. When you work era by era, the boundaries are the era edges. In a single-pass scan, sample one revision per year with `git rev-list -1 --before=<YYYY-12-31> HEAD`. For a young repo, compare the root commit against `HEAD`. A directory that appears or disappears between two boundaries is a structural signal. Locate the originating commits with `git log --diff-filter=A --oneline -- <dir>`.
6. **Big-bang commits.** Run `git log --date=short --pretty='%h|%ad|%s' --shortstat`, and flag any commit that touches more than roughly 100 files.

### Phase 3: Cluster the hits into candidate decisions

- Group the hits that share a theme, which is the same dependency, subsystem, or directory, **and** that share a time window. Commits within a few weeks of each other usually belong to one decision, and a migration spans many commits.
- Assemble an evidence card per candidate, with six parts:
  - The inferred title, in the imperative style of log-decision, such as *"Adopt MediatR for in-process messaging"*.
  - The date range of the cluster.
  - Two to five representative commit hashes: the first, the last, and the most descriptive.
  - The authors of the commits in the cluster, from `git shortlog -sn <first>~1..<last> -- <path>`. Fall back to `git shortlog -sn <last>` when `<first>` is the root commit, because a plain `<first>..<last>` excludes the first commit, which is often the most important one.
  - A one-line evidence summary.
  - The confidence: high, medium, or low.

  Here is an example evidence card:

  > **Adopt SQS for asynchronous messaging** — 2023-03-02..2023-04-11 · commits `a1b2c3d`, `e4f5a6b`, `c7d8e9f` · authors: J. Doe, M. Silva · evidence: `aws-sdk-sqs` added to package.json, `rabbitmq` removed three weeks later, CI gained an SQS integration test job · confidence: **high**
- **Reversal detection**: the same subject is sometimes adopted and later removed or replaced, such as a dependency added in 2022 and deleted in 2024. Pair the two as **two linked candidates**. The original becomes `superseded by DR-NNNN`, or `retired` when nothing replaced it. The reversal becomes `adopted`, and it references the first. Present them as a linked pair in triage.
- **Trade-off check**: a DR is interesting for the trade-off that it weighs. Sometimes the evidence shows no rejected alternative, because nothing was removed or replaced, and no accepted downside. Then downgrade the confidence of the candidate by one level. Carry the note *"no observable trade-off"* into its triage line. The user can still confirm it, and it must not ride in with the high-confidence batch by default.

### Phase 4: Triage with the user

1. Print a numbered markdown table in the chat, with the columns `# | Proposed DR title | Date | Evidence | Confidence | Note`. A note holds an *"already recorded in DR-NNNN"* exclusion, or a *"pair: reverses #3"* link. Here is an example row:

   | # | Proposed DR title | Date | Evidence | Confidence | Note |
   |---|---|---|---|---|---|
   | 4 | Adopt SQS for asynchronous messaging | 2023-03 | aws-sdk-sqs added, rabbitmq removed, CI job added | high | pair: reverses #3 |
2. Then ask one `AskUserQuestion` with three options: **write all high-confidence**, **let me select**, or **rescan with a different scope**. On "let me select", follow up with `multiSelect: true` questions, batched four candidates at a time.
3. The user can rename, merge, or split candidates in free text before you write anything.
4. **Never write a DR for an unconfirmed candidate.** Cap the run at roughly 10 DRs. Continue era by era in a follow-up run when more candidates remain.

### Phase 5: Write the DRs through the log-decision workflow

For each confirmed candidate, go straight into the writing steps of the log-decision skill, which cover the directory, the numbering, the filename, and the template. Do not ask the user again for information that the mining already established. Apply these retroactive adaptations:

- **Template**: read `${CLAUDE_SKILL_DIR}/../log-decision/assets/dr-template.md`. That path resolves in both install modes, because log-decision is a sibling skill in this plugin. When the file does not exist, stop and tell the user that this skill requires the log-decision skill.
- **File naming**: the target directory sometimes has an established naming convention, such as the MADR-style `0007-use-postgres.md` with no `DR-` prefix. Match that pattern and continue its numbering. A forked scheme splits the log in two. Use the log-decision default, which is `DR-NNNN-kebab-title.md`, only when the directory is new or holds no consistent pattern.
- **Status**: default to `adopted`. For a reversal pair, the original gets `superseded by DR-NNNN`, or `retired` when nothing replaced it. Cross-link both files in `## More Information`. Both files are new, so write the links directly instead of editing them in later.
- **Date**: use the commit date of the decision, which is the first commit of the cluster or the merge date. Do **not** use today.
- **Decision-makers**: use the commit authors of the cluster. Omit `consulted` and `informed`, because history cannot reveal them.
- **Considered Options**: always include the chosen option, with the pros and cons that the evidence shows. When history reveals a rejected alternative, which is the thing that was removed or replaced, include it too. Otherwise keep only the chosen option, and add this note: *"Alternatives considered at the time were not documented."* Do not ask the user, and do not invent alternatives.
- **Decision**: write the full Y-statement form that log-decision uses, inferred from the evidence and phrased honestly: *"In the context of [observed situation], facing [concern visible in the history], we decided for **X** (inferred from history) and against [the alternative the evidence shows was removed or replaced], to achieve [observable outcome], accepting [downside the evidence reveals]."* Keep the `and against` clause only when history reveals a rejected alternative. That alternative is the one listed in Considered Options. Otherwise drop the clause instead of inventing an alternative.
- **More Information**, which is mandatory here, and optional in log-decision:
  - List the evidence commits as `` `abc1234` (YYYY-MM-DD) — subject ``.
  - When a subject contains `#NNN`, and `git remote get-url origin` resolves to GitHub or GitLab, render each one as a PR or MR link.
  - Cross-link paired DRs with relative paths.
  - End with a provenance line: *"This DR was reconstructed retroactively from git history on YYYY-MM-DD."*
- **Numbering**: continue sequentially from the highest existing number, in whatever naming pattern applies. When you write several DRs in one run, number them in the chronological order of the decision date, so the log reads sensibly.

### Phase 6: Wrap up

Report a table of the files you wrote, with the path, the title, the status, and the date. Remind the user that these are reconstructions and that a human review pass is worth the time. Suggest a commit. Do not offer to improve the DRs unless the user asks.

## Principles

- **Evidence over speculation.** Every claim in a backfilled DR must trace to a commit, a diff, or a commit message. Never fabricate an alternative, a rationale, or a piece of context.
- **Fewer well-evidenced DRs beat many speculative ones.** A medium-confidence candidate that the user does not recognize is better skipped than written.
- **All git usage is read-only.** This skill never commits, never checks out, and never mutates the repository beyond writing DR files.
