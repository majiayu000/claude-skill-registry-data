---
name: orchestrator-preamble
description: "The ≤60-line imperative rules block that every GERMO job's base prompt loads. Generated from the canonical engineering skills by scripts/gen-preamble.mjs; do not hand-edit the body — regenerate it."
license: MIT-compat
compatibility: "framework-agnostic; text; any host"
metadata: {}
allowed-tools: []
---

# Orchestrator Preamble

Every GERMO job that owns a product repo starts from the rules below. They are the
contract between the orchestrator and the job, and they are **generated** — the canonical
source is `references/preamble.md`, produced by `scripts/gen-preamble.mjs` from the four
canonical engineering skills. Hand-editing the body breaks reproducibility; change a rule
by changing the canonical skill and re-running the generator.

## The four rules (generated)

1. **company_id / RLS** — every tenant table carries `company_id` (or the repo's tenant
   discriminator), `FORCE ROW LEVEL SECURITY` is set, a `USING`/`WITH CHECK` policy exists,
   and the grant is scoped. Check:
   `python3 scripts/check_rls_migration.py <migration.sql>` — exit 0 means the migration
   is RLS-clean; any finding is a merge blocker.
2. **outbox** — any write that outlives the request goes through an outbox table with a
   UNIQUE `idempotency_key`, the business write and the outbox INSERT are in ONE
   transaction, the poller uses `ORDER BY created_at ... FOR UPDATE SKIP LOCKED`, and
   poison messages are moved to `poison_outbox` (never deleted). Check:
   `python3 scripts/check_outbox.py <outbox-sql-file> [--poller <poller-source-file>]` —
   exit 0 means all invariants hold.
3. **problem+json** — every HTTP >=400 response is RFC 9457 `application/problem+json`
   with an absolute `type` URI, a `status` equal to the HTTP code, a catalogue code that
   matches the JSON Schema `enum` exactly, and `retry_after` as integer seconds for
   retriable errors. Check:
   `python3 scripts/check_problem_catalogue.py --catalogue <cat> --openapi <spec> --schema-dir <dir>` —
   exit 0 means the catalogue, the OpenAPI spec and the schemas agree.
4. **honest status** — "done" means a command ran, you saw its exit code, and the log path
   is recorded. A claim without a runnable evidence pointer is FALSE_DONE, never DONE.
   Check: `python3 scripts/check_status_evidence.py STATUS.md --root .` — exit 0 means
   every DONE/VERIFIED entry names a command + exit code + log path.

## Reproducibility

`node scripts/gen-preamble.mjs` reads the four canonical skills' rules sections and emits
`references/preamble.md`. The same skill set always produces the same file (the generator
is deterministic and takes no input beyond the skills on disk). Verify:
`node scripts/gen-preamble.mjs --check` — exit 0 means the committed preamble matches a
fresh generation.

## Contracts

The body ends with a fixed `## Contracts` section that documents the interface contract
(generator, body, canonical-source and consumer). It is generated text, not prose: it is
part of the byte-identical output and is covered by the same `--check` gate. The section
names the four contracts, states the exit codes (0 = pass, 1 = stale/missing) and points
consumers at this `SKILL.md` as the human-readable contract. Edit the contract by editing
the generator's `CONTRACTS` constant, never the emitted file.

## Related

- Canonical skills: `skills/engineering/pg-rls-multitenant/`,
  `skills/engineering/outbox-idempotency/`, `skills/engineering/problem-json-contracts/`,
  `skills/engineering/honest-status/`.
- Generated body: `references/preamble.md`.
