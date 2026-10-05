---
name: quality-verify
description: 面向完成宣称前的验证门禁 skill。先拿到 fresh verification evidence，再说通过、完成或 ready；没有新鲜证据就是 not-ready。
---

# Quality Verify

这个 skill 解决的不是“顺手跑一下检查”，而是完成宣称前的验证门禁。先有证据，再有结论。

## 何时使用

- 你准备说“完成了”“修好了”“通过了”
- 你准备提交 commit、PR 或进入下一阶段
- 你已经做完一轮改动，想判断是否 `ready`
- 用户明确触发 `/verify`

不适用：

- 还没进入任何实现或修复阶段
- 只是做研究，不涉及代码状态判断

## 产物

每次使用本 skill，默认产出以下最小集合：

1. 验证证据
   - 本轮实际执行的命令
   - exit code 或结果摘要
   - 失败项、跳过项、风险项
2. 质量结论
   - `ready`
   - `not-ready`
3. 质量记录
   - 若当前任务已有自己的记录文件，回写 Verify 阶段摘要
   - 若没有既定记录位置，默认写入 `.quality/quality-check.md`

## 工作流

1. 识别
   - 先明确：哪条命令能证明当前宣称
2. 执行
   - 运行完整检查，而不是局部替代
3. 读取
   - 看完整输出、exit code、失败数量
4. 核对
   - 判断输出是否真的支持当前宣称
5. 宣称
   - 只有在证据成立后，才能说 `ready`

## 门禁规则

- 铁律：没有 fresh verification evidence，就不要做完成宣称
- 没有 fresh evidence，结论必须是 `not-ready`
- partial verification 不是完成证据
- 旧日志、旧截图、旧印象都不能代替本轮 fresh evidence
- 可以写入当前任务记录，但验证结论本身不依赖任何特定任务框架
- 没有任务容器时，也应把验证结果落在 `.quality/quality-check.md`，而不是只写在回复里

## 最小验证范围

- build 或等效编译检查
- tests
- diff 检查
- 如项目存在 types、lint、静态分析，也应纳入

## 红旗

- “应该可以”
- “看起来没问题”
- “我挺有信心”
- “上次跑过了”
- “只要这一条过了，其他应该也没问题”

这些都不是证据，只是主观判断。
