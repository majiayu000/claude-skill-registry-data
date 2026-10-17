---
name: ask-advisor
description: 显式把当前决策点交给强模型顾问（strong-model-consultant），获取决策建议。
disable-model-invocation: true
---

把当前决策点交给强模型顾问：用 `Agent(subagent_type="strong-model-consultant")` 调度顾问，把决策点、约束和相关上下文传入 prompt。拿到建议后继续当前工作。
