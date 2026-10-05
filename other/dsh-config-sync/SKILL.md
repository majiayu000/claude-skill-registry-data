---
name: dsh-config-sync
description: 把 DSH（DeepSeek Harness）的用户配置（~/.dsh 下的 AGENTS.md、settings.yaml 及可选 profiles/预设）打包成脱敏骨架并在设备间安全同步恢复，提供只读审计、显式应用与 SHA-256 校验，绝不携带凭据和运行态。用于复现 DSH 环境、跨设备迁移偏好与模型路由配置。
version: 1.0.0
triggers:
  - "同步 DSH 配置"
  - "在另一台设备复用我的 DSH 设置"
  - "打包 ~/.dsh 配置"
  - "跨设备迁移 DSH 偏好 / 模型路由"
not_for:
  - "同步技能栈（Skills 请交给 environment-bootstrap）"
  - "编辑 ~/.dsh 的实际运行文件（本 skill 只做打包与恢复）"
depends_on:
  - skill-repository-maintainer
---

# DSH 配置同步（dsh-config-sync）

## 使用场景

当你想在另一台设备上复用本机的 DSH 用户配置，或把当前配置生成一份可追溯的脱敏归档时触发。它负责 `~/.dsh/` 下**配置类文件**（偏好、模型路由、预设）的安全打包与恢复。

职责边界很重要：**技能栈的同步交给 `environment-bootstrap`**，本 skill 只管 DSH 配置本体。

## 纳入与排除清单

对 `$DSH_HOME`（默认为 `~/.dsh`，可用 `$env:DSH_HOME` 覆盖）做如下归类：

| 路径 | 类型 | 处理 |
|---|---|---|
| `AGENTS.md` | 文件 | ✅ 纳入（用户全局偏好，纯文本无敏感） |
| `settings.yaml` | 文件 | ✅ 纳入（仅含 provider/model 与 `apiKeyEnv` 环境变量名，无明文密钥） |
| `profiles/` | 目录 | ⚠️ 可选（需显式指定才纳入） |
| `.agent-presets/` | 目录 | ⚠️ 可选 |
| `patches/` | 目录 | ⚠️ 可选 |
| `.credentials.yaml` | 文件 | ❌ **强制排除**（真实凭据，打进公开仓库即泄密） |
| `sessions/`storages/` | 目录 | ❌ **强制排除**（运行时态，仓库硬约束禁止） |
| `skills/` | 目录 | ⛔ 不归本 skill，交给 `environment-bootstrap` |

## 安全边界

- **凭据绝不出包**：`.credentials.yaml` 和任何可能含明文密钥的路径，打包含前必须显式排除并由校验确认不存在。
- **settings.yaml 只携带环境变量引用**：`apiKeyEnv: BAI_API_KEY` 这样的条目是“环境变量名”，换设备时由目标端设置同名环境变量即可，不在包内放任何密钥值。
- 不通过恢复删除目标端额外文件；旧/未登记的配置文件应单独审查。
- 不隐式安装插件、MCP、包、hooks 或全局配置。
- 不以旧目标文件、stdout 或 apply exit code 单独作为成功证据。
- 回滚应从已知稳定归档/提交重新复制，不使用递归删除。

## 模板渲染（跨设备路径适配）

导出时加 `--template` 自动将已知设备路径替换为占位符，恢复时渲染回目标设备值：

| 占位符 | 替换场景 | 示例 |
|---|---|---|
| `{{DSH_HOME}}` | `~/.dsh` 目录下的任何路径 | `C:\Users\<user>\.dsh\profiles\web` → `{{DSH_HOME}}\profiles\web` |
| `{{DESKTOP}}` | 桌面路径（含 Windows 双反斜杠形式） | `C:\Users\<user>\Desktop\work` → `{{DESKTOP}}\work` |
| `{{HOME}}` | 用户主目录 | `C:\Users\<user>\` → `{{HOME}}\` |

> 替换顺序按最长优先，防止嵌套路径（如 `{{DSH_HOME}}` 在 `{{HOME}}` 之前替换）。恢复时同步处理 Windows 双反斜杠路径。`--with-optional` 导出 `profiles/` 或 `.agent-presets/` 时模板渲染尤其有用，因为这些目录常含设备绝对路径。特殊自定义路径（如非标准布局的 `C:\Desktop\`）需手动模板化后按 `{{DSH_HOME}}`/`{{HOME}}` 同样处理。

## 打包（export）

1. 确认源 `$DSH_HOME` 存在，并解析其真实路径。
2. 按“纳入/排除清单”收集要打包的配置项；`.credentials.yaml`、`sessions/`、`storages/` 无论是否显式指定都强制排除。
3. 可选：`--with-optional` 额外纳入 `profiles/`、`.agent-presets/`、`patches/` 目录中的文件。
4. 在仓库内建立一个脱敏架构录（例如 `dsh-config/` 或打包器输出目录），把每个纳入路径复制进去。复制后跑一次敏感扫描：若发现 `apiKeyEnv` 之外的疑似密钥、`.credentials.yaml` 或运行时文件，把该包标为 FAIL 并停止。
5. 可选：`--template` 把已知设备路径（`~/.dsh`、桌面、主目录）替换为 `{{DSH_HOME}}`/`{{DESKTOP}}`/`{{HOME}}` 占位符，使包可跨设备复用。渲染后的文件 SHA-256 记录在 manifest 中，恢复时跳过 SHA 校验（因为内容会因设备而异）。
6. 为每个文件计算 SHA-256，生成 `manifest.json`（含路径、版本号、SHA-256、打包时间、模板渲染记录）。
7. 报告：源路径、纳入项、排除项、SHA-256、敏感扫描结果、模板化文件列表。只有扫描干净才报 `PASS`。

## 恢复（restore）

1. 明确目标 `$DSH_HOME`（Windows 常见 `C:\Users\<user>\.dsh`），不得猜测其他用户目录。
2. 先做只读 `check`：对比归档与目标端，列出 missing / different / extra、已模板化文件（跳过 SHA 校验），不写任何文件。
3. 用户明确要求时执行 `apply`，自动将 `{{DSH_HOME}}`/`{{DESKTOP}}`/`{{HOME}}` 渲染为目标设备路径；然后对同一目标端再次 `check` 并核对 SHA-256（模板化文件仅验证存在性）。
4. 目标端仅此文件（额外文件）保持不动，并在报告中列明。

## 输出契约

报告：模式（`check`/`apply`/`export`）、源/目标路径、纳入与排除项数量、`missing`/`different`/`extra`、每个文件的 SHA-256、敏感扫描结果、模板化文件列表、剩余风险。只有 post-apply 校验干净且敏感扫描为空时才报 `PASS`；有明确的非阻塞目标差异时报 `PARTIAL`。

## 验证

成功同步的最低证据：

```text
export: completed
sensitive-data scan: PASS (no .credentials.yaml, no runtime files, no inline secrets)
apply: completed
post-apply SHA-256 check: PASS (templated files: existence verified)
destination-only files: preserved and reported
```
