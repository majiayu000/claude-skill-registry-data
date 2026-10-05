---
name: skill-refactor
description: Audit and refactor existing Codex skills when the user asks to 整理、精简、去重、瘦身、重构、清理或审计 Skill。Find obsolete artifacts, duplicated ownership, overloaded entrypoints, trigger conflicts, broken routing, and deterministic logic maintained in multiple places. Do not use for ordinary skill creation or unrelated feature work.
---

# Skill Refactor

整理已有 Skill，使每条现行规则只有一个维护位置，入口只保留执行所需的最少决策。把 skill-creator 视为结构规范来源，不在这里复制通用的 Skill 创建教程。

## 先确定授权边界

- 用户说“看看”“检查”“审计”“先不改”时，只读核实并报告，不修改文件。
- 用户明确说“整理”“精简”“修改”“执行”时，只修改点名范围；先完成预检，再实施可追溯的改动。
- 删除对象、唯一负责人或外部调用方不明确时，先提交删除清单和迁移图，等待确认。
- 开始前查找并读取目标范围适用的 `AGENTS.md`；文件不存在时记录这一事实后继续。目标位于 Git 仓库时读取 `git status`，否则记录没有 Git 基线。保留用户已有的未提交改动，不清理无关内容。
- 不把审计发现自动当成删除许可。

## 必读事实

审计每个目标 Skill 时，读取：

1. 目标 SKILL.md。
2. SKILL.md 直接引用的 reference、脚本、配置和测试。
3. 调用该 Skill 或其脚本的当前入口。
4. 与判断相关的当前结果、台账或运行状态。
5. references/review-rubric.md。

记忆和历史提交只用于定位线索。文件存在不等于流程已采用；历史提交不等于当前规则。

## 运行机械审计

定位当前已加载的 `skill-refactor/SKILL.md`，使用它同目录下的审计脚本；不要假设本 Skill 安装在目标仓库内部。把待审计的 skills 根目录、单个 Skill 目录或 `SKILL.md` 作为参数：

    python3 "<skill-refactor 目录>/scripts/audit_skills.py" "<目标 skills 根目录>"

例如目标可能位于项目级 `.agents/skills`，也可能位于全局 `~/.codex/skills`。只审计单个 Skill 时直接传它的目录。

需要机器可读结果时增加：

    --format json

脚本只读扫描 frontmatter、描述预算、精确重复文件、退役占位、同步维护提示、触发词冲突、本地 Markdown 断链、疑似孤立 reference 和生成物。扫描结果都是候选证据，不是自动裁决。

## 建立唯一负责人图

对每条发现先回答“谁负责”，再决定放在哪里：

- 全仓不变量：AGENTS.md。
- 触发、路由、阶段顺序、停止条件：一个 SKILL.md。
- 仅在特定模式需要的领域细节：该负责人下的一份 reference。
- 确定性变换、阈值、schema 或可执行校验：一个脚本或配置，并由测试约束。
- 易变账号、数量、版本、批次和服务状态：实时事实源。
- 历史原因：git 历史。
- 已无现行用途且无调用者：彻底删除。

其他位置只保留到负责人的短路由，不复制规则正文。出现“保持一致”“同步修改”“同名文件也要改”时，默认视为多处维护信号。

## 分类并处理

把每项候选归入以下一个动作：

1. 删除：同时删除文件、引用、调用和退役说明，不留 .retired、.bak 或“已弃用”墓碑。
2. 路由：保留一句何时转交给哪个 Skill，不复制对方流程。
3. 下沉 reference：只用于条件性细节，且由 SKILL.md 直接链接。
4. 下沉脚本或配置：只用于需要确定性、一致性或重复执行的逻辑。
5. 改查实时事实源：移除会过期的静态状态。
6. 保留：能够改变当前决策，且确实属于本层唯一职责。

不要用固定行数衡量精简。目标是减少重复决策和默认加载量，同时让每条保留规则仍有明确用途。不要制造 reference 套 reference 的深链。

## 不要误删

- 业务数据中的 active、discarded、deprecated 等状态可能是现行领域语义，不等于废弃代码。
- 兼容层只有在当前调用方、测试或外部契约能证明需要时才保留；“可能有人用”不算证据。
- 单一负责人不等于把所有内容塞进一个大文件。互斥模式可拆成多份 reference，但公共规则仍只维护一次。
- 删除历史说明后，用正向现行措辞描述剩余流程；不要在入口里讲旧流程故事。

## 验证

修改后至少完成：

1. 重新运行机械审计，解释仍保留的例外。
2. 目标环境存在 `skill-creator/scripts/quick_validate.py` 时用它校验目标 Skill；不存在或缺依赖时，区分“校验器不可用”和“Skill 无效”，并继续完成其他可用验证。
3. 检查本地引用、脚本语法和受影响的定向测试。
4. 检查代表性触发词和排除场景，避免聚合 Skill 抢走专用 Skill。
5. 检查差异，只保留能追溯到本次请求的修改。

报告变更前后行数、description 字符数、删除文件、负责人迁移、验证结果和明确例外。不要把“更短”本身写成成功结论。

## 停止条件

遇到以下情况先停并报告：

- 当前事实源或直接引用无法读取。
- 两个 Skill 都像唯一负责人，且现有入口无法消歧。
- 待修改区域与用户未提交改动重叠，无法安全保留。
- 删除对象仍有无法解释的调用者、测试或兼容契约。
