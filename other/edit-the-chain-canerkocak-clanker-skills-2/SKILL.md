---
name: edit-the-chain
description: >
  Before any non-trivial edit, map the real call chain and blast radius, then
  say if the user's ask is awkward parkour through this codebase. After the
  implementation, bind every review to the exact candidate and use distinct
  contract, runtime-boundary, and evidence-audit passes. Use when editing money,
  auth, chain, withdraw, quote, fees, or multi-file work; when the user says
  edit-the-chain, parkour, blast radius, call chain, hidden assumption, or after
  "the coding is done". Slash: /edit-the-chain.
---

# Edit the chain

Do not cut until you can name who calls this, what else shares the invariant,
and whether the request is the short path or parkour. Do not call a review
complete unless its evidence belongs to the candidate being shipped.

This skill owns parkour pushback, candidate binding, and review convergence.
Read [the review convergence contract](references/review-contract.md) before a
post-change review. Delegate the map and specialist checks instead of repeating
them here:

- `semantic-blast-radius` owns the canonical impact graph.
- `ast-grep-callchain-audit` contributes structural edges to that graph.
- `call-chain-invariants` classifies the graph into applicable product surfaces.
- `yagni-anti-ceremonial` decides whether a proposed extra guard or fallback is
  part of the current contract and reachable.
- `thermo-nuclear-code-quality-review` runs the two distinct local quality
  passes on the final candidate.

## Phase 1 — Before the first edit

1. Restate the ask as one falsifiable product sentence.
2. Build one impact graph. Name the roots, producers, consumers, boundaries,
   user-facing surfaces, and focused tests with source evidence.
3. List the load-bearing assumptions. An assumption is load-bearing when making
   it false would make the quote, state transition, authorization, or UI lie.
4. Classify the requested route:

| Label | Meaning | Action |
|---|---|---|
| **SHORT PATH** | The existing owner can implement the behavior directly. | Edit that path. |
| **PARKOUR** | The request adds hops, rails, or proxy checks that do not match the real owner or oracle. | Explain the mismatch and take the direct route when already authorized. Ask only when the choice changes product behavior or authority. |
| **WRONG ORACLE** | The named signal is not what the environment uses. | Name and prove the real signal. Do not encode the proxy as truth. |

Do not start implementation before the map is coherent enough to identify the
owner and the relevant test boundary. Mark unresolved dynamic or inaccessible
edges `partial`; do not fill them from memory.

## Phase 2 — After the implementation

The review sequence is evidence-diverse, not three repetitions of one opinion:

```text
focused tests
candidate manifest
thermo pass A: ownership and boundary coherence
thermo pass B: counterfactual simplification and hidden coupling
review triad: blind contract reconstruction | runtime boundary | evidence audit
receiving gate
targeted invalidation and re-checks, if the candidate changes
```

### Freeze the candidate

Resolve the base from the active task or PR; never assume `main`. Record the
base ref and SHA, merge base, HEAD and tree SHAs, dirty-state hashes, changed
files, clean submodule pointers, and one combined fingerprint. The bundled
review harness does this and refuses to mix outputs from a changing tree. Review
a dirty nested repository separately before the parent candidate.

### Run the local review

Run `thermo-nuclear-code-quality-review` on the frozen candidate. Its two passes
have different questions. Batch accepted fixes; do not restart an exhaustive
loop after each line edit. The final code fingerprint still needs both thermo
passes because this review contract binds them to the current diff.

### Write a neutral brief

The brief supplies the user contract and canonical evidence, not the history of
the agent's opinions. Do not include prior findings, dispositions, vote counts,
"we fixed", "please verify", or "do not restore" anchoring.

```markdown
# User contract
<requested outcome, constraints, authority, and explicit non-goals>

# Reachability envelope
<target branch and deployment; rollout history; supported entry points and input
shapes; security-relevant untrusted inputs; state or formats that shipped and can
remain at cutover; explicit exclusions>

# Canonical domain contracts
<money/state/unit/authorization semantics with source locations>

# Impact graph
<graph version; roots, producers, consumers, boundaries, applicable surfaces,
and open frontier>

# Test and runtime evidence
<evidence version; commands, database/environment identity, timestamps, and
exact limitations>

# Open assumptions
<only facts that remain genuinely unproved>
```

