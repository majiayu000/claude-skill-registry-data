---
name: use-astgrep
description: ตั้งค่าและใช้งาน ast-grep สำหรับ code search, lint และ refactoring ด้วย AST-based patterns — dispatcher เข้า workflows/{scan,rewrite,transform,migration}
argument-hint: "[scan|rewrite|transform|migration|scope]"
related:
  - update-astgrep-rules
  - check-code-structure
  - replace
  - search-with-astgrep
  - use-astgrep-programmatic
  - migration-with-astgrep
  - deep-review
---

## Goal

ตั้งค่าและใช้งาน ast-grep สำหรับ code search, lint และ refactoring ด้วย AST-based patterns ที่แม่นยำกว่า regex — setup อยู่ที่นี่, execution อยู่ใน workflows

## Scope

ครอบคลุมการตั้งค่า `sgconfig.yml`, project structure, scan script และ dispatch เข้า workflows — การเขียน rules ถาวรอยู่ใน `/update-astgrep-rules`, ad-hoc search อยู่ใน `/search-with-astgrep`, programmatic/scripting อยู่ใน `/use-astgrep-programmatic`

## Execute

### 1. Install Or Use ast-grep

> Goal: ติดตั้งหรือเรียกใช้ ast-grep ได้ถูกต้อง

1. ถ้า project มี `@ast-grep/cli` ใน `devDependencies` ให้ใช้ `bunx ast-grep` (bin `ast-grep` หรือ `sg` จาก local install)
2. ถ้าไม่มี local install ให้ใช้ `bunx -p @ast-grep/cli ast-grep` — ห้าม `bunx ast-grep` ลอยๆ เพราะจะดึง package `ast-grep` (คนละ package ที่ถูก abandon)
3. ถ้าต้องการใช้งานประจำ แนะนำให้เพิ่ม `@ast-grep/cli` ใน `devDependencies` — latest `0.45.3 (verified 2026-09-12)`

### 2. Configure sgconfig.yml

> Goal: สร้าง `sgconfig.yml` พร้อม fields ที่จำเป็น

1. สร้างไฟล์ `sgconfig.yml` ที root directory ด้วย `ruleDirs` ชี้ `rules/{dependencies,architecture,glob}` ตาม canonical layout ใน `/update-astgrep-rules`
2. ถ้า project มีหลาย workspace ให้เพิ่ม rule dir ของแต่ละ workspace ใน `ruleDirs` (ไม่มี `devPaths` field — fields ที่มีจริง: `ruleDirs`, `testConfigs`, `utilDirs`, `languageGlobs`, `customLanguages`, `languageInjections`)
3. ถ้า project มี custom file extensions ให้เพิ่ม `languageGlobs`
4. ถ้าต้องการ test rules ให้เพิ่ม `testConfigs`
5. ถ้าต้องการ reusable patterns ให้เพิ่ม `utilDirs`
6. ตรวจสอบว่า config ถูกต้องด้วย `ast-grep scan --inspect summary`

### 3. Setup Project Structure

> Goal: สร้างโครงสร้าง directories สำหรับ rules และ tests

1. สร้าง ast-grep rules ใน `rules/` directory ที project root ตาม canonical layout ใน `/update-astgrep-rules` (`.devin/rules/` markdown rules deprecated — ถ้าพบให้ลบ)
2. ถ้ามี `testConfigs` ให้สร้าง directory `rule-tests/` ที project root
3. ถ้ามี `utilDirs` ให้สร้าง directory `utils/` ที project root
4. ใช้ `ast-grep new` สำหรับ scaffold project ใหม่ได้ (หรือ `bunx -p @ast-grep/cli ast-grep new` ถ้ายังไม่ได้ติดตั้ง)

### 4. Add Scan Script

> Goal: เพิ่ม scan script ใน `package.json`

1. เพิ่ม script ใน `package.json`:

```json
{
  "scripts": {
    "scan": "ast-grep scan"
  }
}
```

2. ใช้ `ast-grep scan` หรือ `sg scan` เมื่อ `@ast-grep/cli` ติดตั้งเป็น devDependency แล้ว — ถ้ายังไม่ได้ติดตั้งใช้ `bunx -p @ast-grep/cli ast-grep scan`

