---
name: github-issue-helper
description: GitHub 이슈 작성 도우미. 사용자가 이슈 초안이나 아이디어를 제시하면 고품질 GitHub 이슈로 개선. Use when user asks to (1) write/create/draft a GitHub issue, (2) improve/refine an issue draft, (3) convert an idea into a proper issue format, (4) review issue quality. Supports bug reports, feature requests, and improvement proposals. Communicates in Korean but produces final issues in English.
---

# GitHub Issue Helper

Transform rough ideas or drafts into high-quality GitHub issues that contributors and coding agents can easily understand.

## Core Principles

### Language Rules
- Communicate with user in **Korean**
- Write final issue output in **English**

### Quality Standards
1. **Clear Context**: Provide enough background for unfamiliar contributors
2. **Concrete Code Examples**: Include snippets showing the problem and solution
3. **Neutral Stance**: Never mark any solution as "Recommended" - best approach varies by context
4. **Link Related Resources**: Reference relevant issues, PRs, and docs

## Workflow

1. **Analyze**: Examine user's draft or idea
2. **Classify**: Determine if bug report, improvement, or feature request
3. **Gather Info**: Ask user for missing information if needed
4. **Research**: Search related issues/PRs on GitHub if possible
5. **Draft**: Write issue in English using templates in [references/templates.md](references/templates.md)
6. **Explain**: Provide feedback in Korean about intent and improvements

## Template Selection

- **Bug Report / Improvement**: Use when reporting defects or proposing enhancements to existing functionality
- **Feature Request**: Use when proposing entirely new capabilities

See [references/templates.md](references/templates.md) for complete templates.

## Quality Checklist

Before finalizing, verify:

- [ ] Background section provides sufficient context
- [ ] Motivation is clear and compelling
- [ ] Code examples are included where applicable
- [ ] Multiple solution options are presented
- [ ] No "Recommended" labels on any option
- [ ] Related issues/PRs are linked
- [ ] (Feature) Benefits section is clear
- [ ] (Feature) Already Answered section addresses common questions
- [ ] English grammar and expressions are natural

## Key Guidelines

- Present pros/cons objectively for each solution option
- Write code examples that are concrete and runnable
- Assume reader is unfamiliar with the codebase
- Actively use GitHub URLs or issue numbers if provided by user