The bundle includes an optional Codex-specific harness. It appends the exact
candidate manifest and a different role contract to each reviewer:

```bash
BRIEF=/tmp/edit-the-chain-brief-$$.md
OUTDIR=/tmp/codex-review-edit-the-chain-$$
BASE_REF=remote/base # replace with the resolved task base
EDIT_CHAIN_DIR=/absolute/path/to/edit-the-chain
"$EDIT_CHAIN_DIR/scripts/luna-review.sh" \
  --brief "$BRIEF" \
  --base "$BASE_REF" \
  --out-dir "$OUTDIR"
```

Use the task's real base. The brief and output directory must be outside the
reviewed repository. The helper requires `codex exec`; use it only in a Codex
environment. In another agent runtime, reproduce the same candidate manifest,
role separation, read-only boundary, and fingerprint checks with that
platform's native isolated-review mechanism. Do not replace those obligations
with an unbound review shortcut. The bundled helper binds the repository with
`-C`, uses read-only sandboxes, emits Markdown as `.md`, attests both
fingerprints, and detects candidate movement.

### Receive findings

External review generates claims; it does not authorize code. Run
`yagni-anti-ceremonial` for every proposed new guard, fallback, rail, or recovery
path. Bind each claim to the brief's reachability envelope before considering a
fix. Record applicability, target deployment, producer, residual inventory,
reachability, candidate causality, authority, and evidence limits. Vote count,
priority, and reviewer confidence are search signals, not authority.

Only `LIVE` or justified `RESIDUAL` findings inside the authorized contract may
change the candidate. Decline `N/A`, `CEREMONIAL`, and `THEATER`; keep
`FOLLOW-UP` outside the patch; leave `PARTIAL` as an evidence gap rather than
encoding a speculative fallback. A compatibility finding must show that the old
representation shipped to the target and can still exist at cutover. An
unsupported client shape creates no product-support obligation unless an
untrusted caller can use it to cross a security boundary.

If the candidate changes, update its manifest and invalidate evidence by its
stated invalidation conditions. Re-run the affected test or review mode. Do not
discard unrelated verified evidence merely because a comment or file changed.
Conversely, do not carry a review forward when its candidate, database,
valuation basis, or runtime boundary changed.

Completion means every acceptance obligation is either supported by current,
appropriately scoped evidence or reported `partial` with the exact remaining
gap. Another reviewer repeating the same unsupported conclusion is not
progress.

## Unmodeled assumptions

An unmodeled assumption is a fact about the chain, VM, database, library,
wallet, UI, or operating environment that is load-bearing but absent from the
specification or calculation. For every "always", "just", "only", "free",
"already covered", or "the cap is", ask:

1. What does the environment actually do?
2. Where is that effect represented in the quote, write, receipt, ledger, or UI?
3. What evidence would falsify the proposed model?

Use [the unmodeled-assumption hunt list](references/unmodeled-assumptions.md).

## User communication

Keep detailed manifests, ledgers, raw queries, and reviewer transcripts in
support artifacts. Update the user when the conclusion, scope, risk, authority,
external state, or material milestone changes. If the runtime requires a
heartbeat, use one plain sentence. Do not announce "final" until the work is
actually terminal.

## Compact output

Before editing:

```markdown
## Chain map
**Contract:** …
**Owner and oracle:** …
**Impact graph:** …
**Load-bearing assumptions:** …
**Route:** SHORT PATH | PARKOUR | WRONG ORACLE
**Coverage:** verified | partial — <gap>
```

After review, report only decision-relevant deltas:

```markdown
## Review result
**Candidate:** <base SHA, head SHA, candidate fingerprint, brief fingerprint>
**Accepted:** <finding and evidence>
**Declined:** <finding and failed applicability/reachability evidence>
**Partial:** <unclosed boundary, if any>
**Verification:** <current tests/runtime evidence>
```
