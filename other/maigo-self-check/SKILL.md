---
name: maigo-self-check
description: This skill should be used when a maigo diff touches agents/, commands/, skills/ (including SKILL.md and references/), mkdocs.yml, or docs/ — in those cases validate_plugin + mkdocs --strict are the verification standard, not just pytest.
---

<!-- mkdocs-include-start -->

# Maigo Self-Check

**Owner**: Taki (Verifier)
**Consumers**: `/maigo:go`, `/maigo:quick`, `/maigo:team`, `/maigo:crystallize`

## 觸發條件

diff 動到以下任一路徑時啟用本 skill：

- `agents/`
- `commands/`
- `skills/`（含 `SKILL.md` 與 `references/` 子目錄）
- `mkdocs.yml`
- `docs/`

純動 Python source（`hooks/`、`scripts/`、`tests/`）→ 只跑 pytest，不觸發本 skill。
兩者都動（如同時改 `scripts/` 與 `docs/`）→ pytest + 本 skill 兩條都跑。

## 驗證指令

```
uv run python scripts/validate_plugin.py
uv run mkdocs build --strict
```

**為什麼都用專案環境**：

- `uv run python scripts/validate_plugin.py` — validator 使用專案宣告的 Python
  版本；不受 host 上較舊的系統 `python3` 影響。
- `uv run mkdocs build --strict` — mkdocs 是 venv 工具（在 `pyproject.toml` 的
  docs dependency 裡）。

## 這兩條抓的是 pytest 抓不到的東西

| 問題類型 | 被哪條抓到 |
|---------|-----------|
| include shim 缺失（`docs/skills/<name>.md` 沒建） | `validate_plugin.py` |
| frontmatter `name` 對不上目錄名 | `validate_plugin.py` |
| skill catalog（`docs/reference/skills.md`）漏列 | `validate_plugin.py` |
| mermaid 相依圖缺 skill 節點 | `validate_plugin.py` |
| 相對 link 在 include-markdown rewrite 後炸 strict-mode | `mkdocs build --strict` |
| docs nav 指到不存在的 page | `mkdocs build --strict` |
| command 檔缺「掛名」角色台詞（引號旁邊沒有角色 emoji / 名字） | `validate_plugin.py` |
| `CLAUDE.md` / `AGENTS.md` 的共同驗證慣例漂移 | `validate_plugin.py` |

pytest 測的是 Python 行為；上述問題都在 plugin 結構層——pytest 對它們是盲的。

新增 / 改 `commands/*.md` 時，至少保留一段**掛名**角色台詞（MyGO!!!!! 濃度慣例）——單純
「有「」引號」不算數，旁邊要看得到角色 emoji / 名字（或是 `> 「...」` blockquote 標題引言），
不能只是 UI/error 訊息引號。機器兜底由 `validate_plugin.py` 的
`check_command_persona_quotes` 檢查，不必自己記著掃。

## 改 `references/*.md` 時：跟 SKILL.md 摘要同步

幫某個 skill 的 `references/*.md` 加新內容時，兩件事一起做，缺一都算沒改完：

1. **改之前**先看該 reference 檔開頭宣告的範圍（例如「Read this file when ...」）是否覆蓋新主題。
   題材對不上就不要硬塞——擴大宣告範圍，或改放進更貼切的位置（往往是 SKILL.md 本體裡已經在談同主題的段落）。
2. **改之後**同步 SKILL.md 本體對這份 reference 檔案的摘要（列出的條數、bullet 清單）——SKILL.md
   是永遠會被載入的主體，reference 檔是 on-demand；摘要沒同步，新內容等於沒人看得到。

**為什麼**：`/maigo:crystallize` 一次批次畢業多筆記憶時踩過兩次——`references/*.md` 加了新內容，
但 SKILL.md 本體的條數摘要（如「Three cross-cutting patterns」）沒跟著改成新的數字。這條檢查
不限 crystallize；`/maigo:quick`、`/maigo:go` 只要動到 `skills/` 都算。

## 兩條都必須綠才算完成

任何一條紅 → 驗證未通過，不算 Taki PASS。回報實際錯誤，不跳過、不假裝綠。
