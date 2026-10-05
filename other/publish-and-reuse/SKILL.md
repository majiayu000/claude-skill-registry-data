---
name: publish-and-reuse
description: Personal AI Infrastructure 多设备生命周期同步总入口：一句“同步一下我的 Personal AI”自动判断 PULL/MERGE/NO ACTION/REVIEW/BLOCKED（AUTO_SYNC），覆盖 personal-ai、personal-ai-private（curated + Dynamic Memory 合并）、项目仓库、runtime refresh 与新设备 Fresh Restore；同时保留 DSH 四层环境上传/更新/体检/复现作为子步骤。只自动处理确定安全的变更，冲突与 dirty 一律留给人工；commit/push 受 canonical ownership lease 与 receipt 约束。
version: 2.0.0
triggers:
  - "同步一下我的 Personal AI / 同步一下 / 更新一下这台电脑 / 让这台电脑跟另一台一致 / 把最新状态同步过来"
  - "把这台机器的变化同步出去 / 只上传"
  - "只检查同步状态 / 只拉远端 / 只上传 / 在新电脑恢复我的 Personal AI"
  - "一键上传环境 / 上传环境 / 备份环境 / 同步到 GitHub / 推送环境配置"
  - "一键更新环境 / 从 GitHub 同步 / 同步到 DSH / 刷新环境 / 拉取环境"
  - "一键检查环境 / 环境体检 / 检查四层一致性 / 对比环境差异"
  - "在新设备复现 / 安装我的环境"
  - "发布 Skill / 脚本 / 插件 / 整个仓库 / 跑发布门禁"
not_for:
  - "在非 personal-ai 仓库的其他业务工作区中执行环境同步、更新或上传（本 skill 仅在 personal-ai 仓库本体生效）"
  - "修改具体业务代码或单个 Skill 的内部逻辑实现（交给 minimal-implementation）"
  - "日常代码编写与单点 Bug 修复"
depends_on:
  - skill-repository-maintainer
  - dsh-config-sync
  - environment-bootstrap
---

# Personal AI 生命周期同步（publish-and-reuse）

## 定位

本 skill 是 **Personal AI Infrastructure 长期、多设备、增量生命周期同步的最高层入口**。
用户平时只需要说“同步一下我的 Personal AI”，系统自动判断本次应该
PULL / PUSH / MERGE / NO ACTION / REVIEW / BLOCKED——用户不负责判断方向。
Fresh Restore 只是 `local canonical missing` 时的特殊 SYNC。

旧的 DSH 四层能力（Skills / 插件 / MCP / DSH 配置的上传、更新、体检、新设备复现）保留，但作为整体同步中的子步骤。

复杂协议、SYNC_OWNERSHIP_MATRIX、方向规则、Memory 合并契约、RESTORE 全流程：
`references/personal-ai-lifecycle-sync.md`（先读它再执行非常规场景）。

## 不适用（负向边界）

- 在非 personal-ai 仓库的其他业务工作区执行环境同步/上传/覆盖。
- 修改具体业务代码或单个 Skill 的内部实现（交给 `minimal-implementation`）。
- 日常代码编写与单点 Bug 修复。
- 用本入口同步 secrets、sessions、broker sqlite、device-local 路径或派生索引——这些永不进入 git 生命周期同步。

## 模式路由

| 用户说 | 进入模式 |
|---|---|
| 同步一下 / 同步我的 Personal AI / 更新一下这台电脑 / 让两台电脑一致 | `SYNC`（AUTO_SYNC，自动判方向） |
| 把变化同步出去 / 只上传 | `PUSH`（显式上传，必须有 ownership receipt） |
| 只检查 | `CHECK`（只读） |
| 只拉远端 | `PULL`（禁止 push/merge） |
| 只上传 | `PUSH`（禁止 pull/merge） |
| 在新电脑恢复 | `RESTORE` |
| 上传环境 / 更新环境 / 环境体检 / 新设备复现（旧表达） | 继续工作，映射到 PUSH / PULL / CHECK / RESTORE 子流程 |

## 高层工作流

编排器（薄，只 inspect/classify/调用既有工具/排序/报告）：

```powershell
python scripts\personal_ai_sync.py check      # 只读分类，连 checkpoint 都只读更新
python scripts\personal_ai_sync.py sync       # AUTO_SYNC 默认日常入口
python scripts\personal_ai_sync.py sync --detail   # 下钻
python scripts\personal_ai_sync.py restore    # Fresh/缺失恢复
```

