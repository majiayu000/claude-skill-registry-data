---
name: convert-svg
description: แปลงรูปภาพ bitmap เป็น SVG ด้วย bunx CLI
argument-hint: "[input]"
related:
  - convert
  - idea
  - draw-svg-image

---

## Goal

แปลงรูปภาพ bitmap (PNG/JPG) เป็น SVG vector ด้วย `bunx` CLI

## Scope

- รับ input เป็นไฟล์รูปภาพ
- ใช้ potrace-based CLI สำหรับ tracing
- รองรับ output path และ optimization

## Execute

### 1. Identify Input

> Goal: ตรวจสอบ input

1. รับ input path จาก user
2. ตรวจสอบว่าไฟล์มีอยู่และเป็น image (png/jpg/jpeg/gif/bmp)
3. ตรวจสอบขนาดไฟล์ ถ้าใหญ่เกินไป ให้ resize ก่อนหรือเตือน user

### 2. Choose CLI

> Goal: เลือก tool ทีพร้อมใช้

1. Primary: `bunx images-to-svg convert <input>`
   - รองรับทั้งไฟล์และ directory
   - ใช้ sharp, potrace, svgo
2. Fallback: `bunx potrace-cli <input> -o output.svg`
3. Fallback: `bunx potrace <input> -s -o output.svg`
4. สุดท้าย: ติดตั้ง `sharp` + `potrace` แล้วเขียน Node/Bun script

### 3. Run Conversion

> Goal: แปลง bitmap เป็น SVG

1. รันคำสั่งพร้อม output path
2. ถ้า input เป็น directory → แปลงทั้งหมด
3. ตรวจสอบ output file

### 4. Optimize And Validate

> Goal: ให้ SVG ถูกต้องและพร้อมใช้

1. ใช้ `bunx svgo` optimize output ถ้าต้องการ
2. ตรวจสอบ SVG เปิดได้ด้วย browser
3. รายงาน input/output paths

## Rules

### 1. Quality

- Tracing ทำงานดีกับรูปทีมี contrast สูง
- ถ้า input เป็น photo สีสัน → แจ้ง user ว่า SVG อาจไม่สมจริง
- สำหรับ logo/line art → ผลดีทีสุด

### 2. Color

- potrace default เป็น monochrome
- ถ้าต้องการ color ให้ใช้ `images-to-svg` หรือขั้นตอนหลัง tracing

### 3. Fallback

- ถ้า tool แรก fail → ลอง `potrace-cli`
- ถ้า fail อีก → ใช้ script ด้วย `sharp` + `potrace`

- ใช้ /convert-git-submodules ถ้าจำเป็น
- ใช้ /idea-convert-my-global-cli-to-skills ถ้าจำเป็น
- ใช้ /convert-files-format ถ้าจำเป็น
- ใช้ /draw-svg-image ถ้าจำเป็น

## Expected Outcome

- ไฟล์ `.svg` ถูกสร้างจาก bitmap
- SVG สามารถแก้ไขและ scale ได้
- รายงาน tool ทีใช้และ output path
