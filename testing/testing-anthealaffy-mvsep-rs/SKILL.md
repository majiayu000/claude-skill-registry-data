---
name: testing
description: >
  测试与覆盖率：单元/集成/功能测试、TDD、回归测试、性质测试（Hypothesis/QuickCheck）、
  mock 外部依赖、行覆盖率与 Codecov。Use when the user asks to write tests, raise coverage,
  or choose a testing approach. 触发于「写测试/提覆盖率/选测试策略」。
---

# 测试

主线：测试是提高正确性信心的标准技术——写代码去调用你的代码，行为不符预期就报错。TDD 的红-绿-重构纪律另见 dsh 的 `tdd` skill；本 skill 只做 MIT 讲义的科学面（测试类型与工具）。

## 测试类型

- 按粒度：单元测试（单个函数）、集成测试（模块/服务之间的交互）、功能测试（端到端场景）。
- TDD 先写测试再写实现；发现 bug 时写**回归测试**——未来再坏立刻能抓住。
- 性质测试（property-based）：QuickCheck（Haskell）开创，Hypothesis（Python）等实现——声明性质，框架随机生成输入验证并给出具体反例。它不是数学证明：要人工限定输入范围（如字符串长度 0–20、整数 0–50）。
- 用哪种看项目，通常是若干种的组合。测试放哪随语言约定：Rust 单测常与函数同文件、集成测试分离；Python 有 doctest。
- 依赖数据库/Web API 等外部服务时，测试里 mock 它们：实现相同 API 的假实现注入测试——可控制返回错误、可离线跑。不想写 mock 的替代是 VCR 类工具（pytest-vcr）：录一次真实 API 通信，之后重放。

## 覆盖率

- 行覆盖率：测试跑过哪些行，按行显示、指导补测试（HTML 报告给人看，XML 更密、更适合喂 LLM）；Codecov 类服务提供 Web 界面跟踪项目历史；也是粗筛开源项目质量的指标。
- 覆盖率是质量指标之一，不是目标本身——100% 覆盖的测试可能毫无意义（有人见过前端仓库满覆盖但测试全废）；高质量的测试更重要。
- 让 AI 提覆盖率时，要给它「带覆盖率跑测试 + 逐行报告」的环境，它才知道聚焦在哪；它生成的测试越放任越水，要用「测试这个功能的行为」这类指令引导并审查（见 `agentic-coding`）。

## 练习

学习材料在 `exercises.md`。

> 改编自 MIT The Missing Semester 课程 Lecture 9: Code Quality（讲义 + 口播稿，CC BY-NC-SA 4.0）：https://creativecommons.org/licenses/by-nc-sa/4.0/ · 课程站点：https://missing.csail.mit.edu/ · 讲座视频：https://www.youtube.com/watch?v=XBiLUNx84CQ
