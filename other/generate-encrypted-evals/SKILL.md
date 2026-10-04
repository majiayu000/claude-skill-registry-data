---
name: generate-encrypted-evals
description: Generate testable verification evaluations from spec inputs (product-spec behaviors, verification scenarios, epic success and failure conditions, LLD exit-gate text), encrypt the resulting YAML with AES-256-CBC + PBKDF2, delete plaintext, and write a manifest.json. Single common skill for the evals-engineer agent.
user-invocable: false
model: sonnet
allowed-tools: Read, Write, Bash
deprecated: true
deprecated_note: '#434 ProductOS realignment — superseded by the command model; retained for Phase E reference, not installed'
---

# generate-encrypted-evals

Model-invocable skill that owns all mechanical steps of eval generation + encryption + manifest authorship for the `evals-engineer` agent.

## Purpose

The agent reads spec artifacts and assembles a generation request. This skill takes that request, generates concrete testable evaluations, encrypts the file, deletes plaintext, verifies no plaintext remains on disk, and writes the manifest.

One skill, many generation modes. The agent tells the skill what to generate via an `include` list. Encryption boundary lives here — not in the agent prompt.

## Input

| Field | Required | Description |
|-------|----------|-------------|
| `product_spec_path` | yes | Path to product-spec.md |
| `scenarios_path` | yes | Path to scenarios.md (verification scenarios) |
| `epics_path` | yes | Path to epics.yaml |
| `epic_id` | yes | Target epic ID (e.g., `E1`) |
| `phase_num` | yes | Phase number (e.g., `1`) |
| `lld_exit_gate` | yes | Extracted exit-gate text — NOT the full LLD |
| `include` | yes | List of eval sources to generate from: `behaviors`, `scenarios`, `epic_success`, `epic_failure`, `exit_gate`. Any non-empty subset. |
| `milestone_id` | optional | For validate-play mode; scopes eval set to a single milestone |
| `encryption_key_env` | yes | Name of env var holding the passphrase (never the passphrase itself) |
| `output_base` | yes | Directory outside the repo for encrypted eval + manifest |

## Process

1. **Read inputs.** Load product-spec, scenarios, epics, exit-gate text. For each requested source in `include`:
   - `behaviors` — enumerate B-xxx IDs, extract behavior text, map to testable eval
   - `scenarios` — enumerate SC-xxx IDs, derive concrete pass/fail checks
   - `epic_success` — enumerate success scenarios for `epic_id`, derive evals
   - `epic_failure` — enumerate failure conditions for `epic_id`, derive evals
   - `exit_gate` — derive evals from the LLD exit-gate text

2. **Author plaintext eval YAML.** Each eval entry contains:

   ```yaml
   - eval_id: E-{epic_id}-{phase}-{seq}
     category: behavior | scenario | epic_success | epic_failure | exit_gate
     source_id: {B-xxx | SC-xxx | epic_id | ...}
     description: {one-line}
     method: {how to verify — grep, command, file-shape check, etc.}
     pass_criteria: {concrete}
     fail_criteria: {concrete}
     priority: P0 | P1 | P2
   ```

   Write plaintext to a temp file at `{output_base}/evals-{epic_id}-phase-{phase_num}.yaml.tmp`.

3. **Encrypt.** Use `openssl enc -aes-256-cbc -pbkdf2 -salt -in <tmp> -out <tmp>.enc -pass env:{encryption_key_env}`. The passphrase is referenced via env var — never read into this skill's context.

4. **Delete plaintext.** `rm <tmp>`. Then verify with `ls {output_base}/*.tmp 2>/dev/null` — if ANY plaintext remains, halt with `status: failed`, `reason: plaintext_residue`.

5. **Write manifest.json** at `{output_base}/manifest.json`:

   ```json
   {
     "manifest_version": 1,
     "epic_id": "{epic_id}",
     "phase_num": {phase_num},
     "milestone_id": "{milestone_id|null}",
     "eval_count": {n},
     "counts_by_category": { "behavior": n, "scenario": n, ... },
     "encrypted_path": "{output_base}/evals-{epic_id}-phase-{phase_num}.yaml.enc",
     "encryption": "aes-256-cbc+pbkdf2",
     "key_env": "{encryption_key_env}",
     "generated_at": "{ISO-8601}",
     "source_hashes": {
       "product_spec": "sha256:...",
       "scenarios": "sha256:...",
       "epics": "sha256:...",
       "lld_exit_gate": "sha256:..."
     }
   }
   ```

6. **Return** the output contract.

## Output

```yaml
encrypted_eval_path: "{output_base}/evals-{epic_id}-phase-{phase_num}.yaml.enc"
manifest_path: "{output_base}/manifest.json"
eval_count: {n}
counts_by_category: { ... }
status: written
```

## Failure Modes

| What failed | Cause | Return |
|-------------|-------|--------|
| Spec input unreadable | I/O | `status: failed`, `reason: missing_input`, `path` |
| Empty `include` list | No sources requested | `status: failed`, `reason: no_sources` |
| openssl not on PATH | Tooling | `status: failed`, `reason: encryption_tool_missing` |
| Encryption failed | openssl non-zero exit | `status: failed`, `reason: encryption_failed`, `stderr` |
| Plaintext residue | Delete failed or glob found `.tmp` | `status: failed`, `reason: plaintext_residue`, `paths` |
| Zero evals generated | No matching content across `include` | `status: failed`, `reason: empty_eval_set` |

## Boundaries

- You never read implementation code, builder prompts, builder reasoning, prior eval results, technical-approach, or CLAUDE.md. Same context-isolation rules as evals-engineer.
- You never decrypt or read an encrypted eval file.
- You never verify evals against an implementation — that is judge's domain.
- Output paths are always OUTSIDE the repo to prevent accidental commit of plaintext or key material.
- The encryption passphrase is referenced only via `encryption_key_env` — never passed as a literal.
