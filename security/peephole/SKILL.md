---
name: peephole
description: Show or change Peephole's enforcement mode (guided (default), audit, strict, hardened, off). Use when the user says /peephole, wants to see the current security mode, or asks to make enforcement stricter or looser.
---

# Peephole mode control

Peephole is a plugin for coding agents: it steers the write and can ask or deny
before a file is saved. Modes:

- **guided** — **Default.** Findings are asks. Self-protection and org mandates still deny.
- **audit** — warn + log only. Org-`enforce` CWEs and self-protection still deny.
- **strict** — deny high-confidence CWE patterns, ask on lower-confidence ones.
- **hardened** — deny-by-default; deny unverified package installs and uninspectable writes.
- **off** — enforcement disabled.

## To change mode

**Raising** enforcement (to `strict` or `hardened`) can be done from the shell:

```sh
sh "$CLAUDE_PLUGIN_ROOT/hooks/peephole.sh" mode strict
```

**Lowering** enforcement (to `audit` or `off`) is a human-only action — peephole
denies a model-issued `mode off`/`mode audit` command as a self-protection
measure. To lower it, the **user** types the whole message `/peephole off` (or
`audit`), which the UserPromptSubmit hook applies directly. This prevents the
assistant from waiving the gate on its own.

## To see current mode and activity

Run `/sec-audit` (see the sec-audit skill), which prints the current mode, decision tally, and log-chain integrity.
