---
name: deskclaw-security-vuln-check
slug: deskclaw-security-vuln-check
version: 1.1.1
displayName: 安全自动检查（Security Vuln Check）
summary: DeskClaw 安全自检工具，通过 Python 脚本检查 gateway-venv 及 PATH 上所有解释器是否残留 litellm，支持版本比对（1.82.7/1.82.8 通报版本标记），跨平台（macOS/Linux/Windows），纯标准库。
tags: security, vulnerability, check, litellm, deskclaw, audit
description: "DeskClaw advisory self-checks for litellm via scripts/check_deskclaw_litellm.py (gateway-venv then every distinct python on PATH; reports version and flags 1.82.7/1.82.8) or equivalent shell snippets in SKILL.md. Use when users ask for 安全漏洞检查, litellm checks, or post-upgrade hygiene audit."
---

# DeskClaw 安全漏洞检查（可迭代）

DeskClaw 团队在升级与排障过程中**发现**若干**环境与依赖演化**下可能出现的风险，**特此整理成自检步骤，提醒用户在本机核对**——**并非**声称「由 DeskClaw 当前版本向你的电脑植入了某包」。本 Skill 随发现增补检查项：**后续可在本文档追加新小节**（建议结构：背景 → 步骤 → 解读 → 处置）。

**安装位置**：本 Skill 目录为 `~/.deskclaw/skills/deskclaw-security-vuln-check/`（脚本在同级 `scripts/`）。DeskClaw 或 Agent 调用时请使用该路径，勿依赖仓库内 `.cursor/skills/` 旧位置。

## 检查顺序（须按序执行）

1. **DeskClaw `gateway-venv`**（`~/.deskclaw/gateway-venv`）— **与产品自身安全最相关**，优先查。  
2. **PATH 上各目录中的 Python**— 脚本按 PATH **逐目录**查找 `python3` / `python`（Windows 为对应 `.exe`），按**解析后的真实路径去重**，**每个 distinct 解释器各查一遍**，避免 PATH 首部被临时注入时只检查到那一个。**通常由 DeskClaw 拉起**，PATH 即应用环境；开发机手动跑时仍以 **gateway** 为产品结论依据。仅需查单个解释器时用 `--default-python`。

## 当前检查项一览

| 编号 | 项目 | 状态 |
|------|------|------|
| 1 | **gateway-venv 残留 litellm**（历史环境可能未清干净；**含版本与 1.82.7/1.82.8 比对**） | 已纳入 |
| 2 | **PATH 上各 distinct 解释器是否安装 litellm**（去重后逐一检查） | 已纳入 |

---

## 1. gateway-venv 是否仍残留 litellm

### 背景

**`litellm` 存在已知安全风险**（供应链与漏洞面等，细节以公开安全通告为准）。**DeskClaw 当前随附的 `nanobot-ai` 已在最新版本中完全移除对该包的依赖**，运行时**不应再需要** litellm。

若你曾长期使用旧版本，本地 `~/.deskclaw/gateway-venv` 里**仍可能残留**早年装上的 litellm（包管理器未必会自动卸载已不再依赖的包）。本项自检用于**确认你的环境里是否还带着这个不应再保留的依赖**。

### 何时做这项

- 用户问是否残留 litellm、gateway-venv 是否干净  
- 诊断显示 venv 中存在 litellm  
- 从大版本 DeskClaw / nanobot 升级后做自查  

### 检查步骤

**首选：运行 Skill 随附脚本**（仅标准库、跨平台；**pip + import + site-packages 目录** 与手写片段逻辑一致）。

