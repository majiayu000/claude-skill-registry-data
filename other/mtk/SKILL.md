---
name: mtk
description: Unified entry point that routes natural language requests to the right MTK skill
type: skill
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent, AskUserQuestion
argument-hint: <what you want to do>
user-invocable: true
---

# MTK — Unified Entry Point

You are a router. Classify the user's intent from their input, then load and follow the matching workflow skill inline. Do not do the work yourself — delegate by reading the target skill and following it end-to-end.

## Route Table

Match the user's input against these patterns. Check from top to bottom; first match wins.

**Order matters — do not "tidy" it.** `batch-fix` sits above `pre-commit-review` and `fix` on purpose: its multi-word phrases (`apply review findings`, `batch fix`, `several fixes`) contain those rows' single-word keywords (`review`, `fix`), so a lower position would let them shadow it. The PR-mining row sits above `pre-commit-review` for the same reason: "mine PR reviews" contains `review`. The code-review, brainstorming and spec rows sit above it too, so its bare `review`/`check`/`commit` cannot take "review PR 123", and `add`/`new`/`fix` lower down cannot take "how should we add…" or "write a spec for a new endpoint". The duplicates row sits high too: lower down, `add` (implement) or the bare `audit` (setup redirect) would take "find duplicate capabilities before I add another mapper" or "audit duplicates". The `converge` row sits above the setup redirect so the bare `principles` keyword cannot turn it into a full setup run. `scripts/run-fixtures.sh` simulates first-match-wins precedence and will fail if the order regresses.

| Pattern (keywords / intent) | Route to | Example inputs |
|---|---|---|
| `escalated from fix (batch)` (internal marker: fix found multiple independent fixes) | `.claude/skills/batch-fix/SKILL.md` | — internal self-escalation only |
| `escalated from fix`, `escalated from batch-fix` (internal markers from Scope Guards) | `.claude/skills/implement/SKILL.md` | — internal self-escalation only |
| `batch fix`, `apply findings`, `apply review findings`, `corrective batch`, `several fixes`, `multiple fixes` | `.claude/skills/batch-fix/SKILL.md` | "apply these review findings", "run a batch fix over these nits" |
| `audit duplicates`, `audit-duplicates`, `duplicate capabilities`, `find existing helper`, `find an existing helper`, `is there an existing helper`, `already have a helper` | `.claude/skills/prior-work-check/SKILL.md` | "audit duplicates", "find duplicate capabilities before I add another mapper" |
| `mine pr`, `pr mining`, `pr review mining`, `reviewer feedback`, `reviewers keep` | `.claude/skills/repo-health/SKILL.md` (PR-mining section) | "mine PR reviews", "what do reviewers keep repeating?" |
| `review pr`, `review the pr`, `review this pr`, `pr review`, `review pull request`, `review the pull request`, `review this branch`, `review the branch`, `review this diff`, `review the diff` | `.claude/skills/code-review-and-quality/SKILL.md` | "review PR 123", "review this branch before merge" |
| `brainstorm`, `explore approaches`, `explore alternatives`, `compare approaches`, `design options`, `how should we` | `.claude/skills/brainstorming/SKILL.md` | "brainstorm approaches for rate limiting", "how should we model refunds?" |
| `write a spec`, `write the spec`, `draft a spec`, `spec out`, `spec it out`, `spec only`, `just the spec` | `.claude/skills/spec-driven-development/SKILL.md` (spec only — it stops at approval; `/mtk:implement <spec path>` adopts it) | "write a spec for the export endpoint", "spec out the billing change" |
| `review`, `check`, `commit`, `staged`, `pre-commit`, `before I commit` (staged changes about to be committed; a PR, branch or diff review is the code-review-and-quality row above) | `.claude/skills/pre-commit-review/SKILL.md` | "review before commit", "check staged changes" |
| `repo-health`, `repo health`, `readiness`, `scorecard`, `ai-ready`, `ai ready`, `repo report` | `.claude/skills/repo-health/SKILL.md` | "is this repo AI-ready?", "run repo-health" |
| `doctor`, `install broken`, `integrity`, `install health` | `.claude/skills/mtk-doctor/SKILL.md` | "run mtk doctor", "is the install broken?" |
| `toolkit health`, `usage`, `stats`, `analytics`, `adoption` | `.claude/skills/mtk-doctor/SKILL.md` (`--usage`) | "toolkit health", "show usage stats" |
| `research`, `best practice`, `best-practice`, `current way`, `latest version`, `up to date`, `migration guide`, `upgrade guide` | `.claude/skills/research-context/SKILL.md` | "research the current EF Core batching approach", "what's the best-practice for X in v9" |
| `fix`, `bug`, `broken`, `error`, `typo`, `patch`, `wrong`, `failing` | `.claude/skills/fix/SKILL.md` | "fix the null check", "this test is broken" |
| `add`, `create`, `build`, `feature`, `implement`, `new`, `endpoint`, `refactor` (multi-file) | `.claude/skills/implement/SKILL.md` | "add user auth", "create a payment endpoint" |
| `status`, `what's loaded`, `context report`, `diagnostic`, `active config` | `.claude/skills/mtk-doctor/SKILL.md` | "what's loaded?", "show toolkit status", "context report" |
| `audit claude.md`, `claude.md audit`, `is claude.md still good`, `claude.md stale`, `memory rot`, `claude.md quality`, `audit agents.md`, `agents.md audit`, `instructions audit`, `audit instructions` | `.claude/skills/instructions/SKILL.md` (mode `audit`) | "audit AGENTS.md", "is CLAUDE.md still good?" |
| `capture claude.md`, `update claude.md`, `save what we learned`, `session learnings`, `remember this for next time`, `revise claude.md`, `capture instructions`, `instructions capture`, `update agents.md` | `.claude/skills/instructions/SKILL.md` (mode `capture`) | "save what we learned to AGENTS.md", "capture instructions from this session" |
| `promote lesson`, `promote this lesson`, `share lesson`, `share this lesson` | `.claude/skills/lessons/SKILL.md` (mode `promote`) | "promote this lesson to the team", "share that lesson" |
| `mine lessons`, `what did we learn`, `harvest lessons`, `lesson sweep`, `mine transcripts` | `.claude/skills/lessons/SKILL.md` (mode `mine`) | "mine lessons from last week", "what did we learn this sprint?" |
| `refresh lessons`, `audit lessons`, `stale lessons`, `prune lessons`, `clean up lessons` | `.claude/skills/lessons/SKILL.md` (mode `refresh`) | "are the lessons stale?", "clean up lessons.md" |
| `capture this lesson`, `capture a lesson`, `capture lesson`, `record this lesson`, `golden path`, `correction capture` | `.claude/skills/lessons/SKILL.md` (mode `capture`) | "capture this lesson", "record this lesson for the team" |
| `hand off`, `handoff`, `save state`, `snapshot session`, `resume`, `pick up`, `continue from handoff` | `.claude/skills/handoff/SKILL.md` | "hand off to a teammate", "save state before I stop" |
| `converge`, `convergence`, `principle drift`, `drift from the principles`, `drifted from the principles` | `.claude/skills/mtk-setup/SKILL.md` (direct the user to `/mtk-setup --check`) | "converge", "where has the code drifted from the principles?" |
| `setup`, `bootstrap`, `init`, `initialize`, `first time`, `prepare repo`, `audit`, `architecture`, `principles` | `/mtk-setup` (direct the user) | "set up this repo", "audit this repo" |
| `help`, `commands`, `what can you do` | (print help below) | "help", "what commands are there?" |

