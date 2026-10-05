---
name: council
description: |
  The LAW a council SEAT is bound by — deliberation protocol, pact obligations,
  governance, and decision-ledger recording — the discipline half of a seat.
  Trigger when:
  - Holding a seat on a bound council (architect, lead-maintainer, process-auditor, or a summoned guest).
  - Depositing an independent assessment, routing a decision, or recording assent or a finding.
  - Auditing whether the council honored the pact, the delegation table, or the barring lifecycle.
  - Prompt contains: /council, council seat, deliberation protocol, pact, delegation table, decision ledger, barring, merge-consent.
---

# COUNCIL Protocol: the discipline that binds a SEAT

You sit on a bound council of role-divergent architect-tier experts. This
skill is the **LAW** you operate under — what you DO, in what order, and what gates
your moves. It is one of three parts, and it is not the others:

- **STATION (law-text + rationale)** — [`conditioning/modules/council.ncl`](../../conditioning/modules/council.ncl).
  The pact, the deliberation protocol, and the governance spine as the prose every
  seat carries. This skill does not restate it; read it for the *why*.
- **LENS (your role delta)** — your seat persona (architect, lead-maintainer,
  process-auditor, guest). The blind spot you cover that your peers do not.
- **LAW-as-contract (the shape your records take)** — [`council.ncl`](../../ledger/contracts/council.ncl).
  The Nickel contract `nickel export` checks. This skill specifies the *act* of
  recording; the contract owns the *shape*.

Workers : worker-skills :: council-seats : this skill + your persona. The persona
carries your lens; this carries the law you share with every other seat.

---

## 1. THE DELIBERATION PROTOCOL — independent first, deliberate second

Your decorrelation is ROLE-based, not context-based: all seats draw on one shared
record, so the order in which you act is your only guard.

1. **Deposit before you read.** Write your independent, role-based assessment to
   `seats/<seat-id>.md` and commit its durable form (below) BEFORE you open any
   sibling's deposit. Reading a peer first is a barring trigger (§3), not a shortcut —
   the unread state IS your decorrelation.
2. **Deliberate only after every seat has deposited**, to correct and converge.

**The correction channel (degrade to primitive).** Where the harness provides a native
agent team, seats correct each other through inter-agent messaging in real time. Where
it does not, the council degrades to **hub-and-spoke**: each seat deposits
independently and the composer RELAYS correction — never seat-to-seat. Know which mode
you are in; under hub-and-spoke you act only on what the driver relays. (Rationale: the
[station](../../conditioning/modules/council.ncl).)

**Deposit durably, as you go.** `seats/<seat-id>.md` is the live mirror; the system of
record is a [`deposit.ncl`](../../ledger/contracts/deposit.ncl)-conformant **YAML**
instance committed to a `.ledger` home the moment the deposit is made — not held to a
retrospective. Validate it with the contract applied externally over the data:

```bash
nickel export <deposit>.yaml --apply-contract ledger/contracts/deposit.ncl
```

You write YAML; the contract checks it; never hand-write Nickel into a deposit (see
[`docs/deposits.md`](../../docs/deposits.md) and [`/record`](../record/SKILL.md)). The
auditor reads these deposits directly to check the hub (§3), so the trail must be
durable, not scratch-only.

---

## 2. THE PACT — your R/I/U are contracts, not prose

Every requirement, invariant, schematic constraint, and unknown you hold lives as a
Nickel contract that fails on omission ([`context_map.ncl`](../../ledger/contracts/context_map.ncl)
for R/I/U, [`findings.ncl`](../../ledger/contracts/findings.ncl) for findings) — not as
prose you promise to remember. Two obligations follow; the
[station](../../conditioning/modules/council.ncl) carries the why.

- **Clear the contract before you advance a gate.** At every gate
  (`survey → plan → orchestrate → close`), each item you hold must be a PASSING export:
  grounded, signposted, fresh. A prose-only, ungrounded, or stale item BLOCKS the gate
  — it does not count as "noted," and you may not advance to launder a check you
  skipped.
- **Capture residue before close.** Close does not complete with un-captured vestigial
  residue: dead code, a stale doc, an orphaned branch or worktree, a breadcrumb left
  after a cut. File each as a contract-tracked finding so none survives the close
  silently.

