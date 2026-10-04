---

name: search-npmx
description: ค้นหา เปรียบเทียบ และประเมิน npm packages บน npmx.dev
argument-hint: "[package-query]"
related:
  - follow-best-practice
  - follow-tool-crw
  - learn
  - use-my-packages-on-registry
  - deep-review
  - ask-me
  - run-install
---

## Goal

ใช้ `npmx.dev` ค้นหา เปรียบเทียบ และเลือก `npm packages` ทีเหมาะสมกับ project โดยดูข้อมูลแบบ `package details`, `versions`, `dependencies`, `docs`, `changelog`, `stats`, `security` และ `source code`

## Scope

ใช้ `npmx.dev` เท่านั้น (ไม่ใช่ `npmjs.com` หรือ CLI search) สำหรับหา package ตาม requirement แล้วสรุปเป้นตารางเปรียบเทียบ ไม่รวมการติดตั้งหรือ implement ใน project

## Execute

### 1. Clarify Search

> Goal: เข้าใจสิ่งที่ user ต้องการ

1. รับ `package-query` จาก argument หรือ context — เช่น ชื่อ package, keyword, หรือ feature
2. ถ้าไม่ชัด → ทำ `/ask-me` ถามเพิ่ม:
   - ใช้ทำอะไร? (state management, router, UI, etc.)
   - ต้องเป็น TypeScript และ ESM ไหม?
   - มีข้อจำกัดเรื่องขนาดหรือ license ไหม?
   - ต้องเปรียบเทียบกับตัวเลือกอื่นไหม?

### 2. Build Search URL

> Goal: ได้ URL ทีถูกต้องของ npmx.dev

1. ถ้าค้นหาด้วย keyword → `https://npmx.dev/search?q=<query>`
2. ถ้ารู้ชื่อ package ทันที → `https://npmx.dev/<package>` หรือ `https://npmx.dev/package/<package>`
3. ถ้าเป้น scoped package → `https://npmx.dev/@scope/name`
4. ถ้าต้องการ version ชัดเจน → `https://npmx.dev/<package>@<version>` หรือ `https://npmx.dev/package/<package>/v/<version>`
5. ถ้าต้องการ compare → `https://npmx.dev/compare?packages=<pkg1>,<pkg2>`
6. ใช้ `/` บน npmx.dev เพื่อ focus search bar

### 3. Evaluate Candidates

> Goal: รวบรวมข้อมูลเพียงพอเพื่อตัดสินใจ

1. เปิดหน้า package ด้วย `crw_scrape` หรือ `follow-tool-crw`
2. อ่าน `README` — สรุป purpose, quick start, caveats
3. ดู `Versions` — latest, release cadence, deprecated versions
4. ดู `Dependencies` — count, มี peer deps หรือ native deps หรือไม่
5. ดู `Code` (กด `.`) — โครงสร้างไฟล์, entry points, source quality
6. ดู `Docs` — มี generated API docs หรือไม่
7. ดู `Changelog` — มี release notes หรือไม่
8. ดู `Stats` — downloads, install size, repository stars/forks
9. ดู `security` badges — vulnerabilities, provenance, license change warnings
10. บันทึก URL ทีตรวจสอบไว้ทุกครั้ง

### 4. Compare Packages

> Goal: เลือกตัวทีดีทีสุดเมื่อมีหลายตัวเลือก

1. ถ้ามี 2-3 ตัวเลือก → ใช้ `/compare?packages=<a>,<b>` บน npmx.dev
2. สร้างตารางเปรียบเทียบด้วย column:
   - ชื่อ + version
   - ขนาด (publish/install size)
   - จำนวน dependencies
   - รองรับ TypeScript / ESM / CJS
   - license
   - provenance
   - สถานะ security (vulnerabilities)
   - downloads ต่อสัปดาห์
   - last published
   - ข้อดี/ข้อเสีย
3. หา native/smaller/safer alternatives จาก `Module replacement suggestions` ถ้า npmx แสดง
4. ทำ `/follow-best-practice` ถ้า category นี้มี best practice เฉพาะ

### 5. Recommend

> Goal: สรุปผลและชี้ไปยัง URL

1. เลือก package ทีดีทีสุดตาม criteria
2. ระบุ exact version ทีแนะนำให้ pin
3. ให้ URL ที share ได้ เช่น `https://npmx.dev/<package>@<version>`
4. ถ้าไม่แน่ใจ → ทำ `/ask-me` ก่อนตัดสินใจ
5. ถ้าต้องใช้ package ใน project → ส่งต่อ `/use-my-packages-on-registry` หรือ `/deep-review`

## Rules

### 1. URL Conventions

- ใช้ `https://npmx.dev/<package>` สำหรับ package ทั่วไป
- ใช้ `https://npmx.dev/package/<package>/v/<version>` สำหรับ version ชัดเจน
- ใช้ `https://npmx.dev/search?q=<query>` สำหรับค้นหา
- ใช้ `https://npmx.dev/compare?packages=<a>,<b>` สำหรับเปรียบเทียบ
- ใช้ `https://npmx.dev/~<username>` สำหรับดู packages ของ user
- ใช้ `https://npmx.dev/@<org>` สำหรับดู packages ของ org
- npmx.dev URLs แทนที่ `npmjs.com` ได้โดยตรง (replace domain)

### 2. Keyboard Shortcuts

- `/` — focus search bar
- `Ctrl+K` / `⌘K` — open command palette
- `.` — open code viewer
- `d` — open docs
- `c` — compare package
- `-` — open changelog
- `t` — open timeline
- `s` — open stats

### 3. Selection Criteria

- ลำดับความสำคัญ: TypeScript types > ESM support > ขนาดเล็ก > provenance > active maintenance
- หลีกเลี่ยง packages ทีมี deprecation หรือ vulnerability
- หลีกเลี่ยง `latest` ใน production — แนะนำ pin exact version
- ตรวจสอบ license ก่อนใช้ใน project ที่มีข้อจำกัด

### 4. Tools

- ใช้ `follow-tool-crw` หรือ `crw_scrape` เพื่อดึงข้อมูลจาก npmx.dev
- ใช้ `follow-tool-crw` ถ้าต้องหา context เพิ่มเติม
- ใช้ `learn` (web) ถ้าต้องอ่าน docs นอก npmx
- ใช้ `deep-review` ถ้าต้อง audit ลึก

### 5. Safety

- ไม่ install package ด้วยตัวเอง (skill นี้ทำเฉพาะ research)
- ไม่ expose API key หรือ registry token
- ไม่สร้าง file ใดๆ ใน project target นอกจาก report ใน chat
- ใช้ /run-install ถ้าจำเป็น

## Expected Outcome

- ได้ package ทีเหมาะสมพร้อมเหตุผล
- มีตารางเปรียบเทียบ (ถ้ามีหลายตัวเลือก)
- มี exact npmx.dev URL สำหรับ package และ version ทีแนะนำ
- มีข้อมูลขนาด, dependencies, license, security, และ maintenance status
