---
name: report
description: "เลือก format รายงานทีเหมาะสม: table หรือ numbered list"
argument-hint: "[scope]"
related:
  - report-todo
  - report-progress
  - suggest-next-action
  - deep-review

---

## Goal

เลือกและ execute format รายงานทีเหมาะสมกับ context

## Scope

ใช้สำหรับรายงานผลในแชท โดย `/report` จะ dispatch ไปยัง `report-table` หรือ `report-numbered` ตามประเภทข้อมูล

- รวม capability จาก skills เดิมที่ถูกย้ายเข้า workflows

## Execute

### Workflows

| Domain      | Workflow |
|-------------|----------|
| `table`     | `workflows/table/SKILL.md` — ตอบเป็นตารางพร้อมคอลัมน์ `No.` เรียงลำดับ |
| `html`      | `workflows/html/SKILL.md` — ไฟล์ HTML ไฟล์เดียวโต้ตอบได้บน browser |
| `numbered`  | `workflows/numbered/SKILL.md` — numbered list เรียงลำดับความสำคัญ |
| `codeblock` | `workflows/codeblock/SKILL.md` — code blocks สำหรับ commands, snippets, config, logs, diff |

### 1. Select Format

> Goal: เลือกรูปแบบรายงาน

1. ถ้าข้อมูลเหมาะกับตารางหลาย columns → ใช้ `/report table`
2. ถ้าข้อมูลเหมาะกับลำดับ steps/priority → ใช้ `/report numbered`
3. ถ้าเป็น action plan จาก chat โดยยังไม่ลงมือ → ใช้ `/report-todo`
4. ถ้าเป็น commands, code snippets, config, logs, diff → ใช้ `/report codeblock`
5. ถ้าเป็น progress/status → ใช้ `/report-progress`
6. ถ้าเป็น TODO markers → อ่าน `TODO.md` + ใช้ `/scan-codebase` หา `TODO`/`FIXME`/`HACK` markers แล้ว report table

### 2. Execute Selected Skill

> Goal: รายงานตาม format

1. ส่งข้อมูลให้ skill ทีเลือก
2. ตรวจ output ว่าตรง format
3. ถ้าจำเป็น ใช้ `/deep-review`

### 3. Apply UX/UI Format

> Goal: ทำให้ report อ่านง่าย

1. ทำตาม `[references/uxui.md](references/uxui.md)`
2. ใช้ emoji ตาม legend ทีกำหนด
3. เรียงลำดับตาม status ให้ `completed` อยู่บนสุด
4. ไม่ใช้ bold markers

### 4. Finalize

> Goal: สรุปและชี้ next action

1. ทำ `/suggest-next-action` ถ้ามี next steps
2. ถ้า output มาจาก `/report-todo` ต้องมีตาราง + สรุป numbered list

## Rules

- `/report` ไม่ใช่รายงานเอง แต่ dispatch ไปยัง format ย่อย
- ใช้ `/report table` เมื่องานมี comparison/status หลาย columns
- ใช้ `/report numbered` เมื่องานเน้นลำดับ steps
- ใช้ `/report-todo` เมื่องานยังไม่ลงมือ ต้องการ action plan
- ทุกตารางต้องมีคอลัมน์ `No.` เป็นคอลัมน์แรก
- ทุก report ต้องสรุป key findings ด้านบน
- ใช้ emoji ตาม legend ใน `references/uxui.md`
- ไม่ใช้ bold markers

## Merged Details

### codeblock

##### Goal

ตอบในแชทเป็น code block เพื่อเน้น commands, code snippets, config, logs หรือ output ทีต้อง copy-paste ได้

##### Scope

ใช้เมื่อข้อมูลเหมาะกับ code block มากกวาตารางหรือ numbered list เช่น:
- commands หรือ scripts
- code snippets
- config files
- error logs
- diff output

##### Execute

###### 1. Select Code Block Type

> Goal: เลือก language/annotation ทีเหมาะสม

1. ถ้าเป็น shell command → ใช้ `bash` หรือ `powershell`
2. ถ้าเป็น code snippet → ใช้ language ทีตรง เช่น `typescript`, `rust`, `python`
3. ถ้าเป็น config → ใช้ `json`, `toml`, `yaml`, `kdl`
4. ถ้าเป็น log → ใช้ `text`
5. ถ้าเป็น diff → ใช้ `diff`

###### 2. Add Context Header

> Goal: บอกว่า code block นี้คืออะไร

1. ก่อน code block ใส่ heading หรือสั้น ๆ บอกว่าเป็นส่วนไหน
2. ถ้ามีหลาย block ให้แยกเป็นส่วน ๆ พร้อม `###` หรือ short description

###### 3. Format Content

> Goal: ทำให้ code block อ่านและ copy ได้ง่าย

1. ไม่ใส่ line numbers ภายใน code block
2. ใช้เครื่องหมาย ``` เปิดและปิด
3. ระบุ language หลัง ```
4. ถ้ามีหลาย block ให้แยกเป็นส่วน ๆ พร้อมสั้น ๆ ข้างบน
5. ถ้ามีคำอธิบายเพิ่มเติม ใส่นอก code block

