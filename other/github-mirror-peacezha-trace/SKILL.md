---
name: github-mirror
description: "自动寻找当前网络环境下最快的 GitHub 代理镜像，用于克隆仓库、下载文件或获取 Release 资产。当需要从 github.com 下载任何内容时使用本 skill——包括 git clone、wget/curl 下载、Release 资产获取等。"
trigger: 当用户请求涉及以下任一场景时加载本 skill：
  1. 需要 git clone GitHub 仓库
  2. 需要 wget/curl 下载 GitHub 上的文件（github.com 或 raw.githubusercontent.com）
  3. 需要下载 GitHub Release 资产（tarball、二进制文件等）
  4. GitHub API 下载缓慢或超时
  5. 用户提到"GitHub 加速"、"GitHub 镜像"、"GitHub 代理"
---

# GitHub 镜像加速 — 自动寻找并使用最快的 GitHub 代理

当需要从 GitHub 下载代码时，直连可能很慢或被阻断。本 skill 自动寻找当前网络环境下最快的 GitHub 代理镜像，然后使用它完成下载。

## 使用场景

以下**任何**涉及从 GitHub 下载的操作均应使用本 skill：
- `git clone` GitHub 仓库
- `wget`/`curl` 下载 github.com 或 raw.githubusercontent.com 的文件
- 下载 Release 资产（tarball、二进制文件）
- 获取 GitHub 仓库中的原始文件
- 任何缓慢或超时的 GitHub API 下载

## 工作流程

### 第一步：检查缓存，直接使用已知镜像

先读取缓存文件 `{skill_dir}/scripts/mirrors-github.txt`：

```bash
cat {skill_dir}/scripts/mirrors-github.txt
```

- **如果文件存在且有内容**：取第一行作为 `BEST_MIRROR`，直接跳到第三步使用它。无需测速，无需爬取。
- **如果文件不存在或为空**：进入第二步，运行完整的测速流程来填充缓存。

### 第二步（仅在缓存不可用时）：运行 Mirror Scout 测速

运行 mirror-scout 工具对可用的 GitHub 代理镜像进行测速排名：

```bash
python3 {skill_dir}/scripts/mirror-scout.py --github --no-scrape --top 5
```

默认加 `--no-scrape` 跳过网页爬取以节省时间，仅测试内置可靠镜像和缓存中的镜像。

如果缓存为空且 `--no-scrape` 没有找到可用镜像，去掉该参数进行完整爬取：
```bash
python3 {skill_dir}/scripts/mirror-scout.py --github --top 5
```

该工具会：
1. 从 `mirrors-github.txt` 加载已知镜像
2. （可选）从内置来源爬取更多候选镜像
3. 通过每个镜像下载测试文件并测量实际速度
4. 按下载速度排名并展示前 5 个
5. 将结果保存回 `mirrors-github.txt`，下次直接使用缓存

### 第二步附：解析输出并选择最佳镜像

输出会展示排名结果，类似：
```
=== Ranking by download speed  ===
Rank  Speed          Latency      Mirror
1     12.34 MiB/s    0.234s       https://ghfast.top
2      8.21 MiB/s    0.512s       https://ghproxy.link
```

选择排名第 1 的镜像（速度最快）。

### 第三步：使用最佳镜像进行下载

**git clone：**
```bash
# 原始命令：git clone https://github.com/user/repo.git
git clone https://BEST_MIRROR/https://github.com/user/repo.git
```

**wget/curl 原始文件：**
```bash
# 原始命令：wget https://raw.githubusercontent.com/user/repo/main/file.txt
wget https://BEST_MIRROR/https://raw.githubusercontent.com/user/repo/main/file.txt
```

**Release 资产：**
```bash
# 原始命令：wget https://github.com/user/repo/releases/download/v1.0/file.tar.gz
wget https://BEST_MIRROR/https://github.com/user/repo/releases/download/v1.0/file.tar.gz
```

**规律：** 在完整的 `https://github.com/...` 或 `https://raw.githubusercontent.com/...` URL 前面加上 `BEST_MIRROR/` 即可。

## 参数说明

| 参数 | 默认值 | 说明 |
|------|---------|------|
| `--github` | False | 启用 GitHub 镜像模式（必须） |
| `--no-scrape` | False | 跳过网页爬取，仅测试已知镜像 |
| `--top N` | 0（全部） | 仅展示前 N 个结果 |
| `--mirror URL` | — | 手动添加待测镜像（可重复使用） |
| `--timeout N` | 10 | 下载超时（秒） |
| `--connect-timeout N` | 3 | 连接超时（秒） |
| `--workers N` | 8 | 并发测试线程数 |
| `--max-mb N` | 1 | 每个镜像最大测试下载量（MB） |
| `--source URL` | 内置 | 额外爬取的来源页面（可重复使用） |

## 错误处理

- 如果**缓存中的镜像下载失败**：尝试缓存文件中的下一个镜像（第二行、第三行……）。
- 如果**所有缓存镜像都失败**：运行完整测速重新筛选：
  ```bash
  python3 {skill_dir}/scripts/mirror-scout.py --github --top 5
  ```
- 如果**仍无可用镜像**，手动添加后重新测速：
  ```bash
  python3 {skill_dir}/scripts/mirror-scout.py --github --mirror https://ghproxy.net --mirror https://mirror.ghproxy.com --top 5
  ```
- 测速结果会自动保存到 `mirrors-github.txt`，后续使用无需重复测速。

## 依赖

本工具需要 Python 3.6+ 和 `requests` 库。如未安装，先执行：
```bash
pip install requests
```
