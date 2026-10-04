---
name: ba-discovery
description: Use when the user explicitly wants a guided BA workflow across one or more phases toward a chosen outcome.
argument-hint: "[เป้าหมายหรือสิ่งที่ต้องการ]"
disable-model-invocation: true
---

# BA Discovery Pipeline

**Pipeline owns navigation. Phase skills own the work.**

Before creating or mutating Project Brain, read `${CLAUDE_PLUGIN_ROOT}/shared/contract-core.md` and `${CLAUDE_PLUGIN_ROOT}/shared/contract-snapshots.md`. Load `${CLAUDE_PLUGIN_ROOT}/shared/contract-records.md` only when routing or persistence needs record semantics. Read `${CLAUDE_PLUGIN_ROOT}/shared/contract-changes.md` when `.ba/changes/` exists or approved truth may be changing.


## Pending change guard

If relevant OPEN changes exist, treat them as visible **pending** context, not approved truth. Do not silently fold candidate meaning into canonical phase work. If the requested work is primarily changing already-approved truth, route the user to `/ba-change`.

## Structural validation

When Python 3 is available, run:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/ba_lint.py" --project "${CLAUDE_PROJECT_DIR}"
```

Use it on resume before trusting durable state and before presenting an approval-ready checkpoint. If Python 3 is unavailable, say plainly that **deterministic lint was not run**. The BA conversation may continue, but never claim structural validation without command evidence.

## Start / resume

1. Read `${CLAUDE_PROJECT_DIR}/.ba/PROJECT.md` if present.
2. If durable state exists, orient from current phase, current activity, target, pipeline status, current baselines, and Next Focus. Prefer **resume** over restarting.
3. If no Project Brain exists, do not create it merely to ask which Target Outcome the user wants. Bootstrap only when the first mutating phase actually starts.
4. Resolve **Target Outcome** from `$ARGUMENTS` or ask one simple question if unclear:
   - understand the problem,
   - validated requirements,
   - system design,
   - final FRD/spec.
5. When work begins, set `workflow_mode: PIPELINE`, the mapped `target_phase`, and `pipeline_status: ACTIVE`.

## Route one phase at a time

Map the next work to exactly one skill:

- UNDERSTAND → `/ba-understand`
- REQUIREMENTS → `/ba-requirements`
- DESIGN → `/ba-design`
- SPEC → `/ba-spec`

Do not copy or paraphrase another phase's playbook. Invoke that phase skill and let it own reasoning, persistence, and approval.

Preferred prior baselines are **Soft Guards**. If missing, explain the risk. Allow explicit approved external input and preserve provenance according to the Project Brain contract. Never fabricate the skipped baseline.

## Checkpoint contract

After a phase is explicitly approved and its snapshot exists:

1. return control here,
2. confirm the completed phase and snapshot,
3. compare current phase with the Target Outcome,
4. if target reached, set `pipeline_status: COMPLETE` and stop,
5. otherwise present the next phase in user language and ask whether to continue.

When an approved Final FRD/spec has just completed, you may offer one optional follow-up: `/ba-report` for a professional ELI5 FRD report. The report is **not** a pipeline phase or Target Outcome. Do not generate it unless the user explicitly wants it.

Never cross a phase checkpoint silently.

If the user pauses, keep the target, set `pipeline_status: PAUSED`, preserve exact current activity and Next Focus, and stop. A later `/ba-discovery` should resume from that durable state automatically.
