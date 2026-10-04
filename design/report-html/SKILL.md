---
name: report-html
description: สร้างไฟล์ HTML ไฟล์เดียวแบบโต้ตอบได้สำหรับรายงานบนเบราว์เซอร์ พร้อมตาราง, dropdown, sort/filt...
related:
  - visualize-in-web
  - open-web
---

## Goal

สร้างไฟล์ HTML ไฟล์เดียวที่นำเสนอผลการวิเคราะห์โปรเจกต์, การวิเคราะห์ หรือแผนฟีเจอร์บนเบราว์เซอร์ รายงานรองรับตารางแบบโต้ตอบได้ พร้อม sort, filter, group, search และ dropdown รายแถว รวมถึงการสลับธีมและเมนูนำทางแบบ sticky

## Scope

- สร้างไฟล์ `.html` ไฟล์เดียวที่พึ่งพาตัวเองได้ โดยไม่ต้อง build
- ใช้ Tailwind CSS ผ่าน CDN และอาจใช้ Vue 3 สำหรับการโต้ตอบ
- รวมตารางที่สามารถ sort, filter, group และ search ได้
- แต่ละแถวของตารางสามารถขยายเป็น dropdown พร้อมคอลัมน์เพิ่มเติมได้
- เนื้อหาเนื้อหารายงานเป็นภาษาอังกฤษ; เนื้อหาในเซลล์ตารางอาจใช้ภาษาของโปรเจกต์

## Execute

### 1. Prepare Data

> Goal: มีข้อมูลที่สะอาดและมีโครงสร้างก่อนเรนเดอร์

1. รัน `/analyze-project` หรือ skill หลักที่สร้างข้อมูล (เช่น `/idea-features`)
2. แปลงผลลัพธ์เป็น JavaScript array ของ objects หรือ 2D arrays
3. ตรวจสอบให้แต่ละแถวมี `id` ที่ไม่ซ้ำและครบทุกฟิลด์ที่จำเป็น
4. เพิ่มฟิลด์คำนวณสำหรับ `group` และ `searchText` หากจำเป็น

### 2. Build HTML Shell

> Goal: ไฟล์เดียวที่โหลด assets ทั้งหมดจาก CDN

1. ใช้ `<!DOCTYPE html>`, `<html lang="en">`, `<meta charset="UTF-8">`
2. โหลด Tailwind CSS: `https://cdn.tailwindcss.com`
3. สำหรับโหมดโต้ตอบ โหลด Vue 3: `https://unpkg.com/vue@3/dist/vue.global.js`
4. ตั้งค่า `tailwind.config = { darkMode: 'class' }`
5. สร้าง `<div id="app">` และบล็อก `<script>` โดยใช้ `Vue.createApp`

### 3. Add Header And Theme Toggle

> Goal: ส่วนหัวชัดเจนพร้อมโหมดมืด/สว่าง

1. แสดงชื่อรายงานและคำบรรยายสั้นๆ
2. เพิ่มปุ่มสลับธีมที่สลับคลาส `dark` บน `<html>`
3. บันทึกการตั้งค่าใน `localStorage`
4. อ่าน `prefers-color-scheme` เมื่อโหลด
5. ใช้ตัวบ่งชี้สถานะที่ชัดเจน (เช่น badge หรือ icon) สำหรับประเภทรายงาน

### 4. Add Sticky Tabs And Key Findings

> Goal: เมนูนำทางระดับบนและสรุป

1. สร้างแถบแท็บแบบ sticky ด้วย `position: sticky; top: 0`
2. ใช้ `backdrop-blur` และพื้นหลังที่ตัดกัน
3. แท็บแรกแสดงการ์ด `Key Findings` ในกริดแบบ responsive
4. แต่ละแท็บมี badge แสดงจำนวนรายการ
5. ใช้ลำดับชั้นภาพที่ชัดเจน: title > subtitle > key findings > tabs

### 5. Build Interactive Table

> Goal: ตารางรองรับการโต้ตอบที่หลากหลาย

