---
name: auto-oe-autop
description: "Finish each Adversary run with scoped IDE learning and practical repairs; run the full estate-maintenance pipeline only when explicitly requested."
invocation: entry
operad_source_colours: ["State", "Audit"]
operad_target_colour: "Contract"
operad_arity: 2
operad_residual: "unknown"
families: [meta]
---

# Auto OE Autop

**AuthorityEffect:** `None`.

The default `/auto-oe-autop` is a small finish step in the current IDE session.
After every outer `/adversary` and `/adversary-digests` run, including partial or failed
work, invoke [/auto-learn](../auto-learn/SKILL.md) once with the original need,
concrete observations, corrections, changed paths and unresolved findings.
Do useful learning now; do not substitute a receipt pile for applied structure.

## Routine Finish

1. Read `auto-learn`, recall relevant existing owners and inspect the actual
   obstruction/correction. Every spawned worker also reads that guidance and the
   relevant lesson paths before acting.
2. Deduplicate against the existing catalog. Apply the smallest HIGH-confidence
   code, skill, rule or concrete anti/helpful-pattern improvement in scope.
   A proposed antibody must bind a tangible prompt, fixture or detector with a
   falsifier and benign control; existing activation rules still apply.
3. Recheck the original need using a focused check appropriate to the change and
   the user's instructions. Distinguish observed results from source reports,
   implementation completion from proof and unavailable checks from failure.
4. Mirror only selected canonical agent changes through the existing host path.
   Preserve unrelated host-maintained files and all historical evidence.
5. Put applied paths, the actual recheck and unresolved next steps into the normal
   response and next worker brief. If no justified improvement exists, say so.

No new receipt, intake file, `learning.json`, proposal queue entry or run directory
is required for routine learning. Temporary state is sufficient. Do not sweep
the repository, run every anti-pattern package or archive files merely because
this finish step was invoked. Deletion/archival follows the user's separately
authorized scope and existing custody rules.

## One Outer Finish, No Recursion

The outer run owns this finish step. Inner AutoP/Adversary/auto-learn helpers return
their findings to it; the outer finish consumes them once. Applying a lesson and
rechecking it do not start another AutoP finish. A simple in-session flag or the
existing task context is sufficient; no scheduler or hook registry is needed.

If a Python call requests IDE learning from a bare shell, it must return a pending
IDE action honestly. A shell cannot impersonate this assistant session or switch
to OpenRouter. The skill performs the IDE action with available host tools.

## Explicit Estate Maintenance

Run the full sequential nine-stage script only for an explicit maintenance
request or an explicitly configured legacy maintenance integration:

```powershell
py -3.12 operads/skills/auto-oe-autop/scripts/orchestrate_autop.py --maintenance --verbose
```

Existing callers that explicitly supply `--receipt` or `--output` retain their
legacy maintenance behavior with a warning; new calls should use `--maintenance`.
Combining those options with `--post-run` is an error. No arguments/default mode
and `--post-run` remain receipt-free IDE handoffs.

The preserved [legacy maintenance reference](references/legacy_maintenance.md)
describes stages 0 through 8, prior self-review handoffs, admission history,
budget/parity checks, documentation and governance repair machinery. That
reference is not an automatic after-run instruction.

Inspect actual maintenance stage statuses, including failures and skips; do not
require or manufacture nine PASS labels. Do not replay an already applied repair.
Keep specialized native/research authorities, sealed sources and evidence
contracts in their existing owners. Automatic skill admission does not activate
an antibody, establish proof or grant execution authority.

Keep changed skill Markdown below 300 lines and 20 KB, UTF-8 without BOM. Inspect
formatting and local links for selected files; use available focused linting when
appropriate, without introducing a whole-repository test requirement.
