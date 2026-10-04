---
name: run-release
description: Auto-detect platforms, release ไปยัง external platforms, gen CHANGELOG
argument-hint: "[scope]"
related:
  - deep-review
  - follow-secret-manager
  - ship-to-dev-branch
  - setup-cicd
  - update-project
  - run-verify
  - resolve-errors
  - gen-changelog-md
  - publish-package-to-registry
  - use-my-packages-on-registry
  - update-devin-global-skills

---

## Goal

Auto-detect platforms ที่ project รองรับจาก configuration files, release ไปยัง external platforms อัตโนมัติ และ gen `CHANGELOG.md` จาก git tags ด้วย `gen-changelog-md`

## Scope

Release ไปยัง npm, crates.io, VSCode Marketplace, Chrome Web Store, และ Docker Hub พร้อม gen `CHANGELOG.md` จาก git tags

## Execute

> Pre-Run: ทำ `/deep-review` ก่อนเสมอ — `run-*` ต้อง review/ประเมินก่อนลงมือหลัก ห้ามข้าม; ถ้า findings เป็น blocker ให้แก้หรือ report ก่อนรัน (release)

### 1. Check Conditions And Detect Platforms

> Goal: ยืนยันวา release ถูกต้องและปลอดภัยก่อน run และ detect platforms ที่ project รองรับ

1. ตรวจ `git branch --show-current` และ `git describe --tags --exact-match` หรือ `git tag --points-at HEAD`
   - ถ้า HEAD ไม่อยู่บน tag `v*` และไม่อยู่บน `main` หรือ `master` → stop และ report
2. ถ้าอยู่บน `main`/`master` แต่ยังไม่มี tag → หยุดและแนะนำให้สร้าง tag หรือใช้ `/ship-to-dev-branch` ก่อน
3. ตรวจ `git status --porcelain` ต้อง clean
4. ตรวจ CI ผ่านสำหรับ SHA ปัจจุบัน:
   - GitHub Actions: `gh run list --branch main --json databaseId,headSha,status --limit 5` แล้ว `/resolve-cicd <run-id>`
   - ถ้า CI ยังไม่ผ่าน → stop และ report
5. ตรวจ secrets ทีจำเป็นพร้อมใช้งาน (`NPM_TOKEN`, `VSCE_PAT`, `CARGO_REGISTRY_TOKEN`, `CLIENT_ID`, `CLIENT_SECRET`, `REFRESH_TOKEN`, `DOCKER_USERNAME`, `DOCKER_PASSWORD`)
6. ถ้าทุก condition ผ่าน → detect platforms:
   - ตรวจสอบ `package.json` มี `private: false` → รองรับ `npm`
   - ตรวจสอบ `package.json` มี `publisher` field → รองรับ `vscode`
   - ตรวจสอบ `Cargo.toml` มีอยู่ → รองรับ `crates`
   - ตรวจสอบ `manifest.json` มีอยู่ → รองรับ `webstore`
   - ตรวจสอบ `Dockerfile` มีอยู่ → รองรับ `docker`

### 2. Check Configuration

> Goal: Check Configuration

ตรวจสอบ configuration ครบถ้วนก่อน release ตาม platforms ที่ detect ได้

- `npm`: ตรวจสอบ `package.json` มี name, version, description, license, repository, homepage, files
- `vscode`: ตรวจสอบ `package.json` มี publisher, engines.vscode, activationEvents, main, contributes
- `crates`: ตรวจสอบ `Cargo.toml` มี name, version, description, license, repository, categories, keywords, edition, rust-version
- `webstore`: ตรวจสอบ `manifest.json` มี name, version, manifest_version, permissions, icons, action
- `docker`: ตรวจสอบ `Dockerfile` มี FROM, WORKDIR, COPY, RUN และ `.dockerignore` มีการ exclude files
- ถ้า package manifest หรือ release config ไม่ครบ → ทำ `/update-project` `### setup-package` หรือตั้งค่า release tool/workflow ผ่าน `/setup-cicd` + `/follow-tool-*` ก่อน แล้วกลับมาทำ `/run-release` ใหม

### 3. Setup Authentication

> Goal: Setup Authentication

ตั้งค่า authentication สำหรับ platforms ที่ detect ได้

