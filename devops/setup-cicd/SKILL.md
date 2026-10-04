---
name: setup-cicd
description: ตรวจจับ platform และตั้งค่า CI/CD config files, secrets และ workflows
argument-hint: "[scope]"
related:
  - update-project
  - follow-tool-github-actions
  - follow-secret-manager
  - follow-tasks
  - deep-review
  - run-verify
  - run-test-all
  - follow-tool-mr-boxington
  - ship-to-dev-branch
  - report
  - suggest-next-action
  - run-deploy
  - research-setup-integrations
---

## Goal

ตรวจจับ CI/CD platform ที project ใช้ แล้วตั้งค่า workflow files, secrets, และ package scripts ให้พร้อมรัน verify, test, build, deploy, release บน CI

## Scope

ใช้ครั้งเดียวตอน setup หรือเมื่อ CI/CD config ไม่พร้อม ไม่รวมรัน pipeline, commit, push, deploy หรือ release (setup release workflow ได้ แต่ไม่รัน release)

ถ้าต้องการรัน cloud verify หรือ ship บน cloud ให้ใช้ `/run-verify` หรือ `/ship-to-dev-branch` แทน

## Execute

### 1. Detect Platform

> Goal: รู้ว่า project ใช้ CI/CD platform อะไร

1. ตรวจหาไฟล์ config ทีมีอยู่:
   - GitHub Actions: `.github/workflows/*.{yml,yaml}`
   - GitLab CI: `.gitlab-ci.yml`
   - Azure DevOps: `azure-pipelines.yml`
   - CircleCI: `.circleci/config.yml`
   - Jenkins: `Jenkinsfile`
   - Cloudflare Pages: `wrangler.toml`, `wrangler.jsonc`
   - Vercel: `vercel.json`
2. ถ้าพบหลาย platform → เลือกตามลำดับ: GitHub Actions → GitLab CI → Azure DevOps → CircleCI → Jenkins → Cloudflare → Vercel
3. ถ้าไม่พบ → ทำ `/ask-me` ถาม user หรือ default เป็น GitHub Actions

### 2. Verify Package Scripts

> Goal: มั่นใจว่า package manifest มี scripts ที CI จะเรียก ตามขนาด project

1. อ่าน `package.json` หรือ `Cargo.toml` หรือไฟล์ manifest ที่เหมาะสม
2. ถ้า package manifest ขาด fields พื้นฐานสำหรับ publish (`name`, `version`, `description`, `license`, `repository`) → ทำ `/update-project` `### setup-package` ก่อน
3. ตรวจสอบขนาด project:
   - ถ้า project เล็ก (ไม่ monorepo, build/test ไม่หนัก) → `verify` ต้องรวม `scan`, `lint`, `typecheck`, `test`, `build` ใน package manifest เลย
   - ถ้า project ใหญ่ (monorepo หรือ build/test หนัก) → CI/CD pipeline จะรัน full suite แทน; package manifest ต้องมี `test:all`, `build` และ `verify` อย่างน้อย `check && test`
4. ถ้าไม่มี scripts `verify`, `test:all`, `build` → ทำ `/follow-tasks` เพื่อตั้งค่า
5. ตรวจว่า `verify` ครบตามขนาด project
6. ถ้า project ไม่มี package manifest (เช่น skill collection, docs repo) → หา tool directories ที่มี package.json แล้วรัน verify จากแต่ละ subdir ใน CI

### 3. Setup Secrets

> Goal: ตั้งค่า secrets ที CI/CD ต้องใช้

1. ทำ `/follow-secret-manager` เพื่อจัดการ secrets อย่างปลอดภัย
2. ถ้าใช้ GitHub Actions → เปิดหน้า GitHub Secrets ด้วย `/open-github`
3. ตรวจสอบว่ามี secrets ทีจำเป็น เช่น `NPM_TOKEN`, `CARGO_REGISTRY_TOKEN`, `CLOUDFLARE_API_TOKEN`, `VERCEL_TOKEN`
4. ไม่ hardcode secrets ลงในไฟล์ config

### 4. Create Workflow Files

> Goal: สร้าง CI/CD config files ตาม platform

#### GitHub Actions

1. ทำ `/follow-tool-github-actions` เพื่อตั้งค่า workflows ครบถ้วน
2. ถ้าอยากสร้างเอง → สร้าง `.github/workflows/ci.yml` ด้วยเนื้อหาพื้นฐาน:

```yaml
name: ci
on:
  push:
    branches: [main, master]
  pull_request:

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  verify:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v7

      - uses: oven-sh/setup-bun@v2
        with:
          bun-version: latest

      - uses: actions/cache@v6
        with:
          path: ~/.bun/install/cache
          key: ${{ runner.os }}-bun-${{ hashFiles('bun.lockb') }}
          restore-keys: |
            ${{ runner.os }}-bun-

      - run: bun install
      - run: bun run verify
      - run: bun run test:all
      - run: bun run build
```

3. ถ้า project ไม่มี root package.json (เช่น skill collection, docs repo) → รัน verify จาก tool directories ที่มี package.json ของตัวเอง โดยไม่ต้อง `bun install` ที root

4. ถ้าต้องการ deploy ให้สร้าง `.github/workflows/deploy.yml` โดย trigger บน `push` ไป `main`/`master` และเรียก `bun run deploy` หรือ deploy tool ตาม platform

5. ถ้าต้องการ release:
   - ถ้ายังไม่มี release tool → เลือกผ่าน `/follow-tool-changesets`, `/follow-tool-changelogen`, `/follow-tool-semantic-release` หรือ `/follow-tool-release-it` ก่อน
   - สร้าง `.github/workflows/release.yml` โดย trigger บน `push` tag `v*` เท่านั้น:

