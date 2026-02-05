---
name: whalefall-version-update
description: WhaleFall(鲸落) 全局版本更新/发版同步工作流. 用于 bump 版本号(语义化 MAJOR.MINOR.PATCH)、消除 APP_VERSION/pyproject/env/uv.lock/部署脚本/健康检查/页脚/错误页/README/CHANGELOG/About 时间轴的版本漂移,并提供自检脚本与提交/PR 模板.
---

# WhaleFall 版本更新

## 输入

- 目标版本号 `X.Y.Z`(语义化版本).
- 本次发版主题/一句话摘要(用于 `CHANGELOG.md` 与 About 时间轴).

## 工作流

1. 读取强一致清单并确认当前版本号.
   - 需要完整指南时,读取 `references/VERSION_UPDATE_GUIDE.md`.
2. 优先更新 `app/settings.py` 的 `APP_VERSION`,再同步其余文件.
3. 更新 `CHANGELOG.md` 与 `app/templates/about.html` 的本次发版记录.
4. 运行自检脚本与质量命令,核对 `git status` 只包含必要文件.

## 强一致文件清单(必须同步)

- `app/settings.py`: 更新 `APP_VERSION`(运行时版本号唯一来源).
- `pyproject.toml`: 更新 `[project].version`.
- `env.example`: 更新 `APP_VERSION=...`.
- `uv.lock`: 在 `[[package]] name = "whalefalling"` 节点更新 `version = "..."`.
- `scripts/deploy/deploy-prod-all.sh`: 更新脚本头部注释/横幅/日志中的版本号.
- `app/routes/main.py`: 更新 `app_version` 返回值(供前端展示).
- `app/templates/base.html`: 更新页脚版本展示.
- `nginx/error_pages/404.html` 与 `nginx/error_pages/50x.html`: 更新错误页版本展示.
- `README.md`: 更新顶部徽章与底部“最后更新/版本”.
- `CHANGELOG.md`: 顶部新增或更新本次版本条目(倒序).
- `app/templates/about.html`: 时间轴追加本次版本记录(不改历史条目).

## 验证与自检

1. 运行版本一致性自检(最小集): 确认 `app/settings.py`/`pyproject.toml`/`env.example`/`uv.lock` 的版本号一致.
   - 可用 `rg -n \"X\\.Y\\.Z\"` 辅助核对是否还有遗漏.
2. 运行质量/检查命令(按需选择): `make quality` 或 `ruff check <files>`.
3. 核对 `git status`/`git diff`,避免仅为版本号而改动 `docs/Obsidian/architecture/*`、`docs/reports/*` 等大文档.

## 输出模板

- 提交信息: `chore: bump version to X.Y.Z` 或 `chore: release vX.Y.Z`.
- PR 核对清单:
  - [ ] `app/settings.py` 的 `APP_VERSION` 已更新并作为基准值
  - [ ] `pyproject.toml`/`env.example`/`uv.lock` 已同步
  - [ ] `/admin/api/app-info` 的 `app_version` 已同步
  - [ ] 页脚/错误页/README 已同步
  - [ ] `CHANGELOG.md` 与 About 时间轴已补充
  - [ ] 已确认 `app/settings.py`/`pyproject.toml`/`env.example`/`uv.lock` 版本一致

## 兼容与回退

- 若仓库中缺少指南里提到的历史脚本(例如 `check_missing_docs_smart.py`),使用 `make quality` 作为回退验证.
- 若依赖文件出现与项目版本相同的数字,先确认是否为第三方依赖版本,避免误替换.
