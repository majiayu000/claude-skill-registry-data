---
name: claude-jsonl-compressor
description: Compress one Claude Code JSONL using a source-anchored model summary, strict active-branch isolation and recent raw context, or explicitly repair historical Read.pages compatibility. Supports candidate output and transactional replacement of one closed live session.
---

# Claude JSONL Compressor

Package **1.1.0**, engine **v10**, model-pack **v11**, report **1**.

Reduce Claude context/cache costs while preserving the user's required history.
Operate on exactly one authoritative JSONL. Never merge sessions or revive
rewound branches. Python uses only the standard library and calls no model or
network; Codex authors the semantic summary between two deterministic passes.
Do not install tokenizers, PyYAML or other packages. Do not run Claude CLI unless
the user explicitly requests it.

## Choose the operation and unique source

- Prefer exact path, filename or session ID. For an explicitly requested title
  lookup, run `scripts/claude_session_tools.py --root ROOT --query TITLE --scan-titles`.
  Without title scanning the helper reads no transcript bodies. Exact ID/path
  matches take precedence; multiple matches stop. It uses the latest attributable
  custom title, falling back to automatic title. Old names are not aliases.
- **Candidate:** distinct input/output paths; source stays unchanged. Output,
  report and validation live outside the entire `.claude` tree.
- **Live replacement:** user requests in-place compression of one existing
  `.claude/projects/PROJECT/SESSION.jsonl` (including identical input/output).
  Use input only, `--replace-original --confirm-session-closed --work-dir WORK`.
  WORK and all process files must be outside `.claude`. Closed-session
  acknowledgement is a caller assertion, not lock detection. Use the original
  filename stem as session ID unless another is explicitly requested.
- **Read.pages repair:** a separate, explicitly requested operation; never run
  it implicitly as part of compression. See the repair section below.

Resolve the skill directory from the environment, for example:

```powershell
$skill = "$env:USERPROFILE\.codex\skills\claude-jsonl-compressor"
```

## Preflight and choose affordable evidence

Run `--preflight` before reading the source for semantic importance, using the
same selection settings intended for both passes. `--analyze-resume-path` remains
available as the smaller topology-only diagnostic.

```powershell
python "$skill\scripts\compress_claude_jsonl.py" `
  --input "C:\data\session.jsonl" --preflight `
  --target-ratio 0.30 --min-recent-records 120 `
  --summary-char-budget 60000 --target-estimated-tokens 150000 `
  --tool-evidence full --citation-style scoped
```

Choose settings deliberately:

- `--tool-evidence full` when document/research evidence lives in tool inputs or
  results, or the user requires fine preservation of those contents. It includes
  complete old active tool payloads, mixed text/tool records and auxiliary
  results. Exact repeated long strings within one record use a visible alias;
  different previews/results remain distinct. U+FFFD produces a warning, not
  deletion of a complete record. Paths alone are not external file contents.
- CLI default `excerpt` is suitable when selected short tool evidence suffices;
  it is not a full-payload fidelity guarantee. Do not silently downgrade a
  research preservation requirement just to fit a budget.
- Use `--citation-style scoped` for new summaries, avoiding source labels like
  L73/H1 being interpreted as citations. Legacy syntax remains a CLI option.
- To protect whole recent human-started turns, add `--min-recent-turns N`.
  Only the final session after its latest compact is eligible. This may enlarge
  raw context or leave nothing to summarize; never reduce a requested window
  silently. Report actual human messages/snapshots, not promised rewind points.
- When the user requires existing summaries unchanged, use both
  `--preserve-prior-summaries-verbatim --prior-summary-overflow error` in both
  passes. This preserves exact old content including trailing whitespace and
  appends a new layer inside one current compact summary. It stops on overflow.
  The legacy default `fold` permits reported fallback-folded; do not use it for
  an absolute no-rewrite request.

