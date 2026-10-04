---
name: run-review
description: alias → /update-review-cli-then-run (รัน review CLI วิเคราะห์ผล และแนะนำ action items)
argument-hint: "[target]"
related:
  - update-review-cli-then-run
  - deep-review
  - run-verify
  - suggest-next-action
---

## Goal

Alias ของ `/update-review-cli-then-run` — รัน `tools/review-codebase` CLI วิเคราะห์ผล และแนะนำ action items ตาม findings

## Scope

ใช้เมื่อ user เรียก `/run-review` — skill นี้เป็น alias stub เท่านั้น workflow จริงอยู่ใน `update-review-cli-then-run`

## Execute

ทำ `/update-review-cli-then-run` เต็ม workflow — run path คือ Steps 7-10 (Validate CLI → Run Review And Analyze → Verify And Follow Tasks → Report And Suggest Actions); ถ้าต้อง update CLI ก่อนให้เริ่ม Steps 1-6

- ถ้าต้องแก้ไข analyzer logic → `/update-create-analyze-cli` ก่อน แล้วกลับมาทำ skill นี้
- Known Issues อยู่ใน `update-review-cli-then-run/references/known-issues.md` เท่านั้น (single source)

## Rules

- ห้าม duplicate workflow ของ `/update-review-cli-then-run` ในไฟล์นี้
- ถ้า alias ขาด steps → อ่าน `update-review-cli-then-run/SKILL.md` เสมอ
- ถ้าต้อง review กว้างกว่า CLI → ใช้ `/deep-review`; ถ้าเจาะ `.devin` ใช้ `/deep-review`
- verify ผลหลัง review ด้วย `/run-verify` แล้วปิดท้ายด้วย `/suggest-next-action`

## Expected Outcome

- `/update-review-cli-then-run` ถูก execute ครบตาม run path พร้อม action items จาก findings
