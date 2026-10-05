---
name: codexqa-code-reviewer
description: >
  Graph-evidence AI code review (codexqa-code-reviewer) for ANY language repo using
  ONLY the CodexQA CLI symbol graph (call chains, classes, methods, configs,
  blast radius, test edges), then an order-16 Agent LLM judgment pass by the
  host agent's embedded model with deterministic dedupe/merge against heuristic
  findings. Use when the user asks for codexqa-code-reviewer (former name ai-code-reviewer), code review, PR review,
  代码评审, impact analysis, 影响面, regression scope, test gaps, full-repo health
  review, 全仓评审, CodexQA evidence-pack, 证据包, graph-backed review, or LLM
  semantic CR on a pack. Requires codexqa CLI for every language; never embeds
  CodexQA source; never substitutes git-diff-only analysis.
  Not SAST+agent scan reports
  (that is codexqa-defect-analyzer), not structure/impact mapping alone
  (that is codexqa-code-analyzer), and not exception RCA (that is codexqa-rootcause-analyzer).
license: Apache-2.0
compatibility: >
  Requires Node.js >= 18, bash 3.2+, jq, Python 3.10+ (via `scripts/acr-python`),
  and the `codexqa` CLI for every language. Resolve it with the Preflight gate
  (`codexqa_cli_path` after sourcing `scripts/lib/codexqa-preflight.sh`), not with
  `command -v` on the default PATH. Install only when that probe prints nothing.
  Collect / validate / render / merge-llm-findings need no external LLM API; review
  prose and the order-16 semantic pass use the host agent's embedded model. Data lands under
  `<repo>/.codexqa-review/<run-id>/`.
metadata:
  author: open-source
  version: "0.0.3"
  open-standard: agentskills
---

# AI Code Reviewer

Graph-first code review via **CodexQA CLI** only. Collect a JSON evidence pack,
then reason from those artifacts. Applies to every language / polyglot monorepo.

CLI: `{baseDir}/scripts/collect-pr-evidence.sh` (and full-repo / adhoc variants).
Runtime pack: `<repo>/.codexqa-review/<run-id>/` → `review-conclusion.json` +
`REVIEW-REPORT.html`.

**Install:** Prefer `npx skills add openqa-cn/codexqa --skill codexqa-code-reviewer`.
Do not copy into a skills library manually until the user names the install target.

`README.md` / `README.zh-CN.md` / `HOW_IT_WORKS.md` / `KNOWN_LIMITATIONS.md`
(and their `.zh-CN` twins) are human-facing. Do not load them at runtime.

## Boundaries

| Need | Skill |
|---|---|
| Graph-evidence pack → bilingual HTML CR (`REVIEW-REPORT.html`) | **this skill** (`codexqa-code-reviewer`) |
| SAST + Agent LLM Detection → `report_scan.*` | `codexqa-defect-analyzer` |
| Symbol-graph change impact, callers, test gaps | `codexqa-code-analyzer` |
| Exception RCA from stacks/logs on top of CLI analysis | `codexqa-rootcause-analyzer` |

## Prerequisites

| Dependency | Why |
|---|---|
| `codexqa` (Node ≥ 18) | Sole primary analysis backend. Resolve it with the Preflight gate below, not with `command -v` on the default PATH. `npm i -g @openqa-cn/codexqa` only when that probe prints nothing. |
| `jq` | Evidence JSON / HTML render |
| `bash` 3.2+ | Collect / validate / render scripts (macOS OK) |
| Python 3.10+ (`scripts/acr-python`) | Local `derive-*` helpers / validate-skill gate |
| Semgrep, Bandit, gosec, gitleaks, osv-scanner, ruff, eslint | Deterministic SAST. **If any binary is missing, install it before collect** (`scripts/lib/install-sast-tools.sh`) |

Local skill gate (Eval substitute when `skill-up` is missing):

```bash
./scripts/validate-skill.sh
```

## Preflight gate

Run this once in the current shell before any later step. Collect, SAST install, index, validate, review, merge, and render stay blocked until `codexqa_cli_path` has actually executed here and its stdout is known. Intending to preflight later does not open those steps. A second probe is needed only after an install that can change PATH.

