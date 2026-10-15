---
name: pb-inbox-zero
description: >-
  Sort an email backlog into reply, delegate, archive and ignore, and draft
  the replies. Nothing is sent without your GO. Use for "inbox zero", "sort
  my mail", "clear my email backlog", "draft replies to my mail".
category: bdb-core
kind: playbook
trigger: ["inbox zero", "sort my mail", "email backlog"]
inputs: [mail_export_folder, "connector?"]
requires:
  skills: [memb-skill]
  agents: []
  mcps: []
  store: [email-ops]
go_points: [send replies]
outputs: ["triage.md", "drafts.md", "run-log.md"]
verify: "every mail in the export appears exactly once in triage.md"
difficulty: beginner
est_time: 10-20 min
---

# Inbox zero
What you get: your email backlog sorted into reply / delegate / archive / ignore, with reply drafts. Nothing is sent without your GO.

## Inputs
- A mail export folder (.eml or .mbox) — exported from your mail app; there is no mail connector configured by default
- A connector for sending — optional, you name it
- A save folder — asked once; default `./pb-inbox-zero-<date>/`

## Steps
1. Ask once — save folder, mail export folder, optional sending connector (email-ops if `test -d ~/.claude/skills/email-ops` passes; absent → logged "Missing store item: email-ops, install via aos-store" and the run continues with the connector the human names, or none) → `run-log.md` — the export folder holds at least one .eml or .mbox; if you have neither an export nor a connector, stop with `Missing mail source: export your inbox to .eml/.mbox` and write nothing but the run log
2. Read every mail → `triage.md`, one row per mail: sender, subject, date, class (reply / delegate / archive / ignore), one-line reason, source file — every mail in the export appears exactly once; the row count equals the mail count
3. memb-skill — optional, ask first: search open commitments to the senders to inform the class — skipped and logged if memB is not installed
4. For each reply row → `drafts.md`: recipient as name + address (`?` blocks sending until you fill it), subject, body — draft only, nothing is sent
5. Show `triage.md` and `drafts.md` in full and apply your edits until you approve — approval logged
6. [GO] Send the replies through the connector you named — show every recipient and the full text of every message first. The run stops here until the human types GO. The GO covers exactly the recipients and messages shown and nothing else; a different or added recipient needs a fresh GO. Never send to anyone not listed in `drafts.md`. The go-gate hook does not guard sending: this [GO] is the only guard. Without a connector you copy the drafts yourself and the hand-off is logged.

Run log: `run-log.md` in the save folder. One line per step as it completes (`N. done|skipped|failed — file — check result`), and `WAITING FOR GO: <step>` at the gate. Anything other than the literal GO (case-insensitive) is not a GO. If a check fails, stop, write the failure into the log and tell the user.
