---
name: briefbound-skill-authoring
description: "Use when adding, changing, or removing a skill in the Briefbound package itself: contract structure, routing anchors, catalogs, test cases, validator budgets, and install refresh; do not use for ordinary project features or general documentation work."
license: MIT
---

# Briefbound Skill Authoring

## 目标

让技能包自身的增、改、删保持一致：契约结构、路由可达、目录登记、用例覆盖、预算不越线、校验全绿。它只维护技能包，不实现业务功能。

## Briefbound task contract

- Context Boundary: 目标技能与动机、触发/排除语义、与相邻 owner 的边界、允许写入的包内路径。
- Output Contract: 技能目录（SKILL.md、agents/openai.yaml、按需 references/）、全部锚点同步、测试用例、预算登记和校验结果。
- Allowed Action: 修改 `skills/`、`tests/`、`scripts/`、`.claude-plugin/plugin.json`、README 与桶 README；不动无关技能内容。
- Success Evidence: `validate_briefbound_skills.py --repo-root .` 退出码 0；新旧技能在 routing_cases 各有正/负用例；徽章计数与实际技能数一致。
- Stop Condition: 设计分歧需用户拍板、router 预算无法在不破坏语义下腾出、或改动会破坏既有 pinned markers。
- Route Out: 包外实现工作回对应工程 owner；已验证残留 `briefbound-development-cleanup`；`briefbound-router` 或 BLOCKED。

## 统一调用契约

- 只处理 Briefbound task contract 范围；复合任务不吞其他 owner。
- 用户可见内容默认中文，先说技能定位与边界，再报锚点清单与校验结果；Route Out 仅以 Briefbound task contract 为准，有自然闸门时末行 `下一步建议: <一个具体动作>`，否则继续已授权工作。

## 激活闸门

请求对象是技能包本身的技能新增、修改、删除或结构变更时进入。给业务项目写 prompt、文档或配置不适用本 skill。

## 契约结构

每个技能必须满足校验器的结构规则：

- `SKILL.md` frontmatter：`name`、英文 `description`（Use when…/do not use…）、`license: MIT`。
- 恰好一条 `- Route Out:`（任务契约内）；输出示例中的 Route Out 只能写 `Route Out: <沿用 Briefbound task contract>`。
- 统一调用契约四标记：`## 统一调用契约`、`用户可见内容默认中文`、`下一步建议: <一个具体动作>`、`Route Out 仅以 Briefbound task contract 为准`。
- 会写文件或改环境的技能加入 `DIRECT_WRITE_OWNERS`，且 Route Out 必须含 `briefbound-development-cleanup`。
- `agents/openai.yaml` 三字段：display_name、short_description、default_prompt（引用 `$skill-name`）。
- 正文引用的每个 `briefbound-*` 名字都必须是已打包技能。

## 预算纪律

- 估算公式：CJK 字符 + 拉丁词数 × 1.3 + 标点 ÷ 3。
- router `SKILL.md` 的组合预算（alignment/maximum profile）在上游压线：**只能缩不能增**；新增路由提及必须先在别处等量压缩。
- `routing-practice.md` 预算同样贴线；新增行先压缩既有行。
- pinned markers（`ROUTER_CORE_MARKERS`、`ROUTER_REFERENCE_REQUIRED_MARKERS`、各专项契约块）不可触碰；压缩前先核对清单。
- 新技能预算按实测 token 加约 150 余量登记进 `TOKEN_BUDGETS`。

## 完整锚点清单

新增一个技能要同步：router `SKILL.md` 路由提及、`references/routing-practice.md` 仲裁行、`.claude-plugin/plugin.json`、桶 `README.md`、`README.zh-CN.md` 与 `README.md`（精选行、完整目录条目、结构树行、徽章与数量文案）、`README.en.md`（同上）、`tests/routing_cases.json`（正向用例 + 至少一条 forbidden 覆盖）、校验器（TOKEN_BUDGETS、按需 DIRECT_WRITE_OWNERS 与专项 markers）。

删除一个技能要：合并或确认语义去向、清理上述全部锚点、重定向以它为 primary 的用例、移除校验器专项块、**手动删除各 harness 已安装副本**（安装器不会删除消失的技能）。`README.md` 必须与 `README.zh-CN.md` 逐字节一致。

变更后流程：跑校验器到绿 → `install_codex_library.py --agent <targets>` 刷新 → 核对技能数 → 提交。长清单细节读 `references/anchor-checklist.md`。

## 输出

```text
结论: <技能定位、边界与结构>
锚点: <已同步清单>
验证: <校验器输出与技能数>
下一步建议: <有自然闸门时的一个具体动作；否则声明继续已授权工作>
```
