---
name: refactor
description: Refactor ไฟล์, workspace, หรือ codebase ตาม context — SRP, boundaries, style, consistency
argument-hint: "[@files... | scope | clean | layered | orm | structure]"
related:
  - refactor-skills
  - simplify
  - refactor-workspace
  - refactor-to-packages-shared
  - no-hard-code
  - no-use-ignore
  - update-references
  - update-agents-md
  - update-config
  - update-tests
  - run-verify
  - check-code-structure
  - deep-review
  - check-long-files
  - resolve-errors
  - dont-over-engineer
  - follow-single-of-source
  - follow-reusable
  - follow-my-techstack
  - use-lib-effective
  - follow-architecture
  - deep-validate
  - check-long-files
  - relocation
  - scan-codebase
  - follow-review
  - run-check
  - use-astgrep
  - migration-with-astgrep
  - use-subagents

---

## Goal

Refactor ตาม context โดยเลือก scope ที่เหมาะสม: ไฟล์, workspace, codebase หรือ SRP แล้วดำเนินการจนผ่าน verify

## Scope

- ถ้า user ระบุ `@files...` → refactor เฉพาะไฟล์ โดยลงลึกถึง SRP/naming/structure
- ถ้า context เป็น workspace หรือ monorepo → ใช้ `/refactor-workspace`
- ถ้า context คือจัด architecture ตาม directory หรือเลือก clean/layered → ทำ architecture refactor — selection + dispatch ผ่าน `/follow-architecture` (หลาย apps unified → clean, app เดียว → layered)
- ถ้า context คือไฟล์/โมดูลที่รวมหลาย concerns ปนกัน (UI + logic + IO + config ในที่เดียว) → ทำ `### /separate-of-concerns` (merged)
- ถ้า context คือ extract shared code ไป `packages/shared` (duplication ข้าม packages) → ใช้ `/refactor-to-packages-shared`
- ถ้า context คือ restructure data access เป็น ORM (raw SQL, scattered queries, N+1) → ทำ data access refactor ตาม `references/orm.md` + `references/repository-pattern.md`
- ถ้า context คือ physical structure (naming, file split, content separation, relocation, barrel exports) → ทำ structure refactor ตาม `references/scope-structure.md`
- ถ้า context คือรวม/ซิงค์ tool configs และ dependency catalogs ข้าม workspaces → ใช้ `/update-config`
- ถ้า context คือลบ hardcoded values (secrets, URLs, magic strings/numbers) → ใช้ `/no-hard-code`
- ถ้า context คือลบ ignore/suppression comments (`@ts-ignore`, `eslint-disable`, `biome-ignore`, `# noqa`, `//nolint` และ ecosystem อื่น) → ใช้ `/no-use-ignore`
- ถ้า context คือทำไฟล์สั้น/อ่านง่ายขึ้นโดยไม่เปลี่ยน boundaries (verbosity, redundancy, nesting) → ใช้ `/simplify`
- ถ้าไฟล์/โมดูลยาว >250 บรรทัด หรือมี SRP issues → ทำ `### /refactor-to-srp` (merged)
- ถ้าต้องการ refactor ทั้ง codebase → ทำ codebase refactor ตาม `references/scope-codebase.md` (deep procedure: baseline → impact → batches → validation)
- ถ้า context คือเตรียมเพิ่ม feature → preparatory refactor ("make the change easy, then make the easy change") — refactor แยก commit ก่อน feature เสมอ
- ถ้าต้องการย้ายไฟล์ → ใช้ `/relocation`
- mechanical refactor หลายไฟล์ (rename/pattern/batch transform) → ใช้ `/use-astgrep rewrite` (dry-run + confirm ก่อนเขียนทับเสมอ); migration ทั้ง codebase ด้วย rule file → `/migration-with-astgrep`

## Execute

### 1. Detect Scope

> Goal: ระบุ scope ของ refactoring

1. ทำ `/follow-review` ก่อน refactor เสมอ — เลือกและรัน `review-*` ที่ตรง context ก่อนลงมือ
2. ถ้ามี `@files...` → file refactor
3. ถ้าไม่มี `@files` แต่ context เป็น monorepo/workspace → workspace refactor
4. ถ้า project มีไฟล์/โมดูลยาว >250 บรรทัด หรือมี SRP issues → SRP refactor
5. ถ้าไม่มี scope ชัดเจน → หา hotspots ด้วย evidence ก่อนเลือก target: `git log --format=format: --name-only | sort | uniq -c | sort -rn | head -20` (churn สูง × complexity สูง = คุ้มสุด)
6. เก็บ evidence ด้วย check skills ก่อนเลือก target — `/check-long-files` (ไฟล์เกิน 250 บรรทัด), `/check-code-structure` (file-level symbols/exports), `/deep-review` (SRP counts, function metrics) — ใช้ findings เป็น baseline และเลือก target ที่ severity สูงสุด
7. ถ้า scope กว้างหรือต้อง evidence เยอะ → spawn `subagents/hotspot-scout.md` (read-only) เก็บ baseline แทนการสแกนเอง แล้วใช้ prioritized target table ที่คืนมาเลือก target
8. ถ้าต้องการ refactor ทั้ง codebase หรือไม่มี files/workspace context → codebase refactor
9. ถ้า argument/context เป็น `clean`, `layered` หรือ architecture restructure ของ package/app → architecture refactor (dispatch `/follow-architecture`)
10. ถ้า argument/context คือ concerns ปนกันในไฟล์/โมดูล → `### /separate-of-concerns` (merged)
11. ถ้า argument/context เป็น `orm` หรือ data access restructure → data access refactor
12. ถ้า argument/context เป็น `structure` หรือ physical file/folder restructure → structure refactor
13. ถ้า user บอกว่าต้องการย้ายไฟล์ → ใช้ `/relocation`

