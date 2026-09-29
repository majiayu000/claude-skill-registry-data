---
name: skills-validate
description: Use when explicitly asked to run a live or plan-only application test for a published Scenario skill.
license: MIT
metadata:
  internal: true
argument-hint: <skill-name> [--pr <number>] [--plan-only] [--task "..."] [--no-post] [--keep]
disable-model-invocation: true
---

Validate the skill named in the invocation arguments by having a fresh agent do real work with it, then report where that agent got stuck. A defect here is a defect in the skill text, never in the agent.

Flags: `--pr <number>` targets a PR instead of detecting one, `--plan-only` runs the zero-cost planning protocol from AGENTS.md instead of live generation, `--task "..."` supplies the use case instead of writing one, `--no-post` stops before publishing anything, `--keep` keeps the run directory.

Live runs spend Scenario credits. Keep every generation the smallest one that still proves the point.

## 1. Review the objective

Read the skill's `SKILL.md` and every file it links; `node scripts/lib/skills.mjs --dir <name>` prints its folder, nested under `skills/dcc/` or `skills/game-engines/` for an expert tool. If no skill has that name, list the close ones and stop.

State, in your own words: the objective (one sentence), the triggering conditions the `description` claims, and the three to six non-obvious facts the skill exists to teach, the ones an agent would otherwise guess wrong (upload flow, `jobs_wait` re-calls, `runs_as` wiring, dry runs, launch semantics). Those facts are the traps the run has to spring.

## 2. Write a concrete use case

One realistic task, in the words a user would actually use, that forces at least three of those traps and cannot be satisfied by generic MCP intuition (for an expert tool, generic knowledge of the application; its budget counts application runs, not generations). Give it explicit success criteria (which artifacts must exist, and what has to be true of them) and a hard budget (how many generations, which of them may be `dry_run`). Print the task and the criteria before spending anything. With `--task`, use the supplied task and still write the criteria.

## 3. Run the mechanical checks first

They are free and they catch the cheap failures: `pnpm spec` (spec validation), plus `pnpm test` when the skill ships a script. Record the results and continue either way; the report carries both layers.

## 4. Spin up the fresh agent

Build a run directory outside the repository and install the skill under test into it, from the working tree, so the run tests the version under review rather than the published one:

```bash
SKILL="<name>"
DIR=$(node scripts/lib/skills.mjs --dir "$SKILL")
RUN=$(mktemp -d "${TMPDIR:-/tmp}/skill-validate-$SKILL-XXXXXX")
mkdir -p "$RUN/.claude/skills" "$RUN/assets"
cp -R skills/scenario "$RUN/.claude/skills/"
case "$DIR" in
  skills/*/*/*) cp -R "${DIR%/*}"/scenario-* "$RUN/.claude/skills/" ;; # expert tool: its whole family
  *) cp -R "$DIR" "$RUN/.claude/skills/" ;;
esac
awk 'f; /^---$/ { if (++c == 2) f = 1 }' .claude/agents/skill-tester.md >"$RUN/contract.md"
```

Copy `scenario` alongside every other skill: real installs ship both. An expert tool brings its whole family, since the specialists import the lead skill's `scripts/`, and a live run needs the application installed: ask which machine and application version the run may drive, and ask for a team and project only when the task hands off to a Scenario skill. Otherwise, ask which team and project the run should use before spending anything: every generation and upload lands in that scope, and the tester must never pick one (`teams_list` and `projects_list` enumerate the choices). Write the task from step 2 to `$RUN/task.md`, including the budget, the success criteria, the run directory path, and the team and project.

Then pick the strongest isolation available. If the Claude Code CLI is installed, run `cd "$RUN" && claude mcp list`; otherwise use the subagent route below.

- **Separate process** (preferred, and a genuinely empty context) when that lists a connected Scenario server:

  ```bash
  cd "$RUN" && claude -p --setting-sources user,project \
    --append-system-prompt "$(cat "$RUN/contract.md")" \
    --allowedTools "mcp__<server> Read Write Bash" \
    --output-format json "$(cat "$RUN/task.md")" | tee "$RUN/result.json"
  ```

  Use the server name `claude mcp list` printed, normalized the way tool prefixes are: dots and spaces become underscores, so `claude.ai Scenario` is `mcp__claude_ai_Scenario`. The child loads the skills from `$RUN/.claude/skills/` and never sees this repository, though `--setting-sources user,project` (which a user-scope connector needs) also carries the user's plugins and hooks into it; watch the transcript for injected noise.

