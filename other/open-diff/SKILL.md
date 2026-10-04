---
name: open-diff
description: เปิดดู diff จาก PR, git, branch, หรือไฟล์สองไฟล์ ใน TanStack Start SPA (Solid) บน Bun
argument-hint: "[pr <n>] | [git <ref>] | [branch <base>..<head>] | [file <old> <new>] [--repo owner/repo]"
related:
  - follow-create-web
  - follow-lib-unocss
  - report-git-diff
  - deep-review
---

## Goal

เปิด diff จากหลายแหล่ง (GitHub PR, git ref, branch, หรือไฟล์สองไฟล์) ใน browser ด้วย SolidJS + TanStack Router (TanStack Start, SPA mode) บน Bun server โดยมี UX แบบ dim-focused และ close tab แล้ว terminal จะ prompt ให้เลือก action

## Scope

ใช้สำหรับ review diff แบบสวยงาม อ่านง่าย เน้นโค้ดที่เปลี่ยนแปลง โดยไม่ต้องพึ่ง GitHub web UI

รองรับ:
- GitHub PR: `open-diff pr <number> [--repo owner/repo]`
- Git ref vs HEAD: `open-diff git <ref> [--repo path]`
- Branch base..head: `open-diff branch <base>..<head> [--repo path]`
- ไฟล์สองไฟล์: `open-diff file <old> <new>`
- แสดง diff ด้วย `@pierre/diffs` (diffs.com)
- Syntax highlighting ด้วย Shiki
- Dark / light mode
- Sidebar file tree ด้านซ้าย (group ตาม directory, collapse ได้, file-type icons, status letter, +/- badges)
- Source tabs + params อยู่ใน nav (PR/Commit/Branch/File + dropdown เลือก PR/branches/tags/commits จาก `/api/prs`, `/api/refs`)
- Auto-load เมื่อสั่งจาก CLI
- Prompt ใน terminal เมื่อปิด tab
- Action buttons (Merge ▾ merge/squash/rebase, Approve, Comment, Checkout, Close) ส่งคำสั่งไป terminal ให้ execute
- CI status pill บน header (`gh pr checks`) — auto-poll ทุก 8s จนกว่า pending หมด
- Merge button ถูก block จนกว่า CI เขียวครบ (pending/fail → disabled พร้อม tooltip บอก check ที่พัง)
- Action log stream ไป terminal แบบ real-time (`[open-diff] $ cmd`, `[open-diff:out]`, `[open-diff:err]`) — เห็น merge progress ขณะ `run dev`
- File filter/search (กด `f` เพื่อ focus — อยู่ใน sidebar)
- Sidebar toggle (กด `b`)
- Unified/Split view toggle (`v`) และ line wrap toggle (`w`)
- Lazy load: split raw diff เป็น chunk ต่อไฟล์ แล้ว parse เฉพาะไฟล์ที่เลือก
- Status bar แสดง keyboard hints และไฟล์ปัจจุบัน
- Help overlay กด `?` แสดง keyboard shortcuts ทั้งหมด
- Keyboard: ←/→ หรือ [/] เปลี่ยน file, ↑/↓ หรือ j/k scroll diff, PageUp/PageDown, f filter, v view, w wrap, b sidebar, t theme, r reload, ? หรือ Shift+/ help, Esc ปิด menu/blur input

ไม่รองรับ:
- PR diff ที่ใหญ่เกิน GitHub API limit
- binary files

## Execute

### 1. Resolve Source

> Goal: ระบุ diff source

1. อ่าน argument แรกเป็น subcommand (`pr`, `git`, `branch`, `file`)
2. อ่าน argument `--repo` สำหรับ `pr`/`git`/`branch`
3. ถ้าไม่ระบุ `--repo` สำหรับ `pr` → ใช้ repo ปัจจุบันจาก `gh repo view --json nameWithOwner`
4. ถ้าไม่ระบุ subcommand → เปิด app แบบไม่มี default source

### 2. Prepare App Workspace

> Goal: ติดตั้งและ build แอป `open-diff` ถ้ายังไม่มี

1. สร้าง workspace ชั่วคราว เช่น `.devin/open-diff-app`
2. Copy ไฟล์ app จาก skill directory (`src/`, `package.json`, `tsconfig.json`, `uno.config.ts`, `vite.config.ts`, `bun.lock`) ไปยัง workspace
3. รัน `bun install` ใน workspace
4. รัน `bun run build` เพื่อสร้าง `dist/client/` (`_shell.html` + assets ซึ่ง server จะ serve โดยตรง)

### 3. Run And Open

> Goal: เปิด diff ใน browser