1. เรนเดอร์ตารางจาก data array โดยใช้ `v-for`
2. เพิ่มช่อง search ผูกด้วย `v-model`
3. เพิ่ม filter chips สำหรับ `Priority`, `Impact`, `Phase`, `Effort`
4. เพิ่มตัวควบคุม sort บนส่วนหัวคอลัมน์ (คลิกเพื่อสลับ asc/desc)
5. เพิ่มตัวเลือก group by (เช่น group by `Phase` หรือ `Priority`)
6. เพิ่มปุ่ม `Clear` เมื่อมี filter ที่ใช้งานอยู่
7. แสดงสถานะว่าง `No results` เมื่อ filter ส่งกลับศูนย์แถว
8. ใช้ computed `filteredRows` สำหรับ sort/filter/group/search

### 6. Add Per-Row Dropdown

> Goal: แต่ละแถวสามารถขยายเพื่อแสดงรายละเอียดเพิ่มเติมได้

1. เพิ่มลูกศรขยาย/ยุบบนแต่ละแถว
2. เมื่อขยาย ให้แสดงพาเนล dropdown ด้านล่างแถว
3. Dropdown มีอย่างน้อยสองคอลัมน์ (เช่น `UX/UI Sketch` และ `Plan`)
4. เนื้อหากระชับ; ใช้ `pre` หรือ `ul` สำหรับ sketches และ plans
5. ขยายได้ครั้งละหนึ่งแถวหากช่วยให้ UX ดีขึ้น

### 7. Add Summary And Diagrams

> Goal: ผลการวิเคราะห์ที่ไม่ใช่ตารางก็มองเห็นได้

1. เพิ่มส่วนสรุปสำหรับ DB/Files, API/Functions, Components
2. เพิ่ม UX/UI sketch และ architecture diagram แบบข้อความ
3. เก็บ diagrams ในบล็อก `<pre>` พร้อมฟอนต์ monospace
4. ใช้การ์ดและกริดสำหรับสรุป ไม่ใช่แค่ลิสต์ธรรมดา

### 8. Add Next Action

> Goal: รายงานจบด้วยข้อแนะนำที่ชัดเจน

1. เพิ่มส่วน `Next Action` ที่ด้านล่าง
2. ใช้ลิสต์แบบลำดับเลขหรือ bullet
3. อ้างอิงรายการที่มีความสำคัญสูงสุดด้วย `#`
4. ตกแต่ง next action ด้วยพื้นหลังหรือขอบที่โดดเด่น

### 9. Open In Browser

> Goal: ตรวจสอบว่ารายงานเรนเดอร์ถูกต้อง

1. บันทึกไฟล์ใน `reports/<report-name>.html` หรือ `.devin/reports/<report-name>.html`
2. รัน `/open-web` หรือ `Start-Process <path>` เพื่อเปิดในเบราว์เซอร์
3. ยืนยันว่าแท็บ, ธีม, sort, filter, dropdown ทำงานได้

## Rules

### 1. Single Self-Contained File

- ไม่มี build step ไม่มีการติดตั้ง package ภายนอก
- JS/CSS ทั้งหมดโหลดจาก CDN
- ข้อมูลฝังอยู่ใน `<script>`
- ขนาดไฟล์ต่ำกว่า 500 KB หากเป็นไปได้

### 2. Report Body Language

- ส่วนหัว, ผลการวิเคราะห์, สรุป, diagrams และ next action เป็นภาษาอังกฤษ
- เนื้อหาในเซลล์ตารางอาจเป็นภาษาของโปรเจกต์ (เช่น ไทย)
- ห้ามผสมภาษาในย่อหน้าเดียวกัน

### 3. Table Interactivity

- ค้นหาด้วยข้อความในทุกคอลัมน์ที่มองเห็น
- Filter ตาม `Priority`, `Impact`, `Phase`, `Effort`, `Difficult`
- Sort ตามคอลัมน์ใดก็ได้ (สลับ asc/desc)
- จัดกลุ่มแถวตามคอลัมน์ที่เลือก
- ปุ่มล้าง filters
- ไฮไลต์สถานะ filter/sort ที่ใช้งานอยู่
- แสดงสถานะว่างเมื่อไม่มีแถวที่ตรง

### 4. Per-Row Dropdown