###### 4. Validate

> Goal: ตรวจคุณภาพก่อนส่ง

1. ตรวจ syntax ถูกต้องตาม language ทีระบุ
2. ตรวจว่า code block อ่านง่ายบนทุก device
3. ถ้ามี commands ให้ระบุ dry run ก่อน execute

##### Rules

- ใช้ code block เมื่องานเหมาะกับ copy-paste หรือ syntax highlighting
- ถ้าต้องการรายงานหลาย columns ให้ใช้ `/report` หรือ `/report table`
- ถ้าต้องการรายงานหลาย code blocks คู่กับ table ให้ใช้ `/report table`
- ระบุ language หลังเครื่องหมาย ```
- ไม่ใช้ bold markers ภายใน code block
- ถ้ามีหลาย block ให้ใช้ `###` หรือสั้น ๆ แยก
- ตอบในแชทเท่านั้น

##### Expected Outcome

- Code block ทีระบุ language ถูกต้อง
- เนื้อหาอ่านง่ายและ copy ได้
- สั้น ๆ ชัดเจน ไม่ยาวเกินจำเป็น

### html

##### Goal

สร้างไฟล์ HTML ไฟล์เดียวที่นำเสนอผลการวิเคราะห์โปรเจกต์, การวิเคราะห์ หรือแผนฟีเจอร์บนเบราว์เซอร์ รายงานรองรับตารางแบบโต้ตอบได้ พร้อม sort, filter, group, search และ dropdown รายแถว รวมถึงการสลับธีมและเมนูนำทางแบบ sticky

##### Scope

- สร้างไฟล์ `.html` ไฟล์เดียวที่พึ่งพาตัวเองได้ โดยไม่ต้อง build
- ใช้ Tailwind CSS ผ่าน CDN และอาจใช้ Vue 3 สำหรับการโต้ตอบ
- รวมตารางที่สามารถ sort, filter, group และ search ได้
- แต่ละแถวของตารางสามารถขยายเป็น dropdown พร้อมคอลัมน์เพิ่มเติมได้
- เนื้อหาเนื้อหารายงานเป็นภาษาอังกฤษ; เนื้อหาในเซลล์ตารางอาจใช้ภาษาของโปรเจกต์

##### Execute

###### 1. Prepare Data

> Goal: มีข้อมูลที่สะอาดและมีโครงสร้างก่อนเรนเดอร์

1. รัน `/deep-analyze` หรือ skill หลักที่สร้างข้อมูล (เช่น `/idea-features`)
2. แปลงผลลัพธ์เป็น JavaScript array ของ objects หรือ 2D arrays
3. ตรวจสอบให้แต่ละแถวมี `id` ที่ไม่ซ้ำและครบทุกฟิลด์ที่จำเป็น
4. เพิ่มฟิลด์คำนวณสำหรับ `group` และ `searchText` หากจำเป็น

###### 2. Build HTML Shell

> Goal: ไฟล์เดียวที่โหลด assets ทั้งหมดจาก CDN

1. ใช้ `<!DOCTYPE html>`, `<html lang="en">`, `<meta charset="UTF-8">`
2. โหลด Tailwind CSS: `https://cdn.tailwindcss.com`
3. สำหรับโหมดโต้ตอบ โหลด Vue 3: `https://unpkg.com/vue@3/dist/vue.global.js`
4. ตั้งค่า `tailwind.config = { darkMode: 'class' }`
5. สร้าง `<div id="app">` และบล็อก `<script>` โดยใช้ `Vue.createApp`

###### 3. Add Header And Theme Toggle

> Goal: ส่วนหัวชัดเจนพร้อมโหมดมืด/สว่าง

1. แสดงชื่อรายงานและคำบรรยายสั้นๆ
2. เพิ่มปุ่มสลับธีมที่สลับคลาส `dark` บน `<html>`
3. บันทึกการตั้งค่าใน `localStorage`
4. อ่าน `prefers-color-scheme` เมื่อโหลด
5. ใช้ตัวบ่งชี้สถานะที่ชัดเจน (เช่น badge หรือ icon) สำหรับประเภทรายงาน

###### 4. Add Sticky Tabs And Key Findings

> Goal: เมนูนำทางระดับบนและสรุป

1. สร้างแถบแท็บแบบ sticky ด้วย `position: sticky; top: 0`
2. ใช้ `backdrop-blur` และพื้นหลังที่ตัดกัน
3. แท็บแรกแสดงการ์ด `Key Findings` ในกริดแบบ responsive
4. แต่ละแท็บมี badge แสดงจำนวนรายการ
5. ใช้ลำดับชั้นภาพที่ชัดเจน: title > subtitle > key findings > tabs

###### 5. Build Interactive Table

> Goal: ตารางรองรับการโต้ตอบที่หลากหลาย

