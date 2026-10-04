---
name: git-commit
description: Commit ทุกไฟล์ที่เปลี่ยนแปลงด้วย conventional commits
argument-hint: "[scope]"
related:
  - run-check
  - run-verify
  - follow-tool-hk
  - list-git
  - refactor-commit
  - deep-review
  - ship-to-dev-branch

---
## Goal

Commit ทุกไฟล์ที่มีการเปลี่ยนแปลงใน global devin skills directory ตามมาตรฐาน conventional commits

## Scope

- variants: no-verify/selected-files/at-devin-global-skills/commit-quality อยู่ใน workflows; `and-push` ย้ายออกเป็น top-level `/git-commit-and-push`; `at-devin-global-skills` มี top-level alias `/git-commit-at-devin-global-skills`

ใช้สำหรับ commit changes ใน `C:\Users\Veerapong\AppData\Roaming\devin\skills` เท่านั้น

- ถ้าต้องการรัน pre-commit validation ก่อน commit ใน devin global skills ให้ใช้ `/git-commit at-devin-global-skills`

## Execute

### Workflows

| Domain                   | Workflow |
|--------------------------|----------|
| `no-verify`              | `workflows/no-verify/SKILL.md` — commit ข้าม pre-commit hooks ด้วย `--no-verify` |
| `selected-files`         | `workflows/selected-files/SKILL.md` — commit เฉพาะไฟล์ที่เลือก ไม่ใช้ `git add .` |
| `and-push`               | `/git-commit-and-push` — top-level skill จริง (commit + push + resolve CI/CD) |
| `at-devin-global-skills` | `workflows/at-devin-global-skills/SKILL.md` — pre-commit validation สำหรับ devin global skills (alias: `/git-commit-at-devin-global-skills`) |
| `commit-quality`          | `workflows/commit-quality/SKILL.md` — lint commit messages ตาม conventional commits |

### 1. Navigate To Global Devin Skills

> Goal: Navigate To Global Devin Skills

เปลี่ยน directory ไปยัง global devin skills

1. เปลี่ยน directory ไปยัง `C:\Users\Veerapong\AppData\Roaming\devin\skills`
2. ตรวจสอบว่าอยู่ใน directory ที่ถูกต้องด้วย `pwd`

### 2. Check Git Status

> Goal: Check Git Status

ตรวจสอบสถานะของ repository

1. รัน `git status --porcelain` เพื่อดูไฟล์ที่มีการแก้ไขทั้งหมด
2. ตรวจสอบว่าอยู่ใน repository ที่ถูกต้อง

### 3. Stage All Changes

> Goal: Stage All Changes

Stage ทุกไฟล์ที่มีการเปลี่ยนแปลง

1. รัน `git add .` เพื่อ stage ทุกไฟล์
2. ตรวจสอบด้วย `git diff --cached` ว่าไฟล์ที่ stage ถูกต้อง

### 4. Determine Commit Type

> Goal: Determine Commit Type

เลือก conventional commit type ที่เหมาะสม

1. ดู Rules ส่วน Commit Types
2. เลือก type ตามการเปลี่ยนแปลง:
   - feat: เพิ่ม skill ใหม่
   - fix: แก้ไข skill
   - docs: แก้ไขเอกสารหรือคำอธิบาย
   - refactor: refactor skill
   - chore: ปรับปรุง configuration หรือ structure

### 5. Write Commit Message

> Goal: Write Commit Message

เขียน commit message ตาม conventional commits format

1. ดู Rules ส่วน Commit Message Format และ Body
2. ใช้รูปแบบ `<type>: <subject>`
3. subject สั้นกระชับไม่เกิน 72 ตัวอักษร
4. ใช้ imperative mood (เช่น add ไม่ใช่ added)
5. ใช้ภาษาอังกฤษเท่านั้น
   - ถ้าเนื้อหาหรือ context ทำให้คิดเป็นภาษาอื่น ให้แปล subject และ body เป็นภาษาอังกฤษก่อน commit

### 6. Execute Commit

> Goal: Execute Commit

ดำเนินการ commit