A bare `command -v codexqa` or `which codexqa` is not this gate. The CLI is an npm global. Its bin directory comes from `prefix` in `~/.npmrc`, `$npm_config_prefix`, and `npm prefix -g`, and that directory is often missing from the default PATH. A failed lookup means this shell has not been probed, not that the CLI is absent. Installing from that failure reinstalls a CLI that is already there.

```bash
source scripts/lib/codexqa-preflight.sh
codexqa_cli_path
command -v jq >/dev/null
codexqa --version
```

Keep `source` and `codexqa_cli_path` in this shell. `$(codexqa_cli_path)` drops the PATH update. Do not hardcode the prefix.

- Printed path: the CLI is installed. Do not run `npm i -g`. Record the path and the version. If the user asked for the latest release, compare that version with `npm view @openqa-cn/codexqa version` only after this probe, and upgrade only when they differ. Source the preflight again after an upgrade.
- Empty stdout: the CLI is absent. Only then `npm i -g @openqa-cn/codexqa` (Node ≥ 18). Source the preflight again. If `codexqa_cli_path` is still empty, stop with `missing_gate: missing_codexqa_engine`.
- `jq` missing stops the same way. Do not switch the engine to grep or a language-native SAST.

## Quick start

```text
Task progress:
- [ ] 1. Preflight gate in this shell (source + codexqa_cli_path). Steps 1b–6 stay blocked until this has run once.
- [ ] 1a+1b. After the path is printed, run resolve-pr-checkout.sh and install-sast-tools.sh in parallel. Do not git fetch or git clone before resolve returns. SAST install stays mandatory.
- [ ] 2. Collect. Stdout is the primary language, the pack path, and validate-evidence. Traces stay in commands.log. status=ok ends the incremental-index question; do not open the collector or commands.log.
- [ ] 3. From 31-model-brief.json, jq only still_open, open_suspects, test_oracle_open, chain_dimensions, and output. Do not print methods. still_open is one row per shape. chain_dimensions.chains is every CodexQA call chain; judge each chain once against its rules. Do not restate look_for, do_not_report, or closed_lines. Do not open rule-construction or review-conclusion.json.
- [ ] 4. If those three lists are empty, render immediately. Do not read methods, judgment-work, 29, or the repository. If any list is non-empty, judge each shape once and read only its hosts. A different shape is a separate finding. Do not compare it with a closed line to decide they are one defect.
- [ ] 5. Render writes the sealed review-conclusion.json. Summarize from that file. Do not reclassify a sealed card by opening the repository.
```

```bash
# Step 1 — required before every command below. See Preflight gate.
source scripts/lib/codexqa-preflight.sh
codexqa_cli_path

# Steps 1a and 1b run in parallel after codexqa_cli_path has printed a path.
# 1a fetches at most one URL. An empty HTTP reply gets one HTTP/1.1 downgrade, then stop.
./scripts/resolve-pr-checkout.sh --pr <url-or-owner/repo#N> --search-root <workspace>
# status=local means do not fetch. Use the printed repo and diff_base.
./scripts/lib/install-sast-tools.sh

# PR / diff (default). derive-sast.sh runs the installer again before the scan.
./scripts/collect-pr-evidence.sh --repo /path/to/repo --diff-base origin/main

# Full-repo (optional)
./scripts/collect-fullrepo-evidence.sh --repo /path/to/repo

# Adhoc / single-file (no PR diff-base)
./scripts/collect-adhoc-evidence.sh --file /path/to/Foo.java

# After review reasoning:
./scripts/render-review-html.sh --dir <OUT_DIR>
```

Default OUT_DIR: `<repo>/.codexqa-review/<run-id>/` with runtime **`manifest.json`**
(+ `09-language-profile.json`). `templates/evidence-manifest.json` is schema-only —
never written by collectors.

## Hard constraints (CodexQA mandate)

1. **CLI only** — call `codexqa` after the Preflight gate, which builds PATH. Never vendor / unzip / import `@openqa-cn/codexqa`. A default-PATH miss is not a missing CLI.
2. **Evidence files first** — the CodexQA evidence pack is a **hard prerequisite** (前置必要条件).
   Impact, callers, entries, coverage must **cite artifact** fields.
