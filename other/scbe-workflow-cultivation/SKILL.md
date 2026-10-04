---
name: scbe-workflow-cultivation
description: "Cycle operational workflows like a cultivation loop: scan lanes (meridians), detect blockages, apply the smallest fix, then compress output into reusable qi pellets (runbooks/scripts/skill patches). Use for self-healing ops across GitHub CI, connectors, GitLab mirrors, publishing, and research ingestion where you want iterative refinement instead of new features."
---

# SCBE Workflow Cultivation

Cultivation = a bounded loop that turns messy execution (logs, failures, partial wins) into refined, reusable artifacts.

## Key mapping (metaphor -> engineering)

- `Meridian` = a workflow lane with endpoints and failure modes (CI, deploy, ingest, publish, mirror).
- `Blockage` = a repeatable failure that constrains flow (auth, flaky test, drift, missing doc, wrong default).
- `Qi pellet` = a compressed reusable unit:
  - a runbook page
  - a deterministic script
  - a skill patch
  - a minimal invariant test
- `Tribulation` = a failure you *expect* during a cycle (used to harden the lane, not to panic).
- `Breakthrough` = lane returns to green and produces a pellet (not just "it worked once").

## Cultivation loop (one cycle)

1. **Set bounds (qi budget)**
   - time budget (e.g. 25 minutes)
   - risk budget (`read-only`, `write-safe`, `destructive`)
   - exit condition (what "green enough" means)

2. **Meridian scan (cheap signal)**
   - run only the lowest-cost checks that reveal blockages
   - capture the output as evidence (path, timestamp)

3. **Pick one blockage**
   - choose the smallest root cause you can actually remove in-budget
   - avoid feature work; this is flow repair

4. **Apply the smallest fix**
   - change the minimum number of files
   - prefer deterministic scripts over "remember to do X"

5. **Validate narrowly**
   - run the smallest smoke check that proves the blockage is gone

6. **Compress into a qi pellet**
   - distill: what was blocked, why, what fixed it, proof, and next action
   - store in a predictable location for future reuse

7. **Decide next cycle**
   - stop if you hit exit condition or budget
   - otherwise repeat with the next blockage

## Meridian scan: default lane list (edit per task)

Pick the lanes that matter to the task:

- `git`: dirty state, drift, upstream tracking
- `github-ci`: PR checks failing, daily failures, flaky jobs
- `connectors`: missing tokens, 401/403, MCP doctor failures
- `gitlab-pond`: mirror failures, token scope, project access
- `publish`: Hugging Face upload, website deploy, KDP/Stripe ops
- `ingest`: Notion export ingest, Obsidian sync, training-data merges

## Qi pellet format (compression contract)

Every cycle should emit *one* pellet (markdown) with this minimum:

- `timestamp` + `timezone`
- `lane` + `blockage`
- `root cause` (one sentence)
- `fix` (exact file(s)/command(s))
- `evidence` (paths / run output)
- `regression guard` (test, assertion, or doc rule)
- `next action` (one line)

### Generate a pellet scaffold (script)

Use the bundled script to create a pellet template:

```powershell
python "C:\Users\issda\.codex\skills\scbe-workflow-cultivation\scripts\qi_pellet_init.py" `
  --title "Fix GitLab mirror redaction" `
  --lane gitlab-pond `
  --out-dir "C:\Users\issda\SCBE-AETHERMOORE\artifacts\cultivation"
```

### Run a meridian scan (second bundled script)

Collect cheap signals and write one JSON scan artifact per cycle.

Local-only (no network):

```powershell
python "C:\Users\issda\.codex\skills\scbe-workflow-cultivation\scripts\meridian_scan.py" `
  --repo-root "C:\Users\issda\SCBE-AETHERMOORE" `
  --out-dir "C:\Users\issda\SCBE-AETHERMOORE\artifacts\cultivation"
```

Optional checks:

```powershell
python "C:\Users\issda\.codex\skills\scbe-workflow-cultivation\scripts\meridian_scan.py" `
  --repo-root "C:\Users\issda\SCBE-AETHERMOORE" `
  --out-dir "C:\Users\issda\SCBE-AETHERMOORE\artifacts\cultivation" `
  --check-gh-auth `
  --check-gh-pr-checks `
  --check-gitlab-pond --gitlab-repo-url "https://gitlab.com/<group>/<project>.git"
```

### Aggregate pellets into a qi bank (optional script)

```powershell
python "C:\Users\issda\.codex\skills\scbe-workflow-cultivation\scripts\qi_bank_aggregate.py" `
  --in-dir "C:\Users\issda\SCBE-AETHERMOORE\artifacts\cultivation" `
  --out-dir "C:\Users\issda\SCBE-AETHERMOORE\artifacts\cultivation"
```

## How to use $skill-synthesis (inspiration, not duplication)

When the task feels "infinite" or metaphor-heavy:

- Use `skill-synthesis` packet discipline:
  - Packet A: scan + evidence
  - Packet B: pick one blockage
  - Packet C: implement
  - Packet D: validate
  - Packet E: compress pellet

If you need a multi-skill run, generate a stack:

```powershell
python "C:\Users\issda\.codex\skills\skill-synthesis\scripts\compose_skill_stack.py" --task "Cultivation loop: clear CI failures and distill runbooks" --top 8
```

## How to use $skill-update (refinement mechanic)

If you hit the same blockage twice, the pellet should usually be a **skill update**, not a one-off fix.

Use `skill-update` when:

- you had to remember a fragile procedure
- a script/runbook was missing
- the same auth/mirror/CI issue repeats
- the "fix" was a sequence of manual steps

Validation rule for skill updates:

- update the skill
- run `quick_validate.py`
- run one real smoke check that uses the updated instructions

## Stop conditions (avoid infinite cultivation)

Stop when any of these are true:

- budget exceeded
- no clear next blockage is smaller than the current one
- changes would become destructive (needs explicit permission)
- you produced a pellet and the lane is green enough for the upstream goal

## Resources

### scripts/

- `qi_pellet_init.py`: create a pellet bundle (md + json) directory
- `meridian_scan.py`: collect cheap lane signals into one JSON scan artifact
- `qi_bank_aggregate.py`: roll up pellet JSON into a bank (json + md)