- 路径：`~/.deskclaw/skills/deskclaw-security-vuln-check/scripts/check_deskclaw_litellm.py`（与本 `SKILL.md` 同目录下的 `scripts/`）
- 子命令：`all`（默认，先 gateway 再 default）、`gateway`、`default`
- 环境变量：`DESKCLAW_GATEWAY_VENV` 可覆盖 gateway venv 根目录
- 参数：`--venv PATH` 同上；`--default-python EXE` 可强制指定第 2 项的解释器（一般不需要）。
- **执行方式**：产品侧以 **DeskClaw 调用**为主；本脚本不专门为「开发机 `uv run`」调校 `default` 的 PATH 语义。
- **版本号**：检出 litellm 后，脚本会用该解释器子进程读取 `importlib.metadata.version("litellm")`，失败则解析 `pip show` 的 `Version:`；将 **release 主版本**（如 `1.82.8.post0` → `1.82.8`）与脚本内常量比对。
- **当前通报需重点关注的 litellm 版本**：`1.82.7`、`1.82.8`（维护时在 `check_deskclaw_litellm.py` 顶部的 `KNOWN_ALERT_VERSIONS` 扩展）。**其他已安装版本**会明确提示「不在当前通报版本」，便于较远版本用户理解风险语境；**退出码仍为 `1` = 任意范围检出 litellm**（与是否命中通报版本无关）；机器可读行末含 `high_risk_version=yes|no`。

```bash
SCRIPT="${SCRIPT:-$HOME/.deskclaw/skills/deskclaw-security-vuln-check/scripts/check_deskclaw_litellm.py}"
python3 "$SCRIPT"                  # 等同 all
python3 "$SCRIPT" gateway
python3 "$SCRIPT" default
python3 "$SCRIPT" --venv /path/to/gateway-venv all
```

Windows（示例，`%USERPROFILE%` 即用户主目录）：

```text
py -3 "%USERPROFILE%\.deskclaw\skills\deskclaw-security-vuln-check\scripts\check_deskclaw_litellm.py"
```

**退出码：`0` = 本次检查范围内未检出 litellm；`1` = 至少一处检出 litellm（无论版本是否命中通报）。**  
**SUMMARY 行**：`litellm_detected=yes|no`；`high_risk_version=yes` 表示至少一处已解析版本属于当前通报的 `1.82.7` / `1.82.8`；若执行了 default 范围则有 `path_interpreters_checked=N`（PATH 去重后的解释器个数）。

**Agent：优先在用户本机执行上述 `python3 …/check_deskclaw_litellm.py`；若无法运行该文件，再使用下方手写 shell。**

---

#### 手写备选（与脚本等价；勿只跑 `pip show`）

**macOS / Linux**

```bash
VENV="${DESKCLAW_GATEWAY_VENV:-$HOME/.deskclaw/gateway-venv}"
if [ ! -d "$VENV" ]; then
  echo "未找到 gateway-venv 目录: $VENV"
  exit 0
fi
PY=""
for cand in "$VENV/bin/python3" "$VENV/bin/python"; do
  if [ -x "$cand" ]; then PY="$cand"; break; fi
done
if [ -z "$PY" ]; then
  echo "未找到可执行解释器: $VENV/bin/python3 或 $VENV/bin/python"
  exit 0
fi
echo "解释器: $PY"
DET=0
if "$PY" -m pip show litellm >/dev/null 2>&1; then
  echo "[pip] 检测到 litellm"
  DET=1
fi
if "$PY" -c "import importlib.util,sys; sys.exit(0 if importlib.util.find_spec('litellm') else 1)" 2>/dev/null; then
  echo "[import] 可加载 litellm 模块"
  DET=1
fi
for f in "$VENV"/lib/python*/site-packages/litellm*; do
  [ -e "$f" ] || continue
  echo "[fs] $f"
  DET=1
  break
done
if [ "$DET" -eq 1 ]; then
  echo "→ 本项：检测到 litellm"
else
  echo "→ 本项：未检测到 litellm"
fi
```

**Windows（PowerShell）**（venv 的 site-packages 在 **`Lib\site-packages`**，不是 `lib\python*`）