3. **No invented graph** — missing facts → `confidence: UNKNOWN`. Never fake green from `test/` paths.
4. **PR gates** — need code identity (`REPO`) + reviewable change (`--diff-base`). Else `status: blocked`.
5. **Human merge decision** — actionable review only; never auto-approve.
6. **No alternate primary backend** — forbid git-diff-only, grep-only “call graph”, or language SAST
   (SpotBugs/ESLint/mypy/…) as the sole engine. `derive-sast.sh` may run Semgrep,
   Bandit, gosec, gitleaks, osv-scanner, ruff, and eslint as a **secondary**
   deterministic pass (`23-sast-signals.json`). Missing/invalid pack →
   `missing_gate: missing_codexqa_engine` (or specific gate).
7. **Primary language gate** — read `09-language-profile.json` / `manifest.primary_language` /
   `review_language_focus` before findings; apply
   [references/review-dimensions.md](references/review-dimensions.md)
   ([references/language-profile.md](references/language-profile.md)).
   Override with `--primary-lang` only when detection is wrong. Label uncertainty for
   reflection / dynamic dispatch / cross-language FFI — do not leave CodexQA.

## Modes

| Mode | When | Script |
|---|---|---|
| **PR/diff (default)** | Branch/PR vs base | `scripts/collect-pr-evidence.sh` |
| **Full-repo (optional)** | Health / architecture / hotspots | `scripts/collect-fullrepo-evidence.sh` |
| **Adhoc (single-file)** | Upload one/few files without PR | `scripts/collect-adhoc-evidence.sh` |

Full-repo deliverables: hotspot modules (ranked by **edges-in**, not `from_count`), layering drift (入口 → 应用 → 领域 → 存储),
entry concentration, hardening backlog P0/P1/P2. Never invent PR `change_status`.
No product scorecard / 产品评测打分.

Adhoc: bootstraps a mini git repo when `--repo` is omitted so CodexQA index gates pass. An empty root commit is the diff base, then `build-review-digest.py` writes `26`–`31` while the source is still on disk. Validate with `--mode adhoc`. Judgment reads `31-model-brief.json` once. `29` stays for seal.

## Capability → pack map

| Capability | Pack evidence |
|---|---|
| Change localization | `03-change-groups` / `05-changed-symbols` / `diffs/*.diff.json` |
| PR review digest | `26-review-digest.json` (commits behind/ahead, three-dot file classes vs two-dot drift, deduped `disposition: report` lines). The judgment pass reads `31-model-brief.json` instead. |
| Model brief | `31-model-brief.json` (the only file the judgment pass opens: closed shapes, candidate hits, still-open shapes, oracle flags, and method source). Short callees used by a kept method are included. An empty `open_suspects[].source` with `source_ref` points at `methods[].source` for that method, or at `judgment-work/` when `source_ref.where` is `judgment-work`. |
| Judgment packet | `29-judgment-packet.json` stays for seal. A review of at most 2000 pending lines, including one file of about 800 lines, does not create `judgment-work/`. Scripted suspects are closed in `judgment-seed.json` before that pass. Question fan-out starts only when the source left for the model exceeds 2000 lines. That question fan-out writes at most four `judgment-work/group-*.json` files, each holding only methods that own a suspect, a business rule, or a lock-order pair. One-line getters stay out. `magic_number` and `rate_literal` are seeded as conventions in `judgment-seed.json` and are not re-judged. Report rows are closed by seal. Group findings are a union. Past that, whole methods pack into chunks of about 800 lines, at most four concurrent `judgment-work/group-*.json` files. A method is cut only when it is longer than the chunk. Each chunk carries field lines and the lock-order summary. Rule text stays once in `shared.json`. Extra agents on the same change are security, correctness, and quality passes over the full change, not line windows, and the packet does not emit them by default. A suspect with `slice_ref` points at the method slice and does not repeat the source. `identical_to_base` matches the base tip and is not a defect. A csv/markdown/txt keyword hit does not force T0. Confirmed magic numbers seal as conventions, not P1. `30-conclusion-skeleton.json` is sealed into the conclusion at render. |
| Design fit | `10-design-fit-signals.json` (path + package/import layers, `import_cross_layer`, `dead_nested_symbols` confirmed via empty edges-in; full: `imports/` + on-disk fallback) |
| Complexity | `11-complexity-signals.json` (method LOC / decisions / nesting / YAGNI hints) |
| Dependencies | `12-dependency-signals.json` (manifest/lock SNAPSHOT, lock drift, license clues, local audit) |
| Privacy | `13-privacy-signals.json` (PII fields, log exposure, retention gaps, consent/transfer clues) |
| Resilience | `14-resilience-signals.json` (timeout, retry, swallow, partial fail, idempotency/compensation) — signal hits → findings hard gate |
| Change / rollout | `15-rollout-signals.json` (migration, dual-write, flags, compat window, breaking announce, rollback) |
| Observability | `16-observability-signals.json` (catch without log/metric/trace) |
| Contract | `17-contract-signals.json` (breaking hints, XSS/HTML sinks, public-sig volume) |
| Maintainability | `18-maintainability-signals.json` (TODO/FIXME, magic numbers, long files) |
| Performance | `21-performance-signals.json` (hot path, N+1, unbounded allocation) |
| Agent LLM judgment | `22-llm-judgment.json` (host-agent semantic CR + dedupe merge vs heuristic findings) |
| Deterministic SAST | `23-sast-signals.json` (per hit `disposition`: report / drop / suspect; class policy allow / suppress_obvious / dedupe_loci) |
| Annotation callbacks | `19-annotation-edges.json` (Spring/Resilience4j synthetic callers when edges-in empty) |
| Risk tier (blast-radius triage) | `20-risk-tier.json` (T0–T3 from paths + tags + sensitive + rollout surfaces; auth/pay/migration/IaC → T0) |
| Blast radius | `impact/*/edges-in.json` / `reach-in.json` (PR + full-repo top hotspots) |
| Entry / flow | `07-tags.json` + `impact/*/paths/` |
| Test gaps | `tested_count` + `tests-reach.json` (not test directory / test path names) |
| Sensitive paths | `06-sensitive-hits.json` + callers |
| Hot-but-thin | `08-hot-but-thin.json` |
| Full-repo architecture | `stats` / `summary` / `imports/` + Design fit signals |
| Primary language | `09-language-profile.json` + manifest stamps |