### 5. Choose Workflow

> Goal: route ไป workflow ที่ตรงกับงาน

| งาน | Workflow |
|-----|----------|
| scan project ด้วย rules, filter/format findings, CI | `/use-astgrep scan` |
| batch rewrite หลายไฟล์ด้วย pattern (`-p`/`-r`, dry-run → confirm → apply) | `/use-astgrep rewrite` |
| rule-YAML transforms (`transform`/`rewriters`/constraints) | `/use-astgrep transform` |
| migration ทั้ง codebase แบบ staged batches | `/use-astgrep migration` |
| ad-hoc search เท่านั้น (ไม่ rewrite) | `/search-with-astgrep` |
| batch/programmatic ผ่าน Bun scripts, napi | `/use-astgrep-programmatic` |
| เขียน/promote rules ถาวรใน `rules/` | `/update-astgrep-rules` |

1. ถ้า argument ตรง workflow → อ่าน `workflows/<name>/SKILL.md` แล้วทำตาม flow ในนั้น
2. ทดสอบ pattern บนไฟล์ตัวอย่าง 1-2 ไฟล์ก่อนรันทั้ง project เสมอ

## Rules

### 1. CLI Reference

- `ast-grep new` สำหรับ scaffold project ใหม่, `ast-grep new rule` สำหรับสร้าง rule ใหม่
- `ast-grep scan` สำหรับ scan ทั้ง project ด้วย rules (options ละเอียด → `workflows/scan/SKILL.md`)
- `ast-grep run --pattern 'PATTERN'` สำหรับ ad-hoc search (`run` เป็น default subcommand)
- `ast-grep run -p 'PATTERN' -r 'REWRITE'` สำหรับ rewrite (options ละเอียด → `workflows/rewrite/SKILL.md`)
- `ast-grep test` สำหรับ test rules, `ast-grep outline` ดู structure, `ast-grep lsp` language server, `ast-grep completions <shell>` completions
- ไม่มี `ast-grep rewrite` subcommand — rewrite ทำผ่าน `run -r`/`scan` กับ `--interactive` หรือ `-U`

### 2. Separation From Devin Rules

- `rules/` เก็บ `.yml` ast-grep rules ที project root (`rules/{dependencies,architecture,glob}`)
- `.devin/rules/` (markdown rules) deprecated — ถ้าพบให้ลบและใช้ `rules/` + `sgconfig.yml` แทน
- rule files ใช้ `kebab-case` filename
- ไฟล์ที่ไม่ใช่ rule ใน `rules/` จะถูก ignore

### 3. Integration With Biome

- ใช้ `ast-grep` สำหรับ structural patterns ที่ `Biome` ไม่สามารถ express ได้ — complements ไม่ใช่ replace
- ใช้ `Biome` สำหรับ standard lint และ format

### 4. Rule Writing

- การเขียน rules ถาวรอยู่ใน `/update-astgrep-rules` ไม่ใช่ workflow นี้

### 5. Pattern Discipline

- ใช้ AST-based patterns สำหรับ structural match ก่อน regex
- ตรวจสอบ syntax ด้วย `ast-grep run --pattern 'PATTERN' --debug`
- ทดสอบ pattern บนไฟล์ตัวอย่างก่อนรันทั้ง project
- ปล่อยให้ ast-grep auto-detect ภาษา หรือระบุ `--lang` ถ้า extension ไม่มาตรฐาน
- ทุก rewrite ต้อง dry-run + preview + confirm ก่อน apply — workflows บังคับอยู่แล้ว ห้ามข้าม

- ใช้ /check-code-structure ถ้าจำเป็น
- ใช้ `/deep-review` ถ้าจำเป็น

## Expected Outcome

- `sgconfig.yml` ตั้งค่าเรียบร้อยครบทุก fields ที่จำเป็น
- Project structure สร้างเรียบร้อย (`rules/`, `rule-tests/`, `utils/`)
- Scan script เพิ่มใน `package.json` และทำงานได้
- งานถูก route เข้า workflow ที่ถูกต้อง (`scan`/`rewrite`/`transform`/`migration`)
- ใช้ร่วมกับ `Biome` ได้โดยไม่ขัดแย้ง
