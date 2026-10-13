---
name: social-eng-physical
description: >
  Run an authorized physical social-engineering assessment — tailgating, pretext entry, badge/RFID
  cloning checks, and media-drop tests — to measure physical and human access controls safely. Load
  after social-eng-methodology when the objective is on-site. Signals: "physical pentest", "test our
  building access", "tailgating", "badge cloning", "USB drop", "can we get into the office/data
  center". Requires a carried authorization letter.
domain: social-eng
type: technique
stability: learning
modes: [pentest]
severity: high
mitre: [T1566.004, T1091, T1200]
schema_version: 1
---

# Physical assessment

## When it applies
The engagement authorizes on-site testing (cleared via `social-eng-methodology`) with a defined
objective — reach a floor/room, plug into the network, or drop test media — to measure physical
access controls and staff response. Physical work has the highest real-world risk (police, injury,
genuine alarm), so the guardrails are non-negotiable.

## Why it works
Physical security leans on people extending courtesy (holding a door), trusting a uniform or a
confident manner, and following habit over procedure. A tester with a plausible pretext and a hi-vis
vest often walks past controls that are technically sound — the finding is the *procedural/behavioral
gap*, captured with minimum intrusion.

## Method
1. **Carry authorization.** A signed get-out-of-jail letter on you at all times, plus a live
   emergency contact (client-side) reachable to confirm the test instantly to security or police.
   No letter → no entry.
2. **Objective and stop-line, agreed in writing.** Reach the target and prove it (a photo of a
   defined marker, a benign network beacon) — then **stop**. No damage, no real data theft, no
   accessing others' belongings.
3. **Recon the site** (public, non-intrusive): entry points, badge readers, delivery/smoking doors,
   shift changes, dress code — enough for a credible pretext.
4. **Choose the least-intrusive technique for the objective:**
   - **Tailgating / pretext entry** — follow a group or present as delivery/contractor/new-hire to
     test door and reception controls.
   - **Badge/RFID exposure check** — assess whether badges are clonable at a realistic distance and
     whether readers accept a cloned/observed credential (demonstrate the exposure; don't build a
     persistent illicit credential).
   - **Media drop** — leave tracked, benign test USBs/QR flyers to measure plug-in/scan rate; the
     payload only phones home a token, it does nothing to the host.
5. **Prove and withdraw.** Capture the agreed proof at the stop-line and leave; do not push further
   "because it's working".
6. **Debrief and restore.** Recover any dropped media where feasible, disable beacons, and report.

## Gotchas
- **Present the letter the instant you're challenged** — never bluff past a security guard or police;
  disclose and let the emergency contact confirm.
- **Two-person rule for higher-risk entries** where the RoE allows, for safety and witnessing.
- **Benign media only** — a test USB beacons a token; it must not deploy real malware or alter the
  host. The metric is "someone plugged it in".
- **Respect people and property** — no searching desks/bags, no coercion, no entering genuinely
  restricted safety areas beyond scope.
- **Reversible and clean** — leave the site as found; account for every dropped item.

## Verify success
The agreed proof-of-access (marker photo or benign beacon) or a media-drop plug-in metric, obtained
at the stop-line with authorization carried, nothing damaged or taken, and all test artifacts
accounted for — feeding a physical-controls report and remediation.

## References
MITRE ATT&CK T1091 (Replication Through Removable Media), T1200 (Hardware Additions), T1566.004;
standard physical-pentest RoE and safety practice.
