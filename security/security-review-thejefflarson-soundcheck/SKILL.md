---
name: security-review
description: Runs a full OWASP/CWE security audit via isolated subagents. Use when the user
  types /security-review or explicitly requests a full security audit of the
  current code.
---

# Full Security Audit (A01:2025–A10:2025 + LLM01:2025–LLM10:2025)

## What this checks

Full repo audit against OWASP Web + LLM Top 10:2025 via a four-stage
pipeline: threat-model → hotspots → review → validate. Main context
dispatches subagents (`threat-modeling`, `hotspot-mapping`,
`vulnerability-audit`, `design-review`, `finding-validate`,
`attack-chain-analysis`) and renders findings; never reads code.

## Vulnerable patterns

This skill is the orchestrator. The actual pattern catalog lives in
the per-category auto-invoking skills (`injection`, `csrf`, `ssrf`,
`broken-access-control`, `authentication-failures`, etc.) — the
`vulnerability-audit` subagent picks the right one per hotspot and
applies its `Vulnerable patterns` section. Skill-list maintenance
is automatic via `.claude/skills/` directory contents; no separate
catalog file.

## Procedure

Use only the **Agent** tool in main context. **No Read/Grep/Glob/
Bash in main context.** Stage prompts live in `.claude/agents/`:
`threat-modeling`, `hotspot-mapping`, `design-review`,
`vulnerability-audit`, `finding-validate`, `attack-chain-analysis`.
This skill is just the coordinator.

Copy this checklist as you progress:

```
- [ ] Stage 0 — threat-modeling returned
- [ ] Stage 1 — hotspot-mapping returned (one whole-repo call)
- [ ] Stages 1b+2 — design-review + N vulnerability-audit in ONE message
- [ ] Stage 2.5 — finding-validate returned; refuted findings dropped
- [ ] Stage 3 — attack-chain-analysis returned
- [ ] Stage 4 — findings table rendered with severity legend
- [ ] Stage 5 — suggested /security-cleanup to the user
```

### Stage 0 — Threat model

Dispatch one `threat-modeling` subagent. It returns JSON with
purpose, deployment, trusted_inputs, untrusted_inputs. Thread this
into every later subagent.

### Stage 1 — Hotspot map

Dispatch **one** `hotspot-mapping` subagent with the threat model.
Returns a JSON array of `{file, lines, name, category, priority, why}`
entries — the hotspot list for Stage 2.

### Stages 1b + 2 — Design review and vulnerability audit (parallel)

**Collapse hotspots by file first** — group into `{file: [hotspots]}`.
Then **in a SINGLE message**, dispatch:

- One `design-review` subagent with the threat model.
- One `vulnerability-audit` subagent **per file** with the threat
  model AND that file's hotspot list. `trusted_inputs` /
  `untrusted_inputs` informs which sinks are reachable. Serial
  launches defeat parallelism.

Concatenate every returned findings array. Dedupe by `(file, line)`.

### Stage 2.5 — Validate findings

Dispatch one `finding-validate` subagent with the merged findings
array and the threat model JSON. It returns a JSON array of 0-based
indices to drop — findings refuted by concrete evidence at the
cited line (guard, sanitizer, correct API). `[]` is common. Remove
the indicated indices before Stage 3.

### Stage 3 — Attack-chain analysis

Dispatch one `attack-chain-analysis` subagent with the threat model
AND the merged findings. The threat model informs effective severity
(does the chain cross an untrusted boundary?). Returns chain objects
with plain-English narratives, or `[]`.

### Stage 4 — Render

Emit `# Security Review`, then the legend *Critical = anyone on the
internet can exploit. High = needs an account. Medium = limited blast
radius. Low = defense-in-depth.* Then a findings table:
**Severity / Where / What's wrong / How to fix** (use the auditor's
`finding`/`fix` verbatim; append `(category: <skill>)` to *What's
wrong*). If chains exist, emit `## Attack chains` with
`### Chain N — <effective_severity>` per chain as prose. One summary
line. Zero findings: `Security review complete. No findings across
N hotspots.`

### Stage 5 — Cleanup

Suggest `/security-cleanup` to apply fixes. Do not auto-rewrite.

## Verification

- [ ] Every vulnerability has a finding with `severity`, `file:line`, OWASP/CWE category, and a concrete fix
- [ ] `finding`/`fix` text is plain language a non-security developer can act on
- [ ] Response ends with a summary line

## References

- CWE-693 ([Protection Mechanism Failure](https://cwe.mitre.org/data/definitions/693.html))
- [OWASP Web Top 10:2025](https://owasp.org/www-project-top-ten/)
- [OWASP LLM Top 10:2025](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
