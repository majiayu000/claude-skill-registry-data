---
name: cc
description: Claude × Codex × GPT-5.5 Pro × Gemini 3 Pro 多模型协作流水线(Anthropic/OpenAI/Google 三族交叉互审)。当 Tony 说「cc」「走 cc」「用 cc 做」「cc 这个任务」「cc 流程」「多模型协作做 X」时触发。风险驱动:先给任务分级(L1/L2/L3),按级路由模型组合,maker/checker 跨模型族真隔离 + 证据锚定 + 机器可恢复。所有模型调用统一走 cc-run.sh(stdin 传参/全量落盘/VERDICT 解析/secret 防线/state 落盘)。用于需要高把握、跨模型族互审的编码任务。
allowed-tools: Bash, Read, Edit, Write, Grep, Glob, Task, TodoWrite
---

# cc —— 风险驱动的多模型协作流水线(v2)

把一个编码任务交给四个角色协作(Anthropic / OpenAI / Google 三个独立模型族),**按风险分级路由 + maker/checker 跨族真隔离 + 证据锚定 + 机器可恢复**。Claude Code(你)= 总编排 + 验收人。

> **v2 元原则(三方审核共识)**:多模型共识 ≠ 可靠通过;prompt 走 wrapper ≠ 工程安全。价值不在"再加模型",而在把**状态/证据/闸门/降级**做成机器可验证。不要把 cc 跑成"都跑一遍"的仪式——按风险给最省的有效组合。

## 0. 绝对铁律(违反即破坏整条流水线)
1. **所有外部模型调用必须走 `cc-run.sh`**,严禁裸 `codex`/`agy`/`gpt5pro`(裸调 = 丢全量日志/丢 exit/截断/注入/无 UNKNOWN 防线)。wrapper 路径:`~/.claude/skills/cc/cc-run.sh`。
2. **maker 不自评,且要跨模型族**:Codex 写的代码,二审主审用**异族**(Gemini 或 Claude),不能又用 Codex(同族盲区共振 = 假独立)。
3. **VERDICT 闸门**:每个 review 以判词结尾(`VERDICT: X` 或 JSON footer),由 `cc-run.sh` 解析的 `.verdict` 文件驱动循环,不靠肉眼。
4. **UNKNOWN/BLOCKED ≠ 通过**:任何调用失败/超时/拒答 → `.verdict=UNKNOWN`,绝不当 APPROVED;高风险审查方失败 → 标 `BLOCKED`,不自动降级,等人工。
5. **证据锚定**:关键判断必须引用 file:line / 命令输出 / 测试结果;无证据的"通过"标 `UNVERIFIED_CLAIM`。
6. **循环有预算 + 内禁不可逆**:每循环 ≤ 上限(见各步);循环内不 push/merge/删数据/发外部。
7. **状态落盘**:产物进 `$WORK`,`state.jsonl` 机器可读,中断可 `cc-run.sh status $WORK` 恢复。

## 调用范式(唯一正确姿势)
```bash
RUN=~/.claude/skills/cc/cc-run.sh
# 1) 把 prompt 写进文件(自包含),再让 wrapper 走 stdin 传给模型
printf '%s' "$PROMPT" > "$WORK/prompts/<role>.txt"
# 2) 调用(role=语义标签;cli∈codex|agy|gpt5pro;sandbox 默认 read-only)
bash "$RUN" call <role> <cli> "$WORK/prompts/<role>.txt" "$WORK/verdicts" [read-only|workspace-write]
# 3) 读结果:全量 $WORK/verdicts/<role>.full.log;判词 $WORK/verdicts/<role>.verdict
```
- **codex/agy 必须前台调用**(后台丢 PATH/环境;wrapper 已用绝对路径但仍守此规)。
- wrapper 自动:secret 预扫(命中私钥/token 即拒)、全量落盘、超时进程组清理、verdict 解析、state.jsonl 追加。
- 账号约束:codex 只能 `-m gpt-5.5`;agy 用 `gemini-3-pro-high`;gpt5pro 网页桶无痕。

---

