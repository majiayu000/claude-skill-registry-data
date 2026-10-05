---
name: factory-kit-audit
description: Measure the factory-kit's token footprint — baseline vs on-demand, heaviest assets, trim candidates
argument-hint: (no arguments)
---

You're auditing the factory-kit's token cost. This is a read-only report — no files change, no symlinks touched.

## What to do

1. **Resolve the kit root.** The script lives at `bin/kit-audit.sh` in the installed kit. Prefer the host's current-skill-directory capability and walk up from `skills/factory-kit-audit/` to the plugin root. For symlink installs, resolve the current `SKILL.md` symlink before walking up. Do not assume a fixed home-directory checkout.

   If the kit can't be found, tell the user to run the kit's `install.sh` first and stop.

2. **Run the audit.** Execute `<kit_root>/bin/kit-audit.sh` through the host's shell capability. The script prints the report to stdout.

3. **Show the output verbatim** in a fenced code block. Don't reformat it — the column alignment matters.

4. **One-line takeaway.** Below the code block, a single sentence calling out what matters most. Pick from:
   - Baseline cost framing — "Baseline is Xk tokens per session; everything else is on-demand."
   - Outlier flag — if the trim section named outliers, restate the action
   - All-good — "Kit is balanced; no trim work needed."

   No further commentary. The numbers speak; you point at the one thing worth doing.

## Style

Follow `factory-voice.md`. This is a diagnostic — terse, numbers-first, no narration. If the user asks "why X is so large," then dig in. Don't volunteer interpretation beyond the one-line takeaway.

The script's estimate is ~4 chars per token. Real tokenizer counts differ by 10-20%. Don't overstate precision — the relative shape across assets is what's actionable, not the absolute numbers.
