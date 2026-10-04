---
name: learn
description: เรียนรู้ concept, tool, หรือ library อย่างเป็นระบบ ด้วย research และ practice
argument-hint: "[topic]"
related:
  - deep-research
  - follow-best-practice
  - update-examples

---

## Goal

เรียนรู้ concept, tool, หรือ library อย่างเป็นระบบ โดยใช้ research และ practice เพื่อให้เข้าใจอย่างลึกซึ้ง

## Scope

ใช้สำหรับเรียนรู้สิ่งใหม่ ไม่ว่าจะเป็น concept, tool, library, framework, หรือ codebase

## Execute

### Learn Skills

| Topic | Skill |
|-------|-------|
| Web / Docs | `/learn-from-web` — เรียนรู้จาก official docs (DeepWiki, Context7, Web Search) แล้วเขียน content ครอบคลุม |
| CLI tool | `/learn-from-cli` — command surface จาก `--help`, subcommands, binary จริง |
| Library API | `/check-types-definition` — API surface จาก `.d.ts` declarations ใน `node_modules` |
| Codebase | `/learn-from-codebase` — `/deep-analyze` + learning path และ concept map ของ codebase |
| Pattern | `/learn-pattern` — สกัด reusable patterns จาก real-world code |
| Slides | `/report-slides` — สร้าง Slidev presentation สรุปความรู้ใน `.devin/temp/` |

เรียก skill ตามตารางตาม topic แล้วทำตาม flow ในนั้น — ไม่ execute จากตารางนี้โดยตรง

### 1. Define Learning Target

> Goal: Define Learning Target

กำหนดเป้าหมายการเรียนรู้:

1. ระบุสิ่งที่ต้องการเรียนรู้ (concept, tool, library, framework, codebase)
2. กำหนดระดับความลึกที่ต้องการ (overview, intermediate, deep)
3. ระบุคำถามหลักที่ต้องการคำตอบ
4. กำหนดเวลาและขอบเขตการเรียนรู้

### 2. Deep Research

> Goal: Deep Research

ทำ `/deep-research` เพื่อค้นหาข้อมูลลึก:

1. ค้นหาจาก NPM, GitHub, DeepWiki, Context7 และ WebSearch
2. อ่าน official documentation ของ tool/library ที่เรียนรู้
3. ค้นหา best practices และ common patterns
4. ค้นหา examples และ tutorials
5. ตรวจสอบ version compatibility กับ project

### 3. Learn From Sources

> Goal: Learn From Sources

ทำ `/learn-from-web` สำหรับเรียนรู้จากเว็บไซต์หลัก และ `/learn-from-cli` สำหรับ CLI discovery:

1. ใช้ DeepWiki สำหรับ GitHub repositories
2. ใช้ Context7 สำหรับ libraries และ frameworks
3. ใช้ Web Search สำหรับ fallback
4. บันทึก code examples และ configuration examples

### 4. Apply Best Practices

> Goal: Apply Best Practices

ทำ `/follow-best-practice` เพื่อนำความรู้ไปใช้:

1. นำ best practices ที่เรียนรู้มาประยุกต์ใช้
2. ตรวจสอบความถูกต้องด้วย linter และ typecheck
3. ทดสอบด้วย examples ที่เรียนรู้มา
4. ปรับปรุงตาม feedback

### 5. Learn From Code Patterns

> Goal: Learn From Code Patterns

ทำ `/learn-pattern` เพื่อสกัด reusable patterns

1. ค้นหา code patterns จาก real-world projects
2. วิเคราะห์ patterns ที่ใช้ใน production codebases
3. ระบุ pattern variants และ trade-offs
4. บันทึก patterns พร้อม use cases

### 6. Hands-On Practice

> Goal: Hands-On Practice

ฝึกปฏิบัติจริงเพื่อยืนยันความเข้าใจ

1. สร้างตัวอย่างการใช้งานจริงใน project context
2. ทดลอง edge cases และ error handling
3. ทดลอง integration กับ existing code
4. เปรียบเทียบผลลัพธ์กับที่เรียนรู้มา
5. ทำ `/update-examples` เพื่อสร้าง examples ครอบคลุม
6. บันทึก lessons learned และ cheat sheet สำหรับ future reference

## Rules

### 1. Learning Approach

- เริ่มจาก overview ก่อน deep dive
- ใช้ multiple sources เพื่อ cross-reference
- ฝึกปฏิบัติจริง ไม่ใช่แค่อ่าน
- สกัด code patterns จาก real-world projects
- สร้าง examples ที่นำไปใช้ได้จริงใน project

### 2. Research Standards

- ทำ `/deep-research` สำหรับค้นหาข้อมูลลึกจาก multiple sources
- ทำ `/learn-from-web` สำหรับเรียนรู้จากเว็บไซต์หลัก, `/learn-from-cli` สำหรับ CLI, `/check-types-definition` สำหรับ API surface
- ตรวจสอบ credibility และ freshness ของข้อมูล
- บันทึก code examples และ configuration examples

### 3. Best Practices

- ทำ `/follow-best-practice` เพื่อนำความรู้ไปใช้ตามมาตรฐาน
- ตรวจสอบความถูกต้องด้วย linter และ typecheck
- รัน tests เพื่อยืนยันความถูกต้อง

### 4. Knowledge Retention

- บันทึกหลักการสำคัญและ core concepts
- บันทึก edge cases และ common pitfalls
- สร้าง examples สำหรับทีม
- แชร์ความรู้ผ่าน documentation

## Expected Outcome

- เข้าใจ concept, tool, หรือ library อย่างลึกซึ้ง
- ข้อมูลครบถ้วนจาก multiple sources
- Code examples และ best practices ที่บันทึกไว้
- การนำความรู้ไปใช้จริงพร้อม validation
- Lessons learned สำหรับ future reference