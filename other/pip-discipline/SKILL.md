---
name: pip-discipline
description: "Evidence-discipline recovery for stalled ecdsa.fail work. Use when the same route, prompt or script has failed twice, an agent keeps tweaking parameters without changing the idea, a failure is blamed on tooling before anyone checked, a completion is claimed without validator output, or a compute request has no owner, validator, kill gate, budget or stop condition. Not for a first pass with a known fix."
license: MIT
---

# Tätschmeischter (pip-discipline)

*PIP evidence discipline*

Use when an agent, operator, or worker has failed twice, is repeating the same
approach, is about to hand the task back without evidence, or has claimed
completion without running the relevant check.

## Source and scope

Adapted from the English PIP edition of `tanweai/pua`:

- Source: `https://github.com/tanweai/pua`
- Audited commit: `f16769945d42bdb568fc956d53f2c9f347d66ae2`
- Audited source file: `codex/pua-en/SKILL.md`
- Audited SHA-256:
  `9ac522d2f80655853a4445a5ef0824ffdc139d737030494beb16ccbc1104f98a`

This Storm integration imports the operating discipline only. It does not
include plugin hooks, prompt routers, telemetry, feedback upload, leaderboard,
survey, remote prompt loading, or always-on behavior.

## Public boundary

This skill is for public `ecdsa.fail` coordination. Do not request or expose:

- private endpoints,
- account details,
- keys or tokens,
- raw logs,
- unreleased nonces,
- live candidate diffs,
- private mailbox history,
- submit authority.

When a next step needs private state, stop at a handoff boundary and name the
public evidence that justifies the request.

## Trigger

Activate this card when any of these are true:

- the same route, prompt, or script failed twice,
- the agent keeps changing parameters without changing the idea,
- a route is blamed on environment or tooling before verification,
- a worker asks for human action before checking public/local evidence,
- a completion claim lacks command output, validator output, or source citation,
- a compute request lacks owner, validator, kill gate, budget, or stop condition.

Do not activate for a normal first pass when a known fix is already being
executed.

## Protocol

1. Stop the current loop. List the last attempts and the shared assumption.
2. Read the failure signal word by word: error, rejection, empty result, stale
   route, missing evidence label, or user critique.
3. Refresh public truth before relying on memory: current target, public docs,
   fixture data, route packet, or source file.
4. Read the raw material, not a summary. For code, inspect local context around
   the failing line. For routes, inspect the packet, validator, and kill gate.
5. Verify assumptions with tools: path, version, input shape, validator command,
   budget, public source, and stop condition.
6. Invert the main assumption. If the route is assumed alive, try to kill it. If
   a bug is assumed local, check the caller, fixture, and validator.
7. Produce three materially different hypotheses, not three parameter tweaks.
8. Execute the smallest bounded check that creates new evidence.
9. Close the loop: record what passed, what failed, what was killed, and what
   must not be retried.

## Output

Return this block before the next major action:

```text
PIP discipline:
- Failure mode:
- Repeated assumption:
- Evidence read:
- Verified facts:
- Three different hypotheses:
- Next bounded check:
- Kill gate:
- Completion evidence required:
```

## Completion gate

Do not say a route, patch, dashboard, or note is complete until the relevant
check has been run or the missing check is named as a blocker.

For this repo, useful completion evidence includes:

- `scripts/redaction-check.sh`
- `scripts/check-public-harness.sh`
- fixture dashboard preview using demo/public data only
- route packet fields filled with owner, validator, budget, and stop condition
- public-note language that avoids win claims unless the submit gate is met

## Exit report

If the route still cannot advance after the protocol, return a structured
handoff instead of a vague failure:

- verified facts,
- excluded possibilities,
- smallest remaining uncertainty,
- next public check,
- exact private boundary, if any,
- reason to proceed, park, kill, or request human review.
