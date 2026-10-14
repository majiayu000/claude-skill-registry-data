---
name: ticketing-skill
description: >-
  Ticket lifecycle for GitHub Issues and JIRA — create, start (in-progress),
  classify/label, update from commits, close (post-merge, idempotent),
  ticket-key↔branch plumbing. CRUD only: no branches, PLANs, execution.
  Triggers: any ticket/issue create·start·label·update·close, bug report,
  feature request.
license: Apache-2.0
compatibility: opencode
category: Git/Workflow
---

Consolidates `ticket-creation-skill`, `git-issue-labeler-skill`,
`git-issue-updater-skill`, `jira-git-integration-skill`,
`jira-status-updater-skill`, `jira-ticket-labeler-skill` (#599).

## What I do

Ticket CRUD and classification on GitHub Issues or JIRA — nothing else:

1. **Detect Platform** (§Platform Detection) — GitHub or JIRA
2. **Route the lifecycle op** (§Lifecycle): create · classify/label · start · update · close · git plumbing
3. **Load the platform values** (`references/github.md` / `references/jira.md`)

Branch creation, PLAN generation, execution, and release/versioning belong to
`worktree-pipeline-skill` (`/run-worktree-pipeline`) and
`semantic-release-convention-skill` — never here.

## Side files (load rules)

| Read | When | Use |
|------|------|-----|
| `references/github.md` | resolved platform is `github` | gh commands, 3-tier tooling fallback, label vocabulary + LABELS array, semver rule, `#N` key format, templates contract |
| `references/jira.md` | resolved platform is `jira` | MCP discovery workflow, REST endpoints, type/priority vocabulary, transitions, `PROJ-123` key format, description templates |

Side files carry VALUES only; this file carries the METHOD. An unknown
platform (Linear, Azure Boards, …) → detect-and-ask; if
`references/<platform>.md` does not exist, report the platform as
unsupported and suggest contributing a side file — never improvise endpoints.

## Platform Detection

Resolve in priority order — explicit beats inferred, inferred beats asked:

1. **Explicit**: user names a JIRA key (`PROJ-123`) or says JIRA → `jira`;
   names `#123` / "GitHub issue" / "create issue" → `github`.
2. **Repo signals**: ticket key format in branch/commits; for JIRA, ONLY if
   `atlassian_*` tools exist in the tool list (see §MCP Availability Guard) —
   tools absent means JIRA is unavailable: run the GitHub flow and report
   JIRA steps as skipped, never hallucinate `atlassian_*` calls.
3. **Ambiguous** ("create ticket"): ask once — "Which platform? GitHub Issues
   (default) / JIRA" — then proceed. One ask per run.

Before any GitHub operation, resolve the **tooling tier**
(`references/github.md` §Tooling fallback): `gh` present → full CRUD; missing
→ prompt the user to install (`gh-cli-setup-skill`); declined → git-only tier
with its honest per-operation limits.

## Lifecycle

### Create

The agent runs the same intake a human runs in the browser issue form. Never
invent field values; ask for what is missing.

**Stage 1 — Classify.** Variant from content: `bug` (broken, reproducible →
bug template, repo form `.github/ISSUE_TEMPLATE/bug_report.yml`) or
`feature`/`task` (new capability or contained work → feature template).
Final type/label resolution happens at classify/label below; the variant here
selects the template.

**Stage 2 — Intake.** Batch one question round for every required field
missing from the request. Field labels are canonical — they match
`templates/` verbatim so agent-created and human-created tickets are
structurally identical.

*Bug variant* (mirrors `bug_report.yml`): Title (≤72 chars, required) ·
Problem description (required) · Steps to reproduce (numbered, required) ·
Expected vs Actual (one line each, required) · Environment (OS/Node/opencode
version + install method, required) · Logs/screenshots (optional) ·
References (optional).

*Feature/Task variant* (mirrors `feature_request.yml`): Title (≤72, required)
· Problem/use case (required) · Proposed solution (required) · Alternatives
considered (optional) · Acceptance criteria (required, definition of done) ·
Scope (required, agent flow only — flows to the PLAN, never the browser form)
· References (optional).

**Stage 3 — Validate.** Required fields non-empty. Missing required → ask,
not guess. Each sub-item in a multi-ticket run gets its own intake round; a
sub-item without acceptance criteria fails validation.

**Stage 4 — Preview.** Render title + body, show the user for confirmation
or edits before any creation call.

**Stage 5 — Submit.** After confirmation, create per the platform side file
(gh commands / MCP-REST flow). Prefix titles with the form's `title` prefix
(`[Bug]: ` / `[Feature]: `) so agent- and form-created tickets match triage
filters.

**Rendering schema** — one canonical schema, two renderings; variant selects
sections; sections mirror the form headings. GitHub bug body: `### Problem
description` / `### Steps to reproduce` / `### Expected vs Actual` /
`### Environment` / `### Logs / screenshots` / `### References`. GitHub
feature body: `### Problem / use case` / `### Proposed solution` /
`### Alternatives considered` (omit if none) / `### Acceptance criteria`
(checklist) / `### References`. JIRA description mapping per
`references/jira.md` §Description templates.

**Scope**: single ticket vs parent with sub-issues/subtasks — ask. Parents
get body-ref linking (`Parent: #N`) on GitHub; native subtasks on JIRA.

**Sequence handoff** (multi-ticket runs only): end with the executable
tickets in suggested order for `/run-worktree-pipeline`, one-line rationale
per position; order derivation = user-stated dependencies > user-given order
> content inference (always labeled "inferred"); omit the umbrella parent.
When the user states dependencies, write `blocked-by: <ref>` as a plain body
line under a `### Dependencies` heading in the DEPENDENT ticket (bare refs:
`#458`, `PROJ-123`, `owner/repo#458`) so the pipeline's skip-guard enforces
the order. Editing an existing body: fetch, append, write back — body edits
REPLACE, never blindly append.

### Classify / Label

Keyword + semantic analysis — keywords are intent signals, not substring
matches ("add" in "address" is not an enhancement); analyze title AND body;
check negations; explicit requests differ from questions; comments may carry
deciding context. Low confidence → leave unlabeled (or `enhancement`) and
comment a clarification request.

**Structural rules (method):**
- Issues get type + priority labels/fields; **PRs get exactly one semver
  label** derived structurally from the PR title's Conventional Commit prefix
  (`feat!`→major, `feat`→minor, else patch) — never from issue content.
  Semver definitions follow `semantic-release-convention-skill` — cited,
  never redefined. Tagging/version-bump are release tooling's job, not this
  skill's.
- Exactly one priority per issue; max 3 labels (type + priority + one
  auxiliary).
- Auto-create missing labels first (GitHub) — never fail on a missing label.

Vocabularies, keyword tables, LABELS arrays, GitHub↔JIRA mappings:
`references/github.md` §Label vocabulary, `references/jira.md` §Vocabulary.

### Start (execution begins)

When implementation of a ticket begins — the pipeline's worktree-creation
boundary; `worktree-pipeline-skill` Step 4 is the canonical caller:

1. **Check current status first** — already in-progress or beyond
   (done-category) → skip the transition. This is the check-first guard,
   mirroring §Close's transition-once rule.
2. **Transition** to the in-progress-category target: JIRA per
   `references/jira.md` §Transitions; **GitHub = no-op with a note** —
   issues have no status field; close-on-merge rides `Closes #N`.
3. **Honest state**: a ticket that fails, halts, or stays held mid-run
   legitimately remains In Progress — work started; never revert it to
   mask a failure.

Never block the calling workflow on this op (§MCP Availability Guard
applies — JIRA unavailable → report the transition skipped).

### Update (commit progress)

After pushing commits that reference a ticket (and before PR creation, to
keep the tracker current):

1. **Latest commit**: `git log -1 --format='%H %an %aI %s'`; files via
   `git diff-tree --no-commit-id --name-only -r HEAD`.
2. **Determine the ticket ref** — never guess: GitHub `#(\d+)` in the commit
   message first; then JIRA `[A-Z]+-\d+`; then branch name (`123` → `#123`,
   `PROJ-123` → JIRA); else ask the user.
3. **Post one progress comment** in the house template below (GitHub via gh;
   JIRA per §MCP Availability Guard / side-file endpoint).
4. **Idempotency**: one comment per commit push — skip if a comment matching
   that commit hash already exists.

House comment template — same shape every update so progress is diffable:

```markdown
## Progress Update - <YYYY-MM-DD at HH:mm (UTC offset)>

### Changes Made
- <subject-line bullets from commits>

### Statistics
- **Commits**: <n> · **Files changed**: <n> (+<adds>/−<dels>)

### Commit Link
- [<short-hash>]($REPO_URL/commit/<sha>) — <subject>

### Files Changed
- <paths>
```

Rules: real user + timestamp from `git log`, never invented; no editorializing.

### Close (post-merge)

After a PR merges, transition its tracker ticket **exactly once** and add a
merge comment. Driven by `worktree-pipeline-skill` / the PR merge flow —
never by PR creation itself.

1. **Detect the ticket ref** from the merged PR: title/body key patterns,
   branch name, or commit footers (`gh pr view <num> --json
   title,body,headRefName`). No key found → report and stop (never guess).
2. **Check current status first** — already done-category → skip the
   transition, still add/verify the merge comment. This is the
   transition-once guard.
3. **Transition** to the done-category target (pick priority and endpoints
   per the side file); add the merge comment (template below).
4. Failure isolation: a comment failure must not trigger a second transition
   attempt; log and continue where possible.

```markdown
## Pull Request Merged
### Status Update
- **Previous**: <from> → **New**: <to>
### Merge Details
- **PR**: #<num> — <title> (<merge SHA>)
### Files Changed
- <summary or count>
```

### Git plumbing (ticket keys ↔ branches ↔ commits)

The general rule: the ticket key rides the branch name first (parses back out
trivially) and the commits carry it in footers (`Refs: <key>` to reference,
`Closes: <key>` to close on merge) — this feeds §Update and §Close detection
and the plan-file conventions downstream skills consume. Per-platform key
formats and branch patterns: side files (`github.md` §Ticket key format,
`jira.md` §Ticket key format & git plumbing).

## MCP Availability Guard

**Canonical policy home** — other skills' §MCP Availability Guard sections
point here; edit the policy only in this file.

The `atlassian` MCP server is **disabled by default** (opt-in). Before any
`atlassian_*` call, check whether the tools exist in your tool list:

- If `atlassian_*` tools are absent, do NOT attempt or hallucinate them.
- Interactive: offer per-project enable via `opencode-repo-setup-skill`
  (writes the FULL atlassian server entry into the project `opencode.json` —
  a bare `{"disabled":false}` stub is inert; effective next session, so this
  session must degrade).
- Fallback: REST with an API token — `curl -u email:token` against
  `https://<site>.atlassian.net` (discover cloudId unauthenticated: `curl
  https://<site>.atlassian.net/_edge/tenant_info`); scoped tokens use
  `api.atlassian.com/ex/jira/{cloudId}`, unscoped use site-direct
  `/rest/api/3/`.
- No credentials/headless: report the JIRA operation as skipped — never block
  the calling workflow.

GitHub-side operations are unaffected (gh or git per the tooling tier).
Per-operation REST endpoints: `references/jira.md` §REST fallback endpoints.

## Attribution (author/assignee)

- **GitHub**: the issue author is the `gh auth` user by construction (token
  owner — GitHub does not allow spoofing); `--assignee @me` self-assigns the
  same identity. `git config user.name`/`user.email` are NOT valid assignee
  sources (display name, not a login; email may be a private noreply
  address).
- **JIRA reporter**: defaults to the account behind the MCP token / REST
  credentials — automatic, no field needed.
- **JIRA assignee**: must be set explicitly by `accountId` (JIRA never
  assigns by display name or email):
  1. Fetch own accountId: REST `curl -u email:token
     https://<site>.atlassian.net/rest/api/3/myself` → `.accountId` (on
     Atlassian MCP v2, `atlassianUserInfo`/`lookupJiraAccountId` are the
     MCP-native equivalents).
  2. Set assignee: REST `PUT /rest/api/3/issue/{key}/assignee` with
     `{"accountId": "<id>"}` — the only guaranteed path; works from the
     §MCP Availability Guard REST fallback.
  3. `atlassian_createJiraIssue` (v1, pinned) assignee parameter:
     **unverified — server absent** (2026-09-19 static inspection:
     Atlassian's supported-tools page documents v2 only — there the create
     tool is `createJiraIssue` with no published per-parameter schema and
     `editJiraIssue` is the documented field-edit path; the pinned v1 schema
     is not statically published). Re-inspect live when a project enables
     the atlassian MCP; until then use the REST PUT above, or MCP v2
     `editJiraIssue` where v2 is enabled.

## Boundaries

**Ticket-vs-plan** (this skill is upstream of `worktree-pipeline-skill`):

1. A ticket must be executable by someone who never saw the discussion —
   anything less belongs in comments, anything more belongs in the PLAN.
2. Every PLAN references exactly one ticket ID; the ticket's Acceptance
   Criteria become the PLAN's definition of done. The plan inherits AC; it
   never rewrites them.
3. Technical Notes (implementation considerations) belong to the PLAN, never
   the ticket body.

**Workflow skills stay external**: `worktree-pipeline-skill`,
`wayfinder-skill`, `dev-uat-promotion-skill` consume this skill; their
orchestration is never part of it.

## Agent behavior rules

- **Ask, don't invent**: missing required field → batched question round.
- **Search first**: search existing tickets before submit (the agent-side
  equivalent of the form's search-first attestation).
- **Parity of required-ness**: the required set equals the form's
  `validations.required`.
- **Headless/CI**: no asks — proceed only if every required field came in the
  original request; otherwise fail naming the missing fields.

> **Harness binding — interactive prompts** (AGENTS.md §Portability
> contract): OpenCode — `question` tool. Claude Code — `AskUserQuestion`.
> Other/none — batch the same fields in a plain reply; proceed per the
> Headless/CI rule if no answer comes.
