---
name: author-intent-yaml
description: Author a structured intent.yaml file (the ICE clean triple) from interview material. Takes an extracted interview digest (goal, constraints, failure conditions) and produces a well-formed intent.yaml conforming to the Garura intent schema. Scenarios and recovery are NOT written here — they are generated into the play's expectation.yaml by draft-play-expectation.
user-invocable: false
model: sonnet
allowed-tools: Read, Write
---

# author-intent-yaml

Model-invocable skill for producing a `intent.yaml` artifact from structured interview material.

## Purpose

The intent-crafter agent collects context through interviews and sharpening conversation. This skill takes that collected material and writes it to disk as a schema-conforming `intent.yaml`. The agent never writes YAML inline — all authorship happens here.

You DO create the intent.yaml artifact. You do NOT run interviews, do NOT sharpen vague answers, and do NOT decide whether the intent is good enough. That is the agent's job.

## Input

Receive from the agent:

| Field | Required | Description |
|-------|----------|-------------|
| `name` | yes | Dotted identifier for the intent (e.g., `fix-it`) |
| `description` | yes | One-paragraph description of the intent |
| `intent_statement` | yes | Free-text "what must be true when done" — the goal |
| `constraints` | yes | List of `{rule: string}` — agent-sharpened constraint text. IDs (C1, C2, …) are assigned by this skill. |
| `failure_conditions` | yes | List of `{condition: string}` — agent-sharpened failure text. IDs (F1, F2, …) are assigned by this skill. |
| `version` | optional | Semver string; defaults to `1.0.0` if absent |

Scenarios are NOT an input — the intent is the clean triple. Success scenarios and recovery are generated into `expectation.yaml` by `draft-play-expectation` after the intent is authored.
| `output_base` | yes | Directory to write `intent.yaml` into |

## Process

1. **Validate inputs.** Every constraint must have non-empty `rule`. Every failure_condition must have non-empty `condition`. If any field is empty, return structured failure: missing required content.

2. **Assign IDs.** Enumerate constraints as C1, C2, …; failure conditions as F1, F2, …. IDs are positional — input order is preserved.

3. **Reject implementation detail.** Scan constraint/failure text for the deny-list: play names, agent names, skill names, tool names, file paths inside the framework's own components. If found, return structured failure naming the offending tokens — the agent must re-sharpen before re-invoking. Intent never references execution mechanism.

4. **Emit intent.yaml** at `{output_base}/intent.yaml` with this exact top-level order:

   ```yaml
   intent: >
     {intent_statement — wrapped at ~72 columns}

   constraints:
     - id: C1
       rule: >
         {rule text}
     # ...

   failure_conditions:
     - id: F1
       condition: >
         {condition text}
     # ...

   version: {version}
   ```

   No `scenarios:` block — the intent is the clean triple.

5. **Return contract** with `intent_yaml_path` pointing at the written file, total counts per section, and the assigned max IDs.

## Output

```yaml
intent_yaml_path: "{output_base}/intent.yaml"
counts:
  constraints: {n}
  failure_conditions: {n}
max_ids:
  constraint: "C{n}"
  failure: "F{n}"
status: written
```

## Failure Modes

| What failed | Cause | Return |
|-------------|-------|--------|
| Missing required field on any entry | Empty rule / condition | `status: failed`, `reason: missing_required_field`, `entry_index` |
| Deny-list token found | Constraint mentions agent/skill/play/tool name | `status: failed`, `reason: implementation_detail`, `tokens` |
| Write failed | Disk error, permission | `status: failed`, `reason: io`, `error` |

## Boundaries

- You never interview users.
- You never sharpen vague text — if the agent passes vague text, you emit it as-is (or fail on empty).
- You never evaluate intent quality.
- You never invoke other skills.