```powershell
$venv = Join-Path $env:USERPROFILE ".deskclaw\gateway-venv"
$py = $null
foreach ($name in @("python.exe", "python3.exe")) {
  $p = Join-Path $venv "Scripts\$name"
  if (Test-Path $p) { $py = $p; break }
}
if (-not $py) {
  "未找到 gateway-venv 或 Scripts\python*.exe"
} else {
  "解释器: $py"
  $det = $false
  & $py -m pip show litellm 2>$null | Out-Null
  if ($LASTEXITCODE -eq 0) { "[pip] 检测到 litellm"; $det = $true }
  & $py -c "import importlib.util,sys; sys.exit(0 if importlib.util.find_spec('litellm') else 1)" 2>$null
  if ($LASTEXITCODE -eq 0) { "[import] 可加载 litellm"; $det = $true }
  $sp = Join-Path $venv "Lib\site-packages"
  if (Test-Path $sp) {
    $hits = Get-ChildItem -Path $sp -Filter "litellm*" -ErrorAction SilentlyContinue
    if ($hits) { "[fs] $($hits[0].Name)"; $det = $true }
  }
  if ($det) { "→ 本项：检测到 litellm" } else { "→ 本项：未检测到 litellm" }
}
```

### 解读

| 结果 | 含义 |
|------|------|
| **`[pip]` / `[import]` / `[fs]` 任一出现** | **本项需关注**：该 venv 下存在 litellm（含 pip 元数据缺失但仍可 import 的情况） |
| **脚本输出的 `[gateway] 版本: …`** | 已解析版本；若 release 为 **1.82.7 / 1.82.8** → 与当前通报一致，**优先处置**；**其他版本** → 不在本次通报版本号内，可结合产品策略评估是否仍要移除 |
| 无 venv、无解释器、或三路皆无 | **未检测到**（或尚未 bootstrap） |

手写片段若未打印版本，可补一行（与脚本同源思路）：`"$PY" -c "import importlib.metadata as m; print(m.version('litellm'))"`。

### 处置建议（可选，按意愿执行）

1. **使用较新版本 DeskClaw**：团队在 bootstrap 中已加强 venv 重建/依赖同步，升级后**重启应用**可自动收敛多数残留场景。  
2. **手动卸载**：`uv pip uninstall -p <gateway-venv 内 python> litellm`  
3. **彻底重建**：删除 `~/.deskclaw/gateway-venv`（及可选 `.gateway-venv-app-version`）后重启应用，由 bootstrap 新建 venv。

---

## 2. PATH 上各解释器是否安装 litellm（补充）

### 背景

与第 1 项不同：脚本会按 PATH **逐目录**查找 `python3` / `python`（Windows 为对应 `.exe`），按**解析后的真实路径去重**，**每个 distinct 解释器各查一遍**，避免 PATH 前面被临时插入的目录只让你检查到「第一个」Python。**DeskClaw 拉起时** PATH 即应用环境；**产品安全结论仍以第 1 项 gateway-venv 为准**。下方手写 shell 仅演示单个解释器；**PATH 全量遍历以脚本为准**。

**请先完成第 1 项**，再执行本节。

### 检查步骤

**首选**：使用 `~/.deskclaw/skills/deskclaw-security-vuln-check/scripts/check_deskclaw_litellm.py`，只跑 PATH 项：

```bash
python3 "$HOME/.deskclaw/skills/deskclaw-security-vuln-check/scripts/check_deskclaw_litellm.py" default
```

---

#### 手写备选（**pip + import** 双路；仅单个「当前 command -v」解释器，不等价于脚本的 PATH 全遍历）

**macOS / Linux**（优先 `python3`，否则 `python`）

```bash
run_litellm_check() {
  py="$1"
  echo "解释器: $(command -v "$py" 2>/dev/null || echo "$py")"
  det=0
  if "$py" -m pip show litellm >/dev/null 2>&1; then echo "[pip] 检测到 litellm"; det=1; fi
  if "$py" -c "import importlib.util,sys; sys.exit(0 if importlib.util.find_spec('litellm') else 1)" 2>/dev/null; then echo "[import] 可加载 litellm"; det=1; fi
  if [ "$det" -eq 1 ]; then echo "→ 默认 Python：检测到 litellm"; else echo "→ 默认 Python：未检测到 litellm"; fi
}
if command -v python3 >/dev/null 2>&1; then run_litellm_check python3
elif command -v python >/dev/null 2>&1; then run_litellm_check python
else echo "未找到 python3 / python，跳过本项"
fi
```

