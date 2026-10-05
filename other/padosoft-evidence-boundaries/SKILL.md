---
name: padosoft-evidence-boundaries
description: >-
  Use this skill when something is being declared done, safe, covered or production-ready and you need to
  know what actually proves it: a release or compliance gate, a security or DR claim, a "CI is green so we
  can ship", a "the job succeeded", a "the tests pass so it works", a coverage or mutation number, a signed
  artifact, an integration verified against an emulator or a mock. It names the claim, names what would
  prove it, and finds the gap where a cheaper artifact was accepted in place of the expensive one. Do not
  use it to write tests (padosoft-test-integrity), to build a CI workflow (padosoft-ci-workflow-gates), or
  to debug a failing check — this is about whether a passing one means anything.
license: MIT
compatibility: >-
  Language- and stack-agnostic. The examples come from storage, identity, telemetry, queue and release
  pipelines because that is where the substitution is easiest to make.
metadata:
  version: 0.3.0
  author: Padosoft
  summary: Name the claim, then name what would prove it.
  profiles: core
  scope: global
  repository: https://github.com/padosoft/skills
  keywords: evidence, proof, release gate, compliance, audit, verification, coverage, signing, boundary
---

# Evidence boundaries

Almost every false "done" has the same shape: a claim was made about the expensive thing, and a **cheaper
artifact** was accepted as proof of it. The artifact is real, it was produced honestly, and it does not
demonstrate the claim.

**The rule: name the claim, then name what would prove it. If what you have is cheaper than the claim, the
claim is asserted, not proven.**

---

## 1. The substitution table

The recurring pairs. Read the middle column as what you are entitled to say, and the right one as what will
be said anyway.

| What you have | It proves | It does **not** prove |
|---|---|---|
| A green run against an emulator or compatible implementation | the request/response shape | the real provider's identity, policy, retention, encryption |
| A static graph, topology or config validation | the transitions are **declared** consistently | that anything ever reached them |
| A write request the API accepted | the option was transmitted | that the provider applied it — read it back |
| A signature on a manifest | the manifest is authentic | the content the manifest points at |
| A digest field, a reference, a ticket id | something was **named** | integrity: nobody recomputed anything |
| Deployment files, linted and secret-scanned | they parse | that a scrape, an export or an alert works |
| An injected or faked client in a test | your control flow | the real storage, transport or locking semantics |
| A parsed report from an external tool | the tool ran and said something | that the finding is fixed, or safe to close |
| Exit code 0 | the process ended | that the effect happened |
| A declared number (coverage, score, RTO) | somebody wrote a number | that it was derived from this run |
| A skipped optional check | nothing | **less than nothing** — it reads as a pass |

The last row is the one that does real damage, because it is the only one that looks identical to success.

**When the claim sits in a specific domain** — storage and encryption, identity and access, telemetry,
queues and effects, supply chain and release, money and settlement, data protection — open
`references/rules.md` and read that one section: it lists the substitution offered in that domain and the
part of the claim it leaves untouched.

## 2. Six questions that turn an artifact into evidence

1. **Who produced it?** An artifact a contributor can regenerate locally proves a local fact. Release
   evidence comes from a protected producer.
2. **What is it bound to?** Commit, tool version, command, key identity, tenant, environment. An unbound
   report is a report about *something*.
3. **Is it verified again at read time?** Writing a digest at creation protects nothing unless the reader
   recomputes it and refuses on mismatch. Every consumer that turns records into a decision verifies first.
4. **What is the boundary of the claim?** One successful path is evidence for that path. It is not evidence
   for rotation, failover, logout, replication or the next tenant.
5. **Does it fail closed?** When the environment is incomplete, the run must refuse. A local skip is not
   production evidence, and a green skipped gate is worse than a red one.
6. **Could all of it be true and the system still be broken?** If yes, you have found the gap. Say what
   would close it, even if you do not close it today.

## 3. When one path hides another, prove each leg

An exporter accepting a span does not prove the metrics endpoint can be scraped, and a successful scrape does
not prove delivery downstream. Wherever a chain has independent legs, assert **each** one; a single end-to-end
"it worked" hides which leg is actually carrying the result — and which one has been broken for months.

Corollary: read **both** output streams when you assert on a tool's own diagnostics. A journey that watches
only stdout reports a false negative on a tool that writes its confirmation to stderr.

## 4. Keep the gates separate, or the cheap one decides

| Keep apart | Because |
|---|---|
| synthetic CI ↔ protected provider evidence | one is free and constant, the other is the truth |
| static validation ↔ live journey | a generated path can look complete with nothing observed |
| parsing ↔ gating | a parser that also decides hides its own failures |
| execution ↔ the report gate | a score becomes evidence only at an explicit boundary |
| the library contract ↔ the shipped command | a contract with no executable command is bypassed operationally |

Merging two gates does not average their strength; the weaker one becomes the verdict.

## 5. Evidence at rest

