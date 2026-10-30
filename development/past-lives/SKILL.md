---
name: past-lives
description: Aang consulting his past lives (Roku, Kyoshi) for why things were decided. Use for why, /why, "why does X work this way", "why did we pick Y", design rationale, the history behind a regression, postmortem context, or where a threshold number came from. Queries every evidence source in parallel (source control, issue tracker, long-form docs, team chat, infrastructure observability, error tracking, analytics warehouse) and returns a cited, confidence-tiered answer. Use seismic-sense for how code works at runtime.
---

# Aang's past lives

When Aang needs to know why the world is shaped the way it is, he asks the Avatars who shaped it. Roku remembers the choices that led to the war. Kyoshi remembers the threats that made her strict. Each past life holds one part of the story, and none of them holds it all. Code is the same. It shows what it does, never why it exists. The why lives in commits, tickets, docs, chats, and alerts, each partial and sometimes wrong. Consult every past life you can reach, keep their voices separate, and say plainly what none of them remembers.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

`seismic-sense` answers what the code does and how it works. `past-lives` answers which forces led to its shape.

## Who answers

| Role | Character | Model from the avatar-setup sheet |
|------|-----------|-----------------------------------|
| Source control investigator | `team-avatar:toph` | the `toph` line |
| Every MCP-backed investigator | `team-avatar:sokka` | the `sokka` line |
| Synthesizer | `team-avatar:iroh` | the `iroh` line |

The sheet lives at `${CLAUDE_CONFIG_DIR:-~/.claude}/team-avatar-models.md` on Claude Code and `${CODEX_HOME:-~/.codex}/team-avatar-models.md` on Codex. A missing sheet or line means the default (`toph: sonnet`, `sokka: opus`, `iroh: opus`). A value of `inherit` means you omit `model`. A value with `@<level>` sets the Agent tool's `effort` parameter on Claude Code and `spawn_agent`'s `reasoning_effort` on Codex. If the Agent tool rejects a model, use the default and say so. Pick each dispatch's effort for the job, as the dispatch rules in `avatar-mode` describe.

Toph's tool list has no MCP access, so she takes only git and `gh`. Never send her an MCP-backed source. Sokka and Iroh keep full tool access so their MCP lookups and citation spot-checks work. Investigators still write nothing.

When you run as a subagent yourself, you cannot dispatch. Run each investigator's brief yourself, one source at a time, then synthesize. Say so in the answer.

## Posture

Work as a careful, cautious, and precise investigator. Be honest about what you know and what you infer. Read [references/epistemics.md](references/epistemics.md) for the full confidence framework and phrasing guide. The synthesizer must follow it.

## Step 1. Understand the target and the question

The **target** is usually a chunk of code, a pattern, a feature, or a named design decision. The **question** is usually a design rationale, a tradeoff, a motivating edge case, an external constraint, dead code, or a broad history sweep.

If the target is vague ("why do we do it this way?" with no clear referent), make your best guess from the conversation (open files, recent edits, what was just discussed). State your reading in one sentence so the user can redirect, then proceed.

## Step 2. Establish the code anchor

Before you dispatch anyone, build the seed context yourself. Collect file paths and line ranges, key symbols (functions, classes, constants), the last few commits touching the target, PR numbers from merge commits (the `(#1234)` pattern in the subject), and any linked ticket IDs.

```bash
git blame -L <start>,<end> <file>      # last-touch commits
git log --follow -p -- <file>          # full history with patches, through renames
git log --oneline -20 -- <file>        # recent commits with PR numbers visible
git log -1 --format=%B <commit>        # a commit body, for PR numbers
gh pr view <number> --json title,body,author,createdAt,mergedAt,labels,closingIssuesReferences,comments,reviews
```

Pull the PR body and discussion for every substantive commit. This anchor goes to every investigator and to the synthesizer.

## Step 3. Dispatch parallel investigators

Default to the full parallel investigation. The goal is a complete coverage map, not a minimal one. Document the null. Do not skip the search.

### Discovery

List the MCPs available in this session. Every MCP appears as a tool named `mcp__<server>__<name>` in the tool list. Failing that, read the project's `.mcp.json`, or run `claude mcp list` on Claude Code and `codex mcp list` on Codex.

Map each available MCP to one evidence category.

1. Source control history
2. Issue or ticket tracker
3. Long-form documents
4. Real-time team chat
5. Infrastructure observability
6. Error or exception tracking
7. Product analytics warehouse

