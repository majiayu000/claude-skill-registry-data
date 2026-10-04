---
name: capture
description: Capture หลักฐานภาพ/วิดีโอ — web, component, terminal, app หรือ all-routes ผ่าน CLI เดียว
argument-hint: "<web|component|terminal|app|all> [options]"
related:
  - use-agent-browser
  - run-dev
  - deep-review

---

## Goal

Capture ภาพหรือวิดีโอหลักฐานตาม target ผ่าน Bun CLI ตัวเดียว — หน้าเว็บ, component, terminal output, app window หรือทุก route x device — สำหรับ documentation, debugging และ testing (merged จาก `capture-web`, `capture-component`, `capture-terminal`, `capture-app`, `capture-all-components-all-routes`)

## Scope

CLI อยู่ที่ `src/` (Bun/TypeScript, entry `src/presentation/cli.ts`) — ใช้ได้กับทุก project โดยไม่ต้องติดตั้ง dependency ฝั่ง project:

```bash
bun <skill-dir>/src/presentation/cli.ts <mode> [options]
```

| Mode | ทำอะไร | Guide |
|------|--------|-------|
| `web` | screenshot/PDF หน้าเว็บเดียว ผ่าน `agent-browser` | [Web](#capture-web) |
| `component` | screenshot element เดียว (CSS selector) บน URL | [Component](#capture-component) |
| `terminal` | render output ของ command เป็น PNG/SVG/HTML | [Terminal](#capture-terminal) |
| `app` | screenshot หน้าต่าง/จอ OS-level (Windows PowerShell) + app sweep workflow | [App](#capture-app) |
| `all` | ทุก route x ทุก device size ในรันเดียว + manifest | [All](#capture-all) |

## Execute

### 1. Select Mode

> Goal: ระบุ capture mode และอ่าน guide ของ mode นั้น

1. อ่าน mode จาก argument — ถ้าไม่ระบุ → ถาม user
2. อ่าน `## Mode Guides` ของ mode นั้นแล้วทำตาม Execute + Rules — ไม่ execute จากตารางนี้โดยตรง
3. ถ้า tool ต้องการยังไม่ติดตั้ง (`agent-browser`, `terminal-shot`, …) → ติดตั้งตาม mode guide หรือ `/download-program`

### 2. Capture

> Goal: ได้ภาพ/วิดีโอตาม mode

1. เตรียม target: เปิด URL/app/terminal ที่ต้องการ (`/run-dev` ถ้าต้อง start server)
2. รัน CLI subcommand ตาม mode พร้อมตั้งชื่อไฟล์สื่อความหมาย
3. บันทึกไปตำแหน่งตาม mode guide (`public/screenshots/`, `docs/screenshots/`, หรือ `.devin/temp/report/<workspace>/captures-<ts>/`)

### 3. Verify And Report

> Goal: ภาพใช้ได้จริงและถูกอ้างถึง

1. ตรวจว่าไฟล์สร้างสำเร็จและไม่ว่าง (เปิดดูด้วย `read` ถ้าเป็นภาพ)
2. `all` mode → เช็ค `manifest.json` errors ก่อนเสมอ
3. รายงาน path และขนาดไฟล์ — ถ้าใช้เป็น bug evidence ให้บันทึกใต้ `.devin/bugs/` พร้อม git state และ env context

## Rules

- ตั้งชื่อไฟล์สื่อความหมาย มีวันที่ถ้าเป็น evidence
- ไม่ capture หน้าจอที่มี secrets/credentials โดยไม่จำเป็น — ถ้า target ต้อง auth ให้ถาม user ก่อน
- แจ้ง path ของไฟล์ที่ capture เสมอ
- ใช้ /run-dev, /use-agent-browser, /resolve-errors, /deep-review ถ้าจำเป็น

## Mode Guides

| Mode | Reference |
|------|-----------|
| web | [references/mode-web.md](references/mode-web.md) |
| component | [references/mode-component.md](references/mode-component.md) |
| terminal | [references/mode-terminal.md](references/mode-terminal.md) |
| app | [references/mode-app.md](references/mode-app.md) |
| all | [references/mode-all.md](references/mode-all.md) |

## Expected Outcome

- ไฟล์ภาพ/วิดีโอ/PDF หลักฐานพร้อมใช้ ตาม mode ที่ระบุ
- `all` mode ให้ `manifest.json` สรุปผล + errors พร้อมใช้ต่อใน `/deep-review` หรือ report