内部顺序（防数据丢失）：fetch all → classify all（git ancestry，禁止 mtime/last-write-wins）→ action plan → 只执行确定安全动作 → 受影响面判定 → 受影响 Harness `aic apply`（generated-only，snapshot+post-diff+rollback）→ 受影响 derived 增量 refresh → validate → 写 machine-local checkpoint（`~/.dsh/.personal-ai-sync/status.json`）→ 短输出。

确定安全的自动动作（其余一律 REVIEW）：锁内 clean FF pull、显式 push 模式下有 ownership receipt 且验证通过的 FF push、不同设备新增 record/revision 的 Memory 确定性合并（复用 MemoryProvider.import_bundle 契约）、派生索引 rebuild、runtime diff/refresh。`SYNC` 不隐式 commit/push。

## 安全规则（铁律）

1. **方向判定只用 git ancestry**，禁止 mtime / last-write-wins / timestamp 覆盖。
2. **LOCAL_DIRTY 一律 UNTOUCHED**：禁止自动 add/commit/stash/reset/checkout/overwrite。
3. **DIVERGED 默认 REVIEW**：禁止自动 merge/rebase/force push 基础设施 canonical；唯一例外是 memory-only 且路径不相交的确定性合并，且 curated state（identity/preferences/goals）双端修改永远 CONFLICT_REVIEW。
4. **secrets 绝不进 git sync**：只检测引用 AVAILABLE/MISSING/NOT_REQUIRED；optional 缺失不阻塞整体。
5. **device-local / derived 永不同步**：路径、GPU、端口、索引、projcache、node_modules——每设备 `aic discover` / 本地 rebuild。
6. **raw history 不走 git sync**：sessions/traces/broker sqlite 继续走 Durability。
7. **凭据绝对不出包**：`.credentials.yaml`、`sessions/`、`storages/` 永远排除。
8. **不破坏目标端无关文件**：所有 apply 仅增量覆盖，不清理未登记文件。
9. 已知外部 blocker（BACKUP_KEY_CUSTODY / NOVEL_REPO_DURABILITY）状态未变只报 `known external blocker, unchanged`，不重复建议解决。
10. public 项目 push 前必须 privacy scan，命中即 BLOCKED_PRIVACY（NOVEL_REPO_DURABILITY 继续保持）。
11. canonical 写操作必须先取得 machine-local mutation lease；dirty、foreign lock、unknown lock 或 scope 未验证时一律 REVIEW/DEFER。
12. commit 只能 stage 声明的 owned paths，并写出 machine-local ownership receipt；禁止 `git add -A`、隐式 push 和非 canonical restore 注册 Scheduler。

## 输出契约

默认短输出（用户说“展开”才下钻 git 日志/diff/governance 细节）：

```text
Personal AI Sync

personal-ai          IN_SYNC / PULLED / PUSHED
personal-ai-private    IN_SYNC / PULLED / PUSHED / MERGED
projects             <简要汇总>
memory               <新增/合并/冲突数量>
runtime              NO DRIFT / refreshed
secrets              READY / PARTIAL
external blockers    known external blocker, unchanged

Result: PASS / REVIEW / BLOCKED
```

冲突时先把确定安全的部分同步完，只把真正冲突留给人工（不问“要不要同步其他没冲突的”）。

## 旧能力：DSH 四层子流程（保留）

- **体检**：`python scripts\sync_skills.py --destination "$env:USERPROFILE\.dsh\skills" --plugins-destination "$env:USERPROFILE\.dsh\profiles\web\plugins" --dsh-config-dir dsh-config --mcp-cordis "$env:USERPROFILE\.dsh\profiles\web\cordis.patch.yml" --profile full --check`
- **上传（Push）**：仅显式 `push` 模式；每个 ahead commit 必须有 ownership receipt，再执行 `git diff --check` + `validate_repo --strict` + `quality_report --strict` + 仓库回归 + `publish_check.py` → `git push` → 四层体检确认。
- **更新（Pull）**：`git pull --ff-only` → 门禁 → 同体检命令 `--apply` → 逐层 `sync_dsh_config.py apply` → 重启 DSH 生效。
- **新设备复现（Install）**：RESTORE 流程（见 reference §14），幂等、可重复执行。

权威细节：`references/personal-ai-lifecycle-sync.md`、`docs/publishing.md`、`docs/sync-ongoing.md`。

## 验证

本 skill 变更后必须全绿：

```text
python scripts/validate_repo.py --strict
python skills/skill-quality-gate/scripts/quality_report.py --root . --strict
python -m unittest discover -s tests -v
python scripts/publish_check.py
```

同步执行后验收：`aic validate = VALID` + 已安装 Harness `aic diff = NO DRIFT` + personal_status 无新增异常。
