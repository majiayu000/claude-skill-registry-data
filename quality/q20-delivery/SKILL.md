---
name: q20-delivery
description: "Manage the delivery of a consignment under ECSS-Q-ST-20C clause 5.7.5: derive the shipping control documents the consignment owes from its own states rather than from a standing list, read the transport monitoring record for excursions outside each declared environmental limit, treat the unmonitored part of a journey as unknown instead of compliant, reconcile the identification on the certificate of conformity with the consignment it covers, and decide whether that certificate may be issued at all. Use when goods are about to move and the paperwork has to travel with them. Trigger: ecss, q-st-20c-clause-5-7-5, shipping-control-documentation, transport-environment-excursion, transport-monitor-coverage-gap, certificate-of-conformity-issue, consignment-identification-match."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: ecss
    reference-only: true
gated: false
domain: space-systems
pack: space-systems
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: space-systems
  subdomain: ecss
  tags: [ecss, q-st-20c-quality-assurance-scope, q20-delivery, shipping-control-documentation, transport-environment-excursion, transport-monitor-coverage-gap, certificate-of-conformity-issue, consignment-identification-match]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Delivery Control (space-systems/ecss/q20-delivery)

Use when the task is the clause 5.7.5 delivery step of ECSS-Q-ST-20C: a
prepared consignment is about to move, the transport is carried out against the
transport standard of the Q-ST-20 series, and the certificate of conformity has
to be issued — or withheld — on what the journey actually shows.

## Domain quick reference

- The shipping document set is derived from the consignment, not chosen from a
  standing list. Crossing a border adds a customs declaration and an export
  authorisation; hazardous contents add a dangerous-goods declaration; a
  temperature or shock limit adds the monitoring record; an oversize lift adds
  the rigging plan.
- A declared environmental limit only means something if something recorded
  against it. An excursion is per parameter and per reading: three shocks over
  the bound are three excursions, and the worst one is what the receiving
  inspection has to be told about.
- A reading that lands exactly on a bound is inside it. The limit is the limit,
  and the few ULPs a sensor conversion carries are a representation question,
  not an engineering one.
- A monitor that stopped halfway leaves the rest of the journey unknown. An
  unmonitored stretch is not a compliant stretch, and the coverage fraction is
  reported so the gap can be sized rather than assumed away.
- The certificate of conformity identifies an item, not a shipment in general.
  Part number, serial and quantity have to be the same on the certificate as on
  the consignment, or the certificate covers something that was not sent.
- Authority to sign sits with the quality function. A delivery the review board
  held cannot acquire a certificate downstream, and a delivery carrying
  reservations needs them written on the certificate, not left in the minutes.

## Workflow

1. Validate the consignment: part number, serial and a positive whole quantity,
   with each transport-relevant state stated rather than assumed.
2. Derive the mandatory shipping documents from those states and name each one
   the consignment is not carrying, matching names without regard to case or
   separator.
3. Validate the declared transport limits, allowing a one-sided bound, and
   refuse a reading for a parameter that has no declared limit instead of
   silently dropping it.
4. Count the excursions per parameter and keep the worst reading and the side
   it left the band on.
5. Compute the monitoring coverage over the transit duration and raise a
   shortfall as an unknown stretch, refusing a record that claims to cover more
   hours than the journey took.
6. Reconcile the certificate identification against the consignment.
7. Check the signing authority and the reservation listing against the delivery
   review outcome, then report every finding; the certificate is issuable only
   when none stands.

## Pitfalls

- Shipping the same document pack every time. The pack that is right for a
  domestic benign move is short by two papers the moment the consignment
  crosses a border.
- Reporting one excursion because the recorder alarmed once. The count and the
  worst value are different facts, and receiving inspection needs both.
- Reading a flat trace from a stopped recorder as a quiet journey. A recorder
  that covered a third of the transit says nothing about the other two thirds,
  and that is a finding, not a pass.
- Issuing the certificate against the shipment rather than the item. A serial
  or a quantity that does not match means the certificate covers hardware that
  did not travel.
- Letting the shipping function sign the conformity. The signature is the
  quality function's, and a delivery the board held has no certificate to sign.
- Leaving reservations in the board minutes. What the customer receives is the
  certificate, so a delivery carried on a waiver has to say so on its face.

## Behavior contract (gate 3)

The consignment validation, derived shipping document set, limit validation,
per-parameter excursion counting, monitoring coverage, certificate
identification reconciliation, signing authority and the combined issuance
decision are exercised by the gate 3 contract test:
scripts/test_q20_delivery.py against scripts/q20_delivery_logic.py (stdlib
unittest, offline). Run:
python3 scripts/test_q20_delivery.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