1. เรนเดอร์ตารางจาก data array โดยใช้ `v-for`
2. เพิ่มช่อง search ผูกด้วย `v-model`
3. เพิ่ม filter chips สำหรับ `Priority`, `Impact`, `Phase`, `Effort`
4. เพิ่มตัวควบคุม sort บนส่วนหัวคอลัมน์ (คลิกเพื่อสลับ asc/desc)
5. เพิ่มตัวเลือก group by (เช่น group by `Phase` หรือ `Priority`)
6. เพิ่มปุ่ม `Clear` เมื่อมี filter ที่ใช้งานอยู่
7. แสดงสถานะว่าง `No results` เมื่อ filter ส่งกลับศูนย์แถว
8. ใช้ computed `filteredRows` สำหรับ sort/filter/group/search

###### 6. Add Per-Row Dropdown

> Goal: แต่ละแถวสามารถขยายเพื่อแสดงรายละเอียดเพิ่มเติมได้

1. เพิ่มลูกศรขยาย/ยุบบนแต่ละแถว
2. เมื่อขยาย ให้แสดงพาเนล dropdown ด้านล่างแถว
3. Dropdown มีอย่างน้อยสองคอลัมน์ (เช่น `UX/UI Sketch` และ `Plan`)
4. เนื้อหากระชับ; ใช้ `pre` หรือ `ul` สำหรับ sketches และ plans
5. ขยายได้ครั้งละหนึ่งแถวหากช่วยให้ UX ดีขึ้น

###### 7. Add Summary And Diagrams

> Goal: ผลการวิเคราะห์ที่ไม่ใช่ตารางก็มองเห็นได้

1. เพิ่มส่วนสรุปสำหรับ DB/Files, API/Functions, Components
2. เพิ่ม UX/UI sketch และ architecture diagram แบบข้อความ
3. เก็บ diagrams ในบล็อก `<pre>` พร้อมฟอนต์ monospace
4. ใช้การ์ดและกริดสำหรับสรุป ไม่ใช่แค่ลิสต์ธรรมดา

###### 8. Add Next Action

> Goal: รายงานจบด้วยข้อแนะนำที่ชัดเจน

1. เพิ่มส่วน `Next Action` ที่ด้านล่าง
2. ใช้ลิสต์แบบลำดับเลขหรือ bullet
3. อ้างอิงรายการที่มีความสำคัญสูงสุดด้วย `#`
4. ตกแต่ง next action ด้วยพื้นหลังหรือขอบที่โดดเด่น

###### 9. Open In Browser

> Goal: ตรวจสอบว่ารายงานเรนเดอร์ถูกต้อง

1. บันทึกไฟล์ใน `reports/<report-name>.html` หรือ `.devin/temp/report/<workspace>/<report-name>.html`
2. รัน `/open-web` หรือ `Start-Process <path>` เพื่อเปิดในเบราว์เซอร์
3. ยืนยันว่าแท็บ, ธีม, sort, filter, dropdown ทำงานได้

##### Rules

###### 1. Single Self-Contained File

- ไม่มี build step ไม่มีการติดตั้ง package ภายนอก
- JS/CSS ทั้งหมดโหลดจาก CDN
- ข้อมูลฝังอยู่ใน `<script>`
- ขนาดไฟล์ต่ำกว่า 500 KB หากเป็นไปได้

###### 2. Report Body Language

- ส่วนหัว, ผลการวิเคราะห์, สรุป, diagrams และ next action เป็นภาษาอังกฤษ
- เนื้อหาในเซลล์ตารางอาจเป็นภาษาของโปรเจกต์ (เช่น ไทย)
- ห้ามผสมภาษาในย่อหน้าเดียวกัน

###### 3. Table Interactivity

- ค้นหาด้วยข้อความในทุกคอลัมน์ที่มองเห็น
- Filter ตาม `Priority`, `Impact`, `Phase`, `Effort`, `Difficult`
- Sort ตามคอลัมน์ใดก็ได้ (สลับ asc/desc)
- จัดกลุ่มแถวตามคอลัมน์ที่เลือก
- ปุ่มล้าง filters
- ไฮไลต์สถานะ filter/sort ที่ใช้งานอยู่
- แสดงสถานะว่างเมื่อไม่มีแถวที่ตรง

###### 4. Per-Row Dropdown

- แต่ละแถวมีปุ่มขยายหรือแถวที่คลิกได้
- พาเนลที่ขยายมีอย่างน้อยสองคอลัมน์ที่มีป้ายกำกับ
- สำหรับผลลัพธ์ของ `/idea-features` คอลัมน์ควรเป็น `UX/UI Sketch` และ `Plan`
- เนื้อหา dropdown ใช้ข้อความกระชับหรือ code blocks

###### 5. Design Tokens And Visual Hierarchy

- กำหนดชุด design token เล็กๆ ด้วย CSS variables สำหรับสี brand, success, warning, danger และ neutral
- ใช้สเกลระยะห่างที่สม่ำเสมอ: `4`, `8`, `12`, `16`, `24`, `32`, `48`
- รักษา font stack: `system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`
- ใช้ `text-sm` สำหรับตาราง, `text-base` สำหรับเนื้อหา, `text-2xl` สำหรับชื่อหน้า
- หลีกเลี่ยงใช้สี accent เกิน 6 สี

