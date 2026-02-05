---
name: release-guide-info
version: 1.2.0
description: |
  Generate Ops Update Guide from Git Diff. Produces internal Operations-facing
  update/migration guides based on git diff analysis. Supports STRICT_NO_TOUCH (default)
  and TEMP_CLONE_FOR_FRESH_REFS modes. Includes tag auto-detection and commit log analysis.

trigger: |
  - Preparing to release a new version
  - Need to document what changed between refs
  - Creating operational update guide
  - Communicating version updates to Ops team
  - "Generate ops guide from main to HEAD"
  - "Generate release guide for <version>"

skip_when: |
  - No git repository available
  - Single file change (too small for formal guide)
  - Customer-facing release notes only (use simpler template)

input_schema:
  BASE_REF:
    type: string
    required: true
    description: Starting point (branch, tag, or SHA)
    examples: ["main", "release/v3.4.x", "v1.0.0"]
  TARGET_REF:
    type: string
    required: true
    description: Ending point (branch, tag, or SHA)
    examples: ["HEAD", "feature/foo", "v1.1.0"]
  VERSION:
    type: string
    required: false
    description: Version number for the release (auto-detected from tags if not provided)
    examples: ["v2.0.0", "1.5.0", "2025.01"]
  LANGUAGE:
    type: enum
    required: false
    default: "en"
    values: ["en", "pt-br", "both"]
    description: Output language(s) for the guide
  MODE:
    type: enum
    required: false
    default: "STRICT_NO_TOUCH"
    values: ["STRICT_NO_TOUCH", "TEMP_CLONE_FOR_FRESH_REFS"]
    description: Git execution mode

output_schema:
  files:
    type: array
    description: List of generated guide files
    items:
      path: string
      language: string
  summary:
    type: object
    description: Quick summary of changes
    properties:
      features: number
      bug_fixes: number
      improvements: number
      breaking_changes: number
  version:
    type: string
    description: Version number (provided or auto-detected)
  refs:
    type: object
    properties:
      base: string
      target: string
      base_sha: string
      target_sha: string

related:
  complementary: [finishing-a-development-branch, handoff-tracking]
---

# Release Guide Info — Ops Update Guide Generator

## Overview

You are a code-aware documentation agent. Produce an **internal** Operations-facing update/migration guide.

## Runtime Inputs (REQUIRED)

| Input | Description | Example |
|-------|-------------|---------|
| `BASE_REF` | Starting point (branch, tag, or SHA) | `main`, `release/v3.4.x`, `v1.0.0` |
| `TARGET_REF` | Ending point (branch, tag, or SHA) | `feature/foo`, `HEAD`, `v1.1.0` |
| `VERSION` (optional) | Version number (auto-detected from tags if not provided) | `v2.0.0`, `1.5.0` |
| `LANGUAGE` (optional) | Output language | `en` (default), `pt-br`, `both` |
| `MODE` (optional) | Execution mode | `STRICT_NO_TOUCH` (default), `TEMP_CLONE_FOR_FRESH_REFS` |

**Language options:**
- `en` — English only (default)
- `pt-br` — Portuguese (Brazil) only
- `both` — Generate two files, one in each language

**Version handling:**
- If `VERSION` provided → Use it directly
- If `TARGET_REF` is a tag → Auto-extract version from tag name
- If neither → Omit version from output

**Comparison range:** Always use triple-dot `BASE_REF...TARGET_REF`

## Safety Invariants

### STRICT_NO_TOUCH (default)

**Hard requirement:** Do NOT alter anything in the current local repo.

**FORBIDDEN commands:**
- `git fetch`, `git pull`, `git push`
- `git checkout`, `git switch`, `git reset`, `git clean`
- `git commit`, `git merge`, `git rebase`, `git cherry-pick`
- `git worktree`, `git gc`, `git repack`, `git prune`
- Any write operation to `.git/` files

**ALLOWED commands (read-only):**
- `git rev-parse`, `git diff`, `git show`, `git log`, `git remote get-url`

**If ref does not exist locally:** STOP and report:
- Which ref failed to resolve
- That STRICT_NO_TOUCH forbids fetching
- Suggest alternative: TEMP_CLONE_FOR_FRESH_REFS

### TEMP_CLONE_FOR_FRESH_REFS (optional)