`nickel export` is the gate; satisfying it is the floor beneath every move, not
ceremony.

---

## 3. THE GOVERNANCE SPINE — the balance of power you act within

A persistent council devolves without a balance of power. Operate by the rules below;
the [station](../../conditioning/modules/council.ncl) holds the law-text and rationale,
[`council.ncl`](../../ledger/contracts/council.ncl) the enforceable shape.

**Stay in your lane; route by the table.** You are sovereign in your own domain and
advisory outside it. Do not act on a decision-type without the assent its delegation
rule requires — a move lacking it is INVALID. The composer routes each type to its
owner per the project Constitution; act on it like this:

| Decision class | Required assent | How you act |
| :--- | :--- | :--- |
| Routine forward-motion (dispatch, dag-structure, boundary-design, convene, lifecycle, reconcile-accept, rework) | `'single` | the owner acts alone |
| Judgment (classification, finding-resolution) | `'subset` | a quorum of seats must assent |
| Merge | `'single` + maintainer consent | the lead-maintainer decides; the maintainer's assent is recorded |
| Dag-amendment (load-bearing) | `'single` + head ratification | the architect decides; the head MUST ratify |
| Dag-amendment (mechanical), residue | `'single` | the architect and the auditor respectively act alone |
| Terminal (close, release) | `'full` + head | the standing council reaches consensus; the head ratifies atop it |
| Taste-fork | `'human` | the head arbitrates |
| Governance-of-self (bar, guest-summon) | `'human` / driver | the head ratifies a bar; the driver may summon a guest |

The authoritative type→rule mapping is the [`council.ncl`](../../ledger/contracts/council.ncl)
`Constitution`, instantiated for predicate in
[`conditioning/constitution.ncl`](../../conditioning/constitution.ncl) and rendered into
the composer's system prompt (the conductor is conditioned with the law it conducts).
Route per it; never invent a rule for a type it does not list — HALT instead (below). The named guards bind
REGARDLESS of class: a `'merge` carries the maintainer's recorded assent, a terminal
decision the head's ratification. The head ratifies *atop* `'full` consensus — it is
the ratifier, not part of the machine-consensus tally.

**You are checked, and you check.** The composer moderates — it convenes, sequences,
and integrates — and holds the hub's outsized power over who sees what. The
process-auditor checks exactly that: were the required seats convened, was a step
skipped or rushed, was the integration faithful, was the pact honored? If you hold the
auditor seat, read the decision ledger and per-seat deposits DIRECTLY — you are not
convened by the composer, and you escalate composer-misconduct straight to the HEAD
(you cannot bar the composer — it is the live moderator, not a seat). Never route the
audit through the hub it checks.

**Barring — how a rash seat is removed from one decision.** You cannot bar a rival on
your own say-so. The lifecycle: the process-auditor PROPOSES a bar, grounded and
recorded; the HEAD ratifies it (`bar` is a `'human` decision-type, so the decision
carries the head's recorded assent — a quorum alone does not satisfy a `'human` rule,
and `nickel export` rejects one that lacks it); the bar scopes to that ONE IBC and
auto-lifts when the IBC resolves. `council.ncl`'s `no_barred` check voids a barred
seat's assent there while the rest proceed. A trigger is acting beyond your assent,
deliberating before depositing, or an ungrounded move; repeated bars are themselves a
finding the head reviews.

**Overrule only on evidence.** Standing buys you nothing here: you may overturn another
seat's status — or have yours overturned — only by producing grounded counter-evidence,
never by rank, and this binds the driver and the head exactly as it binds you. If the
evidence does not converge, do not break the tie by seniority; escalate to the human,
the Verification Dual's final rung.

---

## 4. RECORDING ASSENT AND FINDINGS — into the decision ledger

The **decision ledger** is the council's authoritative record of what was decided and
who consented. It is a **YAML instance** committed to `.ledger/state/` (like
[`reconcile_log.ncl`](../../ledger/contracts/reconcile_log.ncl)'s instance), validated
each write against [`council.ncl`](../../ledger/contracts/council.ncl)'s
`DecisionLedger` — **NOT a Nickel file**. House rule: contracts are Nickel, data
instances are YAML.

**To record your assent**, place your seat id in the relevant `Decision`'s `assent`
array, the decision itself carrying a non-empty `grounding` (a decision-level field, not
a per-assenter one), and satisfying that type's delegation rule. The contract
owns the field shape (`Decision = {id, type, assent, barred, verdict, grounding}` — see
[`council.ncl`](../../ledger/contracts/council.ncl)); your obligation is the ACT:

- Assent without `grounding` FAILS the export — there is no bare "yes."
- A `'merge` FAILS without the maintainer's recorded assent (the id `"maintainer"`); a
  `'dag-amendment` or `'close` FAILS without the head's (the id `"human"`). Place those
  exact ids where the guard expects them.
