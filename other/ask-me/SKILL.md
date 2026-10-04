---
name: ask-me
description: ถามผู้ใช้ด้วยตัวเลือกและคำแนะนำ รองรับ multi-select, multi-step, tech stack
argument-hint: "[question]"
allowed-tools:
  - ask_user_question
  - read
  - skill
  - todo_write
related:
  - ask-project-requirement
  - follow-my-persona
  - follow-your-suggestion
  - ask-again
  - dont-ask-me
  - update-references
  - plan
  - search-skills

---

## Goal

ถามผู้ใช้คำถามพร้อมตัวเลือกที่กำหนดไว้และมีคำแนะนำ (recommended) เพื่อขอคำยืนยัน ตัดสินใจเลือกทางเลือก หรือขอข้อมูลเพิ่มเติม รองรับทั้ง single-select, multi-select, multi-step flow และ tech stack questions

## Scope

ใช้สำหรับการถามคำถามทั่วไปที่ต้องการคำตอบแบบเลือกตัวเลือก ไม่ใช่เก็บ requirements (ใช้ `/ask-project-requirement`) และไม่ใช่สัมภาษณ์ preferences (ใช้ `/follow-my-persona`)

รองรับคำถามเกี่ยวกับ tech stack เช่น runtime, language, framework, library, database, test tool, deploy target, CI tool และ package manager

ใช้ `ask_user_question` tool เท่านั้น ห้ามใช้วิธีอื่นในการถามผู้ใช้

## Execute

### 1. Identify Question Type And Flow

> Goal: ระบุประเภทคำถามและโครงสร้าง multi-step

1. วิเคราะห์ว่าต้องการคำตอบแบบใด: `single`, `multiselect`, `text`, `confirm`
2. ถ้าต้องเก็บคำตอบหลายหัวข้อ → ออกแบบ `multi-step` flow แยกเป็น steps
3. แต่ละ step ประกอบด้วย 1-4 คำถาม ใช้ `ask_user_question` ต่อหนึ่ง call
4. ถ้าเป็น `confirm` ให้ตัวเลือกแบบ yes/no หรือ proceed/abort
5. ถ้าเป็น `single` ให้ตัวเลือก 2-4 ตัวเลือก เลือกได้ตัวเดียว
6. ถ้าเป็น `multiselect` ให้ตัวเลือก 2-4 ตัวเลือก เลือกได้หลายตัว ตั้ง `multi_select: true`
7. ถ้าเป็น `text` ให้ผู้ใช้ตอบเอง ไม่บังคับตัวเลือก

### 2. Prepare Multi-Step Questions

> Goal: เตรียมคำถาม ตัวเลือก และ recommendation สำหรับแต่ละ step

1. แบ่งคำถามออกเป็น steps ตามลำดับทีต้องถาม
2. แต่ละ step มี 1-4 คำถาม แต่ละคำถามมี 2-4 ตัวเลือก
3. แต่ละตัวเลือกต้องมี `label` สั้นกระชับ และ `description` อธิบายรายละเอียด
4. ระบุตัวเลือกแนะนำโดยเพิ่ม visual marker นำหน้า `label` เช่น `✨ ทำ /plan ต่อ` หรือ `(recommended) ทำ /plan ต่อ` พร้อมอธิบายเหตุผลใน `description`
5. ตั้ง `multi_select: true` สำหรับคำถามที่เลือกได้หลายตัว
6. ไม่ใส่ตัวเลือก "other" เพราะผู้ใช้สามารถตอบเองได้เสมอ
7. ตัวเลือกต้องครอบคลุมทุกกรณีที่เป็นไปได้
8. เรียงลำดับตัวเลือกโดยวางตัวเลือกที่แนะนำไว้ลำดับแรก
9. เพิ่มตัวเลือก `Skip` เพื่อให้ผู้ใช้ข้ามคำถามนี้ได้ — `description`: "ข้ามคำถามนี้ ใช้ default หรือดำเนินการต่อโดยไม่ตอบ"
10. เพิ่มตัวเลือก `Suggest another` เพื่อให้ผู้ใช้ขอตัวเลือกอื่น — `description`: "ขอให้ AI เสนอตัวเลือกอื่นที่ไม่อยู่ในรายการ"

### 3. Ask With `ask_user_question`

> Goal: ส่งคำถามให้ผู้ใช้