Goal: Do NOT touch current repo, but allow obtaining up-to-date remote refs in an isolated temporary clone.

**Process:**
```bash
# 1. Get remote URL
REMOTE_URL=$(git remote get-url origin)

# 2. Create isolated temp clone
TMP_DIR=$(mktemp -d) || { echo "Failed to create temp directory"; exit 1; }
git clone --no-checkout "$REMOTE_URL" "$TMP_DIR"

# 3. Fetch refs in temp clone
cd "$TMP_DIR"
git fetch origin --prune --tags

# 4. Continue steps inside temp clone only

# 5. Cleanup after guide is generated
cd - >/dev/null
rm -rf "$TMP_DIR"
```

## The Process

### Step 0 — Determine Execution Location

**If MODE=STRICT_NO_TOUCH:** Operate in current repo with read-only commands only.

**If MODE=TEMP_CLONE_FOR_FRESH_REFS:** Create temp clone, operate there, cleanup after.

### Step 1 — Resolve Refs and Metadata

```bash
# Verify refs exist
git rev-parse --verify BASE_REF^{commit}
git rev-parse --verify TARGET_REF^{commit}

# Capture SHAs
BASE_SHA=$(git rev-parse --short BASE_REF)
TARGET_SHA=$(git rev-parse --short TARGET_REF)

# Get repo/service name
origin_url="$(git remote get-url origin 2>/dev/null)"
[ -n "$origin_url" ] && printf '%s\n' "$origin_url" | sed 's|.*[:/]||;s|\.git$||' || basename "$(pwd)"
```

**If verification fails:**
- STRICT_NO_TOUCH: STOP + suggest TEMP_CLONE_FOR_FRESH_REFS
- TEMP_CLONE: STOP (refs truly not found)

### Step 1.5 — Tag Auto-Detection and Version Resolution

**Detect if refs are tags and extract version:**

```bash
# Check if TARGET_REF is a tag
if git tag -l "$TARGET_REF" | grep -q .; then
    IS_TAG=true
    # Extract version from tag (handles v1.0.0, 1.0.0, release-1.0.0, etc.)
    AUTO_VERSION=$(echo "$TARGET_REF" | sed -E 's/^(v|release[-_]?|version[-_]?)?//i')
else
    IS_TAG=false
    AUTO_VERSION=""
fi

# Check if BASE_REF is a tag
if git tag -l "$BASE_REF" | grep -q .; then
    BASE_IS_TAG=true
else
    BASE_IS_TAG=false
fi

# Resolve final VERSION
if [ -n "$VERSION" ]; then
    FINAL_VERSION="$VERSION"
elif [ -n "$AUTO_VERSION" ]; then
    FINAL_VERSION="$AUTO_VERSION"
else
    FINAL_VERSION=""
fi
```

**Version detection output:**

| Scenario | Result |
|----------|--------|
| `VERSION` provided | Use provided version |
| `TARGET_REF` is tag `v2.0.0` | Auto-detect: `2.0.0` |
| `TARGET_REF` is tag `release-1.5.0` | Auto-detect: `1.5.0` |
| `TARGET_REF` is branch/SHA | No version (omit from title) |

### Step 1.6 — Commit Log Analysis

**Extract context from commit messages:**

```bash
# Get commit messages between refs
git log --oneline --no-merges BASE_REF...TARGET_REF

# Get detailed commit messages for context
git log --pretty=format:"%h %s%n%b" --no-merges BASE_REF...TARGET_REF
```

**Parse commit messages for:**

| Pattern | Category | Example |
|---------|----------|---------|
| `feat:`, `feature:` | Feature | `feat: add user authentication` |
| `fix:`, `bugfix:` | Bug Fix | `fix: resolve null pointer exception` |
| `refactor:` | Improvement | `refactor: optimize database queries` |
| `breaking:`, `BREAKING CHANGE:` | Breaking | `breaking: remove deprecated API` |
| `perf:` | Performance | `perf: improve response time` |
| `docs:` | Documentation | `docs: update API documentation` |
| `chore:`, `build:`, `ci:` | Infrastructure | `chore: update dependencies` |

**Use commit messages to:**
1. Supplement diff analysis with intent/context
2. Identify breaking changes explicitly marked
3. Group related changes by commit scope
4. Extract ticket/issue references (e.g., `#123`, `JIRA-456`)

