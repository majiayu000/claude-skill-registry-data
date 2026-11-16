---
name: alibaba--open-code-review
description: "AI-powered code review CLI từ Alibaba — phân tích git diff, comment chính xác theo dòng, tích hợp GitHub Actions / GitLab CI. Đã review cho hàng chục nghìn developer nội bộ Alibaba."
allowed-tools: Bash, Read, Write
user-invocable: true
---

Open Code Review (OCR) là CLI review code tự động bằng AI — kết hợp deterministic engineering + agent để tránh các lỗi AI review phổ biến (bỏ sót file, comment sai dòng).

## Install

```bash
npm install -g open-code-review
# Hoặc tải binary từ GitHub Releases
```

## Config

```json
// ~/.opencodereview/config.json
{
  "llm": {
    "provider": "anthropic",
    "apiKey": "...",
    "model": "claude-sonnet-4-6"
  }
}
```

```bash
ocr llm test   # kiểm tra kết nối
```

## Usage

```bash
# Review từ HEAD~1 đến HEAD
ocr review

# Review từ branch cụ thể
ocr review --from main --to feature/my-branch

# Review 1 commit
ocr review --commit abc123

# Output JSON cho CI/CD parse
ocr review --output json
```

## CI/CD Integration

```yaml
# GitHub Actions
- name: AI Code Review
  run: |
    npm install -g open-code-review
    ocr review --from ${{ github.event.pull_request.base.sha }} \
               --to ${{ github.sha }} \
               --output json > review.json
```

## Architecture

- **Deterministic file selection** — đảm bảo cover toàn bộ changeset, không bỏ sót
- **Smart bundling** — gom file liên quan thành nhóm cho sub-agent review contextual
- **Fine-grained rule matching** — rule template per file type (TypeScript, Python, Go...)
- **External positioning module** — sửa vị trí comment độc lập với LLM output
- Parallelism mặc định 8 processes — có thể tune

## Web Viewer

```bash
ocr viewer   # localhost:5483 — UI xem kết quả review
```

## Source

https://github.com/alibaba/open-code-review · Apache-2.0
