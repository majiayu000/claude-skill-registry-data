---
name: run-verify
description: รัน verify แบบครบวงจรบน local หรือ CI/CD ตามขนาด project
argument-hint: "[scope]"
related:
  - deep-review
  - run-scan
  - run-lint
  - run-typecheck
  - run-test
  - run-build
  - implement-to-production
  - check-monorepo
  - setup-cicd
  - follow-tasks
  - ship-to-dev-branch
  - resolve-errors
  - report

---

## Goal

รัน verify แบบครบวงจร scan, format, lint, typecheck, test, build โดยเลือก local หรือ CI/CD ตามขนาด project

## Scope

ใช้เป็นจุดรวมเดียวสำหรับ verify ทั้งหมด
- project เล็ก ไม่หนัก RAM/compute ไม่ช้า → รันบน local ผ่าน package script `verify`
- project ใหญ่ monorepo หรือ build/test หนัก → ส่ง branch ไป CI/CD แล้ว watch และ resolve errors
- สามารถ force mode ได้: `/run-verify --local` หรือ `/run-verify --ci`
- ถ้าต้องการ end-to-end readiness gate (ก่อน ship/deploy หรือหลังงานใหญ่) → ทำ section `Deep Verify` ด้านล่างด้วย
- ไม่ merge, ไม่ release, ไม่ deploy โดยอัตโนมัติ
- ใช้หลัง `/implement-to-production` เพื่อ verify ก่อน ship

## Execute

> Pre-Run: ทำ `/deep-review` ก่อนเสมอ — `run-*` ต้อง review/ประเมินก่อนลงมือหลัก ห้ามข้าม; ถ้า findings เป็น blocker ให้แก้หรือ report ก่อนรัน (verify)

### 1. Detect Mode

> Goal: เลือก mode ตาม context

1. ถ้า user ระบุ `--local` → ใช้ local mode
2. ถ้า user ระบุ `--ci` หรือ `--ci-cd` → ใช้ CI/CD mode
3. ถ้าไม่ระบุ → ไปขั้น Auto Detect

### 2. Auto Detect Project Size

> Goal: ตัดสินใจว่า project เล็กหรือใหญ่

1. ตรวจสอบ signals ของ project ใหญ่:
   - ทำ `/check-monorepo` แล้วพบว่าเป็น monorepo
   - มี `workspaces` ใน `package.json`, `pnpm-workspace.yaml`, `moon.yml`, `turbo.json`
   - มีหลาย workspace/package หรือ build/test หนัก (เช่น >60 วินาที, กิน RAM/CPU มาก)
   - `AGENTS.md` หรือ user ระบุให้ใช้ CI verify
2. ถ้าพบ signal ใด signal หนึ่ง → CI/CD mode
3. ถ้าไม่พบ → local mode

### 3. Local Mode (Small Project)

> Goal: รัน verify บน local ผ่าน package manifest

1. อ่าน package manifest (`package.json`, `Cargo.toml`, etc.)
2. ถ้าไม่มี script `verify` → ทำ `/follow-tasks` เพื่อสร้าง `verify` = `scan + format + lint + typecheck + test + build` (format ก่อน lint)
3. ถ้า `verify` ไม่ครบ 6 ส่วน → ทำ `/follow-tasks` เพื่อเติม
4. รัน `verify` script บน local (เช่น `bun run verify`)
5. ถ้า fail → ทำ `/resolve-errors` แล้ว retry สูงสุด 3 ครั้ง

### 4. CI/CD Mode (Large Project)

> Goal: ส่ง branch ขึ้น CI/CD แล้ว watch

1. ทำ `git branch --show-current`, `git status`, `git log origin/<branch>..HEAD`
2. ถ้า working tree ไม่สะอาด → stop และ report
3. ถ้าไม่มี remote → stop และ report
4. ตรวจหา CI/CD config (`setup-cicd` รายการ); ถ้าไม่มี → ทำ `/setup-cicd`
5. ทำ `/git-push` ถ้ามี unpushed commits
6. ถ้า push ถูก reject → stop และ report (ไม่ force push)
7. ถ้าเป็น GitHub Actions → `/resolve-github-actions-fails` มิฉะนั้น `/resolve-cicd`
8. ถ้า fail → ทำ `/resolve-errors` แล้ว push ใหม่และ re-run สูงสุด 3 ครั้ง
9. ถ้า pass → report

### 5. Deep Verify (Readiness Gate)

> Goal: ยืนยัน project ทำงานได้จริง end-to-end — ใช้เมื่อ `--deep` หรือก่อน ship/deploy ใหญ่

1. Runtime gate: ทำ `/run-test` (e2e) ถ้ามี UI flows, `/check-open-ports` + smoke test entry points จริง, `/watch-browser-and-fix` จับ console/network errors ถ้ามี web URL
2. Usage gate: ทำ `/test-usage` ยืนยัน examples ใน README/docs ทำงานได้จริง
3. Deep validation: ทำ `/deep-validate` สำหรับ cross-reference, compliance, security ครั้งสุดท้าย; ถ้าพบ issues → `/deep-review-then-fix` แล้ว verify ใหม่
4. แต่ละ gate fail → fix แล้วเริ่ม gate นั้นใหม่ ไม่ข้าม; retry สูงสุด 3 ครั้ง → stop + report
5. ทำ `/report table` คอลัมน์: No., Gate, Result, Evidence, Fix ที่ทำ — สรุป ready / not-ready

### 6. Ship (If Requested)

> Goal: ส่งมอบงานหลัง verify ผ่าน

- ถ้า user ต้องการ ship ผลงานหลัง verify ผ่าน → ทำ `/ship-to-dev-branch` สำหรับ ship ทั้งหมด ตั้งแต่ verify, release, deploy, จนถึง rollback plan
- ทำ `/suggest-next-action` หลัง `/ship-to-dev-branch` เสร็จ

## Rules

### 1. Verify Only
- ไม่ merge, ไม่ release, ไม่ deploy
- ไม่ commit โดยอัตโนมัติ

### 2. Error Handling
- ใช้ `/resolve-errors` เมื่อพบ error
- retry สูงสุด 3 ครั้ง
- ถ้ายังไม่ผ่าน → stop และ report

### 3. Safety
- ไม่ force push
- ไม่ push ถ้า working tree ไม่สะอาด
- ไม่ hardcode secrets

### 4. Package Manifest
- small project ต้องมี `verify` = `scan + format + lint + typecheck + test + build` (format ก่อน lint)
- large project ใช้ CI/CD pipeline รัน full suite

- ใช้ /run-scan ถ้าจำเป็น
- ใช้ /run-lint ถ้าจำเป็น
- ใช้ /run-typecheck ถ้าจำเป็น
- ใช้ /run-test ถ้าจำเป็น
- ใช้ /run-build ถ้าจำเป็น
- ใช้ /deep-test coverage ถ้าจำเป็น
- ใช้ /run-test-all ถ้าจำเป็น
- ใช้ /ship-to-dev-branch ถ้าจำเป็น
- ใช้ /report ถ้าจำเป็น
- ใช้ /suggest-next-action ถ้าจำเป็น

## Expected Outcome

- small project: code ผ่าน scan, format, lint, typecheck, test, build บน local
- large project: branch ถูก push, CI/CD pipeline ผ่าน หรือมี root cause + next action ชัดเจน
- ไม่มี merge/release/deploy โดยอัตโนมัติ