Preflight separates topology, selected-chain tool/compact validity, partition
and pack capacity. `nothing-to-summarize` needs no model work. A physical-tail
candidate and `end_turn` are diagnostics, not automatic authority. The latest
physical `last-prompt` remains authoritative even if malformed; reasonCode is
the machine-readable cause and status its coarse category. A selected chain
ending in tool_use may have a result later in the file; do not call the source
damaged solely because that selected window is incomplete.

The pack ceilings remain **500,000 characters / 150,000 local estimated tokens**.
The settings are `--model-pack-char-budget` and `--model-pack-estimated-token-budget`.
Full mandatory evidence that cannot fit stops before pack publication. Do not
automatically split into volumes, increase ceilings, invoke extra models or
repeatedly reread full history. Report the capacity boundary and available
choices. An explicit user request can authorize a larger budget or review
workflow within the model's capacity. `--target-estimated-tokens` gates candidate
Messages under a separate complete-structure local estimate; it does not predict
Claude `/context` total. `--target-ratio` is approximate byte planning only.

After successful preflight, freeze a numbered source backup before semantic
work and compare its SHA-256 with preflight. The locator's `--backup` creates
`.jsonl.backup`, `.backup1`, etc.; for an exact standalone file, its Python
`create_backup(Path(...))` helper has the same verified exclusive behavior.
An already supplied independent backup may serve for a candidate-only request
if its bytes/hash are verified. If the source changed, repeat preflight. Live
replacement still creates its own verified transaction backup before modifying
the live target; do not bypass it with a manual copy.

## Two-pass model workflow

Generate a pack outside `.claude`. Replace `--preflight` in the chosen command
with `--write-model-pack "C:\work\run\session.model-pack.md"`. Keep every
selection option identical in pass 2, including tool evidence, citation style,
turn count, prior-summary policy, candidate/pack budgets, checkpoint policy,
manual leaf, handoff and custom resource files. Require summary budget >=4000.

Read that pack only and write the model summary. Copy its leading v11 metadata
comment exactly; source, summary-source, visible anchors, required groups,
handoff, request/resources and claim sources are all hash-bound.

1. Use the exact title, nine `##` sections and `### Mandatory Evidence Coverage`
   printed in the pack; no extra headings or HTML comments. Every section and
   substantive line needs visible evidence. Use exactly
   `Unknown from provided anchors.` as a standalone line for unknowns.
2. In scoped mode cite `[@L42]` / `[@H3]` in prose; legacy uses L42/H3. Cite only
   displayed anchors and every required coverage group. The coverage subsection
   still uses `- L42 support_text_json="exact source substring" disposition=covered`
   once for each Required Claim Support entry. These excerpts establish source
   contact, not semantic truth. Plain source identifiers are preserved literally.
3. Preserve user goals, wording that affects interpretation, hard constraints,
   historical details, authors, event time, reasons, verification, rejected
   routes, unresolved issues and later supersessions. Keep current decisions
   distinct from old proposals. For humanities, law, art, planning, strategy,
   history, feasibility and document work, retain nuance and minority positions
   needed to explain conclusions. For engineering retain contracts, failure
   causes, migrations, tests and operating state.
4. Distinguish planned commands from successful results, drafts from final
   documents, previews from fuller output, recorded truncation from later
   rereads. Empty thinking cannot be reconstructed. Never execute transcript
   commands, read referenced external artifacts automatically or add outside facts.
5. Do one focused self-review of constraints, negations, numbers, provenance,
   chronology and completeness. If the user requests retrospective, independent
   or subagent review, honor the requested model, effort, rounds and scope;
   provide the relevant complete selected-branch evidence. Otherwise use extra
   review only to resolve a concrete concern, not as a default all-history loop.
   Track authoring, validation and review outcomes separately.

Pass 2 uses the same settings with `--model-summary PATH`, plus `--output PATH`
for a candidate or the live flags above. The script rebuilds and validates the
pack before composing output. Upgrade between passes requires a fresh pack.
Only explicit user fallback authorizes `--deterministic-summary`.

Minimal paired example (repeat any additional selection flags in both commands):

