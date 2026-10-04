---
name: style-gate
description: The online VERIFY half of the style-replication loop — the first-span-feedback discipline with a different oracle (match against the Group C exemplar corpus in references/targets.json) and a different sensor (a sidecar-free Style Profile of the DELIVERED span-0 pixels via profile-clip, never our plans). On a levered-field mismatch (|z| > SG_Z vs the corpus distribution) it runs a bounded knob-first fix loop — moves.py maps the worst mismatches to CLAMPED ephemeral env deltas (JUMP_CUT_SEG, JUMP_CUT_MAX_GAP, SPEED, SWITCH_SPACING) in work/<id>/style.env, the entrypoint-owned SG_RERENDER_CMD re-renders span 0 with them, and the fix is accepted only when accept.py passes (no checked field worse, at least one improved, no new mismatch) AND span 0's grade.json did not regress (reuses first-span-feedback's check_grade.py). Accepted knobs steer spans 1..N (the entrypoint sources style.env before fan-out) and land in references/accepted.jsonl; mismatches no knob can reach are SURFACED for an operator-approved durable code change. Self-arming — no corpus targets or n < SG_MIN_REFS → exact no-op, so the stock pipeline is unchanged until a corpus is learned. NON-FATAL everywhere, idempotent (.sgmeta), STYLE_GATE=0 force-disables.
---

# style-gate

```bash
bash .claude/skills/style-gate/style-gate.sh <work_id> <clip_stem> <saved_mp4> [--pane <p>]
```

Emits `work/<id>/<stem>.style.json` (the match verdict: checked fields,
mismatches ranked by |z| each with lever + direction, diagnostic rows) and,
on an accepted move, `work/<id>/style.env` (the knob overrides spans 1..N
inherit) + a `references/accepted.jsonl` record.

Env: `STYLE_GATE` (1; hard no-op without `references/targets.json`),
`SG_Z` (1.5), `SG_MAX_ITERS` (1), `SG_MAX_MOVES` (2), `SG_MIN_REFS` (3),
`SG_RERENDER_CMD` (entrypoint-owned), `STYLE_REFS` (default `references/`).
Vision is off for gate profiling (`PROFILE_VISION=0` internally) — the gate
only scores deterministic levered fields, so it needs no model call.
