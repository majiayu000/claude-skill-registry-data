---
name: restler-fuzzing
description: "Runs stateful REST API fuzzing using Microsoft's RESTler - infers producer-consumer dependencies from an OpenAPI spec, drives sequences of requests (POST → GET → DELETE chains), and reports 5xx errors, resource leaks, and hierarchy violations. Wraps the canonical 4-stage workflow (compile → test → fuzz-lean → fuzz). Use when the API is stateful (resources are created, queried, modified, deleted) and Schemathesis's stateless fuzzing is missing the multi-step bugs."
---

# restler-fuzzing

## Overview

RESTler is a stateful REST API fuzzer that finds security and reliability bugs
([restler-readme][readme]). Its differentiator vs. stateless fuzzers like
`schemathesis-fuzzing` is that it **infers producer-consumer dependencies** from
the OpenAPI spec - if `POST /resources` returns an `id` and `GET /resources/{id}`
accepts that `id`, RESTler sequences them in that order to reach deeper state.

[readme]: https://github.com/microsoft/restler-fuzzer

## When to use

- The API is **stateful**: resources are created, queried, modified,
  deleted, and bugs lurk in the dependency chains.
- A team is on Schemathesis already but suspects multi-step bugs
  aren't being reached. RESTler is the next layer down.
- A new service is launching and the team wants the broadest
  possible auto-coverage before releasing - particularly for cloud
  services.
- The API exposes a complete OpenAPI 2.0 / 3.x specification (RESTler
  consumes JSON or YAML).

If the API is **stateless** (search endpoints, calculator endpoints,
report-generation endpoints), Schemathesis is sufficient and lighter
to operate. RESTler shines on resource lifecycle APIs.

## Install

Prerequisites per [restler-readme][readme]: **Python 3.12.8** and
**.NET 8.0**.

### From source

```bash
git clone https://github.com/microsoft/restler-fuzzer.git
cd restler-fuzzer
mkdir restler_bin
python ./build-restler.py --dest_dir "$(pwd)/restler_bin"
```

(Per [restler-readme][readme].)

### Via Docker (preferred for CI)

```bash
docker build -t restler .
```

For one-off CI runs:

```bash
docker run --rm -v "$PWD/output:/output" restler ...
```

## The four-stage workflow

Per [restler-readme][readme]:

### Stage 1 - Compile

Generate a RESTler **grammar** from the OpenAPI spec. The grammar
captures the producer-consumer dependencies RESTler will exploit
during fuzzing.

```bash
restler compile --api_spec openapi.json
```

Output: `Compile/grammar.py` plus `Compile/dict.json` (a starter
dictionary RESTler uses to seed parameter values).

### Stage 2 - Test (smoke)

Run a single end-to-end pass to verify the spec, auth, and target
URL are wired correctly. Measures **endpoint coverage** - what
fraction of the API RESTler can reach with the current grammar /
dictionary.

```bash
restler test --grammar_file Compile/grammar.py \
             --dictionary_file Compile/dict.json \
             --target_ip <api-host> \
             --target_port 443 \
             --use_ssl
```

If endpoint coverage is below the team's threshold (often 80%+),
stop and amend the dictionary or grammar before continuing.

### Stage 3 - Fuzz-lean

One pass through every endpoint with default **checkers** active - 
fast bug discovery focused on the obvious failure modes.

```bash
restler fuzz-lean --grammar_file Compile/grammar.py \
                  --dictionary_file Compile/dict.json \
                  --target_ip <api-host> \
                  --target_port 443 \
                  --use_ssl
```

### Stage 4 - Fuzz (deep)

Aggressive breadth-first exploration. Run for a fixed time budget
(hours to days for a comprehensive run).

```bash
restler fuzz --grammar_file Compile/grammar.py \
             --dictionary_file Compile/dict.json \
             --target_ip <api-host> \
             --target_port 443 \
             --use_ssl \
             --time_budget 8.0   # hours
```

## Bug detection

Per [restler-readme][readme], RESTler reports two bug categories:

| Category | Trigger |
|----------|---------|
| **5xx errors** | Any 5xx response is a bug; RESTler triages by URL pattern. |
| **Checker violations** | Targeted sequences look for resource leaks, hierarchy violations (e.g. accessing a resource after deletion), and use-after-free patterns. |

Each bug appears in `RestlerResults/.../bug_buckets/` with a **replay
log** - the exact sequence of requests that triggered it. Replay
logs are deterministic - the bug reproduces on demand.