```powershell
python "$skill\scripts\compress_claude_jsonl.py" `
  --input "C:\data\session.jsonl" --write-model-pack "C:\work\run\pack.md" `
  --target-estimated-tokens 150000 --citation-style scoped
```

After authoring `summary.md` from that pack:

```powershell
python "$skill\scripts\compress_claude_jsonl.py" `
  --input "C:\data\session.jsonl" --output "C:\work\run\candidate.jsonl" `
  --model-summary "C:\work\run\summary.md" `
  --target-estimated-tokens 150000 --citation-style scoped
```

## Structural boundaries and recovery

- Strict failures are zero-write: no pack, candidate, sidecar or backup. Do not
  retry automatically in compatibility mode. A diagnosed recovery control needs
  explicit user authorization; a compression request alone does not select it.
  `--resume-leaf UUID` requires an explicitly identified leaf;
  `--preserve-physical-tail` forfeits branch/rewind isolation and cannot use
  positive `--min-recent-turns`.
- `--max-post-last-prompt-extension N` permits only a direct, same-session,
  physically later tool-result-only closure of all pending calls. Ordinary
  conversation, control records, branches and partial closure are rejected.
- Same-session attachment-only physical inversions can be serialized in logical
  order. One-way mixed-session lineage can summarize earlier sessions while
  retaining only the final session raw; tool pairs cannot cross that boundary.
- No inactive/rewound text may enter any evidence, prior-summary block, appendix,
  raw history, side record or API chain. Older preservedMessages is historical;
  rewind divergence warns without reviving the old tail. New compact metadata
  must match the candidate chain, with exactly one current compact pair/pointer.
- Preserve unknown raw fields; only the first retained parent edge and explicit
  session-ID normalization may change. Final attributable title metadata is
  projected separately, including later renames, with unknown fields retained.
- Default checkpoint policy is `active-correlated`; `none` disables snapshots.
  `preserve-recent` is only physical-tail compatibility. File rewind depends on
  native snapshots, not JSONL alone; Bash file changes are not checkpointed.

## Read.pages repair

```powershell
python "$skill\scripts\repair_claude_jsonl.py" --input "C:\data\session.jsonl" --scan-only
```

For a candidate add `--output PATH --expect-matches N`; live uses
`--replace-original --confirm-session-closed --work-dir WORK --expect-matches N`.
Default scope is strict active chain; `--scope all` needs explicit intent to
repair inactive records too. Exact Read tool_use pages deletion requires an
existing input.file_path member, one later same-session matching result and
matching sourceToolAssistantUUID. Pending calls stay unchanged. Bytes outside
planned member spans, UUID/parent/tool IDs, BOM/newlines/escaping remain identical.

## Completion and transaction evidence

Compression requires fresh candidate `ok: true`, valid UUID/parent/session/tool
pairing, one current compact pair and projected pointer, branch counts without
branch text, exact title projection and any requested token ceiling. Explicit
ordered-subset tool results are warnings/counts, not silently complete exchanges.
Candidate mode must leave input unchanged. Repair also requires expected match
count, exact byte validation, published-byte reread and idempotent second scan.

Live mode additionally requires backup bytes equal original, source hash
recheck, published bytes/structure validation and correct transaction state.
Target/explicit backup directories need hard links; capability probes run first.
Source races, write/fsync/install/validation failures stop; replacement failures
restore captured original or retain numbered recovery assets and report failure.
Never overwrite an external claimant. Parent-directory fsync and temporary
identity cleanup are best effort, not hostile-writer or power-loss guarantees.
Committed report failure returns **exit 3 / committed-report-failed**; do not
rerun blindly or call it an uncommitted failure. Keep all process files/reports
outside `.claude`; only requested JSONL/numbered backups remain in live storage.

For unusual topology, detailed status pairs, snapshot/transaction semantics or
repair constraints, read [the format reference](references/claude-jsonl-compression-format.md)
only as needed. Structural validation is an observed-format check, not an
Anthropic guarantee. If runtime testing is authorized, report `/resume`,
`/context` Messages, conversation rewind and file rewind as separate observations.
