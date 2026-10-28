---
name: merge-review
description: Runs Logbook's review agents (bug-hunter, security-scanner, performance-auditor, design-reviewer, spec-keeper, upgrade-tester, deploy-checker, api-contract-checker, ai-evaluator, import-tester) on a branch, pull request or release and turns their reports into one clear MERGE or REJECT decision with the reasons and the shortest path to MERGE. Use this whenever Gareth asks "can I merge this", "is this ready", "review this PR / branch / phase", "should this go in", "pre-merge check", "release check", or invokes /merge-review — even if he names only one concern, since the point is the combined verdict. Never merges, pushes, approves or edits code.
---

# Merge review

Give the owner one defensible answer to "can this be merged?" by running
the review agents, checking their evidence and applying fixed rules. The
value is that the answer is **binary, consistent and explained**: the
same findings always give the same verdict, and every blocking reason
points to proof you re-ran.

You decide; you don't act. Never merge, push, approve a PR, resolve
threads or modify anything outside `var/`. Post the report as a PR comment
only when asked. Never run **test-writer** as part of the review: it
writes files (see step 7).

Read `.claude/review-rules.md` first. Its scope, ownership, severity
scale and report fields are what this skill relies on.

## 1. What's being reviewed

- **Branch mode** (default): the current branch against `origin/master`
  plus uncommitted work (review-rules §1). If the owner names a PR or
  branch, use that. If the diff is empty, ask.
- **Release mode** ("release check", "ready to tag"): everything since
  the last tag; every agent runs in full.
- Record the head SHA. The verdict is for that SHA only.
- List the changed files (`git diff --name-only origin/master...HEAD`);
  steps 2 and 3 depend on them.

## 2. Gates

Run these once, so no agent runs them again. Record pass/fail and the key
output.

| Gate | Command |
|---|---|
| Lint | `composer lint` |
| Static analysis | `composer analyse` |
| Tests, all engines | `bin/test-all-dbs.sh` (SQLite, PostgreSQL, MySQL, MariaDB). Without Docker: `composer test`, with the other engines **not run** |
| JS tests | `composer test:js` |
| Coverage floor | `composer test:coverage && composer coverage:check` |
| Changed-line coverage | `pipx run diff-cover var/coverage/cobertura.xml --compare-branch=origin/master --fail-under=80` |
| Built assets | `composer build-assets`, then `git status --porcelain public/assets` is empty |

The test suite also covers migrate → rollback → migrate on empty
databases. Paperwork (spec, docs, changelog, open questions) is
spec-keeper's, not a gate here.

## 3. Choose the agents

**Release mode:** all ten run, no skips.

**Branch mode:** run an agent when the diff touches its triggers. When in
doubt, run it — a skipped agent must be justifiable from the file list
alone.

| Agent | Runs when the diff touches |
|---|---|
| spec-keeper | **always** |
| bug-hunter | `src/`, `config/`, `db/`, `templates/`, `assets/js/`, `bin/` |
| security-scanner | `src/`, `config/`, `db/`, `templates/`, `assets/js/`, `bin/`, `public/`, `docker/`, `Dockerfile`, `composer.json`/`.lock`, `package.json`/`-lock` |
| performance-auditor | `src/`, `db/`, `templates/`, `assets/`, `config/` |
| design-reviewer | `templates/`, `assets/`, `translations/`, `public/assets/` |
| upgrade-tester | `db/migrations/`; code that reads or writes stored data (repositories, entities and value objects, settings stored as JSON, enums); backup and restore; `docker/entrypoint.sh` |
| deploy-checker | `Dockerfile`, `docker/`, `docker-compose*.yml`, `bin/`, `public/`, `config/settings.php`, `config/middleware.php`, `config/routes.php` or URL building, the service worker or manifest, `composer.json`/`.lock`, built assets |
| api-contract-checker | API or MCP code (actions, serialisers, tool definitions), `docs/api/openapi.json`, `docs/api.md`, `docs/mcp.md`, `config/routes.php`, CSV export code, webhook or notification payloads, the calendar feed, problem `code` values |
| ai-evaluator | AI code, prompts, tool definitions and descriptions, the grounding check, drafting, document reading, provider adapters, the MCP tools, or the services and repositories those tools call |
| import-tester | import or export code, `bin/import-app.php`, app readers, number, date or unit parsing, the fields of fill-ups, odometer readings, maintenance, documents or expenses, `tests/Fixtures/import/` |

A **docs-only** diff (`docs/`, `README.md`, `CHANGELOG.md`, phase files)
runs spec-keeper only, plus the gates.

Record every agent that doesn't run, with the rule that let it skip.

## 4. Run them

