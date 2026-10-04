---
name: merge
description: merge ไฟล์หรือ folder เข้าด้วยกันและลบ source เดิม
argument-hint: "[domain] | @files [destination]"
allowed-tools:
  - read
  - edit
  - write
  - grep
  - find_file_by_name
  - exec
  - ask_user_question
  - todo_write
triggers:
  - user
  - model
related:
  - update-references
  - edit-relative
  - deep-validate
  - ask-me
  - deep-analyze
  - validate-then-apply
  - report
  - report-progress

---

## Goal

merge ไฟล์หรือโฟลเดอร์ต้นทางเข้าด้วยกันเป็นไฟล์หรือโฟลเดอร์ปลายทางเดียว แล้วลบ source เดิม

## Scope

ใช้เมื่อต้องรวมเนื้อหาจากหลายไฟล์หรือหลายโฟลเดอร์เข้าด้วยกัน และลบ source หลัง merge — หรือเมื่อต้องการ merge git branch/PR ตาม domain

- `git-branch` → merge feature branch เข้า target branch ด้วย `--no-ff`
- `github-pr` → merge pull request ด้วย strategy ที่เหมาะสม
- `all-branch-by-me-to-main` → merge ทุก branch ที่ user สร้างเข้า `main` แล้วลบ branch

## Execute

### 1. Identify Sources And Destination

> Goal: รู้ว่าอะไรคือ source และ destination

1. รับ `@files` เป็นรายการ source (ไฟล์หรือ folder) จาก argument หรือ context
2. รับ `destination` จาก prompt หรือ context
3. source อาจเป็นไฟล์หรือ folder หลายรายการ
4. destination อาจเป็นไฟล์ใหม่ ไฟล์เดิม หรือ folder เป้าหมาย
5. ถ้าไม่มี `@files` → ทำ `/ask-me` เพื่อขอรายการ source
6. ถ้าไม่ชัดเจน → ทำ `/ask-me` ก่อนดำเนินการ

### 2. Analyze Sources

> Goal: เข้าใจเนื้อหาก่อน merge

1. ทำ `/deep-analyze` กับแต่ละ source
2. ถ้า source เป็นโฟลเดอร์ → อ่านทุก `SKILL.md` หรือไฟล์หลักในโฟลเดอร์
3. บันทึกโครงสร้าง ความสัมพันธ์ และสิ่งทีซ้ำซ้อน

### 3. Plan Merge

> Goal: วางแผนการ merge อย่างปลอดภัย

1. ทำ `/validate-then-apply` เพื่อ validate ก่อน merge
2. ระบุ references ทีอ้างอิงถึง source
3. วางแผนการ update references ไปยัง destination
4. ถ้ามี references ซับซ้อน → ทำ `/update-references` ล่วงหน้า

### 4. Merge Content

> Goal: รวม source เข้าด้วยกันอย่างถูกต้อง

1. ถ้า source เป็นไฟล์ → อ่าน content ทั้งหมดแล้ว merge เข้า destination
2. ถ้า source เป็นโฟลเดอร์ → รวบรวมไฟล์สำคัญ ลบ redundancy แล้ว merge เนื้อหา
3. ใช้ `git mv` หรือ `git rm` ถ้าอยู่ใน git repo
4. ตรวจสอบว่า merge ถูกต้องและไม่มี data loss

### 5. Delete Old Sources

> Goal: ลบ source เดิมหลัง merge

1. ลบไฟล์หรือโฟลเดอร์ source เดิมหลัง merge สำเร็จ
2. ใช้ `git rm -r` สำหรับโฟลเดอร์ หรือ `git rm` สำหรับไฟล์
3. ตรวจสอบว่าไม่มี references เก่าเหลือถ้า source ถูก reference

### 6. Update References

> Goal: ไม่ให้มี broken references จาก source ทีถูกลบ

1. ทำ `/update-references` เพื่ออัปเดตทุก skills ทีอ้างอิงถึง source
2. ทำ `/edit-relative` เมื่อ merge กระทบ relative paths, imports, markdown links หรือ semantic references (skill names, `related` lists) ของไฟล์อื่น — ครอบคลุมทั้ง path-level และ symbol-level updates
3. ตรวจหา skills ที่เกี่ยวกับ file ops (`move-to`, `rename`, `all-this-patterns`, `edit-only`, `refactor`, `flatten-directory`) และอัปเดต references ให้ชี้ไป destination
4. ใช้ `grep` ตรวจซ้ำเพื่อหา reference เก่าทีหลงเหลือ

### 7. Validate

> Goal: ตรวจสอบความถูกต้อง

1. ทำ `/deep-validate` เพื่อตรวจ merge
2. ตรวจหา broken references
3. ตรวจ data loss
4. ทำ `/report table` สรุป: `No.`, `Source`, `Destination`, `Status`, `Notes`
5. ถ้ามีหลาย step ค้าง → ทำ `/report-progress`

### Skills

> Goal: dispatch ไป skill ปลายทาง ตาม domain เมื่อ merge เป็น git branch/PR workflow

| Domain | Skill |
|--------|----------|
| `github-pr` | /merge-github-pr — merge PR ด้วย strategy ที่เหมาะสม |
| `all-branch-by-me-to-main` | /merge-all-branch-by-me-to-main — merge ทุก branch ของ user เข้า `main` |

1. ถ้า argument ตรง domain ในตาราง → อ่าน `/merge-<domain>` แล้วทำตาม flow ในนั้น — ไม่ execute จากตารางนี้โดยตรง
2. ถ้าเป็น `@files` merge → ทำตาม step 1-7 ด้านบน

## Rules

- ตรวจสอบ merge ถูกต้องก่อนลบ source
- รองรับทั้งไฟล์และโฟลเดอร์เป็น source
- ใช้ git สำหรับ file operations ถ้าเป็นไปได้
- ถ้ามี references ชี้ไปยัง source → ทำ `/update-references` ก่อนลบ
- ถ้าต้องตัดสินใจระหว่างหลายตัวเลือก → ทำ `/deep-validate` แล้วเลือกสิ่งทีดีทีสุด
- ทุก merge ต้องผ่าน `/validate-then-apply` ก่อน

## Expected Outcome

- ไฟล์หรือโฟลเดอร์ถูก merge เข้าด้วยกัน
- source เดิมถูกลบ
- ไม่มี data loss
- ไม่มี broken references
