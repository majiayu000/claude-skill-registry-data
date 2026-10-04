---
name: shadow-skill-publisher
description: Validate, package, submit, publish, or track a local Agent Skill through a safe, evidence-backed workflow.
---

# Shadow Skill Publisher

Use this Skill when validating, packaging, submitting, publishing, or tracking a local Skill. It is agent-neutral and does not require Ego or any browser runtime: local validation, packaging, confirmations, and status tracking run offline. Ego is an optional handoff tool only when a selected channel has no verified API or CLI, the browser surface is part of the documented contract, and the user explicitly authorizes that browser step. Keep the workflow deterministic and evidence-backed. Real platform writes, browser automation, and live channel adapters are limited to documented contracts and handoff instructions.

Follow this sequence exactly:

1. `observe`
   - Load the source, evidence profile, channel contract, and channel reference first.
   - Start without requiring the user to author `profile.json`. When the CLI reports `profile.origin=generated`, use its source-derived facts. Prompt-only Skills may use their frozen `SKILL.md` as core source evidence; scripted Skills remain blocked until execution or other verifiable evidence is supplied.
   - If `prepare` returns `needs_browser_observation`, use the browser flow in [references/browser-execution.md](references/browser-execution.md) to observe the signed-in creator page and update the private profile on the user's behalf. Do not ask the user to type account aliases or platform fields.
   - If `prepare` returns `user_confirmation_required`, draft the fields from source and channel evidence, then ask only for the user's final confirmation. Do not ask them to compose JSON manually.
   - Run local checks. When core evidence declares commands, inspect the source-bound execution plan and pass its current digest to `prepare --exec-digest`; missing or mismatched authorization remains blocked.
   - Package and verify each channel artifact before building its `SubmissionPlan`. Preserve successful channel attempts when another channel blocks.
   - Read [references/channel-contract.md](references/channel-contract.md) plus the selected channel reference before describing any remote step.
2. `authorize`
   - Show the upload disclosure and the current upload digest verbatim from the generated plan.
   - Record upload authorization only through the authorization workflow that binds the exact current digest.
   - A user saying "同意" or similar is not itself a stored authorization record.
3. `act`
   - Prefer the channel's official API or CLI when the verified contract documents one.
   - If no verified API or CLI exists, use a verified browser tool available to the host agent or hand off to any user-controlled browser as documented in [references/browser-execution.md](references/browser-execution.md). Ego is one optional provider, not a dependency.
   - Open the documented creator page, confirm the visible account, fill only fields from the current plan, upload the exact artifact, read back the rendered values, and stop before the final submit action.
   - Pause instead of guessing whenever the flow reaches login, CAPTCHA, QR scan, platform confirmation, user takeover, or an inactive browser space. A session expiry is `login_required`, not a request for credentials in chat.
   - Remote writes, prefills, uploads, and registrations stay bound to the exact `channel`, `account_alias`, artifact path, and artifact SHA-256 in the current plan.
4. `verify`
   - Read back the draft or product ID and the exact rendered field values from the remote surface before any submission step.
   - If the verified contract has no prior remote-write state, finalize against the adapter-defined local preview ID and the exact preview fields before any external write.
   - Unknown remote state is not success. Keep it unknown until read-back proves otherwise.
5. `record`
   - Persist the finalized plan after read-back, transition to `awaiting_submission_confirmation`, and show the new submission digest.
   - Submit or publish only after both current upload and submission authorizations match and the requested action equals the finalized plan's `final_action`.
   - Record lifecycle progress only from non-empty read-back evidence for the same platform ID and source version; `live` also requires the public URL.
   - Refresh the human-readable Markdown ledger after every persisted remote transition. Unchanged monitor observations stay write-free and silent.
6. `handoff`
   - If automation pauses or contract drift appears, hand off with the exact packet described in [references/browser-execution.md](references/browser-execution.md).
   - Do not ask the user to paste credentials, cookies, tokens, or QR payloads into chat.

For repeated work, read [references/orchestration.md](references/orchestration.md), then use `batch` to prepare independent source/channel attempts, `authorize-batch` to bind one acknowledgement to every unchanged digest in that receipt, `resume` to reconstruct bounded continuation packets, and `monitor` to ingest read-only observations. Batch authorization never covers a changed or newly added digest. Keep account-bound browser actions serial even when local packaging runs as a batch.

Store reusable commercial defaults, listing assets, and channel artifact exclusions in the private profile described by [references/user-config.md](references/user-config.md). Validate asset digests and verified channel limits before upload. Reuse a known `platform_id` as an update hint instead of creating a duplicate listing.

Run the local publisher with:

```bash
python3 scripts/publisher.py --help
```
