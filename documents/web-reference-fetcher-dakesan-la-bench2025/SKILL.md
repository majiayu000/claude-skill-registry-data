---
name: web-reference-fetcher
description: Fetch web content from URLs, extract specific topics using subagents, and save structured summaries as markdown. This skill should be used when other skills or workflows need to retrieve and analyze web documentation. Input is URL(s) and topic names, output is detailed markdown summaries saved to specified paths.
---

# Web Reference Fetcher

## Overview

This skill is designed to be called by other skills or workflows. It provides a three-step pipeline:
1. **Fetch**: Retrieve web content using jina.ai reader API
2. **Analyze**: Use subagents to extract specific topics and create detailed summaries
3. **Save**: Store the analyzed content as structured markdown files

## When to Use This Skill

Use this skill when:
- Another skill needs to fetch and analyze web documentation
- You have URL(s) and need structured topic extraction
- You need detailed summaries saved to specific file paths
- Working with reference materials that require analysis and organization

## Input Format

This skill expects:

1. **URL(s)**: One or more web URLs to fetch
2. **Experiment Context**: Filename and entry ID to determine output directory
3. **Output Path**: Standardized path `workdir/<filename>_<entry_id>/references/ref_<N>.md`

**Directory naming convention:**
- Extract filename from JSONL path: `public_test` from `data/public_test.jsonl`
- Combine with entry ID: `public_test_public_test_1`
- Create references subdirectory: `workdir/public_test_public_test_1/references/`
- Save each reference as: `ref_1.md`, `ref_2.md`, etc.

## Workflow

### Step 1: Fetch Web Content

Use the provided script to fetch raw content from URL(s).

**Execute:**

```bash
python3 .claude/skills/web-reference-fetcher/scripts/fetch_url.py <url> --output workdir/<filename>_<entry_id>/references/ref_<N>.md
```

**What it does:**
- Fetches content via `https://r.jina.ai/<url>`
- Returns clean markdown content
- Saves to standardized location

**Script options:**
- `--output <path>`: Save fetched content to file (required for standardized workflow)
- `--silent`: Suppress progress messages

**Standardized output location:**
- Reference files: `workdir/<filename>_<entry_id>/references/ref_<N>.md`
- Example: `workdir/public_test_public_test_1/references/ref_1.md`

**Output:**
The script saves the fetched markdown content to the specified path.

### Step 2: Analyze with Subagents

Pass the fetched content to a subagent along with extraction requirements.

**Subagent invocation pattern:**

Use the Task tool to launch a general-purpose subagent:

```
Prompt template:
以下のウェブコンテンツから、{トピック名}に関する詳細な情報を抽出してください。

コンテンツ:
---
{fetched_markdown_content}
---

抽出要件:
{extraction_requirements}

以下の形式でmarkdownとして出力してください:

# {トピック名}

## {セクション1}
[詳細な説明、テーブル、仕様など]

## {セクション2}
[詳細な説明、手順、コード例など]

...
```

**Extraction requirements** should specify:
- What topics to extract
- What level of detail is needed
- What format to use (tables, lists, code blocks, etc.)
- Any specific sections or keywords to focus on

### Step 3: Save Structured Output

Save the subagent's output to the specified path.

**File operations:**
- Create parent directories if they don't exist
- Save with UTF-8 encoding
- Verify file was written successfully

## Complete Example Usage

### Example 1: Fetch and Analyze a Single URL

```bash
# 1. Fetch content
CONTENT=$(python3 .claude/skills/web-reference-fetcher/scripts/fetch_url.py \
  "https://example.com/docs")

# 2. Pass to subagent via Task tool with:
#    - Fetched content
#    - Topic: "API Authentication Methods"
#    - Extraction: "Extract all authentication methods, parameters, and examples"

# 3. Save subagent output
#    Path: workdir/references/api_auth.md
```

### Example 2: Multiple URLs for Different Topics

