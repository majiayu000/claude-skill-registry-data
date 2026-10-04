---
id: threat-modeling
version: "2.0.0"
title: "Threat Modeling"
description: "Decide what a design must be true before code exists: naming assets and actors, locating trust boundaries, producing a written (asset, boundary, threat, control, owner) list, recording the assumptions the design rests on, and knowing when a change invalidates the model. Use when scaffolding a new feature, service, or endpoint, writing or reviewing a design doc, RFC, or ADR, or introducing a new trust boundary, integration, or data flow."
category: prevention
severity: high
applies_to:
  - "when scaffolding a new feature, service, or endpoint"
  - "when writing or reviewing a design doc / RFC / ADR"
  - "when introducing a new trust boundary, integration, or data flow"
  - "when a design adds a component that acts on someone else's behalf"
languages: ["*"]
token_budget:
  minimal: 1500
  compact: 1900
  full: 2300
related_skills: ["api-security", "auth-security", "database-security", "iam-best-practices", "llm-app-security", "secure-code-review"]
last_updated: "2026-08-14"
sources:
  - "OWASP Threat Modeling Cheat Sheet"
  - "Microsoft STRIDE"
---

# Threat Modeling

## Rules (for AI agents)

### ALWAYS
- Produce a **written list**, not an impression. One row per finding, in the design
  doc, the RFC, or the PR description: `(asset, boundary, threat, control, owner)` —
  what is worth taking, where it crosses, what could go wrong there, what stops it,
  and which component enforces it. A model that exists only in the reasoning that
  produced the code cannot be reviewed, disagreed with, or checked later.
- Name the **assets** and the **actors** first: data, funds, credentials, keys and
  compute on one side; users, tenants, services, admins and the attacker on the other.
  Every later row references one of each, which is what makes the list finite.
- Locate the **trust boundaries** — internet to application, tenant to shared store,
  service to service, user input to an interpreter, model output to anything that acts
  on it. A boundary is where data arrives from a party you do not control, and it is
  the unit the rest of the model is organised around.
- At each boundary, ask the six **STRIDE** questions and write down only the answers
  that matter: can the caller be **spoofed** (is there authentication), can the data be
  **tampered** with in flight, will there be a record if someone **repudiates** the
  action, what is **disclosed** if this crossing leaks, what happens under **denial of
  service**, and does anything here allow **elevation of privilege**. A category with
  no answer is not a gap; a category nobody asked about is.
- Write down the **assumptions the design depends on**: this gateway is the only
  ingress, this queue's producers are authenticated, this field is already validated
  upstream, this CDN strips that header. Assumptions are the part of a threat model
  that later becomes false without anyone noticing, and an unwritten one cannot be
  rechecked.
- Rank the rows and say which ones **block the design**. A model that treats every
  threat as equally urgent gets implemented in whatever order the work happens to
  arrive, which means the ranking gets made anyway, by accident.
- Design controls to **fail closed**: on error, missing configuration, a timeout, or
  an unhandled case, the secure outcome is denial. This is a design property because
  the alternative is usually invisible in the code — an exception that skips a check
  reads exactly like an exception that skips a log line.
- Put each control **at the component that owns the asset**, behind any gateway rather
  than instead of it. The owning service authenticates and authorizes even when a
  perimeter also does, because perimeters get bypassed, reconfigured, and eventually
  routed around by the next service that needs direct access.
- **Re-run the model when its inputs change** — a new actor, a new boundary, a new
  data flow for an existing asset, a component moving between trust zones, or an
  assumption you wrote down turning out to be false. A model is a statement about a
  design, so it expires when the design moves.
- Route each control to the skill that owns it, and record that in the row's `owner`.
  `auth-security` owns who the caller is and what they may touch, `api-security` the
  endpoint's own controls, `database-security` how tenant isolation is actually
  enforced, `iam-best-practices` the privileges a workload runs with, and
  `llm-app-security` what a model's output is allowed to reach. This skill decides
  which controls the design requires; those skills say what the control is.

### NEVER
- Treat anything the **client** controls as a control — hidden fields, disabled
  buttons, client-side role checks, an unverified token, a price in the request body.
  All of it is advisory. This is the design-level statement of a rule several code
  skills enforce, and it belongs here because it is usually decided before any code
  is written.
- Design a component that is **trusted because of where it sits**. "Internal service",
  private subnet, VPN, IP allowlist: those describe reachability, and reachability is
  not authentication. `api-security` owns the endpoint-level rule; the design-level
  version is that a trust boundary drawn around a network segment has no enforcement
  behind it.
- Invent a bespoke authentication, session, or access-control primitive when a vetted
  one exists. Design in the standard building block — OIDC for identity, mTLS or
  SPIFFE for workload identity, a policy engine for authorization decisions.
  `crypto-misuse` owns the equivalent rule for cryptographic primitives.
- Add an external **integration, dependency, or webhook** without deciding three
  things in writing: who may call it, what it is trusted to assert, and what happens
  when the counterparty is compromised or impersonated. The third is the one that gets
  skipped, and it is the one that determines blast radius.
- Leave a sensitive datum with **no sanctioned home**. For each one, name where it
  lives and, by implication, where it must not appear — logs, error payloads, client
  bundles, URL parameters, analytics. An undecided lifecycle is how a credential ends
  up in four places, none of them chosen.
- Ship a design whose security analysis is "we will add auth later". Retrofitting a
  trust boundary onto a built feature means changing the data model, and that is the
  point at which it does not happen.

### KNOWN FALSE POSITIVES
- A genuinely public, read-only surface — marketing site, public docs, a public
  catalog — legitimately has no authentication. The model's job is to confirm it holds
  nothing sensitive and grants nothing, not to add auth to it.
- Network controls layered **on top of** service-level authentication are good design.
  The finding is network position as the *sole* control, never its presence.
- mTLS or SPIFFE workload identity **is** authentication — a cryptographic caller
  identity, not a network location — so a service-to-service call over it is not
  relying on network position.
- A design that reuses an existing, documented boundary without changing it inherits
  that boundary's model. The trigger is a *new* or *moved* boundary; a fifth endpoint
  behind the same authenticated, tenant-scoped surface as the other four is not a new
  model.

## Context (for humans)

The output is the point. Threat modeling done as a discussion produces agreement that
evaporates; done as a written list it produces something an implementer can work
against and a reviewer can disagree with. That is why the first rule is about the
artifact rather than about the analysis — the analysis is worthless if it does not
land anywhere.

For AI-assisted development the failure mode is specific and worth naming: models
produce clean, working, well-tested code that implements an **insecure design**. Tenant
data commingled in one table behind an application-enforced filter. Authorization
checked at a gateway that the service also exposes directly. A credential whose
lifecycle nobody decided. None of these is a bad line of code, so nothing that reads
lines will find them — they are only visible at the altitude where someone asks what
the system is supposed to guarantee.

The assumptions register is the part most often skipped and the part that ages worst.
Designs are usually secure *given* something: that a gateway is the only way in, that
a producer is authenticated, that a field was validated upstream. Those statements are
true when written and silently become false — a second ingress is added, a queue gets
a new producer — and nobody rechecks a claim that was never written down.

## References

- `references/design-level-failures.md` — worked examples of designs that scanners
  cannot flag, a filled-in `(asset, boundary, threat, control, owner)` list for one
  realistic feature, and the division of labour with the code-level skills
- [OWASP Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html).
- [Microsoft STRIDE threat model](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats).