## Workflow detail

### 1. Preflight

This step is the Preflight gate. In a shell where `codexqa_cli_path` has not yet been executed, stop. Do not start 1b, collect, index, or review from a `command -v` miss.

```bash
source scripts/lib/codexqa-preflight.sh
codexqa_cli_path
command -v jq >/dev/null
codexqa --version
```

SAST install is step 1b and starts only after that probe has printed a path (or an install from empty stdout has been probed again):

```bash
./scripts/lib/install-sast-tools.sh
```

Per-tool commands (the installer runs these only when that binary is missing):

| Tool | Install command |
|---|---|
| semgrep | `python3 -m pip install --user --break-system-packages 'semgrep>=1.80'` |
| bandit | `python3 -m pip install --user --break-system-packages bandit` |
| ruff | `python3 -m pip install --user --break-system-packages ruff` |
| eslint | `npm install -g eslint` |
| gitleaks | `go install github.com/gitleaks/gitleaks/v8@latest` |
| gosec | `go install github.com/securego/gosec/v2/cmd/gosec@latest` |
| osv-scanner | `go install github.com/google/osv-scanner/cmd/osv-scanner@latest` |

`codexqa-preflight.sh`, `install-sast-tools.sh`, and `derive-sast.sh` all source `scripts/lib/sast-tool-path.sh` and call `sast_refresh_path`. That is the only PATH policy. It prepends a directory when the directory contains the CodexQA CLI, a SAST binary, or the runtime that installs it. Do not hardcode install prefixes. `codexqa_cli_path` prints the resolved CLI. npm bins (`codexqa`, eslint) come from the `prefix` in `~/.npmrc`, `$npm_config_prefix`, and `npm prefix -g` (`<prefix>/bin` on Unix; the prefix directory itself on Windows, where the file is `eslint.cmd`). pip bins (semgrep, bandit, ruff) come from each Python's `sysconfig` scripts path (`bin` on Unix, `Scripts` on Windows). Go bins (gitleaks, gosec, osv-scanner) come from `$GOBIN`, `$GOPATH`, and `go env` (Windows lists split on `;`); if `go` is not on PATH it is found with `brew --prefix`, `asdf where`, or a depth-capped search for `go` or `go.exe`, then `go env` supplies the bin dir. Lookup also accepts `.exe`, `.cmd`, and `.bat`. Node shims come from `$NVM_DIR`, `$VOLTA_HOME`, `$FNM_DIR`, and `$ASDF_DATA_DIR`. A gitleaks / gosec / osv-scanner file that fails `--version` is moved aside so a truncated download is not treated as installed. The GitHub release download runs only when no `go` binary runs, or `go install` still leaves that tool missing.
Do not set `CODEXQA_SAST_SKIP_INSTALL=1` on a real review.

