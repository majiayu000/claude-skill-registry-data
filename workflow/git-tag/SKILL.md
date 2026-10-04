---
name: git-tag
description: จัดการ git tags — annotated release tags, semver, sync กับ manifest และ remote
argument-hint: "[create|list|push|delete] [version]"
related:
  - deep-review
  - git-push
  - git-commit
  - run-release
  - report
---

## Goal

สร้างและจัดการ git tags ถูก convention — annotated tags สำหรับ releases, semver ชัดเจน, sync กับ manifest version และ remote

## Scope

- create annotated/lightweight tags, list, push, delete (local + remote)
- เชื่อมกับ `/deep-review` — tag ต้องตรง `package.json`/manifest version
- ไม่ครอบคลุม full release process → `/run-release` (skill นี้จัดการ tag อย่างเดียว)

## Execute

### 1. Verify Version Target

> Goal: tag version ตรงกับ release จริง

1. ตรวจ version ใน manifest (`package.json`, `Cargo.toml`, `pyproject.toml`)
2. `git tag -l` + `git ls-remote --tags origin` — tag ยังไม่ซ้ำ, ไม่มี drift (`/deep-review`)
3. tag ต้องชี้ commit ที่ release จริง — ปกติ merge commit ของ release บน main

### 2. Create Tag

> Goal: tag มีข้อมูลครบและตาม convention

```bash
git tag -a v1.2.3 -m "Release v1.2.3"     # annotated — เลือกอันนี้สำหรับ releases เสมอ
git tag v1.2.3                             # lightweight — ใช้เฉพาะ temp/internal marker
git tag -a v1.2.3 <sha> -m "..."           # tag commit ย้อนหลัง
```

1. release tags ใช้ annotated (`-a`) เสมอ — มี tagger, date, message
2. ชื่อ tag ตรง version: `v<semver>` ตาม convention ของ project (เช็ค `git tag -l` ว่า prefix `v` หรือไม่)

### 3. Push And Sync

> Goal: tag ไปถึง remote และถูก CI release pipeline หยิบ

1. `git push origin <tag>` — push เฉพาะ tag ไม่ใช่ `--tags` ทั้งหมด (กัน tag local หลุด)
2. ตรวจ CI/release workflow trigger ถ้า project tag-driven (GitHub release, publish)
3. รายงาน: tag, commit, version, remote status

### 4. Fix Mistakes

> Goal: tag ผิดถูกแก้อย่างปลอดภัย

1. local เท่านั้น: `git tag -d <tag>` แล้วสร้างใหม่
2. pushed แล้ว: ห้าม move tag เงียบๆ — `git push origin :refs/tags/<tag>` ลบ remote, สร้างใหม่, push — แจ้งทีมเพราะ consumers อาจ pin tag อยู่

## Rules

- release tag = annotated เสมอ; lightweight เฉพาะ marker ชั่วคราว
- tag pushed แล้วถือเป็น immutable — move = breaking change สำหรับ consumers
- ชื่อ tag ต้องตรง manifest version — drift = `/deep-review` finding
- ไม่ push `--tags` ทั้งหมด — push เฉพาะ tag ที่ตั้งใจ
- ใช้ /deep-review ถ้าจำเป็น

## Expected Outcome

- Tag ถูกสร้าง ตรง version และ commit ที่ release
- Remote sync แล้ว ไม่มี tag drift
