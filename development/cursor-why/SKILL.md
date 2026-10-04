---
name: cursor-why
description: "Use for 'why does X work this way', 'why we picked Y', design rationale, regressions, postmortems, or data-backed thresholds. Discovers authorized read-only sources through native tools, CLI or MCP and queries each evidence category (source control, issue tracker, long-form docs, real-time chat, infrastructure observability, error tracking, product analytics warehouse) in parallel, then returns a cited read on decisions and tradeoffs. Use how for runtime behavior."
---

## Codex runtime mapping

Use the connectors and read-only scopes actually available in this Codex task. Preserve the seven-category coverage map, source investigators, null results, epistemic framework, citation checks and synthesis. Native model/effort follows the standing `model-capability-router`; delegation does not grant source or write authority. The pinned Cursor skill says readonly mode strips MCP access; current official Cursor Subagents documentation describes readonly as restricting writes and separately says local subagents inherit MCP tools. Treat the source claim as unverified policy, not a platform contract or a reason to grant Codex write access.
Before each connector query, verify read-only access in this task; do not request write scope, relay credentials, or send messages. Treat denial as unavailable evidence, not permission to switch tools or infer the answer.

# Why

Investigate the motivation and intent behind code.

Companion to the `how` skill. `how` answers what the code does and how it works. `why` answers what forces led to its shape.

For each delegation, choose the model and effort through the standing `model-capability-router` and the native Codex inventory. Respect the operator's selection. If a requested model is unavailable, report the exact gap; do not invent a replacement slug.

## Operating Posture

Operate as a **careful, cautious, and precise investigator**. Be honest about what you know vs what you're inferring. Read `references/epistemics.md` for the full confidence framework and phrasing guide. The synthesizer must follow it.

## Step 1. Understand the Target and the Question

Parse what the user is asking. The **target** is usually a chunk of code, a pattern, a feature, or a named design decision. The **question** is usually a design rationale, a tradeoff, a motivating edge case, an external constraint, dead code, or a broad history sweep.

If the target is vague ("why do we do it this way?" with no clear referent), make your best guess from conversation context (open files, recent edits, cursor location, what was just discussed). State your interpretation briefly so the user can redirect if you're off, then proceed.

## Step 2. Establish the Code Anchor

Before spawning investigators, anchor the investigation in concrete code. You need:

- The relevant file path(s) and line range(s)
- The key symbols (function names, class names, constants)
- An initial commit list. The last few commits touching the target.
- PR numbers from merge commits (pattern `(#1234)` in the subject line)

Build this inline.

```bash
# Blame target lines for last-touch commits
git blame -L <start>,<end> <file>

# Full file history, with patches, through renames
git log --follow -p -- <file>

# Last N commits touching the file, PR numbers visible
git log --oneline -20 -- <file>

# Extract PR numbers from a commit message
git log -1 --format=%B <commit>
```

Pull PR bodies and discussion via `gh` for any substantive commits:

```bash
gh pr view <number> --json title,body,author,createdAt,mergedAt,labels,closingIssuesReferences,comments,reviews
```

Capture this as seed context (file paths, symbols, commits, PR numbers, linked ticket IDs). Pass it to the investigators.

## Step 3. Spawn Parallel Investigators (default posture)

**Default to the full parallel investigation.**

### Discovery

Before spawning investigators, inventory the MCP tools and resources actually exposed in this Codex task. Use native tool discovery and resource listings; do not infer installed connectors from names or inspect a Cursor `mcps/` directory. Record unavailable categories.

Map each verified read-only source/tool to one evidence category:

1. Source control history
2. Issue / ticket tracker
3. Long-form documents
4. Real-time team chat
5. Infrastructure observability
6. Error / exception tracking
7. Product analytics warehouse

Local source history is available when the target is a Git checkout; `gh` requires a configured remote and access. Verify both before claiming source-control or PR coverage. For the other six, inspect available native tools, CLIs, connectors and MCP resources, including their actual access and instructions. Classify by the evidence returned, not product name alone. If a tool spans categories, assign the source to each category it can actually answer and record overlap or ambiguity in the coverage map.

Aim for a complete **coverage map**, not a minimal one. Document the null, don't skip the search.

Launch independent investigators concurrently when delegation and source access are authorized. Give each a bounded source category and do not let a single report conceal a category that was never searched.

- Use available native Codex subagents when delegation is authorized. Select model and effort under the standing `model-capability-router` policy. Give each investigator only the tools and source scope it needs; prohibit writes and external messages. If a connector is unavailable to subagents, investigate that category in the coordinator and record the actual access path.

Each investigator gets:
1. The base prompt from `references/investigator-prompt.md`
2. The category playbook `references/sources/<source>.md` for the selected source/tool, adapted from the examples in `references/source-playbook.md`
3. The cross-cutting `references/sources/incident-postmortem.md` **if the target code looks defensive** (null checks, retry logic, timeout handling, rate limiting, feature flags, egress guards, OOM handlers)
4. The code anchor from Step 2 (file paths, symbols, commit hashes, PR numbers, ticket IDs)
5. The user's original question