###### 6. UX/UI Improvements

- มุมโค้งมน (`rounded-lg` สำหรับการ์ด, `rounded` สำหรับปุ่ม/badges)
- เงาเล็กน้อย (`shadow-sm` สำหรับการ์ด, `shadow` สำหรับส่วนหัว sticky)
- แถบแท็บ sticky พร้อม `backdrop-blur`
- ส่วนหัวตาราง sticky (`sticky top-0 z-10`) บนตารางกว้าง
- สถานะ hover ของแถวด้วย `hover:bg-gray-50 dark:hover:bg-gray-700/50`
- สีแถวสลับเป็นทางเลือก แต่ต้องรักษาความตัดกัน
- สีสถานะ: แดงสำหรับ high/danger, เหลืองสำหรับ medium/warning, เขียวสำหรับ low/success, น้ำเงินสำหรับ info
- ใช้ badges/pills สำหรับ `Priority`, `Phase`, `Impact`, `Effort`
- ส่วนหัวกลุ่มแตกต่างจากแถว (พื้นหลัง + ตัวหนา)
- การ์ดสรุปในกริดแบบ responsive (`grid-cols-1 md:grid-cols-3`)

###### 7. Responsive And Accessible

- เลื่อนแนวนอนสำหรับตารางกว้าง (`overflow-x-auto`)
- บนหน้าจอเล็ก ให้เรียง filters และแท็บในแนวตั้ง
- ใช้ `focus:outline-none focus:ring-2 focus:ring-blue-500` สำหรับองค์ประกอบที่โฟกัสได้
- ห้ามใช้สีเพียงอย่างเดียวเพื่อสื่อความหมาย; เพิ่มข้อความหรือ icon
- ใช้ `aria-label` สำหรับปุ่มที่มีเฉพาะ icon
- เคารพ `prefers-reduced-motion`
- รับประกันความตัดกันของสีที่เพียงพอทั้งในโหมดสว่างและโหมดมืด

###### 8. Empty, Loading, And Error States

- แสดงข้อความ `No results` ที่เป็นมิตรเมื่อ filter ไม่ตรงเลย
- แสดง fallback `Loading...` ขณะ Vue เริ่มต้น (ใช้ `v-cloak`)
- จัดปุ่ม `Reset filters` ในสถานะว่าง
- หากข้อมูลหาย ให้แสดงข้อความชัดเจนแทนตารางที่เสีย

###### 9. Micro-Interactions

- ไฮไลต์คอลัมน์ sort ที่ใช้งานอยู่
- แสดง count badge บนแท็บที่ใช้งานอยู่
- เคลื่อนไหวการขยายแถวด้วย transition `max-height` แบบง่าย (เคารพ `prefers-reduced-motion`)
- ใช้ hover transitions เล็กน้อยสำหรับปุ่มและแถว
- แสดง feedback `Copied` หรือ `Saved` สำหรับการ copy/export ใดๆ

###### 10. Print And Share

- เพิ่มบล็อก CSS ที่เหมาะสำหรับการพิมพ์:
  - ซ่อนแถบแท็บ sticky, สลับธีม และ filters
  - ขยายแถว dropdown ทั้งหมดอัตโนมัติ
  - ใช้ข้อความสีดำบนพื้นหลังสีขาว
- รักษา URL และ code blocks ให้อ่านได้เมื่อพิมพ์

###### 11. Always Open After Create

- ทุกครั้งทีสร้างรายงาน HTML เสร็จ ต้องเปิดด้วย `/open-web` เสมอ
- ไม่ถือวารูปงานเสร็จจนกว่าจะเปิดใน browser ได้
- ถ้าไม่สามารถเปิดได้ → รายงานปัญหาและหาทางเปิดด้วย `Start-Process` หรือ OS command

###### 12. Safety

- ห้ามมี secrets, credentials หรือ paths ที่ละเอียดอ่อนที่ hardcode ไว้
- ใช้ relative paths สำหรับไฟล์โปรเจกต์
- ทำความสะอาดเนื้อหาที่ผู้ใช้ให้มาก่อนฉีดเข้า HTML
- ใช้ `DOMPurify` หากเรนเดอร์ HTML จากแหล่งที่ไม่น่าเชื่อถือ

- ใช้ /visualize-in-web ถ้าจำเป็น
- ใช้ /open-files-in-web ถ้าจำเป็น

##### Expected Outcome

- ไฟล์ `.html` ไฟล์เดียวที่บันทึกในโปรเจกต์
- เนื้อหารายงานเป็นภาษาอังกฤษ, เซลล์ตารางเป็นภาษาของโปรเจกต์หากจำเป็น
- ตารางโต้ตอบได้พร้อม sort, filter, group, search และส่วนหัว sticky
- Dropdown รายแถวพร้อมสองคอลัมน์
- สลับธีม, แท็บ sticky, key findings, สรุป, diagrams, next action
- Responsive, accessible และเหมาะสำหรับการพิมพ์
- สถานะว่าง/loading/error ที่ชัดเจน
- ไฟล์เปิดในเบราว์เซอร์และเรนเดอร์ถูกต้อง

