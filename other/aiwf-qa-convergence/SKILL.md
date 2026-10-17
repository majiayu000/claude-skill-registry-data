---
name: aiwf-qa-convergence
description: Run bounded software QA test-fix loops with severity gates, stable issue fingerprints, deterministic checks, runtime evidence, and explicit clean, accepted-minor, stalled, blocked, escalation, or budget exits. Use when asked to repeat QA or bug passes until an app, API, UI, device workflow, or repository converges.
---

# AIWF QA Convergence

## Control Policy

```yaml
AIWF_QA_CLEAN_STREAK: 2
AIWF_QA_ACCEPTED_MINOR_STREAK: 3
AIWF_QA_MAX_CYCLES: 8
AIWF_QA_MAX_NO_PROGRESS: 2
AIWF_QA_MAX_FIX_ATTEMPTS_PER_ISSUE: 3
```

These values guide the loop. They do not reconfigure the host model, reasoning effort, tool permissions, or resource limits.

## Core Rule

Define a fixed QA manifest and bounded exits before fixing the first finding. Only `CLEAN` and `ACCEPTABLE_WITH_MINOR` are successful outcomes.

## Workflow

1. Read project instructions, repository state, current handoffs, and existing QA artifacts. Add `aiwf-repo-sentinel` plus the owning language, framework, device, or security skill when needed.
2. Create a QA manifest using [references/report-schema.md](references/report-schema.md). Include source and test paths, deterministic gates, runtime workflows, supported devices or browsers, exclusions, and evidence locations.
3. Initialize durable state outside the declared source paths:

```powershell
python <this-skill>\scripts\qa_convergence.py init --root <project-root> --manifest <qa-manifest.json> --state <qa-convergence.json> --target <target>
```

4. Run the cheapest affected checks first. Use full build, package, device, browser, or end-to-end checks only where the manifest requires them.
5. Classify findings by impact: `critical`, `high`, `medium`, `low`, or `info`. A terminal warning is not automatically minor. Security exposure, data loss, corruption, crashes, hangs, broken core workflows, and unsafe resource behavior remain blocking regardless of log label.
6. Fingerprint each issue with stable evidence such as tool, rule or exception, normalized path or workflow, and observed behavior. Do not count duplicate wording as a new issue.
7. Record every completed pass:

```powershell
python <this-skill>\scripts\qa_convergence.py record --state <qa-convergence.json> --report <pass-report.json>
python <this-skill>\scripts\qa_convergence.py status --state <qa-convergence.json>
```

8. Fix blocking findings narrowly, add regression evidence when practical, then rerun affected gates. A source, dependency, config, test, or manifest change resets the qualifying streak.
9. Use independent final lenses: deterministic checks, real runtime or device workflows, then a fresh-context review. Repeating an identical model review without new evidence is not an independent pass.

## Exit Gates

- `CLEAN`: two consecutive independent passes with all required gates passing and no unresolved findings.
- `ACCEPTABLE_WITH_MINOR`: three consecutive passes with all required gates passing, no unresolved critical/high/medium findings, no new low/info fingerprints after the first pass, and a reason recorded for every accepted finding.
- `STALLED`: two consecutive passes produce no useful diff, new evidence, passing gate, or reduced blocking set.
- `ESCALATE`: the same unresolved issue survives three attempted fixes, or the next action crosses an approval, architecture, security, or destructive boundary.
- `BUDGET_EXHAUSTED`: eight cycles or the project-defined wall-time or cost limit is reached.
- `BLOCKED`: a required device, service, credential, dependency, user decision, or external system is unavailable.
- `ABORTED`: continuing would violate authorization, safety, data, or repository boundaries.

## Resource Rules

- UI, browser, docs, lint, contract, and unit-test passes do not load a local AI model unless that exact workflow requires one.
- Lower-cost review can handle discovery and routine fixes. Release-critical security, privacy, data-integrity, and destructive-path acceptance needs independent evidence and stronger review.
- Respect shared writer and CPU/RAM/GPU leases. One integration owner controls fixes and final acceptance.

## Output

Report the target and manifest, source and manifest hashes, cycles and streaks, gate evidence, fixed and accepted findings, final state, unresolved risks, and exact next action for every non-success exit.
