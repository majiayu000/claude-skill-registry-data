---
name: write-workflow
version: "1.2.1"
user-invocable: true
description: "Eight-stage document-writing host: clarify → analyze sources → explore → review → outline → execute writer → verify → retrospect. In-repo writer: tech-review-doc. External strong deps: humanizer, humanizer-zh. Auto mode never skips tech-review §1. Triggers — 「写文档」「写技术评审」「去AI痕迹」「人性化改写」「自动写文档」「write workflow」「humanize」. Do NOT use for code PDCA (solve-workflow), performance (perf-optimize-workflow), or marketing articles (article-writer)."
dependencies:
  - clarifying-question-discipline
  - tech-review-doc
  - workflow-mode-lifecycle
  - humanizer
  - humanizer-zh
---

# Write Workflow

> Eight-stage **document-writing** host. Writer skills own methodology; this host owns routing, source analysis, mode lifecycle, path depth, and verify/retrospect.
>
> **Writers:** `tech-review-doc` (in-repo, design → review). `humanizer` / `humanizer-zh` are **external strong dependencies** (not shipped in this repo) for EN/ZH de-slop.
>
> **Not** `solve-workflow` / `analysis-core`. Stage 2 is writing-oriented source analysis only.
>
> **Output templates:** [reference.md](reference.md).

## Prerequisite skill check

At startup, verify every frontmatter `dependencies` entry. If any is missing, abort with an install hint — **no silent degradation**.

| Missing skill | Install (directory / `name` MUST match) |
|---------------|------------------------------------------|
| `clarifying-question-discipline`, `tech-review-doc`, `workflow-mode-lifecycle` | `npx skills add FuDesign2008/open-skills -g --skill <name> --yes` |
| `humanizer` | `npx skills add https://github.com/blader/humanizer.git` → skill dir **`humanizer`** |
| `humanizer-zh` | `npx skills add https://github.com/op7418/Humanizer-zh.git` → skill dir **`humanizer-zh`** |

Or for all **in-repo** open-skills: `npx skills add FuDesign2008/open-skills -g --skill '*' --yes` (does **not** install external humanizers).

**Must not depend on:** `analysis-core`, `runtime-evidence-debug`, `hybrid-debug`, `browser-debug-toolkit`.
**Must not vendor:** do not add `skills/humanizer/` or `skills/humanizer-zh/` to this repository.
## Triggers and modes

| Phrasing | Mode | Note |
|----------|------|------|
| 「写文档」「写文档工作流」「write workflow」 | 👤 Manual | Detect document type |
| 「写技术评审」「生成评审文档」 | 👤 Manual | Route → `tech-review-doc` |
| 「去AI痕迹」「人性化改写」「humanize」 | 👤 Manual | Route → `humanizer` / `humanizer-zh` by language |
| 「自动写文档」「自动模式」+ write intent | 🤖 Auto | Advance; writer-specific hard pauses still apply |

**Mode detection:** 「自动」 → auto; else manual. Mid-run: 「切换自动模式」/「切换手动模式」.

Core lifecycle → `workflow-mode-lifecycle`. **Differences:**

- **Completion** = stage 8 done → revert to manual.
- **Hard pauses (even in auto):**
  - `tech-review-doc`: §1 user approval; missing design path
  - `humanizer` / `humanizer-zh`: confirmed input text or file path (no tech-review §1 gate)
- After hard pause clears in auto: continue writer + stages 7–8 without extra host stops.
- Interruption → revert to manual.

## Path selection

| Path | When | Depth |
|------|------|--------|
| Full | Major review / fuzzy goals / heavy humanize pass | Full writer depth |
| Incremental | Ordinary docs | Default |
| Lean | Small high-certainty change | Minimal optional sections; **verify + writer hard pause never skipped** |

## ⚡ Quick Reference

