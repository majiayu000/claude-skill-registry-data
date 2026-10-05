---
name: codexqa-skill-router
description: >
  Auto-routes a user request to the matching codexqa skill, then ensures that
  skill is on disk and follows its SKILL.md. Use whenever the user is unsure
  which skill to run, says 帮我选 skill、自动路由、选哪个 skill、不知道用哪个、
  route this request、pick the right skill、codexqa 该用哪个, installs only
  codexqa-skill-router and still needs a worker skill, or describes a verification /
  QA / testing / review / RCA / requirements / cases / testdata task without
  naming a skill. Former skill name: skill-router. Matches against live siblings plus a bundled catalog so newly
  published pack skills remain routable; if the winner is not installed, fetch
  it beside this router (ask once, then ensure_skill.py --yes) and hand off —
  do not invent a parallel workflow. Not a replacement for any target skill.
license: Apache-2.0
compatibility: >
  Requires Python 3.10+ on PATH for discover/ensure scripts (auto re-execs from
  older system python3). On-demand install needs network (GitHub tarball) or a
  local --from-repo checkout; optional npx skills add fallback. Target skills
  may need their own runtimes (Node, Python 3.10+, codexqa CLI, etc.).
metadata:
  version: "1.2.0"
---

# codexqa-skill-router

Agent entry map for **discover → match → ensure installed → hand off**. Human
docs (`README.md`, `HOW_IT_WORKS.md`, `KNOWN_LIMITATIONS.md` and `.zh-CN` twins)
are not loaded at runtime.

This skill does not implement defect scans, case writing, RCA, or data build.
It selects a pack skill, makes sure its files exist next to this router, then
**executes that skill's contract**.

## 1. Discover (mandatory, every turn)

Refresh the match catalog:

```bash
python3 <this_skill_dir>/scripts/discover_skills.py --with-catalog
```

- Live siblings with `SKILL.md` appear as `source: "live"`, `installed: true`.
- Missing workers still appear from [references/catalog.json](references/catalog.json)
  as `source: "bundled"`, `installed: false` (for matching only).
- `needsInstall` lists names that must be fetched before hand-off.
- Optional: `--skills-root <abs-path>` when the pack is not this skill's parent.
- Self-check: `python3 …/discover_skills.py --self-check`.

Do **not** hard-code the worker list in your reasoning — use the JSON. New
skills become matchable after `catalog.json` is refreshed (maintainers:
`scripts/refresh_catalog.py` in a full checkout). `codexqa-skill-router` is excluded.

If discovery fails entirely (script error), stop and report it. An empty
*live* count is OK when the bundled catalog is non-empty.

Detailed match rules: [references/routing-rules.md](references/routing-rules.md).

## 2. Match the user request

Read the user's latest message (and only this-turn attachments they named).
Discover still supplies the catalog. Routing does **not** score by overlapping
words in descriptions. Run the decider:

```bash
python3 <this_skill_dir>/scripts/suggest_route.py --text "<user message>"
```

Use `--text-file` when the message is long. If the script fails, stop and
report the error — do not fall back to keyword overlap.

| `outcome` | Action |
|---|---|
| `clear` or `explicit` | Ensure + hand off to `winner` (sections 3–4) |
| `explicit_conflict` | Do not start the named skill. Show `reason` and `alternatives`. Wait |
| `ambiguous` | Ask once with at most three `alternatives` and one-line why. Wait |
| `chain` | Propose `steps` in order. Ensure/start the first only after confirm |
| `none` | Say no catalog skill claimed it; list catalog names; do not invent one |

A `clear` / `explicit` winner is authoritative. Description text must not
override it. In particular, `codexqa-defect-analyzer`'s phrase "review a
diff/MR/PR" is an incremental **scan** scenario. It does not claim 代码评审,
code review, PR review, or "review this PR".

Task shape, not the shared verb:

