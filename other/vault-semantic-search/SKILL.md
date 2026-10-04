---
name: vault-semantic-search
description: Concept-level semantic search across the vault using a FAISS vector index (bge-m3, 中英文 both supported) — finds related notes by meaning, not keywords. Use when the user says "语义搜索" / "semantic search", "找相关笔记" / "find related notes", "what do I know about X", or "重建索引" / "rebuild index". NOT for synthesizing a composed answer across many notes (use vault-knowledge-synthesis).
---

# Semantic Search Skill

使用 FAISS 向量索引进行 vault 语义搜索。**中英文都支持**。

## 触发词

| 用户说 | 动作 |
|--------|------|
| "语义搜索" / "semantic search" | 运行语义搜索 |
| "找相关笔记" / "find related notes" | 语义搜索 |
| "What do I know about X?" | 语义搜索 |
| "重建索引" / "rebuild index" | 重新构建索引 |

## 脚本路径

| 平台 | 路径 |
|------|------|
| MacBook | `{vault}/30_Resources/Technology/AI-LLM/scripts/semantic_search.py` |
| Home PC | `{vault}\30_Resources\Technology\AI-LLM\scripts\semantic_search.py` |

## 使用方法

### MacBook

```bash
cd ~/Documents/Main\ Vault/30_Resources/Technology/AI-LLM/scripts
python3 semantic_search.py "查询内容" --top 10
python3 semantic_search.py "query" --context  # 显示内容片段
python3 semantic_search.py --index            # 重建索引
```

### Home PC (Windows)

```powershell
cd "{vault}\30_Resources\Technology\AI-LLM\scripts"
python semantic_search.py "查询内容" --top 10
python semantic_search.py "query" --context
python semantic_search.py --index
```

## 技术架构

| 组件 | 技术 |
|------|------|
| Embedding 模型 | bge-m3 (1024维, 多语言) |
| 向量存储 | FAISS (IndexFlatIP) |
| Embedding 服务 | Ollama (本地优先，SSH 备份) |
| 索引位置 | `.semantic_index/` |

## 索引范围

- `10_Projects/`
- `20_Areas/`
- `30_Resources/`

不索引: `00_Inbox`, `40_Archive`, `50_Journal`, `99_Attachments`

## 索引维护

### 检查索引状态
```bash
python3 semantic_search.py --check
```

### 智能更新（>7天才重建）
```bash
python3 semantic_search.py --smart
```

### 何时需要重建索引
- 大量新增/删除笔记后
- 索引超过 7 天
- 搜索结果明显过期

### 维护建议
- **自动**: 和 vault-index (link-index) 一起维护，每周一次
- **手动**: 用户说"重建索引"时执行 `--index`

## 注意事项

1. **中英文都支持** - bge-m3 是多语言模型，中英文查询效果都好
2. **索引会自动同步** - 存在 vault 里，通过 Syncthing 同步
3. **需要 Ollama 运行** - `ollama serve` 或后台服务
4. **超长文件会跳过** - 超过 context 长度的文件
5. **首次索引较慢** - bge-m3 比 nomic 大，约 15-30 分钟
6. **索引过期容忍度高** - 7天内的索引仍可用，不像 link-index 需要实时

## 依赖

```bash
pip install faiss-cpu numpy requests
ollama pull bge-m3
```

## 相关

- [[ComfyUI]] - 远程服务器配置
- [[_411 AI tools MOC]]