**Windows（PowerShell）**（依次尝试 `python`、`python3`、再用 `py -3` 解析出的 `sys.executable`）

```powershell
function Invoke-LitellmCheck([string]$pyExe) {
  "解释器: $pyExe"
  $det = $false
  & $pyExe -m pip show litellm 2>$null | Out-Null
  if ($LASTEXITCODE -eq 0) { "[pip] 检测到 litellm"; $det = $true }
  & $pyExe -c "import importlib.util,sys; sys.exit(0 if importlib.util.find_spec('litellm') else 1)" 2>$null
  if ($LASTEXITCODE -eq 0) { "[import] 可加载 litellm"; $det = $true }
  if ($det) { "→ 默认 Python：检测到 litellm" } else { "→ 默认 Python：未检测到 litellm" }
}
if (Get-Command python -ErrorAction SilentlyContinue) {
  Invoke-LitellmCheck (Get-Command python).Source
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
  Invoke-LitellmCheck (Get-Command python3).Source
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
  $exe = py -3 -c "import sys; print(sys.executable)" 2>$null
  if ($exe) { Invoke-LitellmCheck $exe.Trim() } else { "py -3 不可用，跳过本项" }
} else {
  "未找到 python / python3 / py，跳过本项"
}
```

### 解读

| 结果 | 含义 |
|------|------|
| **`[pip]` 或 `[import]` 任一出现**（脚本在任一路径 `#i` 上） | **本项需关注**：该解释器环境下存在 litellm |
| **脚本 `[default#i] 版本: …`** | 同第 1 项：1.82.7 / 1.82.8 为通报重点；其余版本不在该号段内 |
| 未找到解释器或两路皆无 | **本项通过** 或 **跳过** |

### 处置建议（务必谨慎）

- 卸载可能影响**依赖 litellm 的其他项目**；执行前请自行确认。  
- 对**检出 litellm 的那一个（或多个）解释器**分别处理：`python3 -m pip uninstall litellm`（路径与 SUMMARY / 脚本输出一致）。若使用 **uv**：`uv pip uninstall -p <该解释器> litellm`。  
- **Conda**：`conda list litellm` 若存在，用 `conda remove litellm`（以你环境为准）。

---

## 给用户汇总模板（随检查项增加而扩展）

```markdown
## DeskClaw 安全漏洞检查

| 检查项 | 结果 | litellm 版本（若检出） | 是否命中通报 1.82.7/1.82.8 | 是否需关注 |
|--------|------|------------------------|---------------------------|------------|
| ① gateway-venv | 检测到 / 未检测到 / 无 venv | 例 1.82.0 或 — | 是 / 否 / — | 是 / 否 / — |
| ② PATH 各解释器（脚本 default） | 检测到 / 未检测到 / 跳过 | 按 `default#i` 填写 | 按版本 | 是 / 否 / — |
| （后续项…） | … | … | … | … |

**SUMMARY（脚本）：** `litellm_detected=…` `high_risk_version=…` `path_interpreters_checked=…`（若有）

**建议：** …
```

## 迭代说明（给维护者）

新增检查时：优先扩展本目录下 `scripts/check_deskclaw_litellm.py`（或新增 `scripts/` 下脚本），再在「当前检查项一览」与正文补说明；`description` frontmatter 补充触发词。仓库内若仍有旧副本，以 `~/.deskclaw/skills/deskclaw-security-vuln-check/` 为准。

## 注意

- 勿在对话中泄露用户密钥；pip 输出只摘「是否安装 / 版本号」即可。
