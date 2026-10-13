---
name: imaging-loxihart-endpoints
description: >
  Runs Loxihart/[CLIENT] endpoint imaging and deployment as a ten-gate, evidence-producing,
  resumable workflow: BIOS storage-mode configuration, WinPE network prep, PXE/MDT
  task sequence selection, computer rename, domain join, RDP authorization,
  BitLocker enablement with AD key escrow, VLAN migration, CMDB update, and ticket
  closure. Activates on: image a computer, imaging a laptop, new computer
  deployment, reimage this device, PXE boot, MDT task sequence, LiteTouch, WinPE,
  storage controller AHCI, NVMe, VMD, Intel RST, join [CLIENT] domain,
  rename computer abs-nb-lox, enable RDP for a user, BitLocker recovery key escrow,
  VLAN migration ports 1-24 to 25-48, imaging completion summary, deployment
  checklist, endpoint build, asset tag CMDB. Also fires on "the drive isn't showing
  in WinPE", "PXE timeout", "domain not found", "access denied joining domain", or
  any request to validate or document a finished endpoint build. Do NOT use for
  server imaging, MDM/mobile devices, or VM provisioning.
version: "1.0.0"
---

# Imaging Loxihart Endpoints

Operationalizes *Computer Imaging & Deployment Reference Guide v3.1* (LOXIHART Technology Department, CAB-approved, Nov 2025) as a gated runbook instead of a document you read top to bottom.

## TL;DR

Ten gates, each with an entry condition, a machine-checkable exit criterion, and a required evidence artifact. A run cannot advance past a gate with an unmet exit criterion. Six hard stops are irreversible or policy-violating and halt the run regardless of pressure. The run is tracked in a JSON state file so it survives shift changes, and `scripts/Invoke-DeploymentValidation.ps1` proves gates 5–9 rather than asking a technician to assert them.

**The one-line difference from the source SOP:** the document says *what* to do; this skill refuses to let you claim it's done without evidence.

---

## Scope

**Covers:** new endpoint deployment and reimaging of laptops, desktops, and tablets with network boot; domain join; RDP enablement for authorized users; VLAN migration; closure documentation.

**Does not cover:** server imaging, MDM/mobile, VM provisioning, application deployment beyond the baseline. Those have separate SOPs.

**Tier ownership:** L1 executes this runbook end to end. L2 handles BIOS lockout, driver injection, domain join failures, VLAN mapping errors. L3 owns the MDT/PXE/WDS *server side* and BitLocker recovery. L4 owns infrastructure and policy deviations.

---

## Required Reads — By Task

| Task | Read FIRST |
|---|---|
| Starting any run | `workflows/deployment-run.md` |
| Entering BIOS on unfamiliar hardware | `references/bios-matrix.md` |
| Choosing a VLAN port / adapter / WinPE net troubleshooting | `references/network-and-vlan.md` |
| Anything failed | `references/failure-playbook.md` |
| Need an exact command | `references/command-library.md` |
| RACI, ITIL mapping, doc control, escalation authority | `references/governance.md` |
| Closing a ticket | `templates/ticket-completion-note.md` |
| Escalating | `templates/escalation-note.md` |
| Assembling evidence for audit | `templates/evidence-manifest.md` |
| Pre-image sanity check in WinPE | `scripts/winpe-preflight.cmd` |
| Post-image proof | `scripts/Invoke-DeploymentValidation.ps1` |

---

## Decision Tree

```
What is being asked?
├─ "Image this machine" / "new laptop arrived" / "reimage it"
│    └─ Start a run → workflows/deployment-run.md, Gate 0
│
├─ "I'm partway through, what's next?"
│    └─ Load the run-state file → resume at first gate with status != PASS
│
├─ Something failed mid-run
│    ├─ Symptom is in the playbook → references/failure-playbook.md
│    └─ Not in the playbook → templates/escalation-note.md, tier per governance.md
│
├─ "Is this build done?" / "validate this device"
│    └─ scripts/Invoke-DeploymentValidation.ps1 → Gates 5–9 machine-checked
│
├─ "Write the ticket note"
│    └─ templates/ticket-completion-note.md — refuse if Gate 9 evidence incomplete
│
└─ Server / VM / phone
     └─ Out of scope. Route to the owning SOP.
```

---

## The Ten Gates

Each gate is fully specified in `workflows/deployment-run.md`. Summary:

