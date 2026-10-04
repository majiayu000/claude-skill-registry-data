---
name: study-team
description: Use only when the user explicitly asks for an interactive three-perspective review of a completed deep-study report and Claude Code agent teams are already enabled in in-process mode.
allowed-tools: Agent, Read, SendMessage, TaskCreate, TaskGet, TaskList, TaskUpdate
disable-model-invocation: true
version: 1.1.0
changed: "2026-09-30"
---

# Study Team

## Model selection

Use Sonnet by default for delegated work. Explicit `model: opus` escalation is allowed
when the study warrants it; preserve an existing Opus selection. Never request Haiku,
inherit it, or use a built-in delegate that selects it. If this context is running on
Haiku, stop before study work and request a switch to Sonnet or Opus.

Run an optional, interactive challenge-and-reconciliation pass over an already completed
`/deep-study` report. This skill is not part of the deterministic workflow and must never
start automatically.

## Preconditions — Stop Unless All Pass

1. The user explicitly invoked `/study-team` in an attended session.
2. A `/deep-study` report is complete in the current conversation. Complete `/deep-study`
   first if there is no report; do not reconstruct or guess one.
3. Agent teams were enabled by the user before this session with
   `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.
4. The session was launched with `--teammate-mode in-process`.
5. The Agent, SendMessage, and task tools required below are available.

If any precondition cannot be confirmed, explain exactly what is missing and stop.
Do not change settings or enable team mode. Do not fall back to ordinary subagents,
background agents, split panes, or sequential role-play.

## Fixed Team

Use the session's implicit team and create exactly three teammates. Each teammate receives the
complete deep-study report, the user's original request, all evidence and claim identifiers, the shared response
contract below, and only its own role brief. Teammates may not spawn agents, teammates, or
other descendants.

Create one task per role and launch these named teammates:

```yaml
subagent_type: "claude-of-alexandria:study-team-textual-evidence"
name: "textual-evidence"
```

Focus only on passage boundaries, syntax, discourse movement, genre, and whether the report's
claims follow the requested text. Identify the strongest claim, the weakest claim, and any
boundary decision that materially affects interpretation.

```yaml
subagent_type: "claude-of-alexandria:study-team-interpretation"
name: "interpretation"
```

Focus only on historical setting, intertextual context, the interpretive chain from evidence to
claim, source quality, and anachronism risk. Separate evidence found in the report from outside
knowledge; outside knowledge may be proposed for follow-up but may not be promoted to evidence.

```yaml
subagent_type: "claude-of-alexandria:study-team-critique"
name: "critique"
```

Adversarially test theological coherence, canonical connections, confidence calibration, and
whether synthesis overstates what the evidence supports. Preserve genuine disagreements.

## Shared Teammate Contract

Each teammate must:

1. Work only inside its assigned scope and cite exact claim/evidence IDs from the report.
2. Send a concise first-pass finding to both peers with `SendMessage`.
3. Read both peer messages, then state agreement, disagreement, or a dependency explicitly.
4. Send one final deliverable to the team lead with `SendMessage`, then mark its task complete.

The final deliverable has exactly these headings:

```text
PERSPECTIVE:
SUPPORTED:
CHALLENGED:
DEPENDENCIES:
UNRESOLVED:
RECOMMENDED REVISION:
```

No teammate may rewrite the whole report or claim consensus merely because another teammate
agrees.

## Lead Procedure

Wait for all three final deliverables before synthesizing. A task marked complete without a
deliverable does not count; ask that named teammate once for the missing contract. Do not
replace a missing teammate with a subagent or a lead-authored imitation.

The lead is the sole report writer. Then return one review containing:

- the three perspective summaries;
- agreements supported by named claim/evidence IDs;
- disagreements that remain and why;
- dependencies between findings;
- a bounded revision list for the existing report.

Do not silently rewrite the original report. After the review is delivered, send a shutdown
request to each teammate. Claude Code cleans up the implicit team when the session ends; there
is no manual team-deletion step. If shutdown fails, report the failure explicitly.

If the session is resumed, rebuild the team, tasks, role context, and coordination state
explicitly; do not assume teammate state survived. Team output has no workflow-schema
guarantee. It may inform a separately requested `/deep-study`, but it never mutates or resumes
the prior workflow automatically.