### numbered

##### Goal

ตอบในแชทเป็น numbered list เพื่อเน้นลำดับความสำคัญหรือ steps

##### Scope

ใช้สำหรับข้อมูลที่ต้องการเน้นลำดับ ขั้นตอน หรือ priority มากกวา comparison

##### Execute

###### 1. Prepare Items

> Goal: รวบรวม items ทีจะรายงาน

1. รวบรวมข้อมูล
2. แยกแต่ละ item ให้มี single responsibility
3. กำหนด priority

###### 2. Number And Group

> Goal: จัดลำดับและกลุ่ม

1. ใช้เลข 1, 2, 3, ... ตาม priority
2. ถ้ามีหลายหมวด ใช้ `##` headers แยกกลุ่ม
3. ภายในกลุ่มเรียงตาม priority

###### 3. Format

> Goal: ทำให้อ่านง่าย

1. เริ่มด้วย summary 2-3 ข้อก่อน numbered list
2. ใช้ emoji ตาม status: `✅` `⏳` `❌` `⚠️`
3. ใช้ bullet ย่อยภายใต้แต่ละหมายเลขถ้าจำเป็น
4. ใช้ backticks สำหรับ code, paths, skill names
5. ใช้ `/report table` ถ้าข้อมูลเหมาะกับตารางมากกวา
6. ใช้ `/report codeblock` ถ้ามี commands หรือ code snippets

###### 4. Validate

> Goal: ตรวจคุณภาพ

1. ตรวจลำดับเลขถูกต้อง
2. ตรวจแต่ละข้อมี single responsibility
3. ทำ `/suggest-next-action` ถ้ามี next steps

##### Rules

- หนึ่งเลข = หนึ่ง idea/step
- เรียงตาม priority หรือ status ให้ `completed` อยู่ก่อน
- ใช้ backticks สำหรับ paths, commands, skill names
- ใช้ emoji ตาม legend ของ `/report`
- ไม่ใช้ bold markers
- ตอบในแชทเท่านั้น

##### Expected Outcome

- Numbered list เรียงลำดับถูกต้อง
- แต่ละข้อกระชับ ชัดเจน
- ระบุ next action ถ้ามี

### table

##### Goal

ตอบในแชทเป็นตารางที่มีคอลัมน์ `No.` เป็นคอลัมน์แรก เรียงลำดับ 1, 2, 3, ...

##### Scope

ใช้สำหรับข้อมูลที่ต้องเปรียบเทียบหลาย columns หรือต้องการดูสถานะครบในตารางเดียว

##### Execute

###### 1. Prepare Data

> Goal: รวบรวมและจัดเตรียมข้อมูล

1. รวบรวมข้อมูลทีต้องรายงาน
2. จัดกลุ่มตาม category
3. กำหนดลำดับความสำคัญ
4. ตัดสินใจคอลัมน์ทีเหมาะสม

###### 2. Build Table

> Goal: สร้างตารางทีอ่านง่าย

1. คอลัมน์แรกต้องเป็น `No.` เรียง 1, 2, 3, ...
2. ใช้ headers ชัดเจน
3. จัดเรียง columns ตามความสำคัญ
4. ใช้ alignment เหมาะสมกับ data types

###### 3. Group And Sort

> Goal: จัดกลุ่มและเรียงลำดับ

1. จัดกลุ่มข้อมูลตาม category
2. ใช้ headers สำหรับแยกกลุ่ม
3. เรียงลำดับภายในกลุ่มตาม priority
4. ถ้ามี status ให้ sort ตาม: `✅ completed` → `⏳ in_progress` → `⚠️ pending` → `❌ blocker`

###### 4. Add Summary

> Goal: สรุปให้เข้าใจเร็ว

1. เริ่มด้วย key findings 2-3 ข้อ
2. ระบุ overall status ด้วย emoji
3. ทำ `/suggest-next-action` ถ้ามี next steps

###### 5. Validate

> Goal: ตรวจคุณภาพก่อนส่ง

1. ตรวจ `No.` เรียงถูกต้อง
2. ตรวจ grouping และ sorting
3. ตรวจ emoji ใช้ตาม legend
4. ทำ `/deep-review` ถ้าจำเป็น

##### Rules

- ทุกตารางต้องมีคอลัมน์ `No.` เป็นคอลัมน์แรก
- ถ้าไม่แน่ใจ format ให้ใช้ `/report` dispatch ตาม context
- ใช้ backticks สำหรับ code, paths, skill names
- ใช้ symbols ✅ ❌ ⚠️ สำหรับ status
- ไม่ใช้ bold markers
- ตอบในแชทเท่านั้น

##### Expected Outcome

