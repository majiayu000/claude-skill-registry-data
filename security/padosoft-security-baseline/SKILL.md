---
name: padosoft-security-baseline
description: >-
  Use this skill when deciding what security an application must have — starting a new project, taking one
  to production, preparing for an audit, a penetration test or a customer questionnaire, planning a
  hardening backlog, or answering "are we secure enough?". Also when the user asks which controls are
  missing, what to do first, how to prove a control exists, or wants a new service to start at the same
  level as an existing one. It walks the control domains, separates what the framework gives you from what
  you must build, and turns a finding into a control that holds for future code. Do not use it to review a
  specific diff — the per-stack review skills do that — nor to run a scanner or write a threat model for
  one feature.
license: MIT
compatibility: >-
  Stack-agnostic. Mapped onto the current OWASP Top 10, ASVS, the API and mobile equivalents, NIST SSDF and
  SLSA, so an assessment can be handed to an auditor in their vocabulary.
metadata:
  version: 0.1.0
  author: Padosoft
  summary: A control you cannot prove is a control you do not have.
  profiles: core
  scope: global
  repository: https://github.com/padosoft/skills
  keywords: security, owasp, asvs, hardening, posture, audit, baseline, threat model, compliance
---

# Security baseline

Most applications are not insecure because somebody wrote a bad line. They are insecure because a whole
**domain** was never considered, and nothing about the code says so. This is the list of domains, what makes
each one real rather than declared, and the order to take them in.

**The rule: a control you cannot prove is a control you do not have — and a control that only new code
respects is half a control.**

---

## 1. Three things that invalidate defences you already paid for

Before any list, check these. Each one silently cancels controls that appear to be in place.

1. **The origin must be reachable only through the edge.** If the application answers requests that did not
   come through the CDN, WAF or proxy, then every edge rule — bot management, rate limits, IP reputation,
   the trusted client-address header — is an opt-in the attacker declines. Every control that trusts a
   header set by the edge is only as true as this.
2. **After any credential or key exposure, rotate and then verify what the rotation broke.** The application
   signing key usually underwrites sessions, cookies, signed URLs and stored tokens at once; rotating it is
   correct and it invalidates all four. Rotating without checking them is how a fix becomes an outage;
   *not* rotating is how an incident stays open.
3. **A language with no static analysis in the pipeline has no automated floor.** If the main language of
   the codebase is not covered by a scanner, every finding in it depends on someone noticing. Know which
   languages your pipeline actually covers — the default configuration of most tools does not cover all of
   them.

## 2. The domains

Walk them in this order the first time. `references/controls.md` has the individual controls for each, with
what makes them real; read the section for the domain you are working on, not the whole file.

| # | Domain | The question it answers |
|---|---|---|
| 1 | Access control and authorisation | Can one identity reach another's data or actions? |
| 2 | Authentication and identity | Can somebody become a user they are not? See **`padosoft-auth-hardening`** |
| 3 | Injection | Can input become code, a query, a command or markup? |
| 4 | Cryptography and secrets | Where do the secrets live, who can read them, when do they change? |
| 5 | Configuration | Is a safe default actually the default, everywhere, in every environment? |
| 6 | Software supply chain | Do you know what you ship, and would you notice if it changed? |
| 7 | Build and delivery integrity | Can somebody put code into production without going through the gate? |
| 8 | Logging, detection and alerting | If it happens tonight, who finds out, and how? |
| 9 | Exceptional conditions | When something fails, does it fail closed? |
| 10 | Rate limiting and anti-automation | What stops a script doing this ten thousand times? |
| 11 | Business-logic abuse | What happens if somebody uses the feature exactly as designed, maliciously? |
| 12 | Data protection and privacy | What do you hold, for how long, and who else gets it? |
| 13 | Uploads and files | Can a file become an execution path? |
| 14 | API surface | Which endpoints exist, and does each one carry its own authorisation? |
| 15 | Browser surface | What runs on your origin, and who put it there? |
| 16 | Mobile surface | What did you ship inside a bundle that anybody can open? |
| 17 | Infrastructure and edge | What is reachable, with which privileges, and what happens when it is lost? |
| 18 | Process and governance | What keeps all of the above true in six months? |
| 19 | AI and model surface | The model is a caller with unusual reach — see **`padosoft-agent-host-boundaries`** |

Domains 1, 3, 9, 13 and 14 are where a review of the code finds things. Domains 5, 6, 7, 17 and 18 are where
an assessment of the *system* finds things, and they are the ones that get skipped because no diff contains
them.

## 3. Reading a status honestly

The whole value of an assessment is in refusing to overstate it. Four statuses, and the discipline is in the
last two:

| | Means |
|---|---|
| **Covered** | there is a control, and a **gate or a rule applies it to new code** |
| **Native** | the framework provides it unless somebody disables it — the risk is deactivation, not absence |
| **Partial** | it exists and does not cover the whole surface. Write **what is missing**, not just "partial" |
| **Not inspected** | nobody looked. Write **how** to look, so the next person can. This is an honest state |

Two traps that turn an assessment into fiction:

- **"Covered by a rule" does not mean the existing codebase complies.** A rule is applied in review on new
  code. Code written before the rule existed has never been checked against it. Both facts are fine;
  conflating them is not.
