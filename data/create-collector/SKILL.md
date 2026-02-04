---
name: create-collector
description: Create a new collector bot package with automatic implementation and validation. Use when user wants to create a new collector from scratch.
---

# create-collector

Create a new collector bot package with automatic implementation and validation.

## Usage

`/create-collector <vendor> <suite?> <product>`

**Arguments:**
- `vendor` (required) - Vendor name (e.g., `amazon`, `microsoft`, `google`)
- `suite` (optional) - Suite name if vendor has suites (e.g., `aws`, `365`)
- `product` (required) - Product name (e.g., `iam`, `s3`, `entra`)

**Examples:**
```
/create-collector amazon aws s3
/create-collector microsoft entra
/create-collector google workspace sheets
/create-collector adp workforcenowng
```

## Description

End-to-end collector creation with automatic validation:
1. Verify module and schema dependencies exist
2. Create directory structure and configuration files
3. Generate code (npm install + generate)
4. **Spawn 2 creation agents in parallel** (Implementation + Mapping)
5. Create documentation (README, USERGUIDE)
6. Build and lint
7. **Automatically validate with /review-collector**
8. Fix critical issues or report to user
9. Ready for commit

## Execution Instructions for Claude

### Phase 1: Parse Arguments & Verify

**Step 1.1: Parse vendor/suite/product**
```javascript
const args = args.trim().split(/\s+/);
// Examples:
// "amazon aws s3" → vendor=amazon, suite=aws, product=s3
// "microsoft entra" → vendor=microsoft, suite=null, product=entra
// "adp workforcenowng" → vendor=adp, suite=null, product=workforcenowng
```

**Step 1.2: Verify dependencies exist**
```bash
# Check module exists (prefer zerobias-org, fallback auditlogic)
npm view @zerobias-org/module-<vendor>-<suite?>-<product>
npm view @auditlogic/module-<vendor>-<suite?>-<product>

# Or check bundles
npm view @zerobias-org/module-bundle --json | jq '.dependencies'
npm view @auditlogic/module-bundle --json | jq '.dependencies'

# Check schema exists (always auditlogic)
npm view @auditlogic/schema-<vendor>-<suite?>-<product>

# Or check bundle
npm view @auditlogic/schema-bundle --json | jq '.dependencies'

# Check product exists (always zerobias-org)
npm view @zerobias-org/product-<vendor>-<suite?>-<product>

# Or check bundle
npm view @zerobias-org/product-bundle --json | jq '.dependencies'
```

**If missing**: STOP and inform user that module/schema/product must be created first.

---

### Phase 2: Create Structure

**Step 2.1: Create directory**
```bash
mkdir -p package/<vendor>/<suite?>/<product>
cd package/<vendor>/<suite?>/<product>
```

**Step 2.2: Create symlinks**
```bash
# Based on depth (3 or 4 levels)
ln -s ../../../../.npmrc .npmrc    # or ../../../
ln -s ../../../../.nvmrc .nvmrc    # or ../../../
```

**Step 2.3: Copy templates**
```bash
# Copy from reference collector (adp/workforcenowng for simple)
cp ../../../adp/workforcenowng/.eslintrc .
cp ../../../adp/workforcenowng/.mocharc.json .
cp ../../../adp/workforcenowng/tsconfig.json .
```

**Step 2.4: Create .gitignore**
```
node_modules/
dist/
generated/
```

---

### Phase 3: Create Configuration Files

**Step 3.1: Create package.json** (use template from DEVELOPMENT_WORKFLOW.md)
- Version: 0.0.0
- Author: ctamas@zerobias.com
- Dependencies: module + schema (base + ts) + core deps
- Get latest versions from npm

**Step 3.2: Get UUIDs and create hub.yml**
```bash
npm install  # Temporary to get module installed
cat node_modules/@auditlogic/module-*/package.json | grep module-id
cat node_modules/@auditlogic/product-*/index.yml | grep "^id:"
```

Create hub.yml with UUIDs (operations section omitted).

**Step 3.3: Ask user about parameters**
"What parameters should this collector accept (if any)?"
- If none: use minimal template
- If provided: create with user's parameters

**Step 3.4: Explore schema and create collector.yml**
```bash
cat node_modules/@auditlogic/schema-*/dist/index.d.ts
cat node_modules/@auditlogic/module-*/module-*.yml
```

Match operations to classes and include ALL classes with module data.

**Step 3.5: Generate code**
```bash
npm install
npm run generate
```

Verify generated/BaseClient.ts and get module connector name.

---

### Phase 4: Spawn Creation Agents (PARALLEL)

**CRITICAL:** Spawn BOTH agents in a SINGLE message with 2 Task calls.

**Agent 1: Implementation Agent**
- Read `.claude/agents/create-implementation.md`
- Pass: collector path, module connector name, schema classes, vendor type
- Creates: src/index.ts, src/Collector*Impl.ts

**Agent 2: Mapping Agent**
- Read `.claude/agents/create-mappings.md`
- Pass: collector path, module types, schema types, schema classes
- Creates: src/Mappers.ts

Wait for both to complete.

---

### Phase 5: Create Documentation

**Step 5.1: Create README.md**
- What data is collected
- Schema classes
- Required permissions
- Development commands

**Step 5.2: Create USERGUIDE.md** (if has parameters)
- Only document parameters
- Customer-facing tone
- How to find values
- Example JSON

**Step 5.3: Create test/integration/Collector*IT.ts**
- Copy pattern from similar collector
- Adjust class name and parameters

---

### Phase 6: Build & Lint

```bash
npm run build
npm run lint
```

If errors: attempt to fix common issues, otherwise report to user.

---

### Phase 7: Validate with /review-collector

**CRITICAL:** Automatically run the validation system.

```bash
/review-collector .
```

This spawns all 8 validation agents.

**If compliance < 90%:**
- Report issues to user
- Ask if they want auto-fix for simple issues
- **Critical issues** (data loss, data deletion): Must be fixed before commit

**If compliance >= 90%:**
- Report minor issues as warnings
- Proceed to finalization

---

### Phase 8: Finalize

**Step 8.1: Run npm shrinkwrap**
```bash
npm shrinkwrap
```

**Step 8.2: Report to user**

Display summary:
```
✅ Collector created: @zerobias-org/collectorbot-<vendor>-<suite?>-<product>

📦 Package: package/<vendor>/<suite?>/<product>

📊 Validation Results:
   ✅ Configuration: PASS
   ✅ Schema: PASS
   ✅ Mapping: PASS
   ✅ Pagination: PASS
   ✅ GroupId: PASS
   ✅ Security: PASS
   ✅ Performance: PASS
   ✅ Dependencies: PASS

   📈 Compliance: 100%

🎉 Collector is ready for commit!

📝 Next steps:
   1. Review the implementation in src/
   2. Test with: npm run test:integration
   3. Commit with: git commit -m "feat(s3): initial S3 collector"
```

**If issues found:**
```
⚠️  Collector created with issues (Compliance: 75%)

Issues found:
   ❌ Mapping: 2 errors
   ⚠️  Performance: 1 warning

Run /review-collector to see details.

Would you like me to fix these issues automatically?
```

---

## Notes

- Implementation and Mapping agents can share documentation with validation agents
- Validation is AUTOMATIC - no manual step needed
- Creates production-ready collector in one command
- User only needs to review and commit
