---
name: delete
description: ลบไฟล์และโฟลเดอร์อย่างปลอดภัย พร้อม dry-run confirm และ update references
argument-hint: "[scope]"
related:
  - update-references
  - run-check
  - ask-me
  - report
  - scan-codebase
  - resolve-errors
  - suggest-next-action
  - delete-cicd-fails
  - delete-git-branch
  - delete-git-submodules
  - delete-git-worktree
  - delete-projects
  - delete-project-temp

---

## Goal

ลบไฟล์หรือโฟลเดอร์ทีระบุอย่างปลอดภัย โดยตรวจสอบ impact, ขอ confirm, backup ถ้าจำเป็น และ update references

## Scope

ใช้สำหรับลบไฟล์/โฟลเดอร์ใน project ทีมี references หรือต้อง sync หลังลบ ไม่ใช้สำหรับลบ mass หรือ files นอก scope โดยไม่ถาม

สำหรับ domain-specific deletes เรียก skill ตรง: `/delete-cicd-fails`, `/delete-git-branch`, `/delete-git-submodules`, `/delete-git-worktree`, `/delete-projects`, `/delete-project-temp` — แต่ละ skill มี dry-run + confirm gate ของตัวเอง

## Execute

### 1. Identify Targets

> Goal: ระบุไฟล์และโฟลเดอร์ทีต้องลบ

1. รับรายการ targets จาก user
2. ตรวจสอบว่าเป็นชื่อ file หรือ directory จริง
3. ถ้าเป็น pattern หรือ glob → ขยายเป็นรายการ concrete files
4. บันทึก targets พร้อม absolute paths

### 2. Assess Impact

> Goal: รู้ว่าการลบกระทบอะไร

1. ทำ `/report` เพื่อสรุป state
2. ทำ `/scan-codebase` หรือ `/use-astgrep` เพื่อหา references ทีชี้มา targets
3. ตรวจสอบ `git status` ว่า targets ถูก track หรือ untracked
4. ระบุ broken refs ทีจะเกิดขึ้นหลังลบ
5. ถ้ามี reference มากหรือสำคัญ → ทำ `/ask-me` ก่อนดำเนินการ

### 3. Dry Run

> Goal: แสดงผลการลบก่อนจริง

1. แสดงรายการทีจะลบ
2. แสดง references ทีจะ broken
3. แสดงขนาดรวมและจำนวน files
4. ถาม user ว่า `proceed`, `skip`, หรือ `cancel`

### 4. Backup

> Goal: สำรองก่อนลบถ้าจำเป็น

1. ถ้า target อยู่ใน git → สามารถกู้คืนผ่าน git ได้ ไม่ต้อง backup เพิ่ม
2. ถ้า target ไม่อยู่ใน git หรือ uncommitted → สำรองไปยัง `%TEMP%` หรือ `.trash/`
3. บันทึก backup path

### 5. Delete

> Goal: ลบ targets ตามที confirm

1. ลบ files ด้วย `Remove-Item` หรือ `rm`
2. ถ้าเป็น directory → ลบ recursive ถ้า user confirm
3. ถ้า target ไม่อยู่หรือลบไม่ได้ → report error และ stop
4. ถ้ามี target สำคัญ (เช่น config, กุญแจ) → ต้อง double confirm

### 6. Update References

> Goal: แก้ไข references หลังลบ

1. ทำ `/update-references` เพื่ออัปเดตหรือลบ references ทีชี้มา targets
2. ทำ `/review-devin-global-harness` เพื่อตรวจว่าไม่มี broken refs เหลือ
3. ถ้ามี broken refs → แก้ไขหรือลบ (max 3 รอบ)

### 7. Validate

> Goal: ตรวจสอบหลังลบ

1. ตรวจสอบว่า targets ถูกลบจริง
2. ทำ `/run-check` เพื่อ lint, typecheck
3. ทำ `/review-devin-global-harness` อีกครั้ง
4. ถ้าไม่ผ่าน → ทำ `/resolve-errors` แล้ว retry

### 8. Report

> Goal: สรุปผลการลบ

1. รายงานรายการทีลบ
2. รายงาน references ทีแก้ไข
3. รายงาน broken refs ทีแก้ไขหรือค้าง
4. ทำ `/suggest-next-action` เพื่อแนะนำขั้นตอนถัดไป

## Rules

### 1. Never Delete Without Confirmation

- ต้อง dry-run และ confirm ก่อนลบเสมอ
- ไม่ลบ files นอก scope ที user ระบุ
- ไม่ลบ git history หรือ `.git`

### 2. Safety First

- ห้ามลบ files ทีมี secrets, API keys, credentials
- ถ้า target อยู่ใน global config (`~/.config`, `%APPDATA%`) → double confirm
- ถ้า target ใช้โดย process อื่น → หยุด process ก่อน

### 3. Update References

- ทุก reference ที broken ต้องถูกอัปเดตหรือลบ
- ไม่ปล่อยให้ imports, paths, links broken

### 4. Reversibility

- ถ้า target ไม่อยู่ใน git ต้อง backup ก่อนลบ
- บันทึก backup path ไว้ใน report

## Expected Outcome

- Targets ถูกลบตามทีระบุ
- ไม่มี broken refs ค้าง
- ผ่าน `/run-check` และ `/review-devin-global-harness`
- มีรายงานการลบและ references ทีอัปเดต
- สามารถ rollback ได้ถ้ามี backup