- ตารางทีมีคอลัมน์ `No.` เรียงลำดับถูกต้อง
- Grouping และ sorting ชัดเจน
- ข้อมูลอ่านง่าย

### references/format-ansi

#### report-ansi (merged content)

##### Goal

สร้างรายงาน terminal ด้วย ANSI colors, progress bars, status symbols, box-drawing characters, และ summary สำหรับ logs, status, progress, UX/UI sketches และ architecture diagrams

##### Scope

ใช้สำหรับรายงานความคืบหน้า, สถานะ, error summary, UX/UI sketches, และ architecture diagrams ใน terminal ทีอ่านง่าย

##### Execute

###### 1. Collect Status

> Goal: รวบรวมข้อมูลทีต้องรายงาน

1. อ่าน logs หรือ status จาก file/stdout
2. ระบุ categories ของข้อมูล
3. นับจำนวน pass/fail/warning

###### 2. Format With ANSI

> Goal: จัดรูปแบบด้วย ANSI escape codes

1. ใช้สี green สำหรับ success, red สำหรับ error, yellow สำหรับ warning, blue สำหรับ info
2. ใช้ bold สำหรับ headers
3. ใช้ progress bars สำหรับ percentage (ถ้ามี)
4. ใช้ symbols ✅ ❌ ⚠️ ℹ️ สำหรับ status

###### 3. Render Summary

> Goal: แสดงสรุปด้านบน

1. สรุปจำนวนรายการตาม status
2. แสดง key findings สั้นๆ
3. แสดง progress ถ้ามี
4. แยกรายละเอียดด้านล่าง

###### 4. Draw Box Diagrams And Sketches

> Goal: วาด diagram/sketch ด้วย ANSI box-drawing characters

1. ทำ `/scan-codebase` เพื่อหา components, routes, modules ที่เกี่ยวข้อง
2. เลือก view type: full page, dialog/modal, component, flow, system overview, module dependency
3. กำหนด target device: desktop, mobile, หรือ both และความกว้างสูงสุดไม่เกิน 80 characters
4. วาด frame ด้วย `┌─┐│└─┘` (single-line) หรือ `╔═╗║╚═╝` (double-line) สำหรับ outer container
5. วาด sections หลัก: header, content area, sidebar, footer, layers, modules
6. ใช้ `├─┤`, `┬─┴`, `├─`, `└─`, `│` สำหรับ dividers/branching
7. ใช้ `[Button]`, `[Input]`, `[____]`, `[✓]`, `[ ]`, `[Select ▼]`, `[×]` สำหรับ interactive elements
8. ใช้ arrows `→ ↓ ↑ ⇄ ↔ ⇢` แสดง flow/dependency
9. ใช้ `◇` สำหรับ decision, `○` start, `●` end, หรือ numbered steps `① ② ③`
10. แสดง mobile view ด้วย single column, bottom navigation, touch targets `[  Button  ]`
11. ใช้ `//` สำหรับ inline annotations, `⚠` สำหรับ concerns, `✨` สำหรับ new components
12. ตรวจสอบว่า layout ไม่กว้างเกิน 80 characters, alignment สมมาตร, และอ้างอิง codebase จริง

##### Rules

###### 1. ANSI Safety

- ใช้ ANSI codes ที support common terminals
- ถ้า output ถูก redirect ให้รองรับ NO_COLOR
- ไม่ใช้ 256 colors ถ้าไม่จำเป็น

###### 2. Readability

- summary อยู่ด้านบน
- จัดกลุ่มตาม category
- ใช้ symbols คู่กับสี
- ความกว้างสูงสุด 80 characters สำหรับ chat readability
- ใช้ 2 spaces สำหรับ indentation
- แยก sections ด้วย blank lines

###### 3. Consistency

- ใช้ชุดสีเดียวกันกับ `report-table`
- ไม่ผสมหลาย color scheme
- ใช้ box-drawing characters อย่างสม่ำเสมอ

###### 4. Sketch/Diagram Accuracy

- อ้างอิง components, routes, modules ที่มีอยู่จริงใน codebase เท่านั้น
- ห้ามประดิษฐ์ UI elements หรือ services ที่ไม่มี
- ใช้ labels สั้นๆ ไม่เกิน 1 บรรทัดต่อ box/section
- ระบุ route path/technology names ใน boxes ถ้ามี

##### Expected Outcome

- terminal report พร้อม ANSI colors และ status summary
- box-drawing sketches/diagrams ที่อ่านง่ายบน chat
- component structure และ user flow ที่อ้างอิง codebase จริง
- รองรับ common terminals และ NO_COLOR

### references/format-codeblock

#### report-codeblock (merged content)

##### Goal

จัดรูปแบบ code/text output (codeblocks, diffs, JSON, markdown) ให้สวยงามและอ่านง่าย

##### Scope

ใช้สำหรับการจัดรูปแบบ:
- Code snippets พร้อม syntax highlighting
- Code diffs และ changes
- JSON output สำหรับ API responses และ structured data
- Markdown documents สำหรับ documentation และ README

