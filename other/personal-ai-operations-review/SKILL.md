---
name: personal-ai-operations-review
description: 对已进入 OPERATIONS MODE 的 Personal AI / DSH 基础设施做只读运维复查：聚合 governance、durability、aic drift、proposal、memory/model/routing 与 personalization 行为监控（纠正率/重复纠正/选择泄漏），区分 NO ACTION、REVIEW、ACTION REQUIRED 与 EXTERNAL BLOCKER；用于日常健康检查、异常复盘、升级前检查，或用户询问“系统现在健康吗/需要管什么/AI 最近是不是又变难用了/个性化有没有退化”时。默认不修改 canonical，不为变绿而静默修复。
---

# Personal AI 运维复查

## 适用范围

用于已经完成建设、进入 `OPERATIONS MODE` 的 Personal AI Infrastructure。目标是回答“系统现在是否正常、哪些问题需要人处理、哪些只是已知外部阻塞”。

优先复用现有 Control Plane、Governance、Durability、Memory、Model/Trace、Harness Adapter 与 Personalization Calibration 的真实输出；不要重新实现底层检查。

## 不适用

- 不用于设计新的 Architecture Phase、重构 Control Plane、替换 MemoryProvider 或新增基础设施。
- 不用于直接批准 model admission、修改 routing/default model/preference、删除 provider/plugin/memory、清 Git 历史或处理其他 canonical mutation。
- 不把 `BLOCKED`/`DEGRADED` 自动视为系统失败；先判断它是否是治理系统正确暴露的真实约束。
- 用户明确要求实施某个 change 时，先转入既有 `Need → Impact → Proposal → Implementation → Verification → Regression` 流程，不在本 Skill 内静默执行。
- 不在普通任务中自动执行完整巡检。

## 核心契约：Evidence Freshness & Cause-aware Classification

### 1. Evidence Freshness 契约

每个运维域必须同时输出：
- `status`: `HEALTHY` / `DEGRADED` / `BLOCKED` / `UNKNOWN`
- `evidence_state`: `CURRENT` / `LAST_KNOWN` / `UNAVAILABLE`

语义：
- **CURRENT**：本轮成功执行真实检查。
- **LAST_KNOWN**：本轮实时检查不可用/失败，只能读取历史 verified evidence / baseline report。
- **UNAVAILABLE**：既无当前证据，也没有足够可信的历史证据。
- **严禁**：`LAST_KNOWN` 冒充 `CURRENT`；严禁在只有历史快照时宣称“与基线持平”。

### 2. 检查失败与沙箱限制处理

- 检查脚本遇到 not found / permission denied / sandbox denied / timeout / path inaccessible 时：
  - 属于 `OBSERVABILITY_EVIDENCE_LIMITATION`，不直接判为 `DEGRADED`。
  - 若存在历史 verified 证据：`status = <last known status>`, `evidence_state = LAST_KNOWN`。
  - 若无历史证据：`status = UNKNOWN`, `evidence_state = UNAVAILABLE`。
- 仅当真实规则/能力检查器本身执行并检出违规（如 capability drift > 0 或 static boundary violation）时，才标 `DEGRADED`。

### 3. Durability 契约（Backup Age 与 Repo Durability 分离）

- 明确区分 backup age 数据集（sessions, broker, configs）与 repos 数据集：
  - **BACKUP_RPO_AGE_BREACH**：仅指 sessions/broker/configs 等备份年龄超出 RPO 目标。
  - **KNOWN_PRIVACY_BLOCKER / REPO_BLOCKED_PRIVACY**：因包含未脱敏信息拦截推送（如 novel-main），不得被描述为“备份年龄超期”。
  - **REPO_UNPUSHED**：存在未推送提交。
  - **REMOTE_UNAVAILABLE**：远程仓库不可达。
- 当且仅当 sessions/broker/configs 等存在真实超期（`BACKUP_RPO_AGE_BREACH`）时，才触发 `ACTION REQUIRED`。

### 4. Overall Action Resolver

- **ACTION REQUIRED**：只有存在当前证据确认的**新真实运行故障**（actual Harness drift、actual backup age RPO breach、scope leakage、secret exposure、governance check failed、未预期 unpushed repo）。
- **REVIEW**：任一域证据不可用（`UNAVAILABLE` / `LAST_KNOWN`）、非关键指标恶化（over-personalization）、待裁决高危提案。
- **EXTERNAL BLOCKER**：仅存在已知外部 blocker（`BACKUP_KEY_CUSTODY`, `NOVEL_REPO_DURABILITY` 等），且无其他新异常。
- **NO ACTION**：全部健康且为当前证据，无 blocker。

## 工作流程

1. **定位真实入口**
   - 找到 `personal-ai` 仓库根目录和当前分支/commit。
   - 优先读取 `docs/personal-ai-operations.md`、当前 Architecture/operations handoff 与仓库已有脚本说明。
   - 命令或路径不存在时标 `UNKNOWN`，先搜索仓库实际入口；不要凭旧报告猜路径。

2. **读取 Human-facing status**
   - 运行入口：

     ```text
     python scripts/governance/personal_status.py
     ```

   - 记录每个域的 `status`、`evidence_state` 及 `cause/reason`。

3. **验证 Control Plane 与 Harness drift**
   - 运行已有 `aic validate`。
   - 对当前已登记 Harness 逐个执行 `aic diff <target>`；覆盖 dsh/codex/claude/gemini/switchboard。
   - 正常目标应为 `VALID / NO DRIFT`。发现 drift 时只报告 expected/actual/owner，不自动 apply。

4. **检查 Durability**
   - 运行 `python scripts/durability/rpo_check.py --json`。
   - 区分 backup-age 与 repo privacy blocker；获取 per-dataset cause。

5. **检查 Governance / Proposals**
   - 检查 `capability_gov.py` 与 `static_gov.py`。
   - 检查 inbox open proposals，统计数量与高危项。

6. **检查 Personalization（行为监控域）**
   - 运行 `python skills/personal-ai-operations-review/scripts/personalization_status.py --json`。
   - 缺实时数据时诚实输出 `LAST_KNOWN` 或 `UNAVAILABLE`，不伪造精度。

7. **输出 Human-facing 报告**

```text
Personal AI Status

Infrastructure     HEALTHY
  CURRENT — aic VALID, 5 targets NO DRIFT

Personalization    HEALTHY / UNKNOWN
  CURRENT / LAST_KNOWN — 证据说明

Durability         HEALTHY / DEGRADED
  CURRENT — novel-main remains known BLOCKED_PRIVACY; backup-age datasets healthy

Governance         HEALTHY / UNKNOWN
  CURRENT — capability_drift=0; static boundary clean

Proposals          HEALTHY
  CURRENT — 4 open, no new high severity

External Blockers  BLOCKED
  CURRENT — known, unchanged

Overall: NO ACTION / REVIEW / ACTION REQUIRED / EXTERNAL BLOCKER
```

## 安全边界

- 默认只读；不调用 `aic apply`、不写 canonical、不 push、不 admit model、不改 preference/memory、不删除 config。
- 不输出 secret、token、decrypt key 或完整凭据。
- 不通过自动修复把真实异常变成绿色。
- 不新增 daemon、数据库、Harness 或外部通知服务。