| Stage | 👤 Manual stop | 🤖 Auto | Required output |
|-------|----------------|---------|-----------------|
| 1 Clarify intent | ⛔ Confirm route/Path/mode | Skip if clear | Restatement + writer + Path |
| 2 Analyze sources | ⛔ Gaps/readiness | Continue if no blockers | Inventory + gaps |
| 3 Explore approach | ⛔ Choices | Auto-pick | Approach |
| 4 Review approach | ⛔ Checklist OK | Auto-pass if clean | Checklist |
| 5 Make outline | ⛔ Confirm | Hand off | Outline / humanize plan |
| 6 Execute writer | Writer hard pause | Same pause; then continuous | Writer output |
| 7 Verify | ⛔ Confirm | Continue if green | Verify report |
| 8 Retrospect | End | End + revert manual | Brief improvements |

## Stage 1: Clarify intent

1. Document type / writer route (table below).
2. Path (Full/Incremental/Lean) and mode.
3. `clarifying-question-discipline` when unclear (**one question per turn**).
4. **Language for humanize:** primarily Chinese → `humanizer-zh`; primarily English → `humanizer`; ambiguous → ask once.

| Document type | Writer | Status |
|---------------|--------|--------|
| Technical review (design → product/QA) | `tech-review-doc` | In-repo |
| AI de-slop / humanize (English-primary) | `humanizer` | External strong dep |
| AI de-slop / humanize (Chinese-primary) | `humanizer-zh` | External strong dep |
| Other | Ask or stop | — |

**[👤]** Confirm. **[🤖]** Skip confirm when route + inputs already clear.

Output: [reference.md](reference.md) § Stage 1.

## Stage 2: Analyze sources

1. **Existence:** required input readable (design path or text/file to humanize).
2. **Inventory:** for tech-review — title/modules/Mermaid/multi-option; for humanize — language, length, tone target.
3. **Gaps:** list blockers for later stages.
4. Do **not** write the final output file yet (except analysis notes in chat).

**[👤]** Stop after report. **[🤖]** Continue unless blocking gap.

## Stages 3–5 by writer profile

### Profile: `tech-review-doc`

- **3** Diagrams / §3 / §6 / §4 depth  
- **4** Audience checklist (no code in §§1–3)  
- **5** Outline → hand off writer Step 1 (§1 draft)

### Profile: `humanizer` / `humanizer-zh`

- **3** Scope: whole doc vs selection; tone (formal/casual/technical)  
- **4** Checklist: preserve facts; no invented claims; match tone  
- **5** Short plan: input → rewrite → optional change summary  

**[👤]/[🤖]** pauses per Quick Reference.

## Stage 6: Execute via writer

Load the routed writer and **follow it exactly**.

- `tech-review-doc`: HARD-GATE on §1; auto may continuous-run after approval.
- `humanizer` / `humanizer-zh`: require confirmed input; then rewrite per that skill; **do not** apply tech-review §1.

## Stage 7: Verify

- **tech-review-doc:** path/naming, §1 approved, diagrams, §3/§6 rules, §§1–3 language rules.  
- **humanizer*:** facts preserved, AI patterns reduced, tone matched; optional quality score if the writer defines one.

Output: [reference.md](reference.md) § Stage 7.

## Stage 8: Retrospect

Brief improvements. Do not edit skill files unless asked. Revert auto → manual.

## Extension slot (future writers)

1. Add `skills/<name>/` and publish.  
2. Prefer **optional** route unless product requires strong dep (external humanizers are strong by deliberate choice; still not vendored here).  
3. Add route row + description triggers (≤1024).  
4. Stage 6 stays “load writer and follow exactly.”

## Relationship to other skills

| Skill | Relationship |
|-------|--------------|
| `tech-review-doc` | Strong dep (in-repo); review writer |
| `humanizer` | Strong dep (**external**); EN humanize |
| `humanizer-zh` | Strong dep (**external**); ZH humanize |
| `clarifying-question-discipline` | Strong dep |
| `workflow-mode-lifecycle` | Strong dep |
| `solve-workflow` | Sibling — not wired |

## Red flags

- Skipping `tech-review-doc` §1 in auto mode  
- Applying §1 gate to humanizer routes  
- Silent degrade when humanizer skills missing  
- Declaring `analysis-core` on this host  
- Inlining full writer bodies into this file  
