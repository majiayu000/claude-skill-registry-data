---
name: mirror-optimizer
description: 当用户明确要求优化镜像源、配置国内镜像、加速部署或切换依赖源时使用。分析项目技术栈并生成适配的镜像配置。⚠️ 不适用：用户只是询问镜像源概念、无需部署加速，或明确要求使用官方源。
metadata:
  short-description: 智能镜像源优化代理
  keywords: [mirror, registry, 镜像源, 加速部署, 国内镜像, mirror-optimizer]
  category: devops
  author: Bensz Conan
  platform: Claude Code | OpenAI Codex | ChatGPT
  iron-law: |
    NO DEPLOYMENT WITHOUT MIRROR CONFIGURATION FIRST
    (任何部署任务前必须先确认镜像源配置)
---

# Mirror Optimizer - 镜像源优化代理

## 铁律

```
NO DEPLOYMENT WITHOUT MIRROR CONFIGURATION FIRST
```

任何涉及依赖下载的部署任务，必须先确认并优化镜像源配置，否则在国内环境下部署将极慢或失败。

## 核心理念

**智能适配，透明可逆**。根据项目技术栈自动识别需要配置的镜像源类型，生成标准化的配置文件，同时保持官方源兼容性，支持一键切换。

## 何时使用

- 项目包含 `Dockerfile`、`docker-compose.yml` 或 `.dockerignore`
- 项目包含 `requirements.txt`、`pyproject.toml`、`Pipfile`、`setup.py`、`setup.cfg` 或 `poetry.lock`
- 项目包含 `package.json`、`yarn.lock`、`pnpm-lock.yaml` 或 `package-lock.json`
- 项目包含 `go.mod`、`go.sum`、`Gopkg.lock` 或 `Gopkg.toml`
- 项目包含 `pom.xml`、`build.gradle`、`build.gradle.kts` 或 `settings.gradle`
- 项目包含 `Gemfile`、`gems.rb` 或 `Cargo.toml`
- 用户明确要求"配置国内镜像"、"加速部署"、"切换镜像源"
- 部署过程中出现依赖下载超时或失败

## 输入

- **必需**：项目根目录路径
- **可选**：目标部署区域（默认：中国大陆）

## 输出

- 检测报告：识别出的包管理器类型和当前配置状态
- 配置文件：为每个包管理器生成的镜像源配置
- Dockerfile 优化建议（如适用）
- 使用说明：如何应用配置和验证效果
- 跳过清单：未生成的包管理器与原因（记录在报告中）

## 支持的镜像源类型

| 类型 | 检测文件 | 配置输出 | 国内镜像源 |
|------|----------|----------|-----------|
| **Docker** | `Dockerfile`, `docker-compose.yml`, `.dockerignore` | `Dockerfile.mirror` | 阿里云、腾讯云 |
| **Python/pip** | `requirements.txt`, `pyproject.toml` | `pip.conf` | 清华、阿里云、中科大 |
| **Node.js/npm** | `package.json`, `package-lock.json` | `.npmrc` | 淘宝、腾讯云 |
| **Node.js/yarn** | `yarn.lock` | `.yarnrc.yml` | 淘宝、腾讯云 |
| **Go Modules** | `go.mod`, `go.sum` | `go.env` | 阿里云、腾讯云 |
| **Java/Maven** | `pom.xml` | `settings.xml` | 阿里云、腾讯云 |
| **Java/Gradle** | `build.gradle*`, `settings.gradle*` | `init.gradle` | 阿里云、腾讯云 |
| **Ruby/Bundler** | `Gemfile`, `gems.rb` | `config` | 淘宝、腾讯云 |
| **Rust/Cargo** | `Cargo.toml` | `config.toml` | 清华、中科大 |

## 工作流

1. **项目扫描**
   - 使用硬编码脚本扫描项目根目录
   - 识别所有包管理器标记文件
   - 检查现有镜像源配置

2. **智能分析**
   - 根据检测文件确定需要配置的镜像源类型
   - 分析现有 Dockerfile 是否包含镜像源优化
   - 评估当前配置的潜在问题

3. **配置生成**
   - 为每个识别的包管理器生成标准化配置
   - 创建 `Dockerfile.mirror` 优化版本（如适用）
   - 生成 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/mirror-optimizer/output/` 目录存放所有配置文件

4. **文档输出**
   - 生成 `MIRROR_OPTIMIZATION_REPORT.md` 报告
   - 包含配置说明、使用方法、验证命令
   - 提供切换回官方源的指南

5. **验证检查**
   - 提供验证命令测试镜像源连通性
   - 确认配置文件格式正确
   - 建议测试下载速度

## 配置文件结构

> 输出目录以 `config.yaml:mirror_optimization.output_dir` 为准，以下以默认 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/mirror-optimizer/output/` 为例。

```
.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/mirror-optimizer/output/
├── docker/
│   ├── Dockerfile.mirror        # 优化的 Dockerfile
├── python/
│   └── pip.conf                 # pip 配置
├── nodejs/
│   ├── .npmrc                   # npm 配置
│   └── .yarnrc.yml              # yarn 配置
├── golang/
│   └── go.env                   # Go Modules 配置
├── java/
│   ├── maven/
│   │   └── settings.xml          # Maven 配置
│   └── gradle/
│       └── init.gradle           # Gradle 配置
└── MIRROR_OPTIMIZATION_REPORT.md
```

## 质量门槛

- [ ] **完整性**：检测到所有相关包管理器
- [ ] **正确性**：生成的配置文件格式正确
- [ ] **兼容性**：配置与官方源兼容，可一键切换
- [ ] **透明性**：配置有清晰注释说明用途
- [ ] **可验证性**：提供验证命令测试效果

## 国内镜像源推荐

| 类型 | 推荐源 | URL |
|------|--------|-----|
| **Docker** | 阿里云 | `https://registry.cn-hangzhou.aliyuncs.com` |
| **Docker** | 腾讯云 | `https://mirror.ccs.tencentyun.com` |
| **Python** | 清华 | `https://pypi.tuna.tsinghua.edu.cn/simple` |
| **Python** | 阿里云 | `https://mirrors.aliyun.com/pypi/simple/` |
| **Node.js** | 淘宝 | `https://registry.npmmirror.com` |
| **Go** | 阿里云 | `https://mirrors.aliyun.com/goproxy/` |
| **Go** | 腾讯云 | `https://mirrors.tencent.com/go/` |
| **Java/Maven** | 阿里云 | `https://maven.aliyun.com/repository/public` |
| **Ruby** | 淘宝 | `https://gems.ruby-china.com` |
| **Rust** | 清华 | `https://mirrors.tuna.tsinghua.edu.cn/git/crates.io-index.git` |

## 安全注意事项

- 只使用知名云服务商的镜像源
- 验证镜像源的 HTTPS 证书
- 定期检查镜像源可用性
- 生产环境建议配置镜像源备份

## 相关参考

- [镜像源配置最佳实践](references/mirror-configuration-best-practices.md)
- [国内镜像源完整列表](references/china-mirror-sources.md)
- [Dockerfile 镜像源优化模板](references/dockerfile-mirror-templates.md)

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