- **Canonical bytes.** Publish the exact bytes the hash was computed over. A convenience writer that re-runs
  formatting or redaction on the way out changes the content after the chain was built.
- **Strict field sets.** Canonicalising only the fields you know about leaves an unknown property that is
  still displayed to an operator and still consumed downstream — and is covered by no signature. Reject it.
- **Producer-executable canonicalisation.** If the producer cannot run the same normalisation the verifier
  runs, the two will disagree exactly when it matters.
- **Redaction must not mutate identity.** A DLP pass that rewrites a checkpoint key, a run id or an audit
  hash breaks the chain it was protecting. Identity fields are excluded by construction, not by luck.


### When the evidence is a signed record

Four invariants, each of which has been violated by a verifier that reported everything as fine:

- **Sign the whole persisted object**, minus the signature field itself. Signing only the fields you
  enumerate leaves the removal of a key, or the addition of one, invisible — and a verifier will then count
  an emptied record among the valid ones, certifying as intact a row somebody hollowed out.
- **Canonicalise deterministically**: sort maps recursively, leave lists in their order because there the
  order is the data, and normalise the container types before hashing, so the producer holding a native
  object and the verifier holding what came back from the parser compute the same bytes. A signature that
  is not reproducible generates **false tamper alerts**, which is the fastest way to get an integrity check
  switched off.
- **A missing signature is an anomaly, not an exemption.** If unsigned records can be explained away, the
  mechanism is bypassed by deleting two fields instead of forging one.
- **Deletion at the edges leaves no gap.** Removing the first or last records of a file, or the file
  itself, breaks no sequence. Detect it with an external anchor recorded **after** the write succeeds, and
  by checking that the last identifier of one period and the first of the next are adjacent.


## 6. Small ones, same class

- **A timing field that is merely below the objective can still be false**: derive elapsed time from trusted
  timestamps and reject disagreement, rather than trusting the number that was submitted.
- **A successful dump is not a restore.** The evidence is a fresh read from the restored copy.
- **A test file that exists is not a test that runs**: the manifest or script has to execute it.
- **A number derived from a filter is not a number derived from the run.** Coverage is derived, never
  declared.
- **"Verified locally" closes nothing.** A replay against a local fixture and a probe against the real system
  are different claims with different exit codes.

## 6b. Grade every claim, in the words you write

An assessment is read as prose, and prose does not distinguish what you measured from what you inferred
unless you make it. Four grades, and the wording is the grade:

| Grade | How it is written | Earned by |
|---|---|---|
| **Verified** | "is", "verified on…" | read, run, queried, reproduced |
| **Attributed** | "attributed to…, with an offset of N" | derived from a reconstruction, with the uncertainty measured |
| **Suspected** | "suspected", "a precondition" | consistent with the symptom, never reproduced |
| **Not verified** | "not verified: …" | a hypothesis, or behaviour nobody observed |

Then read your own text for the words that assert more than you can show — **exact, always, never,
deterministic, unresolved, the cause is** — and give each one its evidence or rewrite it. A conclusion
that is right in substance and overstated in wording gets corrected by whoever checks it, and costs more
than being wrong would have. See **`padosoft-crash-triage`** for the same discipline applied to a defect
nobody could reproduce.

---

## Gotchas

- **The artifact is usually honest.** Nobody faked anything: the emulator really was green. The defect is in
  the sentence written above it, so review the *claim*, not the evidence.
- **Two weak proofs do not make a strong one** unless they are independent. Two checks reading the same
  fixture are one check.
- **The cheap gate runs on every push and the expensive one runs rarely**, so the cheap one silently becomes
  the definition of "working". Decide that on purpose, and name what the cheap gate does not cover.
- **Documentation goes stale into a risk.** A process document describing evidence that is no longer produced
  is worse than no document — see **`padosoft-docs-match-code`**.
- **An automated decision can be genuine without fabricating evidence.** Automating the verdict is fine;
  automating the *proof* is how a system starts certifying itself.

## Checklist

- [ ] The claim is written in one sentence, and what would prove it in the next
- [ ] Producer identity, and the bindings: commit, version, command, key, tenant, environment
- [ ] Read-time verification wherever a digest, signature or chain exists
- [ ] The boundary of the claim stated explicitly — including what it does not cover
- [ ] Incomplete environment fails closed; no gate can pass by skipping
- [ ] Independent legs asserted independently
- [ ] Cheap and expensive gates kept separate, and the gap between them written down
- [ ] Numbers derived from the run, never declared
- [ ] At least one honest "could this be true and the system still broken?"

## Final report

```
Claim: <what is being asserted>
Evidence held: <artifact> — produced by <who/where>, bound to <commit/version/tenant/key>
Proves: <the narrow thing>
Does not prove: <the rest of the claim>
Verified at read time: yes | no
Fails closed: yes | no (what happens when the environment is incomplete)
Gap: none | <what is still unproven, and what would close it>
```
