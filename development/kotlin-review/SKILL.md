---
name: kotlin-review
description: Review Kotlin tests, architecture, or ABI compatibility, over the working tree, a commit, a pull request, or the whole repository.
disable-model-invocation: true
---

# Kotlin Review

Route a Kotlin quality review to the right agent, over the right scope, and merge the results into one
report. The review criteria live in the agents, not here. This skill decides what to run and reports
what came back.

Three agents ship with this plugin:

| Agent | Question it answers | Applies to |
|---|---|---|
| `kotlin-test-review` | If every test passes, do we know the code works? | any project |
| `kotlin-architecture-review` | Can this codebase absorb the next change without it spreading? | any project |
| `kotlin-abi-review` | Will code compiled against the last release still link? | published libraries only |

All three are read-only. None of them edits files or runs a build.

## Settle the scope first

Do not start until both of these are fixed. Ask only for what the request leaves open.

**1. What to review.** One of:

| Scope | How to get it |
|---|---|
| working tree | `git status --short`, `git diff HEAD`, and the contents of every untracked file named by status |
| a commit | `git show --name-status --format=fuller <ref>` and `git show --find-renames --format= <ref>`; read candidate files from `<ref>`, not from the checkout |
| a pull request | `git diff --name-status <base>...<head>` and `git diff --find-renames <base>...<head>`; read candidate files from `<head>` |
| the whole repository | the module list from the build files |

Default to the working tree when it is dirty, otherwise to the last commit.

The first three scopes are **diff review**. Rank only findings introduced or materially worsened by
that diff. Read surrounding code for context, but do not turn pre-existing debt into findings. Mention
legacy only in an unranked `Pre-existing context` note when it is necessary to explain the change or
blocks a trustworthy verdict. The repository scope is the separate **full scan** mode.

**2. Which review.** Tests, architecture, ABI, or a combination.

- Honor an explicit choice exactly. A request for tests only, for example, does not authorize adding
  architecture or ABI.
- Default to tests and architecture when the scope is the repository or a pull request.
- Default to tests alone when the change touches only test sources.
- When the review type was not explicit, add ABI for modules that have a real publication or external
  consumer contract. In Kotlin Toolchain this means `product: jvm/lib` or `kmp/lib` together with
  `settings.publishing.enabled`; in Gradle it means a library publication configured through
  `maven-publish` or a publishing plugin. API dumps, `explicitApi()`, and ABI-validation configuration
  support that conclusion but do not prove publication on their own.
- Never run the ABI review on an application. There is no ABI to keep.

Confirm the scope and the choice in one line before dispatching, then go. Do not ask a second round of
questions.

## Dispatch

Run all chosen agents in parallel — their initial reviews do not depend on each other.

Give each agent: the scope, the concrete refs or paths, the build system in use, and the module or
modules to look at. For commit and pull-request scopes, include the candidate ref and its comparison
base so the agent never substitutes the current checkout. Do not paste the review criteria into the
prompt; the agent carries its own.

### If the agents are not available

The agents are installed differently per host.

- **Claude Code and Junie.** They come with the plugin/extension. Nothing to do.
- **Codex.** They must be placed into the Codex agents directory first. Run the
  `install-codex-agents` skill from this plugin, then start a new thread. The default target is
  `~/.codex/agents/`, which covers every project on this machine. Installing cannot make an agent
  available to the current thread.

If the user asked to install agents, install them and stop with the new-thread instruction. If the
user asked for a review in the current thread, do not block on installation. Read the full prompt for
each selected agent from `../../agents/<agent>.md`; if that host did not ship the Markdown, read its
generated `developer_instructions` from
`../install-codex-agents/assets/<agent>.toml`. Perform that review directly, say that delegation was
unavailable, and offer installation for future threads. The checklist below is only a routing sanity
check, not a replacement for those full instructions.

Tests:

1. Do assertions check behavior, or only that mocks were called?
2. Are edge cases and failure paths covered, not only the happy path?
3. Does every promised behavior have at least one test that runs the real code path?
4. Is the suite split into slices, one layer each, or does every test boot everything?
5. Do integration tests exist for each external boundary, or is it units only?
6. Does the number of unit, component, integration, and e2e tests fit what the module does?

Architecture:

1. Does the module split follow the domain, or is there a `common`/`util` dumping ground?
2. Are there cycles, backwards dependency arrows, or `api` leaks?
3. Do SOLID violations cost anything real here?
4. Is the core free of framework, IO, and persistence imports?
5. Are time, randomness, IO, and configuration injected rather than called inline?

ABI, on a library only:

1. Resolve the candidate from the requested scope, then compare it with the last verified release of
   that module; keep the requested change range separate from the release range.
2. Do committed `api/*.api` dumps exist, and are they current for that release comparison?
3. Was any public declaration removed, renamed, or moved to another package?
4. Did any generated signature change — return type, parameter type, a new parameter even with a
   default, or `suspend` — or did public inline code change what old and new consumers execute?
5. Did visibility narrow, or did `open` become `final`?
6. Does the version bump match the worst break found? If no released baseline can be verified, the
   ABI verdict is `inconclusive`, not clean.

## Report

One report, findings merged and ranked by risk. Keep the agents' evidence — path, line, and the code
they read. Every finding must name the exact rule ID and title from the agent prompt.

```
## Scope
<what was reviewed, at which ref>

## Verdict
<one sentence per review that ran>

## Tests
<the test agent's verdict table, unproven behaviors, findings, mix table>

## Architecture
<the architecture agent's module map, findings, core purity table>

## ABI
<the ABI agent's verdict, required version bump, breaks, tooling status>

## Pre-existing context
<only legacy needed to understand the diff or a verdict blocker; omit otherwise>

## Do this next
1. <highest value per unit of work, across the reviews that ran>
```

Include only sections for reviews that ran. Name every omitted review and why it was not selected or
did not apply.

When `kotlin-test-review` reports that the real problem is structural, run `kotlin-architecture-review`
next over the files it named, and fold that result into the same report. Tell the user you are doing
this; do not silently widen the scope. Apply the same escalation when `kotlin-abi-review` reports that
the public surface is structurally unstable. If the user explicitly excluded architecture, recommend
it instead of running it.

## Rules

- Read-only. Do not edit code or tests during a review. Offer the fix as a next step.
- Never report a finding without its rule ID and title, a path, a line, and the code that shows it.
- A clean verdict is valid and should be common in healthy changes. Do not manufacture findings to
  fill the report.
- Do not restate the agents' full checklists in the output. Report what they found.
