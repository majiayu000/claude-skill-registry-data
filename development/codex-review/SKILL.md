---
name: codex-review
description: Delegates code review to OpenAI Codex CLI. Use when user says "코드 리뷰해줘", "Codex한테 리뷰 맡겨", "PR 검토해줘", "코드 품질 체크", "리팩토링 제안해줘", "second opinion", or asks for code review, refactoring suggestions.
---

# Codex Code Review

Delegate code reviews to OpenAI Codex for detailed analysis.

## When to Use

- Code quality review
- Pull request analysis
- Refactoring suggestions
- Security vulnerability detection
- Best practices compliance

## How to Use

### For file review:
```bash
codex review < path/to/file.py
```

### For inline code:
```bash
echo "code here" | codex review
```

### For specific task:
```bash
codex exec "review this code for security issues: <code>"
```

## Integration

The Codex CLI is pre-authenticated and ready to use. Results will be returned and summarized for the user.

## Example Workflow

1. User asks: "Review my changes in src/main.py"
2. Read the file content
3. Pipe to `codex review`
4. Summarize the findings for user