1. รัน `git commit -m "<message>"` หรือ `git commit`
2. ตรวจสอบผลลัพธ์จาก git commit
3. ถ้ามี error: แก้ไขแล้วลองอีกครั้ง

### 7. Verify Commits

> Goal: Verify Commits

ตรวจสอบความถูกต้องของ commits

1. รัน `git log --oneline -5` เพื่อดู commits ล่าสุด
2. ตรวจสอบว่า commit messages สอดคล้องกับ conventional commits และเป็นภาษาอังกฤษ
3. ตรวจสอบว่าไม่มีไฟล์ที่ยังไม่ commit เหลืออยู่
4. รัน `git status` เพื่อยืนยันว่า working directory สะอาด

## Rules

### Commit Message Format

ใช้รูปแบบ conventional commits

- ใช้รูปแบบ `<type>: <subject>`
- subject ไม่ต้องขึ้นต้นด้วยตัวพิมพ์ใหญ่หรือจบด้วยจุด
- สั้นกระชับไม่เกิน 72 ตัวอักษร
- ใช้ imperative mood (เช่น add ไม่ใช่ added)
- ใช้ภาษาอังกฤษเท่านั้น
  - ถ้าเนื้อหาหรือ context ทำให้คิดเป็นภาษาอื่น ให้แปล subject และ body เป็นภาษาอังกฤษก่อน commit

### Commit Types

เลือก type ที่เหมาะสมกับการเปลี่ยนแปลง

- feat: เพิ่ม skill ใหม่
- fix: แก้ไข skill
- docs: แก้ไขเอกสารหรือคำอธิบาย
- refactor: refactor skill
- chore: ปรับปรุง configuration หรือ structure

### Body

อธิบายเหตุผลและ context เพิ่มเติม

- อธิบายเหตุผลและ context
- แยกจาก subject ด้วยบรรทัดว่าง
- ใช้ bullet points สำหรับหลายรายการ

- ใช้ /run-check ถ้าจำเป็น
- ใช้ /run-verify ถ้าจำเป็น
- ใช้ /follow-tool-hk ถ้าจำเป็น (เฉพาะ repo ที่ไม่ใช้ moonrepo — moon repos ใช้ `vcs.hooks`)
- ใช้ /list-git-commit ถ้าจำเป็น
- ใช้ /refactor-commit ถ้าจำเป็น
- ใช้ /deep-review ถ้าจำเป็น
- ใช้ /ship-to-dev-branch ถ้าจำเป็น

## Merged Details

### at-devin-global-skills

##### Goal

Commit ทุกไฟล์ที่เปลี่ยนแปลงใน devin global skills repo หลังจาก `review-devin-global-harness`, `deep-validate` และ `review-devin-global-harness` ผ่านเกณฑ์

##### Scope

ใช้สำหรับ `%APPDATA%\devin\skills` บน Windows หรือ `~/.devin/skills` บน Unix

- เป็น wrapper รอบ `/git-commit` ที่เพิ่ม pre-commit validation สำหรับ devin global skills
- ไม่ใช่ tool สำหรับ push, deploy หรือ merge — ถ้าต้องการ push ให้ใช้ `/git-commit-and-push` หลังจากนี้
- ไม่แก้ไข code ให้เอง — ถ้า validation พบ Critical/High ให้ stop และส่งต่อ `/resolve-errors`

##### Execute

###### 1. Navigate And Check Status

> Goal: ตรวจสอบว่าอยู่ใน repo ที่ถูกต้องและมี changes จริง

1. เปลี่ยน working directory ไปยัง `%APPDATA%\devin\skills`
2. รัน `git status --porcelain`
3. ถ้าไม่มี changes ที่จะ commit → stop และ report `no changes to commit`

###### 2. Review Devin Global Skills

> Goal: ตรวจ conventions และ cross-skill consistency

1. ทำ `/review-devin-global-harness`
2. บันทึก findings, severity และ category
3. ถ้ามี Critical หรือ High → stop, รายงานผล, แนะนำ `/resolve-errors`

###### 3. Deep Validate

> Goal: ตรวจสอบความถูกต้องละเอียดของ skill ที่เปลี่ยนแปลง

