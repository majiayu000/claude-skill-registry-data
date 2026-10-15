---
name: audit-docs
description: >
  Audit documentation gaps by comparing code changes between the last docs update (or release version)
  and current HEAD. Detects undocumented features, modified tools/skills, configuration changes,
  and KO-EN translation parity drift. Use when checking for missing documentation, auditing doc gaps,
  verifying translation parity, or preparing documentation before releases. Triggers on: "audit docs",
  "audit-docs", "문서 누락 검토", "문서 누락 감사", "docs audit", "문서 드리프트 감사", "마지막 docs 업데이트 분석".
license: Complete terms in LICENSE.txt
---

# Audit Docs Skill

Analyze the gap between the codebase changes (features, tools, skills, settings) made since the last documentation update (or release tag) and current `HEAD`. Verify whether user documentation (`website/` and `docs/user/`) accurately reflects these changes and maintains Korean-English translation parity.

---

## 🧭 Workflow Decision Tree

```
1. Run Automated Audit Script
   └─ python3 .agents/skills/audit-docs/scripts/audit_docs.py [--since <REF> | --release]
2. Inspect Code Changes vs Document Mapping
   ├─ Built-in Tools → docs/user/guides/builtin-tools.md
   ├─ Bundled Skills → docs/user/guides/skills.md
   ├─ Settings/Config → docs/user/guides/troubleshooting.md & getting-started/
   └─ Scenarios/Workflows → docs/user/scenarios/
3. Audit KO ↔ EN Translation Parity & Truncation
   └─ Check if EN ratio < 70% or headings mismatch
4. Verify ASD-STE100 Style Compliance
   └─ Check active voice, imperative verbs, sentence length <= 20-25 words
5. Output Structured Audit Report & Action Plan
```

---

## Step 1: Run the Audit Script

Run the helper script to detect baseline commits, code changes, and doc parity:

```bash
# 1. Automatic mode: Compares against the last commit that touched docs/user/
python3 .agents/skills/audit-docs/scripts/audit_docs.py

# 2. Release mode: Compares against the latest Git release tag
python3 .agents/skills/audit-docs/scripts/audit_docs.py --release

# 3. Custom baseline: Compares against a specific branch or commit ref
python3 .agents/skills/audit-docs/scripts/audit_docs.py --since dev/0.9.x~10

# 4. JSON format for machine parsing
python3 .agents/skills/audit-docs/scripts/audit_docs.py --json --output audit_report.json
```

---

## Step 2: Analyze Code Diffs & Map to Docs

Inspect code diffs between baseline and HEAD across five key architectural domains:

| Code Domain | Source Paths | Target User Documentation |
| --- | --- | --- |
| **Bundled Skills** | `src-tauri/bundled_skills/` | [`docs/user/guides/skills.md`](file:///home/fritzprix/my_works/libr-agent/docs/user/guides/skills.md) |
| **Built-in Tools** | `src-tauri/src/mcp/`, `src-tauri/src/agent/tools/` | [`docs/user/guides/builtin-tools.md`](file:///home/fritzprix/my_works/libr-agent/docs/user/guides/builtin-tools.md) |
| **Settings & Config** | `src/components/settings/`, `src-tauri/src/config/` | [`docs/user/guides/troubleshooting.md`](file:///home/fritzprix/my_works/libr-agent/docs/user/guides/troubleshooting.md), [`getting-started/connecting-models.md`](file:///home/fritzprix/my_works/libr-agent/docs/user/getting-started/connecting-models.md) |
| **UI Views / Routes** | `src/views/`, `src/routes/` | [`docs/user/guides/navigation-guide.md`](file:///home/fritzprix/my_works/libr-agent/docs/user/guides/navigation-guide.md), [`docs/user/index.md`](file:///home/fritzprix/my_works/libr-agent/docs/user/index.md) |
| **Automation / Cron** | `src-tauri/src/scheduled/` | [`docs/user/guides/scheduled-tasks.md`](file:///home/fritzprix/my_works/libr-agent/docs/user/guides/scheduled-tasks.md), [`docs/user/guides/automation.md`](file:///home/fritzprix/my_works/libr-agent/docs/user/guides/automation.md) |

### Verification Checklist:
- [ ] Were new skills added to `bundled_skills` without being listed in the Skills Catalog?
- [ ] Were new MCP tools or tool parameters added without reference entries?
- [ ] Were UI setting keys renamed or added without updating troubleshooting and setup guides?
- [ ] Were new execution modes (e.g., `YOLO`, `Unsafe`, `Normal`) added without documentation?

---

## Step 3: Audit KO ↔ EN Translation Parity

A common pitfall is updating Korean documentation while leaving English documents as outdated skeletons.

Check the `KO ↔ EN Documentation Parity Audit` table from the script:

1. **`MISSING_EN`**: Korean document exists, but English counterpart does not exist. (Critical)
2. **`SEVERE_TRUNCATION` (Ratio < 40%)**: English document is severely abbreviated or a placeholder stub. (High)
3. **`MODERATE_TRUNCATION` (Ratio 40% ~ 70%)**: English document misses key tables, tips, or sections. (Medium)
4. **`OK` (Ratio >= 70%)**: Content volume and structural depth match.

---

## Step 4: Verify ASD-STE100 Style Guidelines

When writing or reviewing English documentation, enforce ASD-STE100 principles:

1. **Sentence Length**:
   - Procedural instructions: **<= 20 words**.
   - Descriptive statements: **<= 25 words**.
2. **Imperative Verbs**:
   - Begin instruction steps with active verbs (`Specify`, `Configure`, `Inspect`, `Run`).
3. **Clarity and Precision**:
   - Avoid ambiguous modals (`should`, `might`). Use `must` for requirements, `can` for capabilities.
   - Restrict consecutive noun clusters to 3 words or fewer.

---

## Step 5: Generate the Final Audit Report

Structure the final audit report using this markdown format:

```markdown
# 📋 Documentation Gap Audit Report

## 1. Audit Scope & Baseline
- Baseline: `<COMMIT_HASH>` (<SUMMARY>)
- Target Head: `<HEAD_HASH>`
- Audit Mode: `<AUTOMATIC | RELEASE | CUSTOM>`

## 2. Code Changes vs. Document Mapping Gaps
| Change Type | Component / File | Detected Code Change | Affected Documentation | Status |
| --- | --- | --- | --- | --- |
| New Skill | `skill-name` | Added to bundled_skills | `guides/skills.md` | 🔴 Missing |
| Tool Flag | `browser` | Added `--sandbox` arg | `guides/builtin-tools.md` | ⚠️ Outdated |

## 3. Translation Parity Findings (KO ↔ EN)
- Total Files Audited: XX
- Truncated / Outdated EN Files: X
- Parity Gaps List:
  - `path/to/doc.md`: Ratio XX%, missing sections: [...]

## 4. Actionable Remediation Plan
1. [P0] Update `guides/skills.md` (KO & EN) to include `new-skill`.
2. [P1] Re-translate `path/to/doc.md` to ASD-STE100 standards.
3. [P2] Run `pnpm --filter libragent-docs build` to verify clean build.
```