PR: `REPO` + `DIFF_BASE`. Full-repo: `REPO` only. Prefer absolute repo paths.

### 2. Collect

Blocked until the Preflight gate has run once in this shell. Collectors append command traces to `commands.log` and print the primary language, the pack path, and `validate-evidence` status. Shared helpers: `scripts/lib/codexqa-preflight.sh`.
Options: `--full`, `--github-pr owner/repo#N`, `--primary-lang <Lang>`, `--skip-index`, `--skip-validate`, `--out DIR`.
A changed `--diff-base` misses the index cache and forces `--full`. An incremental index that parses 0 files while the three-dot diff or the GitHub PR file list is non-empty is re-run with `--full`.
PR collect writes `26-review-digest.json` after the signal files. Judgment reads that digest for commits behind/ahead, file-class counts, report rows, and dimension cards. Full path lists stay in `26-review-digest-detail.json`. Do not recompute the split with git or open every signal file for the dimension verdict. Residual reading opens each `24-coverage-ledger.json` `read_groups` entry once and still writes one closure row per pending symbol. Non-source files are not residual symbols. Byte-identical copies are scanned once; findings keep every path. Files whose bytes differ are both scanned.

### 3. Validate

```bash
./scripts/validate-evidence.sh --dir <OUT_DIR> --mode pr   # or --mode full
```

Fails: missing CodexQA provenance; empty change-groups; all `change_status=default`;
`lang_stats` present but `primary_language` null. Legacy packs may WARN and still pass.

`stubs≥20` (numeric or `{total:N}`) → cap edge/reach findings at **UNKNOWN**; do not treat `from_count` as real fan-in — prefer `edges-in` callers.

### 4. Review from artifacts

1. When `31-model-brief.json` is absent, read [prompts/pr-diff-review.md](prompts/pr-diff-review.md) or
   [prompts/full-repo-review.md](prompts/full-repo-review.md). When it exists, do not open those prompts.
2. Confirm `manifest.engine` is `codexqa` (or legacy codexqa in commands). Else blocked.
3. Lock language from `manifest.json` + `09-language-profile.json`.
4. For top risks: `diffs/`, `impact/<id>/`, `paths/`, then tags / hot-but-thin / sensitive.
5. Mermaid from [references/mermaid-evidence.md](references/mermaid-evidence.md).
6. **Detection rules** live on the owner dimension card (index:
   [references/dimension-registry.md](references/dimension-registry.md)).
   Build and extend them only with
   [references/rule-construction.md](references/rule-construction.md):
   a rule is a relation plus role-shaped variants, one hit does not close
   the family, and a hard-gate row is a visible finding. Pattern-class
   defects with `disposition: report` are filed from `23-sast-signals.json`.
   `drop` is discarded. Only `suspects[]` go to the SAST suspect channel.
   `allow` records a scanner gap and does not rescan that class. CodexQA
   stays the primary engine.
7. **Agent LLM judgment (order 16):** when `31-model-brief.json` exists, jq `still_open`, `open_suspects`, `test_oracle_open`, and `output` only. Findings in `judgment.json` are already copied from `candidate_hits`. Do not rewrite `title`, `risk`, `fix`, `line`, or `severity`. If those three lists are empty, do not add a finding, do not read methods or `judgment-work`, and render. If a list is non-empty, judge each shape once and read only its hosts. Do not restate `look_for`, `do_not_report`, or `closed_lines`. Do not open rule-construction or `review-conclusion.json`. A different shape is a separate finding. Copy `preset` under `oracle`, judge only `questions`, and leave a preset key unchanged. `boundary_missed` stays false unless `preset` is true. `title`, `risk`, and `fix` are Chinese; leave the English fields empty. An id already in `suspect_hits` is closed. A failed render names the sentence to edit. Do not grep seal or validate scripts for fields. Do not walk `24`, regroup closed rows, or open templates, examples, dimension docs, or `seal-conclusion.py`. When `31` is absent, follow [prompts/llm-judgment-pass.md](prompts/llm-judgment-pass.md).
   On that legacy path, SAST suspects, business logic, and semantic candidates are separate prompts. The residual
   read visits every `pending` symbol in `24-coverage-ledger.json`; scanner hits do not dequeue it.
   The host embedded model reviews those packets, then `scripts/lib/merge-llm-findings.py`
   dedupes `p0`/`p1`/`p2` against heuristic findings (`22-llm-judgment.json`).

