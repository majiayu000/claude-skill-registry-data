---
model_tier: high
name: risk-officer
description: "Use when surfacing and prioritising risk before commit — blast-radius framing, mitigations, residual-risk verdict — even if the user just says 'what could go wrong here?'."
personas:
  - critical-challenger
  - senior-engineer
domain: quality
workspaces:
  - engineering
packs:
  - engineering-base
---

# risk-officer

> Surface risks the implementer or PO is likely to underweight, score
> them by **likelihood × impact**, and propose mitigations the team
> can actually execute. Sibling of
> [`threat-modeling`](../threat-modeling/SKILL.md) (security-only)
> and [`blast-radius-analyzer`](../blast-radius-analyzer/SKILL.md)
> (call-site only) — this skill takes the wider product, ops, and
> coordination view.

## When to use

- Pre-implementation: a roadmap, ADR, or refined ticket needs a risk
  pass before the team commits.
- Pre-merge: a non-trivial diff is about to land and the team wants
  one more risk lens beyond the four standard judges.
- Post-incident: surface the risks the team should track to prevent
  recurrence (without writing the post-mortem itself).
- German triggers: "was kann schiefgehen?", "Risiko-Check", "wo
  brennt es?".

Do NOT use when:

- The concern is exclusively security or authZ — route to
  [`threat-modeling`](../threat-modeling/SKILL.md) or
  [`judge-security-auditor`](../judge-security-auditor/SKILL.md).
- The concern is exclusively call-site impact of a refactor — route
  to [`blast-radius-analyzer`](../blast-radius-analyzer/SKILL.md).
- The user wants a fix, not a risk view — risk-officer never patches.

## Procedure

### 1. Inspect the change

Read the input (roadmap step, ticket, diff, post-mortem) and identify
the scope in one sentence: *"This change does X for users Y, touching
systems Z."* If you cannot, the artefact is not reviewable — stop and
ask.

### 2. Enumerate risks across five lenses

| Lens | Sample questions |
|---|---|
| Product | Wrong outcome shipped, churn, support load, brand impact |
| Operations | Rollback path, observability, on-call burden, alert noise |
| Coordination | Cross-team dependencies, communication gaps, sequencing |
| Data | Loss, corruption, leakage, retention, compliance, residency |
| Time | Schedule slip, opportunity cost, sunk-cost lock-in |

Per lens, list each risk as a single bullet. Reject vague risks —
"could break things" is not a risk; "queue worker silently drops
messages on retry exhaustion" is.

### 3. Score each risk

For every risk, assign **L** (likelihood: low / med / high) and **I**
(impact: low / med / high). Top-5 sort by `LxI` rank; cite the
trigger condition for each L and I. Do NOT pad to a fixed count —
three sharp risks beat ten generic ones.

### 4. Propose mitigations

For the top-5 risks, propose **one** mitigation that the team can
own. Each mitigation has an owner role (eng, ops, PO, support), a
rough size (S / M / L), and a residual-risk note (what stays after
mitigation). Mitigations the team cannot execute are not mitigations
— flag them as `accept` or escalate.

### 5. Issue a verdict

| Verdict  | When to issue |
|---|---|
| `proceed`             | Top-5 risks have owned mitigations; residual is acceptable |
| `proceed-with-mitigations` | Mitigations must land BEFORE or WITH the change |
| `pause`               | One or more `high × high` risks have no executable mitigation |

`pause` is not a veto — it forces the user to decide explicitly.

### 6. Validate the verdict

Before emitting, verify each top-5 risk has: a concrete trigger, a
scored L×I, an owned mitigation (or explicit `accept`), and a
residual note. Ensure the verdict matches the worst residual — a
`high × high` residual without executable mitigation must produce
`pause`, not `proceed`.

## Output format

The report is a single block with these ordered fields:

1. `Target:` — one-sentence scope from step 1
2. `Top-5 risks:` — numbered list, each with `L=`, `I=`, trigger,
   mitigation, owner, size, residual
3. `Other risks tracked:` — count of risks below the top-5 cut
4. `Verdict:` — exactly one of `proceed` / `proceed-with-mitigations`
   / `pause`

```
Risk-Officer
Target: <one-sentence scope>

Top-5 risks:
1. 🔴 <risk> (L=high, I=high)  Trigger: <condition>
   Mitigation: <action>  Owner: <role>  Size: <S/M/L>
   Residual: <what remains>
2. 🟡 <risk> (L=med, I=high)   ...

Other risks tracked: <count>, summarised below or omitted if low/low.

Verdict: proceed | proceed-with-mitigations | pause
```

## Gotcha

- A risk without a trigger is a vibe, not a risk. Reject vibes.
- Likelihood is conditional on the change — not the universal base
  rate of the system. "Postgres goes down" is not a risk of *this
  change* unless the change increases that likelihood.
- Mitigations the team will not execute are theatre. Be honest in
  the residual-risk note.

## Do NOT

- Do NOT enumerate every conceivable risk — top-5 with rationale is
  the contract.
- Do NOT score `high × high` reflexively to be cautious; mis-scoring
  destroys the rank.
- Do NOT propose mitigations the agent itself will own — the owner
  is always a human role.
- Do NOT issue `pause` as a soft veto on something the user already
  decided; issue `proceed-with-mitigations` and surface the residual.