1. ทำ `/deep-validate` บน scope ที่เปลี่ยนแปลง
2. บันทึก findings พร้อม severity
3. ถ้ามี Critical หรือ High → stop, รายงานผล, แนะนำ `/resolve-errors`

###### 4. Check Skill References

> Goal: ตรวจหา broken references และ circular dependencies ระหว่าง skills

1. ทำ `/review-devin-global-harness`
2. ถ้าพบ broken references → stop, แนะนำ `/update-references` แล้วรอผู้ใช้แก้
3. ทำ `/follow-tool-madge` ถ้ามีการแก้ไข `related`
4. ถ้าผ่าน → ดำเนินต่อ

###### 5. Stage Changes

> Goal: เตรียมไฟล์สำหรับ commit อย่างปลอดภัย

1. รัน `git diff --name-only` เพื่อดูไฟล์ที่จะ stage
2. รัน `git add .` ภายใน `%APPDATA%\devin\skills`
3. รัน `git diff --cached --stat` เพื่อตรวจสอบ
4. ถ้ามีไฟล์นอก scope หรือไฟล์ที่ไม่ต้องการ commit → แยกออกก่อน

###### 6. Commit

> Goal: สร้าง commit ตาม conventional commits

1. ทำ `/git-commit`
2. ถ้า `git-commit` ล้มเหลว → อ่าน error, แก้ไข, แล้วลองใหม
3. ถ้าต้องการ scope เฉพาะ skill ใด skill หนึ่ง → ใช้ `/git-commit selected-files` แทน

###### 7. Verify

> Goal: ยืนยันว่า commit ถูกต้องและ working directory สะอาด

1. รัน `git log --oneline -5`
2. รัน `git status --porcelain`
3. ถ้า working directory สะอาด → รายงานสำเร็จ
4. ถ้ามีไฟล์ค้าง → รายงานและแนะนำ action ถัดไปผ่าน `/suggest-next-action`

##### Rules

###### 1. Repo Scope

- ใช้เฉพาะใน devin global skills repo
- ไม่ commit ไฟล์นอก `%APPDATA%\devin\skills` หรือ `~/.devin/skills`

###### 2. Validation Gate

- ต้องผ่าน `/review-devin-global-harness`, `/deep-validate` และ `/review-devin-global-harness` ก่อน commit
- ถ้ามี Critical/High findings ให้ stop และส่งต่อ `/resolve-errors`
- ไม่ใช้ `--no-verify` เพื่อ bypass validation

###### 3. Commit Discipline

- ใช้ `/git-commit` เพื่อรักษามาตรฐาน conventional commits
- subject ไม่เกิน 72 ตัวอักษร
- ใช้ภาษาอังกฤษเท่านั้นใน commit message

###### 4. Post-Commit

- ถ้าต้องการ push ให้ใช้ `/git-commit-and-push`
- ถ้าต้องการ refactor history ให้ใช้ `/refactor-commit`
- ถ้ามี findings หลัง commit ให้ใช้ `/resolve-errors`

- ใช้ `/run-check` ถ้าจำเป็น
- ใช้ `/report` ถ้าต้องการสรุปผล
- ใช้ `/suggest-next-action` เสมอหลังจบ

##### Expected Outcome

- ทุก skill ที่เปลี่ยนแปลงได้รับการ review/validate/check references ก่อน commit
- Commit ถูกสร้างด้วย conventional commits
- Working directory สะอาด
- ไม่มี Critical/High findings ค้าง
- มีรายงานสรุปผลการ validate และ commit

### commit-quality

##### Goal

ตรวจ commit messages ใน repo ว่าตรง conventional commits และมีคุณภาพ — หา messages ที่ผิด format, กำกวม, ยาวเกิน หรือไม่บอก intent

##### Scope

- ใช้กับ git history ของ repo ปัจจุบันหรือ range ที่ระบุ (`HEAD~10`, `main..feature`)
- ครอบคลุม format check (type, scope, subject) และ quality heuristics (imperative, specificity)
- Read-only: รายงานเท่านั้น ไม่ rewrite history

##### Execute

###### 1. Select Commit Range

> Goal: รู้ว่าตรวจ commits ไหน