- 代码评审 / 代码审查 / 走查 / 单文件或整仓评审 / code review / PR·MR review / 审查意见 / 语义评审 / 双语审查 / 证据包 / 合入建议 / 这段代码有没有问题 → `codexqa-code-reviewer`
- 缺陷检测 / SAST / 漏洞·密钥·依赖·CVE / 安全基线 / 粘贴或上传代码找漏洞 / `report_scan` / "review this diff for vulnerabilities" → `codexqa-defect-analyzer`. 格式化、自动改风格不归这里
- Both a review report and a scan list, with no order → `ambiguous` (ask). 先评审再扫描 → `chain`, reviewer then defect
- 影响面 / 谁在调用 / 入口风险 / 敏感路径 / 测试缺口 / 有没有单测 / 回归哪些 / 相对 main 变了什么 / 建索引 / 错误定位 / 模块归属 → `codexqa-code-analyzer`. Those words inside a 代码评审 stay with the reviewer. 补测试缺口 stays here; 补测试 / 写用例 does not
- 变更分析 / 变更代码分析 / 变更影响报告 / 影响入口 / 召回测试用例 / change impact report, or impact words on one diff (变更 / 改动 / PR / diff / 分支) plus an HTML report or 补上缺的测试 → `codexqa-change-analysis`. 只要影响面, a report with no diff, or a named analyzer stays with the analyzer; inside a 代码评审 it stays with the reviewer; PRD or 提测 cases stay with the testcase generator; 先…再… stays a chain
- 架构 wiki / 模块地图 / 模块划分 / 从哪开始读 / 阅读导览 / 仓库导览 / 这个模块是干什么 / `wiki inputs` → `codexqa-code-wiki`. Bare 知识图谱 → ask (wiki vs analyzer)
- 堆栈 / 根因 / 崩溃 / 报错原因 / 线上报错 / 日志里的异常 / 调试输出 / 根因报告 → `codexqa-rootcause-analyzer`. A call chain or "报错在哪" used to explain that failure stays root-cause
- 需求评审 / 需求缺口 / 需求歧义 / 需求一致性 / 非功能需求 / 需求能不能测 / requirements review → `codexqa-requirement-analyzer`, not a code review
- 测试方案 / 测试分析 / 写用例 / 方案和用例 / 按 PRD 出测试 / 提测前改用例 / 提测后补用例 / test plan → `codexqa-testcase-generator`. 写单元测试不归这里
- 造数据 / 用例物料 / 前置账号 / 造一笔订单 / 造数脚本 / 发布成工具 / 回写前置 / OpenAPI 造账号 → `codexqa-testdata-generator`

When the user names a catalog skill whose own boundary rejects that task
shape, `outcome` is `explicit_conflict`: warn and offer `alternatives`. Do
not install the rejected fit. Detail: [references/routing-rules.md](references/routing-rules.md).

## 3. Ensure the winner is installed

If the chosen entry has `installed: false` (or no `skillMd` on disk):

1. Tell the user in one sentence that you will install `<name>` beside
   `codexqa-skill-router` so you can follow its contract (network fetch from the
   codexqa pack, unless a local checkout is available).
2. If the user refuses, stop and give the manual hint:
   `npx skills add openqa-cn/codexqa --skill <name>`.
3. If they agree (or already said to proceed / auto-route fully), run:

```bash
python3 <this_skill_dir>/scripts/ensure_skill.py <name> --yes
```

Dev / offline: add `--from-repo /path/to/codexqa` to copy from a local clone
instead of the network. Dry-run: omit `--yes` or pass `--dry-run`.

4. Re-run `discover_skills.py --with-catalog` and confirm the skill is
   `installed: true` with a real `skillMd` path. If ensure failed, show the
   JSON error and stop — do not invent the worker workflow.

Why ask once: installing copies third-party skill files onto disk. Why still
automate: a router that only prints a name does not complete the user's task.

## 4. Hand off and execute

1. Announce the choice in one short sentence: skill name + why (+ "installed
   just now" if ensure ran).
2. **Read** the chosen `skillMd` (and only the references that skill says to
   load next). Prefer the path returned by discover/ensure — do not rely on
   the host having re-indexed its skill list yet.
3. **Follow that skill completely** for the user's request — same gates,
   scripts, and artifacts.
4. Do not re-implement the target skill inside this router. Do not skip its
   "ask before Exec" or similar stop conditions.
5. If mid-flight the work clearly belongs elsewhere, stop, re-discover, and
   re-route (ensure the new winner if needed).

## 5. Done criteria

Routing is done when either:

- the chosen skill's own done criteria are met, or
- you asked a clarification / install-consent question and are waiting, or
- you reported that no catalog skill fits or ensure failed.

## 6. Boundaries

- Does not replace worker skills; it only selects, installs if needed, and
  follows them.
- Does not install missing CLIs (`codexqa`, `jq`, …); the target skill's
  compatibility section still applies after hand-off.
- Does not edit sibling skills as part of routing (install/copy only).
- Bundled `catalog.json` may lag a brand-new unpublished skill until refreshed;
  live siblings still win when present.
