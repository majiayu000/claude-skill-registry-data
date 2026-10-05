---
name: gstack-upgrade
version: 1.0.0
description: |
  gstack 自升级流程。能区分全局安装与 vendored 安装，执行升级、同步、
  写标记并展示新版本变化。 (gstack)
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
---
<!-- 中文参考译文。 -->

# /gstack-upgrade

这个 skill 负责把 gstack 升到最新版，同时尽量保留用户现有安装方式。

## Inline Upgrade Flow

### 第 1 步：询问用户或自动升级

- 如果配置允许自动升级，就直接继续。
- 否则通过 `AskUserQuestion` 给用户几个选项：现在升级、稍后提醒、跳过本次、彻底关闭提醒。

### 第 2 步：识别安装类型

- 判断当前是全局安装、仓库 vendored 安装，还是两者并存。
- 后续升级路径取决于这个识别结果。

### 第 3 步：保存旧版本

- 记录旧版本号，便于后面给出 “from -> to” 的反馈。

### 第 4 步：执行升级

- 拉取新版本并跑必要的 setup / build。
- 如果同时存在 vendored 副本，还会在后续做同步。

### 第 4.5 步：同步本地 vendored copy

- 确保仓库内 vendored 的 gstack 跟全局版本一致，避免用户在不同入口拿到不同版本。

### 第 5 步：写标记并清缓存

- 写入 “刚升级过” 的标记。
- 清理相关缓存，避免旧版本信息残留。

### 第 6 步：展示 What’s New

- 汇总并展示当前版本变化内容。
- 说明升级成功后的下一步。

## 独立使用场景

除了在共享 preamble 中自动被调用外，用户也可以显式运行 `/gstack-upgrade` 做一次手动升级。
