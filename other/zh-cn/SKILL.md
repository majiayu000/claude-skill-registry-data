---
name: thorlabs-blender-optical-path-zh
description: 从测量需求、二维光路图和有来源记录的 CAD 设计新测量光路，或重建、审核、修订 Blender 光学平台。适用于高精度 optics-only 模型、Thorlabs 兼容光机件、光路拓扑、整机验证及具有明确物理证据范围的发表级渲染。
---

# Thorlabs Blender 光路

把测量需求或二维示意图转换成可解释、可独立审计的 Blender 光学平台。

英文版是技术权威源。涉及几何时读取 `../../skills/thorlabs-blender-optical-path/references/physical-gates.md`；验收前读取 `evidence-contract.md`；修订旧场景时读取 `history-derived-rules.md`；完整案例见 `project-case-study.md`；整机运行前读取 `end-to-end-workflow.md`；多轮规模/发布资格测试读取 `multi-run-qualification.md`。

## 权威与版本

1. 系统约束优先；随后是用户最新文字或标注截图、项目 active rules、本 skill，最后才是旧产物和旧 PASS。
2. 冻结已提交或验收的包；在活动 revision 中集中处理相关纠正，不覆盖冻结证据，不为每张预览发布新版本。
3. 整机保持一个 run ID、writer、revision、生成器/Blend 谱系和 workflow 账本；副 agent 默认只读，禁止拼接独立写入模块冒充整机完成。
4. 把每个截图问题转换为对象族、世界坐标几何、数值门槛和必需证据。
5. 无法证明时使用 `UNVERIFIED` 或 `BLOCKED`。文件存在、CAD 导入、进程成功、AABB 接触和自报文本都不是证据。

## 核心流程

先区分新测量设计、原图重建、既有场景修正与纯渲染。用户要求“参考旧示例的精度生成另一种光路”时，旧示例只作画质比较，需从空场景建立新拓扑、生成器与资产映射。optics-only 包含光学探测器和机械支撑，排除电路及电气/数据信号可视化。详细要求见[新设计与渲染](../../skills/thorlabs-blender-optical-path/references/fresh-design-and-rendering.md)。

1. 用 `scripts/workflow_ledger.py` 初始化一个整机 run spec、状态账本和 append-only 事件哈希链。
2. 建立 `schematic node -> 实验角色 -> 真实资产 -> 光/光纤/电端口 -> 支撑路径`。
3. 列出全部分支、器件、光束高度、孔径和探测终点。
4. 只从 manifest 锁定的厂家 URL 把官方 CAD 下载到私有缓存；原子落盘前复核 bytes 与 SHA-256，并记录型号、来源、尺度、bbox、局部光轴、法向、孔径、provenance 和再分发边界。替代件必须明示；没有明确授权时禁止公开厂家几何。
5. 把 source lock 与其全部哈希文件当作一个原子输入包；几何前运行 producer-to-consumer artifact preflight，确认 source bytes、CAD canonical/型号别名 key、官方图纸和 runtime 均位于下一脚本实际消费的路径。查找前先按强类型 exact-set 合同验证结构化 authority 输入；missing、duplicate、extra、legacy、malformed 或身份不一致必须生成可持久化的结构化 `BLOCKED`，不得异常退出或静默折叠重复项。
6. 发布脚本必须重算同一语义锁且 difference paths 为零。多状态系统的每条 edge 必须有精确 `active_states` 或哈希化确定型展开，每个 state 都要有明确 ray template。
7. 先解光心、镜面、分束面、反射和分支连续性。设计坐标与保存后重开的真实 mesh/port 测量必须分开；常量零误差和命中同名器件族不足以证明孔径及首碰撞。
8. 再从真实桌孔向上按 post-first 构建紧固件、夹具、holder、post、mount 和器件。
9. 修共享根因，在同一运行内先验一个代表件再传播；保存后重开并逐件复核。
10. 先做明亮的机械/轴向/剖切审计图，再做 beauty render。
11. README/GATE 计数必须来自机器证据；随后在同一账本完成重开、整机 ray/BVH、OpenCV、GLB 回导、二进制/PNG 元数据脱敏、manifest、hash 和全 active-rule 合规矩阵。

光束、柔性光纤和电缆必须是不同对象族，仅生成请求范围内的类别。孔径必须真实开放。删除重复 surrogate 和无角色 placeholder。低成本诊断预览可用于检查器件精度、可见光路与构图，但必须注明尚未闭合的物理证据；最终发表级渲染在物理门通过后完成。保留材质槽与多边形索引语义，逐器件近景和逐分支检查；全图清晰度、边缘密度、颜色像素数不能单独证明建模精度或光束连续。实际 2K 图不能满足 4K 交付要求。

达到用户要求与硬门槛后冻结一次交付并发布；只在输入、依赖、runtime 变化或检查失败时复验受影响部分。Skill 文档更新可以记录未通过模型的经验，不能转移模型发布信用。案例数值阈值不得直接成为通用标准。

状态：`PASS` 表示所有适用规则有新鲜证据；`PARTIAL/SCOPED` 只代表局部，必须列出 blocker 且 final/release 保持 false；`UNVERIFIED` 表示证据不足；`BLOCKED` 表示已知失败。禁止把脱敏通过、局部通过或 CAD 导入成功写成整机最终通过。