1. รัน `bun src/serve.ts <subcommand> [args] [--repo ...]` (หรือ `bun run start -- <subcommand> ...`)
2. รอ console แสดง URL (`open-diff running at http://localhost:<port>`)
3. server จะเปิด browser เองอัตโนมัติ → ยืนยันว่า tab เปิด; ถ้าไม่เปิดให้ใช้ `/open-web` หรือ OS command (Windows: `start`, macOS: `open`, Linux: `xdg-open`)
4. env vars: `OPEN_DIFF_PORT` กำหนด port (default random), `OPEN_DIFF_NO_OPEN=1` ไม่เปิด browser อัตโนมัติ

### 4. Verify

> Goal: ยืนยันว่า app ทำงาน

1. ตรวจสอบ header แสดง source ถูกต้อง
2. ตรวจ file strip ด้านบนมี file cards
3. ตรวจ main area แสดง diff พร้อม line numbers และ +/- markers
4. ลอง click เปลี่ยนไฟล์
5. ลองกด Dark/Light
6. ปิด tab แล้วตรวจสอบว่า terminal แสดง prompt หรือข้อความปิด tab
7. ถ้ามี error → ทำ `/resolve-errors`

## Rules

### 1. Source Parsing

- `pr <number>` สำหรับ GitHub PR
- `git <ref>` สำหรับ `git diff <ref>..HEAD`
- `branch <base>..<head>` สำหรับ `git diff <base>..<head>`
- `file <old> <new>` สำหรับ `git diff --no-index <old> <new>`
- `--repo` รับ `owner/repo` สำหรับ `gh` หรือ path สำหรับ `git`

### 2. Workspace Safety

- ติดตั้ง dependencies เฉพาะใน workspace ชั่วคราว
- ไม่แก้ไข `package.json` ของ repo หลัก
- ลบ workspace ชั่วคราวหลังใช้เสร็จถ้า user ไม่ขอเก็บ

### 3. Build Requirement

- ต้องมี Bun ติดตั้ง
- ต้องมี `gh` CLI สำหรับ PR
- ต้องมี `git` สำหรับ git/branch/file diff
- ติดตั้ง dependencies ด้วย `bun install`
- build ด้วย `bun run build` (`bunx vite build`)
- stack จาก `package.json`: `@pierre/diffs` ^1.4.1, `shiki` 4.0.0, `unocss` ^66.10.2 + `@unocss/preset-wind4` ^66.10.0, `vite` ^7.1.0, `@tanstack/solid-start` ^1.168.50 (verified 2026-09-12)
- API อยู่ที่ `src/server/api.ts` (`handleApi`) — expose ผ่าน server route `src/routes/api.$.ts` (vite dev) และ Bun wrapper `src/serve.ts` (prod)
- `src/serve.ts` serve `dist/client` statics + `_shell.html` fallback และ heartbeat/prompt — อย่าสร้าง `src/server.ts` (Start จองชื่อนี้เป็น custom server entry)

### 4. UX Requirements

- ใช้ UnoCSS `presetWind4` จาก `@unocss/preset-wind4`
- ใช้ shortcuts (`btn`, `input`, `panel`, `dim`, `file-item`)
- ใช้ CSS variables สำหรับ dark/light theme
- ใช้ Shiki สำหรับ syntax highlighting
- แยก add/del/context ด้วยสี/background ชัดเจน
- แสดง +/- markers
- แสดง stats +additions/-deletions/files บน header
- แสดง PR metadata (title, author avatar, state) เมื่อโหลด PR

### 5. Close Tab Behavior

- Frontend ส่ง heartbeat ไป `/api/ping` ทุก 2 วินาที
- Frontend ส่ง `/api/close` ผ่าน `navigator.sendBeacon` เมื่อ `beforeunload`
- เมื่อปิด tab (หรือหยุด ping เกิน 5 วินาที) server จะแสดง prompt ใน terminal ให้เลือก:
  - `(r)eopen` → เปิด browser ใหม่
  - `(q)uit` → ปิด server
  - `(c)ontinue` → ทำงานต่อ
- ถ้าไม่ใช่ TTY → server จะรอคำสั่งต่อไป
- ถ้า user ปิด tab แล้ว process ยังไม่ตาย → ตรวจสอบว่ามี tab อื่นเปิดอยู่

### 6. Use Existing Skills

- `gh` CLI สำหรับ PR
- `/follow-lib-unocss` สำหรับ styling
- `/follow-create-web` (solid-tanstack-router) สำหรับ stack
- /open-web สำหรับเปิด browser
- /report-git-diff สำหรับสร้างรายงาน diff
- /deep-review สำหรับ review diff

## Expected Outcome

- Server `open-diff` รันและเปิด tab ใน browser
- แสดง diff source, file list, และ diff view
- มี line numbers, +/- markers, syntax highlight
- สลับ dark/light ได้
- สลับไฟล์ได้
- ปิด tab แล้ว terminal แสดง prompt ให้เลือก action
- ไม่มีไฟล์หรือ dependency ใหม่ใน repo หลัก
