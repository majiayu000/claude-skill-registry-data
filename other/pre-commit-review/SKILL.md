---
name: pre-commit-review
description: Fast security-focused review of staged changes before every commit, checking only critical compliance rules
type: skill
user-invocable: false
---

# Pre-Commit Security Review

## MTK File Resolution

Resolve MTK skill/reference/script paths per `.claude/references/mtk-file-resolution.md` unless the router already stated `MTK_ROOT=<path>` this session; `CLAUDE.md`, `.claude/tech-stack`, `.claude/rules/`, `tasks/`, `docs/`, `.mtk/` stay project-relative.

---

Run a fast, security-focused review on staged changes only. This is the lightweight
check engineers should run before every commit.

## Process

1. Get the staged diff: `git diff --cached`
2. If nothing staged, check unstaged: `git diff`
3. If nothing at all, tell the engineer there's nothing to review
4. **Run the static linter pass first:** `bash hooks/pre-commit-linters.sh`
   - Emits deterministic findings with `source: "linter"` and `confidence: 100`
   - Findings include secrets, raw SQL interpolation, connection strings with
     plaintext passwords, AWS keys, JWTs, and stack-specific patterns
   - Merge linter findings into your final JSON output (they always pass the
     threshold, so they always surface)
4.5. **Merge cached analyzer output (if available).** If `.mtk/analyzer-output.json`
   exists and was modified within the last 10 minutes, read it and **filter
   findings to only those whose `file` field matches a file in
   `git diff --cached --name-only`** (or `git diff --name-only` if using
   unstaged). Discard all other findings — surfacing repo-wide warnings on an
   unrelated commit erodes trust in the gate. Merge the filtered set into your
   output with `source: "analyzer"` and `confidence: 100`. **Do not run the
   build yourself** — the pre-commit gate must stay fast (seconds, not minutes).
   Only consume cached output.
4.6. **Roslyn MCP tools (if available, .NET only).** If `dotnet-claude-kit` is
   installed and the `DetectAntiPatterns` tool is available, call it on the
   changed files for on-demand semantic analysis. Treat results as
   `source: "analyzer"`, `confidence: 100`. This is fast (analyzes specific
   files, not full build) and catches EF Core, async, and disposal patterns
   that the regex linter misses. If the tool is not available, skip this step.
4.7. **Collateral-churn check.** Run `bash hooks/collateral-guard.sh --cached`
   (add `--manifest docs/specs/<date>-<slug>.json` when this commit belongs to a
   spec). It answers a question no other check asks: is this churn *yours*? It
   flags whitespace/EOL-only rewrites (a small edit to a CRLF file rewrites the
   whole file), generated artifacts riding along undeclared (one `npm install`
   drags a lockfile into a feature commit), and asset directories regenerated
   wholesale. Findings are warnings, not blocks — but each carries a working
   revert command, and a commit whose diff is mostly collateral hides the real
   change from every reviewer downstream. The dependency gate below is the
   separate, stricter question of what the lockfile churn *contains*.

4.8. **Dependency-introduction gate (if a manifest changed).** Detect whether
   the staged diff touches any of these manifest files:
   `package.json`, `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`,
   `*.csproj`, `Directory.Packages.props`, `requirements.txt`, `pyproject.toml`,
   `Pipfile`, `poetry.lock`, `go.mod`, `Cargo.toml`, `Cargo.lock`,
   `Gemfile`, `Gemfile.lock`, `composer.json`. If any matches, list the
   **newly added** dependencies (lines beginning with `+` introducing a new
   package name) and walk each through the six-criteria rubric in
   `.claude/references/dependency-intake-checklist.md` — existence & legitimacy
   first, then scope, maintenance, size, security, license. A `Poor` on
   criterion 0 blocks outright; two `Poor` ratings on criteria 1–5 for a single
   dep block the commit; one `Poor` requires explicit override in the PR description.
   Emit each problematic dep as a `category: "dependency"` finding with
   `source: "ai"` and confidence ≥ 85 for `Poor` ratings backed by evidence
   (CVE id, last-release date, license SPDX). Pure version bumps within the
   same major skip the rubric (vulnerability scan only). Skip the gate
   entirely when the checklist file is absent (older repos).
