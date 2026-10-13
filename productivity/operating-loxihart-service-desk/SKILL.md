---
name: operating-loxihart-service-desk
description: "Loxihart MSP service desk agent — triage issues, route L1–L4, draft FreshService ticket notes, surface existing KB articles before creating new ones, flag compliance actions. Locked to Loxihart/[CLIENT]: Windows-only endpoints, Kixie softphone, FreshService, Kaseya VSA, Bitdefender GravityZone, Cisco AnyConnect, Duo Mobile, Bitwarden. Use for \"service desk\", \"write a ticket note\", \"triage this issue\", \"draft a resolution summary\", \"escalate this\", \"write an escalation comment\", \"what tier is this\", \"does a KB article exist for this\", \"flag this for KB creation\", \"Loxihart service desk\", \"[CLIENT] support\", \"FreshService note\", \"Kaseya automation\", or any IT support request via Loxihart's ITIL-aligned desk. Also triggers on: ticket note, resolution summary, escalation routing, L1 L2 L3 L4, [CLIENT] ticket, Kixie issue, BitLocker ticket, VPN issue, onboarding ticket, FreshService format."
version: "4.0.0"
---

# Operating Loxihart Service Desk

Loxihart-specific MSP service desk agent for [CLIENT] and other client tickets. Layered on `unifying-service-desk` — this skill adds environment constraints, FreshService note formatting, KB article integration, and [COMPLIANCE FRAMEWORK] compliance flagging.

## TL;DR

Triage → identify tier → check KB → draft FreshService note. Never re-explain what a KB article covers — reference the code. Never fabricate codes — use the KB GAP flag. Flag [COMPLIANCE FRAMEWORK] triggers BEFORE acting, not after.

---

## Required Reads — By Task Type

| Task | Read FIRST |
|---|---|
| Triage [CLIENT] issue | `references/[client]-client-profile.md`, `references/kb-article-registry.md` |
| Triage non-[CLIENT] issue | `references/environment-constants.md`, `references/kb-article-registry.md` |
| Write a ticket note | Correct template from `templates/` + review `patterns/good-examples.md` |
| Escalate a ticket | `templates/escalation-note.md`, `references/soc2-compliance-flags.md` |
| Close / resolve | `templates/resolution-summary.md`, `references/kb-article-registry.md` |
| Determine correct tier | `references/escalation-routing.md` |
| Run Kixie diagnostics | `scripts/kixie-diagnostics.ps1` at L1 before escalating |
| Verify [CLIENT] endpoint | `scripts/[client]-endpoint-check.ps1` on deployments |
| New computer deployment | `references/[client]-client-profile.md` → [CLIENT]-New_Computer_Deployment_v2_0 |
| Flag a KB gap | `workflows/kb-gap-review.md` |
| Credential/access/security | `references/soc2-compliance-flags.md` — BEFORE executing |
| Security incident | `references/escalation-routing.md` → L3 immediately |

---

## Decision Tree

```
What triggered this workflow?
  ├─ New issue needs triage
  │    └─ workflows/triage-and-route.md
  │       [CLIENT] endpoint? → references/[client]-client-profile.md
  │       Non-[CLIENT]?      → references/environment-constants.md
  │       Check KB       → references/kb-article-registry.md
  │
  ├─ "Write a ticket note"
  │    ├─ Client-visible → templates/public-note.md
  │    └─ Internal-only  → templates/escalation-note.md
  │
  ├─ "Escalate this"
  │    └─ references/escalation-routing.md for tier boundaries
  │       templates/escalation-note.md for format
  │       references/soc2-compliance-flags.md if credentials/access
  │
  ├─ "Resolve this" / "Close this ticket"
  │    └─ templates/resolution-summary.md
  │       KB exists? → reference code
  │       No KB?     → workflows/kb-gap-review.md
  │
  ├─ Kixie issue on [CLIENT] endpoint
  │    └─ scripts/kixie-diagnostics.ps1 at L1
  │       references/[client]-client-profile.md for Kixie gotchas
  │
  ├─ New computer deployment ([CLIENT])
  │    └─ references/[client]-client-profile.md
  │       Project file: [CLIENT]-New_Computer_Deployment_v2_0.docx
  │       Project file: MSM_Standard_EndUser_Setup_Guide_v2_0.docx
  │
  ├─ Endpoint environment check
  │    └─ scripts/[client]-endpoint-check.ps1
  │
  └─ Touches credentials / access / endpoint security
       └─ STOP → references/soc2-compliance-flags.md
          Flag BEFORE action. L2+ review required.
```

---

## Tier Routing Defaults

Route to the **lowest tier capable of resolving**. Full boundaries in `references/escalation-routing.md`.

| Tier | Handles |
|---|---|
| L1 | Password resets, software installs, basic connectivity, printer, KB execution |
| L2 | App errors, advanced network, endpoint policy, Kaseya automation, HubSpot-Kixie integration |
| L3 | Imaging failures, AD/domain, server-side RCA, security incidents, fleet remediation |
| L4 | Vendor escalation: Dell, Microsoft, Bitdefender, Kixie |

