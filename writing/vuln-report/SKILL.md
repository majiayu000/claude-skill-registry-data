---
name: vuln-report
description: Write bug bounty vulnerability reports in the strict 5-section template — Title, Summary, Full PoC, Impact, Remediation. Use whenever the user asks to "write a report", "report this bug", "draft a submission", mentions a finding that needs writing up, or wants bugs documented — every bug written must follow this exact template, no exceptions.
---

# Vulnerability Report Writer — Strict 5-Section Template

Every bug is written in exactly this structure, in this order:

```
## Title
## Summary
## Full PoC
## Impact
## Remediation
```

No section may be skipped, renamed, or reordered. If information does not fit one of the five sections, it goes in the per-report extras described below — never a new top-level section inside a bug.

## Section rules

**Title** — one line: vulnerability type + exact location (endpoint/parameter) + the attacker outcome. Bad: "XSS bug in search". Good: "Reflected XSS via backslash-escape breakout in `GET /catalog?searchTerm=` executes arbitrary JavaScript". Never clickbait, never severity claims in the title.

**Summary** — 2–4 sentences: what the bug is, where it lives, what an attacker can do, and the one mechanism detail that makes it work. A triader who reads only this section must understand the bug.

**Full PoC** — the complete reproduction, copy-pasteable. Numbered steps with exact `curl` commands (or precise click-paths when browser-only), real request/response excerpts, and expected output at each step. The rule: a stranger reproduces the bug from this section alone, twice, deterministically. If the finding was only demonstrated interactively, re-verify it before writing — never report from memory.

**Impact** — concrete attacker outcomes, not vulnerability theory. "Anyone holding the link can download the customer's VAT receipt" beats "sensitive information may be disclosed". Chain where possible (what the primitive unlocks), but mark chains as chains — never present theoretical escalation as achieved impact.

**Remediation** — specific engineering fixes for THIS bug, not generic advice. Name the exact mechanism ("disable DTD processing via `setFeature(...disallow-doctype-decl...)`", "JSON-encode values when interpolating into JS context"), ordered by what stops the bug first.

## Mandatory per-report extras (outside the 5 sections)

- **CVSS 3.1 vector + score on every finding** — put it directly under the Title. Pair it with an honest calibration line: if realistic triage will land lower than the vector (link-possession required, blind primitive, bounded window), say so and name the realistic band. One calibrated sentence beats an inflated vector the triager knocks down.
- **Evidence appendix when the finding spans multiple artifacts** — a table of every verified URL/object with its verified state (e.g. receipt-downloaded vs state-classified). State exactly what was executed vs classified; never let scale claims rest on more than was done.
- **Tested-negative registry** — for engagement-level reports: every rejected lead with the server's own response as proof. Demonstrates diligence and prevents re-testing.
- **Testing-hygiene note** — one line: request count, data retained/discarded, identifiers redacted. Triagers trust reports that show restraint.

## Hard rules

- Third-party credentials and live victim/customer data NEVER appear in PoCs. Redact partial (`84***13`), discard downloaded bodies, say so in the hygiene note.
- No filler: no "upon further investigation", no "I noticed that", no restating the request in prose.
- One file per engagement consolidates all bugs (`BUGS.md` or `REPORT-<finding>.md` for singles); each bug still gets the full 5-section treatment inside it.
- Low/informational findings get grouped together in one section but STILL follow the 5-section template individually.
- Never invent a finding to fill the template. If nothing is confirmed, write exactly that plus top residual risks — a clean report is a credible report.

## Report skeleton (copy this)

```markdown
# <Target> — Bug Bounty Report (date)

## F-1 · <Title>
- **Severity:** CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N — X.X <class>
- **Endpoint:** `<method> <path>`
- **Class:** CWE-xxx

### Summary
<2-4 sentences>

### Full PoC
1. `curl ...`
→ <response excerpt>
2. ...

### Impact
<concrete outcomes>

### Remediation
1. <specific fix>

## Summary table
| # | Finding | Sev | CVSS | One-line fix |

## Tested-negative registry
| Hypothesis | Test | Result |

## Appendix — evidence index
<verified artifact table + hygiene note>
```