## Authentication

RESTler doesn't bake in an auth strategy; for tokens, the canonical
pattern is:

1. Obtain the token with a short pre-script.
2. Pass it via the dictionary's `restler_custom_payload_header` for
   the `Authorization` slot.

```bash
TOKEN=$(curl -s ... | jq -r .access_token)
echo "{\"restler_custom_payload_header\": {\"Authorization\": [\"Bearer $TOKEN\"]}}" > auth-dict.json

restler fuzz-lean ... --dictionary_file auth-dict.json
```

For OAuth flows that rotate tokens during a long fuzz run, supply a
**refresh script** RESTler invokes periodically. See [restler-readme][readme]
for the `--token_refresh_command` flag and cadence settings.

## Output and triage

Results land under `RestlerResults/` with `Compile/`, `Test/`, `FuzzLean/`, and
`Fuzz/` subtrees; each unique bug gets a `bug_buckets/Bug_N/` folder holding a
`bug_replay_log.txt` and `bug_request.txt`. The full directory layout is in
[references/triage-and-ci.md](references/triage-and-ci.md).

Per-bug triage:

1. Read `bug_replay_log.txt` - the deterministic sequence.
2. Confirm the bug locally with `restler replay --replay_log <path>`.
3. File a ticket with the replay log attached; the replay log can be
   converted into a project-specific failing regression test.

## CI integration

RESTler is **not** a per-PR tool by default - fuzz-lean takes 5-30
minutes typically; deep fuzz is hours. The canonical cadence:

| Cadence       | Stage     | Time budget         | Trigger                              |
|---------------|-----------|---------------------|--------------------------------------|
| Per-PR        | Test only | <1 minute           | Schema-validation smoke; fail fast.  |
| Nightly       | Fuzz-lean | 30-60 minutes       | New endpoint regression scan.        |
| Weekly        | Fuzz      | 4-12 hours          | Deep state-machine exploration.      |
| Pre-release   | Fuzz      | 24-72 hours         | Final security / reliability gate.   |

The nightly cadence runs on a `schedule: cron` trigger: build the RESTler
Docker image, `compile` the grammar from `openapi.json`, run `fuzz-lean` against
staging, upload `RestlerResults/` as an artifact (`if: always()`), then fail the
job when any `bug_replay_log.txt` exists (`find ... | wc -l`). The complete
GitHub Actions workflow is in
[references/triage-and-ci.md](references/triage-and-ci.md).

## Anti-patterns

| Anti-pattern                                                    | Why it fails                                                | Fix |
|-----------------------------------------------------------------|-------------------------------------------------------------|-----|
| Running RESTler on production                                    | Generated requests mutate live data; 5xx alerts spam oncall.| Always target staging; production is for runtime monitoring, not fuzz traffic. |
| Skipping Stage 2 (Test)                                          | Spec-vs-impl drift is invisible until Stage 4 wastes hours. | Always run Test first; check coverage before fuzz-lean. |
| Stage 4 (Fuzz) on every PR                                       | Hours-long PR CI; no team accepts that.                     | Fuzz is nightly / weekly only. |
| Triaging bugs without replay-log confirmation                    | Some bugs are environmental (test DB state); confirm reproducibility. | Always run `restler replay` on each bug before opening a ticket. |
| Letting bug counts grow unbounded                                | Backlog of unfixed bugs becomes noise; team learns to ignore RESTler reports. | Treat each bug as a P1 / P2 ticket; fix or document waiver per the team's escape-defect policy. |

## Limitations

- **OpenAPI-driven only.** No GraphQL support; for GraphQL fuzzing,
  use `schemathesis-fuzzing`.
- **Heavy infra.** Python 3.12 + .NET 8 prereqs are non-trivial;
  Docker is the practical install path.
- **Run-time cost.** Deep fuzz is hours-to-days; budget accordingly.
  Fuzz-lean is the cost-effective sweet spot for nightly runs.
- **No native parallelism.** RESTler runs single-threaded; for
  parallelism, shard at the endpoint level via multiple invocations
  with different grammar subsets.
- **State across runs.** Each fuzz run is independent - there's no
  built-in mechanism to remember "we've explored these states
  already." Use the `progress/` directory for manual checkpointing.

## References

- [restler-readme][readme] - main repo: install, 4-stage workflow,
  bug categories, authentication patterns.
- `schemathesis-fuzzing` - 
  stateless complement; lower setup cost; cover happy / boundary on
  PRs.
