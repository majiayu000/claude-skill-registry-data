---
name: run-scan
description: รัน ast-grep scan เพื่อตรวจสอบ codebase ด้วย AST-based patterns
argument-hint: "[scope]"
related:
  - deep-review
  - use-astgrep
  - update-astgrep-rules
  - update-astgrep-rules
  - report
  - loop-until-complete
  - resolve-errors

---

## Goal

รัน `ast-grep scan` เพื่อตรวจสอบ codebase ด้วย AST-based patterns และแก้ไขปัญหาที่พบ

## Scope

ใช้สำหรับ scan codebase ด้วย `ast-grep` ใน project ที่มี `sgconfig.yml` และ rules ใน `rules/` directory

## Execute

> Pre-Run: ทำ `/deep-review` ก่อนเสมอ — `run-*` ต้อง review/ประเมินก่อนลงมือหลัก ห้ามข้าม; ถ้า findings เป็น blocker ให้แก้หรือ report ก่อนรัน (scan)

### 1. Setup And Write Rules

> Goal: Setup And Write Rules

1. ทำ `/use-astgrep` เพื่อติดตั้งและตั้งค่า `ast-grep`
2. ตรวจสอบ `sgconfig.yml` มี `ruleDirs: rules` และมี `scan` script ใน `package.json`
3. ถ้ายังไม่มี rules ให้ทำ `/update-astgrep-rules` เพื่อสร้าง rules ใน `rules/` directory
4. ทำ `/update-astgrep-rules` เพื่ออัปเดตและตรวจสอบ rules `ก่อน`รัน scan เสมอ — rules stale ทำให้ findings คลาดเคลื่อน

### 2. Run Scan

> Goal: Run Scan

1. รัน `bun run scan` หรือ `ast-grep scan`
2. ทำ `/report` เพื่อจัดรูปแบบ output และระบุ issues
3. พิจารณา rules ที่ไม่เหมาะสม ว่าถูกต้องและเหมาะสมหรือไม่
4. แก้ไข code ตาม suggestions ที่เหมาะสม หรือใช้ `--interactive` mode สำหรับ selective apply

### 3. Verify

> Goal: Verify

1. ทำ `/loop-until-complete` เพื่อรัน scan ซ้ำจนกว่าจะไม่มี issues
2. ตรวจสอบว่า fixes ไม่ทำให้ code เสีย
3. ใช้ `ast-grep test` เพื่อ verify rules
4. ถ้ามี errors หลังแก้ไข ให้ทำ `/resolve-errors`

## Rules

- ต้องมี `sgconfig.yml` ที่ root directory และ `scan` script ใน `package.json`
- rules ต้องอยู่ใน `rules/` directory และใช้ severity ตามความสำคัญ (`error`, `warning`, `info`)
- ตรวจสอบ output ทุกครั้งก่อน apply fixes และใช้ `--interactive` mode สำหรับ selective apply
- รัน scan ซ้ำหลัง apply fixes และตรวจสอบว่า code ยังทำงานได้
- ถ้า project มี CI/CD ให้เพิ่ม scan ใน pipeline และรัน scan ก่อน commit
- อัปเดต rules เมื่อมี patterns ใหม่ และตรวจสอบ false positives เพื่อ tune rules

## Expected Outcome

- `ast-grep` CLI ติดตั้งและตั้งค่าเรียบร้อย
- Rules สร้างใน `rules/` directory
- Scan รันได้และระบุ issues ที่ถูกต้อง
- Issues แก้ไขและ verify เรียบร้อย
- Codebase ผ่าน `ast-grep scan` โดยไม่มี errors