```bash
# Fetch URL 1
CONTENT1=$(python3 .claude/skills/web-reference-fetcher/scripts/fetch_url.py \
  "https://example.com/spec")

# Analyze with subagent for Topic 1
# Save to: workdir/references/specification.md

# Fetch URL 2
CONTENT2=$(python3 .claude/skills/web-reference-fetcher/scripts/fetch_url.py \
  "https://example.com/tutorial")

# Analyze with subagent for Topic 2
# Save to: workdir/references/tutorial.md
```

## Integration with Other Skills

This skill is designed to be called by other skills. Example integration:

```markdown
# In another skill (e.g., test-case-handler skill):

## Step 3: Fetch Reference Documentation

For each reference URL in the test case:
1. Invoke web-reference-fetcher skill
2. Pass URL and topic extracted from test case instruction
3. Specify output path: `workdir/references/task_{N}/reference_{M}.md`
4. Use the saved markdown for further processing
```

## Extraction Requirements Examples

### For Technical Specifications

```
抽出要件:
- すべての技術パラメータを表形式で抽出
- 測定手順をステップバイステップで記載
- 計算式と例を含める
- 品質基準と許容範囲を明記
```

### For API Documentation

```
抽出要件:
- すべてのエンドポイントをリスト化
- リクエスト/レスポンス形式を示す
- 認証方法を詳細に説明
- エラーコードと対処方法を含める
```

### For Tutorials/Procedures

```
抽出要件:
- 手順を番号付きリストで抽出
- 各手順の詳細な説明を含める
- 必要なツールと前提条件を明記
- トラブルシューティング情報を追加
```

## Error Handling

### Fetch Errors
- **URL not accessible**: Report error, suggest alternatives
- **Network issues**: Check connectivity and jina.ai availability
- **Invalid URL format**: Validate URL before attempting fetch

### Subagent Errors
- **Content too large**: Split into chunks and analyze separately
- **Unclear extraction requirements**: Ask caller to specify details
- **Format issues**: Validate subagent output before saving

### File System Errors
- **Permission denied**: Check write permissions
- **Path not found**: Create parent directories automatically
- **Disk full**: Report error with suggested cleanup

## Resources

### scripts/

- **fetch_url.py**: Fetches web content via jina.ai
  - Input: URL string
  - Output: Clean markdown content to stdout
  - Options: `--output` to save raw content, `--silent` for quiet mode

## Advanced Usage

### Batch Processing

For multiple URLs:

```bash
for url in "${urls[@]}"; do
  # Fetch each URL
  # Launch subagents in parallel if possible
  # Save to respective paths
done
```

### Custom Output Formatting

Provide detailed formatting instructions to subagents:

```
フォーマット要件:
- 見出しレベル: H2を最上位とする
- コードブロック: 言語を明示する
- テーブル: Markdown形式、ヘッダー行を含む
- リスト: 階層構造を保持する
```

### Caching Fetched Content

To avoid re-fetching:

```bash
# Save raw content first
python3 .claude/skills/web-reference-fetcher/scripts/fetch_url.py \
  "https://example.com/docs" --output /tmp/cached_content.md

# Use cached content for multiple analyses with different extraction requirements
```

## Dependencies

- Python 3.6+
- `curl` command-line tool
- Internet connectivity
- Access to Task tool for subagent invocation
- Write permissions to output directories

## Quality Assurance

Before completing:
- [ ] URL was fetched successfully
- [ ] Subagent received correct content and extraction requirements
- [ ] Output file is well-structured and comprehensive
- [ ] File was saved to the correct path
- [ ] Caller has been informed of the saved location

## Communication Protocol

When called by other skills:
1. **Receive**: URL(s), extraction requirements, output path(s)
2. **Execute**: Fetch → Analyze → Save pipeline
3. **Return**: Success status and saved file path(s)
4. **Report errors**: Clear error messages with suggested fixes

## Self-Contained Design

This skill is self-contained and can be invoked without knowledge of:
- JSONL file structures
- Test case formats
- Specific project conventions

It only requires:
- Valid URL(s)
- Clear extraction requirements
- Valid output path(s)
