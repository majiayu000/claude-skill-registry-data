---
name: use-linter
description: ใช้ linter CLI (Rust) สำหรับ deterministic code checks — rules+AST+metrics → score/report/baseline
argument-hint: "[path] [--diff|--baseline|--format json]"
---

## Goal

ใช้ `linter` CLI (Rust, `D:\newkub\wpackages\rust-packages\packages\tools\linter`) สำหรับ deterministic checks ทุกภาษา — regex rules + ast-grep syntax-tree rules + metrics — ผลิต `review-report.json` schema เดียวกับ `deep-review`

## Scope

ใช้เมื่อต้อง scan code หา issues แบบ deterministic (rules/metrics/secrets/frameworks), diff-only review, baseline delta, CI gate, หรือเติม findings เข้า `deep-review` Step 3 — `ไม่ใช่` แทน manual/AI review สำหรับ architecture/business-logic judgment

## Execute

### 1. Verify CLI

> Goal: ยืนยัน linter binary พร้อมใช้งาน

1. `linter doctor` — ตรวจ git, rules dirs, rule counts ก่อนเสมอ
2. ถ้า binary ไม่มี → `cd D:\newkub\wpackages\rust-packages && cargo build -p wrikka-linter`

### 2. Scan Modes

> Goal: เลือก scan mode ให้ตรง use case

| No. | Use case | Command |
|-----|----------|---------|
| 1 | Full scan (default) | `linter` หรือ `linter scan <path>` |
| 2 | Diff-only review | `linter scan --diff HEAD` (หรือ `--changed main`) |
| 3 | Re-review หลัง fix | `linter scan --baseline` → status new/existing/fixed/regressed |
| 4 | สร้าง baseline วันแรก | `linter scan --save-baseline` |
| 5 | CI gate | `linter scan --fail-on high --format sarif --out results.sarif` |
| 6 | Machine report | `linter scan --format json` → `reports/review-report.json` |
| 7 | Domain/severity filter | `linter scan --domain security --severity medium` |
| 8 | Summary only | `linter scan -q` |

### 3. Extend Rules

> Goal: เพิ่ม rules เมื่อ built-in packs ไม่พอ

- Regex rules: YAML sequence ใน `rules/<pack>/*.yml` (id/language/message/severity/regex/fix)
- AST rules: standard `sg` format ใน `rules/ast/<lang>/*.yml` (id/language/rule/severity/message) — reuse ast-grep rules เดิมได้เลย
- ภาษา AST ที่รองรับ: ts/tsx/js/rs/py/go/java/c/cpp/json/yaml/html/css/lua/php/rb/swift/kt/cs/scala/sh/md
- เพิ่ม pack ผ่าน `--rules <dir>` (repeatable), `linter.toml` `rules = [...]`, หรือ `~/.config/linter/rules`
- `linter explain <rule-id>` — ดู pack/analyzer/message/fix ของ rule
- `linter init` — scaffold `linter.toml` + `rules/ast/` starter

### 4. Integration

> Goal: ใช้ linter output เป็น SSOT ของ findings

- `deep-review` Step 3: `linter scan --format json` = single source of truth (drop-in แทน `review-codebase:json`)
- `update-review-cli-then-run`: maintain = เพิ่ม rule YAML หรือ analyzer module ใน `packages/tools/linter` — ห้าม fork TS CLI เก่า
- `multi-agents-review`: เพิ่ม AI findings เข้า report schema เดียวกัน (`confidence` ใน evidence)
- เก็บ `score`, `grade`, `domains`, `analyzerErrors`, `baseline` delta เสมอ

## Rules

- รัน `--diff`/`--baseline` เมื่อ re-review — อย่า rescan ทั้ง repo โดยไม่จำเป็น
- ทุก finding ต้องมี `fixSkill` routing — ห้ามรายงานโดยไม่มีทางแก้
- ถ้า AST rule เขียนยาก → fallback regex rule ได้ แต่ให้ AST ก่อนถ้า pattern เป็น structural
- อย่าแก้ business logic จาก linter run — linter แค่ report

## Expected Outcome

`reports/review-report.json` ครบ schema + score/grade + per-domain + baseline delta + analyzer errors โปร่งใส
