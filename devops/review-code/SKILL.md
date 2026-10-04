---
name: review-code
description: "A thorough multi-agent audit of an existing codebase against the development skills, with one sub-agent per domain. Use when re-engaging a project you have not touched recently, when the skills may have changed since the code was written, when auditing a specific package or domain, or when a deliberate compliance pass is wanted. Not for checking the diff you just wrote, which the develop skill already covers. Accepts an optional target: a domain keyword such as cli, node, infra, or concurrency, or a package path such as internal/server."
user-invocable: true
---

# Review Code

**Detect the project type, work out which domains apply, hand each to a sub-agent that reads the governing skills, then combine the findings into one report.**

## Start here: required reading

Read the manifest for every domain in scope before that domain is reviewed: by you for a targeted review, or by the domain's sub-agent for a full one. A manifest names the skills to load, the applicability rules, and how each check is verified. Read only the manifests for domains that apply to the detected project type.

**Before reviewing a domain:**
- `./references/review-domain-go-core.md`: Go layout, idioms, logging, config, tests
- `./references/review-domain-go-cli.md`: the command tree, flags and arguments, output tiers, prompts, progress
- `./references/review-domain-go-server.md`: package architecture, HTTP server, OAuth, frontend
- `./references/review-domain-go-concurrency.md`: goroutine primitives and the job pipeline
- `./references/review-domain-node.md`: Node layout, idioms, server, auth, config, frontend
- `./references/review-domain-infra.md`: Makefiles, release workflow, containers, README, extensions

## Where the Expected Pattern Comes From

A manifest lists what to check and how to verify it. It does not restate what the correct answer is. The expected pattern for every check lives in the skill that owns it, and the reviewing agent reads that skill before running the check.

This is deliberate. A check table that repeats a rule is a second copy that drifts the moment the skill is edited, and the copy in the review is the one nobody notices is stale. Improving a skill improves the review for free.

Every finding cites the skill and the section it comes from. A finding that cannot cite one is not a finding, and reporting it anyway trains the reader to ignore the report.

## Workflow

### Step 1: Detect the project type

| Indicator | Type |
|---|---|
| `go.mod` with `cmd/` and `utils/`, no `internal/server/` | Go CLI Only |
| `go.mod` with `internal/server/static/`, no `utils/` | Go Web Only |
| `go.mod` with `internal/server/static/` and `utils/` | Go CLI + Web |
| `go.mod` with `internal/server/` and no `static/`, no `utils/` | Go Headless API Service |
| `go.mod` with no `main.go` and no `cobra` | Go Library |
| `manifest.json` carrying `manifest_version` | Chrome Extension |
| `package.json` with `"type":"module"`, plus `public/` and `src/`, no `go.mod` | Node Web Only |
| `go.mod` alone | treat as Go CLI Only |

Report and stop when nothing matches, since a review against the wrong taxonomy produces findings that are all false.

### Step 2: Parse the target

With no target, go to Step 3a. With one, resolve it here first.

| Keywords | Domain | Scope |
|---|---|---|
| `core`, `foundations`, `layout`, `logging`, `idioms`, `config` | Go Core | whole domain |
| `tests`, `testing` | Go Core and Node | the testing checks only |
| `cli`, `cobra`, `structure`, `root`, `commands`, `flags`, `args`, `stdin`, `output`, `prompts`, `progress`, `tui` | Go CLI | whole domain |
| `server`, `backend`, `frontend`, `web`, `http`, `auth`, `oauth`, `markdown`, `mermaid` | Go Server and Frontend | whole domain |
| `concurrency`, `goroutines`, `pipeline` | Go Concurrency | whole domain |
| `node`, `nodejs`, `esm` | Node | whole domain |
| `makefile`, `assets`, `build` | Infrastructure | Makefile checks only |
| `ci`, `cd`, `cicd`, `release`, `workflow` | Infrastructure | release workflow checks only |
| `docker`, `container`, `dockerfile` | Infrastructure | container checks only |
| `readme` | Infrastructure | README checks only |
| `chrome`, `extension` | Infrastructure | extension checks only |
| `deps`, `dependencies` | Go Core and Node | dependency checks only |
| `infra`, `infrastructure` | Infrastructure | whole domain |

A target containing `/` is a package path:

| Path | Domains |
|---|---|
| `cmd/**` | Go CLI |
| `utils/**` | Go CLI |
| `internal/server/static/**` | Go Server and Frontend |
| `internal/server/**` | Go Server and Frontend |
| `internal/auth/**` | Go Server and Frontend |
| `internal/**`, anything else | Go Core and Go Server and Frontend |
| `src/**`, `public/**`, `test/**`, `package.json` | Node |
| `.github/**`, `Makefile`, `Dockerfile`, `README.md` | Infrastructure |

A target that matches no keyword row and contains no `/` resolves to nothing, and is reported rather than guessed at:

```
No domain matches the target "[target]". The domains are core, cli, server, concurrency, node, and infra.
```

Guessing at the nearest-looking domain reviews something the user did not ask about, and every finding it produces is noise they have to read before discarding. Naming the domains costs one message and lets them say which they meant.

When the resolved domain does not apply to the detected project type, report that and stop:

```
The [domain] domain does not apply to this project type ([project type]).
```

Otherwise go to Step 3b.

### Step 3a: Full review