1. เขียน `question` ให้ชัดเจน กระชับ และมี context เพียงพอ
2. ส่ง 1-4 คำถามพร้อมกันใน `ask_user_question` ต่อหนึ่ง step
3. ส่ง `options` พร้อม `label`, `description` และ `multi_select: true/false`
4. ถ้าเป็น multi-step ให้ถาม step ถัดไปหลังประมวลผลคำตอบ step ปัจจุบัน

### 4. Process Multi-Step Response

> Goal: ประมวลผลคำตอบจากผู้ใช้ใน multi-step flow

1. คู่คำถามกับคำตอบจาก mapping ที่ `ask_user_question` return
2. ถ้า `multi_select: true` → `selected` เป็น array สามารถมีหลาย labels
3. ถ้า `multi_select: false` → `selected` มี label เดียว
4. ถ้าผู้ใช้ให้คำตอบเอง (custom_text) ให้วิเคราะห์และปรับแผนตามคำตอบ
5. ถ้าผู้ใช้เลือก `Skip` ให้ดำเนินการต่อโดยใช้ default หรือข้ามขั้นตอนนั้น
6. ถ้าผู้ใช้เลือก `Suggest another` ให้เสนอตัวเลือกใหม่ 2-4 ตัวเลือกที่ไม่ซ้ำกับเดิม
7. ถ้ายังมี step ถัดไป → ถาม step ถัดไป
8. ถ้าเสร็จสิ้น multi-step → สรุปคำตอบทั้งหมดและดำเนินการ
9. ไม่ถามซ้ำคำถามที่ผู้ใช้ตอบแล้ว

### 5. Tech Stack And Tool Questions

> Goal: รองรับคำถามเกี่ยวกับ tech stack, runtime, framework, library และ tool

1. วิเคราะห์ว่าคำถามเกี่ยวกับ technology ประเภทใด: `runtime`, `language`, `framework`, `library`, `database`, `test-tool`, `deploy-target`, `ci-tool`, `package-manager`
2. ใช้ `follow-lang-*`, `follow-framework-*`, `follow-tool-*`, `follow-lib-*`, `follow-service-*` เพื่อสร้างตัวเลือกและคำแนะนำ
3. อ้างอิง project manifest (`package.json`, `Cargo.toml`, `go.mod`, `pyproject.toml`) และ conventions เพื่อระบุ default และ recommended
4. ถ้า tech stack ซับซ้อน → แบ่งเป็น multi-step: `runtime` → `language` → `framework` → `library` → `deploy-target`
5. ตัวเลือกแนะนำต้องระบุเหตุผลเชิงเทคนิค เช่น "Bun ใช้ native APIs ได้เร็วกว่า Node.js ในโปรเจกต์นี้"
6. ถ้าต้องการแสดง map ของ skills ตาม tech stack หรือ task ให้ทำ `/search-skills`

## Rules

### 1. When To Ask

ถามผู้ใช้เมื่อ:

- มีทางเลือกที่ต้องตัดสินใจและไม่ชัดเจนว่าผู้ใช้ต้องการอะไร
- ต้องการยืนยันทิศทางก่อนดำเนินการ
- ข้อมูลไม่เพียงพอที่จะดำเนินการได้ถูกต้อง
- มีหลายวิธีที่ทำได้และผู้ใช้ควรเลือก

### 2. When Not To Ask

ไม่ถามผู้ใช้เมื่อ:

- คำตอบชัดเจนจาก context หรือจาก memory
- เป็นการเก็บ requirements (ใช้ `/ask-project-requirement`)
- เป็นการสัมภาษณ์ preferences (ใช้ `/follow-my-persona`)
- เป็น low-risk action ที่ทำได้เลย
- ผู้ใช้หรือ workflow ระบุ `/dont-ask-me`

### 3. Question Design

- คำถามสั้นกระชับ มี context เพียงพอ
- ใช้ภาษาที่ผู้ใช้เข้าใจ หลีกเลี่ยง jargon
- หลีกเลี่ยงคำถามที่ก่อให้เกิดความสับสนหรือคลุมเครือ
- รายละเอียด options, multi_select, multi-step อยู่ใน Execute #2 แล้ว ไม่ขอซ้ำ
- ถ้า multi-step ให้บอกผู้ใช้ว่าขั้นตอนนี้เป็น step ที่เท่าไร

### 4. Recommendation