### Step 2 — Produce the Diff

```bash
# Stats view
git diff --find-renames --find-copies --stat BASE_REF...TARGET_REF

# Full diff
git diff --find-renames --find-copies BASE_REF...TARGET_REF
```

### Step 3 — Build Change Inventory

From the diff, identify:

| Category | What to Look For |
|----------|------------------|
| **Endpoints** | New/changed/removed (method/path/request/response/status codes) |
| **DB Schema** | Migrations, backfills, indexes, constraints |
| **Messaging** | Topics, payloads, headers, idempotency, ordering |
| **Config/Env** | New vars, changed defaults |
| **Auth** | Permissions, roles, tokens |
| **Performance** | Rate-limits, timeouts, retries |
| **Dependencies** | Bumps with runtime behavior impact |
| **Observability** | Logging, metrics, tracing changes |
| **Operations** | Scripts, cron, job schedules |

### Step 4 — Write the Ops Update Guide

**Use the appropriate template based on LANGUAGE parameter.**

---

## Language Templates

### Template Selection

| LANGUAGE | Use Template |
|----------|--------------|
| `en` | English Template |
| `pt-br` | Portuguese Template |
| `both` | Generate BOTH templates as separate files |

---

### 🇺🇸 English Template (LANGUAGE=en)

**Title Format (with version):**
```markdown
# Ops Update Guide — <repo/service> — <VERSION> — <TARGET_SHA>
```

**Title Format (without version):**
```markdown
# Ops Update Guide — <repo/service> — BASE_REF → TARGET_REF — <TARGET_SHA>
```

**Header Block:**
```markdown
| Field | Value |
|-------|-------|
| **Mode** | `STRICT_NO_TOUCH` or `TEMP_CLONE_FOR_FRESH_REFS` |
| **Comparison** | `BASE_REF...TARGET_REF` |
| **Base SHA** | `<BASE_SHA>` |
| **Target SHA** | `<TARGET_SHA>` |
| **Date** | YYYY-MM-DD |
| **Source** | based on git diff |
```

**Section Format:**
```markdown
## <N>. <Descriptive Title> [<Category> <Emoji>]
```

**Category Mapping (English):**

| Category | Emoji |
|----------|-------|
| Feature | ✨ |
| Bug Fix | 🐛 |
| Improvement | 🆙 |
| Breaking | ⚠️ |
| Infrastructure | 🔧 |
| Observability | 📊 |
| Data | 💾 |

**Section Labels (English):**
- **What Changed** — Bullet list with concrete changes
- **Why It Changed** — Infer from code/comments/tests
- **Client Impact** — Risk level: Low/Medium/High
- **Required Client Action** — "None" or exact steps
- **Deploy/Upgrade Notes** — Order of operations, compatibility
- **Post-Deploy Monitoring** — Logs, metrics, signals
- **Rollback** — Safety: Safe/Conditional/Not recommended

**Uncertain Info Markers (English):**
- Mark as **ASSUMPTION** + **HOW TO VALIDATE**

---

### 🇧🇷 Portuguese Template (LANGUAGE=pt-br)

**Title Format (with version):**
```markdown
# Guia de Atualização (Ops) — <repo/serviço> — <VERSION> — <TARGET_SHA>
```

**Title Format (without version):**
```markdown
# Guia de Atualização (Ops) — <repo/serviço> — BASE_REF → TARGET_REF — <TARGET_SHA>
```

**Header Block:**
```markdown
| Campo | Valor |
|-------|-------|
| **Mode** | `STRICT_NO_TOUCH` ou `TEMP_CLONE_FOR_FRESH_REFS` |
| **Comparação** | `BASE_REF...TARGET_REF` |
| **Base SHA** | `<BASE_SHA>` |
| **Target SHA** | `<TARGET_SHA>` |
| **Data** | YYYY-MM-DD |
| **Fonte** | baseado em git diff |
```

**Section Format:**
```markdown
## <N>. <Título descritivo> [<Categoria> <Emoji>]
```

**Category Mapping (Portuguese):**

| Categoria | Emoji |
|-----------|-------|
| Funcionalidade | ✨ |
| Correção | 🐛 |
| Melhoria | 🆙 |
| Breaking | ⚠️ |
| Infra | 🔧 |
| Observabilidade | 📊 |
| Dados | 💾 |