## 步骤 0:初始化 + 能力探测
```bash
TS=$(date +%Y%m%d-%H%M%S)
SLUG=$(bash ~/.claude/skills/cc/cc-run.sh slug "<任务关键词>")   # 中文转拼音/保 ascii/空则 task
WORK=".omc/cc/${SLUG}-${TS}"; mkdir -p "$WORK"/{context,prompts,verdicts,patches,reviews,verify,final}
bash ~/.claude/skills/cc/cc-run.sh probe "$WORK"   # 写 capabilities.md;UNAVAILABLE 的模型不得算有效审查方
```
建 `$WORK/ledger.md`:DoD(Must/Won't/验收命令/停止条件)+ 各步勾选。

## 步骤 0.5:风险分级(Triage)→ 决定跑哪条路由 ⭐v2 新增
先判 `risk_level`,**只跑该级所需**,不要无脑五步。判据(取最高命中级):

| 级别 | 判据(任一命中即归此级或更高) | 路由(模型组合) |
|------|------------------------------|----------------|
| **L1 轻** | <20 行改动、单文件、无状态、不触敏感目录、可逆 | Claude 规划 → Codex 执行(③)→ Claude review(④)。**跳过外部规划①、跳过隔离二审⑤** |
| **L2 标准** | 普通功能、20–80 行、多文件但边界清晰 | Claude+Codex 红队规划(②简版)→ Codex 执行(③)→ Claude review(④)→ **Codex 隔离单审⑤ 1 轮** |
| **L3 高危** | >80 行 / 触及 安全·认证·支付·数据库·文件系统·网络 / 公开资产 / **客户交付** / 易错重构 / 迁移 | 全量①–⑤:三族规划 → 执行 → Claude 审 → **跨族二审(Gemini 全repo + Codex)+ 一票否决**;不收敛调 GPT-5.5 Pro 仲裁 |

把 `risk_level` 写进 `ledger.md`。**拿不准就升一级**(宁可多审不可漏审),但别给 L1 套 L3。

---

## 步骤 ①:三族独立规划(仅 L3 全量;L2 简版只 Claude+Codex;L1 跳过)
目标:同一任务拿到**独立**方案(独立性是命门,别互相看)。统一输出 schema:`Assumptions / Plan / TaskBreakdown / Risks / TestStrategy / OpenQuestions`。

1. **先发慢的外部模型**(各 1–5min,先发好并行后台等待 wrapper 返回),prompt 自包含(任务/约束/**事实包**——只给代码事实,不给 Claude 的方案倾向,保独立):
   ```bash
   printf '%s' "$PLAN_PROMPT" > "$WORK/prompts/plan-gemini.txt"
   bash "$RUN" call plan-gemini agy "$WORK/prompts/plan-gemini.txt" "$WORK/verdicts" read-only &
   # L3 且需深推理架构时才加 GPT-5.5 Pro(最贵桶,见下"GPT-5.5 Pro 触发判据"):
   # printf '%s' "$PLAN_PROMPT" > "$WORK/prompts/plan-gpt5pro.txt"
   # bash "$RUN" call plan-gpt5pro gpt5pro "$WORK/prompts/plan-gpt5pro.txt" "$WORK/verdicts" &
   wait
   ```
   **Gemini 甜区:让它读整个 repo** —— 规划时可在 prompt 里说明项目结构,审查时用 `--add-dir`(见步⑤)。
2. **同时 Claude 自己独立写一份** → `$WORK/context/plan-claude.md`(先写完自己的再读别人,保独立)。
3. 外部失败不阻塞:用就绪的继续(至少 Claude + 一个外部族)。失败方在最终报告写**降级声明**。

## 步骤 ②:Codex 整合挑刺 + Claude↔Codex 到一致(循环 1,≤3 轮)
目标:一份双方认可的定稿 `$WORK/context/plan-final.md`。**对抗姿态**:Codex 默认 `REVISE`,除非找不到任何实质问题才 `CONSENSUS`。
```bash
# 把待审计划组装进 prompt 文件(首轮喂三份原始;次轮起喂 plan-final 草稿)
printf '你是资深架构评审,默认怀疑。整合并批判下列计划,找漏洞/缺步骤/风险/三份分歧点。给整合改进版+问题清单(步骤级)。结尾恰一行 VERDICT: CONSENSUS 或 VERDICT: REVISE。\n\n=== 计划 ===\n' > "$WORK/prompts/consensus-r$ROUND.txt"
cat "$WORK/context/plan-final.md" 2>/dev/null || cat "$WORK/context/plan-claude.md" "$WORK/verdicts/plan-*.full.log" 2>/dev/null >> "$WORK/prompts/consensus-r$ROUND.txt"
bash "$RUN" call consensus-r$ROUND codex "$WORK/prompts/consensus-r$ROUND.txt" "$WORK/verdicts" read-only
```
- Claude 评估 Codex 批评(receiving-code-review 纪律:先验证对不对,不盲从),更新 `plan-final.md`,记 `$WORK/reviews/consensus-log.md`。
- **Exit**:`.verdict=CONSENSUS` 且 Claude 认可 → 退出。
- **Budget ≤3 轮**(三方共识:3 轮不收敛多半是表述歧义或架构死结)。到顶仍 REVISE → **默认停手**,把分歧写进 `plan-final.md` 标 `[需人工]`;仅当残留分歧全是 Medium/Low 且 Claude 写明取舍,才允许带定稿继续。
- **计划冻结**:定稿后 `shasum "$WORK/context/plan-final.md"` 记 hash 进 ledger,执行引用该 hash;改计划必出新版本。

## 步骤 ③:Codex 按定稿执行(写)
```bash
printf '严格按下列定稿实现,不自行扩 scope,每步简述改了什么。\n\n' > "$WORK/prompts/exec.txt"
cat "$WORK/context/plan-final.md" >> "$WORK/prompts/exec.txt"
git --no-pager diff > "$WORK/patches/baseline.patch"   # 执行前快照,失败可回滚
bash "$RUN" call exec codex "$WORK/prompts/exec.txt" "$WORK/verdicts" workspace-write
```
- 大改/并行用 git worktree 隔离防 stomp;主工作区直接改要确认 scope。
- 收集**完整改动清单**(三方盲区:diff 不只 unstaged):
  ```bash
  git --no-pager diff > "$WORK/patches/diff.patch"
  git --no-pager diff --cached >> "$WORK/patches/diff.patch"
  git status --short > "$WORK/patches/status.txt"
  git ls-files --others --exclude-standard > "$WORK/patches/untracked.txt"
  ```
- **scope 守门**:对照定稿检查 touched files,超出计划范围 → 视为 REVISE,回步②。

## 步骤 ④:Claude code review(maker/checker 第一道,跨族)
Claude 亲审 Codex diff:正确性/边界/回归/是否符合定稿意图/测试够不够。结果 → `$WORK/reviews/review-claude.md`(每条 file:line + 严重度)。发现问题交 Codex 修(`workspace-write`),复审,小循环 ≤3 轮。无 High/Critical 遗留 → 进步⑤。

## 步骤 ⑤:跨族隔离二审 + 最终报告 ⭐v2 重构
**核心修复**:二审主审用**异族**,不是又一个 Codex(同族 = 假独立)。

**组装"非盲"审查包**(三方共识:diff 不自包含,盲审漏报率高+幻觉误报):
```bash
# 把被改文件 + 其核心依赖(import 的本地文件)读进 context,随 diff 一起给审查方
# Claude 负责挑选受影响文件,写进 $WORK/context/review-context.md
```

- **L2 routine**:Codex 隔离单审 1 轮(干净会话,prompt 注明"独立二审、无前序上下文"):
  ```bash
  printf '你是独立二审,无前序上下文。依据【定稿】【受影响文件上下文】【diff】对抗式审查:bug/安全/边界/与计划不符。给清单(file:line+严重度)。结尾恰一行 VERDICT: APPROVED 或 VERDICT: ISSUES_FOUND。\n' > "$WORK/prompts/iso-r$ROUND.txt"
  cat "$WORK/context/plan-final.md" "$WORK/context/review-context.md" "$WORK/patches/diff.patch" >> "$WORK/prompts/iso-r$ROUND.txt"
  bash "$RUN" call iso-r$ROUND codex "$WORK/prompts/iso-r$ROUND.txt" "$WORK/verdicts" read-only
  ```
- **L3 高危:跨族交叉 + 一票否决**(替代旧 2/3 多数票——三方共识:Claude 是编排者有偏见,非独立票;多数票会掩盖安全问题):
  - **Gemini 全 repo 回归审**(激活其 1M 上下文唯一价值,经 wrapper 透传 `--add-dir`,仍享 verdict/state/全量落盘):
    ```bash
    AGY_ADD_DIR=<项目根> bash "$RUN" call gemini-r$ROUND agy "$WORK/prompts/iso-r$ROUND.txt" "$WORK/verdicts" read-only
    ```
    (Gemini 专审:全局依赖影响/跨文件调用链/接口签名一致性——Claude/Codex 上下文装不下的盲区。)
  - **判定 = 一票否决**:Codex 或 Gemini 任一报 High/Critical 且经 Claude 验证属实 → **必修**,回本轮重审。不靠投票通过。
  - 审查方失败(UNKNOWN)→ 标 `BLOCKED`,不降级,告知 Tony。
- **Budget ≤3 轮**;到顶仍有未修真问题 → 列残留 + `[需人工]`,不谎称通过。
- **可执行验证**:跑项目 test/build/lint(步0 扫出的 `verify.sh`),证据进报告;无 verifier 显式标"需人工确认"。

### 最终报告 → `$WORK/final/report.md`(回贴 Tony,简洁)
含:任务 / risk_level / 定稿要点+hash / 一致轮次 / 改了哪些文件 / Claude审+跨族二审结论 / **降级声明**(原定审查方 vs 实际 / 失败原因 / 风险影响)/ 可执行验证证据 / 残留 `[需人工]` / 下一步(push/merge 由 Tony 拍板,流水线内不做)。
同时出 `$WORK/final/run-summary.json`(可作客户交付证据:做了什么/谁审过/如何验证/残留风险)。

## GPT-5.5 Pro 触发判据(最贵桶,用在刀刃 ⭐v2 重定位)
**不再进常规规划**。仅以下触发(否则不调,省桶):
- 步② Claude↔Codex 连续 2 轮不收敛 → GPT-5.5 Pro 做**首席仲裁**定分歧。
- L3 触及核心架构/公共 API/迁移/性能重构 → GPT-5.5 Pro 做**架构红队/发布前终审**。
```bash
printf '%s' "$ARBITRATION_PROMPT" > "$WORK/prompts/arbiter.txt"
bash "$RUN" call arbiter gpt5pro "$WORK/prompts/arbiter.txt" "$WORK/verdicts"
```

## 失败与恢复
- 任一调用失败:wrapper 自动记 `UNKNOWN`(≠通过)。重试 1 次仍失败按上面 BLOCKED/降级处理。
- `gpt5pro` 报 `session=no` → 提示 Tony 在 bb-browser 的 Chrome 登录 ChatGPT Pro。
- `agy` 报 "Please sign in" → 提示 Tony 裸跑一次 `agy` 登录 Google/Gemini。
- **中断恢复**:`bash ~/.claude/skills/cc/cc-run.sh status "$WORK"` 看已发生调用 + 异常,读 `ledger.md` 跳过 `[x]` 续跑。

## 何时用 / 不用
- **用**:把握要求高、值得跨族互审的编码任务(架构落地/关键模块/易错重构/客户交付)。
- **不用**:一行小改、纯查询、机械批量 → 直接做或走 L1,别为仪式跑五步烧多份额度。
- **省钱默认**:先 Triage,大多数任务是 L1/L2,只有真高危才 L3 全量。

分工背景见 memory `reference_claude-codex-collab-protocol`、`reference_gpt5pro-bridge`;Codex 细节见 `reference_codex-exec-resume-flags`、`reference_codex-mcp-chatgpt-account-model`;审核留痕见 `~/.omc/cc/audit-synthesis.md`。
