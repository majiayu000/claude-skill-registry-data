---
name: rename
description: เปลี่ยนชื่อ identifier, file, directory หรือ skill รวม batch rename ตาม pattern พร้อมอัปเดต references
argument-hint: "[old-name] [new-name] หรือ <pattern> <replacement> [path]"
related:
  - update-references
  - check-long-files
  - search-files-patterns
  - review-devin-global-harness
  - resolve-errors
  - report
  - use-astgrep
  - fix
---

## Goal

เปลี่ยนชื่อ identifier (variable, function, type, class, interface, enum) ใน code ด้วย ast-grep และอัปเดท references ทั้งหมดอย่างปลอดภัย

## Scope

Rename code identifiers ด้วย ast-grep, หรือ rename file/skill/directory พร้อม update context: `name`, `description`, `related`, `AGENTS.md`, `global_rules.md`, paths — รวม mass/batch file rename ตาม pattern (merged จาก `/batch-rename-files` เดิม)

## Execute

### 1. Identify Rename Target

> Goal: ระบุ identifier ที่จะ rename และ scope ของการเปลี่ยนแปลง

1. ระบุ identifier เดิมและชื่อใหม่ที่ต้องการ
2. ระบุประเภท: variable, function, type, class, interface, enum, property
3. ระบุ language: TypeScript, JavaScript, Rust, Python, etc.
4. ตรวจสอบว่าชื่อใหม่ไม่ขัดแย้งกับ identifier ที่มีอยู่แล้ว
5. ถ้าชื่อใหม่ซ้ำกับ identifier ที่มีอยู่ → stop และ report

### 2. Search All References

> Goal: ค้นหา references ทั้งหมดของ identifier เดิมก่อน rename

1. ใช้ `ast-grep run -p '$OLD_NAME' --lang <lang> <path>` เพื่อค้นหาทุก occurrence
2. ใช้ `grep_search` สำหรับค้นหาใน config files, markdown, และ non-code files
3. จำแนก references: definition, call site, type annotation, import/export
4. บันทึกจำนวน references ที่พบเพื่อ verify หลัง rename
5. ถ้าไม่พบ references → stop และ report

### 3. Rename With Ast-grep

> Goal: ใช้ ast-grep สำหรับ rename identifier ทั้ง definition และ usage

1. Batch rewrite หลายไฟล์ → ทำ `/use-astgrep rewrite` (dry-run + diff preview + confirm ในตัว) แทนรัน `--rewrite` ตรงๆ:
   ```sh
   ast-grep run -p 'oldName' --rewrite 'newName' --lang ts <path>
   ```
2. ใช้ interactive mode เพื่อ review ทุก change ก่อน apply — `-i`/`--interactive` หรือ flow ของ `/use-astgrep rewrite`:
   ```sh
   ast-grep run -p 'oldName' --rewrite 'newName' --lang ts -i <path>
   ```
3. สำหรับ rename ที่ต้อง match เฉพาะประเภท (เช่น function เท่านั้น) ให้สร้าง YAML rule (apply ผ่าน `/use-astgrep rewrite` rule-file flow):
   ```yaml
   id: rename-function
   language: TypeScript
   rule:
     pattern: oldName($$$ARGS)
   fix: newName($$$ARGS)
   ```
4. สำหรับ rename ที่ต้อง match หลายรูปแบบพร้อมกัน ใช้ YAML doc separator (`---`) เพื่อ define หลาย rules ในไฟล์เดียว:
   ```yaml
   id: rename-def
   language: TypeScript
   rule:
     pattern: function oldName($$$ARGS) { $$$BODY }
   fix: function newName($$$ARGS) { $$$BODY }
   ---
   id: rename-call
   language: TypeScript
   rule:
     pattern: oldName($$$ARGS)
   fix: newName($$$ARGS)
   ```
5. รัน `ast-grep scan --config <rule.yml> --update` เพื่อ apply ทุก rules
6. ถ้า ast-grep ไม่ match บางกรณี → ใช้ `edit` หรือ `multi_edit` แก้ manually

### 4. Update Non-Code References

> Goal: อัปเดท references ในไฟล์ที่ ast-grep ไม่ครอบคลุม

1. ทำ `/update-references` เพื่ออัปเดท references ใน config files, markdown, JSON, YAML
2. ค้นหาด้วย `grep_search` อีกครั้งเพื่อยืนยันว่าไม่มีชื่อเดิมเหลือ
3. อัปเดท documentation ที่อ้างอิง identifier เดิม
4. อัปเดท test files ที่อ้างอิง identifier เดิม
5. อัปเดท comments ที่อ้างอิง identifier เดิม

### 5. Validate Changes

> Goal: ตรวจสอบว่า rename สมบูรณ์และไม่ทำลาย code

1. รัน `grep_search` ค้นหาชื่อเดิมอีกครั้ง → ต้องไม่พบ (ยกเว้นใน git history หรือ comments ที่ไม่เกี่ยวข้อง)
2. รัน typecheck: `tsc --noEmit` หรือ `bun run typecheck`
3. รัน lint: `biome lint` หรือ `bun run lint`
4. รัน tests: `bun run test` หรือ `vitest run`
5. ถ้า validation ไม่ผ่าน → ทำ `/resolve-errors` และ fix จนผ่าน (max 3 ครั้ง → stop/report)

### 6. Rename File Or Skill