### 5. Deliver

1. Optional chat notes: [templates/review-report.md](templates/review-report.md)
2. **Required:** `review-conclusion.json` is already in the pack. Do not replace it.
3. **Required:** `./scripts/render-review-html.sh --dir <OUT_DIR>` → **`REVIEW-REPORT.html`**
   and **`review-comments.json`** (same defect id, no score).
   Render runs `scripts/lib/seal-conclusion.py` before
   `scripts/lib/validate-conclusion.py`. The seal fills report-row cards,
   `span_hash`, `test_gaps`, rule shapes, default oracle skips, and unconfirmed
   per-line skips from the pack. The model writes `judgment.json` only.
   The gate still refuses HTML when any check fails after that fill:
   - Every behavioral `disposition: report` row is the primary `line` of a finding,
     or an `also_lines` entry with `same_fix: true`. A line number written only in
     prose does not close the row. One finding cannot close two `rule_id`,
     `pattern_class`, or `kind` values. Magic numbers, long files, and stale imports close
     in `conventions`, not in P0/P1/P2. A sentence that says another card covers
     a defect must name a line that a finding lists.
   - Each `test_oracle_inventory` row has `oracle.unsafe_pass`,
     `oracle.boundary_missed`, and `oracle.branch_uncovered`, plus that row's
     extra questions. Skip is legal only when every flag is false.
   - Production symbols with `tested_count == 0` are in `test_gaps.symbols` or
     `waived_symbols` inside `review-conclusion.json`. The HTML report does not
     render that table. A static initializer, a type or constructor, a get/set/is
     accessor, or a private helper goes to `waived_symbols`. A rule whose look-for has several shapes lists
     every shape; the first hit does not close the rest.

Cover: 页头四块（能否合入、最高严重级别、行为缺陷数与证据行数、必测三条路径）、一张卡一个失败场景、规范项（不计缺陷）、回归必测清单、敏感路径。有问题的维度和调用链默认折叠，排在发现项之后。`ok`/`none` 维度不进报告。`seal-conclusion.py` 在渲染前用信号文件补上结论里空着的维度（风险分档、架构契合、复杂度、依赖、韧性、隐私、变更发布、性能、模型语义评审），所以判定稿不写维度长文时，HTML 仍会展示有信号的维度。
**不渲染：** 测试缺口表、建议修复顺序、残留风险与假设、独立影响面示意。`test_gaps` 仍写入 `review-conclusion.json` 供闭合校验，不进 HTML。
`render-review-html.sh` 会过滤干净维度；仍须在 `review-conclusion.json` 写全评估结果与
`dimensions_covered`。Final findings must already be **dedupe-merged** (no duplicate
heuristic + LLM cards for the same defect).

High-severity findings cite: symbol id/file/lines, callers or entry path,
`tested_count` / tests-reach, confidence (high|medium|low|**UNKNOWN**).
Human-facing prose (dimension `hotspots`, finding risk/evidence, summary) must
explain risks in plain language — see [references/review-dimensions.md](references/review-dimensions.md)
**Reader prose**.

**Card voice** (scanner cards in `scripts/lib/seal-conclusion.py`, model cards in
[prompts/llm-judgment-pass.md](prompts/llm-judgment-pass.md)):

- `title`: SARIF `shortDescription`，规则名，例如 `SQL 注入`。不写规则编号，不写 `这一行不是…`。
- `risk`: Semgrep / SARIF `message`。`在第 N 行检测到 \`代码\`。` 接一条影响。不写 `不会` / `不是` / `而不是`。
- `fix`: SARIF `fix` / Sonar recommendation。`将第 N 行 \`代码\` 改为：` 接安全写法。不写 `不用` / `不要` / `而不是`。
- `call_chain`: `谁会走到这一行`. No recorded caller stays `未记录调用方`, not `没有入边` and not a dead function. Do not add that the index is thin, that stubs capped confidence at UNKNOWN, or that real edges may be missing.
- Stub counts and the UNKNOWN confidence cap stay in the validate log and `manifest.index_quality`. Do not put them in `REVIEW-REPORT.html` or in the user-facing summary.
- PR cards only. A file outside the three-dot diff is a branch-drift skip, not `既有代码`.

