---
name: harnesses
description: "Generate project-adapted enterprise-configuration assets (CI, scanning, supply-chain, content) into /harnesses, record them in the lock file, and surface each for approval so the engine can verify them."
---

## User Input

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

`/akka:harnesses` is a generator. It writes the enterprise-configuration assets a
project needs — CI workflows, scanner configs, supply-chain steps, content style
packages — into `/harnesses/<surface>/`, records what it generated in
`.akka/harnesses.lock`, and surfaces each asset for approval. The engine does not
generate anything and does not call a model: generation lives here in the
assistant; the engine detects surfaces, verifies the generated assets
deterministically, and records attestations you submit. This command is paired
with the harness exit-condition family (activated / configured / attested), the
same way `/akka:specify` is paired with the functional and data-integrity family.

## The three auditor kinds

Every required surface resolves as one of three kinds. Which one it is decides
whether you generate an asset and how the engine verifies it.

| Kind | Where the check runs | Asset generated | How it resolves |
|---|---|---|---|
| Introspective | the project's own tree (a compiler, test runner, linter, prose linter over `docs/`) | none | verified locally — green or red |
| Provisioned | a generated asset (a CI workflow, scanner config, IaC module, style package) wired to an external system | yes — one per surface under `/harnesses/<surface>/` | verified where inspectable — present, correct, and enforcing — otherwise `open` with the tool or environment gap named |
| Delegated | a check that runs only in an external system, or needs a judgment the engine cannot make | a config stub, optional | resolved by an attestation you submit; otherwise stays `open` with `needs-user-action` until the receipt is recorded |

## Outline

1. **Detect the required surfaces.** Read the policy's `required_surfaces` (the
   enterprise-mandated set: SAST, secret scanning, SBOM, signing, identity, and
   so on). Detect the project's own surfaces from tree markers (a GitHub
   directory, `pom.xml`, `package.json`, `go.mod`). The gap is the set of
   required surfaces with no covering harness. Introspective surfaces (a coverage
   gate a local tool already runs) need no asset — note them and move on.

2. **Generate a project-adapted asset for each provisioned gap.** For each
   uncovered provisioned surface, write one asset into `/harnesses/<surface>/`,
   adapted to this project's modules and detected surfaces — not a copied
   template:
   - `/harnesses/ci/` — a CI workflow that runs the enterprise-mandated steps and
     the `akka` conformance step, gating the merge.
   - `/harnesses/scanning/` — the mandated SAST / secret-scanner config, pointed
     at this project's modules.
   - `/harnesses/supply-chain/` — SBOM and signing steps wired to the mandated
     registry or signing service.
   - `/harnesses/content/` — the content style package (`.vale.ini`, `styles/`)
     for the content governance family, plus `diagram_check.py` copied from
     `plugins/akka/harnesses/content/` — the structural checker for generated
     diagrams. Both feed CONTENT-LANGUAGE; see `/akka:docs`.
   Use the enterprise's target values, mandated vendors, and privileged endpoints
   where the policy supplies them. Leave the last-mile connection the developer
   alone can make — adding a secret, enabling a workflow, linking an account — as
   an explicit instruction, not a fabricated credential.

3. **Write the lock file as the currency contract.** Write `.akka/harnesses.lock`
   recording the policy version and, per asset, its path, the surface it covers,
   and a content signature. This is what lets the provisioned auditor prove
   currency: it reds when the policy version moves, when the surface signature
   changes, or when a managed asset was hand-edited. Presence alone never passes.
   A project that passed on day one cannot go stale silently. Do not hand-edit a
   generated asset outside this command — re-run `/akka:harnesses` so the lock
   stays authoritative.

4. **Run the adversarial self-check.** Before recording an asset as covering,
   construct the case where it passes while its invariant is false, and treat that
   case as failing:
   - a CI job that contains the mandated step but sets `continue-on-error: true`
     is not enforcing — treat it as failing.
   - a job that runs a scanner but does not gate the merge (the result is ignored,
     the step is not a required check) is not enforcing — treat it as failing.
   - a scanner config that excludes the modules it is meant to cover is hollow —
     treat it as failing.
   Fix the asset so the mandated step runs and blocks the merge, then re-check.

5. **Surface each asset at the exit-condition level.** Present the generated
   assets in plain language — *"I generated these harnesses,"* each with the
   surface it covers and how the engine will verify it — and ask the human to
   approve / adjust / skip. Never phrase this as "approve running a command"; it
   is always about the check the asset backs. Record and approve through the
   exit-condition flow (`akka_ec_capture`, then `akka_ec_approve` on approval),
   the same flow `/akka:specify` uses. Skipping a surface is a recorded waiver
   with a reason, not a silent omission.

6. **Attest delegated surfaces.** For a check that runs only in an external
   system — a scan enforced in a central SAST service, a control verified in the
   identity provider — the engine cannot inspect it. Confirm it is in place, then
   call `akka_harness_attest` with the capability / condition key and a receipt
   reference (a run URL, a ticket id, a policy id). The attestation is keyed to the
   current policy-and-surface signature, so a policy change invalidates it and the
   surface returns to `open` with reason `needs-user-action` until re-attested.
   Without an attestation a delegated surface stays `open` — it never false-passes
   to `green`.

7. **Report.** Call `akka_ec_conform`, then present `akka_ec_summary` to the user
   **verbatim** — the plain outcome. Do NOT restate internal condition ids, the
   words "auditor" / "coverage gate" / "currency", or the lock-file internals.
   Offer *"say 'show details' for the full checklist"* for the manifest.

## Key rules

- Generation is here; verification is in the engine. This command never asserts a
  surface is `green` — it writes the asset and records it; the engine's provisioned
  auditor decides present-correct-enforcing, or leaves the condition `open` with a
  reason.
- Nothing false-passes. A missing surface reds the coverage gate; a present-but-not-
  enforcing asset reds the adequacy self-check; a delegated surface with no
  attestation stays `open` with `needs-user-action`. A stall is the correct outcome,
  never a `green` pass.
- Currency is proven, not remembered. The lock file plus the provisioned auditor
  catch drift; a developer never has to notice that the policy moved.
- Same behavior wherever the exit-condition set is active. The generator and its
  checks exist in À la carte and Enforced mode alike; only ship-gating differs,
  advisory in À la carte and blocking in Enforced. Where the set is dormant the
  generator still produces its assets, but records no conditions and no gate —
  the harnesses are the deliverable, not the checking of them.

## Done When

- [ ] `required_surfaces` was read from policy and the uncovered set was computed against the project's detected surfaces; introspective surfaces were noted and skipped (no asset).
- [ ] For each provisioned gap, a project-adapted asset was written into `/harnesses/<surface>/`, using the enterprise's target values and mandated vendors, with the developer's last-mile step stated explicitly.
- [ ] `.akka/harnesses.lock` was written with the policy version and a per-asset record (path, surface, content signature) as the currency contract.
- [ ] The adversarial self-check ran on every generated asset; any asset that had the step but set `continue-on-error` or did not gate the merge was treated as failing and fixed.
- [ ] Each generated asset was surfaced at the exit-condition level for approve / adjust / skip via `akka_ec_capture` / `akka_ec_approve`; a skipped surface was recorded as a waiver with a reason.
- [ ] Every delegated surface was attested via `akka_harness_attest` with its capability / condition key and a receipt reference, or left `open` with reason `needs-user-action` — never marked `green` without an attestation.
- [ ] `akka_ec_conform` was called and the plain `akka_ec_summary` (never internal ids or the word "auditor") was shown to the user.
