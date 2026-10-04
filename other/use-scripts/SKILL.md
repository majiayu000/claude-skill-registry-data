---
name: use-scripts
description: สร้าง scripts สำหรับ automate งานด้วย Bun, nushell, pwsh, หรือ ast-grep
argument-hint: "[target]"
related:
  - use-bun-shell
  - use-bun-native-api
  - create-files-in-os-temp
  - use-nu-shell
  - use-pwsh-shell
  - use-astgrep
  - follow-tool-rolldown
  - follow-lib-esm-sh
  - transform
  - run-verify
  - update-references

---

## Goal

สร้าง scripts เพื่อ automate งานและประมวลผลไฟล์ ด้วย Bun native APIs, nushell, pwsh, หรือ ast-grep ตามความเหมาะสม

## Scope

ใช้สำหรับสร้าง scripts ใน workspace ด้วย Bun native APIs, nushell, pwsh, หรือ ast-grep — รวมการแก้ไขหลายไฟล์ผ่าน scripts (merged `/edit-with-use-scripts`, ดู `### 5. Edit Files Via Scripts`)

## Execute

### 1. Choose Shell And Type

> Goal: เลือก shell/script type ให้เหมาะสม

1. ค่าเริ่มต้น: ใช้ skill นี้ หรือ `/use-bun-shell` เมื่อ:
   - ต้องการ Bun native APIs สำหรับ automate งาน
   - ใช้ JS/TS scripts เป็นค่าเริ่มต้น
   - ต้องการ JavaScript/TypeScript runtime
   - ทำงานกับ JSON, HTTP, async/await, npm packages
   - ต้องการ Bun native APIs เช่น `Bun.file`, `Bun.write`, `Bun.$`
   - ต้องการ cross-platform scripts ด้วย JS/TS
2. ใช้ `/use-nu-shell` เมื่อ:
   - ต้องการ structured data pipelines
   - อ่าน/ประมวลผล JSON, CSV, TOML, YAML ด้วย built-in commands
   - ต้องการ cross-platform shell syntax ที่อ่านง่าย
   - ไม่ต้องการ .NET หรือ Windows-only features
3. ใช้ `/use-pwsh-shell` เมื่อ:
   - ทำงานบน Windows โดยเฉพาะ system administration
   - ต้องการ call .NET APIs, registry, WMI, COM
   - ต้องการ verbose try-catch error handling
4. ใช้ `ast-grep` เมื่อ:
   - ต้องการ AST-based code search
   - ต้องการ code transformation หรือ linting
5. ถ้าไม่แน่ใจ → ใช้ Bun native APIs เป็นค่าเริ่มต้น แล้วระบุเหตุผลถ้าเปลี่ยนไป shell อื่น

### 2. Choose Script Location

> Goal: เลือก location สำหรับ script

1. ทำ `/create-files-in-os-temp` เพื่อสร้างและจัดการ scripts ชั่วคราวใน OS temp directory (throwaway, ไม่สร้างใน project)
2. `.devin/scripts/` — scripts ถาวร (committed, เก็บไว้ใช้ซ้ำ)
3. ไม่สร้าง `temp/` หรือ `.devin/scripts/temp/` ใน project workspace
4. ถ้าใช้ Bun native APIs โดยตรง → ใช้ `os.tmpdir()` หรือ `$env:TEMP` เฉพาะกรณีที skill ไม่เหมาะสม

### 3. Create Script

> Goal: เขียน script ตาม standards

1. เขียนแบบ composable: `createScript()` return state + actions
2. ใช้ Bun native APIs สำหรับ `.ts` scripts โดยไม่ใช้ Node.js libraries ยกเว้นไม่มีทางเลือก (ดู `/use-bun-shell`, `/use-bun-native-api`)
3. ใช้ `nu` สำหรับ `.nu` scripts ถ้าประมวลผล structured data
4. ใช้ `pwsh` สำหรับ `.ps1` scripts ถ้า Windows-specific
5. ใช้ CDN imports สำหรับ external dependencies ที Bun native APIs ไม่ครอบคลุม: `https://esm.sh/<name>`
6. ใช้ `eta` ผ่าน `https://esm.sh/eta@4.6.0` สำหรับ template/render ใน Bun scripts (eta `4.6.0 (verified 2026-09-26)` — ดู `/follow-lib-esm-sh` สำหรับ CDN convention)
7. ถ้าต้องการ parse JS/TS AST ด้วยความเร็วสูง → ใช้ `oxc-parser` ผ่าน `https://esm.sh/oxc-parser` หรือ `bun add oxc-parser` (`0.149.0 (verified 2026-09-26)`)
8. ถ้าต้องการ bundle ด้วยความเร็วสูง → ใช้ `rolldown` ตาม `/follow-tool-rolldown` (`1.2.11 (verified 2026-09-26)`, ใช้ `oxc` parser เหมือนกัน)
9. เพิ่ม `dryRun` option สำหรับ testing

### 4. Test And Execute

> Goal: ทดสอบและรัน script อย่างปลอดภัย

1. รัน script ใน dry run mode เพื่อดูผลลัพธ์
2. แก้ไข errors ก่อนรันจริง
3. รัน:
   - `bun run <script>.ts` สำหรับ Bun scripts
   - `nu <script>.nu` สำหรับ Nushell scripts
   - `pwsh <script>.ps1` สำหรับ PowerShell scripts
   - `ast-grep scan` สำหรับ AST operations
4. ลบ scripts จาก OS temp หลังใช้งานเสร็จ หรือให้ `/create-files-in-os-temp` จัดการ cleanup

### 5. Edit Files Via Scripts

> Goal: แก้ไขหลายไฟล์ผ่าน script ที่ reproducible และ audit ได้ (merged `/edit-with-use-scripts`)

