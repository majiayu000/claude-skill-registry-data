---
name: modeling-threats
description: >-
  Guides a short threat model for a design: naming the assets, trust boundaries, and entry points it creates or changes,
  and the threats each design choice opens or closes, recorded beside the decision.
when_to_use: >-
  Use while designing a change that adds an entry point, moves data across a trust boundary, or adds a dependency,
  before its decision record is written.
compatibility: Requires read access to the design under review, the code around it, and its recorded decisions.
---

# Modeling Threats

The standards own the rules. [Developing Applications](../developing-applications/SKILL.md) places validation where
trust ends, No Secrets in Tracked Files keeps credentials out of the repository, and Architecture Decision Records
records a decision and its consequences. This skill covers the judgement a design needs before those apply: what an
attacker could do with the shape being chosen.

## Name What Is Worth Protecting

List the assets the design touches: stored data, credentials and tokens, the ability to act as a user, money or quota,
and the availability of the service itself. An asset nobody named is one no later choice protects. Keep the list to what
this change adds or reaches; a model of the whole system is a different, larger piece of work.

## Draw the Trust Boundaries

A trust boundary is wherever data or control passes between parties that trust each other differently: a user and the
service, the service and a third party, one tenant and another, a process and the store it writes. Mark each boundary
the design crosses, and the direction data moves across it. A boundary drawn after the code exists is usually drawn
where the code happens to be, not where trust actually changes.

## Walk Each Entry Point

For every entry point the design adds or changes — a request handler, a message consumer, a file it reads, a command it
accepts — ask the six questions in turn:

| Question                                      | The threat it names    |
| --------------------------------------------- | ---------------------- |
| Can a caller claim to be someone else?        | spoofing               |
| Can input or stored data be altered en route? | tampering              |
| Can an action be denied after the fact?       | repudiation            |
| Can data reach someone it should not?         | information disclosure |
| Can a caller exhaust or stall the service?    | denial of service      |
| Can a caller gain rights it was not given?    | elevation of privilege |

A question that does not apply is answered "not applicable" with the reason, never skipped.

## Tie Each Threat to a Choice

For each threat that applies, name the design choice that opens or closes it, and the deterministic test that would fail
if the mitigation were removed: an authorization test per protected operation, a rejected malformed payload, a rate
limit exercised at its edge. A mitigation no test can show failing is a hope. A threat the design accepts is stated as
accepted, with who accepted it and why.

## Record It With the Decision

The threat notes travel with the decision record they inform, as a short section or a file beside it: assets,
boundaries, entry points, each threat with its choice and test, and each accepted risk. Written separately, they drift
from the design the first time either changes.

## Before Calling It Done

- every asset the change touches is named;
- every trust boundary it crosses is drawn, with the direction data moves;
- every new or changed entry point has all six questions answered;
- every applicable threat names its choice and a test that would fail without the mitigation; and
- every accepted risk names who accepted it and why.
