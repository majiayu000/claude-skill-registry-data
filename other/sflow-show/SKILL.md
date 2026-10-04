---
name: sflow-show
description: Expand one registered Singularity Flow reference handle deterministically, with optional section, pointer, or range selection.
disable-model-invocation: true
argument-hint: "<sfref:v1:...> [--section HEADING | --json-pointer POINTER | --range RANGE] [--max-bytes N]"
---
# Show a governed reference

<!-- sflow-output-contract: concise-relay -->
**Output contract:** Relay requested CLI fields or output faithfully; preserve warnings/errors and only the explanations required below.
<!-- sflow-execution-boundary -->
**Boundary:** `singularity-flow session current --json` → `ready`/`workId`, cwd=`repositoryPath`; use CLI/`workItemRoot` paths; never `$HOME`.

Run `singularity-flow show <HANDLE>` with only the selection options explicitly requested by the user:

- `--section "<exact Markdown heading>"`
- `--json-pointer "<RFC 6901 pointer>"`
- `--range "lines:<start>..<end>"` or `--range "bytes:<start>..<end>"`
- `--max-bytes <N>` up to 65536

Only `sfref:v1:` handles registered in committed Story or Initiative context are accepted. A failed hash, stale revision, ambiguous section, human-only visibility, or unknown handle is a hard stop. Never fall back to arbitrary filesystem reads.
