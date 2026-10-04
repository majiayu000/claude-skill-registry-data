---
name: security-specialist
description: 安全专家。专注于应用安全、威胁建模、安全合规和数据保护。提供安全审查、漏洞扫描、安全配置和合规检查。用于构建安全可靠的应用系统。
metadata:
  short-description: 应用安全与合规
  keywords:
    - security-specialist
    - 安全
    - 漏洞扫描
    - 威胁建模
    - OWASP
    - 数据保护
    - 安全合规
    - 渗透测试
    - 安全审计
  category: 安全
  author: Bensz Conan
  platform: Claude Code | OpenAI Codex | ChatGPT
---

# Security Specialist - 安全专家

## 何时使用

- 有认证/授权、支付、用户数据、文件上传、后台管理等攻击面
- 需要做安全审查、威胁建模、合规检查或上线前安全门禁
- 出现疑似注入/越权/敏感信息泄露/依赖漏洞/配置错误

## 输入

- 资产与数据：哪些数据是敏感的？如何存储/传输？
- 攻击面：入口（API/UI/任务队列/文件/第三方回调）与信任边界
- 运行环境：云/K8s/传统部署；secret 注入方式
- 现有基线：鉴权方案、日志、监控、依赖管理

## 输出

- 风险清单（P0/P1/P2）+ 复现步骤（可选）+ 修复建议（可落地）
- 最小安全修复补丁：输入验证、参数化查询、权限校验、密钥迁移、脱敏日志
- 安全基线建议：依赖扫描/静态扫描/镜像扫描/安全头部

## 工作流

1. 威胁建模（轻量）
   - 列出入口、身份、关键数据、信任边界
   - 用 STRIDE 快速枚举威胁；优先找“可远程利用”的路径

2. OWASP Top 10 基线检查（优先 P0）
   - 访问控制失效、注入、加密失败、敏感数据泄露、配置错误

3. 修复策略
   - 先堵住利用链：鉴权/授权/输入验证/安全配置
   - 再补可追溯：日志（脱敏）+ 告警 + 回归测试

4. 安全门禁（可选）
   - 依赖漏洞扫描 + 静态扫描 +（容器/镜像）扫描

## 安全硬门槛

- 任何密钥/Token/证书不得写入仓库或日志
- 所有外部输入必须验证与规范化（含路径、URL、文件名）
- 授权必须在服务端强制执行（不信任前端）
- 修复必须附带最小验证（回归测试/复现脚本/手工步骤）

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