**Section Labels (Portuguese):**
- **O que mudou** — Bullet list with concrete changes
- **Por que mudou** — Infer from code/comments/tests
- **Impacto para clientes** — Risk level: Baixo/Médio/Alto
- **Ação necessária do cliente** — "Nenhuma" or exact steps
- **Notas de deploy/upgrade** — Order of operations, compatibility
- **O que monitorar pós-deploy** — Logs, metrics, signals
- **Rollback** — Safety: Seguro/Condicional/Não recomendado

**Uncertain Info Markers (Portuguese):**
- Mark as **ASSUNÇÃO** + **COMO VALIDAR**

---

## Section Structure (applies to both languages)

**1) Contextual Narrative (REQUIRED - comes FIRST)**
- 1-3 paragraphs explaining business/operational context
- Problem being solved or scenario that triggered change
- Concrete examples (anonymized if needed)

**2) What Changed / O que mudou**
- Bullet list with concrete changes
- Include `file:line` references (e.g., `pkg/mmodel/balance.go:332-335`)
- Show key code snippets if they clarify behavior

**3) Why It Changed / Por que mudou**
- Infer from code/comments/tests if possible
- If not derivable, use the appropriate uncertainty marker for the language

**4) Client Impact / Impacto para clientes**
- Who/what is impacted
- Risk level with justification
- Expected behavior differences

**5) Required Client Action / Ação necessária do cliente**
- "None"/"Nenhuma" if none
- If yes: exact steps (API fields, headers, retries, config updates)

**6) Deploy/Upgrade Notes / Notas de deploy/upgrade**
- Order of operations, compatibility concerns
- Rolling deploy safety
- Flags/canary recommendations

**7) Post-Deploy Monitoring / O que monitorar pós-deploy**

For log messages:
```markdown
| Level/Nível | Message/Mensagem | Meaning/Significado |
|-------------|------------------|---------------------|
| `INFO` | `Message text` | Explanation |
| `WARN` | `Warning text` | What this indicates |
```

For tracing spans:
```markdown
#### Tracing Span: `span.name.here`

| Scenario/Cenário | Span Status | Description |
|------------------|-------------|-------------|
| Success/Sucesso | ✅ OK | Description |
| Error/Erro | ❌ Error | Description with error details |
```

Include:
- **Where/Onde**: Log sources, dashboards, metric names
- **Suggested threshold/Threshold sugerido**: If not derivable, label as "Suggestion"/"Sugestão"
- **Success signals/Sinais de sucesso**: Expected positive indicators
- **Failure signals/Sinais de falha**: Warning signs

**8) Rollback**
- **Safety/Segurança**: Safe/Conditional/Not recommended (or Portuguese equivalent)
- **Steps/Passos**: Specific steps (revert image, wait for TTL, etc.)
- **Concerns/Preocupações**: Data/compat concerns

#### Special Sections

**⚠️ Attention Point / Ponto de Atenção (when applicable)**

English:
```markdown
### ⚠️ Attention Point

**The client may observe [specific change] after this deploy.**

This is expected because:
- [Reason 1]
- [Reason 2]

**Upside**: [Benefit]
**Required action**: [What to do]
```

Portuguese:
```markdown
### ⚠️ Ponto de Atenção

**O cliente pode observar [mudança específica] após este deploy.**

Isso é esperado porque:
- [Razão 1]
- [Razão 2]

**Lado positivo**: [Benefício]
**Ação necessária**: [O que fazer]
```

**Compatibility Tables (when applicable)**

English:
```markdown
### Backward Compatibility

✅ **100% compatible** with existing data:

| Scenario | Handling | Location |
|----------|----------|----------|
| Scenario 1 | How handled | `file:line` |
```

Portuguese:
```markdown
### Compatibilidade retroativa

✅ **100% compatível** com dados existentes:

| Cenário | Tratamento | Local |
|---------|------------|-------|
| Cenário 1 | Como tratado | `arquivo:linha` |
```

### Step 5 — Write Summary Section

**English Summary:**
```markdown
## Summary

| Category | Count |
|----------|-------|
| Features ✨ | N |
| Bug Fixes 🐛 | N |
| Improvements 🆙 | N |
| Data/Migrations 💾 | N |

## Rollback Compatibility Analysis

✅/⚠️ **[Overall assessment]**

| Item | Rollback | Justification |
|------|----------|---------------|
| 1. [Item name] | ✅ Safe | [Brief reason] |
| 2. [Item name] | ⚠️ Conditional | [Brief reason] |
```

