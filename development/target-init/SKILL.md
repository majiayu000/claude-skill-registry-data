---
name: target-init
description: Initialize a bug-bounty target from its http.md seed. Use when a new targets/<name>/http.md exists, or when the user says "start target <name>", or when targets/<name>/status.json is missing. Parses scope, auth, notes into normalized status.json so all downstream skills can read scope without re-parsing.
---

# target-init

## Purpose
Convert the user-authored `targets/<name>/http.md` seed file into a
normalized `targets/<name>/status.json` so every later skill can read
scope, auth type, and notes from a single structured place.

## Inputs
- `targets/<name>/http.md` (required) with sections **Scope**, **Auth**,
  **Notes** as documented in `PLAN.md > §6`.

## http.md template
```markdown
# <target name>

## Scope
- in:  example.com
- in:  *.example.com
- out: blog.example.com

## Auth
- type: session
- creds: caido_workflow:login-user-a
- creds: caido_workflow:login-user-b   # optional second account for idor

## Notes
- prior bugs: <free text>
- rate limits: <free text>
- known auth quirks: <free text>
```

## Steps
1. Read `targets/<name>/http.md`. If missing, abort with a message
   linking the template above.
2. Parse `## Scope`: collect `in:` and `out:` lines into
   `{in: [...], out: [...]}`. Allow `*` glob; convert to regex.
3. Parse `## Auth`: extract `type` and zero or more `creds:` lines.
4. Parse `## Notes`: keep as raw markdown string.
5. Build `status.json` skeleton:
   ```json
   {
     "name": "<name>",
     "created_utc": "<iso>",
     "scope": { "in": [...], "out": [...] },
     "auth":  { "type": "...", "creds": [...] },
     "notes": "...",
     "phase": "init",
     "phases": { "init": { "status": "done", "ts": "<iso>" } },
     "errors": []
   }
   ```
6. Write `targets/<name>/status.json`. Do NOT clobber if one exists —
   merge (preserve `phases.*` entries already there).

## Outputs
- `targets/<name>/status.json` (created or merged).

## Follow-up (post js-index)

After `js-index` lands `index/frameworks.json` and
`chain-triage`/`extract_chains_bounded` lands `chains/triage.json`,
run the V2 flag recommender once per target so V2 subsystems are not
silently off:

```bash
python3 bin/recommend_v2_flags.py <name>
source targets/<name>/v2_flags.env
```

The recommender is read-only against the per-target snapshot DB
(no LLM, no API key). It writes `targets/<name>/v2_flags.env` and a
`status.json.phases.v2_recommend` block listing the chosen flags and
why each one fired.

## Failure modes
- `http.md` missing → emit template, halt.
- Empty scope → halt, demand user add at least one `in:` line.
- Unknown auth type → halt, list supported types
  (`session | bearer | none | mtls`).

## Result block written to status.json
```json
"phases": { "init": { "status": "done", "ts": "<iso>", "scope_in": N, "scope_out": M } }
```
