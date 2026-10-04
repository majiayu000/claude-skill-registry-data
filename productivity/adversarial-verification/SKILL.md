---
name: adversarial-verification
description: Dispatch an independent, skeptical agent to re-derive whether a fix/claim/artifact actually worked, instead of trusting the builder's self-assessment. Use when a subagent, Workflow stage, or parallel candidate reports "fixed it" and the cost of a false green is high — code fixes, pipeline output, generated assets, live-site claims. Do NOT use for verifying your OWN uncommitted work (that is verification-loop — just run the gates), and do NOT use for vetting a plan before anyone builds (that is adversarial-planning).
---

# Independent Re-Check

## The problem

An agent that builds a fix and then grades its own fix will round up. "Looks better to
me" is not evidence — it is the builder's incentive to report success talking. This is
the same failure `verification-before-completion` names for a single agent's own work;
adversarial verification is the version for orchestrated/multi-agent work, where the fix
is a **separate artifact** another agent can independently inspect.

The repo has the receipts. Adversarial review of code whose own TDD suite was green
found **3 real defects** in the content-evaluator (bug-148), **16** in the deterministic
fraud scorer (bug-150), **4** across the Tier-2 scorers (bug-151). In every case the
builder's tests passed. They tested that each rule fires; nobody re-derived whether the
contract held.

## When to use

Use it when:

- a subagent or Workflow stage returns a "done / fixed / verified" report and you are
  about to relay that to the founder or ship on it
- multiple independent candidates were built in parallel and need honest, *comparable*
  grading before one is selected
- the claim carries severity — "production bug fixed", "renders are canon-clean",
  "the deploy is live" — and the only evidence is the builder's prose
- a gate the builder cites is one that has historically failed open (bug-230)

Do **not** use it:

- on your own uncommitted edit. Re-reading your own diff is not independence; run the
  gates ([`verification-loop`](../verification-loop/SKILL.md)) instead.
- before anything is built. A claim with no artifact cannot be re-derived —
  [`adversarial-planning`](../adversarial-planning/SKILL.md) is the pre-build loop.
- on a trivially checkable claim you can settle yourself in one command. Dispatching an
  agent to run `git log -1` is ceremony, not verification.

## Inputs

| Required | Why | If absent |
|---|---|---|
| An **artifact**, not a claim — a diff, an exported file, a rendered image, a raw command transcript, a query result | The verifier must inspect something the builder cannot re-narrate | **Stop.** Send the builder back for the artifact. Verifying prose produces a verdict about prose. |
| The **original problem statement**, verbatim | The verifier grades against the requirement, not against the builder's restatement of it | **Stop.** Without it the verifier grades "did something change", which always passes. |
| A **re-runnable check** the verifier can execute itself (test command, curl, vision read, query) | Independence means re-derivation, not re-reading | **Stop and say so.** "Cannot be independently checked" is a legitimate verdict; a confident `clean` is not. |
| The builder's notes — **labeled as unverified claims to check** | Useful context, toxic as premise | If they arrive as fact, relabel before handing over. |
| For a `[live]` verdict: production access | Severity requires a production probe | Downgrade to `[repo]`/`[repro]` and say production is unverified. |

## Procedure

1. **Collect the artifact and the original problem statement.** Strip the builder's
   self-assessment out of the premise; re-attach it as *claims under test*.
2. **Dispatch a fresh agent** with no memory of building it. For higher-stakes work make
   it a *different model* — a fresh instance of the same model can carry the same blind
   spot. Pair via `agent()`'s `model` option (e.g. builder `sonnet`, verifier `opus`).
3. **Instruct it to default to skeptical**: assume still-broken unless the evidence
   proves otherwise. A partial improvement is `partially-improved`, never `clean`. Ties
   go to "not fixed".
4. **Require re-derivation, not summary.** It re-runs the test, re-renders the asset,
   re-executes the query, re-reads the pixels. If it cannot reproduce the check, it
   cannot confirm the claim — that is a `cannot-verify` outcome, not a pass.
5. **Force a structured verdict**: an enum (`clean` / `partially-improved` /
   `no-improvement` / `regressed`) plus a boolean `recommend_ship`. Free-form prose
   gives synthesis nothing to compare.