## Route Disambiguation (negative boundaries)

Positive keyword matches collide on adjacent intents. These boundaries say when not to take
the obvious route — encoding the contested pairs measurably cuts misroutes.

| Route to… | …not… | …when |
|---|---|---|
| `fix` | `implement` | the change is 1–3 files with no new public contract; if it's feature-sized it's `implement`, if it's several small independent fixes it's `batch-fix` (ambig branch → ask once) |
| `batch-fix` | `fix` | the batch is more than 3 files OR multiple distinct independent fixes — too big for the single-change `fix` loop. A purely mechanical sweep past 3 files is no exception: it runs in batch-fix's mechanical mode |
| `batch-fix` | `implement` | the batch introduces no new public contract and no architecture; a finding that needs one escalates THAT finding to `implement` |
| `batch-fix` | `pre-commit-review` | the ask is "apply review findings" / "apply the review comments" — running the corrective-batch loop, not a staged-changes security gate; batch-fix's row sits above `pre-commit-review` so `review` cannot shadow it |
| `repo-health` | `pre-commit-review` | the ask is "mine PR reviews" / recurring reviewer feedback — repo-health's suggest-only PR-mining section, not a review of staged changes |
| `research-context` | `implement`/`fix` | the ask is an external/best-practice/version question ("what's the current way to…"), not a change to this repo |
| `pre-commit-review` | `code-review-and-quality` | the trigger is staged/about-to-commit; full PR/branch review is the workflow skill, not the pre-commit gate |
| `mtk-doctor` | `mtk-doctor --usage` | the ask is install health or "what's loaded right now"; usage/adoption/analytics over time is `--usage` |
| `instructions` (`capture`) | `handoff` | the target is AGENTS.md/CLAUDE.md content; capturing session state to resume later is `handoff` |
| `instructions` (`capture`) | `lessons` (`capture`) | the finding is a fact about this repo (a command, a path, an env quirk) that belongs in the constitution; a reusable rule from a correction or a dead end is a lesson |
| `lessons` (`promote`) | `lessons` (`mine`) | a specific known lesson goes native memory → team; sweeping transcripts for candidates is `mine` |
| `lessons` (`refresh`) | `lessons` (`mine`) | auditing/retiring EXISTING lessons is `refresh`; harvesting NEW candidates from transcripts is `mine` |
| `prior-work-check` | `implement`/`code-simplification` | the ask is whether a capability or helper already exists ("audit duplicates", "find existing helper") — a read-only search of CODE_INDEX, skills and helpers, not a change or a cleanup |
| `/mtk-setup` | `implement`/`fix` | anything setup/bootstrap/audit/architecture-principles — always redirect to `/mtk-setup`, never absorb. Code drifting from the agreed principles ("converge") is `/mtk-setup --check`. Exceptions: `audit duplicates` (prior-work-check), `audit lessons` (lessons refresh) and `audit agents.md`/`audit claude.md` (instructions audit) are not setup |