**Bilingual HTML:** Write primary prose in Chinese (`summary`, `intent`, `scope`,
dimension `risk`/`yagni`/`evidence`, finding `title`/`risk`/`evidence`/`fix`,
`call_chain.title`, regression/test-gap notes, `sensitive`). On `judgment.json`
findings, leave `title_en`, `risk_en`, and `fix_en` empty. `seal-conclusion.py`
copies the Chinese text into those English fields at render. The HTML
toolbar switches `data-zh`/`data-en`; a hand-written English card is not required
for delivery.

## Blocked result

```markdown
### Code Review Blocked
- status: blocked
- missing_gate: missing_codexqa_engine | missing_code_identity | missing_reviewable_change | ...
- supplied: ...
- required: ...
- next_commands: ...
```

Do not emit P0/P1/P2 or merge advice when blocked.

## Examples

End-to-end walkthrough: [examples/pr-review-walkthrough.md](examples/pr-review-walkthrough.md)

## Progressive disclosure

- CLI contract: [references/codexqa-cli-contract.md](references/codexqa-cli-contract.md)
- Language profile: [references/language-profile.md](references/language-profile.md)
- Industry bar: [references/industry-bar.md](references/industry-bar.md)
- Dimension registry: [references/dimension-registry.md](references/dimension-registry.md)
- Rule construction (mandatory for new or extended detection rules): [references/rule-construction.md](references/rule-construction.md)
- Dimensions: [references/review-dimensions.md](references/review-dimensions.md)
- Design fit card: [references/dimensions/design-fit.md](references/dimensions/design-fit.md)
- Complexity card: [references/dimensions/complexity.md](references/dimensions/complexity.md)
- Dependencies card: [references/dimensions/dependencies.md](references/dimensions/dependencies.md)
- Privacy card: [references/dimensions/privacy.md](references/dimensions/privacy.md)
- Resilience card: [references/dimensions/resilience.md](references/dimensions/resilience.md)
- Change / rollout card: [references/dimensions/rollout.md](references/dimensions/rollout.md)
- Risk tier card: [references/dimensions/risk-tier.md](references/dimensions/risk-tier.md)
- Observability card: [references/dimensions/observability.md](references/dimensions/observability.md)
- Contract card: [references/dimensions/contract.md](references/dimensions/contract.md)
- Maintainability card: [references/dimensions/maintainability.md](references/dimensions/maintainability.md)
- Performance card: [references/dimensions/performance.md](references/dimensions/performance.md)
- Agent LLM judgment card: [references/dimensions/llm-judgment.md](references/dimensions/llm-judgment.md)
- LLM judgment pass prompt: [prompts/llm-judgment-pass.md](prompts/llm-judgment-pass.md)
- Correctness card: [references/dimensions/correctness.md](references/dimensions/correctness.md)
- Security card: [references/dimensions/security.md](references/dimensions/security.md)
- Concurrency card: [references/dimensions/concurrency.md](references/dimensions/concurrency.md)
- Correctness family checks: [references/dimensions/correctness-family-checks.md](references/dimensions/correctness-family-checks.md)
- Eval gate: `scripts/validate-skill.sh` + [evals/eval.yaml](evals/eval.yaml)
- Plan audit: `scripts/audit-plan-coverage.sh` → [examples/plan-coverage-audit.md](examples/plan-coverage-audit.md)

## Common pitfalls

- Do not treat README / subjective scoring as graph evidence.
- Do not equate “file under `test/`” / test directory names with `tests` edges
  (`tested_count > 0`). Path names do not prove coverage.
- Do not add a detection rule whose look-for is a sample API, constant, or
  test name. Extend a family in `references/rule-construction.md`.
- Do not run `codexqa wiki` / `chat` unless the user asks (LLM cost).
- Do not claim reflective / cross-language calls are complete; label uncertainty.
- Multi-branch: pin `@branch` on `repo_id`; do not guess.
- Never skip CodexQA for Java/Go/TS “to save time”.
- Never invent primary language from folders/README.
- A failed `command -v codexqa` is not a missing CLI. The npm prefix is often off the default PATH. Run the Preflight gate once before install, collect, or review.
