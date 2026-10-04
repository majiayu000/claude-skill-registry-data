---
name: siloos-code-review
description: "Guidelines and procedures for reviewing SiloOS frontend, hardware bridge, and protocol changes."
---

# SiloOS Code Review Skill

## When to Use
- Before merging any changes
- After completing a task (self-review)
- When auditing code quality
- Before deployment to Pi

## Procedure

### Step 1: Scope the Review
Identify which files changed and which domain they belong to:
- `dashboard/src/` → Frontend review
- `ble_bridge.py` → Hardware bridge review
- `dashboard/src/sfwu/` → SFWU protocol review

### Step 2: Verify Build & Types
```bash
cd dashboard && npm run build && npm run lint
npx tsc --noEmit
```

### Step 3: Security & Compliance
- [ ] No hardcoded secrets in `config.json` or code
- [ ] WebSocket messages validated
- [ ] Imports use correct paths (`parsers/` not `responses/`)
- [ ] Logger used instead of `console.log`

### Step 4: Protocol Correctness
- [ ] CRC32 calculation verified
- [ ] Byte offsets correct in parsers
- [ ] Command codes match `constants.ts`
