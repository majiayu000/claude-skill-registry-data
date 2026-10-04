---
name: operator-module-final-test
description: >
  Conductor for Operator Module Final Test (OMFT): module-agnostic PREP (module
  pack + run brief) → human live run with photos/POV → INTAKE into USER-NAV-REPORT
  with stable NAV-IDs → IMPLEMENT only approved IDs via live-fix/ship. Use when
  the user says OMFT, "module final test", "operator final test", "corrida final
  de módulo", "prepará el pack de prueba", or wants a reusable live E2E review
  loop that correctly wires their observations into implementation for any module
  (logistica, envios, techo, hub, WA, custom — not only one surface).
---

# Operator Module Final Test (OMFT)

You are the **conductor** of a module-agnostic final-test ritual. The **human is the operator** (real work, real data). You prepare context, receive their report, and wire findings into implementation **only by stable IDs**.

```text
PREP  →  YOU RUN  →  INTAKE  →  IMPLEMENT
(agent)   (human)    (agent)    (agent, after approve)
```

**Do not** invent UI, bugs, or requirements. **Do not** implement code in PREP or INTAKE unless the user explicitly approves NAV-IDs for IMPLEMENT.

## Triggers

| Phrase | Phase |
|--------|--------|
| `OMFT prep: <module>` / `prepará el pack de prueba de <module>` | PREP |
| `OMFT intake` / `procesá mi corrida OMFT` + notes/photos | INTAKE |
| `OMFT implement NAV-…` / `implementá los P0 del informe OMFT` | IMPLEMENT |
| `OMFT` alone / `module final test` / `corrida final de módulo` | Ask which phase; default explain + offer PREP |

## Paths (Calculadora-BMC repo root)

| Artifact | Path |
|----------|------|
| Module pack template | `docs/team/ux-feedback/TEMPLATE-MODULE-PACK.md` |
| Run brief template | `docs/team/ux-feedback/TEMPLATE-OMFT-RUN-BRIEF.md` |
| Module packs | `docs/team/ux-feedback/module-packs/<slug>.md` |
| Run briefs | `docs/team/ux-feedback/runs/OMFT-PREP-YYYY-MM-DD-<slug>.md` |
| Intake report | `docs/team/ux-feedback/USER-NAV-REPORT-YYYY-MM-DD-<slug>-omft.md` |
| Nav report template | `docs/team/ux-feedback/TEMPLATE-USER-NAV-REPORT.md` |
| Folder index | `docs/team/ux-feedback/README.md` |

Default base URL: `https://calculadora-bmc.vercel.app` unless the user specifies preview/local.

## Downstream skills (reuse, do not rewrite)

| Need | Skill / command |
|------|-----------------|
| Structured backlog from notes + photos | `navigation-user-feedback` |
| Long transcript + MCP plan | `live-devtools-transcript-action-plan` |
| Agent browser corroboration | `live-devtools-narrative-mcp` |
| Video session | `user-session-video-to-backlog` / Video-User-interactive-dev |
| Single prod bug fix | `live-fix` |
| Routine ship | `ship` |
| Messy voice STT | `dictado` |
| Refine chaotic input | `contribut` |

---

## Phase A — PREP

**Goal:** Give the operator a module map so their run and later intake map cleanly.

1. Parse **module slug** (kebab-case): e.g. `logistica`, `envios`, `techo`, `hub-cotizaciones`, `wa-cockpit`, `calculadora-core`, or `custom`.
2. If `docs/team/ux-feedback/module-packs/<slug>.md` exists → **load and refresh** tip SHA / recent context only if cheap (git log, PROJECT-STATE). Do not invent new screens.
3. If missing → create from `TEMPLATE-MODULE-PACK.md` using:
   - User-stated URL/goal
   - Grep/routes in repo when in Calculadora
   - Linked SDD paths if known
   - Empty placeholders marked `NEEDS_OPERATOR` for success criteria they must edit
