---
name: dotnet-test-triage
description: Run dotnet test, capture failed test cases, and generate a rerun filter plus a markdown failure summary. Use when test runs fail and you need a focused rerun command or a compact failure report.
---

# dotnet-test-triage

Run `dotnet test`, collect failed test cases, and write a compact failure report plus a rerun filter.

## Outputs
- `artifacts/codex/test-failures.md`
- `artifacts/codex/test-filter.txt`

## Run
```bash
bash .codex/skills/dotnet-test-triage/scripts/run-test-triage.sh
```

Optional: pass arguments through to `dotnet test`:
```bash
bash .codex/skills/dotnet-test-triage/scripts/run-test-triage.sh ./src/Incursa.slnx --no-restore
```

Optional: override the default command (useful for repo-specific defaults):
```bash
DOTNET_TEST_CMD="dotnet test ./src/Incursa.slnx --no-restore" \
  bash .codex/skills/dotnet-test-triage/scripts/run-test-triage.sh
```

## Rerun recommendations
- Basic rerun of failures:
  - `dotnet test --filter "$(cat artifacts/codex/test-filter.txt)"`
- More output:
  - `dotnet test --filter "$(cat artifacts/codex/test-filter.txt)" -v normal`
  - `dotnet test --filter "$(cat artifacts/codex/test-filter.txt)" -v diag`
- Capture blame for crashes/hangs:
  - `dotnet test --filter "$(cat artifacts/codex/test-filter.txt)" --blame`
  - `dotnet test --filter "$(cat artifacts/codex/test-filter.txt)" --blame-hang --blame-hang-timeout 10m`
- Disable parallelization if needed:
  - `dotnet test --filter "$(cat artifacts/codex/test-filter.txt)" --no-parallel`

## Notes
- The filter file is empty when no failing tests are detected.
- The failure report contains the test name and a short error snippet from the TRX logs.
