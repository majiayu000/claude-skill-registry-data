---
name: cc-ops-safety
description: Shell、服务、容器、数据库、部署或环境敏感操作的安全规范，适用于风险说明、回滚思路和影响面控制；不负责语言细节。
---

# CC Ops Safety

当任务涉及命令执行、系统配置、部署、服务重启、容器操作、数据库写入或环境敏感行为时，使用本技能。

不要用于：

- 普通语言风格规范
- 正式 review 输出格式
- 一般性编码实现细节

## 核心规则

- 优先选择影响面更小的步骤。
- 先做只读检查，再做写入动作。
- 对不可逆或高风险动作，先说明风险和回滚思路。
- 明确区分本地、测试、预发、生产环境。
- 能用更安全的读操作降低不确定性时，先读后改。

## 工作方式

1. 判断环境和 blast radius。
2. 区分检查类动作和修改类动作。
3. 对非低风险动作，先说明风险与回滚。
4. 尽量分步、可回退地执行。
5. 变更后做最小必要验证。

## 按需展开

- 风险评估：`references/risk-assessment.md`
- 回滚思路：`references/rollback-thinking.md`
- 环境边界：`references/environment-scope.md`
- 破坏性动作：`references/destructive-actions.md`