```yaml
name: release
on:
  push:
    tags: ['v*']
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: oven-sh/setup-bun@v2
        with:
          bun-version: latest
      - run: bun install
      - run: bun run verify
      - run: bun run build
      - name: release
        run: |
          # ใส่คำสั่ง release ตาม platform ที detect ไว้
          # npm: npm publish
          # crates: cargo publish
          # vscode: npx vsce publish
          # webstore: npx chrome-webstore-upload
          # docker: docker build . -t <image>:<tag> && docker push <image>:<tag>
        env:
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
          VSCE_PAT: ${{ secrets.VSCE_PAT }}
          CARGO_REGISTRY_TOKEN: ${{ secrets.CARGO_REGISTRY_TOKEN }}
          CLIENT_ID: ${{ secrets.CLIENT_ID }}
          CLIENT_SECRET: ${{ secrets.CLIENT_SECRET }}
          REFRESH_TOKEN: ${{ secrets.REFRESH_TOKEN }}
          DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}
          DOCKER_PASSWORD: ${{ secrets.DOCKER_PASSWORD }}
```

#### GitLab CI

สร้าง `.gitlab-ci.yml` ด้วย stages: `verify`, `test`, `build`, `deploy`, `release`

#### Azure DevOps

สร้าง `azure-pipelines.yml` ด้วย jobs: `verify`, `test`, `build`, `deploy`

#### CircleCI

สร้าง `.circleci/config.yml` ด้วย workflows: `verify`, `test`, `build`, `deploy`

#### Cloudflare Pages

ตรวจ `wrangler.toml` แล้วเพิ่ม GitHub Actions workflow สำหรับ deploy ถ้าขาด

#### Vercel

ตรวจ `vercel.json` แล้วเพิ่ม GitHub Actions workflow หรือใช้ Vercel Git Integration

### 5. Validate Config

> Goal: ตรวจสอบว่า CI/CD config ถูกต้อง

1. ทำ `/deep-review` เพื่อตรวจ drift และ duplication
2. ทำ `/deep-review` เพื่อตรวจว่า config ครอบคลุม security, testing, deployment
3. รัน dry run ถ้า platform รองรับ (เช่น `act` สำหรับ GitHub Actions) — optional
4. ถ้าต้องการ validate test suite ใน local → ทำ `/run-test-all` ก่อนขึ้น CI
5. ถ้ามี syntax error → แก้ไขก่อนจบ

### 6. Report

> Goal: สรุปสถานะ setup

1. ใช้ `/report` สรุป: platform, workflow files, missing scripts, missing secrets, next action
2. ทำ `/suggest-next-action`

### 7. Optional Release Setup

> Goal: ตั้งค่า release workflow ถ้าจำเป็น

1. ถ้า project ต้องการ release บน tag → ทำตาม Step 5 release workflow + เลือก release tool ผ่าน `/follow-tool-*`
2. ถ้าไม่ต้องการ release → ข้าม

## Rules

### 1. Setup Only

- `setup-cicd` ทำเฉพาะตั้งค่า config ไม่รัน pipeline
- ไม่ commit, ไม่ push, ไม่ deploy, ไม่ release
- ถ้าต้องการรัน pipeline ให้ใช้ `/run-verify` หรือ `/ship-to-dev-branch`

### 2. Platform First

- ตรวจหา platform ทีมีอยู่ก่อนสร้างไฟล์ใหม่
- ถ้ามี config แล้ว → ตรวจสอบและเติมส่วนทีขาด ไม่ทับซ้ำ
- ถ้าไม่พบ → default เป็น GitHub Actions หรือถาม user

### 3. Secrets Safety

- ใช้ `/follow-secret-manager` หรือ GitHub Secrets / GitLab CI Variables
- ไม่ hardcode secrets ลง workflow files
- ไม่ log secrets

### 4. Package Scripts

- ต้องมี package scripts ก่อนสร้าง CI workflow
- project เล็ก: `verify` ต้องรวม `scan`, `lint`, `typecheck`, `test`, `build` ใน package manifest เลย
- project ใหญ่: CI/CD pipeline รัน full suite; package manifest มี `test:all`, `build` และ `verify` อย่างน้อย `check && test`
- `test:all` ควรรวม unit, integration, e2e, coverage ตาม project
- ไม่ใส่ `release` ลง package manifest — release ทำผ่าน CI/CD workflow บน tag หรือ `/run-release`

### 5. No Auto Commit

- ไม่ commit หรือ push config files โดยอัตโนมัติ
- ถ้า user ต้องการ commit → ทำ `/git-commit` หรือ `/ship-to-dev-branch` หลัง setup

### 6. Overlap And Cost

- `run-verify`, `check-quality`, `review-*`, `check-*` ทำงานซ้ำซ้อนกันได้ ควรรวมลงใน `verify` job เดียว
- ใช้ `concurrency`, `timeout-minutes`, `cache`, runner เดียว และหลีกเลี่ง matrix เพื่อประหยัด cost
- ถ้าไม่มี root package.json ให้รัน verify จาก tool directories แทนการสร้าง root package หลอก
- ใช้ /research-setup-integrations ถ้าจำเป็น (เลือก CI actions/plugins จาก official sources ก่อนเขียน workflow)
- ใช้ /run-deploy ถ้าจำเป็น

## Expected Outcome

- CI/CD platform ถูก detect หรือถาม user
- Workflow files สร้างถูกต้องตาม platform
- Package scripts ครบถ้วนสำหรับ verify, test, build, deploy — `release` ไม่อยู่ใน package manifest
- Secrets ถูก setup อย่างปลอดภัย
- ไม่มีการ commit/push/deploy/release โดยอัตโนมัติ
- มีรายงาน setup status และ next action ชัดเจน