##### Execute

###### 1. Format Code Blocks

> Goal: Format Code Blocks

1. ระบุ programming language สำหรับ syntax highlighting
2. ใช้ language tags ที่ถูกต้อง (`typescript`, `python`, `rust`, ฯลฯ)
3. ใช้ proper indentation (2 หรือ 4 spaces)
4. เพิ่ม comments สำหรับ code ที่ซับซ้อน

###### 2. Format Diffs

> Goal: Format Diffs

1. ใช้ standard unified diff format (`+`, `-`, context)
2. จัดกลุ่ม changes ตาม files
3. เพิ่ม file paths และ change statistics (additions, deletions)
4. ใช้ context lines สำหรับ readability

###### 3. Format JSON

> Goal: Format JSON

1. ใช้ pretty print ด้วย indentation 2 spaces
2. ใช้ consistent naming conventions (`camelCase` หรือ `snake_case`)
3. ใช้ `null` แทน undefined หรือ empty strings
4. เพิ่ม metadata: `timestamp`, `version`, `status`

###### 4. Format Markdown

> Goal: Format Markdown

1. ใช้ hierarchy ของ headings (H1-H6) อย่างเหมาะสม
2. ใช้ H1 สำหรับ document title (เพียง 1 ครั้ง)
3. ใช้ H2-H3 สำหรับ main sections, H4-H6 สำหรับ subsections
4. ไม่ข้าม heading levels

###### 5. Add Metadata

> Goal: Add Metadata

1. เพิ่ม filename หรือ path ด้านบน code block
2. เพิ่ม line numbers ถ้าจำเป็น
3. เพิ่ม commit hash สำหรับ diffs
4. เพิ่ม timestamp สำหรับ JSON output

###### 6. Highlight Key Parts

> Goal: Highlight Key Parts

1. ใช้ bold สำหรับ keywords สำคัญ
2. ใช้ comments สำหรับ explanations ใน code
3. ใช้ markers สำหรับ function/class changes ใน diffs
4. ใช้ inline annotations ถ้าจำเป็น

##### Rules

###### Report UX/UI

> Goal: report อ่านง่าย สรุป key findings ไว้ด้านบน และนำไปสู่ action

1. สรุป key findings ไว้ด้านบนก่อนรายละเอียด
2. ใช้ `/report table` สำหรับตารางเปรียบเทียบหลาย columns
3. ใช้ `/report-progress` สำหรับรายงานสถานะ/progress/logs
4. ใช้คอลัมน์ "No." เป็นคอลัมน์แรก เรียงลำดับ 1, 2, 3, ... โดย headers ชัดเจน จัดกลุ่ม/เรียงลำดับตามความสำคัญ
5. ใช้ symbols ✅ ❌ ⚠️ สำหรับ status indicators
6. ทำ `/suggest-next-action` ท้าย report เสมอ

###### Code Formatting

- ใช้ language tags ที่ถูกต้องและ standard
- ใช้ consistent indentation ทั้ง code block
- ใช้ consistent code style
- ใช้ plain text ถ้าไม่มี language ที่เหมาะสม

###### Diff Format

- ใช้ standard unified diff format
- ใช้ consistent markers สำหรับ additions/deletions
- ใช้ sufficient context สำหรับ readability
- ระบุ change type (added, modified, deleted)

###### JSON Format

- ใช้ consistent naming conventions ทั้ง JSON
- จัดลำดับ fields ตามความสำคัญ
- ใช้ nested objects สำหรับ data ที่เกี่ยวข้องกัน
- ตรวจสอบไม่มี circular references

###### Markdown Format

- ใช้ bold สำหรับ keywords, italic สำหรับ emphasis
- ใช้ code blocks พร้อม language tags
- ใช้ backticks สำหรับ inline code
- ใช้ descriptive link text และ alt text

##### Expected Outcome

- Code blocks ที่มี syntax highlighting ถูกต้อง
- Diffs ที่ชัดเจนและอ่านง่าย
- JSON output ที่ valid และ consistent
- Markdown documents ที่อ่านง่ายและ well-structured
- Report อ่านง่าย มี key findings ด้านบน
- มี next action ชัดเจน

### references/format-numbered-bullet

#### report-numbered-bullet (merged content)

##### Goal

จัดรูปแบบ output ให้เป็น numbered list, bullet list, หรือผสมระหว่าง numbered กับ bullet ตาม context

##### Scope

ใช้สำหรับ report ทั่วไปที่ไม่จำเป็นต้องเป็นตาราง โดยเลือก format ตามลำดับ ความสัมพันธ์ของข้อ และความต้องการ action

##### Execute

###### 1. Choose Format

> Goal: เลือกรูปแบบรายงานทีเหมาะสม

1. ถ้าต้องการลำดับก่อนหลังหรือ priority → ใช้ numbered list
2. ถ้าต้องการรายการทีไม่มีลำดับ → ใช้ bullet list
3. ถ้ามีหัวข้อหลักหลายข้อ และแต่ละหัวข้อมีรายละเอียดย่อย → ใช้ numbered + bullet
4. ถ้าต้องการผสมกับตาราง → ทำ `/report table` คู่กัน