ใช้เมื่อ task เป็นการแก้ไขไฟล์ที่ซับซ้อน ต้องแก้หลายไฟล์พร้อมกัน หรือต้องการ reproducibility และ audit trail — ไม่ใช่สำหรับไฟล์เดียวแบบ simple (`/edit-only`), config files (`/edit-manual`) หรือ AST-pattern edits (`/use-astgrep rewrite`)

1. Identify: รับรายการไฟล์ + changes จาก user — ทำ `/scan-codebase` หาไฟล์ที่เกี่ยวข้องและ patterns, วางแผน minimal changes ด้วย `/dont-over-engineer`
2. Script requirements (บังคับทุกข้อ):
   - dry run mode เป็น default — execute จริงเฉพาะหลัง preview + user confirm เท่านั้น
   - backup mode: สำเนาไฟล์เดิมก่อนแก้
   - validate โครงสร้างไฟล์หลังแก้ (JSON/YAML/TS syntax)
   - report สรุป: ไฟล์ที่แก้, จำนวน changes, errors ถ้ามี
   - เก็บใน OS temp เท่านั้น ห้าม commit เข้า repo
3. AST edit logic ใน script → ใช้ ast-grep ผ่าน `Bun.$`/napi ตาม `/use-astgrep-programmatic` หรือ delegate ทั้ง flow ไป `/use-astgrep rewrite`
4. Dry run → ตรวจ output → แก้ script → dry run ใหม่จนถูก → ขอ user confirmation → execute
5. หลัง execute: ทำ `/run-verify` (lint/typecheck/scan) → fail แก้ด้วย `/resolve-errors` (max 3 ครั้ง → rollback จาก backup + report) → ทำ `/update-references`
6. Cleanup: ลบ scripts จาก temp + ลบ backup หลัง validation ผ่านครบ — เก็บ script/output เป็น audit trail ถ้าจำเป็น

## Rules

### 1. Script Type Selection

- `/use-bun-shell` — JS/TS, JSON, HTTP, async, cross-platform
- `/use-nu-shell` — structured data, pipelines, cross-platform shell
- `/use-pwsh-shell` — Windows system admin, .NET, COM, WMI
- `ast-grep` — AST-based code search/transformation

### 2. File Locations

- ทำ `/create-files-in-os-temp` สำหรับ throwaway scripts (OS temp directory, ไม่สร้างใน project)
- `.devin/scripts/` — permanent scripts (committed)
- ใช้ `.ts` สำหรับ Bun, `.nu` สำหรับ Nushell, `.ps1` สำหรับ PowerShell

### 3. Edit Scripts Safety

- Script ที่แก้ไฟล์ต้องมี dry run mode เสมอก่อน execute จริง และต้องสร้าง backup ก่อนแก้
- ถ้า validation ไม่ผ่าน → rollback จาก backup และ report
- ห้าม execute จริงโดยไม่มี user confirmation หลัง dry run
- Script ต้องให้ผลเหมือนเดิมเมื่อรันด้วย input เดิม — ไม่สร้าง side effects นอกจากการแก้ไฟล์ที่กำหนด

### 4. Bun Native API Preference

- เมื่อใช้ Bun ให้ใช้ Bun native APIs เท่านั้นสำหรับ `.ts` scripts โดยไม่ใช้ Node.js libraries ยกเว้นไม่มีทางเลือก
- `Bun.Glob` แทน `fast-glob`, `Bun.$` แทน `execa`, `Bun.file()` + `Bun.write()` แทน `fs-extra`
- ไม่ import `node:fs` โดยตรงถ้า `Bun.file`/`Bun.write` ทำงานได้
- ถ้าต้องการ parse JS/TS AST ด้วยความเร็วสูง → ใช้ `oxc-parser` ก่อน `acorn` หรือ `babel`
- ถ้าต้องการ bundle ด้วยความเร็วสูง → ใช้ `rolldown` ตาม `/follow-tool-rolldown`

### 5. CDN Libraries

```typescript
import { z } from "https://esm.sh/zod"
import { glob } from "https://esm.sh/glob"
import { render } from "https://esm.sh/eta@4.6.0"
```

- CLI: `zod`, `cac`, `consola`, `@clack/prompts`, `picocolors`
- Parsing: `yaml`, `gray-matter`, `jsonc-parser`
- JS/TS AST: `oxc-parser` สำหรับ parse/transform JS/TS ด้วยความเร็วสูง
- Bundling: `rolldown` สำหรับ bundle ด้วย `oxc` parser (ดู `/follow-tool-rolldown`)
- File System: `pretty-bytes`, `env-paths`, `semver`
- Async: `p-limit`, `p-queue`, `p-map`
- Template: `eta` สำหรับ generate text/files จาก template

### 6. Decision Records

- ระบุเหตุผลทุกครั้งที่เลือก shell ใด shell หนึ่ง
- บันทึกเหตุผลใน comment หรือ docstring ของ script
- ถ้า fallback จาก shell หนึ่งไปอีก shell ต้องระบุเหตุผล

## Expected Outcome

- Scripts ทำงานได้ด้วย Bun, nushell, pwsh, หรือ ast-grep
- การเลือก shell มีเหตุผลชัดเจน
- Dependencies ผ่าน CDN (ไม่ต้อง install)
- สามารถใช้ `eta` สำหรับ template/render ใน Bun scripts
- Scripts อยู่ใน location ถูกต้องตาม Rules
- Temp scripts ใน `$env:TEMP` ถูกลบหลังใช้งาน, permanent scripts เก็บไว้ใช้ซ้ำ
- Dry run mode สำหรับทดสอบก่อน execute จิง
- สามารถใช้ /use-pwsh-shell /use-bun-shell /use-astgrep (programmatic workflow) ได้ ตามเหมาะสม

