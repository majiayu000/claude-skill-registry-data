---
name: create-hld
description: >
    Invoke to author a High-Level Design (HLD) at discovery / prototyping phase.
    Design-only: delivers intent + spec for AI and humans to build against — no
    implementation plan, no code outside examples/. Trigger keywords: "HLD",
    "high level design", "design doc", "architecture design", "create a design".
    Also triggers on /create-hld.
allowed-tools: >
    Bash(.agents/skills/create-hld/scripts/scaffold-hld.sh:*),
    Bash(.agents/skills/create-hld/scripts/hld-agents-rules.sh:*),
    Read, Write, Edit
models:
  claude: opus        # high-complexity; multi-step clarification gates + architectural judgment
  copilot: auto
  codex: gpt-5.5
---

# Create HLD — High-Level Design authoring

## TL;DR

Produce a `docs/hlds/NNN-<slug>/` folder that captures **intent + spec** for a design at
discovery/prototyping phase. The HLD says *what* we are building, *why*, the decisions behind
it (LADRs), the quality bar it must meet (NFRs), and its architecture (diagrams). It does
**not** say *how to build it* — no implementation plan, no phasing, no code (except an optional
`examples/` folder). This skill is the source of truth for HLD structure in this repo.

## Non-Negotiables

- **Design only.** No implementation plan, no execution phasing/sequencing, no sub-issue
  breakdown — that lives in the issue/work tracker. The HLD is for discovery/prototyping.
- **No code** anywhere except `examples/`. README, LADRs, NFRs, and AGENTS.md are code-free.
- **AGENTS.md has no architecture section.** Architecture lives in `diagrams/`. The HLD
  AGENTS.md follows `scripts/hld-agents-rules.sh`, which deliberately omits System Context.
- **C1 is the floor, not the ceiling.** Always produce a C4Context. Investigate the design and
  *recommend* further diagrams (`references/diagram-selection.md`); do not pad by default.
- **Clarify before inventing.** Initiative name, goals, constraints, stakeholders, target
  system — ask, do not assume (Phase 1 of the AI workflow rules).
- **Every NFR is measurable + verifiable.** Vague NFRs ("fast", "reliable") are forbidden.
- **Every LADR and NFR is one file** — a horizontal concern spanning the vertical HLD.

## Invocation

`/create-hld <kebab-slug>` — or describe the design in natural language and follow the workflow.

## Output structure (the contract)

```
docs/hlds/NNN-<kebab-slug>/
├── README.md            # human entry point: intent + spec (no impl, no code)
├── AGENTS.md            # AI-coder guardrails — NO architecture/System-Context section
├── diagrams/
│   └── c4-context.md    # C1 System Context (mandatory) + AI-recommended diagrams
├── ladrs/
│   └── LADR-NN-<slug>.md   # one decision per file
├── nfrs/
│   └── NFR-NN-<attribute>.md  # one quality attribute per file
└── examples/            # OPTIONAL — the only place code may appear
```

- `NNN` is 3-digit, zero-padded, next-available — the scaffold script computes it.
- `AGENTS.md` is plain-named (root of the HLD folder); the `load-agents-context` hook still
  auto-loads it. It is guardrails, not narrative.
- File shapes are defined by the templates in `assets/`; the scaffold script seeds them.

## Workflow

1. **Clarify scope** — initiative name, the problem and target outcome, key goals, hard
   constraints, stakeholders, the target system and its external dependencies. Do not invent.
2. **Scaffold** — run:
   ```bash
   .agents/skills/create-hld/scripts/scaffold-hld.sh <slug> [--title "Title"] [--examples]
   ```
   It prints JSON of the created paths. Add `--examples` only if code samples will help.
3. **Draft README.md** — Intent, Key Goals (each with **acceptance criteria / DoD**), Core
   Separation of Concerns (blockquoted thesis), Guiding Principle. Get the thesis and goals
   signed off before writing decisions. No rollout/phasing section, no risks section.
4. **Draft strategic LADRs** (`ladrs/LADR-01..N`) — one architectural decision each, derived
   from the goals. Default status **Draft** (discovery). One file per decision.
5. **Investigate and recommend diagrams** — C1 is mandatory. Using
   `references/diagram-selection.md`, decide whether container / flow / sequence / ER / class
   diagrams add understanding. **Surface the recommendation to the user with a one-line
   rationale per diagram before writing them.** Then write into `diagrams/`.
6. **Draft NFRs** (`nfrs/NFR-01..M`) — one quality attribute per file: measurable Requirement,
   Verification mechanism, Acceptance Criteria, Applies-To. Reference them from the README NFR table.
7. **Draft tactical LADRs** if any *how* decisions surfaced (runtime, protocol, config). Number
   after the strategic ones; never renumber.
8. **Draft AGENTS.md** — apply `scripts/hld-agents-rules.sh`. Derive Non-Negotiables from the
   LADRs, fill the decisions and NFR pointer tables. No architecture section.
9. **Wire the tables** — README LADR table and NFR table list every file with status.

To read the AGENTS.md rules at any point (agent-agnostic, no hook needed):
```bash
.agents/skills/create-hld/scripts/hld-agents-rules.sh
```

## Quality bar before marking ready

- [ ] Every Key Goal has acceptance criteria / DoD.
- [ ] Every LADR has Context, Decision, Consequences (Alternatives recommended).
- [ ] Every NFR has a measurable target AND a verification mechanism AND acceptance criteria.
- [ ] C1 diagram present; every extra diagram is justified and one-concern.
- [ ] AGENTS.md has no architecture section, no code, no impl/phasing.
- [ ] No code outside `examples/`.
- [ ] Mermaid renders (no syntax errors).
- [ ] All cross-links are relative and resolve. No `[TODO]`; use `TBD` with owner/trigger.

## Agent-agnostic notes

- Scripts are `bash` + coreutils only; no Claude-specific behaviour.
- The AGENTS.md quality rules ship inside the skill (`scripts/hld-agents-rules.sh` + the
  summary above), so Codex / Copilot / Cursor — which do not run Claude Code hooks — are fully
  self-contained. The repo's global `knowledge-rule-enforce.sh` hook is unaffected and still
  governs general (non-HLD) AGENTS.md files.

## References

- `references/status-vocabulary.md` — Draft / Prototype / Accepted lifecycle; strategic vs tactical.
- `references/diagram-selection.md` — when to add each diagram type beyond C1.

## Changelog

| Date | Change | Ref |
| :---- | :---- | :---- |
| 2026-07-23 | Corrected the HLD scaffold contract to the visible `docs/hlds/` tree. | #253 |
| 2026-06-16 | Created — design-only HLD skill, made project-agnostic for the smooth-devex template. | — |