## Routing Rules

1. **Strip flags first.** If the input starts with `--terse`, `--verbose`, `--staged-only`, `--preview`, `--merge`, `--non-interactive`, `--usage`, pass them through to the target skill.
2. **Unambiguous → route silently.** If the input matches exactly one row of the table, invoke immediately — no confirmation question.
3. **Escalation marker → route by marker (most specific first).** If the input contains `escalated from fix (batch)`, route to `batch-fix`. Otherwise, if it contains `escalated from fix` or `escalated from batch-fix`, route straight to `implement`. These markers are produced only by the `fix` / `batch-fix` Scope Guards.
4. **Ambiguous → ask, but only if genuinely ambiguous.** If input matches two rows with similar specificity (e.g., "fix the auth feature" — fix verb + feature-sized noun), ask one clarifying question: "Is this a small fix (1-3 files), a batch of small independent fixes, or a larger feature?" Do not ask for inputs that clearly match one row.
5. **No input → help.** If invoked with no argument, print the help text.
6. **Pass description through.** When loading the target skill, treat the user's original description as the task input — don't summarize or rephrase.
7. **Setup requests → redirect.** If the user asks for setup/bootstrap/audit, tell them to run `/mtk-setup` directly (with appropriate flags) rather than routing through mtk. An `audit` that matched an earlier row (`audit duplicates`, `audit lessons`, `audit agents.md`, `audit claude.md`) is not a setup request; `converge` goes to `/mtk-setup --check`.

## Help Output

When the user asks for help or provides no input, respond with:

```
MTK — entry points:

  /mtk-setup                     → first-time setup (bootstrap + audit)
  /mtk-setup --audit             → re-run architecture audit
  /mtk-setup --merge             → merge multi-repo audits
  /mtk-setup --refresh           → drift-scoped refresh of all generated docs (--dry-run to preview)
  /mtk-setup --check             → read-only CI staleness gate + drift from the agreed principles
  /mtk-setup --update-guidelines → bump the pinned coding-guidelines SHA
  /mtk-doctor                    → install health check (--json, --fix, --usage)
  /lessons <mode>                → capture | mine | refresh | promote team lessons

  /mtk <description>             → everything else:
    /mtk review before commit      → pre-commit security review
    /mtk repo-health               → AI-readiness checklist + PR review mining
    /mtk fix <description>         → small fix (1-3 files)
    /mtk apply these findings      → batch-fix: several small independent fixes, one gate
    /mtk <feature description>     → full implementation workflow
    /mtk research <question>       → cited brief, grounded in this repo's versions
    /mtk audit AGENTS.md           → instructions audit (capture: "save what we learned")
    /mtk status                    → mtk-doctor: what's loaded and healthy
    /mtk usage stats               → mtk-doctor --usage

Update: MTK is distributed as a Claude Code plugin — use the plugin
manager to update rather than an in-repo update skill.
```

## Execution

Once matched, resolve the MTK root once per `.claude/references/mtk-file-resolution.md` and state it as a single line — `MTK_ROOT=<path>` — so the dispatched skill does not re-resolve. On a plugin install the path is `${CLAUDE_PLUGIN_ROOT}` (substituted into this text at load time; it is not a Bash environment variable). Then read the target skill file and follow every step of that workflow. Do not summarize; do not skip verification. The target skill owns its own acceptance criteria.

If the route is `/mtk-setup` (setup family, including the `converge` row, which maps to `--check`), tell the user:

> "Setup lives at `/mtk-setup` — run that directly. Flags: `--audit` re-audits only, `--merge` unifies multi-repo audits, `--refresh` drift-refreshes all generated docs (`--dry-run` previews), `--check` is the read-only staleness gate, `--preview` shows planned changes, `--non-interactive` skips interview."

Do not add preamble or commentary before routing. Just route.
