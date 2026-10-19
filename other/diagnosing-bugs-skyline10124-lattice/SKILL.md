---
name: diagnosing-bugs
description: 先建立可复现反馈，再诊断失败、错误行为或性能退化。
---

先按当前宿主读取 [Pi 说明](../../README.pi.md)或 [Delta 说明](../../README.delta.md)，再读取仓库内的[源工作流](../../skill-sources/diagnosing-bugs/SKILL.md)。

使用目标 crate 的验证入口，保留复现、最小化、假设、插桩、修复与清理各阶段的完成条件。真实红灯与证据先于推测；源码、测试结果和规范冲突如实报告。

性能实验按具体任务授权和现行诊断要求执行，本地测量不等于批准新的 qualification campaign，不修改历史结果或降低门槛。

需要人类操作才能复现时，读取源 [scripts/hitl-loop.template.sh](../../skill-sources/diagnosing-bugs/scripts/hitl-loop.template.sh) 并将适用步骤交给用户；不启动无人值守、等待用户输入的阻塞命令。