**Portuguese Summary:**
```markdown
## Resumo

| Categoria | Quantidade |
|-----------|------------|
| Funcionalidades ✨ | N |
| Correções 🐛 | N |
| Melhorias 🆙 | N |
| Dados/Migrações 💾 | N |

## Análise de Compatibilidade de Rollback

✅/⚠️ **[Avaliação geral]**

| Item | Rollback | Justificativa |
|------|----------|---------------|
| 1. [Nome do item] | ✅ Seguro | [Razão breve] |
| 2. [Nome do item] | ⚠️ Condicional | [Razão breve] |
```

End with:
- Schema changes
- Incompatible serialization changes
- Data that old version cannot read
- Irreversible migrations

### Step 6 — Preview Before Saving

**MANDATORY: Show preview summary before writing to disk.**

Present to user for confirmation:

```markdown
## 📋 Release Guide Preview

**Configuration:**
| Setting | Value |
|---------|-------|
| Repository | <repo-name> |
| Comparison | `BASE_REF...TARGET_REF` |
| Version | <VERSION or "Not detected"> |
| Language(s) | <en/pt-br/both> |
| Mode | <STRICT_NO_TOUCH/TEMP_CLONE_FOR_FRESH_REFS> |

**Change Summary:**
| Category | Count |
|----------|-------|
| Features ✨ | N |
| Bug Fixes 🐛 | N |
| Improvements 🆙 | N |
| Breaking Changes ⚠️ | N |
| Infrastructure 🔧 | N |
| Data/Migrations 💾 | N |

**Key Changes (top 5):**
1. [Brief description of most significant change]
2. [Second most significant]
3. [Third]
4. [Fourth]
5. [Fifth]

**Output File(s):**
- `notes/releases/{filename}.md`

---
**Proceed with saving?** [Yes/No]
```

**Wait for user confirmation before Step 7.**

### Step 7 — Persist Guide to Disk

**File naming convention:**

| Has Version? | LANGUAGE | Filename Pattern |
|--------------|----------|------------------|
| Yes | `en` | `{DATE}_{REPO}-{VERSION}.md` |
| Yes | `pt-br` | `{DATE}_{REPO}-{VERSION}_pt-br.md` |
| No | `en` | `{DATE}_{REPO}-{BASE}-to-{TARGET}.md` |
| No | `pt-br` | `{DATE}_{REPO}-{BASE}-to-{TARGET}_pt-br.md` |
| Any | `both` | Generate BOTH files above |

```bash
# Output directory
OUT_DIR="notes/releases"
mkdir -p "$OUT_DIR"

# Base filename components
DATE=$(date +%Y-%m-%d)
REPO_SLUG=<repo-kebab-case>
VERSION_SLUG=<version-sanitized>  # e.g., v2.0.0 -> v2-0-0
BASE_SLUG=<base-ref-sanitized>
TARGET_SLUG=<target-ref-sanitized>

# Determine filename based on version availability
if [ -n "$FINAL_VERSION" ]; then
    BASE_FILENAME="${DATE}_${REPO_SLUG}-${VERSION_SLUG}"
else
    BASE_FILENAME="${DATE}_${REPO_SLUG}-${BASE_SLUG}-to-${TARGET_SLUG}"
fi

# Generate files based on LANGUAGE
case "$LANGUAGE" in
  en)
    FILE="$OUT_DIR/${BASE_FILENAME}.md"
    # Write English guide
    ;;
  pt-br)
    FILE="$OUT_DIR/${BASE_FILENAME}_pt-br.md"
    # Write Portuguese guide
    ;;
  both)
    FILE_EN="$OUT_DIR/${BASE_FILENAME}.md"
    FILE_PT="$OUT_DIR/${BASE_FILENAME}_pt-br.md"
    # Write BOTH guides
    ;;
esac
```

**After saving, confirm:**
- Path(s) of saved file(s)
- `BASE_REF...TARGET_REF` used
- SHAs used
- Version (if detected/provided)
- Language(s) generated

## Hard Rules (Content)

