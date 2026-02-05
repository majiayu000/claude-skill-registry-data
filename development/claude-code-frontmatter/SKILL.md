---
name: claude-code-frontmatter
description: Use when creating or editing Claude Code skills, agents (subagents), or slash commands. Provides complete YAML frontmatter property reference.
---

# Claude Code YAML Frontmatter Reference

Skills、Agents（subagents）、Commands のYAML frontmatter完全リファレンス。

## Skills (SKILL.md)

```yaml
---
name: skill-name                    # 必須: 識別子（小文字、ハイフン）
description: Use when...            # 必須: いつ使うか（第三人称）
allowed-tools: Read, Grep, Glob     # 任意: 許可ツール（カンマ区切り）
model: inherit                      # 任意: inherit / 具体的モデル名
version: "1.0.0"                    # 任意: バージョン管理用
disable-model-invocation: false     # 任意: trueでSlash tool自動呼び出し禁止
mode: false                         # 任意: trueでMode Commandsセクション表示
---
```

| Property | Required | Values |
|----------|----------|--------|
| `name` | Yes | 小文字・ハイフンのみ |
| `description` | Yes | "Use when..."形式推奨 |
| `allowed-tools` | No | Read, Grep, Glob, Bash, Write, Edit, Task... |
| `model` | No | `inherit` / `claude-opus-4-20250514` 等 |
| `version` | No | セマンティックバージョン |
| `disable-model-invocation` | No | `true` / `false` |
| `mode` | No | `true` / `false` |

## Agents (Subagents)

```yaml
---
name: agent-name                    # 必須: 識別子
description: |                      # 必須: 説明（マルチライン可）
  Use when reviewing code...

  <example>
  user: "レビューして"
  assistant: "agent-nameで確認します"
  </example>
tools: Read, Grep, Glob, Bash       # 任意: 許可ツール（省略時は全継承）
model: sonnet                       # 任意: sonnet/opus/haiku/inherit
color: blue                         # 任意: 視覚識別用カラー
permissionMode: default             # 任意: 権限モード
skills: skill1, skill2              # 任意: 自動ロードするスキル
---
```

| Property | Required | Values |
|----------|----------|--------|
| `name` | Yes | 識別子 |
| `description` | Yes | 説明（example付きマルチライン推奨） |
| `tools` | No | カンマ区切り（省略=全ツール継承） |
| `model` | No | `sonnet` / `opus` / `haiku` / `inherit` |
| `color` | No | `red` / `blue` / `green` / `yellow` / `purple` / `orange` / `pink` / `cyan` |
| `permissionMode` | No | `default` / `acceptEdits` / `bypassPermissions` / `plan` |
| `skills` | No | カンマ区切りのスキル名 |

### color について
- 公式ドキュメントには未記載だが `/agents` コマンドで生成される
- ターミナルでsubagent呼び出し時に視覚的に識別可能

### permissionMode 詳細
| Mode | 説明 |
|------|------|
| `default` | 通常の権限確認 |
| `acceptEdits` | ファイル編集を自動承認 |
| `bypassPermissions` | 全権限を自動承認（危険） |
| `plan` | 読み取り専用、変更不可 |

## Commands (Slash Commands)

```yaml
---
description: コマンドの説明          # 推奨: SlashCommand toolで必要
argument-hint: [arg1] [arg2]        # 任意: 引数ヒント
allowed-tools: Bash(git:*), Read    # 任意: 許可ツール
model: claude-3-5-haiku-20241022    # 任意: 使用モデル
disable-model-invocation: true      # 任意: SlashCommand tool禁止
---
```

| Property | Required | Values |
|----------|----------|--------|
| `description` | Recommended | 説明文 |
| `argument-hint` | No | `[message]`, `[file] [options]` 等 |
| `allowed-tools` | No | ツール制限（ワイルドカード可） |
| `model` | No | 具体的なモデル名 |
| `disable-model-invocation` | No | `true` / `false` |

### Bash実行機能
`allowed-tools`を指定すると、プロンプト内で `!` プレフィックスでBash実行可能：
```markdown
Current status: !`git status`
```

### 引数プレースホルダー
- `$ARGUMENTS` - 全引数
- `$1`, `$2`, `$3`... - 位置引数

## 配置場所

| Type | Project | User | Plugin |
|------|---------|------|--------|
| Skills | `.claude/skills/` | `~/.claude/skills/` | `skills/` |
| Agents | `.claude/agents/` | `~/.claude/agents/` | `agents/` |
| Commands | `.claude/commands/` | `~/.claude/commands/` | `commands/` |

**優先順位:** Project > User > Plugin

## Sources

- [Subagents - Claude Code Docs](https://code.claude.com/docs/en/sub-agents)
- [Agent Skills - Claude Code Docs](https://code.claude.com/docs/en/skills)
- [Slash Commands - Claude Code Docs](https://code.claude.com/docs/en/slash-commands)
- [GitHub Issue #8501 - Frontmatter documentation](https://github.com/anthropics/claude-code/issues/8501)
- [Claude Agent Skills Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
