---
name: match
description: หา match items จาก codebase แล้ว apply rules ที่ผู้ใช้กำหนดให้กับแต่ละ match
argument-hint: "<what-to-match>"
allowed-tools:
  - read
  - grep
  - find_file_by_name
  - exec
  - ask_user_question
  - skill
  - run_subagent
  - todo_write
  - use-astgrep
triggers:
  - user
  - model
related:
  - scan-codebase
  - search-in-git
  - ask-me
  - follow-your-suggestion
  - use-scripts
  - plan
  - deep-validate
---

## Goal

หา match items ใน workspace หรือ skill set แล้วนำเสนอพร้อมหลักฐาน จากนั้นให้ผู้ใช้กำหนด conditional rules แล้ว apply rule ให้กับแต่ละ matched item โดยอัตโนมัติ

## Scope

ใช้เมื่อผู้ใช้พูดในลักษณะ "find X, then do Y if A, do Z if B" หรือต้องการรัน rule-based batch operation บนชุด items ที่ค้นพบ ใช้ได้กับ files, code symbols, skills, dependencies หรือ searchable target ใดๆ

ดูเพิ่มเติม: /search-in-git, /report-file-structure, /ask-me, /follow-your-suggestion, /use-scripts, /plan

## Execute

### 1. Identify What To Match

> Goal: Identify What To Match

1. รับ match target จาก argument หรือ context.
2. ตัวอย่าง: `*.test.ts`, `skills with TODO`, `functions longer than 50 lines`, `packages with no tests`.
3. ถ้า target คลุมเครือ ให้ถามหา concrete pattern หรือ example.
4. บันทึก matching criteria ลงใน `todo_write`.

### 2. Match Items

> Goal: Match Items

หา items ทั้งหมดที่ตรงกับ criteria.

1. ใช้ `find_file_by_name` สำหรับ file patterns.
2. ใช้ `grep` สำหรับ text patterns.
3. ใช้ `use-astgrep` สำหรับ AST-based code patterns.
4. ใช้ `scan-codebase` สำหรับการค้นหาที่กว้างหรือมีหลาย criteria.
5. จำกัดผลลัพธ์ให้เหมาะสม; ถ้ามากเกินไป ให้แสดงสรุปแล้วถามก่อนขยาย.

### 3. Present Matches

> Goal: Present Matches

แสดง match items เป็นรายการลำดับเลขพร้อมหลักฐาน.

1. ลำดับเลขแต่ละ item เริ่มจาก 1.
2. แสดง identifier ที่เกี่ยวข้อง: path, symbol, skill name หรือ code snippet.
3. รวม match attribute ที่จะใช้สำหรับ rules เช่น:
   - file extension
   - directory
   - content snippet
   - size หรือ line count
4. ถามผู้ใช้ว่า match set ถูกต้องหรือไม่ก่อน apply rules.

### 4. Collect Rules

> Goal: Collect Rules

รับ conditional rules จากผู้ใช้.

1. ถามผู้ใช้สำหรับ rules ในรูปแบบ: `if <condition> => <action>`.
2. ยอมรับหลาย rules ในข้อความเดียว.
3. รองรับ default rule: `else => <action>`.
4. Conditions สามารถใช้ attributes ที่เปิดเผยในขั้นตอนที่ 3 เช่น:
   - `ext == .ts`
   - `path contains packages/`
   - `size > 1000`
   - `content contains TODO`
5. Actions สามารถเป็น skills, commands หรือ instructions เช่น:
   - `review`
   - `refactor`
   - `delete`
   - `update-references`
   - `add tests`
   - `skip`
6. ถ้า action เป็น destructive หรือ irreversible ให้เตือนแล้วถามยืนยัน.

### 5. Apply Rules

> Goal: Apply Rules

รัน action ที่ตรงกันให้แต่ละ item.

1. วนซ้ำรายการ match ตามลำดับเลข.
2. สำหรับแต่ละ item ประเมิน rules จากบนลงล่าง.
3. Execute action แรกที่ตรงกัน.
4. ถ้าไม่มี rule ตรงกัน ให้ apply default rule หรือ skip.
5. บันทึกสิ่งที่ทำสำหรับแต่ละ item.
6. หยุดแล้วถามหาก action ที่รุนแรงหรือ irreversible กำลังจะรัน.

### 6. Report And Validate

> Goal: Report And Validate

รายงานผลลัพธ์และตรวจสอบความถูกต้อง.

1. แสดงตารางที่มีคอลัมน์: No., item, matched rule, action, status.
2. รัน `deep-validate` ถ้า actions เปลี่ยน code หรือ skills.
3. รัน `run-verify` สำหรับ lint, typecheck หรือ tests เมื่อเกี่ยวข้อง.
4. รายการ items ใดที่ประมวลผลไม่ได้ พร้อมเหตุผล.

## Rules

### 1. Match Before Act

- ต้องหาและนำเสนอ matches ก่อนจึง apply rules.
- อย่าสมมติว่าผู้ใช้ต้องการ action เดียวกันทุก item.
- ยืนยัน match set เว้นแต่ผู้ใช้จะไว้วางใจ criteria อย่างชัดเจน.

### 2. Rule Clarity

- แต่ละ rule ต้องมี condition และ action อย่างละหนึ่ง.
- Conditions ต้องอ้างอิง match attribute.
- Actions ต้องเป็น known skill, command หรือคำสั่งที่ชัดเจน.
- ถ้า rule คลุมเครือ ให้ถามผู้ใช้ให้ชัดเจน.

### 3. Safety

- Destructive actions ต้องมี user confirmation ก่อน execution.
- รองรับ dry-run ก่อนเมื่อถูกขอหรือเมื่อ action มีความเสี่ยง.
- อย่ารัน actions ที่กระทบ secrets, credentials หรือ remote systems โดยไม่มี confirmation.

### 4. Ordering

- Rules ถูกประเมินตามลำดับที่ผู้ใช้ให้มา.
- Rule แรกที่ตรงกันใช้ได้.
- ถ้าไม่มี rule ตรงกัน ให้ใช้ default rule หรือรายงาน "no match".

### 5. Evidence

- ทุก match ต้องมีหลักฐาน: path, snippet, line number หรือ attribute.
- ทุก applied action ต้องถูกบันทึกใน report.
- ถ้า action ล้มเหลว ให้บันทึก error แล้วทำต่อกับ item ถัดไป เว้นแต่จะถูกบอกให้หยุด.

## Expected Outcome

- แสดงรายการ match items แบบลำดับเลขก่อนที่ action ใดจะรัน.
- User rules ถูก apply เป็นระบบต่อแต่ละ matched item.
- Report แสดง rule ใดตรงกันและผลลัพธ์ของแต่ละ item.
- Code หรือ skills ยังคง valid หาก validation เกี่ยวข้อง.