1. รับ `range` จาก argument — default: `HEAD~20..HEAD` หรือ commits ที่ยังไม่ push
2. รัน `git log --format='%h|%s|%an|%ad' <range>` เพื่อดึง messages
3. ข้าม merge commits และ bot commits ตาม convention ของ repo

###### 2. Check Format Compliance

> Goal: ตรง conventional commits spec

1. Pattern: `<type>(<scope>)?: <subject>` — types: `feat`, `fix`, `docs`, `refactor`, `chore`, `test`, `perf`, `build`, `ci`, `style`
2. Flag `bad-format` ถ้าไม่ match pattern
3. Flag `bad-type` ถ้า type ไม่อยู่ใน list ที่ repo ใช้
4. Flag `long-subject` ถ้า subject >72 ตัวอักษร
5. Flag `capitalized`/`trailing-dot` ตาม convention

###### 3. Check Message Quality

> Goal: message บอก intent จริง

1. Flag `vague` สำหรับ subjects เช่น `update`, `fix bug`, `changes`, `wip`, `misc`
2. Flag `non-imperative` ถ้าใช้ past tense (`added`, `fixed`)
3. Flag `no-context` ถ้า commit ใหญ่ (diff หลายไฟล์) แต่ subject สั้นเกินและไม่มี body
4. Flag `mismatch` ถ้า type ไม่ตรง diff (เช่น `docs:` แต่แก้ source code)

###### 4. Suggest Rewrites

> Goal: เสนอ message ที่ดีกว่า

1. สำหรับ commits ที่ flag → draft conventional message จาก diff summary
2. ใช้ `git show --stat <sha>` เพื่อเข้าใจ change จริง
3. เสนอ `<type>(<scope>): <imperative subject>` ต่อ commit

###### 5. Report

> Goal: สรุป quality และแนวทางแก้

1. ทำ `/report` คอลัมน์: `No.`, `SHA`, `Message`, `Issues`, `Suggested`
2. สรุป compliance rate และ issue breakdown
3. แนะนำ `/refactor-commit` ถ้าต้อง rewrite (เฉพาะ commits ที่ยังไม่ push)
4. แนะนำ `commitlint` + git hooks ถ้าต้องการ enforce ต่อเนื่อง — repo ที่มี `.moon/workspace.yml` → `vcs.hooks` ของ moon (`/follow-tool-moonrepo` Step 7); repo อื่น → `/follow-tool-hk`

##### Rules

###### 1. Read-Only

- ไม่ rebase, amend หรือ rewrite history ใน skill นี้
- เสนอ suggestion เท่านั้น — rewrite ผ่าน `/refactor-commit` เมื่อ user สั่ง

###### 2. Repo Convention

- ใช้ types/scopes ที่ repo ใช้จริงจาก `git log` — ไม่บังคับ set มาตรฐานถ้า repo มีของตัวเอง
- ถ้า repo ไม่ใช้ conventional commits เลย → รายงาน quality เท่านั้น ไม่ flag format

###### 3. Actionable

- ทุก flag ต้องมี suggested rewrite หรือเหตุผลที่ชัด
- ไม่ flag bot commits (`dependabot`, `renovate`) เว้นแต่ repo บังคับ format

- ใช้ /list-git-commit ถ้าจำเป็น
- ใช้ /refactor-commit ถ้าจำเป็น
- ใช้ /follow-tool-hk ถ้าจำเป็น (เฉพาะ repo ที่ไม่ใช้ moonrepo — moon repos ใช้ `vcs.hooks`)

- ใช้ /git-commit ถ้าจำเป็น

##### Expected Outcome

- รู้ compliance rate และ commits ที่ผิด format/quality
- มี suggested messages พร้อมใช้
- รู้ว่าควร `/refactor-commit` หรือตั้ง commitlint hook

### no-verify

##### Goal

Commit ไฟล์ที่มีการเปลี่ยนแปลงโดยข้าม pre-commit hooks ด้วย `git commit --no-verify`

##### Scope

ใช้เมื่อ pre-commit hooks ล้มเหลว ช้า หรือขัดขวาง commit ที่ตั้งใจ โดยต้องได้รับ confirmation จากผู้ใช้ก่อนเสมอ

##### Execute

