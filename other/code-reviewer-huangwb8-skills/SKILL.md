---
name: code-reviewer
description: 用于审查已完成的工作、重大功能或合并前的变更，核对需求并按严重程度识别风险。未经审查不得合并。
metadata:
  short-description: 代码审查与质量保证
  keywords:
    - code-reviewer
    - 代码审查
    - Code Review
    - 代码质量
    - 安全检查
    - 性能优化
    - 最佳实践
    - code review
    - quality check
  category: 代码质量
  author: Bensz Conan
  platform: Claude Code | OpenAI Codex | ChatGPT
  iron-law: |
    NO MERGE WITHOUT CODE REVIEW FIRST
---

# Code Reviewer - 代码审查专家

## 何时使用

- 重大功能完成后、合并前、发布前
- 大重构/跨模块变更
- 引入新依赖、新权限、新数据流

## 审查输入

- 需求/计划：用户描述、PR 描述、任务计划/设计文档（如 `PLAN.md`、`docs/plans/*.md` 或其它项目约定文件名）
- 代码改动：diff、关键文件、测试结果
- 风险偏好：可接受的破坏性/性能回退范围

## 输出格式（必须结构化）

对每个问题输出：
- 严重程度：Critical（严重）/ Important（重要）/ Minor（次要）
- What：问题是什么（具体到文件/函数/行为）
- Why：为什么是问题（风险与影响）
- Fix：如何修（最小变更优先）
- Verify：如何验证（测试/复现步骤）

## 审查顺序（先 P0 再 P2）

1. Critical（严重，P0）
   - 鉴权/授权缺陷、注入、路径遍历、敏感信息泄露
   - 数据一致性/事务边界错误、不可恢复的数据破坏

2. Important（重要，P1）
   - 明显性能风险（N+1、O(n^2) 热路径、内存爆）
   - 测试覆盖不足（关键路径无回归验证）

3. Minor（次要，P2）
   - 可维护性：命名、重复、复杂度、模块边界
   - 文档/注释/类型标注缺失

## 快速检查清单

- [ ] 输入验证与输出编码是否到位？
- [ ] 权限校验是否在服务端强制执行？
- [ ] 是否引入了新的敏感数据写入/日志输出？
- [ ] 是否有回归测试或至少可复现的验证步骤？
- [ ] 改动是否严格服务于用户目标，没有无关格式化、顺手重构或过度抽象？
- [ ] 是否能对应到明确的验收标准；缺少标准时是否已标为阻塞风险？
- [ ] 是否存在明显的性能/资源泄露风险？

## 约束

<!-- BEGIN COMMON CONSTRAINTS -->
<!-- Source-Hash: sha256:15120201e9e0c7569517261d57ecefb63ac279c26ed13876f8e95b6dc35854d3 -->
<!-- Template-ID: skill-common-constraints; Template-Version: 1; Sync-Policy: exact-block -->

### 公共硬约束

本块由 `docs/templates/skill-common-constraints.md` 统一维护；每个 `SKILL.md` 的 `## 约束` 必须逐字同步本块，不得在副本中改写公共规则。

- 任务需要落盘时，使用唯一的 `./.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/` 根目录；共享材料放入 `shared/`，Skill 专属材料放入该 Skill 的 `input/`、`output/`、`log/`。
- 正式交付物、源代码和正式计划按项目约定保存，不写入任务工作区；未经授权不覆盖、删除、迁移或远程写入。
- 项目维护变更检查 BAC 可用性并记录需求、AI 产出、工具结果、文件改动和验证摘要；BAC 只做过程审计，不替代署名、责任或合规判断。
- 不记录 API Key、访问令牌、密码、Cookie、环境/凭据文件、私有 Prompt、身份信息、本地用户名、主机名或不必要的大体积原始数据。
- 文件路径必须规范化并限制在授权项目范围内；外部 URL、子进程和网络访问遵循最小权限，防止路径遍历、SSRF 和命令注入。
- Skill 版本唯一记录在自身 `config.yaml:skill_info.version`；公开 API、协议、目录或配置变更同步文档与 `CHANGELOG.md`。
- `bensz-collect-bugs` 是一个 Agent Skill；仅将 Bensz Agent Skill 或 Bensz 基础设施本身的设计缺陷交给它。先脱敏写入 `~/.bensz-skills/bugs/`，当前任务不中断，只有用户明确要求才公开上报，禁止直接修改用户已安装的 Skill 源码。

<!-- End of canonical common constraints. -->
<!-- END COMMON CONSTRAINTS -->