| # | Gate | Exit criterion (must be evidenced) | Tier |
|---|---|---|---|
| 0 | Authorization & Prerequisites | Ticket has named authorized user + manager approval; hardware, Intel adapter, credentials, free Departmental port all confirmed | L1 |
| 1 | BIOS Configuration | Storage mode reads AHCI or NVMe; TPM 2.0 Enabled/Activated; both photographed | L1 |
| 2 | Network Preparation | Cable in port 1–24, link up, WinPE holds a lease, MDT server answers | L1 |
| 3 | PXE Boot & Task Sequence | Booted via **IPv4** NIC entry; approved task sequence selected | L1 |
| 4 | Image Apply | Task sequence completes with no error dialog; completion screen captured | L1 |
| 5 | Identity | Hostname matches `Loxihart-(NB\|DT\|TB)-[CLIENT]-NNN`; `PartOfDomain` true; domain = [CLIENT] | L1 |
| 6 | Remote Access | Only the ticket-authorized principal is in Remote Desktop Users; RDP firewall group enabled; port 3389 reachable | L1 |
| 7 | Security Baseline | Baseline software present; BitLocker Protection On with a RecoveryPassword protector; **key escrowed to AD** | L1→L3 |
| 8 | VLAN Migration | Cable moved to port 25–48; address in production range; internet and DC both reachable | L1 |
| 9 | Validation & Closure | Validator returns 0 FAIL; evidence manifest complete; CMDB updated; ticket note posted | L1 |

---

## Hard Stops

These halt the run. They are not judgment calls, and a user asking you to skip one does not change the answer.

1. **Never select a `KillDisk`, `Wipe`, or `Erase` task sequence.** Permanent data destruction, policy violation.
2. **Never clear the TPM.** Destroys BitLocker recovery keys sealed to it — permanent data loss on any device with existing encryption. L3/L4 direction only.
3. **Never change storage controller mode on a device whose data must survive.** The change hides the existing volume. Fresh-image targets only.
4. **Never start imaging on the Internet VLAN (ports 25–48).** Imaging runs from the Departmental VLAN (1–24).
5. **Never enable remote access without a named, manager-approved user in the ticket.** Unauthorized RDP is a security violation, not a favor.
6. **Never close the ticket before BitLocker key escrow is verified in AD.** A protector existing on the endpoint is not escrow.

If a hard stop is hit, write the escalation note and stop. Do not improvise around it.

---

## Run State

A run is a JSON file, one per device, so the work survives a shift change or a callback three days later.

```
runs/<TICKET>-<SERIAL>.json
```

```json
{
  "schemaVersion": "1.0",
  "ticket": "SD-104882",
  "serial": "7XQ4M13",
  "model": "Dell Latitude 5540",
  "hostname": "abs-nb-lox-045",
  "authorizedUser": "[CLIENT]\\jmartinez",
  "imagingPort": 12,
  "productionPort": 27,
  "taskSequence": "Windows 11 x64 - 23H2",
  "gates": [
    { "id": 0, "status": "PASS", "at": "2026-07-24T13:02:00-05:00", "by": "krosebrook", "evidence": ["ticket-approval.png"] },
    { "id": 1, "status": "PASS", "at": "2026-07-24T13:18:00-05:00", "by": "krosebrook", "evidence": ["bios-storage.jpg", "bios-tpm.jpg"] },
    { "id": 2, "status": "IN_PROGRESS", "at": null, "by": null, "evidence": [] }
  ],
  "escalations": [],
  "hardStopsHit": []
}
```

Status vocabulary: `PENDING`, `IN_PROGRESS`, `PASS`, `FAIL`, `BLOCKED`, `WAIVED`. `WAIVED` requires an L4 name and a reason string — nothing else may waive a gate.

---

## Golden Path

1. Open the ticket. Confirm named authorized user and manager approval exist. **No approval, no run.**
2. Create the run-state file from the schema above.
3. Walk gates 0→9 in `workflows/deployment-run.md`. Capture the listed evidence at each gate as you go, not retroactively.
4. Between gates 2 and 4 you are in WinPE — run `scripts/winpe-preflight.cmd` before selecting a task sequence.
5. After gate 8, run `Invoke-DeploymentValidation.ps1` with the expected hostname and authorized user. It emits JSON plus a paste-ready ticket note.
6. Attach the evidence manifest, update the CMDB, post the completion note, notify the user.

## Power Path