- `npm`: ใช้ `/follow-secret-manager` จัดการ `NPM_TOKEN` แล้ว sync ไป GitHub Secrets หรือใช้ `gh secret set NPM_TOKEN` แบบ manual
- `vscode`: ตั้งค่า `VSCE_PAT` ใน GitHub Secrets ด้วย `gh secret set VSCE_PAT`
- `crates`: ตั้งค่า `CARGO_REGISTRY_TOKEN` ใน GitHub Secrets ด้วย `gh secret set CARGO_REGISTRY_TOKEN`
- `webstore`: ตั้งค่า `CLIENT_ID`, `CLIENT_SECRET`, `REFRESH_TOKEN` ใน GitHub Secrets
- `docker`: ตั้งค่า `DOCKER_USERNAME`, `DOCKER_PASSWORD` ใน GitHub Secrets

### 4. Run Verify

> Goal: Run Verify

ตรวจสอบคุณภาพโค้ดก่อน release

1. ทำ `/run-verify` เพื่อตรวจสอบคุณภาพโค้ด
2. ทำ `/deep-validate` ก่อน tag/release
3. ถ้า verify ไม่ผ่าน ให้แก้ไขก่อนดำเนินการต่อ

### 5. Setup Release Tool

> Goal: Setup Release Tool

ตั้งค่า release tool ตาม platforms ที่ detect ได้

1. `npm`: ทำ `/publish-package-to-registry` เพื่อตั้งค่า release tool
2. `crates`: ทำ `/publish-package-to-registry` เพื่อตั้งค่า release tool
3. `vscode`: ทำ `/follow-create-plugins` (vscode) เพื่อตั้งค่า release tool
4. `webstore`: ทำ `/follow-create-plugins` (browser-wxt) เพื่อตั้งค่า release tool
5. `docker`: ทำ `/follow-release` เพื่อตั้งค่า release tool

### 6. Run Prerelease

> Goal: รัน prerelease ก่อน publish จริง

1. `npm`: รัน `bun run build` หรือ `npm run build`
2. `crates`: รัน `cargo build` หรือ `cargo build --release`
3. `vscode`: รัน `vsce package` เพื่อสร้าง `.vsix`
4. `webstore`: รัน `chrome-webstore-upload validate` เพื่อ validate ก่อน publish
5. `docker`: รัน `docker build --no-cache` เพื่อ build image
6. ถ้า prerelease ไม่ผ่าน → แก้ไขและรันใหม่

### 7. Test Release Artifact

> Goal: smoke test artifact ก่อน publish — ห้าม publish ในขั้นนี้

1. ถ้ามี artifact จาก step prerelease อยู่แล้วและ version ตรง → reuse ได้
2. smoke test ตาม platform:
   - `npm`: `npm pack` + `npm install <tarball>` ใน temp dir แล้ว `node -e "require('<pkg>')"`
   - `crates`: `cargo test --release` + `cargo publish --dry-run`
   - `vscode`: validate `.vsix` ด้วย `vsce ls` หรือ `code --install-extension` ใน temp profile
   - `webstore`: `chrome-webstore-upload validate` หรือ upload แบบ draft
   - `docker`: `docker run --rm <image>:test --help` หรือ health check
3. ตรวจ version ใน artifact ตรง manifest + audit deps (`npm audit`, `cargo audit`)
4. ถ้า test ไม่ผ่าน → stop และแก้ไขก่อน ห้ามข้ามไป publish; ล้าง temp files หลัง test

### 8. Run Release

> Goal: Run Release

รัน release ตาม platforms ที่ detect ได้

1. `npm`: ทำ `/publish-package-to-registry`
2. `crates`: ทำ `/publish-package-to-registry`
3. `vscode`: รัน `vsce publish`
4. `webstore`: รัน `chrome-webstore-upload`
5. `docker`: รัน `docker build` และ `docker push`
6. ถ้า release ไม่สำเร็จ ให้แก้ไขแล้วรันใหม่จนกว่าจะผ่าน

### 9. Write Release Notes

> Goal: เขียน release notes สรุปสวยงาม อ่านง่าย ก่อน publish

1. ใช้ template จาก `templates/release-note.md`
2. สรุป changes ตั้งแต่ tag ล่าสุด: ดึง commits ด้วย `git log <last-tag>..HEAD --oneline`
3. จัดหมวดหมู่: `Breaking Changes`, `Features`, `Bug Fixes`, `Chores`, `Other`
4. เขียนภาษาสุภาพ กระชับ ไม่ใช้ bullet ยาวเกิน 2 บรรทัด
5. แนบลิงก์ `CHANGELOG.md`, เอกสาร release, และ migration guide ถ้ามี breaking changes
6. บันทึกผลลัพธ์เป็น `RELEASE_NOTES.md` หรือใช้เป็น body ของ GitHub Release

### 10. Generate CHANGELOG.md

> Goal: Gen CHANGELOG.md จาก git tags ด้วย `gen-changelog-md` ไม่แก้ไขด้วยมือ