4.9. **Monorepo ripple check.** Run
   `bash scripts/monorepo-ripple.sh $(git diff --cached --name-only)`.
   On a non-monorepo it exits 0 with no output (no false positives). On a
   monorepo, each `RIPPLE <pkg>: affects <downstream>` line becomes a
   `category: "ripple"`, `severity: "warning"`, `source: "linter"`,
   `confidence: 90` finding. Ripples never block the commit on their own —
   they exist to make the author aware that staged changes will affect
   downstream packages.
5. Run the AI review pass on the same diff to catch issues the linter can't
   reach (design, intent, context-sensitive rules). AI findings use
   `source: "ai"` and their own confidence scores per the rubric.
6. Combine linter + AI findings into a single schema-conformant output.

## Check only these (from `.claude/rules/security.md` §1.x and the generated `pre-commit-review-list.md` (tech-stack items); if neither exists, use the fallback list below):

- **Secrets**: Any hardcoded credentials, connection strings with passwords, API keys, tokens?
- **SQL Injection**: Any string-concatenated SQL? Must be parameterized only (EF Core LINQ is fine; `FromSqlRaw` with concatenation is still injection — [.NET example]).
- **PII in Logs**: Any PII (names, emails, account numbers) in log statements or exception messages?
- **Auth Missing**: Any new endpoints, internal ones included, without `[Authorize]` or `RequireAuthorization()`? [.NET example]
- **Audit Missing**: Any state-changing operations on financial data without audit log writes? [finance-domain example]
- **Secrets in Env**: Any connection strings or passwords hardcoded in `appsettings.json` or CDK environment vars? [.NET/AWS example]
- **IAM Blast Radius**: Any new IAM grants with `*` resource that should be scoped? [AWS example]
- **Dependency Intake**: New third-party dep added — does it pass the six-criteria gate in `.claude/references/dependency-intake-checklist.md`? (A `Poor` on criterion 0, or two on criteria 1–5, blocks.)

## Output Contract

Emit the schema-conformant output per `.claude/references/review-finding-schema.md`:

1. **Markdown table** of surfaced findings (rows where `confidence >= threshold`).
2. **Fenced JSON block** with the full structured result. If you need extra
   context fields, stay within the canonical review envelope defined in
   `.claude/references/review-finding-schema.md`.

Read `.claude/review-config.json` for the threshold (default 80; `.claude/review-config.local.json` overrides if present). Apply the **confidence rubric** and the **anti-inflation rule**.

- Any `critical` finding at/above threshold, unless validly `pre_existing` (schema Field rules) → `verdict: "NEEDS_CHANGES"`.
- Otherwise → `verdict: "PASS"`.
- If `findings[]` is empty, `below_threshold_rationale` is mandatory — state what you checked and why you conclude the diff is clean.

Keep the table tight. This is a pre-commit gate, not a full review.

### Clean pass — compact output

When verdict is `PASS` **and** `findings[]` is empty, skip the table and JSON block entirely. Instead emit a single compact summary:

```
✅ Pre-commit review passed — 0 findings across 8 rules ({N} files, {A}+/{D}−)

Checked: secrets · SQL injection · PII in logs · auth · audit trail · env secrets · IAM scope · dependency intake
```

Replace `{N}`, `{A}`, `{D}` with actual file count, additions, and deletions from the diff.
This is the **only** output for a clean pass. No table, no JSON block, no rationale dump.

### Findings present — full output

When there are findings (PASS with warnings/suggestions, or NEEDS_CHANGES), emit the standard schema output: markdown table + fenced JSON block per `.claude/references/review-finding-schema.md`.
