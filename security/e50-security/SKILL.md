---
name: e50-security
description: "Audit the security a space communication system applies to the data it carries under ECSS-E-ST-50C clause 5.8.3, which asks that protection match how sensitive that data is. Compare each flow's declared services against what its sensitivity group needs — integrity, authentication, replay protection, confidentiality — because none of them substitutes for another; price the tag, initialisation vector and replay counter against every frame; and work out how long one key lasts before the counter space or the per-key frame limit runs out. Use when reviewing a link security design or sizing a rekey interval. Trigger: ecss, e-st-50c-clause-5-8-3, space-link-security-services, security-field-frame-overhead, replay-counter-width-sizing, rekey-interval-lifetime, data-sensitivity-service-mapping."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: ecss
    reference-only: true
gated: false
domain: space-systems
pack: space-systems
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
clauses:
  - standard: ECSS-E-ST-50C Rev.2
    clause: 5.8.3
    items: [a]
    relation: verifies
metadata:
  domain: space-systems
  subdomain: ecss
  tags: [ecss, e-st-50c-clause-5-8-3, e50-security, space-link-security-services, security-field-frame-overhead, replay-counter-width-sizing, rekey-interval-lifetime, data-sensitivity-service-mapping]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Communications — Security (space-systems/ecss/e50-security)

Use when the data a communication system carries has to be protected in
proportion to its sensitivity, per ECSS-E-ST-50C clause 5.8.3 — which
services each flow actually gets, what they cost every frame, and how long a
key survives the traffic it protects.

## Domain quick reference

- The four services stop four different attacks and none of them covers
  another. Integrity detects corruption, authentication says who sent
  it, replay protection stops a valid old frame being played again, and
  confidentiality keeps a listener out. A design that encrypts and does
  not authenticate is open to an attack encryption never addressed.
- Protection is proportional, which makes the requirement a mapping
  rather than a level. Each sensitivity group names the services it
  needs, and a heavier group keeps everything a lighter one asked for,
  so the check is a set comparison per flow and not a single verdict
  for the link.
- Applying more than a group needs is a cost, not a defect. It belongs
  in the report as a service beyond the requirement so the overhead it
  buys is visible, but it never fails the assessment.
- Security overhead is per frame and permanent. The tag, the
  initialisation vector and the replay counter are charged on every
  frame for the life of the mission, so the overhead fraction and the
  payload rate left behind are what a data budget has to use.
- Replay protection has a lifetime, and it is usually shorter than the
  key's. Once the counter space is exhausted the numbers repeat, and a
  repeated counter under the same key is exactly the condition replay
  protection existed to prevent — so the counter width, the frame rate
  and the rekey interval are one calculation, not three.
- Two different bounds can end a key, and the remedy depends on which
  one binds. A narrow counter is fixed with more bits; a per-key frame
  limit from the cryptographic design is not, and saying which bound
  binds is what makes the finding actionable.

## Workflow

1. Describe each flow by name, sensitivity group and declared services.
   Reject an unknown group or an unrecognised service name rather than
   passing it through.
2. Grade the ground network separately from the flows it carries. List
   the security mechanisms it provides so that nobody unauthorised
   reaches its facilities to command the spacecraft or take its data,
   and hold each mechanism to naming which of those two it denies. A
   flow whose services are all present says nothing about an operator
   console an unauthorised person can reach.
3. Compare the declared services against the group's required set;
   report present, missing and beyond-requirement separately.
4. Sum the tag, initialisation vector and replay counter into a
   per-frame security overhead, treating a zero width as an absent
   field rather than an error.
5. Express that overhead as a share of the whole protected frame and
   compare it with the allowance under a relative tolerance, so a
   design landing exactly on the allowance passes on every host.
6. Report the payload rate the link delivers once the frames are
   protected, which is the figure a data budget needs.
7. Compute the key lifetime as the smaller of the replay counter space
   and the per-key frame limit, divided by the frame rate, and name
   which of the two bound it.
8. Compare that lifetime against the time the design has to go without
   rekeying. Where the counter binds, give the width that carries it;
   where the key schedule binds, say so instead of widening a counter
   that was never the problem.

## Obligations

| Item | Step |
|---|---|
| ECSS-E-ST-50C Rev.2 5.8.3a | 2 |

## Pitfalls

- Treating confidentiality as the whole of security. Encryption says
  nothing about who sent a frame or whether it has been played before,
  and a flow that needs authentication is not served by a cipher.
- Grading the link instead of the flows. Sensitivity is a property of
  the data, so a link carrying routine telemetry and critical commands
  has two different requirements on it at once.
- Failing a flow for being protected beyond its group. Extra protection
  costs overhead and belongs in the report, but it is not a defect and
  reporting it as one drives designs the wrong way.
- Budgeting the link at capacity. Every frame pays its tag, vector and
  counter, so the delivered payload rate is lower by the overhead
  fraction, permanently.
- Sizing the replay counter from the frame size. What matters is the
  frame rate against the rekey interval: a wide counter on a fast link
  can still wrap under one key, and a wrapped counter under one key
  ends replay protection.
- Answering an exhausted key lifetime by widening the counter without
  checking which bound binds. Where the per-key frame limit is the
  smaller of the two, extra counter bits change nothing at all.

## Behavior contract (gate 3)

Sensitivity-group and service-name validation, the per-group service
set comparison including beyond-requirement services, the per-frame
overhead and its exact allowance boundary, the delivered payload rate,
the key lifetime with its binding bound and the integer replay-counter
sizing across the power-of-two boundary are exercised by the gate 3
contract test:
scripts/test_e50_security.py against
scripts/e50_security_logic.py (stdlib unittest, offline).
Run:
python3 scripts/test_e50_security.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