6. **Check the verdict's evidence scope covers its claim scope.** A `clean` +
   "production fixed" backed only by `[repo]` reading is rejected and sent back for a
   `[live]` probe.
7. **Synthesis compares verdicts, never builder claims.** Only verifier-confirmed
   artifacts move forward to deploy/merge/ship.

### Two-model debate loop (hard-capped at 3 rounds)

Rounds 1-2 are argument; round 3 is not — it is a forcing function that ends debate by
making both sides touch ground truth.

1. **Round 1 — proposal + challenge.** Builder (model A) proposes. Verifier (model B)
   challenges skeptically and must state specifically what evidence would change its
   verdict.
2. **Round 2 — rebuttal + recheck.** Builder addresses that specific challenge, not a
   full re-argument. Verifier rechecks. Satisfied → stop; do not burn round 3 on
   agreement.
3. **Round 3 — mandatory execution, no more argument.** Both sides stop arguing and
   **execute the verifiable task themselves** right now — run the test, re-render, re-run
   the query — and the verdict comes from that raw output. This is the exit condition
   whether or not the models agree: empirical execution outranks continued debate. Never
   let round 3 become "argue again, harder."

```js
const MODELS = { builder: 'sonnet', verifier: 'opus' } // deliberately different

let verdict = null
let transcript = []
for (let round = 1; round <= 3; round++) {
  const finalRound = round === 3
  if (verdict?.overall_verdict === 'clean') break // converged early, skip round 3

  const builderTurn = await agent(
    finalRound
      ? `Final round. No more argument. Execute the verifiable check yourself right
         now (run the command/test/render) and report the raw output.
         Debate so far: ${JSON.stringify(transcript)}`
      : `Round ${round}. Defend or refine against this challenge (if any):
         ${JSON.stringify(verdict) || 'none yet — initial proposal'}.`,
    { label: `builder-r${round}`, model: MODELS.builder, schema: BUILD_SCHEMA }
  )

  const verifierTurn = await agent(
    finalRound
      ? `Final round. Do not argue further — independently execute the same
         verifiable check yourself and report raw output. Compare against the
         builder's round-3 execution: ${JSON.stringify(builderTurn)}`
      : `Round ${round}. Skeptically challenge this artifact. Default to "not fixed"
         unless proven. State specifically what would change your mind next round.
         Artifact: ${JSON.stringify(builderTurn)}`,
    { label: `verifier-r${round}`, model: MODELS.verifier, schema: VERIFY_SCHEMA }
  )

  transcript.push({ round, builderTurn, verifierTurn })
  verdict = verifierTurn
}
```

Fan the whole loop out per candidate with `pipeline()` when independent builders compete
— each candidate gets its own debate, own pairing, own verdict; only synthesis needs a
barrier, since it must compare all candidates at once.

**Standalone (non-Workflow) use.** The same discipline applies to a single dispatch:
after `Agent()` returns "fixed it", dispatch a **second, independent** `Agent()` with the
artifact and skeptical instructions before relaying "done".

## Verification

The verifier's own output is an artifact and gets checked like any other.

**1 — The verdict is structured and in-vocabulary.** Free prose fails here.

```bash
python3 -c "import json;v=json.load(open('/tmp/verdict.json'));assert v['overall_verdict'] in {'clean','partially-improved','no-improvement','regressed'},v;assert isinstance(v['recommend_ship'],bool),v;assert v.get('evidence'),'no re-derived evidence';print('verdict schema OK')"
```

**PASS:** exits 0 and prints `verdict schema OK`. A verdict with no `evidence` field is
prose wearing a schema. `[test]`

**2 — The verifier re-derived, it did not re-read.** Re-run the check yourself and
compare to the transcript it reported.

```bash
rtk proxy pytest tests/mcp/test_http_mount.py -q
```

**PASS:** your run's pass/fail counts equal the counts inside `verdict.evidence`. A
mismatch means the verifier reported a run it did not do — reject the verdict. `[repro]`

**3 — Scope covers severity.** A verdict asserting production behaviour needs a
production probe of its own.

```bash
grep -o '\[live\]\|\[repo\]\|\[repro\]\|\[inferred\]' /tmp/verdict.json | sort -u
```

**PASS:** if the verdict text says "production" / "live" / "critical", `[live]` appears
in that output. If only `[repo]` / `[inferred]` appear, downgrade the claim before
relaying it. `[test]`

**4 — Prove the verifier can return "no"** before trusting a `clean`. Hand it a known-bad
artifact once per pairing.

```bash
git archive HEAD mcp_tools/http_mount.py | tar -x -C /tmp/pristine-mcp
```

Then dispatch the same verifier against that pre-fix file with the same problem
statement. **PASS-OF-THE-PROOF:** the verdict is *not* `clean` — the pre-fix file
compares tokens with `!=`. A verifier that returns `clean` against the pristine tree is
decoration; replace it. `[test]`

Never `git stash` to produce that pristine tree; the stash stack is shared across
worktrees and you can pop another session's work.

**A verifier run that errored, timed out, or hit a session limit produced an artifact,
not a result.** Re-run it by hand. Its empty findings list is the fail-open pattern
(bug-230), and a verification stage is precisely where it hides.

## Worked example

Claim under test (builder): *"Hardened the MCP bearer-token check — bug-211 closed."*

The verifier was given `mcp_tools/http_mount.py`, the bug-211 statement from
`.wolf/buglog.json` ("plain string `!=` leaks length/prefix; missing `MCP_SERVICE_TOKEN`
→ warn-and-serve-open"), and no builder commentary. It re-derived both halves.

```bash
$ grep -n "compare_digest\|MCP_SERVICE_TOKEN" mcp_tools/http_mount.py
7:Auth: a shared Bearer service token (``MCP_SERVICE_TOKEN``). When the token is set
32:_TOKEN_ENV = "MCP_SERVICE_TOKEN"
53:    Enforced only when ``MCP_SERVICE_TOKEN`` is configured. An unset token in a
88:        if not hmac.compare_digest(provided, f"Bearer {token}")
```

`[repo]` — the timing-safe comparison is present at line 88.

```bash
$ rtk proxy pytest tests/mcp/test_http_mount.py -q
......                                                                   [100%]
```

`[repro]` — 6 passed, 0 failed, re-run by the verifier itself, not quoted from the
builder.

**Verdict issued: `partially-improved`, `recommend_ship: false`.** Reasoning: half the
bug — the timing side-channel — is confirmed closed at `[repo]` + `[repro]` scope. The
other half, "fail-closed when the token is unset **in production**", is asserted by
`http_mount.py:53` and by a unit test, both of which describe the *code*. No probe of a
running production instance was performed, so the fail-open half is `[inferred]` and
carries no severity. `clean` would have been the round-up.

That is the whole discipline in one verdict: the builder was not wrong, and the verdict
still is not `clean`, because the evidence scope did not reach the claim scope.

## Failure modes

| Symptom | What is really happening | Bug |
|---|---|---|
| Verifier returns `clean` with prose like "the fix looks correct" | It re-read the builder's diff instead of re-deriving. No command in its evidence = no verification. | — |
| Green tests cited as proof the contract holds | Tests prove each rule fires; they do not exercise calibration, boundaries, or the never-raises guard. Adversarial review found 16 defects behind a green suite. | bug-150 |
| Verifier and builder are the same model, verdict is always `clean` | Shared blind spot. Use different weights, not a fresh instance. | — |
| Debate reaches round 3 and keeps arguing | Round 3 is execution-only by construction. Argument in round 3 means the loop has no exit condition. | — |
| Verdict says "production bug fixed", evidence is all `[repo]` | Scope jump. Severity requires `[live]`. State scope before severity. | bug-287 |
| Verifier stage errored; orchestrator recorded zero findings and moved on | Fail-open. A gate that dies is not a gate that passed. | bug-230 (×6) |
| Verifier confirms an asset "looks like a plausible Black Rose piece" | Checking against memory of the collection, not side-by-side against the canonical reference. Lenient QC ships hallucinations. | bug-276 |
| Verdict is free-form prose; synthesis picks a winner anyway | No enum, nothing comparable — synthesis is guessing with extra steps. | — |
