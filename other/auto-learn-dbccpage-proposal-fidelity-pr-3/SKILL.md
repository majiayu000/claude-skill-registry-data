---
name: auto-learn
description: "Recall repository lessons, apply a supported correction and recheck the original task in the current IDE."
operad_source_colours: ["State", "Audit", "Code", "Contract"]
operad_target_colour: "Contract"
operad_arity: 4
operad_residual: "unknown"
families: [meta, governance, adversary]
---

# Auto Learn

**AuthorityEffect:** `None`.

Use `/auto-learn <task or concrete observation>` in the current IDE session.
The durable result is a useful change to the existing implementation or agent
estate, recalled when the next task needs it. A collection of new reports is not
the learning outcome. This is inspired by the requested Antigravity LEARN
behavior. No installed LEARN specification was located in the inspected
Antigravity built-in skills or bundled extension; this is an independently
adapted repository workflow, not a clone of a private implementation.

## Before Work and Every Worker Spawn

1. Read this guidance before starting substantive work. Include this instruction
   and the relevant lesson paths in each spawned worker's brief; the worker reads
   them before acting. Shared context is enough: do not invent a startup service.
2. Search the existing catalog and affected code for the actual task, failure and
   correction. Use targeted `rg` searches in `.agents/skills`, `.agents/rules`,
   `.agents/antiskills`, `.agents/patterns`, `.agents/antibodies` and the
   applicable typed catalog. Open the matching entries, not the entire garden.
3. Recall the applicable procedure, counterexample and exceptions in the working
   brief. Check whether the source or implementation changed before trusting an
   old lesson. Reuse the existing owner; avoid a parallel rule or skill.

## Learn, Apply and Recheck

1. Identify a concrete obstruction, correction or helpful alternative from the
   actual work: rejected input, wrong output, failed assumption, operational
   failure, user correction or successful repair. Keep the original need visible.
   Read decisive source/code and contrary evidence. A filename, PASS label or
   agreement between personas is insufficient.
2. Explain the failure, witness, supported cause, correction, observed check,
   applicability and exceptions. Use these existing lesson concepts in the
   working context; a nine-field JSON record is optional. Separate an observed
   cause from a hypothesis, retained evidence from a new execution and finite
   checks from general mathematical claims.
3. Deduplicate against the existing owner. Apply the smallest HIGH-confidence
   change within the authorized task: fix code, improve the relevant skill or
   rule, or add a concrete anti/helpful pattern. If a source-reported lesson is
   unverified, preserve that limit instead of installing an unconditional rule.
   If no justified reusable change exists, say so; do not manufacture learning.
4. An anti-skill names the forbidden procedure and its falsifier. An antibody
   binds an actual prompt, fixture or detector and states both the harmful trigger
   and a benign negative control. Use the existing typed admission/generation
   and OEEIS activation rules when applicable. A new sighting never activates a
   detector; a detached slogan is not an antibody.
5. Recheck the original need against the changed artifact. Choose the smallest
   relevant observation, source inspection, executable check or user-visible
   exercise; honor the user's testing constraints. Report exactly what happened.
   A useful source edit can be completed while an unavailable proof or live check
   remains open. Never change frozen pins, old receipts or assertions to invent
   success.
6. Mirror only selected canonical agent files to the active host destinations
   through the existing generation/parity path. Inspect affected bytes and links.
   Preserve unrelated host-maintained agents, skills, rules and workflows.
   For typed digested guidance, inspect both generated Markdown and the composed
   instruction operand: source limits, deciding controls and exceptions must reach
   the worker through either path. Reuse the existing typed compiler and owners.
   After an owner relocation, inspect the successor content and update the typed
   source path/hash together. Check the inherited packages on merged main first;
   retain old evidence and never recreate a retired owner just to satisfy a hash.
   Lint the composed Markdown too: generated titles, instruction headings and
   attached-prompt headings share one document even when each fragment is valid.
7. Carry unresolved findings and applicable learned paths into the next worker
   brief. Stop when the useful correction and original-task recheck are complete,
   or when a concrete residual needs new input. Do not create another framework.

## Automated Repair Step (`remediation_suggestions`)

When `remediation_suggestions` are emitted by `auto-anti-pattern-lint` or an AutoP
post-run handoff:

1. **Invocation**: Run `py -3.12 operads/skills/auto-learn/scripts/auto_learn.py --repair`
   (optionally passing `--remediations <json_file>`, `--changed`, or `--files <file...>`).
2. **Smallest High-Confidence Correction**: The engine evaluates each suggestion against
   proven dual healthy patterns:
   - `AP_MD_058` (`markdown_asterisk_list_syntax`): Replaces leading asterisk bullet
     markers `* ` with hyphen bullet markers `- `, strictly preserving indentation,
     achieving MD004 compliance with the minimal character diff.
   - `AP_PY_001` (`blanket_mypy_ignore`): Probes `mypy --show-error-codes` via shadow file
     evaluation to extract exact scoped compiler error codes on the target line, replacing
     blanket `# type: ignore` with scoped `# type: ignore[code1, code2]`.
   - Ambiguous or non-high-confidence patterns without definitive compiler or pattern
     evidence are held for manual review rather than guessing or applying speculative rewrites.
3. **Fail-Closed Diff Re-Check**:
   - Computes unified diff and captures repository `git diff`.
   - Re-runs `anti_pattern_lint.py --files <file> --check` against each repaired file.
   - For Python files, re-checks `mypy` against the modified file to ensure compiler acceptance.
   - If violations remain or unexpected errors occur, automatically rolls back file
     modifications to the pre-repair snapshot (`FAILED_RECHECK_ROLLED_BACK`).
   - If verification passes, outputs the verified clean git diff and records the receipt
     (`VERIFIED_CLEAN`).

## Finish Hook and Storage


After each outer `/adversary` or `/adversary-digests` run, including a partial or failed
run, `/auto-oe-autop` invokes this skill once in the current IDE with the original
need, actual observations, changed paths and remaining findings. Run the same
small loop on a failed run; a missing prerequisite can itself yield a scoped
lesson without pretending the original task succeeded.

Inner AutoP, Adversary and learning helpers return their observations to the outer
run. The outer finish consumes those observations once. Learning edits and their
recheck do not invoke another finish hook. This prevents an AutoP -> Adversary ->
AutoP or auto-learn -> auto-learn recursion chain. Use a simple in-session flag
or the existing task context; no persistent hook registry is needed.

Routine IDE learning requires no new receipt, intake file, `lessons.json`,
`learning.json`, novella or learning run directory. Temporary backend exchange
state is fine. Keep useful knowledge in the existing code/skill/rule/pattern and
summarize the change, recheck and residual in the normal response. Preserve
historical evidence already on disk. Use the existing typed intake and receipt
commands only when the task explicitly needs source-bound interchange, native
execution evidence or custody-preserving cleanup.

Never copy credentials, environment dumps, private conversations or raw provider
secrets into learned artifacts. A narrow sanitized source reference is enough.