| Project type | Domains |
|---|---|
| Go CLI Only | Go Core, Go CLI, Go Concurrency (conditional), Infrastructure |
| Go Web Only | Go Core, Go CLI, Go Server and Frontend, Infrastructure |
| Go CLI + Web | Go Core, Go CLI, Go Server and Frontend, Go Concurrency (conditional), Infrastructure |
| Go Headless API Service | Go Core, Go Server and Frontend, Go Concurrency (conditional), Infrastructure |
| Go Library | Go Core |
| Chrome Extension | Infrastructure |
| Node Web Only | Node, Infrastructure |

With one domain applying, handle it inline: read the manifest, load its skills, run the checks, and produce the report. Spawning a single sub-agent adds a round trip and no parallelism.

With several, launch one sub-agent per domain, all in a single message so they run concurrently.

Resolve `[SKILLS_DIR]` to an absolute path before building any prompt: it is the parent of this skill's own directory. Sub-agents run in the target project's working directory, so a relative path resolves against the wrong root.

```
You are a focused code review agent for the [DOMAIN_NAME] domain.

## Context
- Project type: [PROJECT_TYPE]
- Working directory: [CWD]
- Skills directory (absolute): [SKILLS_DIR]

## Instructions

1. Read your domain manifest:
   [SKILLS_DIR]/review-code/references/review-domain-[DOMAIN_FILE].md

2. Read, in full, every skill the manifest lists. They are at
   [SKILLS_DIR]/[SKILL_NAME]/SKILL.md
   The manifest states what to check and how to verify it; the skill states what the
   correct answer is. Running a check without having read its skill produces a
   finding you cannot cite.

3. Inspect the project in [CWD] against every check in the manifest that applies to
   [PROJECT_TYPE]. Use Read, Glob, Grep, and read-only Bash. For a conditional check,
   detect whether the pattern is present before reviewing it. Read the actual source
   files rather than inferring from names.

4. Report using the output format in the manifest.

5. Do not flag anything that is not defined in a skill you loaded. If you cannot cite
   a specific skill section, it is not a finding.

6. End your response with exactly:
   SUMMARY_LINE: categories_checked=N pass=N issues=N skipped=N total_issues=N
```

Go to Step 3c.

### Step 3b: Targeted review

Handle it inline with no sub-agents. Read the manifest, load the skills it names, narrow to the requested subset or package scope, run the applicable checks, and produce the report.

A package path narrows file-existence checks to that package while keeping cross-cutting checks such as error handling and logging, since those are the ones a package most commonly gets wrong in isolation.

Go to Step 3c.

### Step 3c: Comment audit

Run this once for the whole review rather than per domain, over the files in scope.

```bash
rg -n '^\s*(//|/\*|\*)' --glob '*.go' --glob '*.js' --glob '*.ts' <scope>
```

Read each hit and map it to one of the two exceptions in AGENTS.md (CLAUDE.md if you are Claude). Anything that maps to neither is a `low` finding citing that rule, with `file:line` and `delete` as the disposition. The comment rules are the one source outside the skills that produces a finding, so a citation to them satisfies the citation requirement everywhere it appears.

Go to Step 4.

### Step 4: Report

Combine the sub-agent outputs, or use the inline findings.

```
## Code Review Report: [Project Name]

**Project type:** [type]
**Review scope:** [Full | Targeted: domain | Targeted: path]
**Skills checked against:** [list]

---

[domain sections]

---

### Summary

| Category | Status | Issues |
|----------|--------|--------|
| Project Layout | PASS | 0 |
| Core Principles | ISSUES | 2 |

**Total issues found:** N
```

### Step 5: Offer to fix

```
Would you like me to fix these issues? I can address them one category at a time.
```

Work through the categories in order when the answer is yes.

## Principles

Be specific enough to act on. "Missing `PrintFatal` in `utils/printer.go`" is a finding; "the utils package is incomplete" is a complaint.

Every finding carries `file:line`, a severity, and what to do about it. A finding without a location is a complaint, and one without a disposition leaves the reader to redo the analysis that produced it.

A finding changes behavior, breaks a build, or opens a hole. Severity is `high` when it breaks a build or opens a hole, `medium` when behavior is wrong in a case a user can reach, and `low` when a loaded skill's rule is broken with no behavioral consequence yet. Style preferences, naming, and hypotheticals are not findings at any severity, because a report padded with them trains the reader to skim past the two that matter.

Every expected value and every suggested fix comes from a loaded skill rather than from general practice, because a review that invents standards produces work nobody agreed to.

Detect before diving. Check whether a pattern is even used before reviewing it in depth, so a project with no goroutines gets a skip rather than a paragraph.

Skip categories that do not apply to the detected project type. A `utils/` finding against a Web Only project is backwards: its absence is the rule.

## Out of Scope

None of the following is defined in any skill, so none of it is ever a finding. This is the full list, and it is stated here once rather than in each manifest.

| Category | Examples |
|---|---|
| Linting and formatting | no golangci-lint, no eslint, no gofmt, inconsistent formatting |
| Pre-commit | no hooks, no husky |
| Code quality CI | no lint or format steps in a workflow |
| Documentation beyond README | no godoc, no jsdoc, no changelog, no contributing guide |
| Compose files | no docker-compose for development |
| Database | no migrations, no schema files |
| Dependency tooling | no dependabot, no renovate |
| Security scanning | no SAST, no container scanning |
| Style opinions | naming conventions no skill defines, personal preference |

If you are about to flag something and cannot point at a specific section of a loaded skill that defines the expected pattern, do not flag it.
