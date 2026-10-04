---
name: sflow-auto
description: Plan, ratify, inspect, and control one bounded Singularity Flow Auto flight.
disable-model-invocation: true
argument-hint: "plan <requirement> [--until <phase>] | plan --story <STORY-ID> | --goal <GOAL-ID> | adopt --from-adhoc <AHS-ID> | start <PLAN-ID> | list | continue <STORY-ID> | status|report|compare|needs-you|repair|respond|switch-unit|pause|stop|takeover|resume|discard <FLIGHT-ID>"

---
# Run bounded Auto work

<!-- sflow-output-contract: explicit-selection -->
**Output contract:** Collect every required choice explicitly; never infer or preselect; preserve errors, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

1. Use Boundary cwd. Without arguments, show forms and change nothing.
2. Plan with `singularity-flow auto plan "<REQUIREMENT>" [--until <PHASE>] --json` or `singularity-flow auto --goal <GOL-ID|GEX-ID> --json`. Ask among returned eligible capability IDs or relay `CAPABILITY_REGISTRATION_REQUIRED`; never invent one. Show Plan/Story/branch and complete ratification-packet SHA-256. Planning grants no authority.
3. Model-free reads are `singularity-flow auto plan --story <STORY-ID> --json`, `singularity-flow auto show-plan <PLAN-ID> --json`, `singularity-flow auto list --json`, `singularity-flow auto status <FLIGHT-ID> --json`, `singularity-flow auto report <FLIGHT-ID> --json`, `singularity-flow auto needs-you <FLIGHT-ID> --json`, and `singularity-flow auto continue <STORY-ID> --json`. Use `singularity-flow auto compare <FLIGHT-ID> --study <ID> --json` only for a reviewed study. `singularity-flow auto adopt --from-adhoc <AHS-ID> [options] --json` verifies effects and moves no bytes.
4. Start after the user types the full packet hash: `singularity-flow auto start --plan <PLAN-ID> --confirm <PACKET-SHA256> --json`. Never extract or prefill confirmation.
5. Preview `singularity-flow auto repair <FLIGHT-ID> --refusal <REFUSAL-ID> --json`; show scope, evidence, budget, eligibility, and hash. Confirm only a user-typed hash. Machine-actionable policy permits one repair for an unchanged Candidate with failed deterministic verification; otherwise stop, and halt after a second failure.
6. Show Human Request options. Respond with `singularity-flow auto respond <FLIGHT-ID> --request <REQUEST-ID> --choice <ID> --confirm <REQUEST-SHA256> --json`; use allowed `--answer` or credential `--broker-reference`. Never collect credentials. A response does not approve, waive, or resume.
7. Preview `singularity-flow auto switch-unit <FLIGHT-ID> --execution-unit <ID> --reason "<TEXT>" --json`; apply only its exact-hash command. It links a new attempt, not a new Task Contract.
8. After showing the complete checkpoint SHA-256, control with `singularity-flow auto pause|takeover|stop <FLIGHT-ID> --confirm <HASH> --json`; resume uses `singularity-flow auto resume <FLIGHT-ID> --confirm <HASH> --json` and open requests block it. Discard requires the user to type the exact flight ID as confirmation; `halt` aliases stop.
9. Reports show contracts, events, Candidate, lineage, and quality. Only `singularity-flow auto compare` reports reviewed Impact comparison. Never invoke `singularity-flow auto flight-step` directly, infer tokens/hashes, expose prompts, rank people, waive authority, expand scope, merge, or deploy. Report failures, Git outcome, checkpoint, and one exact next command.
