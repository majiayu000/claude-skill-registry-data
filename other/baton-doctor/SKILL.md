---
name: baton-doctor
description: Baton 项目健康诊断与能力自检（版本/漂移/骨架/发布面/凭据清单）。只读，不修改任何文件。触发：用户要求体检、诊断、看 Baton 状态、为什么口令没反应时使用。
---

# baton-doctor（只读健康诊断）

## 检查清单

1. **版本事实分层**：先判断当前目录是否为 Baton 框架源码仓库（`package.json.name=@kakadeka/baton`）。若是，源码版本只取本地 `package.json.version` + 本地 HEAD；框架仓库的 `skills/` 是 canonical 源目录，不把其中的 `baton-lean-review` / `baton-debt` 当业务项目残留。npm latest 与公开库 SHA/tag 只列为发布面证据，不得与私有源码 HEAD 混称新旧。普通业务项目看已跟踪的 `.baton/config.json`、`.baton/manifest.json`、项目 Skill 与 `docs/ai_memory/`；不再把缺失 `.baton/version.json` 当故障。
2. **Skill 漂移**：canonical `skills/baton/SKILL.md` 与三端镜像逐字节一致？项目内可用 `node scripts/check-drift.mjs`（有脚本时）。默认安装只有 `baton` + `baton-doctor`；`baton-lean-review` / `baton-debt` 仅框架仓保留。
3. **项目 manifest**（仅普通业务项目）：`.baton/manifest.json` 必须存在、是可解析 JSON，且 `managed` 至少包含当前默认九项：`.cursor/rules/baton.mdc`、`.baton/runtime/baton-closeout.mjs`、`.baton/runtime/baton-public-update.mjs`，以及 `.agents/.claude/.cursor/skills/{baton,baton-doctor}/SKILL.md` 六个项目镜像。逐项读取并用 SHA256 与 manifest 比对；缺失、不可解析、缺项、文件缺失或 hash 不一致都只报告 FAIL，不删除、不修复。项目中的 `baton-lean-review` / `baton-debt` 若存在且未被 manifest 管理，报告为旧默认残留；框架源码的 canonical `skills/` 目录不适用此条。
4. **骨架完整**：`docs/ai_memory/` 关键文件存在且含【归档分卷索引】+【修订记录】；`.baton/config.json` 可解析；`.cursor/rules/baton.mdc` 与三端 Skill 镜像存在且受 manifest 管理。核对主 Skill 含自动语义分卷与即时自动记忆规则。
5. **Git 状态**：分支/HEAD/工作区干净/远端同步（`git fetch` 只读检查 ahead/behind；**不做任何写入**）。
6. **单写入者锁**：`git show-ref refs/baton/ownership-lock` 是否存在、state.ownership 状态。
7. **发布面**（框架仓库场景）：公开库 CI 最近 run、npm latest 与 tag 对齐。
8. **凭据红线自检**：最近 diff 与待提交文件扫描——报告命中清单，**绝不显示命中正文**。
9. **Codex Windows ACL 兼容**：仅当 `.agents` Owner 命中 `CodexSandboxOffline`/`CodexSandbox` 或关键 ACE 异常时报告 FAIL。Doctor 不改 Owner/ACE。

## 输出格式

```text
## Baton doctor 报告 <时间>
- 版本：源码 vX @ <本地HEAD> / npm vZ / 公开 tag+SHA（分别报告，禁止混称）
- Skill：四份一致 / 漂移点名；默认安装=baton+doctor
- 骨架：完整 / 缺失清单
- Git：分支 / HEAD / 干净 / ahead/behind
- 锁：holding(<owner 前 8 位>) / released / 无 ref
- 发布面：CI 最近 <成功/失败> / tag 对齐
- 凭据：命中 N 处（只列文件名）/ 零命中
- Codex Windows ACL：正常 / FAIL
- 建议：<唯一下一步>
```

## 边界

- 只读：不修改、不 commit、不 push、不抢锁。
- 诊断结论标注证据来源（命令 → 结果）；无法验证的写「未验证」，不得 PASS。
- 修复必须回到 Baton 正常口令（更新 Baton / init）；doctor 不越权执行。
