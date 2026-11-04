---
description: Build the authentication and authorization stack for a repository already set up to STACKSPEC — packages/auth, the auth endpoints in apps/api, sessions, MFA, consent, erasure, audit and their required test suites — per the binding AUTHSPEC, or audit an existing implementation against it. Use when the user asks to add authentication, login, signup, sessions, passkeys, MFA, admin access, or an auth audit, or invokes /luismc-project-setup:auth-setup. Requires tech-stack-setup to have run first; it refuses on a repository that is not set up.
model: opus
effort: medium
---

# Auth setup — build and check

Builds authentication and authorization to **`AUTHSPEC`**, the binding
specification at `references/authentication.md` alongside this file. Version
3.1.0. It governs authentication flows, authorization, sessions, MFA and
step-up, account recovery, consent, data-subject rights, abuse prevention,
notifications, audit, and retention.

**Read the spec before acting on it.** It has about 3,800 lines. This file does
not summarize it. Read the sections a step needs. Never generate against a
clause you have not read. Some `AUTHSPEC` requirements depend on their
rationale. `R15.12` forbids soft-delete as an erasure mechanism. `R16.4` forbids
personal data in audit metadata *because* audit records must survive erasure.
Code written from a paraphrase gets these wrong.

## Step 0 — Preflight. Do this before anything else

```bash
python3 ../tech-stack-setup/assets/preflight.py --require stack --for-skill auth-setup
```

**If it exits non-zero, stop and report its message verbatim. Write nothing.**

It checks for `docs/architecture/stack-profile.md` (or the old `docs/specs/stack-profile.md`), `pnpm-workspace.yaml`, and a
`packages/` or `apps/` directory. `tech-stack-setup` produces these. The Stack
Profile is required: `AUTHSPEC §2.1` resolves the technology stack by reading
it. Without it, this skill does not know the database, the runtime, the package
layout, or the language version.

This guard prevents a quiet, expensive failure. On an empty repository, an agent
invents a plausible structure, such as a `src/auth/` here and an Express app
there. The user accepts it because it looks reasonable. The repository then has
two competing layouts. Undoing that costs far more than running the skills in
order.

**Do not offer to set the stack up yourself.** Tell the user to run
`tech-stack-setup`, and stop. That skill interviews for a dozen decisions. This
skill must not default them.

## Mode 1 — Build the auth stack

`AUTHSPEC` has no generation order of its own, unlike `STACKSPEC §26`. Use this
one. Each step is a dependency of the next.

1. **Resolve the stack.** Read `docs/architecture/stack-profile.md` (else the old `docs/specs/stack-profile.md`) fully
   (`AUTHSPEC §2.1`). Note the database, runtime, package manager, and the
   `AUTHSPEC` version it claims. If it claims a version older than
   `references/`, say so before generating. The difference is a finding.
   Generating 3.1.0 code into a repo that declares 1.0.0 conformance makes the
   profile wrong without any warning.

2. **Interview for the decisions the spec does not default.** Do not guess any
   of these. `AUTHSPEC` states them as choices, not as defaults:
   - which authentication methods the user plane offers (`§7.2` — password,
     passkey, magic link / email OTP, social OIDC, enterprise SAML)
   - whether an admin plane exists at all. If it does, `§4.5` and `§9.4` are
     mandatory and non-negotiable: **passkey-only, no password attribute of any
     kind, ≥2 authenticators before enrollment completes**
   - the grace period for erasure (`§15.4`, default 30 days, configurable 0–30)
   - retention windows where `§23.2` allows a range
   - whether service accounts are needed now (`§13`)