###### 1. Check Status

> Goal: ตรวจสอบไฟล์ที่จะ commit

1. รัน `git status --short`
2. รัน `git diff --cached --name-only` เพื่อดูไฟล์ staged
3. ถ้ายังไม่มี staged files → หยุดและแจ้งให้ stage ก่อน

###### 2. Verify Reason

> Goal: ยืนยันว่าต้องใช้ `--no-verify` จริง

1. ถาม user ว่าทำไมต้อง bypass hooks
2. ถ้า bypass เพราะ pre-commit ล้มเหลว → บันทึกสาเหตุไว้สำหรับแก้ไขภายหลัง
3. ถ้า user ไม่ยืนยัน → ใช้ `/git-commit` แทน

###### 3. Review Staged Diff

> Goal: ตรวจสอบความถูกต้องก่อน commit

1. รัน `git diff --cached --stat`
2. ถ้ามีไฟล์ไม่เกี่ยวข้อง → แยกออกก่อน
3. ตรวจสอบ message ร่าง

###### 4. Execute Commit

> Goal: commit โดยข้าม hooks

1. ถ้ามี message จาก user รัน `git commit --no-verify -m "<message>"`
2. ถ้าไม่มี message → รัน `git commit --no-verify` แล้วแก้ไขใน editor
3. ตรวจสอบ exit code

###### 5. Post-Commit

> Goal: ตรวจสอบและวางแผนแก้ hooks

1. รัน `git log --oneline -3`
2. รัน `git status --short`
3. ถ้า bypass เพราะ hook ล้มเหลว → สร้าง TODO ให้แก้ `/run-check` หรือ `/run-verify` ภายหลัง

##### Rules

###### 1. No Automatic Add

- ไม่ใช้ `git add .` ใน skill นี้
- commit เฉพาะไฟล์ที่ถูก stage แล้ว

###### 2. User Confirmation

- ถาม user ก่อนใช้ `--no-verify`
- อธิบาย risk: hook จะไม่ทำงาน commit อาจพาไฟล์ที่ไม่ผ่าน check เข้า repo

###### 3. Message Format

- ใช้ conventional commits เหมือน `/git-commit`
- subject ไม่เกิน 72 ตัวอักษร
- ใช้ภาษาอังกฤษ

###### 4. Post-Commit Discipline

- ถ้า hook ล้มเหลว ต้องมีแผนแก้ไข
- ใช้ `/run-check` หรือ `/run-verify` ทีหลังเพื่อตรวจสอบ
- ห้ามใช้ `--no-verify` เพื่อซ่อน error ที่ต้องแก้

- ใช้ `/git-commit` เมื่อ hooks ทำงานได้ปกติ
- ใช้ `/git-commit selected-files` เมื่อต้องการ commit เฉพาะไฟล์
- ใช้ `/git-commit-and-push` เมื่อต้องการ push พร้อมกัน
- ใช้ `/run-check` หรือ `/run-verify` ก่อน `--no-verify` ถ้าเป็นไปได้
- ใช้ `/resolve-errors` เมื่อ hook ล้มเหลวและต้องแก้ root cause
- ใช้ `/refactor-commit` ถ้า history ต้องปรับ

##### Expected Outcome

- ไฟล์ staged ถูก commit โดยไม่รัน pre-commit hooks
- ผู้ใช้ยืนยันการ bypass
- มี message ตาม conventional commits
- มี plan สำหรับตรวจสอบหรือแก้ hooks ภายหลัง
- working directory สะอาดสำหรับไฟล์ที่ตั้งใจ commit

### selected-files

##### Goal

Commit only selected files, without using `git add .`

##### Scope

- ใช้เมื่อต้องการ commit เฉพาะบางไฟล์จาก working directory
- ไม่ stage ทุกไฟล์โดยอัตโนมัติ
- รองรับการเลือกด้วย pattern หรือ user confirmation

##### Execute

###### 1. List Changed Files

> Goal: รู้ว่ามีไฟล์อะไรเปลี่ยนแปลงบ้าง

