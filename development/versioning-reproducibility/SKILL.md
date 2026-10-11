---
name: versioning-reproducibility
description: >
  版本与可复现性：SemVer/CalVer、依赖版本范围与锁文件、库 vs 应用的约束策略、
  hermetic builds（Nix/Bazel）、升级监控与回滚。手动点名使用。
---

# 版本与可复现性

主线：代码连续演进、离散发布；版本号是「库在某一时刻的状态」的标识。盯着自己的依赖已经够累，算上传递依赖（依赖的依赖）更不可行——所以有版本约定（SemVer）、约束语法、锁文件、封闭构建这一整条复现链。

## 版本号

- SemVer：`MAJOR.MINOR.PATCH`——PATCH 只修 bug、完全兼容；MINOR 加功能、向后兼容；MAJOR 破坏兼容、可能要改代码。注意 0.x 阶段语义不同（0.1.3 → 0.2.0 也可能破坏兼容），`1.0.0-rc.1` 这类预发布也有讲究。
- CalVer：按日期命名（Ubuntu 24.04 / 24.10）——一眼看出多旧，但不传达任何兼容性信息。
- changelog 记录每次发布改了什么。SemVer 也会失手（维护者在 MINOR/PATCH 里意外引入破坏），别盲信。

## 约束与锁定

- 约束语法（Python）：`==` 精确；`>=` 最低版本；`>=1.24,<2.0` 区间；`~=2.1.0` 兼容发布（= >=2.1.0,<2.2.0，≈ npm/cargo 的 `^`）。
- 锁定（pinning）：用精确版本而非区间。包管理器解完所有传递依赖约束后，把最终版本清单存成锁文件（如 uv.lock、Cargo.lock，含下载地址与哈希，面向机器而非人读）。之后用 `uv sync` 这类命令安装，保证与测试时完全同版本——直接按 pyproject.toml 现解的话，可能解析到更新的版本。
- 库 vs 应用/服务，策略相反：库会被别人的代码引用，约束太严容易和用户的其他依赖冲突 → 用宽松区间（例：requests 只给三条宽区间、主要约束 major）；应用是最终消费者 → 精确锁定（例：ripgrep 的依赖全部精确版本——他们测过这套组合），让所有人跑同一套依赖。
- 极致复现：Nix/Bazel 的 hermetic builds——编译器、系统库、构建环境全部锁定并内容寻址，任何时间地点构建产物逐位一致。动机：Python 3.12 本身就依赖特定版本的 C 编译器，这类「运行时之外的变数」正是普通包管理器管不到的（NixOS/flakes 连整机配置都能版本化）。

## 升级与回滚

- 恒久张力：新版本引入破坏（有意或无意）vs 旧版本随时间积累安全漏洞。对策：CI 里对新版本跑测试（见代码质量一讲）+ Dependabot 类自动化盯新版本发布。
- 升级出问题多半是 dev/prod 环境不一致——预置回滚计划：版本降回去，重新部署已知好版本。

> 改编自 MIT The Missing Semester 课程 Lecture 6: Packaging and Shipping Code（讲义 + 口播稿，CC BY-NC-SA 4.0）：https://creativecommons.org/licenses/by-nc-sa/4.0/ · 课程站点：https://missing.csail.mit.edu/ · 讲座视频：https://www.youtube.com/watch?v=KBMiB-8P4Ns