3. **Build in this order.**

   | Step | What | Spec |
   |---|---|---|
   | 1 | The `§4` entity tables as migrations in `packages/db` — every entity, with the `[ENC]` / `[BIDX]` / `[HASH]` classifications | `§4`, `§5` |
   | 2 | `packages/auth`: crypto (`§5`), sessions (`§6`), flows (`§7`), MFA and step-up (`§8`), recovery (`§9`) | `§5`–`§9` |
   | 3 | Authorization: the permission catalog declared **in code** (`R4.13`), the ownership predicate (`R4.16`) | `§11` |
   | 4 | The auth endpoints in `apps/api` per `§19.4`, each with its rate-limit bucket (`§17.3`) and explicit authorization declaration | `§19`, `§17` |
   | 5 | Admin plane, if step 2 said yes | `§12` |
   | 6 | Consent and legal-document versioning | `§14` |
   | 7 | Data-subject rights: export, rectification, erasure — including `§15.4.1`'s per-entity disposition | `§15` |
   | 8 | Audit trail, hash-chained and append-only | `§16` |
   | 9 | Notifications, the `§18.2` `security_event.kind` table | `§18` |
   | 10 | Retention jobs into the existing `packages/jobs` (`§23.3`) | `§23` |
   | 11 | The `§27.2` test gate — every suite it names | `§27` |

4. **Do not weaken a `MUST` to make a step easier.** If a requirement cannot be
   met with the stack the profile declares, stop and say so. `§0.2` defines only
   `MUST` / `MUST NOT`, `SHOULD`, and `MAY`. A `MUST` you cannot satisfy is a
   matter to raise with the user, not a judgement call to make silently.

5. **Wire into what `tech-stack-setup` already built.** Do not create parallel
   structures:
   - notifications go through the existing `packages/mail` adapter
   - retention pruners join the existing `packages/jobs`
   - the route-authorization coverage test harness already exists in
     `apps/api`; your new routes must satisfy it, and it should fail as soon as
     a route ships without a declaration

6. **Update the Stack Profile.** Record the `AUTHSPEC` version now implemented,
   plus every `SHOULD` not followed and every `MUST` waived, each with a named
   approver (`§27` item 13). A profile that still claims no auth after this
   skill has run is out of date.

7. **Run Mode 2 against what you built** and report the result. Then say what
   remains: default UX pages for the user and admin apps are **not** part of
   this skill.

## Mode 2 — Check an existing implementation

1. **Preflight with `--require stack --require auth`.** If auth does not exist,
   there is nothing to audit. Say it is absent and stop.

2. **Work `§27.4`'s coverage map**, clause by clause. It is the spec's own
   index of what must be demonstrable. Mark each clause **conforms**,
   **violates**, **absent**, or **not applicable** with the reason. Cite file and
   line for every violation.

3. **Check the controls that fail silently when absent.** When these are
   missing, nothing visibly breaks. The gap shows up only in an incident:
   - every `§4` entity has a `§15.4.1` erasure disposition — an entity nobody
     answered for is personal data that survives an erasure request
   - `§23.2` retention windows have a `§23.3` job actually pruning them
   - every `§19.4` route maps to a `§17.3` rate-limit bucket
   - audit records carry no personal data (`R16.4`) — the reason erasure and the
     6-year retention obligation do not conflict
   - lockout invalidates live sessions, not just the login path (`R4.8`)
   - `pending_verification` and `locked` fail session validation at stage 7 of
     `§3.4` (`R4.8`, `R4.8a`)

4. **Report severity-ranked findings grouped by spec section, and do not edit
   while surveying.** A check that repairs as it goes cannot show you what the
   repo looked like.

5. **Then offer to fix, opt-in and never automatic.** Most auth findings are
   not mechanical. A missing erasure disposition is a compliance decision, not
   a template. Offer only what is mechanical, list it explicitly, and re-run the
   check afterwards. A repair that was not re-verified is a claim.

## What this skill does not do

- **The tech stack.** That is `tech-stack-setup`, and it runs first.
- **UX.** Login screens, account settings, admin consoles, and the flows that
  wire them to these endpoints are out of scope on purpose. A future
  `auth-ux-setup` skill covers them. It will preflight with
  `--require stack --require auth`, that is, on what this skill produces.
- **Editing `AUTHSPEC`.** The spec is maintained in the `dev-standards`
  repository, which gates every edit. A product never carries a copy of it
  (`STACKSPEC §23`). It carries a Stack Profile that names the version it
  conforms to.
