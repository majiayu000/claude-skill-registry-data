---
name: gate-authoring
description: Author or tighten a mechanical gate so a defect class cannot recur. Use after fixing a bug whose class will return, or when a review found a contract nothing enforces.
triggers:
  - add a gate
  - tighten the gates
  - make this enforceable
  - stop this class recurring
  - why did the gates miss this
  - add a semgrep rule
  - add a conformance suite
  - this check is self-attested
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - find_references
  - run_command
  - write_file
  - search_replace
---

<!-- Provenance: written from the 2026-08-29 subagent-stall investigation, where 13 reachable bugs shipped through a full gate suite. Every rule below is a lesson that batch paid for. -->

# Gate Authoring

## Purpose

Turn a defect class into something a machine refuses. A gate that cannot fail
is documentation wearing a gate's clothes, and this repository has shipped
serious bugs behind exactly that.

Use this after a `fix` whose class will recur, or when a review found a
contract that only prose enforces.

## The one test of a gate

**Can it fail, and did you watch it fail?**

A gate you have not seen reject something is not a gate. Before you commit
any gate in this skill, you must have run the mutation: break the thing the
gate protects, watch the gate reject it, restore, watch it pass. Record that
in the commit body. `.agents/rules/20-agent-quality.md` already says
inspection-only mutation proof is invalid; this is that rule applied to the
gate itself.

## Choosing the layer

Match the gate to what the defect actually is. Picking the wrong layer
produces a gate that is either noisy or blind.

| The defect is… | Gate layer | Where it lives |
|---|---|---|
| A syntactic pattern, always wrong | Semgrep rule | `semgrep/agent-standards.yml` + a probe |
| A contract two implementations must both honor | Conformance suite | one `_test.go` table over every implementation |
| A behaviour only real I/O exposes (timers, sockets, subprocesses) | Test against a real server/process | `httptest`, real transport, real `exec` |
| A repo-shape or policy rule | Script gate | `scripts/check_*.py` + a contract test |
| A claim an author makes in prose | Validate the claim's content | e.g. the commit-msg trailer rules |
| A fast regression worth catching at commit time | Pre-commit subset | `scripts/git-hooks/pre-commit`, keyed on staged dir |

**Prefer the highest-signal layer that can actually see the defect.** A
behavioural contract cannot be caught by grep, and a syntactic ban does not
need a test suite.

## The sibling rule

This repository's most expensive recurring defect is a contract enforced in
one implementation of an interface and silently absent from another. Seven
bugs of that one shape shipped together in `provider.Completer`.

**When an interface has more than one implementation, the gate is a
conformance suite, not another per-implementation test.** A per-implementation
test answers "does this one work?". Only a table over every implementation
answers "do they agree?", which is the question that keeps being wrong.

Write it so a new implementation must join the table or its absence is
visible. Assert through the exported interface, not internals.

Reference: `internal/provider/completer_conformance_test.go`.

## Do not test the network with a fake

For anything involving a timer, a socket, a subprocess, or a partial read,
**a hand-written fake cannot fail.** Fakes return whole answers instantly, so
they are green through every stall, every half-sent body, and every timeout
misclassification.

Use `httptest` with a real `http.Transport`, or a real child process. If you
need a stall, flush headers and then block on a channel the test releases —
and register the release cleanup LAST so it runs FIRST, because `srv.Close`
waits for the handler and LIFO cleanup order will otherwise deadlock the test
binary rather than the product.

Reference: `internal/provider/anthropic_watchdog_test.go`.

## Validate content, never presence

A required field, trailer, or section that is checked only for existence
decays into a placeholder. If you are gating on something an author writes,
gate on what it *says*:

- a named test must resolve to a real `func Test…`;
- a named class must exist in `.agents/quality/defect-taxonomy.md`;
- a claimed search must report a **count**, not an assertion that a check
  happened.

Keep an explicit `none (<reason>)` escape so the honest small case stays
cheap, and put the rules in `.mivia/policy/*.json` so the gate stays
data-driven.

Reference: `scripts/git-hooks/commit-msg` `check_trailer_content`.

## Procedure

1. **Name the class in terms of mechanism, not symptom.** "A body read with no
   bound of its own", not "the Anthropic client hung". The mechanism is what a
   gate can match; the symptom is not.
2. **Find the boundary at which the class stops being possible.** That is where
   the gate goes. If there is no such boundary, say so — that absence is
   itself a finding about the design.
3. **Pick the layer** from the table above.
4. **Write the gate and run it against the CURRENT tree first.** A new gate
   that finds existing violations has already earned its place; fix them in
   the same change. A gate that is clean on arrival still needs its mutation
   proof.
5. **Mutation-prove it.** Break the protected thing, watch the gate fail,
   restore, watch it pass. Never skip this for "obvious" gates.
6. **Register it everywhere it must be known** (see checklist).
7. **Record the class** in `.agents/quality/defect-taxonomy.md` if it is new,
   and the trap in `.agents/memories/` if it will surprise the next reader.

## Registration checklist

A gate nobody runs is not a gate. Depending on layer:

- **Semgrep rule** → add the rule to `semgrep/agent-standards.yml`; add a
  `PROBES` entry (violation + clean fixture) to
  `scripts/check_semgrep_probes.py`; if `scripts/test_semgrep_rules.py`
  asserts a rule-id list, add it there. Run both. Note `make semgrep` uses
  `--disable-nosem`, so a rule must be clean by construction — there is no
  suppression escape.
- **Script gate** → wire into the `verify` chain in `Makefile`; add a contract
  test under `scripts/test_*.py`; if `scripts/verify_agent_config.py` asserts
  the Makefile target list, add it there.
- **Test gate** → if it is fast and guards a live class, add it to the staged
  directory map in `scripts/git-hooks/pre-commit` so it runs at commit time.
  Keep the whole staged subset in the low seconds.
- **Policy** → put thresholds and lists in `.mivia/policy/*.json`, never inline
  in the hook or script.

## Anti-patterns

- **A gate that only greps for the symptom string.** It passes the moment the
  wording changes.
- **Raising a baseline to make a gate pass.** `.mivia/policy/go-structure.json`
  has a baseline map; adding to it to silence a failure converts a gate into a
  record of defeat. Split the file instead.
- **A gate with no probe.** If the gate stops matching, nothing notices.
- **Gating on a count you did not measure.** If you assert "found 0 further
  sites", you must have run the search.
- **Adding a weaker duplicate of an existing gate.** If a conformance suite
  already catches the class behaviourally, a syntactic rule that catches a
  subset adds noise, not safety — unless it catches the defect at authoring
  time in code the suite does not execute. Say which applies.

## Report shape

State, briefly:

- the class, named by mechanism;
- the layer chosen and why that layer can see this defect;
- the mutation you ran and what the gate did (this is the evidence — without
  it the gate is unproven);
- anything the gate found in the current tree;
- where it is registered;
- what the gate still cannot catch.