> Goal: เปลี่ยนชื่อไฟล์, directory, หรือ skill พร้อม update context

1. ถ้า rename skill → เปลี่ยนชื่อ directory ด้วย `git mv`
2. อัปเดท `name` ใน frontmatter ให้ตรง directory name
3. อัปเดท `description` ถ้าชื่อเปลี่ยนทำให้ความหมายเปลี่ยน
4. อัปเดท `related` ถ้ามี skill ที่เปลี่ยนชื่อ
5. อัปเดท body ทั้งหมด: `/<old-name>` → `/<new-name>`, paths, และ markdown links
6. อัปเดท `AGENTS.md` และ `global_rules.md` ถ้ามี slash references
7. ทำ `/update-references` ทั่ว repo
8. ทำ `/review-devin-global-harness` ยืนยันครบ

### 7. Batch Rename Files By Pattern

> Goal: rename ไฟล์จำนวนมากตาม pattern — preview + collision handling + reference updates

1. รับ pattern + replacement — literal/regex (`-replace`), case transforms, numbering; ระบุ scope: recursive, include/exclude patterns
2. Preview `old → new` mapping ทุกไฟล์ก่อนเสมอ (dry-run default); flag issues: collisions (หลายไฟล์ map ไปชื่อเดียวกัน), no-ops, case-only (Windows case-insensitive fs ต้อง two-phase via temp name), locked files (ตรวจ locked files ด้วย handle/Resource Monitor)
3. Confirm แล้วค่อย rename — `git mv` ใน repo เพื่อรักษา history; collisions → two-phase (temp name ก่อน); error >0 ใน critical scope → หยุดทั้ง batch
4. ทำ `/update-references` เสมอ — imports, requires, config, docs; ค้น filename เดิมด้วย `/search-files-patterns`; reference update ที่เป็น AST pattern → `/use-astgrep rewrite`
5. Verify: build/tests/lint ผ่าน; `/report` สรุป renamed / skipped / failed + undo path (`git revert`)

## Rules

### 1. Ast-grep First

ใช้ ast-grep เป็นเครื่องมือหลักสำหรับ rename:

- ใช้ `--rewrite` flag สำหรับ ad-hoc rename แบบเร็ว
- ใช้ YAML rule กับ `fix` field สำหรับ rename ที่ซับซ้อนหรือต้อง match เฉพาะประเภท
- ใช้ `--interactive` flag เมื่อต้อง review ทุก change ก่อน apply
- ใช้ meta-variables (`$OLD`, `$$$ARGS`) เพื่อ capture และ replay ใน fix
- ใช้ `transform` สำหรับ case conversion (เช่น camelCase → PascalCase)
- อ้างอิง `/use-astgrep` สำหรับการใช้งาน ast-grep โดยละเอียด

### 2. Match All Occurrence Types

Rename ต้องครอบคลุมทุกรูปแบบการใช้งาน:

- Function: definition, call site, type reference, import/export
- Variable: declaration, usage, destructuring, reassignment
- Type/Interface: definition, type annotation, generic parameter, import/export
- Class: definition, instantiation, type reference, import/export
- Enum: definition, member access, import/export
- Property: definition, access, destructuring, optional chaining

### 3. Safety And Scope Control

ป้องกันการ rename ผิดตัว:

- ใช้ `kind: identifier` ใน rule เพื่อจำกัดเฉพาะ identifier nodes
- ใช้ `constraints` เพื่อกรองเฉพาะ identifier ที่ต้องการ
- ใช้ `files` และ `ignores` ใน rule เพื่อจำกัด scope
- ตรวจสอบว่าชื่อใหม่ไม่ซ้ำกับ identifier ที่มีอยู่ก่อน rename
- ใช้ `--interactive` เมื่อไม่แน่ใจว่า match ถูกต้องทุกตัว

### 4. YAML Rule For Complex Rename

ใช้ YAML rule เมื่อ ad-hoc `--rewrite` ไม่เพียงพอ:

- ใช้ YAML doc separator (`---`) เพื่อ define หลาย rules ในไฟล์เดียว
- แยก rule สำหรับ definition และ call site อย่างชัดเจน
- ใช้ `transform` สำหรับ case conversion หรือ string manipulation
- ใช้ `rewriters` สำหรับ nested transformation
- เก็บ rule ไว้ใน `rules/` หา้งต้องการ reuse

### 5. Batch File Rename

- Preview `old → new` mapping ครบก่อน execute — ไม่ rename เองโดยไม่ confirm; collisions/no-ops ต้อง resolve ก่อน
- ใช้ `git mv` ใน repo — history ต้องไม่หาย; case-only rename บน Windows ต้อง two-phase via temp
- `/update-references` บังคับทุกครั้งหลัง mass rename — verify ไม่มีชื่อเดิมเหลือก่อนจบ

### 6. Validation Checklist

ตรวจสอบหลัง rename ทุกครั้ง:

- ค้นหาชื่อเดิมด้วย `grep_search` → ต้องไม่พบใน code files
- Typecheck ผ่าน
- Lint ผ่าน
- Tests ผ่าน
- จำนวน references ใหม่ตรงกับจำนวน references เดิมที่บันทึกไว้

## Expected Outcome

- identifier ถูก rename สมบูรณ์ในทุก occurrence
- ไม่มี broken references ใน code, config, และ docs
- Typecheck, lint, และ tests ผ่าน
- ประวัติการ rename สามารถ track ผ่าน git diff
