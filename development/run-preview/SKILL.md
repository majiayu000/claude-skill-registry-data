---
name: run-preview
description: รัน preview build เพื่อทดสอบก่อน deploy จริง
argument-hint: "[scope]"
related:
  - deep-review
  - run-build
  - watch-browser
  - run-test
  - report
  - resolve-errors
  - run-deploy
  - run-dev
  - run-review
---

## Goal

รัน preview build เพื่อทดสอบก่อน deploy จริง ครอบคลุม build, start server, test, verify และ share preview

## Scope

ใช้สำหรับ preview ทุกประเภททั้ง local preview server และ deployment preview (Vercel, Cloudflare, Netlify) ก่อน deploy จริง

## Execute

> Pre-Run: ทำ `/deep-review` ก่อนเสมอ — `run-*` ต้อง review/ประเมินก่อนลงมือหลัก ห้ามข้าม; ถ้า findings เป็น blocker ให้แก้หรือ report ก่อนรัน (preview)

### 1. Build Preview

> Goal: Build Preview

สร้าง preview build สำหรับทดสอบ

1. ทำ `/run-build` เพื่อสร้าง preview build
2. ตั้งค่า build mode เป็น preview ไม่ใช่ production
3. ตรวจสอบ build output ว่าไม่มี errors
4. ถ้าเป็น Vite: ใช้ `bun run build` แล้ว `bun run preview`
5. ถ้าเป็น Next.js: ใช้ `bun run build` แล้ว `bun run start`
6. ถ้าเป็น Nuxt: ใช้ `bun run build` แล้ว `bun run preview`
7. ถ้าเป็น Vercel: ใช้ `bunx vercel preview` สำหรับ deployment preview
8. ถ้าเป็น Cloudflare: ใช้ `bunx wrangler pages dev` สำหรับ local preview

### 2. Start Preview Server

> Goal: Start Preview Server

รัน preview server ตาม framework

1. รัน preview server command ตาม framework ที่ใช้
2. ตรวจสอบว่า server ทำงานโดยดู console output
3. บันทึก preview URL (local หรือ deployment URL)
4. ถ้าเป็น deployment preview ให้รอจนกว่า URL จะพร้อม

### 3. Test Preview

> Goal: Test Preview

ทดสอบ preview ใน browser

1. เปิด preview URL ใน browser
2. ทำ `/watch-browser-and-fix` เพื่อตรวจสอบหน้าเว็บต่อเนื่อง
3. ทดสอบ features สำคัญที่เปลี่ยนแปลงล่าสุด
4. ตรวจสอบ console errors และ warnings
5. ทำ `/run-test` สำหรับทดสอบแบบละเอียด

### 4. Verify Preview

> Goal: Verify Preview

ตรวจสอบความถูกต้องของ preview

1. ตรวจสอบว่า pages โหลดถูกต้องทุกหน้า
2. ตรวจสอบ assets และ static files โหลดครบ
3. ทดสอบ critical user flows สำคัญ
4. ตรวจสอบ responsive design บนหลาย screen sizes
5. ตรวจสอบ API endpoints ทำงานถูกต้อง (ถ้ามี)
6. ตรวจสอบ environment variables ถูกต้องสำหรับ preview

### 5. Report Issues

> Goal: Report Issues

รายงาน issues ที่พบในรูปแบบตาราง

1. ทำ `/report` เพื่อจัดรูปแบบตาราง
2. สร้างตารางพร้อม columns: Category, Issue, Severity, Location, Action Required
3. หมวดหมู่: Build, Pages, Assets, API, Console Errors, Responsive
4. จัดลำดับ issues ตาม severity (critical, high, medium, low)

### 6. Share Preview

> Goal: Share Preview

แชร์ preview ให้ทีมและรวบรวม feedback

1. แชร์ preview URL ให้ทีม
2. รวบรวม feedback และบันทึก issues ที่พบ
3. ถ้ามี issues ให้ทำ `/resolve-errors` แล้ว rebuild preview
4. ถ้าทุกอย่างผ่าน ให้ทำ `/run-deploy` เพื่อ deploy จริง

## Rules

- ใช้ preview build mode ไม่ใช่ production
- ตั้งค่า environment variables สำหรับ preview แยกจาก production
- ใช้ preview database หรือ staging database หากจำเป็น
- ทดสอบ features ที่เปลี่ยนแปลงล่าสุดก่อน
- ทดสอบ critical user flows ทุกครั้ง
- ทดสอบ responsive design บนหลาย screen sizes
- ใช้ `/watch-browser-and-fix` สำหรับตรวจสอบต่อเนื่อง
- ใช้ `/run-test` สำหรับทดสอบแบบละเอียด
- ใช้ `/report` สำหรับรายงาน issues
- Preview server ควรหยุดเมื่อไม่ใช้งาน
- ลบ preview builds เก่าเป็นระยะ
- ใช้ preview URLs ชั่วคราว ห้ามใช้เป็น production
- ถ้ามี issues ให้แก้ก่อน deploy จริง
- ถ้าเป็น deployment preview ให้รอจนกว่า URL จะพร้อมก่อนทดสอบ

## Common Mistakes

- ใช้ production build แทน preview build
- ไม่ตั้งค่า environment variables สำหรับ preview
- ทดสอบเฉพาะหน้าที่เปลี่ยน ไม่ทดสอบ critical flows
- ไม่ตรวจสอบ console errors
- ลืมหยุด preview server เมื่อไม่ใช้งาน
- ใช้ preview URL เป็น production

## Anti-Patterns

- Deploy จริงโดยไม่ผ่าน preview ก่อน
- ใช้ production database สำหรับ preview
- ละเว้น responsive design testing
- ไม่รายงาน issues ที่พบใน preview
- ข้าม API testing ใน preview
- ใช้ /run-dev ถ้าจำเป็น
- ใช้ /run-review ถ้าจำเป็น

## Expected Outcome

- Preview build สำเร็จไม่มี errors
- Preview server ทำงานได้
- Features ทำงานถูกต้องใน preview
- Console ไม่มี errors หรือ warnings
- Responsive design ทำงานบนทุก screen sizes
- Issues ถูกระบุ รายงานในตาราง และแก้ไขก่อน deploy
- Feedback จากทีมถูกรวบรวม
- พร้อมสำหรับ `/run-deploy` เพื่อ deploy จริง
