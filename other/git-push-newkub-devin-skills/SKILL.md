---
name: git-push
description: Push commits จาก local repository และ git submodules ไปยัง remote repository อย่างปลอดภัย
argument-hint: "[scope]"
related:
  - git-commit
  - refactor-commit
  - update-github-metadata
  - resolve-errors

---

## Goal

Push commits จาก local repository และ git submodules ไปยัง remote repository อย่างปลอดภัย

## Scope

ใช้สำหรับ push commits ไปยัง remote repository ทั้ง root และ git submodules

## Execute

### 1. Check Status And Commits

> Goal: Check Status And Commits

- ทำ `git branch --show-current`, `git status`, และ `git submodule status` เพื่อดูสถานะปัจจุบัน
- ทำ `git log --oneline origin/<branch>..HEAD` เพื่อดู commits ที่จะ push
- พิจารณา `/refactor-commit` ก่อน push เสมอ — ตรวจสอบว่า commits มีขนาดเหมาะสม message ชัดเจน และ logical order — ถ้า commits ใหญ่เกินไป หรือ message ไม่ชัด ให้ทำ `/refactor-commit` ก่อน push

### 2. Push

> Goal: Push

- ทำ `git push origin <branch>` และ `git submodule foreach --recursive git push origin <branch>` — ห้ามใช้ `--no-verify` หรือ flag ที่ข้าม git hooks ทุกประเภท
- ถ้า git hook แจ้ง error ให้แก้ที่ root cause ไม่ข้าม hook — ทำ `/resolve-errors` ถ้าจำเป็น
- ถ้า push ถูก reject ให้หยุดและแจ้งผู้ใช้ ไม่ force push

### 3. Validate

> Goal: Validate

- ทำ `git log --oneline origin/<branch> -5` เพื่อยืนยันว่า commits ปรากฏบน remote แล้ว
- ทำ `git status` เพื่อยืนยันว่า local และ remote sync กัน

### 4. Check GitHub Actions

> Goal: Check GitHub Actions

- ทำ `gh workflow list` เพื่อตรวจสอบว่ามี GitHub Actions ใน repo ไหม
- ถ้ามี ให้ทำ `/resolve-github-actions-fails` เพื่อตรวจสอบและรันจนกว่าจะผ่าน

### 5. Update GitHub Repo Metadata

> Goal: Update GitHub Repo Metadata

อัปเดต repository metadata ให้สะท้อน project จริง ใช้ `/update-github-metadata` เป็น canonical workflow

1. ทำ `/update-github-metadata` เพื่ออัปเดต description, homepage, topics, default branch
2. ตรวจสอบว่า `package.json` มี `repository`, `homepage`, `bugs`, `license` fields ครบ
3. ถ้าเป็น public repo ให้ตั้ง `--enable-issues=true` และ `--enable-wiki=false` (ใช้ docs แทน)

### 6. Open Repo

> Goal: Open Repo

- ทำ `git remote get-url origin` เพื่อดู remote URL
- แปลง SSH URL เป็น HTTPS URL แล้วทำ `/open-web` เพื่อเปิด repo ใน browser

### 7. Ensure Repository Ready (Optional)

> Goal: Ensure Repository Ready (Optional)

ทำเฉพาะเมื่อ `git` แจ้ง error ว่าไม่มี repository หรือไม่มี remote

- ถ้าไม่มี `.git` ให้ทำ `git init`, `git add -A`, `git commit -m "Initial commit"`, และทำ `/follow-gitignore`
- ถ้าไม่มี remote ให้ทำ `gh repo create <repo-name> --private --source=. --remote=origin --push` โดยใช้ชื่อโฟลเดอร์เป็น repo name

## Rules

### 1. Repository Initialization

- เป็น optional step ทำเฉพาะเมื่อ `git` แจ้ง error
- ถ้าไม่มี remote ให้สร้างด้วย `gh repo create` และเป็น `--private` เบื้องต้น
- ใช้ชื่อโฟลเดอร์ปัจจุบันเป็น repo name อัตโนมัติ
- ทำ `/follow-gitignore` หลัง `git init` เพื่อให้แน่ใจว่า `.gitignore` ครบถ้วน

### 2. Safety

- ห้ามใช้ `--no-verify` หรือ flag อื่นใดที่ข้าม git hooks (เช่น `--no-verify`, `HOOK_SKIP=true`) — git hooks ต้องทำงานทุกครั้ง
- ถ้า git hook แจ้ง error ให้แก้ที่ root cause ไม่ข้าม hook — ทำ `/resolve-errors` ถ้าจำเป็น
- พิจารณา `/refactor-commit` ก่อน push เสมอ เพื่อให้ commits สะอาดและเหมาะสม
- ไม่ force push โดยไม่จำเป็น
- ถ้า push ถูก reject ให้หยุดและแจ้งผู้ใช้ ไม่ force push

### 3. Submodules

- ต้อง push ทั้ง root และ submodules เสมอ
- ใช้ `git submodule foreach --recursive` สำหรับ operations ทั้งหมด

### 4. GitHub Repo Metadata

- ใช้ `/update-github-metadata` เป็น canonical workflow สำหรับ metadata
- ตั้งค่า metadata ทุกครั้งหลังสร้าง repo ใหม่หรือ push ครั้งแรก
- ตรวจสอบ `package.json` มี `repository`, `homepage`, `bugs`, `license` ครบ
- ถ้าเป็น public repo ให้ตั้ง `--enable-issues=true` และ `--enable-wiki=false`

- ใช้ /git-commit ถ้าจำเป็น
- ใช้ /git-commit-and-push ถ้าจำเป็น

## Expected Outcome

- Repository พร้อม push แม้ยังไม่มี `.git` หรือ remote
- Commits ถูก push ไปยัง remote สำเร็จ (ทั้ง root และ submodules)
- Local และ remote sync กัน
- GitHub Actions ผ่านทั้งหมด
- Repo เปิดใน browser อัตโนมัติหลัง push สำเร็จ
- แสดง URL commit บน remote ที่กดแล้วเปิดได้
