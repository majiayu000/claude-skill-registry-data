---
name: build-test-suite
description: Build a compact Coval test set from product requirements, observed conversation failures or a coverage gap. Design realistic scenarios with separate expected behaviors, provenance and controlled voice/persona variation.
argument-hint: "[agent-or-failure-mode]"
---

# Build a useful Coval test suite

Create tests that change a product decision. A small set covering distinct
failure mechanisms is more useful than many paraphrases of a happy path.

## Understand and reuse

Confirm organization/workspace, agent and scope. Inspect the selected agent,
existing cases, relevant recordings and the customer's source-of-truth policy.
Use `coval --agent agents get <id>`, `test-sets get`, and `test-cases list
--test-set-id <id>`. Check command help, errors and pagination. Do not replace
an existing suite or derive requirements solely from a buggy agent prompt.

For a large corpus, `distill-test-set` can help shortlist source rows; inspect
its resulting input/expectation pairs. For unexplored conversations, use
`coval-discover-failures`. Neither is mandatory when the requirement is known.

## Design the coverage before prose

Make a compact matrix with: requirement or observed failure, source, meaningful
variation, scenario, expected behaviors, evidence needed, and risk/priority.
Distinguish observed failure, policy requirement and synthetic hypothesis.

Choose axes that could alter behavior: ambiguous request, changed information,
missing tool result, unsupported request, caller correction, or a relevant audio
condition. Avoid an automatic Cartesian product. Generate combinations first,
then realistic caller scenarios; discard impossible combinations and semantic
duplicates. Preserve a few untouched cases for later regression checks.

For voice, separate scenario from persona and audio condition. Start with normal
audio; vary accent/noise/interruption only for a stated hypothesis. Don't put
sensitive real customer details in synthetic cases. Keep examples fictional
and realistic for the customer's supported language and workflow.

Example for a clinic whose published hours are Monday–Friday, 8am–5pm:

| Case | Scenario for the caller | Expected agent behavior | Source |
|---|---|---|---|
| Hours | Ask when the clinic closes on Friday; thank them and end after the answer | Says 5pm on Friday | Office policy |
| Closed day | Ask whether the clinic is open Sunday; don't suggest an answer | States it is closed Sunday; doesn't invent Sunday hours | Office policy |
| Correction | Ask about Thursday, then correct yourself to Friday | Answers the corrected day | Hypothesized repair failure |

This verifies information, not that an appointment was persisted.

## Make expectations evaluable

Write each mandatory behavior as a separate array item. State the relevant
precondition and observable outcome. Avoid “helpful,” arbitrary numeric scores,
or requiring a particular phrase when a correct paraphrase is acceptable.

Don't leak the answer through `input_str` or persona instructions. A scenario
sets the caller's goal, not the agent's response. Choose the input mode from the
current test-case spec: SCENARIO for flexible interaction; SCRIPT only when exact
caller turns matter. Do not call generated dialogue real production evidence.

Use transcript evidence for conversation behavior, audio for acoustic behavior,
and correlated tool results for actual side effects. If the evidence cannot
support a criterion, revise it or flag the instrumentation gap before scoring.

## Create and read back

Prepare the exact cases locally before asking for any missing write authority.
Respect creation already authorized in the conversation. Use structured JSON
rather than interpolating customer prose into shell strings:

```bash
coval --agent test-sets create --input-json @test-set.json
coval --agent test-cases create --input-json @case.json
```

`test-set.json` uses the public API shape:

```json
{"display_name":"Clinic information checks","test_set_type":"SCENARIO"}
```

After obtaining the actual test-set ID, `case.json` is:

```json
{
  "test_set_id":"<returned-id>",
  "input_str":"Ask when the clinic closes on Friday. After the answer, thank them and end the conversation.",
  "expected_behaviors":["The assistant states that the clinic closes at 5pm on Friday."],
  "description":"Friday closing time; source: office policy",
  "input_type":"SCENARIO"
}
```

Check `coval test-cases create --help` and the current
[test-cases schema](https://api.coval.dev/v1/openapi/test-cases) before creation.
A CLI lacking structured input can use the documented public API. Check every
response before creating the next item; on ambiguous timeouts inspect existing
resources before retrying to avoid duplicates. Read every created case back
and verify its input and **individual** expected behaviors. Confirm the count
using pagination when necessary.

## Handoff

Show the coverage matrix, IDs and untested gaps. Keep source distribution
separate from intentionally overweighted failure cases. Creating a suite does
not authorize running it. Propose an explicit small subset for `quick-eval`,
with counts including iterations, personas and base + mutations. Use
`configure-metrics` to turn appropriate criteria into a provisional measure.
