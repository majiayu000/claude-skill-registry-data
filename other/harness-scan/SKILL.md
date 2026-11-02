---
name: harness-scan
description: Scan a reference harness for material upstream drift and missing capabilities.
disable-model-invocation: true
---

# Harness Scan

Resolve the named reference harness or path; ask only when ambiguous.

1. Run `python3 harness_lifecycle/scan.py drift reference_harnesses/<name>`.
2. Run `uv run python harness_lifecycle/registry/registry.py gap <name>`: capabilities never ruled on, those changed
   upstream since their ruling, and those we have but never ruled on.
3. Report material drift and useful candidates, considering existing equivalents.
   Use harness-evaluate for an authorized curation decision.
4. When an authorized pin move happens, regenerate the catalog at the new pin;
   `registry.py status <name>` then shows which skills need analysis. The
   review follows `harness_lifecycle/playbook.md` §4: its report is
   `harness_lifecycle/registry/reviews/<yyyy-mm-dd>-upstream-<name>-<version>.yaml`
   (`registry.py report draft`), committed with the pointer.

Scanning does not authorize ledger records or adoption. When filing follow-up
work is authorized, `registry.py gap <name> --beads` prints creation commands to
review. Record decided outcomes in the registry ledger only within that authority.

These commands preserve submodule pins. Drift may fetch upstream refs; use its
`--no-fetch` option when offline or network access is outside the request.
Reject/defer is a valid outcome when a candidate adds no durable behavioral value.