###### 2. Numbered List

> Goal: แสดงลำดับทีชัดเจน

1. ใช้รูปแบบ `N. <ข้อความสั้น>`
2. เรียงลำดับตาม priority, dependency, หรือลำดับเวลา
3. ไม่ให้ข้อเดียวมีหลายงาน — ถ้ามี → ทำ `/follow-single-responsibility` ก่อน
4. ใช้เมื่อ reader ต้องทำตาม step

###### 3. Bullet List

> Goal: แสดงรายการทีไม่ต้องเรียงลำดับ

- ใช้ `-` หรือ `*` สำหรับแต่ละรายการ
- แต่ละ bullet ควรย่อยากระชับ
- ใช้เมื่อข้อมูลมีความสำคัญเท่ากัน
- สามารถจัดกลุ่มด้วย sub-heading ถ้ามีหลายหมวด

###### 4. Numbered + Bullet

> Goal: แสดงหัวข้อหลักพร้อมรายละเอียดย่อย

1. ใช้ numbered list สำหรับหัวข้อหลัก
2. ใช้ bullet list สำหรับรายละเอียดภายใต้แต่ละหัวข้อ
3. ทำให้ single responsibility: หัวข้อหลัก 1 ข้อ = 1 หน่วยงาน
4. ใช้เมื่อมี plan, รายงาน findings, หรือ action items

##### Rules

###### 1. Single Responsibility

- หัวข้อหลักหนึ่งข้อต้องมี single responsibility
- ถ้าพบคำว่า "และ" หรือ "," หลายตัวในข้อเดียว → ทำ `/follow-single-responsibility` ก่อน

###### 2. Reference Support

- ถ้ามี URL → ใส่เป็น `<url>` หรือ markdown link
- ถ้ามี skill → ใช้ `/<skill-name>`
- ถ้ามี file path → ใช้ backticks
- ถ้ามี code/command → ใช้ code block

###### 3. Consistency

- ใช้ภาษาเดียวกันในรายการเดียวกัน
- ตัวหนังสือเริ่มต้นสัมผัสกัน (sentence case หรือ title case ตลอด)
- ไม่ผสม `1.` กับ `1)` หรือ `-` กับ `*` ในหมวดเดียวกัน

###### 4. Output Length

- ไม่เกิน 250 บรรทัดต่อ report ถ้าเกิน → แยกหัวข้อไป `references/` หรือ `/report html`
- แต่ละ bullet/number ไม่ยาวเกิน 2 บรรทัดถ้าไม่จำเป็น

- ใช้ /report-todo ถ้าจำเป็น

##### Expected Outcome

- Output ในรูปแบบ numbered, bullet หรือ numbered + bullet ตาม context
- แต่ละข้อมี single responsibility
- มี references ครบ: URL, skills, paths
- อ่านง่าย กระชับ และพร้อม action

### references/uxui

#### Report UX/UI Guidelines

##### Goal

ทำให้รายงานทุกรูปแบบอ่านง่าย เข้าใจเร็ว และ action ชัดเจน

##### Principles

###### 1. Summary First

- ทุก report ต้องเริ่มด้วย key findings หรือสรุปผล 2-3 ข้อ
- ใช้ bullet สั้น ก่อนรายละเอียด

###### 2. Sort By Status

- ถ้ามี status: เรียง `completed` หรือ `done` ขึ้นก่อน
- ลำดับถัดไป: `in_progress` → `pending` → `blocker` → `failed`

###### 3. Emoji Legend

| Status | Emoji |
|---|---|
| ผ่าน/เสร็จ | `✅` |
| ค้าง/กำลังทำ | `⏳` |
| ติดปัญหา | `❌` |
| warning | `⚠️` |
| info | `ℹ️` |
| รอ user | `❓` |

###### 4. Table Format

- คอลัมน์แรกต้องเป็น `No.`
- ไม่ใช้ bold markers `**`
- ใช้ backticks สำหรับ code, paths, skill names
- หัวตารางชัดเจน ไม่อักษรพิเศษเกิน

###### 5. Numbered List

- หนึ่งเลข = หนึ่งข้อ single responsibility
- เรียงตาม priority
- ใช้ sub-bullet ถ้าจำเป็น

###### 6. Code Blocks

- ระบุ language
- ไม่ใส่ line numbers
- แยกหลาย block ด้วย heading สั้น ๆ

###### 7. Progress

- ใช้ progress bar เช่น `████████████░░ 80%`
- ระบุเปอร์เซ็นต์และ trend (↑ ↓ →)

###### 8. Next Action

- จบด้วย next action ที่ actionable
- ไม่ทิ้ง report โดยไม่มีทิศทาง

## Expected Outcome

- รายงานออกมาตาม format ทีเหมาะสม
- `/report-todo` สำหรับ action plan จาก chat
- สรุป key findings และ next action ชัดเจน