### 2. File Refactor

> Goal: แก้ไขไฟล์ที่ระบุ

ทำตาม [references/scope-file.md](references/scope-file.md)

### 3. Workspace Refactor

> Goal: จัดระเบียบ workspace หรือ monorepo

ทำตาม [references/scope-workspace.md](references/scope-workspace.md)

### 4. Codebase And SRP Refactor

> Goal: แก้ไขปัญหา SRP, long files, consistency ทั้ง codebase ด้วย baseline, impact analysis, incremental batches

ทำตาม [references/scope-codebase.md](references/scope-codebase.md)

### 5. Architecture Refactor

> Goal: apply architecture pattern ให้ target — selection + execution dispatch ผ่าน `/follow-architecture`

1. ทำ `/follow-architecture` กับ target — เลือก pattern ตาม context (หลาย `apps/*` unified → clean; app เดียว/`apps/*` → layered; `packages/`/`crates/` → clean); argument `clean`/`layered` → pattern นั้นโดยตรง
2. Detail procedure ตาม [references/architecture-clean.md](references/architecture-clean.md) / [references/architecture-layered.md](references/architecture-layered.md) เมื่อต้องการรายละเอียดใน refactor context
3. ถ้าเจอ mixed concerns ระหว่าง restructure → ทำ `### /separate-of-concerns` (merged) แยก concern ก่อนจัด layer
4. ทำทีละ target — ห้าม mix pattern ใน target เดียว; หลังแต่ละ target → `/update-references` + `/run-check` ก่อน target ถัดไป
5. Canonical pattern detail อยู่ที่ `/deep-review` `## Pattern Guides` (SSOT); microservices ไม่ครอบคลุม — อ่าน `### Pattern: Microservices Architecture` ที่นั่นโดยตรง

### 6. Data Access Refactor

> Goal: restructure data access ให้ใช้ ORM type-safe — หนึ่ง ORM ต่อ project

1. ทำตาม [references/orm.md](references/orm.md) — select ORM → models/relations → queries → migrations → tests
2. repository pattern (interfaces, mappers, UnitOfWork, QuerySpec) → ทำตาม [references/repository-pattern.md](references/repository-pattern.md)
3. schema review/migration drift → `/deep-review`; boundary validation → `/follow-tool-data-validation`

### 7. Structure Refactor

> Goal: physical file/folder structure ทุกไฟล์มี single responsibility — naming, split, content separation, relocation, imports

ทำตาม [references/scope-structure.md](references/scope-structure.md)

### 8. Update References

> Goal: ไม่มี broken references

1. ทำ `/update-references` สำหรับ relative paths/imports
2. ทำ `/update-references` สำหรับ global references/skills
3. ถ้า structure/paths เปลี่ยน (ย้าย/rename/สร้าง dir ใหม่) → ทำ `/update-agents-md` ให้ AGENTS.md ตรงกับ structure ใหม่
4. ถ้ามี broken references → ทำ `/resolve-errors`

### 9. Verify

> Goal: ตรวจสอบว่า refactor ผ่าน

ทำตาม [references/verify.md](references/verify.md)

### 10. Report

> Goal: สรุปผล

1. ทำ `/report` สรุป sub-skill/scope, การเปลี่ยนแปลง, status
2. ทำ `/report-before-after` ถ้ามี baseline
3. ทำ `/suggest-next-action`

### Subagents

> Goal: dispatch งาน refactor ที่อิสระไปยัง subagent profiles

| Task | Subagent |
|------|----------|
| เก็บ baseline evidence หา refactor targets (read-only) | `subagents/hotspot-scout.md` |
| refactor ไฟล์/scope เดียว — spawn ทีละไฟล์ขนานกันเมื่อมีหลายไฟล์อิสระ | `subagents/file-worker.md` |

1. spawn ผ่าน `/use-subagents` โดยส่ง inputs ตามที่แต่ละ profile กำหนด
2. `hotspot-scout` เป็น read-only — `file-worker` แก้เฉพาะ `files` ที่ได้รับ
3. parent เป็นคน rewire consumers, checkpoint commit และ verify รวมเสมอ

## Rules

Checklist สั้น — detail ฉบับเต็มของแต่ละ rule อยู่ที่ `references/principles.md`

### 1. Preserve Behavior

- ห้าม mix feature/bug fix กับ refactor ใน commit เดียว (Two Hats) — public API/behavior เหมือนเดิมเสมอ