1. รัน `git status --short` เพื่อดู modified, staged, untracked
2. รัน `git diff --name-only` สำหรับ modified
3. จัดกลุ่มไฟล์ตาม category: skills, docs, config, scripts
4. ระบุ pre-existing/unrelated files ทีไม่ควร commit

###### 2. Select Files To Commit

> Goal: เลือกเฉพาะไฟล์ทีต้องการ commit

1. ถ้า user ระบุ argument (pattern/path) → ใช้ pattern กรอง
2. ถ้าไม่ระบุ → แสดง list ให้ user เลือกด้วย `ask_user_question`
3. รองรับ multi-select
4. ข้าม untracked ทีไม่เกี่ยวข้องเว้นแต่ user เลือก

###### 3. Stage Selected Files

> Goal: เตรียมไฟล์ทีเลือกสำหรับ commit

1. รัน `git add <file1> <file2> ...` เฉพาะไฟล์ทีเลือก
2. ไม่ใช้ `git add .` หรือ `git add -A`
3. ตรวจสอบด้วย `git diff --cached --name-only`

###### 4. Determine Commit Type

> Goal: เลือก conventional commit type

1. ดู Rules ส่วน Commit Types
2. เลือกตามการเปลี่ยนแปลง:
   - `feat` สำหรับ skill ใหม่
   - `fix` สำหรับการแก้ไข
   - `docs` สำหรับเอกสาร
   - `refactor` สำหรับ refactor
   - `chore` สำหรับ config/structure
   - `test` สำหรับ test

###### 5. Write Commit Message

> Goal: เขียน commit message

1. ใช้รูปแบบ `<type>(<scope>): <subject>`
2. subject ไม่เกิน 72 ตัวอักษร
3. ระบุ scope จาก directory/ประเภทของไฟล์
4. ถ้ามีหลายไฟล์จากหลาย scope → ใช้ `,` คั่น หรือ commit แยก

###### 6. Execute Commit

> Goal: commit ไฟล์ทีเลือก

1. รัน `git commit -m "<message>"`
2. ตรวจสอบ exit code
3. ถ้ามี error → แก้ไขและลองอีกครั้ง

###### 7. Verify

> Goal: ยืนยันว่า commit ถูกต้อง

1. รัน `git log --oneline -3`
2. รัน `git status --short` เพื่อดูไฟล์ทียังไม่ถูก commit
3. ตรวจสอบว่าไม่มีไฟล์ทีไม่เกี่ยวข้องถูก stage

##### Rules

###### 1. No Add All

- ห้ามใช้ `git add .` หรือ `git add -A`
- ต้อง stage ทีละไฟล์ตามทีเลือก
- ถ้าไม่แน่ใจ → ถาม user

###### 2. User Confirmation

- ถ้าไม่มี argument ให้ถามก่อน stage
- แสดงรายการไฟล์ก่อน commit
- ให้ user ยืนยัน message

###### 3. Scope Clarity

- หนึ่ง commit ควรอยู่ใน scope เดียวกัน
- ถ้ามีหลาย scope แยก commit
- ระบุ scope ใน message

###### 4. Conventional Commits

- ใช้ type ให้ถูกต้อง
- subject ใช้ imperative mood
- ไม่ต้องขึ้นต้นด้วยตัวพิมพ์ใหญ่ ไม่จบด้วยจุด

- ใช้ /git-commit ถ้าจำเป็น
- ใช้ /git-commit-and-push ถ้าจำเป็น
- ใช้ /git-push ถ้าจำเป็น
- ใช้ /refactor-commit ถ้าจำเป็น
- ใช้ /deep-validate ถ้าจำเป็น

##### Expected Outcome

- เฉพาะไฟล์ทีเลือกถูก commit
- ไฟล์ทีไม่เกี่ยวข้องยังคงอยู่ใน working directory
- Commit message ชัดเจนตาม conventional commits
- รายงานไฟล์ที commit และไฟล์ทีเหลืออยู่

## Expected Outcome

- Commit messages ที่สอดคล้องกับ conventional commits และเป็นภาษาอังกฤษทั้งหมด
- Git history ที่อ่านง่ายและติดตามง่าย
- ทุกไฟล์ที่มีการเปลี่ยนแปลงใน global devin skills ถูก commit
- Working directory สะอาด

