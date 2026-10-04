---
name: skill-rag-indexer
description: "RAG indexer for local skill documents with semantic search and intelligent skill recommendation."
---

# Skill RAG Indexer

## Description
RAG (Retrieval-Augmented Generation) 索引器，用于本地 skill 文档的语义搜索和智能推荐。支持自然语言搜索、基于任务的 skill 推荐、以及知识库管理。使用 TypeScript + sqlite-vss 构建，本地优先、零外部依赖。

## Activation Keywords
- skill rag search
- search skills
- find skill
- recommend skill
- 搜索技能
- 推荐技能
- skill index
- 技能索引
- rag index
- 查找技能
- 技能搜索

## Tools Used
- exec: 运行 TypeScript CLI 工具
- read: 读取 SKILL.md 文件
- write: 更新索引数据库
- glob: 发现 skill 目录

## Installation

### Prerequisites
- Node.js 20+
- npm or yarn

### Install Dependencies
```bash
cd collection/skills/skill-rag-indexer
npm install
npm run build
```

### Configure Embeddings
Create a `.env` file:
```bash
# .env
EMBEDDING_PROVIDER=openai
OPENAI_API_KEY=sk-your-api-key-here

# Or use Cohere
# EMBEDDING_PROVIDER=cohere
# COHERE_API_KEY=your-api-key-here
```

### Build Initial Index
```bash
npm run index:build
```

## Usage Patterns

### Search Skills
```bash
# 语义搜索 (默认)
skill-rag search "我需要分析股票数据"

# 关键词搜索
skill-rag search --keyword "python"

# 混合搜索
skill-rag search "web开发" --hybrid

# 限制结果数量
skill-rag search "编程" --limit 5
```

### Recommend Skills
```bash
# 为任务推荐 skill
skill-rag recommend "我想创建一个新的 agent"

# 推荐并限制数量
skill-rag recommend "数据分析" --limit 3

# 只包含特定 skills
skill-rag recommend "coding" --include opencode,claude-code
```

### Manage Index
```bash
# 构建完整索引
skill-rag index build

# 强制重建
skill-rag index build --force

# 增量更新 (只处理变更)
skill-rag index update

# 查看索引状态
skill-rag index status
```

### Using npm Scripts
```bash
# 快捷命令
npm run index:build
npm run index:update
npm run index:status
npm run search -- "your query"
npm run recommend -- "your task"
```

## Instructions for Agents

### Step 1: Check Installation
When the skill is activated, first verify installation:

```bash
cd collection/skills/skill-rag-indexer
if [ ! -d "node_modules" ]; then
  echo "Installing dependencies..."
  npm install
  npm run build
fi
```

### Step 2: Check Index Status
Check if the index exists and is up-to-date:

```bash
npm run index:status
```

If index doesn't exist, build it:
```bash
echo "Building initial index..."
npm run index:build
```

### Step 3: Determine Operation Type
Identify what the user wants:
- **Search**: User asks to find/search skills
- **Recommend**: User asks for skill recommendations for a task
- **Index Management**: User wants to build/update the index

### Step 4: Execute the Command
Run the appropriate CLI command with user's query.

For search:
```bash
npm run search -- "user's query here"
```

For recommendation:
```bash
npm run recommend -- "user's task description here"
```

For index management:
```bash
npm run index:build    # or index:update, index:status
```

### Step 5: Present Results
Format results clearly, showing:
- Skill name and description
- Relevance score
- Key features
- Quick access path

If results are found, offer to:
- Show more details about a specific skill
- Activate a recommended skill
- Refine the search

## Context Files

### Config File (.skill-rag-indexer.json)
```json
{
  "databasePath": "./skills-index.db",
  "embeddingsProvider": "openai",
  "embeddingsModel": "text-embedding-3-small",
  "skillsRoot": "../../collection/skills",
  "search": {
    "defaultLimit": 10,
    "minScore": 0.5,
    "hybridWeight": 0.7
  }
}
```

### Environment Variables (.env)
```bash
EMBEDDING_PROVIDER=openai
OPENAI_API_KEY=sk-...
COHERE_API_KEY=...
SKILL_RAG_DB_PATH=./skills-index.db
SKILL_RAG_DEFAULT_LIMIT=10
SKILL_RAG_MIN_SCORE=0.5
SKILL_RAG_HYBRID_WEIGHT=0.7
```

## Error Handling

### Embedding API Error
```
If embedding generation fails:
  1. Check API key environment variables
  2. Fall back to keyword search only (if available)
  3. Inform user of limited functionality
  4. Suggest verifying API key configuration
```