- ทุกคำถามต้องมีตัวเลือกที่แนะนำอย่างน้อย 1 ตัวเลือก
- ระบุตัวเลือกแนะนำด้วย visual marker นำหน้า `label` เช่น `✨`, `⭐`, `👍` หรือข้อความ `(recommended)`
- ถ้าผู้ใช้หรือ context ไม่ต้องการ emoji ให้ใช้ `(recommended)` แทน
- ไม่ต้องสร้างตัวเลือก `recommended` แยกต่างหาก
- อธิบายเหตุผลใน `description` ว่าทำไมแนะนำตัวเลือกนี้
- คำแนะนำต้องอ้างอิงจาก context, best practices หรือ project conventions
- ถ้ามีหลายตัวเลือกที่ดีพอๆ กัน ให้เลือกตัวที่ง่ายที่สุดเป็น recommended

### 5. Interaction Patterns

- multi-step: ถาม step ละ 1-4 คำถาม รอคำตอบ แล้วถาม step ถัดไป
- ถ้าผู้ใช้ตอบเอง ให้ปรับแผนตามคำตอบ
- ไม่ถามซ้ำคำถามที่ตอบแล้ว
- ถ้าคำตอบนำไปสู่คำถามใหม่ ให้ถามตามมา
- หลังได้คำตอบ ให้ดำเนินการทันทีไม่ชะลอ
- ถ้าผู้ใช้เลือก `Skip` หลายครั้งติดต่อกัน ให้พิจารณาใช้ default แทนการถามต่อ
- ถ้าผู้ใช้เลือก `Suggest another` ครั้งที่ 2 ให้ใช้ `/ask-again` หรือถามแบบ open-ended
- ถ้าผู้ใช้บอก "ไม่เข้าใจ", "ถามใหม่", "ask again" → ใช้ `/ask-again` เพื่อ rephrase
- ถ้าผู้ใช้เลือก `Skip` ทุกคำถาม ให้หยุดถามและดำเนินการด้วย default ทั้งหมด

### 6. Update References

- ถ้าคำตอบของผู้ใช้นำไปสู่การแก้ไข ย้าย เปลี่ยนชื่อ หรือลบไฟล์/skill → ดำเนินการตามคำตอบแล้วทำ `/update-references` เสมอ
- ไม่ต้องถามยืนยันก่อน update references เพราะเป็นขั้นตอนทีต้องทำเสมอหลังการเปลี่ยนแปลง

- ใช้ /follow-your-suggestion ถ้าจำเป็น
## Examples

### Question Categories

- `runtime`: "เลือก runtime สำหรับ backend" — `Bun`, `Node.js`, `Deno`, `Rust`, `Go`
- `language`: "เลือกภาษาสำหรับ CLI" — `TypeScript/Bun`, `Rust`, `Zig`, `Python`
- `framework`: "เลือก framework สำหรับ web app" — `Next.js`, `Nuxt`, `SolidStart`, `SvelteKit`, `Astro`
- `library`: "เลือก validation library" — `Zod`, `ArkType`, `Valibot`
- `database`: "เลือก database" — `PostgreSQL`, `SQLite`, `Turso`, `Supabase`
- `test-tool`: "เลือก test runner" — `Vitest`, `Playwright`, `Cypress`
- `deploy-target`: "เลือก deploy platform" — `Vercel`, `Cloudflare`, `Railway`
- `ci-tool`: "เลือก CI tool" — `GitHub Actions`, `Renovate`, `Changesets`

### Example: Single-Select Question

```json
{
  "question": "เลือก runtime สำหรับ backend",
  "header": "Runtime",
  "multi_select": false,
  "options": [
    { "label": "✨ Bun", "description": "แนะนำ — เร็ว ใช้ native APIs ได้" },
    { "label": "Node.js", "description": "ecosystem ใหญ่ ใช้งานได้ทั่วไป" },
    { "label": "Deno", "description": "secure by default สำหรับ TypeScript" }
  ]
}
```

### Example: Multi-Select Question

```json
{
  "question": "เลือก tools ทีต้องติดตั้งเพิ่ม",
  "header": "Extra tools",
  "multi_select": true,
  "options": [
    { "label": "Vitest", "description": "test runner" },
    { "label": "Playwright", "description": "E2E testing" },
    { "label": "Biome", "description": "lint + format" }
  ]
}
```

## Expected Outcome

- ผู้ใช้ตัดสินใจได้ง่ายจากตัวเลือกที่ชัดเจนและมีคำแนะนำ
- รองรับ single-select, multi-select และ multi-step flow
- รองรับ tech stack questions ทั้ง runtime, language, framework, library, tool
- ลดการคาดเดาของ AI
- การทำงานสอดคล้องกับความต้องการของผู้ใช้
- ผู้ใช้สามารถข้ามหรือขอตัวเลือกอื่นได้ตลอดการสนทนา