- **Subagent** when the CLI is unavailable or the list has no connected Scenario server. Spawn a fresh agent with the contract, the task, and the run directory path (Claude Code can use its `skill-tester` agent). Isolation is weaker: it can still see repository context, which is why the contract tells it to ignore it.

Say in the report which mode ran. With `--plan-only`, the same setup applies but the task asks for a numbered tool-call plan with exact tool names and argument shapes, executing nothing.

## 5. Grade the run

Fetch https://mcp.scenario.com/docs/tools fresh rather than recalling it, then judge. With `--plan-only`, judge the numbered plan by the same rubric: objective met asks whether the planned calls would reach the criteria, and the evidence table stays empty.

An expert tool is graded against its lead skill's execution channels and the application's own documentation instead of the tool reference: real names are the application's API, command, and UI names for the version the skill targets, the correct flow is the lead's loop (channel choice, stage gates, review renders or captures, audits), and the model-id and MCP bullets below do not apply.

- **Objective met.** The artifacts exist and satisfy the criteria from step 2. Open them; do not take the tester's word for it.
- **Real names only.** Every tool and parameter the tester used exists. One invented name is a fail.
- **Correct flow.** The loop the skill under test teaches. For a generation task that is discovery, `model_schema_get`, `model_run`, then `jobs_wait` re-called with `pending_job_ids` for any job still running (fast models return complete inline, and `job_get` polling is never correct), then `asset_display` or `asset_download`. Skills built on other loops (workflows, training, reporting) are graded against their own.
- **No constant generative model ids.** They came from a `recommend` step (a capability) or a `search` step (a member known by name, or private). A named first-party tool model is not a violation when it is a sanctioned singleton or the member the skill under test is dedicated to; a named generative model always is.
- **MCP for the agent's own steps.** The calls the tester made itself went through MCP tools. Reaching for the Scenario REST API, the official SDK, or a CLI in place of an MCP tool is a fail even when it produced the artifact, and inventing an API call to cover something MCP does not expose is a worse one: that gap belongs in the defects list. Running a script the skill ships is not a fail, whatever the script uses internally, and neither is saving a URL `asset_download` returned.
- **Traps handled** the way the skill teaches.
- **No guessing.** Anything asserted that appears in neither the SKILL.md nor the tool reference is a guess, even when it happens to be right. The tester's `guesses` and `friction` entries are the shortest route to the missing sentence.

Verdict: pass, pass with notes, or fail. Tie every defect to the exact line of SKILL.md to add or change. After a fix, re-run with a new fresh agent: an agent that already failed is contaminated by its own mistake.

## 6. Determine the context

`git rev-parse --abbrev-ref HEAD`, then look for an open PR with that head branch: `gh pr view --json number,url,title` when `gh` is available, otherwise the GitHub MCP tools (`list_pull_requests` with `head: <owner>:<branch>`). `--pr` overrides the detection. Say which context you found before acting on it.

## 7. Report

Assemble the report with the template below. This repository is public: only publicly shareable language (see AGENTS.md), never a signed asset URL, which is a credential in itself, and never the team or project the run used. Assets travel as ids and local filenames; surface the files in this session so they can be looked at or dragged into the thread.

**In a PR context**, post it as a PR comment (`gh pr comment <n> --body-file` or the GitHub MCP `add_issue_comment`), ending with the attribution line, and print the comment URL. `--no-post` prints the report here instead.

**With no PR**, ask what to do with it: open a tracker issue for the defects (the `scenario-report` skill covers the forms and the redaction rules), save it to a file, post it to a PR number they name, or leave it in this conversation. Post nothing until they pick.

Finally, delete the run directory unless `--keep` was passed, and say where the assets went if it survives.

```markdown
## Skill validation: `<name>` (<verdict>)

Objective: <one sentence>
Use case: <the task, one or two sentences>
Run: <separate process|subagent>, model <model>, commit <sha>, <UTC timestamp>

### Mechanical checks

| Check     | Result |
| --------- | ------ |
| pnpm spec |        |
| pnpm test |        |

### End to end

| #   | Tool | Outcome |
| --- | ---- | ------- |

Objective met: yes/no. <one sentence on what the agent produced>

### Evidence

| Artifact | Asset id | Job id | Model id | File |
| -------- | -------- | ------ | -------- | ---- |

### Defects

1. `<skill folder>/SKILL.md:<line>` <what the agent got wrong> -> <the sentence to add or change>

### Re-run

`/skills:validate <name>` after the fix, with a fresh agent.

---

_Generated by <agent name and verified model>_
```
