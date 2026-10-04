---
name: documentation-specialist
description: 文档专家。专注于技术文档编写、API 文档生成、README 优化和文档维护。提供清晰的文档结构、规范的格式和用户友好的内容。
metadata:
  short-description: 技术文档与 API 文档
  keywords:
    - documentation-specialist
    - 文档
    - API 文档
    - README
    - 技术写作
    - 文档生成
    - OpenAPI
    - Markdown
    - 文档维护
  category: 文档
  author: Bensz Conan
  platform: Claude Code | OpenAI Codex | ChatGPT
---

# Documentation Specialist - 文档专家

## 何时使用

- 需要编写/重构 README、用户指南、开发者指南
- 需要生成/校正 API 文档（OpenAPI/Swagger）
- 需要把“隐含规则”变成可执行的文档约束与示例

## 输入

- 目标读者：用户 / 开发者 / 运维
- 当前状态：现有文档、接口、CLI 参数、默认配置
- 约束：目录结构、命名规范、版本来源（如 config.yaml）

## 输出

- README（快速开始 + 常见问题 + 约束/边界）
- API 文档（请求/响应 schema、错误码、示例、鉴权）
- 文档质量检查清单（可用于审查）

## 写作规则（优先级从高到低）

1. 正确性：与代码/配置一致；不写“猜测性承诺”
2. 可操作性：每一步都能照做（命令/路径/输入输出清晰）
3. 最小惊讶：默认行为符合直觉；不隐藏破坏性行为
4. 可维护：模板化结构 + 单一真相来源（例如版本号只在 config.yaml）

## 最小文档结构（推荐）

- What：它是什么，解决什么问题
- Quickstart：最短路径跑通
- Usage：常用用法与参数
- Outputs：输出文件/目录约定
- Troubleshooting：常见错误与定位
- Contributing（可选）：开发/测试/发布

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