| Rule | Enforcement |
|------|-------------|
| No invented changes | Everything MUST be supported by diff |
| Uncertain info | Mark as **ASSUMPTION** + **HOW TO VALIDATE** |
| Operational language | Audience is Ops, not customers |
| External changes | API, events, DB, auth, timeouts MUST be called out |
| Preview required | MUST show preview before saving |
| User confirmation | MUST wait for user approval before writing files |

## Anti-Rationalization Table

| Rationalization | Why It's WRONG | Required Action |
|-----------------|----------------|-----------------|
| "The diff is too large, I'll summarize" | Summarizing loses critical details. Ops needs specifics. | **Document ALL significant changes** |
| "This change is obvious, no need to explain" | Obvious to you ≠ obvious to Ops. Context is required. | **Add contextual narrative** |
| "I'll skip the preview, user is in a hurry" | Preview prevents errors. Skipping risks wrong output. | **ALWAYS show preview first** |
| "No breaking changes detected" | Did you check commit messages for BREAKING CHANGE? | **Verify commit messages AND diff** |
| "Version not important for this guide" | Version helps Ops track releases. Auto-detect or ask. | **Include version when available** |
| "Rollback analysis not needed, changes are safe" | ALL changes need rollback assessment. No exceptions. | **Include rollback section** |
| "I'll invent a likely reason for this change" | Invented reasons mislead Ops. Mark as ASSUMPTION. | **Mark uncertain info clearly** |
| "This file change isn't relevant to Ops" | You don't decide relevance. Document it, Ops decides. | **Document ALL changes** |
| "Skip commit log, diff is enough" | Commit messages contain intent not visible in diff. | **Analyze commit messages** |
| "User didn't ask for Portuguese, skip it" | Check LANGUAGE parameter. If `both`, generate both. | **Respect LANGUAGE parameter** |

## Quality Checklist

Before output, self-validate:

- [ ] Every section starts with contextual narrative
- [ ] All log messages in table format (Level | Message | Meaning)
- [ ] All tracing spans in table format when applicable
- [ ] Emojis used consistently for category tags
- [ ] Rollback analysis consolidated as matrix at end
- [ ] No invented changes - everything traceable to diff
- [ ] File:line references included for key code changes
- [ ] "⚠️ Attention Point" used for confusing expected behaviors

## Special Handling Rules

| Change Type | Required Info |
|-------------|---------------|
| **DB migrations** | Forward steps, rollback steps, irreversibility, compat matrix |
| **Breaking API/events** | Explicit contract diffs + mitigation/versioning |
| **Feature flags** | Name, default, operational toggling guidance |
| **Security/auth** | Privilege/role changes, operational checks |
| **Log level changes** | Document what was ERROR→INFO, etc. |

## Example Invocations

**With version (from tag):**
```
User: Generate release guide from <base-tag> to <target-tag>
Assistant: [Detects tags, auto-extracts version from <target-tag>]
Assistant: [Shows preview summary]
User: Yes, proceed
Assistant: [Writes guide]
Output: notes/releases/{DATE}_{REPO}-{VERSION}.md
```

**With explicit version:**
```
User: Generate release guide from <base-ref> to <target-ref>, version <version>
Assistant: [Uses provided version]
Assistant: [Shows preview summary]
User: Yes, proceed
Output: notes/releases/{DATE}_{REPO}-{VERSION}.md
```

**Without version (branch to branch):**
```
User: Generate ops guide from <base-branch> to <target-branch>
Assistant: [No version detected]
Assistant: [Shows preview summary]
User: Yes, proceed
Output: notes/releases/{DATE}_{REPO}-{BASE}-to-{TARGET}.md
```

**Portuguese only:**
```
User: Generate ops guide from <base-ref> to <target-ref> in Portuguese
Assistant: [Shows preview summary]
User: Yes, proceed
Output: notes/releases/{DATE}_{REPO}-{BASE}-to-{TARGET}_pt-br.md
```

**Both languages:**
```
User: Generate release guide for <version> in both English and Portuguese
Assistant: [Shows preview summary]
User: Yes, proceed
Output:
  - notes/releases/{DATE}_{REPO}-{VERSION}.md (English)
  - notes/releases/{DATE}_{REPO}-{VERSION}_pt-br.md (Portuguese)
```

**Via slash command:**
```
User: /release-guide <base-ref> <target-ref>
Assistant: [Executes skill with BASE_REF and TARGET_REF]
```