Give every agent the same brief: the scope, the head SHA, the gate
results from step 2 (so it doesn't run them), and a reminder that its
report must use review-rules §7.

- Launch the agents **in parallel** (one Task call each, in the same
  turn). They isolate their Docker stacks by compose project name and
  port (review-rules §2), so they can run together. If the machine can't
  cope, run the Docker-heavy ones (upgrade-tester, deploy-checker,
  performance-auditor, import-tester) one after another and the rest alongside.
- If an agent file is missing from `.claude/agents/`, that agent is
  **not run**.
- Collect each report in full, including *Not run* and *Handed over*.

## 5. Check the evidence

Agents can be wrong. Before a finding can block:

1. **Proof.** It needs a failing test, a reproducible request, a
   measurement, command output or a screenshot pair. Without one, move it
   to *Unconfirmed*. Unconfirmed findings never block.
2. **Re-run it.** For every finding that would block, run its proof
   yourself. If it doesn't reproduce, move it to *Unconfirmed* and say so.
3. **One finding per cause.** The same root cause reported by two agents,
   or reported by one and handed over by another, becomes one finding at
   the higher severity, listing both. If two agents rate the same cause
   differently, use the scale in review-rules §6 to settle it, and note
   the disagreement.
4. **New or already on master.** Take each agent's *New in this diff*.
   For every blocking finding marked `no` or `unknown`, check it on a
   scratch worktree of `origin/master` (`git worktree add
   var/merge-review/master origin/master`). A problem already on master
   blocks only if this diff **makes it worse or reachable in a new way**;
   otherwise it's a follow-up.
5. **Handed over, but not picked up.** If an agent handed something over
   to an agent that didn't run, treat it as unconfirmed and add that
   agent's skip to *Notes for the owner*.

## 6. Decide

The verdict is **REJECT** if any one of these is true; otherwise it is
**MERGE**.

**Gates**
- Lint, static analysis, JS tests or the test suite fails, on any engine.
- Coverage below the floor, or below 80% of changed `src/` lines.
- Built assets stale.

**Confirmed findings, new or made worse by this diff**
- Any **CRITICAL**, from any agent.
- Any **HIGH** from bug-hunter, security-scanner, spec-keeper,
  upgrade-tester, deploy-checker, api-contract-checker or import-tester.
- Any **HIGH** from ai-evaluator that is a **regression** against master
  in the deterministic pass. Live-pass results never block on their own;
  a consistent drop goes under *Notes for the owner*.
- Any **HIGH** from performance-auditor that is a **regression** against
  master.
- Any **HIGH** from design-reviewer that is an accessibility failure or
  makes a flow unusable (content hidden by overflow, broken without JS or
  by keyboard, status by colour alone, contrast).
- Upgrade-tester's verdict is **UNSAFE**.
- Three or more **MEDIUM** findings from one agent: a pattern, not a nit.

**Incomplete review** → **REJECT — review incomplete**
- An agent that step 3 says should run didn't, or its *Not run* covers
  something the diff touches (an engine, a proxy path, arm64 when the
  Dockerfile changed, screenshots when templates changed).
- A gate that couldn't run (for example the other engines without
  Docker).

An unverified change isn't a mergeable one. Say exactly what needs
running, and where (CI, another machine).

Everything else — MEDIUM and LOW findings, problems already on master,
unconfirmed findings, open questions, upgrade notes — goes in the report
and doesn't change the verdict.

Don't bend these rules on your own judgement. If you think one gives the
wrong answer for this diff, say so under *Notes for the owner* and still
give the verdict the rules produce. Overriding it is the owner's call.

## 7. Report

Save it as `var/merge-review/<branch>-<short-sha>.md` and show it in full,
in exactly this structure:

```markdown
# Merge review: <branch> @ <short-sha>

## Verdict: MERGE ✅ | REJECT ❌ | REJECT — review incomplete ⚠️

<One or two plain sentences saying why.>

## Blocking reasons
<Only when rejected. Numbered, most serious first. Each: the rule from
§6, the finding, where, the agent(s), and the proof you re-ran.>

1. **[CRITICAL · security-scanner] A member without cost access sees fuel costs through the API**
   Rule: CRITICAL finding. Where: src/Action/Api/FuelListAction.php:57.
   Also reported by: bug-hunter. Proof: `ApiCostVisibilityTest` fails on
   all four engines (re-run ✔).

## To get to MERGE
<Only when rejected. The shortest ordered list of things to do, each tied
to a blocking reason. No patches. End with: "Then run test-writer on
blocking reasons N, M to keep them fixed." Then list any scratch AI
cases and import files the agents said should be committed.>

## Gates
| Gate | Result |
|---|---|

## Agents
| Agent | Ran | C/H/M/L | Blocking | Notes |
|---|---|---|---|---|
| spec-keeper | ✅ | 0/0/1/2 | 0 | |
| upgrade-tester | ✅ SAFE WITH NOTES | … | … | 4 engines, 12 s on pgsql |
| deploy-checker | ⏭ skipped | – | – | no Docker, bin/, public/ or routing changes |
| … | | | | |

## Follow-ups (don't block this merge)
<Non-blocking findings grouped by agent, one line each with severity and
location. Problems already on master are marked "on master".>

## Upgrade notes
<From upgrade-tester, api-contract-checker and spec-keeper: what
CHANGELOG.md should tell self-hosters and integrators, or "None
needed".>

## Unconfirmed
## Open questions
<De-duplicated across agents, for docs/phases/open-questions.md. Not
decided here.>

## Notes for the owner
<Rules that may give the wrong answer here, disagreements between agents,
skips worth knowing about, what wasn't checked. Omit if empty.>
```

The verdict line, blocking reasons and *To get to MERGE* must make sense
on their own: the owner should be able to stop reading there and know
exactly what to do.

## Recording follow-ups

When this is the phase's final review, offer to run `/issue-sweep` on
this report, so the follow-ups and problems already on master are checked
by finding-reviewer and recorded in `docs/phases/known-issues.md`
(`CLAUDE.md` §12). Don't write that file from this skill.

## Re-reviews

After fixes, review the new head SHA from scratch; don't carry results
over. Add a *Since last review* line under the verdict: which blocking
reasons are resolved, which remain, and anything new.

## Clean-up

Remove `var/merge-review/master` and every agent's scratch folder
(`var/bug-hunter/`, `var/security-scanner/`, `var/performance-auditor/`,
`var/spec-keeper/`, `var/upgrade-tester/`, `var/deploy-checker/`, `var/api-contract-checker/`, `var/ai-evaluator/`,
`var/import-tester/`), except
screenshots in `var/design-reviewer/` that the report links to. Check no
`review-*` compose projects are left running (`docker compose ls`). Keep
the report.
