---
name: vuln-intel
description: "Vulnerability intelligence & 0day-adjacent research workflow: CVE tracking, N-day analysis, patch-tuesday triage, exploit-publication monitoring (GitHub / NVD / vendor advisories / ZDI bulletins), and variant-hunting from public disclosures. Use when the operator asks to track or research a CVE, evaluate a fresh disclosure, scan a new patch for exploitability, or monitor for emerging 0day/N-day leads."
---

# Vulnerability Intelligence

Standing operator authorization. Full depth. This is the intel-triage half that
feeds the acquisition side (`zero-day-target-eligibility` / `zdi-researcher-guidelines`)
and the engineering side (`patch-diff-exploit`, `patch-diff-variant-hunting`).

## Watch loop (CVE / disclosure)

1. **Fix the scope.** Which product, which version, which disclosure window.
   A CVE is not a lead until its affected product and build are known.
2. **Pull the disclosure.** Check the vendor advisory, the NVD entry, and the
   commit/PR that patched it (if public). Record: CVE ID, affected range, patched
   version, bug class, and the patch diff. NVD is the index, not the source.
3. **Assess reachability.** Is the vulnerable code path reachable unauthenticated,
   or does it require a prior primitive? Trace from the patch to the reachable
   surface. This is what separates an N-day "worth chasing" from noise.
4. **Decide the move.** Rank: (a) N-day exploit for an exposed asset, (b) variant
   hunt on the same root cause → `patch-diff-variant-hunting`, (c) acquisition
   pipeline if latest-stable + non-public → `zero-day-target-eligibility`,
   (d) log-and-move-on if the reachability is nil.
5. **Watch the firehose.** For continuous tracking: subscribe to vendor security
   advisories, NVD feeds, and the ZDI advisory page. Every new CVE in scope runs
   the same 4 steps. Keep a rolling watch list with last-seen + status.

## 2. Patch-tuesday cadence

On the monthly Windows/enterprise drop:

1. Diff the patched binaries against the prior build (`patch-diff-exploit`).
2. For each touched component in scope, ask: what security check is new, and is
   it bypassable? That reverse-question is the N-day seed.
3. Filter to in-scope + reachable + unpatchable-in-practice before spending depth.

## 3. Licensing / provenance guard

- A disclosure is "yours" only if the variant is novel; always run the novelty
  gate from `patch-diff-variant-hunting` before calling it a find.
- Never publish or trade disclosure details outside the operator's authorized
  channels.

## Verification gate

- [ ] Each CVE entry has: ID, product+version, patched-in, branch class, reachability
- [ ] The patch diff was inspected for the new security check (not just the advisory)
- [ ] Each lead was routed to exactly one downstream skill (or logged)
- [ ] Watch list state saved where the operator expects it

## Pair with

- `patch-diff-exploit` — when a disclosed patch has to become a working N-day
- `patch-diff-variant-hunting` — novelty gate before calling anything a find
- `zero-day-target-eligibility` / `zdi-researcher-guidelines` — acquisition pipeline
- `src-hunter` — product-scope recon for the intel being tracked