4. Write **Run Brief** from `TEMPLATE-OMFT-RUN-BRIEF.md` to  
   `docs/team/ux-feedback/runs/OMFT-PREP-YYYY-MM-DD-<slug>.md`
5. Reply to the user with:
   - Link/path to pack + brief
   - Capture protocol reminder (ACTION / EXPECT / OBSERVED / Fig / severity)
   - **Stop.** Explicit: “Corré en vivo; cuando vuelvas, `OMFT intake` + notas/fotos.”

**PREP anti-patterns:** no findings table, no “I already found bugs”, no code edits, no auto-implement.

### Capture protocol (include in every brief)

Per meaningful step:

| Field | Meaning |
|-------|---------|
| Step # | Order |
| ACTION | What you did |
| EXPECT | Your POV of correct behavior |
| OBSERVED | What happened |
| Verdict | OK \| FAIL \| CONFUSING \| BLOCKED |
| Fig | Photo id (optional) |
| Severity | P0 \| P1 \| P2 if FAIL |

---

## Phase B — YOU RUN (human)

Agent does **nothing** until intake, unless the user asks a clarifying question mid-run.

Valid evidence: screenshots, bullets, voice transcript (`dictado`), screen video (Video-User-interactive-dev).

---

## Phase C — INTAKE

**Goal:** Wire the operator pack into a implementable report with stable IDs.

1. Require (or ask once for): notes and/or photos; optional prep path / slug.
2. Load module pack + prep brief if paths given.
3. Follow **`navigation-user-feedback`** rules:
   - Output `USER-NAV-REPORT-YYYY-MM-DD-<slug>-omft.md`
   - Structure = `TEMPLATE-USER-NAV-REPORT.md`
   - IDs: `NAV-YYYY-MM-DD-01`, …
   - Max **5 P0**
   - No inventing UI; `NEEDS_CONFIRMATION` when evidence missing
4. Prefer mapping each FAIL/CONFUSING step to one NAV row with:
   - repro minimum
   - actual vs expected
   - testable acceptance criteria
   - propagation table
5. Optional: MCP only on FAIL/CONFUSING steps (do not re-audit whole module by default).
6. Present prioritized backlog. **Wait for approval** of which NAV-IDs to implement.

**Hard rule for later sessions:** when OMFT context is active, code changes may only claim **approved NAV-…** (or U-… if only transcript beats exist) from the report. No free-form “while I was there I also fixed…”.

---

## Phase D — IMPLEMENT

Only after explicit approval (e.g. “implementá NAV-01 y NAV-03”).

| Approved set | Route |
|--------------|--------|
| One clear prod bug with repro | `live-fix` |
| Several PR-sized items | one PR per cluster; `ship` / github-solver |
| Research only | short investigation note; no product code |

Verify each acceptance criterion on the same base URL as PREP. Link commits/PRs back to NAV-IDs in PR body.

---

## Module slug registry (seed)

| Slug | Typical surfaces |
|------|------------------|
| `logistica` | `/logistica` — 3D truck, adjunto, packing |
| `envios` | envíos / reparto / wizard / workspace |
| `techo` | irregular roof, dual plant, limpia |
| `hub-cotizaciones` | `/hub/cotizaciones` pipeline |
| `wa-cockpit` | WhatsApp operator |
| `calculadora-core` | quote calculator steps |
| `custom` | operator supplies URL + goal in PREP |

Add new packs under `module-packs/` as OMFT runs accumulate.

---

## Anti-patterns

- Treating OMFT as agent-only browser audit (that is `mcp-production-browser-audit`).
- Skipping PREP and then guessing which module/success criteria applied.
- Implementing without NAV-IDs or without user approve.
- Mixing prod and local findings without labeling environment.
- Putting secrets, passwords, or full private order payloads into committed reports (redact).

## Success (skill quality)

- `OMFT prep: <slug>` → pack + brief, stop for human run.
- `OMFT intake` → USER-NAV-REPORT with stable IDs and backlog.
- Same ritual for any slug without forking the skill.
