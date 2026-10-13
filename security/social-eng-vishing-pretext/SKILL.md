---
name: social-eng-vishing-pretext
description: >
  Run authorized voice-phishing (vishing) and pretext-based scenarios that test whether staff and
  help desks follow verification procedures — safely and by consent. Load after social-eng-methodology
  when the objective is phone/live-interaction based (help-desk password reset, MFA-reset abuse,
  pretext callback). Signals: "vishing", "call the help desk", "pretext", "test our verification
  process", "MFA reset social engineering".
domain: social-eng
type: technique
stability: learning
modes: [pentest]
severity: high
mitre: [T1598.004, T1656, T1566.004]
schema_version: 1
---

# Vishing & pretexting

## When it applies
The engagement authorizes live-interaction testing (cleared via `social-eng-methodology`) and the
objective is a process test: will the help desk reset a password or MFA without proper verification?
Will an employee act on a convincing caller? This targets *procedure adherence*, which phishing
email can't measure. Help-desk MFA-reset abuse is a leading real-world initial-access vector, so
testing it is high-value.

## Why it works
Voice adds urgency, authority, and social pressure that written channels lack — a confident caller
with a few true details (from `recon-osint`) and a plausible reason routinely gets a human to skip a
verification step. The finding is the *gap in the verification procedure*, not the individual who
answered.

## Method
1. **Define the process under test** and the pass/fail line with the client: e.g. "help desk must
   require callback-to-known-number + a second factor before any reset." The test measures whether
   that line holds.
2. **Build a proportionate pretext** within allowed themes — a plausible role (a named-role, not a
   real named person, unless consented), a believable reason, and only the OSINT detail needed for
   credibility.
3. **Prepare a call plan and an immediate stand-down.** Script the ask, the escalation, and the
   point at which you disclose. Keep the authorization/emergency contact ready if challenged.
4. **Execute a bounded number of attempts** per RoE, tracking each: target, request, which
   verification steps were performed vs. skipped, and the outcome.
5. **Stop at the objective.** Once a step is bypassed (or correctly refused), you have the result —
   do **not** proceed to actually reset/log in or take any real account action beyond proving the
   procedure gap; disclose per plan.
6. **Debrief.** Capture where the procedure failed and why; hand it to the awareness/report step.

## Gotchas
- **Prove the gap, don't exploit it.** A help desk agreeing to reset MFA *is* the finding — you do
  not complete a real takeover; stop and record it.
- **De-escalate distress.** If a target becomes anxious or suspicious, disclose the assessment and
  reassure them; their cooperation isn't the point, the procedure is.
- **No coercion or protected topics** — the excluded-theme and no-harm rules from
  `social-eng-methodology` apply in full over the phone.
- **Attribute cleanly** — use test lines/tokens so a call can be confirmed as the assessment, and
  coordinate so it isn't mistaken for a real fraud attempt.
- **Recording laws vary** — only record calls where lawful and agreed in the RoE.

## Verify success
A documented result per attempt — which verification steps held or failed and the outcome — with no
real account actions taken and every target debriefed, feeding a procedure-focused report and
remediation (stronger help-desk verification, callback policy, MFA-reset controls).

## References
MITRE ATT&CK T1598.004 (phishing for information via voice), T1656 (impersonation); help-desk
verification / MFA-reset hardening guidance.
