---
name: ci-cd
description: >
  提交与发布自动化：pre-commit 钩子、GitHub Actions 持续集成（push/PR/定时、测试矩阵、
  只检查模式、状态徽章）、持续部署、just/npm scripts 命令运行器。Use when the user asks to
  set up pre-commit hooks, CI/CD workflows, or project command shortcuts.
  触发于「配 pre-commit/CI/CD/工作流/just」。
---

# CI/CD 与命令运行器

主线：质量工具要自动跑才会被跑。pre-commit 管提交前，CI 管推送后，CD 用同一套设施部署；命令运行器把长命令缩成 `just lint`。CI 测试新版本的逻辑与 `versioning-reproducibility` 的升级策略衔接。

## Pre-commit 钩子

- pre-commit 框架让 Git pre-commit 钩子好用：钩子定义在 `.pre-commit-config.yaml`（如提交前跑 `hatch fmt --check`），每个开发者只需 `pre-commit install` 一次；失败就拦下提交直到修复，确有需要可用 flag 跳过。

## 持续集成

- GitHub Actions 在 push、PR、定时三种时机触发脚本：跑格式化、lint、测试；编译型语言验证能编译，静态类型语言验证类型检查通过。
- 三类价值：每次 push 抓引入主分支的错误；PR 上抓贡献者的问题（他们往往不跑格式化/类型检查，CI 替他们跑，结果附在 PR 上一眼可见）；定时跑抓外部依赖的问题（有人发了声称 semver 兼容、实际破坏行为的版本）。
- 工作流组成：YAML 声明触发事件与 jobs（典型拆分 test/typecheck/format 三个 job），actions 可组合（checkout、setup-python 等），任一命令返回非零退出码即 CI 失败；CI 里还可跑覆盖率并上传 Codecov 跟踪历史。
- 没人背 GitHub Actions 语法：用的时候查文档、抄相似仓库的配置，或让 coding agent 写（见 `agentic-coding`）。
- 矩阵：不同操作系统 × 语言版本组合跑测试；耗时长的任务适合放 CI（在开发者机器之外独立跑）。
- 惯例：CI 只检查、不改代码——格式不符就报错，而不是直接格式化。
- 徽章：README 里放 CI 状态/覆盖率徽章。链接检查器（如 proof-html Action）也能进 CI——常因第三方网站故障而失败，但抓过不少失效链接。
- 学习途径：去 GitHub 找高质量开源项目（语言/领域/规模越接近越好），研究它们的 pyproject.toml、.github/workflows/、DEVELOPMENT.md。

## 持续部署

- CD 用 CI 设施真正部署变更：本课程网站就是每次 push 后自动构建并部署到 GitHub Pages；也可以在 CI 里为多平台编译二进制并自动发布，或构建 Docker 镜像等制品。

## 命令运行器

- just：项目上下文里 `just lint` / `just format` / `just typecheck`，不必记 `uv run ruff check --fix` 这类长命令。
- 语言内置的就不必再引 just：npm 的 package.json scripts、Hatch 的 tool.hatch.envs.*.scripts（`hatch fmt` 这类内置命令底层就是 Ruff 的 formatter/linter）。

## 练习

学习材料在 `exercises.md`。

> 改编自 MIT The Missing Semester 课程 Lecture 9: Code Quality（讲义 + 口播稿，CC BY-NC-SA 4.0）：https://creativecommons.org/licenses/by-nc-sa/4.0/ · 课程站点：https://missing.csail.mit.edu/ · 讲座视频：https://www.youtube.com/watch?v=XBiLUNx84CQ
