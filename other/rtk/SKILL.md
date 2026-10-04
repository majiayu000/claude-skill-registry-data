---
name: rtk
description: Use RTK explicitly to reduce verbose human-facing shell output while preserving structured data, failure evidence, and native command behavior. Load when the user asks for RTK, compact shell output, or an RTK-assisted command session.
compatibility: RTK 0.49.0 installed by the dots-managed Linux x86_64 launcher. No installation, hooks, shell replacement, or network access occurs when this skill loads.
metadata:
  provenance: https://github.com/rtk-ai/rtk/releases/tag/v0.49.0
  ownership: dots-installs-personal-skills-authors-policy
---

# RTK: explicit, opt-in compression

Use the dots-owned `rtk` executable explicitly. Loading this skill never installs software, changes PATH, modifies shell configuration, activates hooks, or rewrites commands automatically.

## Supported human-facing reads

Wrap only a supported read when compact output is useful. Examples:

```text
rtk git status
rtk git log -5
rtk cargo test
```

Check `rtk --version` and relevant help before unfamiliar usage. Keep harness-native search, read, edit, Git, and verification tools when they are more suitable. Do not guess wrappers. Run unsupported commands normally.

## Preserve correctness

Run the native command without RTK for:

- JSON, porcelain, NUL-delimited output, patch content, or machine-consumed pipelines.
- Complete audit evidence or output that another program will parse.
- Mutations, deployment, authentication, provisioning, or commands whose exact diagnostics matter.

RTK output is lossy. Preserve the exit status and report failures as failures. If details are missing, rerun the original command only when it is safe and repeatable. Never repeat a non-repeatable mutation just to recover output.

## Failure and missing-tool behavior

If `rtk` is missing or broken, report that limitation and use the native command as a safe fallback. Do not install or repair it implicitly. If a wrapped command omits needed diagnostics, capture the raw command output before making a claim.

## Verification

For a disposable repository read, compare native `git status --short` with `rtk git status` and confirm both represent the same changes. For a safe failing supported command, confirm RTK preserves the nonzero exit status. When reporting compression, measure observed output bytes for the specific command. Do not infer token, cost, or billing savings from byte reduction.

Read [references/scenarios.md](references/scenarios.md) when evaluating installation ownership, structured-output boundaries, or failure handling.
