---
name: clawpatch
description: "Clawpatch review/fix/revalidate loop. Verify findings, preserve IDs, triage with evidence."
---

# Clawpatch

Trigger: user says `clawpatch`, clawpatch finding/review/fix/revalidate/triage, deslopify loop.

Refs: [official docs](./references/official-docs.md), [CLI](./references/cli.md). Exact flags? run `clawpatch <cmd> --help`.

Core rule: finding = hypothesis. Verify current code before fix/triage/claim.

## Flow

1. Guardrails:

```bash
git status --short
test -f AGENTS.md && sed -n '1,220p' AGENTS.md
test -f AGENTS.local.md && sed -n '1,220p' AGENTS.local.md
clawpatch --help
clawpatch review --help
clawpatch show --help
clawpatch revalidate --help
clawpatch triage --help
```

2. Review:

```bash
clawpatch review --mode deslopify --limit 10 --reasoning-effort high --jobs 10
clawpatch status --json
clawpatch next --status open --json
```

- Multi-project -> add `--project <name-or-root>`.
- Dirty diff review only when asked -> `--include-dirty`.
- Keep run cmd + report path.

3. Inspect:

```bash
clawpatch show --finding <id> --json
```

- Preserve exact finding ID in `tsq` notes, commits, reports.
- Check evidence paths/lines still exist or moved equivalent.
- Syntax-sensitive proof -> `ast-grep`.
- Missing old line != fixed.
- Classify: `open|fixed|false-positive|wont-fix|uncertain`.

4. Fix when valid + in scope:

- Smallest holistic fix at owning boundary.
- Deslopify -> delete/consolidate/reuse; no new wrapper/adaptor.
- Arch smell changes plan -> stop, explain, ask/propose.
- Automated fix? treat diff as untrusted:

```bash
clawpatch fix --finding <id> --dry-run --json
```

5. Revalidate:

```bash
clawpatch revalidate --finding <id> --reasoning-effort high --json
clawpatch revalidate --status open --limit 10 --reasoning-effort high --json
python skills/clawpatch/scripts/revalidate_findings.py --repo-root <repo> --throttle 8
```

For parallel ID-by-ID revalidation, use `scripts/revalidate_findings.py`. It reads `.clawpatch/findings/*.json`, defaults to `status=open`, writes JSONL to temp, and prints the exact `RESULT_FILE`. Add `--finding <id>` one or more times to skip discovery. Keep the JSONL path in notes/reports when triaging many IDs.

6. Triage only with evidence:

```bash
clawpatch triage --finding <id> --status fixed --note "<evidence>"
clawpatch triage --finding <id> --status false-positive --note "<evidence>"
clawpatch triage --finding <id> --status wont-fix --note "<rationale>"
clawpatch triage --finding <id> --status uncertain --note "<blocker>"
```

7. Before success claim: run relevant repo gates. Blocked gate -> quote blocker, weaker evidence.

## Output

Verification:

```text
<id>: <open|fixed|false-positive|wont-fix|uncertain>
Evidence: <files/cmds>
Revalidate: <cmd/outcome>
Next: <fix|triage|blocked>
```

Fix:

```text
Fixed: <ids>
Changed: <files>
Revalidated: <cmd/outcomes>
Tests: <cmd/outcomes>
Risks: <real only>
```
