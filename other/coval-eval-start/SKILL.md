---
name: coval-eval-start
description: Choose the next useful step for evaluating a voice or chat agent with Coval. Use for getting started or deciding what to do next; use a specific skill directly when the task is already clear.
---

# Start a Coval evaluation

Help the customer answer a product question, not accumulate evaluation resources.
Find their situation, explain the next useful step in one sentence, and follow
the matching skill. Reuse supplied context; ask only for missing information.

## Establish the starting point

Identify the agent's job, the decision the customer wants to make, and what
evidence they already have: an endpoint, a test set, completed conversations,
an observed failure, or reviewer labels. A first-time Coval user may already
have production recordings; don't send them through synthetic onboarding.

For a connected account, check `coval --version`, `coval --agent agent doctor`,
and the relevant resource's `context`/`--help`. Confirm the intended organization,
API environment and workspace with the customer or their existing configuration.
Doctor checks authentication/connectivity; it does **not** prove the organization
identity. Never print a key or inspect other organizations to find a match.

Start with a small, scoped inventory. `--agent` responses wrap payloads in `data`;
check `ok` and the process exit code. A list can be one page, not the whole account.
No credentials yet? Explain setup using the [CLI installation guide](https://docs.coval.ai/cli/installation),
and continue designing locally if the customer wants that.

## Route by evidence

| Customer situation | Next skill | Useful output |
|---|---|---|
| No completed conversations; wants a first live evaluation | `onboard` | A small, real run with inspected results and clear limits |
| Has recordings, transcripts or runs; wants to understand failures | `coval-discover-failures` | Evidence-backed failure hypotheses and a review sample |
| Has a specific requirement or observed coverage gap | `build-test-suite` | A compact scenario matrix with checkable expectations |
| Knows what to measure; needs a Coval metric | `configure-metrics` | The simplest suitable metric and a tested rubric |
| Has a judge; wants to know whether its scores are trustworthy | `coval-calibrate-metric` | Class-specific errors on independent human labels, or a labeling plan |
| Has resources ready and explicitly wants to run them | `quick-eval` | A bounded run and a result audit |
| Has before/after runs; asks whether a change helped | `coval-compare-runs` | Matched evidence, regressions and comparison limits |
| Has an existing evaluation setup; wants a trust/coverage audit | `coval-eval-audit` | Prioritized findings tied to actual Coval artifacts |

These are installed skill names, not shell commands. Locate the selected skill
in the agent's installed skill catalog. If absent, explain the missing skill
and install it only in the user's intended scope, or perform the bounded task
using current public documentation. Do not invent an executable `/skill` command
or assume sibling directories survive a single-skill installation.

## Keep the next step small

- Reuse existing resources. Don't create a second agent, rewrite a production
  metric, attach defaults, schedule runs, or enable notifications merely to start.
- For a new voice connection, propose **one case, one persona, one iteration,
  concurrency one**. A request to plan or audit does not authorize a paid run.
  Honor an already authorized execution budget; don't ask again inside it.
- Before execution, state the selected cases, metric IDs, maximum simulations,
  call-duration limit, and stopping condition. Count base + every mutation and
  every persona. Reruns and metric tests consume budget too.
- When the customer already knows the failure, don't require a large discovery
  study before adding a useful regression test. Label assumptions as hypotheses.
- Finished execution is not proof of agent quality. Missing outputs, failed
  metrics, simulator mistakes and unvalidated judges must remain visible.

Do not call a starter run statistically conclusive or release-certified. End
with the evidence obtained and the single next action it supports.
