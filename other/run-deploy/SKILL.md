---
name: run-deploy
description: Deploy application ไปยัง platform ที่กำหนด พร้อม commit, push และ watch จน live
argument-hint: "[scope]"
related:
  - follow-secret-manager
  - open-web-for-config-secret
  - deep-review
  - resolve-errors
  - resolve-cicd
  - run-verify
  - run-build
  - follow-tool-vite
  - follow-create-plugins
  - deploy-to-vercel
  - deploy-to-cloudflare
  - deploy-to-railway
  - create-cloudflare

---

## Goal

Deploy application ไปยัง platform ที่กำหนด พร้อม post-deploy validation, commit/push และ watch browser จนกว่า deployment จะ live

## Scope
- สำหรับ skills ที่เกี่ยวข้อง: `open-web-for-config-secret`, `deep-review`

ครอบคลุมการ verify, build, deploy, commit/push, post-deploy validation, watch until live และ rollback & recovery

## Execute

> Pre-Run: ทำ `/deep-review` ก่อนเสมอ — `run-*` ต้อง review/ประเมินก่อนลงมือหลัก ห้ามข้าม; ถ้า findings เป็น blocker ให้แก้หรือ report ก่อนรัน (deploy)

### 1. Verify

> Goal: Verify

ตรวจสอบคุณภาพโค้ดก่อน deploy

1. ทำ `/run-verify` เพื่อตรวจสอบคุณภาพโค้ด
2. ตรวจสอบว่า verify สำเร็จ
3. ตรวจสอบว่าไม่มี error หรือ warning ที่สำคัญ

### 2. Build Application

> Goal: Build Application

Build application สำหรับ deployment

1. ทำ `/run-build` เพื่อ build application
2. ตรวจสอบว่า build สำเร็จ
3. ตรวจสอบ artifacts ที่สร้าง

### 3. Deploy

> Goal: Deploy

Deploy application ตาม platform ที่ใช้

1. สำหรับ Vercel: ทำ `/deploy-to-vercel`
2. สำหรับ Cloudflare:
   - ถ้า Worker project ยังไม่ถูกสร้าง → ทำ `/create-cloudflare-worker` ก่อน
   - จากนั้นทำ `/deploy-to-cloudflare`
3. สำหรับ Railway: ทำ `/deploy-to-railway`
4. สำหรับ platform อื่น: ทำตาม workflow ที่เกี่ยวข้อง
5. ตรวจสอบว่า deploy สำเร็จ

### 4. Commit And Push

> Goal: Commit And Push

Commit และ push changes ไปยัง repository

1. ทำ `/git-commit`
2. ทำ `/git-push`

### 5. Verify Deployment

> Goal: Verify Deployment

ตรวจสอบว่า deployment ทำงานได้

1. เปิด URL ของ deployment
2. ตรวจสอบว่า application ทำงานได้
3. ตรวจสอบ logs ว่าไม่มี error
4. ทำ `/watch-browser-and-fix` ถ้ามี URL

### 6. Watch Until Live

> Goal: Watch Until Live

Watch deployment ด้วย browser จนกว่าจะ live

1. ทำ `/watch-browser-and-fix` ด้วย deployment URL
2. ตรวจสอบว่า page load สำเร็จ
3. ตรวจสอบ console errors และ network errors
4. ทำ `/resolve-errors` ถ้าพบปัญหา
5. ทำ `/loop-until-complete` จนกว่า deployment live สำเร็จ

### 7. Post-Deploy Validation

> Goal: Post-Deploy Validation

ตรวจสอบ deployment อย่างละเอียดหลัง deploy (ดู `references/post-deploy-validation.md`)

1. ทำ `/run-test` (e2e) เพื่อทดสอบ critical paths หลัง deploy
2. ตรวจสอบ health endpoint และ readiness probes
3. ตรวจสอบ error logs หลัง deploy 5-10 นาที
4. ถ้าพบ critical errors → ทำ rollback ทันที (ดู `references/rollback-recovery.md`)

### 8. Rollback And Recovery

> Goal: Rollback And Recovery

เตรียม rollback procedure และตรวจสอบ backup (ดู `references/rollback-recovery.md`)

1. ทำ `/deep-review` เพื่อตรวจสอบ backup strategy ก่อน deploy
2. เตรียม rollback procedure ชัดเจนก่อน deploy
3. ถ้า deploy ล้มเหลว → rollback ทันทีและทำ `/resolve-errors`

## Rules

### 1. Verify

- ต้อง verify สำเร็จก่อน build
- ใช้ `/run-verify` สำหรับ verify
- ไม่มี error หรือ warning ที่สำคัญ

### 2. Build

- ต้อง build สำเร็จก่อน deploy
- Artifacts ต้องถูกต้อง
- ใช้ `/run-build` สำหรับ build

### 3. Deploy

- ใช้ `/follow-secret-manager` สำหรับจัดการ secrets และ API tokens ก่อน deploy
- ใช้ `/deploy-to-<platform>` ตาม platform ที่เลือก
- ต้อง deploy สำเร็จ
- ตรวจสอบ deployment status
- ถ้า deploy ไป Cloudflare และ deploy ไม่ผ่าน ให้ทำ `/resolve-cicd` เพื่อ watch และ fix จนกว่าจะผ่าน

### 4. Commit And Push

- Deploy ก่อน commit/push ถ้าจำเป็น
- Commit/push หลังจาก deploy สำเร็จ
- Watch browser หลังจากได้ deployment URL

### 5. Watch Until Live

- ใช้ `/watch-browser-and-fix` สำหรับ monitoring
- ใช้ `/resolve-errors` เมื่อพบปัญหา
- ตรวจสอบ console และ network errors
- ทำ `/loop-until-complete` จนกว่า deployment live

### 6. Post-Deploy Validation

- ต้องทดสอบ critical paths หลัง deploy
- ต้องตรวจสอบ health endpoint
- ต้องตรวจสอบ error logs หลัง deploy 5-10 นาที
- ถ้าพบ critical errors ให้ rollback ทันที

### 7. Rollback And Recovery

- ต้องเตรียม rollback procedure ก่อน deploy
- ต้องตรวจสอบ backup strategy ก่อน deploy
- ถ้า deploy ล้มเหลว ให้ rollback ทันที
- ต้องมี zero-downtime deploy (ถ้าต้องการ)

- ใช้ /follow-tool-vite ถ้าจำเป็น
- ใช้ /follow-create-plugins (vite) ถ้าจำเป็น (deploy)

## Expected Outcome

- Application ถูก deploy สำเร็จ
- Changes committed และ pushed แล้ว
- URL สามารถเข้าถึงได้
- Application ทำงานได้ปกติ
- ไม่มี console หรือ network errors
- Post-deploy validation ผ่าน (smoke test, health check, logs)
- Rollback procedure พร้อมใช้งาน
- Backup strategy ถูกตรวจสอบก่อน deploy