### 2. Safety Net First

- ไม่มี tests → เขียน characterization tests ก่อน (`/update-tests`); tests เขียวก่อนและหลัง

### 3. Small Steps

- ทีละ transformation เดียว → verify green → `/git-commit` checkpoint ทุก batch
- mechanical batch หลายไฟล์ → `/use-astgrep rewrite` (dry-run+confirm); rule-file migration → `/migration-with-astgrep`

### 4. Context Aware

- ไม่เดา scope — ไม่ชัดให้ `/ask-me`; ทำทีละ sub-skill ตาม priority

### 5. Minimal Change

- `/dont-over-engineer` + `/follow-reusable` (reuse > extend > extract > create); แก้ root cause ตาม `references/code-smells.md`; ห้าม perf tuning ใน refactor pass
- ก่อนเลือก/เพิ่ม dependency → `/follow-my-techstack` (เทียบ `deep-review`) + `/use-lib-effective` (ใช้ dep ที่มีแทน reinvent)

### 6. SRP And Consistency

- ไฟล์ ≤250 บรรทัด (`/check-long-files`); หนึ่ง fact หนึ่ง source (`/follow-single-of-source`); naming/patterns สอดคล้อง
- import paths ใช้ path alias ของ project (เช่น `~/*`) แทน relative paths ที่ซับซ้อน — ห้าม relative import 3+ levels (`../../../`)

### 7. Safety

- ย้าย/ลบ/rename → `/update-references`; destructive → dry run + confirm; ไม่ force push

### 8. Verification

- ผ่าน `/run-verify`; ไม่มี broken references

## Merged Details

### /separate-of-concerns (merged)

แยก concerns ที่ปนกันในไฟล์/โมดูลออกตามประเภท — concern types: `presentation` (UI/routes/handlers), `domain` (pure rules), `data` (persistence/queries), `io` (http/queue/external calls), `config` (env/settings), `orchestration` (composition/wiring)

1. Identify: classify แต่ละ block → concern type พร้อม `file:line` evidence; สรุป concern map (block → type → target location)
2. Plan: map concern → location ตาม architecture ของ project — ไม่ชัด layer → `/follow-architecture` ตัดสินก่อน; เรียง extract leaf ก่อน (pure domain → data/io → orchestration ทีหลัง); ระบุ consumers เตรียม `/update-references`
3. Extract ทีละ concern เดียว: move → file/module เป้าหมาย → export ผ่าน barrel → `/update-references` + verify green ก่อน concern ถัดไป — caller เหลือแค่ orchestration
4. Verify: ทุก unit เหลือ concern เดียว + `/run-check` + tests + `/report-before-after` (concern map เดิม vs ใหม่)

Rules: 1 extraction = 1 concern ไม่ mix behavior change; pure logic extractable ก่อนเสมอ; placement ตาม dependency direction; preserve public API

### /refactor-to-srp (merged)

แยก unit ที่มีหลาย responsibility — 1 unit = 1 reason to change, ไฟล์ ≤250 บรรทัด (ยกเว้น barrel/index)

1. Identify: list responsibilities ทั้งหมด (smells: Divergent Change, Shotgun Surgery, Long Method — `references/code-smells.md`) + `/deep-review` SRP counts/function metrics เป็น evidence → จัดกลุ่มตาม reason to change (ใครขอเปลี่ยน, เปลี่ยนบ่อย, เปลี่ยนพร้อมกันไหม); ไม่มี violation จริง → stop + report (`/dont-over-engineer`)
2. Split: เลือก technique ตาม smell — Extract Method → Extract Class/Module → Move Method/Field ทีละตัว; แยก content ประเภทเดียวรวมกัน (`types.ts`, `constants.ts`, `config.ts`, `schema.ts` หรือตามชื่อ domain); คง public API ผ่าน barrel re-export; หลายไฟล์อิสระ → `subagents/file-worker.md` ขนานผ่าน `/use-subagents`
3. `/update-references` ทุก split — rewire importers + ค้น refs เก่าไม่ให้เหลือ (broken → `/resolve-errors`)
4. Verify: `/run-verify` + `/check-long-files` + `/check-code-structure` เทียบ baseline — ทุกไฟล์ ≤250 บรรทัด; ไม่ผ่าน → กลับ step 2 (max 3 รอบ → stop + report)

Rules: 1 file/class/function = 1 reason to change, 1 โฟลเดอร์ = domain เดียว; หนึ่ง fact หนึ่ง canonical source (`/follow-single-of-source`); ไม่มี tests → characterization tests ก่อน (`/update-tests`); minimal split — cohesion สูงที่เปลี่ยนด้วยกันเสมออย่าแยก

## Expected Outcome

- Scope ที่เหมาะสมถูกเลือกและดำเนินการ
- ไฟล์/packages มีขนาดเหมาะสม
- imports/exports สะอาด ใช้ alias แทน relative paths ที่ซับซ้อน
- SRP ชัดเจน
- naming, patterns, structure สอดคล้อง
- ผ่าน lint/typecheck/test/build
- รายงาน before/after ครบ