### Investigator roster. One per available evidence category

Use one investigator per category with a verified authorized source, or search that category directly when native delegation cannot access it. Each owns a named source and records its access path.

Each entry names the category and the kind of "why" it uniquely surfaces. Use it to know what to expect back, how to name a gap when a category returns empty, and (only in the rare provably-irrelevant case) to justify a skip.

1. **Source control investigator**. Local Git history; `gh` for PRs only when a remote and access exist. Investigate directly if native delegation is unavailable. The only guaranteed source. Best at surfacing *implementation-time rationale captured during review*.

2. **Issue / ticket tracker investigator** (e.g. Linear, Jira, GitHub Issues, Plane, Shortcut MCP). Best at surfacing *the product or business forcing function*. Strongest when the why is external to engineering.

3. **Long-form documents investigator** (e.g. Notion, Confluence, Google Docs, Coda MCP). Best at surfacing *long-form design rationale*. Where the why is written out before it becomes code.

4. **Real-time team chat investigator** (e.g. Slack, Discord, Microsoft Teams, Mattermost MCP). Best at surfacing *real-time deliberation that never reached a doc*. Especially important when the source control, ticket, and doc paper trail is thin.

5. **Infrastructure observability investigator** (e.g. Datadog, New Relic, Honeycomb, Grafana, Splunk MCP). Infra/runtime view. Best at surfacing *infrastructure and runtime reality that motivated the code*. Strongest when the target reacts to an infra signal (timeouts, retries, rate limits, circuit breakers).

6. **Error / exception tracking investigator** (e.g. Sentry, Rollbar, Bugsnag, Airbrake MCP). Best at surfacing *the specific exceptions and error trajectories that motivated defensive or corrective code*. Strongest for catch blocks, null guards, type checks, retries, and other defenses.

7. **Product analytics warehouse investigator** (e.g. Databricks, Snowflake, BigQuery, ClickHouse, dbt, Redshift MCP). Product/data view. Best at surfacing *product and data reality that shaped the code*. Strongest for flag-gated code, experiment-driven ships, data migrations, and "where did this number come from" questions.

### When to skip an investigator

Only skip with an **explicit, written justification** that goes in the final "Sources Consulted" section. Two valid reasons:

- **No authorized read-only source is available for that category** in this environment. Check native tools/CLI and MCP resources before calling it unavailable. Flag the gap, not a negative result. Example: "Real-time team chat skipped. No authorized chat source was accessible, so the conversational record was not searched."
- **The source is provably irrelevant**, not just "probably irrelevant." A high bar. Example: "Error / exception tracking skipped. Target is a build-time script with no runtime code path."

If a single-commit trivial target has a PR description containing the complete answer, you may answer inline after checking that available additional categories cannot change the claim. Record which categories were actually assessed and which were unavailable. Say so explicitly. This should be rare.

## Step 4. Synthesize

- Use an available native Codex synthesizer subagent when authorized, with model and effort chosen under the standing `model-capability-router` policy. Provide read-only source access required for spot checks; otherwise synthesize and verify citations in the coordinator.

The synthesizer gets:
1. The investigator findings, including any null results and any categories skipped with justification
2. The code anchor from Step 2 (file paths, symbols, commit hashes, PR numbers, ticket IDs)
3. The user's original question
4. The epistemics framework from `references/epistemics.md`
5. The synthesizer prompt template from `references/synthesizer-prompt.md`

## Step 5. Present

Spot-check the synthesizer’s citations and present the supported result. Correct factual errors while preserving the distinction between observed facts, inferences and unknowns; the coordinator owns the final answer.

## Output Format

The output structure is the one in `references/synthesizer-prompt.md`: The Question, The Code in Question, What We Found, What We Can Reasonably Infer, Competing Hypotheses, What We Don't Know, Sources Consulted, Confidence Summary. Adapt as needed, but keep the confidence separation intact, and keep Sources Consulted as one line per investigator, including the ones that returned nothing or were skipped, with the reason.

After the Sources Consulted block, if the user's `why` question is a precursor to actually changing this code, convert the lineage findings into a Preserve / Change / Avoid / Risk constraint set suitable for planning the change.

## Common Failure Modes to Avoid

- **Recency bias**. Assuming the most recent commit is authoritative. The current shape is often the accretion of many earlier decisions. Trace back.

## Reference Files

- `references/epistemics.md`. Confidence tiers and phrasing guide. The synthesizer must follow it.
- `references/investigator-prompt.md`. Base prompt template for investigator subagents.
- `references/source-playbook.md`. Index pointing at the category playbooks below.
- `references/sources/*.md`. One self-contained example playbook per category, plus cross-cutting `incident-postmortem.md`. Give an investigator the single file that matches its category and adapt it to the available read-only source/tool.
- `references/synthesizer-prompt.md`. Prompt template for the synthesizer subagent, including the output format.
