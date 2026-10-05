---
name: cx-accessibility-review
description: Use to audit whether customer support is reachable for people with access needs — channels, hours, authentication barriers, CAPTCHA, voice-only paths, and alternate formats. Trigger for "support accessibility audit", "can customers with disabilities reach us", CAPTCHA on contact form, voice-only support, alternate format requests, or accessibility checklist for CX.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Support accessibility review

Accessibility reviews often stop at the marketing site. **Support is where problems
become urgent** — and where teams hide behind "call us", CAPTCHA gates, and PDF-only
policy documents. This is a practical operations audit, **not legal advice**. It
answers: can someone with common access needs complete a support journey?

## Scope the journeys

Test **end-to-end paths**, not individual pages:

| Journey | Minimum path |
| --- | --- |
| Get help on billing error | Help centre → contact → resolution |
| Account locked out | Recovery → verify identity → support |
| Report accessibility barrier | Feedback channel that does not require the barrier |
| Escalate unresolved issue | Supervisor or complaint route |
| Receive critical reply | Email/SMS/portal notification readable with AT |

Assign **modality personas** — do not require one person to represent all needs:

- Screen reader + keyboard only.
- No hearing on phone path (relay if offered).
- No speech — text-only contact.
- Low vision — zoom, contrast, no colour-only status.
- Cognitive load — plain language, consistent steps.

## Channel checklist

| Channel | Pass criteria | Common failures |
| --- | --- | --- |
| **Help centre** | Headings, labels, focus order, alt text | Search autocomplete unreachable |
| **Web chat** | Keyboard open/close, readable transcript | Widget trap focus |
| **Email form** | Labels, error identification | CAPTCHA without audio alternative |
| **Phone** | Clear IVR, callback option, wait info | Voice-only identity steps |
| **Callback** | Request without holding live line | Callback only after long hold |
| **Social/DM** | Private handoff to accessible channel | Support only via public reply |
| **In-app** | Support entry same AT as app | Hidden behind gesture-only menu |

## Authentication and barriers

| Barrier | Who it blocks | Mitigation pattern |
| --- | --- | --- |
| CAPTCHA on contact form | Vision, cognitive | Accessible CAPTCHA, honeypot, rate limit |
| SMS-only 2FA for login | No mobile, hearing relay issues | Alternate verification with fraud review |
| Voice-only identity | Deaf, speech impaired | Secure async verification path |
| Photo ID upload only | Motor, vision | Alternate verification policy |
| Time-limited magic links | Cognitive, assistive tech delay | Regenerate without penalty |

**Document alternate paths** agents can invoke — not "we'll figure it out."

## Hours and staffing

- Is there **any human reachable path** within published hours for each tier?
- After hours: is bot/KB **equally accessible**, or a worse experience?
- **Relay / text relay** (where applicable): published number and agent training.

## Alternate formats

Customers may request:

- Large print, plain language summary.
- Structured email instead of PDF attachment.
- Transcript of phone call.

| Check | |
| --- | --- |
| Policy exists and is findable | |
| Agents trained; not "we don't do that" | |
| SLA for format provision | |
| No charge for reasonable format | |

## Agent tooling accessibility

Agents with disabilities also need accessible workspaces. **Inaccessible internal
tools produce inaccessible replies** — template pickers, knowledge search, after-call
work forms. Include internal UI in scope when agent population includes AT users.

## Scoring and severity

| Severity | Example |
| --- | --- |
| **Blocker** | Cannot submit contact without CAPTCHA alternative |
| **Major** | Phone-only path for security issue |
| **Minor** | Low contrast on non-critical help article |
| **Process** | No documented alternate verification |

Do not average severities into one score. **List blockers first** with journey and
 reproduction steps.

## Traps

**Overlay widgets.** Third-party "accessibility" buttons do not fix support forms.

**PDF-only legal or policy replies.** Inaccessible attachment on ticket close.

**Assuming chat is accessible.** Many widgets fail focus and announcements.

**Testing with automated scan only.** Support flows need manual AT passes.

**Conflating compliance badge with reachable support.**

## Present results to the user

1. **Journey results table** — persona × journey × pass/fail/blocker.
2. **Blocker list** — reproduction steps, affected channels, suggested fix type.
3. **Authentication alternatives** — gaps and proposed operational paths.
4. **Hours and channel gaps** — who is unreachable when.
5. **Agent-side findings** — if internal tools block accessible service delivery.
6. **Prioritised remediation** — blockers before polish; owner suggestions by team
   (product, web, support ops, telephony).