1. ทำ `/gen-changelog-md` เพื่อ gen `CHANGELOG.md` จาก `git tag --sort=-version:refname`
2. หรือรัน script โดยตรง:
```bash
bun run skills/gen-changelog-md/scripts/gen-release-md
```
3. อ่าน `CHANGELOG.md` ที่ gen แล้วเพื่อตรวจสอบ version numbers และ dates ถูกต้อง
4. ถ้าต้องการอัปเดต → รัน script ใหม่อีกครั้ง ห้ามแก้ไข `CHANGELOG.md` ด้วยมือ

## Rules

### 1. Conditions

- ต้องอยู่บน tag `v*` หรือ `main`/`master` เท่านั้น
- ถ้าอยู่บน `main` แต่ไม่มี tag → หยุดและแนะนำ `/ship-to-dev-branch`
- working tree ต้อง clean
- CI ต้องผ่านก่อน release
- secrets สำหรับ platforms ที detect ต้องพร้อม
- ไม่ release โดยอัตโนมัติจากทุก merge

### 2. Auto-Detection

- ตรวจสอบ `package.json` สำหรับ npm และ vscode
- ตรวจสอบ `Cargo.toml` สำหรับ crates
- ตรวจสอบ `manifest.json` สำหรับ webstore
- ตรวจสอบ `Dockerfile` สำหรับ docker
- รันเฉพาะ platforms ที่ detect ได้เท่านั้น

### 3. Configuration Requirements

- ทุก platform ต้องมี name, version, description, license
- `npm`: `private` ต้องเป็น `false`, ต้องมี `repository` และ `homepage`
- `vscode`: ต้องมี `publisher`, `engines.vscode`, `contributes`
- `crates`: ต้องมี `categories`, `keywords`, `edition`, `rust-version`
- `webstore`: ต้องมี `manifest_version`, `permissions`, `icons`
- `docker`: ต้องมี `.dockerignore` และ tag ที่ชัดเจน

### 4. Authentication

- ใช้ API/Automation tokens ไม่ใช่ personal tokens
- ตั้งค่า secrets ใน GitHub Secrets ก่อน release
- ตรวจสอบว่า token มีสิทธิ์ publish ไปที่ package/extension ที่เกี่ยวข้อง
- `npm` alternative: ใช้ npm Trusted Publishers (OIDC) แทน token

### 5. Release Tool Usage

- ใช้ `release-*` workflows สำหรับตั้งค่า release tool แต่ละ platform
- ใช้ `/publish-package-to-registry` สำหรับ npm และ crates
- รัน verify ก่อน release เสมอ
- รัน prerelease script ก่อน release สำหรับ npm
- รัน `vsce package` ก่อน publish สำหรับ vscode
- รัน `chrome-webstore-upload validate` ก่อน publish สำหรับ webstore
- รัน `docker build --no-cache` สำหรับ build ใหม่ทั้งหมด

### 6. CHANGELOG.md Generation

- `CHANGELOG.md` เกิดจากการ gen ด้วย `gen-changelog-md` skill จาก `git tag --sort=-version:refname` เท่านั้น
- ห้ามแก้ไข `CHANGELOG.md` ด้วยมือ — ถ้าต้องการอัปเดต ให้รัน script ใหม่
- ใช้ `scripts/gen-release-md` สำหรับ generation logic
- ใช้ semantic versioning format: `vX.Y.Z` (เช่น `v1.0.0`, `v1.2.3`)
- ใช้ annotated tags สำหรับ releases
- สำหรับ projects ที่ต้องการ conventional commits grouping และ changelog generation ให้ใช้ `/follow-tool-changelogen` แทน

- ใช้ /setup-cicd ถ้าจำเป็น
- ใช้ /use-my-packages-on-registry ถ้าจำเป็น
- ใช้ /deep-review ถ้าจำเป็น
- ใช้ /update-devin-global-skills ถ้าจำเป็น (release)

- ใช้ /resolve-errors ถ้าจำเป็น

## Expected Outcome

- Platforms ถูก detect อัตโนมัติจาก project configuration
- Packages ถูก release สำเร็จไปยัง platforms ที่ detect ได้
- Version ถูก bump อัตโนมัติ
- Changelog ถูกสร้างอัตโนมัติ
- Git tags ถูกสร้างอัตโนมัติ
- `CHANGELOG.md` ถูก gen จาก git tags ด้วย `gen-changelog-md` ไม่แก้ไขด้วยมือ
- Release notes ถูกเขียนสรุปสวยงาม อ่านง่าย จาก template
