---
name: code-explorer
description: Search and analyze code repositories on GitHub and Hugging Face (Models, Datasets, Spaces). This skill should be used when exploring open-source projects, finding implementation references, discovering ML models/datasets, or analyzing how others have solved similar problems.
---

# Code Explorer

## Overview

To search and analyze code repositories across GitHub and Hugging Face platforms, use this skill. It enables discovering implementation patterns, finding relevant ML models/datasets, and exploring demo applications (Spaces) for learning and reference.

## Supported Platforms

| Platform | Search Targets | Tool |
|----------|---------------|------|
| **GitHub** | Repositories, Code | `gh` CLI |
| **Hugging Face** | Models, Datasets, Spaces | `uvx hf` CLI + `huggingface_hub` API |

## 검색 품질 원칙 (필수)

### 1. 현재 날짜 확인

```bash
date +%Y-%m-%d
```
아래 예시의 연도는 참고용. 실제 검색 시 **현재 연도** 사용.

### 2. Long-tail Keywords 적용

예시의 Short-tail을 그대로 쓰지 말고 확장:

| 예시 (참고용) | 실제 검색 (Long-tail) |
|---------------|----------------------|
| `"object detection"` | `"open vocabulary object detection pytorch inference {현재연도}"` |
| `"gradio demo"` | `"gradio image segmentation interactive demo huggingface"` |
| `"qwen vl"` | `"qwen2-vl vision language model zero-shot example code"` |

### 3. Multi-Query 적용

한 번에 찾기 어려우면 **2-3개 관점**으로 검색:

```bash
# 모델명 중심
gh search repos "qwen2-vl" --sort stars

# 기능 중심
gh search repos "vision language open vocabulary detection" --sort stars

# 구현 중심
gh search repos "vl model gradio demo inference" --sort stars
```

### 4. 필터 활용

```bash
# 최신 + 품질 필터 (현재 연도 적용)
gh search repos "keyword" stars:>50 pushed:>{현재연도-1}-01-01 --language python
```

### 5. 검색 전 체크리스트

- [ ] 현재 날짜 확인했는가?
- [ ] Short-tail을 Long-tail로 변환했는가?
- [ ] 필요시 2-3개 변형 쿼리로 검색했는가?
- [ ] 적절한 필터(언어, 스타, 날짜) 적용했는가?

---

## Workflow Decision Tree

```
User wants to explore code/resources
    |
    +-- Looking for code implementations?
    |   +-- Use GitHub search
    |       +-- scripts/search_github.py (or gh CLI directly)
    |       +-- Analyze repo structure, README, key files
    |
    +-- Looking for ML resources?
        +-- Use Hugging Face search
            +-- scripts/search_huggingface.py (search via API)
            +-- uvx hf download (download files)
```

## Scripts

**Always run scripts with `--help` first** to see usage. These scripts handle common search workflows reliably.

### Available Scripts

- `scripts/search_github.py` - GitHub repository search using gh CLI
- `scripts/search_huggingface.py` - Hugging Face search (models, datasets, spaces)

### Quick Examples

```bash
# GitHub search
python scripts/search_github.py "object detection" --limit 10 --help

# Hugging Face search
python scripts/search_huggingface.py "qwen vl" --type models --help
```

## GitHub Search

### Using gh CLI Directly

```bash
# Search repositories by keyword
gh search repos "open vocabulary detection" --sort stars --limit 10

# Filter by language
gh search repos "gradio app" --language python --limit 5

# View repository details
gh repo view owner/repo

# Search code within repositories
gh search code "Qwen2VL" --extension py
```

### Repository Analysis

To analyze a found repository:

1. Review README.md for usage instructions
2. Identify main entry points (app.py, main.py, inference.py)
3. Check dependencies (requirements.txt, pyproject.toml)
4. Study implementation patterns in source files

## Hugging Face Search

### Search (via script or Python API)

```bash
# Search models
python scripts/search_huggingface.py "object detection" --type models --limit 10

# Search datasets
python scripts/search_huggingface.py "coco" --type datasets --limit 5

# Search spaces (demos)
python scripts/search_huggingface.py "gradio demo" --type spaces --limit 10

# Search all types
python scripts/search_huggingface.py "qwen vl" --type all
```

### Download (via uvx hf)

```bash
# Download space source code (use /tmp/ for temporary analysis)
uvx hf download <space_id> --repo-type space --include "*.py" --local-dir /tmp/<space_name>

# Download model files
uvx hf download <repo_id> --include "*.json" --local-dir /tmp/<model_name>

# Download to project directory (when needed permanently)
uvx hf download <repo_id> --local-dir ./my-model
```

**Note**: Always use `--local-dir /tmp/` for temporary code analysis to avoid cluttering the project.

### Common Search Patterns

```bash
# Find models for specific task
python scripts/search_huggingface.py "open vocabulary detection" --type models
python scripts/search_huggingface.py "qwen2 vl" --type models
python scripts/search_huggingface.py "grounding dino" --type models

# Find demo applications
python scripts/search_huggingface.py "object detection demo" --type spaces
python scripts/search_huggingface.py "gradio image" --type spaces
```

### Analyzing a Space

To understand how a Space is implemented:

1. Find the space: `python scripts/search_huggingface.py "keyword" --type spaces`
2. Download source: `uvx hf download <space_id> --repo-type space --include "*.py" --include "requirements.txt" --local-dir /tmp/<space_name>`
3. Or view online: `https://huggingface.co/spaces/{space_id}/tree/main`
4. Focus on `app.py` for main logic
5. Check `requirements.txt` for dependencies

## Example Use Cases

### Find Qwen3-VL Open Vocab Detection Code

```bash
# Search GitHub
gh search repos "qwen vl object detection" --sort stars
gh search code "Qwen2VL" --extension py

# Search Hugging Face
python scripts/search_huggingface.py "qwen2-vl" --type models
python scripts/search_huggingface.py "qwen vl" --type spaces
```

### Find Gradio Demo Patterns

```bash
# Search spaces using Gradio
python scripts/search_huggingface.py "gradio object detection" --type spaces

# Download a space to study
uvx hf download username/space-name --repo-type space --include "*.py" --local-dir /tmp/space-name
```

### Find Pre-trained Detection Models

```bash
python scripts/search_huggingface.py "object-detection" --type models --limit 20
python scripts/search_huggingface.py "grounding-dino" --type models
python scripts/search_huggingface.py "yolo-world" --type models
```

## Resources

### scripts/
- `search_github.py` - GitHub repository search wrapper
- `search_huggingface.py` - Hugging Face Hub search wrapper

### references/
- `github_api.md` - GitHub CLI detailed reference
- `huggingface_api.md` - Hugging Face Hub API and CLI reference

## Tips

1. **Start broad, then narrow**: Begin with general keywords, then add filters
2. **Check stars/likes**: Higher counts often indicate quality
3. **Review recent activity**: Recently updated repos are better maintained
4. **Use --help first**: Scripts have detailed usage information
5. **Download selectively**: Use `uvx hf download --include` to download only needed files
6. **Always cite sources**: Include repository URLs, Space links, or model IDs you referenced
