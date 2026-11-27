---
name: agent-harness-settings-parity
description: >-
  Enforce the same model, reasoning budget or thinking effort, auto-compaction threshold and
  approval mode across installed coding CLIs like Codex, Pi and OpenCode. When knobs differ in units
  (tokens, percent, fractions) or profiles override them, verify effective values with config
  readback and session traces. Not for hermes-models.
metadata:
  revision: "4"
  areas: "software-development"
  targets: "runtime-agnostic"
  summary: "hold one policy across every coding harness despite different config files, knob names and units"
  summary_zh: "让同一条策略在每个 coding harness 上生效，尽管配置文件、键名与单位各不相同"
  kind: "entry"
---

# Agent harness settings parity

Prove that the operator's policy holds across the installed harnesses and profiles in scope.
An audit is read-only; apply only the changes the operator authorized.

1. **Inventory.** Resolve each executable (including version-manager or package installs not
   on PATH), version, config root, and active profile or preset. Use that version's schema,
   help and docs to identify the knob, unit, default and override order. Treat existing values
   as hypotheses until read back.
2. **Translate.** Distinguish a trigger threshold from a reserve or buffer: for a reserve
   subtracted from the context window, threshold = window - reserve. Check the actual model
   window, unit and any additional caps. Prefer a percentage only if that version implements
   it with the semantics required by the policy. Check the scope that owns the effective value,
   including nested presets; a host-level setting may be inert.
3. **Apply.** Prefer the harness's validated config command, especially for protected files;
   otherwise back up the authorized file in the task directory before editing. Prefer a
   supported user-layer override. Report any managed or package-owned edit that an update
   could replace. Do not bypass approval or protection.
4. **Read back per version and profile.** Use the supported parse/dump/get command and
   distinguish parse success from effective-value proof. For a runtime-only value, use an
   isolated session with the same model and profile; cite the exact resolution event or other
   runtime evidence. A banner, config diff, or successful write is not runtime proof.
5. **Check activation.** Determine whether this version reloads config, reads it at startup,
   or restores a value on resume; test fresh and resumed sessions separately if both matter.
   Never interrupt real work to prove a setting. Let the turn finish; get explicit approval
   for any disruptive restart and state its impact on live sessions and watchers. A stopped
   harness needs no restart, but it does need runtime evidence before claiming parity.
6. **Report** harness/version/profile, key and unit, before/after, and exact readback or runtime
   evidence. Mark inaccessible or unsupported verification as unverified, not equivalent.

- When normalizing auto-compaction thresholds, read the
  [2026-11-21 key map](references/2026-11-21-context-compaction.md), then open only the harnesses in
  scope. Confirm lookup candidates against the installed versions before use.
- When verifying OMP model effort, read the [OMP runtime evidence note](references/harnesses/omp.md#runtime-evidence).