- A barred seat in `assent` FAILS. Do not record an assent you are barred from.

**To record a finding**, write it per [`findings.ncl`](../../ledger/contracts/findings.ncl):
a resolved finding NAMES the evaluator that closed it (the Verification Dual — a finding
closed by review names the review; one closed symbolically names the gate). Vestigial
residue the auditor surfaces is captured here too, so it cannot be dropped.

Write the YAML; let `nickel export` gate it. The contract is applied externally — the
instance carries no Nickel logic and cannot self-bind.

---

## Prime Directives

1. **INDEPENDENT_BEFORE_DELIBERATE:** Deposit your own assessment before you read any
   sibling's. Reading first collapses decorrelation and is a barring trigger.

2. **DEPOSIT_DURABLY:** Commit your assessment, as it is made, into the testimony
   namespace — `.ledger/deposits/<topic>/<signer>/` — as a `deposit.ncl`-conformant
   YAML signed by your seat (the pen law:
   [`docs/entries.md`](../../docs/entries.md)). Scratch is the mirror, the ledger
   is the record. The auditor reads the durable trail; an ephemeral one defeats
   the check.

3. **PACT_GATES_ADVANCEMENT:** Never advance a gate while any R/I/U or constraint you
   hold is prose-only, ungrounded, unsignposted, or stale. A held item that is not a
   passing contract BLOCKS — it is not "noted."

4. **ROUTE_PER_THE_TABLE:** Act only with the assent your decision-type's delegation
   rule requires. A move lacking it is INVALID; never invent a rule for an unlisted
   type or substitute seniority for a missing co-signer.

5. **GROUNDED_ASSENT_ONLY:** Record assent only with non-empty `grounding` and only
   where you are not barred. There is no bare "yes"; a merge or terminal decision
   carries its named co-signer id (`"maintainer"`, `"human"`) regardless of class.

6. **EVIDENCE_OVER_AUTHORITY:** Overrule and be overruled only on grounded
   counter-evidence, never on standing — in both directions, the head included.
   Non-convergence escalates to the human; it is never a seniority tie-break.

7. **AUDITOR_INDEPENDENCE:** The process-auditor reads the ledger and deposits
   directly and cannot be convened or suppressed by the composer; composer-misconduct
   escalates straight to the head. Do not route the audit through the hub it checks.

8. **DATA_IS_YAML_LAW_IS_NICKEL:** Deposits and the decision ledger are YAML instances
   validated by an externally-applied contract. Never hand-write Nickel into a record;
   never treat a contract file as a place to store data.

### Protocol Violations (FORBIDDEN)

| Violation | Why it's wrong |
| :--- | :--- |
| Reading a sibling's deposit before writing your own | Collapses role-decorrelation into one basin; the value of the seat is gone |
| Advancing a gate with a prose-only R/I/U | Re-creates the exact failure the pact makes structurally impossible |
| Recording assent with empty `grounding` | A bare "yes" the contract rejects; status without evidence |
| Acting beyond your assent class | Unilateral capture — the move is INVALID and a barring trigger |
| Writing the decision ledger as a Nickel file | Data is YAML; the contract is the external gate, not the record |
| Routing the process-auditor through the composer | Lets the hub suppress its own audit; breaks the only check on the hub |

---

## MANDATORY HALT Points

Freeze and surface — do not guess — when:

1. A decision-type has no delegation rule in the constitution (ungoverned: the export
   FAILS; you cannot route it).
2. A required co-signer (maintainer consent, head ratification) is unavailable at a
   merge or terminal gate.
3. Deliberation does not converge on grounded evidence — escalate to the head (the
   Verification Dual's human rung).
4. The pact cannot be satisfied because a held item resists contracting — surface the
   item, do not advance past it.
