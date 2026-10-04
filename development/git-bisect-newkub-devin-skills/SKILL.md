---
name: git-bisect
description: Binary search หา commit ที่ทำให้ bug เกิด — manual marks หรือ bisect run script
argument-hint: "[<good-sha> <bad-sha>|run <script>]"
related:
  - deep-debug
  - check-git-logs
  - git-file-history
  - run-test
  - resolve-errors
---

## Goal

หา commit ที่ introduce bug ด้วย `git bisect` — binary search ลดจาก N commits เหลือ ~log2(N) checks

## Scope

- manual bisect (`start`, `good`, `bad`) และ automated (`bisect run <script>`)
- ใช้เมื่อรู้ว่า bug ไม่มีใน commit A แต่มีใน commit B แล้วอยากหาตัวแปลง
- คู่กับ `/deep-debug` — bisect หา culprit commit, debug หา root cause ใน commit นั้น

## Execute

### 1. Establish Range

> Goal: มี good/bad boundary ที่ verify แล้วจริง

1. หา `bad` commit (ปกติ HEAD): ยืนยัน bug reproduce ได้
2. หา `good` commit: tag/release เก่าหรือ commit ที่ bug ยังไม่มี — ต้อง verify จริงก่อนเริ่ม ไม่เดา
3. `git bisect start <bad> <good>` — git checkout commit กลางทางให้เอง

### 2. Mark Each Check

> Goal: แต่ละ step ตัด search space ครึ่งหนึ่ง

1. Reproduce test ที่ commit ปัจจุบัน → `git bisect good` หรือ `git bisect bad`
2. commit ที่เทสไม่ได้ (build พัง ฯลฯ) → `git bisect skip`
3. ทำซ้ำจน git บอก culprit: `<sha> is the first bad commit`

### 3. Automate With bisect run

> Goal: bisect อัตโนมัติเมื่อเทส scriptable ได้

```bash
git bisect start <bad> <good>
git bisect run <test-command>     # exit 0=good, 1-124/126-127=bad, 125=skip
git bisect run bun test path/to/specific.test.ts
```

1. test command ต้อง exit code ถูกต้อง — เขียน script สั้นที่ wrap ถ้าจำเป็น
2. จำกัด scope เทสให้เล็ก (เทสเดียว/คำสั่งเดียว) — bisect รันหลายครั้ง

### 4. Conclude

> Goal: ได้ culprit commit และกลับสู่ state ปกติ

1. `git show <culprit>` — ดู change ที่ก่อ bug
2. `git bisect reset` — กลับ branch เดิมเสมอ (ห้ามลืม — detached HEAD ค้างทำงานต่อพลาด)
3. ต่อด้วย `/deep-debug` หา root cause ใน culprit หรือ `/git-revert` ถ้าต้อง rollback

## Rules

- verify `good` จริงก่อนเริ่ม — good ผิด = bisect ชี้ผิดทั้งรัน
- `bisect run` ต้อง deterministic — flaky test ทำ bisect หลอก → แก้ flakiness ก่อน
- `git bisect reset` ทุกครั้งหลังจบ — ไม่ว่าจบปกติหรือ abort
- ใช้ /deep-debug ถ้าจำเป็น

## Expected Outcome

- ระบุ culprit commit พร้อม `git show` evidence ใน ~log2(N) checks
- Repo กลับสู่ branch เดิม (`bisect reset`) พร้อมทำ fix ต่อ