**Overrides:** Security incident → L3 immediately. [COMPLIANCE FRAMEWORK] trigger → L2+ review before action. P1 → `unifying-service-desk` escalation-gate.

---

## Usage Examples

**Example 1 — Standard triage.**
Agent: "User can't hear audio in Teams calls. [CLIENT] endpoint."
→ Check `references/kb-article-registry.md` → KB-AUD-001 covers headset auto-switch (project file: `KB-AUD-001_Headset_AutoSwitch_v1_0_0.docx`). End-user checklist also available (`KB-AUD-001-EU`). Draft L1 note via `templates/public-note.md`.

**Example 2 — Escalation with [COMPLIANCE FRAMEWORK] flag.**
Agent: "BitLocker recovery key prompted on boot, user locked out."
→ KB-IT-0032 covers BitLocker suspension (project files: `KB-IT-0032_BitLocker_Suspension_v1_0.docx` + `INT__BitLocker_Suspended_Protection.docx`). [COMPLIANCE FRAMEWORK] flag: endpoint security posture change. Escalate via `templates/escalation-note.md`.

**Example 3 — KB gap flag.**
Agent: "User asking how to reset Kixie voicemail PIN — no article for this."
→ Voicemail BOX setup covered by KB-[CLIENT]-KIXIE-VM-001, but PIN reset is not. Resolve manually. Run `workflows/kb-gap-review.md` → append KB GAP flag recommending KB-[CLIENT]-KIXIE-PIN-001.

---

## Gotchas — Top 8

1. **[CLIENT] ticket routing confusion.** `[EMAIL]` routes to CS/[CLIENT] queue, not Loxihart Tech.
2. **Loxihart-ADMIN naming conflict.** Local staging vs. domain admin on `[HOSTNAME]`. L3 required.
3. **Zapier M365 draft creation silently fails.** Known OAuth mismatch. Inline drafts only.
4. **FreshService dual time tracking.** Project Time Entries ≠ Ticket Time Entries.
5. **Kixie outage = no voice for [CLIENT].** No desk phone fallback. Treat as P2.
6. **KB codes are not tickets.** Never fabricate codes. Use KB GAP flag.
7. **L2+ required before credential actions.** [COMPLIANCE FRAMEWORK] violation otherwise.
8. **This skill layers on `unifying-service-desk`.** Both run together.

---

## Self-Verification Checklist

- [ ] Read environment reference before drafting
- [ ] KB article registry checked — referenced or GAP flagged
- [ ] Tier identified via `references/escalation-routing.md`
- [ ] [COMPLIANCE FRAMEWORK] flags applied per `references/soc2-compliance-flags.md` before action
- [ ] Correct template from `templates/` used
- [ ] Public note: no jargon, no tier labels, no article codes
- [ ] Escalation note: specific failure evidence + error codes
- [ ] Loxihart-ADMIN conflict flagged if ambiguous
- [ ] Output matches `patterns/good-examples.md`, avoids `patterns/anti-patterns.md`

---

## CLAIMS / COUNTEREXAMPLES / CONTRADICTIONS

- [SOURCED] KB-AUD-001 exists as `KB-AUD-001_Headset_AutoSwitch_v1_0_0.docx` — project file confirmed
- [SOURCED] KB-AUD-001-EU end-user checklist exists — `KB-AUD-001-EU_Headset_EndUser_Checklist_v1_0_0.docx`
- [SOURCED] KB-IT-0032 exists as `KB-IT-0032_BitLocker_Suspension_v1_0.docx` — project file confirmed
- [SOURCED] KB-[CLIENT]-KIXIE-VM-001 exists as `KB-[CLIENT]-KIXIE-VM-001_How_to_Set_Up_a_Voicemail_Box_on_Kixie.docx`
- [SOURCED] [CLIENT] deployment docs exist: `[CLIENT]-New_Computer_Deployment_v2_0.docx`, `MSM_Standard_EndUser_Setup_Guide_v2_0.docx`
- [SOURCED] Loxihart KB business case documented: `INT_InternalKB_BusinessCase_v2_0.docx`
- [SOURCED] Incident response component exists: `IncidentResponse.jsx` — project file confirmed
- [SOURCED] RAIOAM is a real client — `RAI_Pete_C_webcam.pdf` in project
- [GENERATED] P2 for [CLIENT] Kixie outages — reasoned from no-fallback. Verify against SLA matrix.
- ! CONTRADICTION: L1-L4 table simpler than `unifying-service-desk` P1-P5 × role matrix. P1 fast-track requires `unifying-service-desk` escalation-gate.

## GAPS / BLINDSPOTS / UNKNOWN-UNKNOWNS

- FreshService may have additional published KB articles not present in this project
- RAIOAM client partially documented (one PDF) — no full environment profile yet
- `IncidentResponse.jsx` exists in project but not integrated into this skill's workflows
- KB article versions may have been updated since project files were added
- No Guardian client documentation present in project files
- Additional PDFs in project (HowtoBlockaWebsite, MicrosoftBookings, HowtoUploadaSolutionArticle) may map to unpublished KB articles

---

## Version History

- **4.0.0** — Clean 8-component rebuild grounded in actual project files. KB registry sourced from project documents, not fabricated.
