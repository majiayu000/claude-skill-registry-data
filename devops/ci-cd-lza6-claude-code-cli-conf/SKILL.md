---
name: "CI-CD"
description: "CI/CD 自动化 - 跨 Web、移动和后端应用的自动化构建、测试和部署。"
---

## 适用场景

触发条件：自动化部署、持续集成、管道设置、GitHub Actions、GitLab CI、构建失败、自动部署、CI 配置、发布自动化。

## 平台选择

| 技术栈 | 推荐平台 | 原因 |
|-------|-------------|-----|
| Web（Next.js, Nuxt, 静态） | Vercel, Netlify | 零配置、自动部署、预览 URL |
| 移动（iOS/Android/Flutter） | Codemagic, Bitrise + Fastlane | 预配置签名、应用商店上传 |
| 后端/Docker | GitHub Actions, GitLab CI | 完全控制、可选自托管运行器 |
| 单仓库 | Nx/Turborepo + GHA | 受影响检测、构建缓存 |

**决策树：** 如果平台自动处理部署（Vercel, Netlify）→ 跳过自定义 CI。仅在需要测试、自定义构建或部署到自己的基础设施时才添加 GitHub Actions。

## 快速开始模板

关于可复制粘贴的工作流，请参见 `templates.md`。

## 常见管道陷阱

| 错误 | 影响 | 修复方法 |
|---------|--------|-----|
| 使用 `latest` 镜像标签 | 构建随机失败 | 固定版本：`node:20.11.0` |
| 不缓存依赖 | 每次构建增加 5-10 分钟 | 缓存 `node_modules`、`.next/cache` |
| 工作流文件中包含密钥 | 在日志/PR 中泄露 | 使用平台密钥管理，OIDC 用于云 |
| 缺少 `timeout-minutes` | 卡住的任务消耗预算 | 始终设置：`timeout-minutes: 15` |
| 无 `concurrency` 控制 | 快速推送时重复运行 | 按分支/PR 分组 |
| 每次推送都构建 | 浪费资源 | 仅在推送到 main 时构建，PR 时测试 |

## 移动端特定：代码签名

这是最痛苦的问题。iOS 需要证书 + 配置描述文件。Android 需要密钥库。

**解决方法：** 使用 **Fastlane Match** — 将证书/描述文件存储在 git 仓库中，在团队和 CI 之间同步。

```bash
# 一次性设置
fastlane match init
fastlane match appstore

# 在 CI 中使用
fastlane match appstore --readonly
```

关于详细的移动 CI/CD 模式（iOS、Android、Flutter），请参见 `mobile.md`。

## Web 特定：构建缓存

没有缓存时 Next.js/Nuxt 构建很慢。`No Cache Detected` 警告 = 完整重建。

```yaml
# GitHub Actions：持久化 Next.js 缓存
- uses: actions/cache@v4
  with:
    path: .next/cache
    key: nextjs-${{ hashFiles('**/package-lock.json') }}
```

关于框架特定的配置，请参见 `web.md`。

## 调试失败的构建

| 错误模式 | 可能原因 | 检查项 |
|---------------|--------------|-------|
| 本地正常，CI 失败 | 环境差异 | Node 版本、环境变量、操作系统 |
| 间歇性失败 | 不稳定测试、资源限制 | 重试逻辑、增加超时 |
| `ENOENT` / 找不到文件 | 构建顺序、缺少构件 | 检查 `needs:` 依赖 |
| 退出代码 137 | 内存不足 | 使用更大的运行器或优化代码 |
| 证书/签名错误 | 过期或不匹配的凭据 | 使用 Match/Fastlane 重新生成 |

## 本技能不涵盖的内容

- 容器编排（Kubernetes）→ 参见 `k8s` 技能
- 服务器配置 → 参见 `server` 技能
- 监控和可观察性 → 参见 `monitoring` 技能