- **An identifier quoted in a comment is not a control.** Code that says it implements a security rule, with
  no rule behind it, means the control exists *today* and nothing prevents the next change from removing it.
  The inverse of the previous trap: there, old code is unverified; here, **future** code is unguarded.

## 4. The rules that recur in every domain

These are not domain-specific. They decide whether a control is real.

- **A setting is not a boundary.** An authorisation or security boundary must not be switchable at runtime
  by anybody who can reach a settings screen. If it must be configurable, the configuration cannot reach
  *off*, and the floor is in code.
- **An empty configuration value must not mean "disabled".** The absent case is the common case: a fresh
  environment, a tenant nobody configured, a variable with a typo. Absent means the **secure default**, and
  disabling takes an explicit, visible value.
- **A control that fails open needs a written reason and a second control behind it.** Failing open is
  sometimes right — refusing every login because a third-party verifier is unreachable is worse than the
  friction it was buying. It is only acceptable while something else carries the weight, and that
  dependency is written down so that removing the other control re-opens the question.
- **A control that fails closed needs an escape.** A guard that denies on its own internal error is correct
  and will one day deny everybody; know which of the two you chose, and why.
- **Half a switch is worse than none.** A toggle that disables the server-side check while the client keeps
  behaving as if the control were on gives the impression of a decision nobody actually made.
- **Twin endpoints must be protected identically.** Where two routes reach the same resource — an older and
  a newer one, a page and its asynchronous counterpart, a web form and an API — the one built last usually
  has the controls, and the one built first is still wired.
- **A gate that is born red and left red gets switched off within a week**, and then it protects nothing at
  all. Introduce a strict check on new work first, and bring the backlog in behind it.
- **Remove an endpoint rather than gating it.** A route that exists in order to be refused is a route that
  one configuration change makes reachable.

## 5. Turning a finding into a control

A closed finding is worth very little; the class it belongs to is worth a lot.

1. **Fix it** in a small change, with a test that fails without the fix.
2. **Name the class.** Not "this endpoint leaked the model name" but "error messages must not carry internal
   identifiers".
3. **Write the rule**, and put the check where it will run without anyone remembering — a validator, a
   grep in review, a test, a gate.
4. **Label the change**, so the set of security work is answerable in one query when an auditor, a customer
   or your own team asks what was done and what is still open. A security fix that stays open is an exposure
   window, not a backlog item.
5. **Find the twins.** The same class almost always exists somewhere else in the codebase.

## 6. Where to start, on a new application

In order, because each one makes the next cheaper:

1. Authorisation derived from the authenticated identity, never from a parameter — **`padosoft-tenant-isolation`**.
2. Errors that carry nothing internal, and logs that carry nothing personal — **`padosoft-logging-discipline`**.
3. Rate limiting on everything that can be attempted repeatedly — **`padosoft-auth-hardening`**.
4. Secure defaults for headers, cookies and the environment gate — **`padosoft-environment-gating`**.
5. Dependency and secret scanning in the pipeline, blocking on the diff — **`padosoft-ci-workflow-gates`**.
6. One audit trail whose integrity can be shown — **`padosoft-evidence-boundaries`**.
7. Only then the long tail in `references/controls.md`.

---

## Gotchas

- **A penetration test is a sample, not a coverage measure.** Closing its findings raises the floor by
  exactly the height of that sample.
- **The report that arrives too often is not read.** A monthly access review gets attention; a weekly one
  becomes a filter rule — see **`padosoft-failure-visibility`**.
- **The control everybody forgets is the one for privileges granted outside the role system.** Reviewing
  roles does not show them, and they are the channel through which access grows silently.
- **A configuration flag and an environment name are two gates**, and the dangerous arrangement is the one
  where either alone turns a convenience on.
- **Owning a scanner is not running it, and running it is not reading it.** The finding with no owner and no
  date is the same as no finding.
- **An exception in an allow-list outlives the thing that justified it.** When that name comes back, the
  exception authorises it silently. Expire them, or report the orphans.

## Checklist

- [ ] Origin reachable only through the edge; every header-trusting control depends on it
- [ ] Keys rotated after any exposure, and what the rotation invalidated has been verified
- [ ] Static analysis covers the main language of the codebase
- [ ] All 19 domains have a status, and *not inspected* says how to inspect
- [ ] No status claims coverage of the existing codebase when the rule only applies to new code
- [ ] No security boundary governed by a runtime setting; no empty value meaning "off"
- [ ] Every fail-open documented with the control that carries the weight
- [ ] Twin endpoints compared side by side
- [ ] Each closed finding has a named class, a rule and a check that runs by itself
- [ ] Security changes labelled so the whole set is answerable in one query

## Final report

```
Scope: <application / service>   ·   assessed against: <standards>
Domains: covered <n> · native <n> · partial <n> · not inspected <n>
Invalidators: edge-only origin <…> · key rotation <…> · static analysis <…>
Top gaps, in the order to take them: 1. <…>  2. <…>  3. <…>
Rules added from findings: <which, and where the check runs>
Stated honestly: <what is "partial" and why> · <what nobody looked at>
```
