---
name: flight-forge-local-skill
description: 从用户指定的本机 Codex Skill 显式派生一个项目级 Codex Flight Control Private Skill，同时不修改、移动、禁用或删除原 Skill。仅当用户直接调用 $flight-forge-local-skill 时使用；禁止隐式调用，也禁止在普通项目扫描中自动熔炼。
---

# 从本机 Skill 熔炼 Private Skill

这是显式创建命令。`UserPromptSubmit` Hook 必须注入 source kind 为 `LOCAL_SKILL` 的
一次性 `forge_authorization_token`。没有该授权时，在解析或读取路径前停止。

1. 调用 `flight_status`；必须满足 `private_skills: true`、持久状态健康并且 Lead
   session 已 attested。
2. 调用 `flight_surface_status`；仅在本轮 `LOCAL_SKILL` authorization 有效时，使用
   exact Lead credential 调用 `flight_surface_select` 选择 `FORGE`。禁止选择
   `FULL_COMPAT`，也禁止在选择失败后解析来源路径。
3. 只能使用用户明确选定的绝对 Skill 目录。禁止扫描用户 Skill 根目录、自动选择相似
   Skill，也禁止把普通项目工作解释为读取授权。
4. 使用注入 token，只调用一次 `flight_forge_prepare`，并固定 source kind 为
   `LOCAL_SKILL`。服务端执行只读、拒绝 symlink 的读取前后 identity 与 digest 快照。
   禁止 edit、format、move、chmod、disable、uninstall 或 delete 原 Skill。
5. 只从返回的 Source Capsule 提取范围狭窄的战术派生物。禁止复制原 Skill 的环境级
   自动激活行为；Private Skill 只能在困难节点由路由器注入。
6. 提交一个完整候选：trust 固定为 `USER_LOCAL`，license 必须诚实，并包含适用条件、
   前置条件、不变量、禁止动作、playbook、确定性验证、停止条件、反例、fixtures、
   holdout tags 和已验证关系。
7. 按 lifecycle 顺序审查。如果原路径仍位于已启用 Skill 根目录，必须保留
   `COEXISTENCE_BLOCKED` 并停在 `SHADOW`；禁止声称私有派生物已经替换或禁用原 Skill。
8. 报告读取前后 source digest、不可变 version ID/digest、coexistence 状态、
   lifecycle 和 evaluation。禁止把派生物安装为全局 Skill。

来源在读取期间变化、symlink、特殊文件、资源超限、权限拒绝或 coexistence conflict
都是失败关闭证据。禁止通过复制或修改来源重试。