Source control is always available through git and `gh`. For the other six, classify by the MCP's name, server instructions, tool names, and resource descriptors. If an MCP fits more than one category, pick the one that matches its primary evidence. Record ambiguous cases in the coverage map.

Dispatch one investigator per category that has a matching MCP, all in one message so they run concurrently, each owning exactly one tool or MCP. Never ask one investigator to cover several MCPs. Use `run_in_background: true`.

Each investigator's brief is [references/investigator-prompt.md](references/investigator-prompt.md) filled in, plus:

- the category playbook from [references/sources/](references/sources/) for the selected MCP, adapted from the examples in [references/source-playbook.md](references/source-playbook.md)
- [references/sources/incident-postmortem.md](references/sources/incident-postmortem.md) when the target code looks defensive (null checks, retry logic, timeout handling, rate limiting, feature flags, egress guards, OOM handlers)
- the code anchor and the user's original question

### The roster, one past life per evidence category

Each category is best at one shape of "why". Use this to know what to expect, to name the gap when a category returns empty, and only in the rare provably irrelevant case to justify a skip.

1. **Source control** (git history, `gh` for PRs, code comments, tests). Always dispatch. It is the only guaranteed source. Best at implementation-time rationale captured during review.
2. **Issue or ticket tracker** (Linear, Jira, GitHub Issues, Plane, Shortcut). Best at the product or business forcing function. Strongest when the why is external to engineering.
3. **Long-form documents** (Notion, Confluence, Google Docs, Coda). Best at design rationale written out before it became code.
4. **Real-time team chat** (Slack, Discord, Microsoft Teams, Mattermost). Best at deliberation that never reached a doc. Especially important when the source control, ticket, and doc trail is thin.
5. **Infrastructure observability** (Datadog, New Relic, Honeycomb, Grafana, Splunk). Best at the runtime reality that motivated the code. Strongest when the target reacts to an infra signal (timeouts, retries, rate limits, circuit breakers).
6. **Error or exception tracking** (Sentry, Rollbar, Bugsnag, Airbrake). Best at the specific exceptions that motivated defensive or corrective code. Strongest for catch blocks, null guards, type checks, and retries.
7. **Product analytics warehouse** (Databricks, Snowflake, BigQuery, ClickHouse, dbt, Redshift). Best at the product and data reality that shaped the code. Strongest for flag-gated code, experiment-driven ships, data migrations, and "where did this number come from".

### When to skip an investigator

Only with an explicit, written reason, which goes in the final Sources Consulted. Two reasons are valid.

- **No MCP is available for that category.** Flag it as a gap, not a choice. "Real-time team chat skipped. No matching MCP is available, so the conversational record was not searchable."
- **The source is provably irrelevant**, not just probably irrelevant. The bar is high. "Error tracking skipped. The target is a build-time script with no runtime code path."

For a single-commit target whose PR description already holds the complete answer, you may answer inline, but only after you confirm that every available category search would be redundant. Say so explicitly. This should be rare.

## Step 4. Synthesize

Dispatch one synthesizer. Its brief is [references/synthesizer-prompt.md](references/synthesizer-prompt.md) filled in, with:

1. every investigator's findings, including null results and each skipped category with its reason
2. the code anchor
3. the user's original question
4. the framework in [references/epistemics.md](references/epistemics.md)

## Step 5. Present

Present the synthesizer's output to the user. You may lightly edit for clarity or add context from the conversation. Never rewrite the confidence language.

## Output format

The structure is the one in [references/synthesizer-prompt.md](references/synthesizer-prompt.md). Its sections are The Question, The Code in Question, What We Found, What We Can Reasonably Infer, Competing Hypotheses, What We Don't Know, Sources Consulted, and Confidence Summary. Adapt as needed, but keep the confidence tiers separate. Keep Sources Consulted as one line per investigator, including each one that returned nothing or was skipped, with the reason.

When the user asks why as a step toward changing this code, add a constraint set after Sources Consulted. Convert the lineage findings into **Preserve**, **Change**, **Avoid**, and **Risk** lines for planning the change.

## Failure modes

- **Recency bias.** The most recent commit is not authoritative. The current shape is often the accretion of many earlier decisions. Trace back.
- **Embedded hypotheses.** "I assume it's for performance?" is one candidate, not the answer. Check it like any other.
- **Code as its own evidence.** Code is mechanics, not motivation. It never proves its author's intent.
