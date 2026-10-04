---
name: draw-ansi
description: วาด/ปรับ ANSI box-drawing ให้กล่องภายนอกมีขนาดเท่ากัน ไม่เพี้ยน
argument-hint: "[input]"
related:
  - draw-svg-image
  - draw-excalidraw
  - draw-tldraw
---

## Goal

สร้างหรือปรับ ANSI box-drawing ให้มีกล่องภายนอก (outer box) ทีกว้างเท่ากันทุกบรรทัด ขอบขวาตรงกัน และไม่เพี้ยนจากเนื้อหาภายใน

## Scope

ใช้สำหรับ:
- สร้าง ` ```text ` codeblock สำหรับ README UI/CLI sketch
- ตรวจสอบและซ่อม ANSI drawing ทีมีบรรทัดไม่เท่ากัน
- ห่มเนื้อหา (text หรือ nested box) ด้วย outer box ทีขนาดคงที

## Execute

### 1. Install / Run

> Goal: รัน `draw-ansi` script

```bash
bunx /path/to/draw-ansi/scripts/draw-ansi.ts [options] < input.txt
bunx /path/to/draw-ansi/scripts/draw-ansi.ts --width 60 --title "My App" < input.txt
bunx /path/to/draw-ansi/scripts/draw-ansi.ts --fix --width 60 existing-box.txt
```

### 2. Input Modes

> Goal: รองรับทุกรูปแบบ input ของ box

1. Plain lines: บรรทัดปกติ ไม่มี border → สคริปต์จะห่มด้วย outer box
2. Existing box: บรรทัดเริ่มต้นด้วย `│` หรือ `┌`/`└` → สคริปต์จะลอง detect กล่องเดิม แล้ว wrap ใหม่

### 3. Output Modes

> Goal: รองรับทุกรูปแบบ output ของ box

- `--format text` (default): ข้อความธรรมดา เอาไปใส่ ` ```text ` block
- `--format markdown`: ห่มด้วย ` ```text ` block พร้อม

### 4. Options

> Goal: ระบุ options ที่รองรับ

| Option | Description | Default |
|--------|-------------|---------|
| `--width` | ความกว้างภายในกล่อง (ไม่รวม border) | 58 หรือ auto |
| `--title` | ใส่ title บรรทัดแรก | none |
| `--fix` | ซ่อม existing box ให้ขนาดเท่ากัน | false |
| `--format` | `text` หรือ `markdown` | text |

## Rules

### 1. Uniform Width

- ทุกบรรทัดใน output ต้องมีความกว้างเท่ากันพอดี
- ถ้าเนื้อหายาวเกิน `--width` ให้ตัด (truncate) หรือเตือน
- ถ้าเนื้อหาสั้นกว่า `--width` ให้ pad space ทางขวา

### 2. Outer Box

- ขอบบน: `┌` + `─` × width + `┐`
- ขอบล่าง: `└` + `─` × width + `┘`
- ขอบซ้าย/ขวา: `│` + content (padded) + `│`

### 3. Nested Box Support

- ถ้าภายในมี nested box ที่กว้างกว่า `--width` ให้ expand outer box ให้พอ หรือ warn
- ไม่ทำให้ nested box หด/เพี้ยน ยกเว้นต้อง truncate

### 4. No Distortion

- ไม่เพี้ยนจากตัวอักษรพิเศษหรือ emoji
- ไม่ใช้ ` ```ansi ` block
- output พร้อมใช้ใน README ` ```text ` block ทันที
- ใช้ /draw-svg-image ถ้าจำเป็น
- ใช้ /draw-excalidraw ถ้าจำเป็น
- ใช้ /draw-tldraw ถ้าจำเป็น

## Expected Outcome

- บรรทัดทุกบรรทัดใน ANSI box มีความกว้างเท่ากัน
- ขอบขวาตรงกัน
- outer box ไม่เพี้ยนจากเนื้อหาภายใน
- สามารถนำไปวางใน README ได้ทันที
