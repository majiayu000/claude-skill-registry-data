---
name: tradecraft-complex-engagements
description: >
  Structure and discipline for complex, multi-stage targets — where the path is a chain of
  several bugs across multiple hosts, needs source review / custom exploit work, and spans
  sessions. Load when a foothold needs chaining, work spans multiple hosts, you're deep in
  dead-ends, or "stuck", "chain", "multi-host", "hard target".
domain: tradecraft
type: methodology
stability: locked
modes: [pentest, bugbounty]
schema_version: 1
---

# Complex, multi-stage engagements

Hard targets differ in *kind*, not just difficulty. The path is usually a chain of 2–4 bugs
wrapped in deliberate dead-ends — sometimes needing source review, custom exploit work,
reversing, or a crypto attack — and it often spans multiple hosts and sessions. Wins come from
disciplined enumeration and ruthless dead-end tracking, not a bigger exploit. In-scope,
authorized targets only (see `tradecraft-scope-roe`).

## Keep a working record (per engagement)
```
engagement/
  state.md          # live status + a "haven't tried yet" list
  deadends.md       # ruled-out leads WITH the reason each was dropped   ← the key habit
  chains/           # working exploit chains / PoC drafts, one link at a time
  findings/         # confirmed findings + evidence
  hosts/<host>/     # one subdir per internal host reached
```

## Extended method
1. **Exhaustive recon.** Every port, vhost, parameter, version string. The lead is often in
   the thing you skipped (`recon-arsenal`, `recon-content-discovery`).
2. **Clue harvesting.** Log everything, including what looks irrelevant — odd headers, unusual
   filenames, custom apps, strange responses.
3. **Foothold by chain.** Expect to combine bugs (e.g. SSRF → internal service →
   deserialization → RCE). Build it in `chains/`, verifying each link before adding the next
   (`exploit-chaining`).
4. **Stabilize + situational awareness.** Get a stable shell, then map users/services/internal
   network before moving.
5. **Pivot / lateral.** Enumerate internal reachability; one `hosts/<host>/` per host; repeat
   the loop per host (`network-pivoting-tunneling`).
6. **Privilege escalation (often custom).** Standard checks first, but be ready for a
   target-specific vector — a custom SUID binary, a bespoke service, an ACL path (`privesc-arsenal`).
7. **Write up the chain.** Document it end to end; each link needs reproduction steps and evidence
   (`reporting-bug-bounty-writeup`).

## Dead-end discipline (the skill that separates good operators)
- The moment a lead dies, write it in `deadends.md` **with why** it's ruled out. This stops you
  re-walking dead-ends over a multi-day engagement and reveals what you actually haven't tried.
- Keep a live "haven't tried yet" list in `state.md`. When stuck, work that list before reaching
  for exotic exploits.
- Truly stuck? Re-run enumeration on the least-examined service, diff against earlier output, and
  re-read the clue log. The path is usually already in your notes.

## Custom-exploit workflow
Read any public PoC fully before running it and note the source (`exploit-poc-development`). When
a PoC needs adapting, keep a clear record of what changed and why — that becomes report content
and a capture-worthy new skill. Review application source when you have it: auth logic, input
handling, serialization, crypto (`code-review-methodology`).

## Capture what you learn
When an engagement teaches a reusable technique (a novel chain, a bespoke privesc, a crypto
attack), add it as a new `stability: learning` technique skill under the right domain so future
work benefits (see the library `README.md`).

Working style: enumerate first, track dead-ends, build chains incrementally, and explain your
reasoning — on complex targets the reasoning *is* the skill.