### Index Not Found
```
If index doesn't exist:
  1. Auto-build the index (may take time)
  2. Show progress to user
  3. Continue with search after build
```

### Database Locked
```
If database is locked:
  1. Wait 1 second and retry
  2. If still locked, ask user to retry later
  3. Suggest checking for other processes using the database
```

### Node.js Not Installed
```
If Node.js 20+ is not available:
  1. Inform user of requirement
  2. Provide installation instructions
  3. Suggest alternative: manually browse SKILLS.md
```

## Configuration

### Search Options
- `--limit <n>`: Number of results to return (default: 10)
- `--min-score <0-1>`: Minimum similarity score threshold (default: 0.5)
- `--keyword`: Keyword-only search using FTS5
- `--semantic`: Semantic-only search using vector embeddings
- `--hybrid`: Combined search (default weight: 0.7 semantic, 0.3 keyword)

### Recommendation Options
- `--limit <n>`: Number of recommendations (default: 5)
- `--include <skills>`: Comma-separated list of skills to include
- `--exclude <skills>`: Comma-separated list of skills to exclude

### Index Options
- `--force`: Force full rebuild (drop existing index first)
- `--verbose`: Show detailed progress output

## Examples

### Example 1: Search for Stock Analysis Skills
```
User: "search for skills that can analyze stock data"

Agent Process:
1. Verify installation ✓
2. Check index status ✓
3. Run: npm run search -- "stock data analysis"
4. Present results:
   🟢 stock-analysis (92%) - 股票技术分析系统
   🟡 akshare (85%) - 中国金融数据接口库
   ...
```

### Example 2: Recommend Skills for Web Development
```
User: "recommend skills for building a web application"

Agent Process:
1. Run: npm run recommend -- "build web application"
2. Present recommendations with reasons:
   ⭐ fullstack-engineer (88%) - "For full-stack web development"
   👍 opencode (82%) - "For AI-assisted coding"
   ...
```

### Example 3: Build Index First Time
```
User: "build the skill index"

Agent Process:
1. Check if index exists
2. Run: npm run index:build
3. Show progress:
   - Found 5 skills
   - Indexing opencode... ✓
   - Indexing claude-code... ✓
   - ...
4. Confirm: "Index built successfully with 5 skills"
```

### Example 4: Incremental Update
```
User: "update the skill index"

Agent Process:
1. Run: npm run index:update
2. Show what changed:
   - New: 1 skill (new-agent)
   - Updated: 2 skills
   - Deleted: 0 skills
   - Unchanged: 3 skills
```

## Best Practices

1. **Keep Index Fresh**: Run `index update` after adding/modifying skills
2. **Use Hybrid Search**: Combine semantic and keyword for best results
3. **Environment Variables**: Store API keys in `.env`, not in code
4. **Version Control**: Add `.env` and `*.db` to `.gitignore`
5. **Performance**: For large collections, use incremental updates
6. **Quality**: Start with `text-embedding-3-small`, upgrade to `large` if needed

## Limitations

- Requires Node.js 20+ runtime
- Embeddings require API key (OpenAI or Cohere)
- sqlite-vss has platform-specific binaries
- First index build may take time (depending on number of skills)
- Vector search quality depends on embedding model choice

## Troubleshooting

### "sqlite-vss failed to load"
```bash
# Try re-installing sqlite-vss
npm rebuild sqlite-vss

# Or use pre-built binaries
npm install sqlite-vss --build-from-source=false
```

### "No API key provided"
```bash
# Check .env file exists and has valid keys
cat .env

# Make sure variables are exported
export OPENAI_API_KEY=sk-...
```

### "Database locked"
```bash
# Check for running node processes
ps aux | grep node

# Kill hanging processes if needed
pkill -f "skill-rag"
```

### "Skill not found"
```bash
# Verify skillsRoot path in config
skill-rag index status

# Check that SKILL.md exists in collection/skills/
ls ../../collection/skills/
```

## Resources

- [sqlite-vss GitHub](https://github.com/asg017/sqlite-vss)
- [OpenAI Embeddings API](https://platform.openai.com/docs/guides/embeddings)
- [Cohere Embeddings](https://docs.cohere.com/docs/embeddings)
- [Project README](./README.md)

## Related Skills

- **opencode**: For coding tasks that may use recommended skills
- **fullstack-engineer**: A comprehensive agent that can use discovered skills
- **research-agent**: For deep research that may benefit from skill discovery
