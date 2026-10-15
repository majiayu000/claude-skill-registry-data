---
name: win-04-foundation
description: Windows App Workflow 阶段 4 —— 工程地基搭建。适用场景：设计已定，需要建立 Git 仓库与提交规范、CI 流水线（构建/测试/产物）、代码签名基础设施，并完成一次"会走路的骨架"发布。提炼自 DevOps Automator、Git Workflow Master、Studio Operations 与 Desktop App Engineer 的"签名先于功能"规则。
---

# 阶段 4：工程地基（骨架先立起来）

> 目标：让"构建 → 测试 → 打包 → 签名 → 产物发布"这条链子在写第一个功能之前就全绿。**签名基础设施是发布阻塞项，第一天建，不是上线前补。**

## 1. 仓库与 Git 规范（来自 Git Workflow Master）

- 初始化仓库 + `.gitignore`（Node/Rust/.NET 按栈选模板；产物目录、证书文件永不入库）
- **原子提交**：每个提交只做一件事，可独立回滚
- **约定式提交**：`feat:` `fix:` `chore:` `docs:` `refactor:` `test:`
- 分支命名：`feat/user-auth`、`fix/crash-on-startup`、`chore/deps-update`
- 合并前 rebase 到最新目标分支；共享分支禁止强推（必要时 `--force-with-lease`）
- 版本策略：语义化版本 `MAJOR.MINOR.PATCH`，从 `0.1.0` 开始，打 tag 触发发布

## 2. 项目脚手架（按阶段 2 选型）

- Electron：electron-vite / electron-forge 模板；TypeScript；主进程/预加载/渲染三分离
- Tauri：`create-tauri-app`；Rust 侧 + 前端框架；capabilities 目录建好
- 原生：.NET 8 + WPF/WinUI3 或 Qt 模板
- 统一接入：linter + formatter、husky/pre-commit（可选）、错误上报（Sentry 或同类，含符号上传）

## 3. CI 流水线（GitHub Actions 模板要点，来自 DevOps Automator + Desktop App Engineer）

```yaml
# 每次 push/PR 必跑；发布流水线在其上叠加签名与发布
jobs:
  quality:
    steps: [lint, typecheck, unit-test]
  build-windows:
    runs-on: windows-latest
    steps:
      - build + package            # 产出安装包/绿色版
      - 足迹检查                    # 冷启动/空闲内存/安装体积，超预算即失败
  sign:                            # 有证书后启用
    - AzureSignTool / signtool + 时间戳（见阶段 7）
  publish-artifacts:               # 未签名的构建也作为 CI 产物留存
```

要点：
- 每个 PR 都跑全量测试；main 分支的构建必须可安装运行
- 测试失败、lint 失败、足迹超标 = 合并阻塞
- 密钥管理：签名证书/密码**绝不**进仓库和明文 CI 变量，用 GitHub Secrets / 云 HSM（Azure Key Vault 等）

## 4. "会走路的骨架"发布（Walking Skeleton）

在功能开发之前，用一个空壳应用完整走一遍发布链：

1. 空壳应用（只有窗口 + 关于页）
2. 走完整流水线：构建 → 打包 → 签名 → 上传 Release → 更新通道拉取成功
3. 在一台**干净**的 Windows 机器上全新安装、升级、卸载各走一遍
4. 更新器回滚演练：发布 N+1 后回退清单到 N，确认客户端干净降级

**这一步通过，才有资格开始写功能。**（对应仓库规则：签名、公证、更新通道、灰度、回滚——用内部渠道的 walking-skeleton 验证。）

## 5. 目录与文档模板

- `docs/adr/`（架构决策）、`docs/runbooks/`（发布/回滚操作手册）
- PR 模板：改了什么 / 为什么 / 怎么测的 / 截图
- `CHANGELOG.md`（Conventional Commits 自动生成 + 人工校对）

## 6. 质量门

| # | 判据 | 证据 | 通过？ |
|---|------|------|--------|
| 1 | CI 全绿（lint + test + build） | 流水线日志 | ☐ |
| 2 | 构建产物可在干净 Windows 安装运行 | 安装截图 | ☐ |
| 3 | 签名链走通（或证书采购单已下，有明确日期） | 签名验证输出 | ☐ |
| 4 | 更新通道 + 回滚演练通过 | 演练记录 | ☐ |
| 5 | 足迹预算基线已录入 CI | 预算配置 | ☐ |
| 6 | Git 规范与模板就位 | 仓库文件 | ☐ |

通过后 → 阶段 5（迭代实现）。