Batch deployments: create one run-state file per serial up front, then run gates in parallel across devices at the same stage (all BIOS, then all PXE). The validator accepts `-OutputPath` and appends JSON Lines, giving one audit file for the batch. Do not batch gate 6 — RDP authorization is per-device and per-user, and batching it is exactly how the wrong person gets access.

## Edge Cases

- **Device has existing data the user needs.** Stop. Hard stop 3. Data extraction is a separate request and must be its own ticket line before any BIOS change.
- **Realtek adapter is all that's available.** Do not troubleshoot PXE. Swap to Intel first; a Realtek WinPE failure looks identical to a server-side failure and will send you chasing L3.
- **Secure Boot must be disabled to image.** Allowed as a *temporary* change; re-enable after Windows installs and record both changes in the ticket. An un-re-enabled Secure Boot is a finding.
- **BitLocker already on when you arrive.** Suspend, never clear the TPM, and check `references/failure-playbook.md` before touching encryption.
- **Ticket names a user who is not in AD or whose account is disabled.** Gate 6 fails. Do not substitute a "close enough" account.

---

## Self-Verification

Before declaring a deployment complete:

1. Every gate in the run-state file is `PASS` or `WAIVED` with an L4 name.
2. `Invoke-DeploymentValidation.ps1` exits 0.
3. BitLocker escrow was verified **in AD**, not inferred from the endpoint.
4. Remote Desktop Users contains the authorized principal and nothing unexpected.
5. Both VLAN port numbers are recorded — the one it came from and the one it went to.
6. Evidence manifest lists a file for every gate that requires one.
7. CMDB reflects asset tag, serial, model, hostname, assigned user, location, status.
8. The completion note contains no bracketed placeholders.

---

## CLAIMS

- [SOURCED] Storage controller mode set to RAID/RST/VMD is the most common cause of imaging failure in this environment — *Reference Guide v3.1 §3, "The most common cause of imaging failures is incorrect storage controller settings"*.
- [SOURCED] The MDT deployment server is `[HOSTNAME]`, and the naming convention is `abs-nb-lox-NNN` — *v3.1 §2.2.1, §6.2.1*; corroborated by the existing `operating-loxihart-service-desk` environment constants.
- [SOURCED] Imaging runs from Departmental VLAN ports 1–24; production is 25–48 — *v3.1 §2.2.2, §9*.
- [GENERATED] Gate-based execution with machine-checked exits will catch more incomplete builds than a paper checklist, because §10.1's checklist is self-attested and unverifiable after the technician walks away. This is a design judgment, not a measured result — no before/after defect rate exists for this process.
- [GENERATED] `Get-CimInstance Win32_Product` is avoided for baseline software detection because enumerating it triggers MSI reconfiguration on every installed package. Registry uninstall-key enumeration is used instead. Well-established Windows behavior; not measured here.

## COUNTEREXAMPLE

- Gate 7's escrow check degrades to `MANUAL` on any endpoint without the ActiveDirectory RSAT module, which is most freshly imaged endpoints. The gate then depends on a human checking ADUC — the exact failure mode the gating was meant to remove.
- Gate 1 cannot be machine-verified at the time it is performed. The validator infers storage mode later from `Get-PhysicalDisk BusType`, which reports `RAID` for RST but can report `Unspecified` on some NVMe controllers, producing a false WARN.

## CONTRADICTIONS

- ! The source document states MDT is reachable only from the Departmental VLAN, yet gives the MDT server address as `[SUBNET]` and the production VLAN range as `[SUBNET]`, while WinPE on the Departmental VLAN receives `[SUBNET]`. Either MDT sits on the production subnet and reachability is enforced by ACL rather than isolation, or one of the published addresses is wrong. Treated as an ACL statement in this skill; the `[SUBNET]` literal is marked unverified in `references/network-and-vlan.md`.
- ! `operating-loxihart-service-desk/references/escalation-routing.md` assigns "MDT imaging" to L3, while v3.1 §1.3 assigns imaging execution to L1. Reconciled here as: L1 executes the runbook, L3 owns MDT/PXE server-side. If the routing reference is authoritative for ticket assignment, it needs updating to match.
- ! The upload contains three overlapping documents. `COMPLETE_v3.1.docx` (1,929 words) is an abridged variant of the Part1+Part2 pair (6,305 words) and its Appendix B RACI has fewer rows than Part2's Appendix C RACI. This skill is built from the two-part set. The abridged copy should be retired to prevent divergent guidance.