- แต่ละแถวมีปุ่มขยายหรือแถวที่คลิกได้
- พาเนลที่ขยายมีอย่างน้อยสองคอลัมน์ที่มีป้ายกำกับ
- สำหรับผลลัพธ์ของ `/idea-features` คอลัมน์ควรเป็น `UX/UI Sketch` และ `Plan`
- เนื้อหา dropdown ใช้ข้อความกระชับหรือ code blocks

### 5. Design Tokens And Visual Hierarchy

- กำหนดชุด design token เล็กๆ ด้วย CSS variables สำหรับสี brand, success, warning, danger และ neutral
- ใช้สเกลระยะห่างที่สม่ำเสมอ: `4`, `8`, `12`, `16`, `24`, `32`, `48`
- รักษา font stack: `system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`
- ใช้ `text-sm` สำหรับตาราง, `text-base` สำหรับเนื้อหา, `text-2xl` สำหรับชื่อหน้า
- หลีกเลี่ยงใช้สี accent เกิน 6 สี

### 6. UX/UI Improvements

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

### 7. Responsive And Accessible

- เลื่อนแนวนอนสำหรับตารางกว้าง (`overflow-x-auto`)
- บนหน้าจอเล็ก ให้เรียง filters และแท็บในแนวตั้ง
- ใช้ `focus:outline-none focus:ring-2 focus:ring-blue-500` สำหรับองค์ประกอบที่โฟกัสได้
- ห้ามใช้สีเพียงอย่างเดียวเพื่อสื่อความหมาย; เพิ่มข้อความหรือ icon
- ใช้ `aria-label` สำหรับปุ่มที่มีเฉพาะ icon
- เคารพ `prefers-reduced-motion`
- รับประกันความตัดกันของสีที่เพียงพอทั้งในโหมดสว่างและโหมดมืด

### 8. Empty, Loading, And Error States

- แสดงข้อความ `No results` ที่เป็นมิตรเมื่อ filter ไม่ตรงเลย
- แสดง fallback `Loading...` ขณะ Vue เริ่มต้น (ใช้ `v-cloak`)
- จัดปุ่ม `Reset filters` ในสถานะว่าง
- หากข้อมูลหาย ให้แสดงข้อความชัดเจนแทนตารางที่เสีย

### 9. Micro-Interactions

- ไฮไลต์คอลัมน์ sort ที่ใช้งานอยู่
- แสดง count badge บนแท็บที่ใช้งานอยู่
- เคลื่อนไหวการขยายแถวด้วย transition `max-height` แบบง่าย (เคารพ `prefers-reduced-motion`)
- ใช้ hover transitions เล็กน้อยสำหรับปุ่มและแถว
- แสดง feedback `Copied` หรือ `Saved` สำหรับการ copy/export ใดๆ

### 10. Print And Share

- เพิ่มบล็อก CSS ที่เหมาะสำหรับการพิมพ์:
  - ซ่อนแถบแท็บ sticky, สลับธีม และ filters
  - ขยายแถว dropdown ทั้งหมดอัตโนมัติ
  - ใช้ข้อความสีดำบนพื้นหลังสีขาว
- รักษา URL และ code blocks ให้อ่านได้เมื่อพิมพ์

### 11. Safety

- ห้ามมี secrets, credentials หรือ paths ที่ละเอียดอ่อนที่ hardcode ไว้
- ใช้ relative paths สำหรับไฟล์โปรเจกต์
- ทำความสะอาดเนื้อหาที่ผู้ใช้ให้มาก่อนฉีดเข้า HTML
- ใช้ `DOMPurify` หากเรนเดอร์ HTML จากแหล่งที่ไม่น่าเชื่อถือ

## Expected Outcome

- ไฟล์ `.html` ไฟล์เดียวที่บันทึกในโปรเจกต์
- เนื้อหารายงานเป็นภาษาอังกฤษ, เซลล์ตารางเป็นภาษาของโปรเจกต์หากจำเป็น
- ตารางโต้ตอบได้พร้อม sort, filter, group, search และส่วนหัว sticky
- Dropdown รายแถวพร้อมสองคอลัมน์
- สลับธีม, แท็บ sticky, key findings, สรุป, diagrams, next action
- Responsive, accessible และเหมาะสำหรับการพิมพ์
- สถานะว่าง/loading/error ที่ชัดเจน
- ไฟล์เปิดในเบราว์เซอร์และเรนเดอร์ถูกต้อง
