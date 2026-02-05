---
name: sync-openapi
description: |
  core-interface OpenAPI 스펙 조회 및 동기화. Use when:
  (1) API 구현 전 스펙 확인, (2) Controller 작성 시 DTO 확인,
  (3) Response 형식 확인, (4) v0.4.x CODE 단계.
tools: [Bash, Read, GitHub CLI]
---

> **🔔 시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: sync-openapi 호출 - {API 경로}` 시스템 메시지를 첫 줄에 출력하세요.

# Sync OpenAPI Skill

> core-interface OpenAPI 스펙을 기반으로 API 구현 가이드

## Background

```text
core-interface (OpenAPI 3.1 Spec)
        ↓ (Single Source of Truth)
   ┌────┴────┐
   ↓         ↓
core-backend   cm-template
(Spring Boot)  (Next.js)
```

## When to Use

- API Controller 구현 전
- Request/Response DTO 작성 시
- API 응답 형식 확인 시
- v0.4.x CODE 단계

## Quick Start

```bash
# OpenAPI 스펙 전체 조회
gh api repos/semicolon-devteam/core-interface/contents/openapi-spec.json \
  --jq '.content' | base64 -d

# 특정 Path 조회 (jq 필요)
gh api repos/semicolon-devteam/core-interface/contents/openapi-spec.json \
  --jq '.content' | base64 -d | jq '.paths["/api/v1/posts"]'
```

## DTO Naming Convention

| OpenAPI Operation | Request DTO | Response DTO |
|-------------------|-------------|--------------|
| createPost | CreatePostRequest | CreatePostResponse |
| getPost | - | GetPostResponse |
| updatePost | UpdatePostRequest | UpdatePostResponse |
| deletePost | - | - |
| listPosts | - | PagedPostsResponse |

## ApiResponse Pattern

```kotlin
sealed class ApiResponse<T> {
    data class Success<T>(
        val success: Boolean = true,
        val data: T,
        val message: String? = null,
        val timestamp: Instant = Instant.now()
    )

    data class PagedSuccess<T>(
        val success: Boolean = true,
        val data: List<T>,
        val pagination: Pagination,
        val message: String? = null,
        val timestamp: Instant = Instant.now()
    )

    data class Error(
        val success: Boolean = false,
        val message: String,
        val errorCode: String? = null,
        val fieldErrors: Map<String, String>? = null,
        val timestamp: Instant = Instant.now()
    )
}
```

## Output Format

```markdown
[SEMO] Skill: sync-openapi 호출 - {endpoint}

## API Spec: POST /api/v1/posts

### Request
```json
{
  "title": "string",
  "content": "string"
}
```

### Response (201)
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "title": "string",
    "content": "string",
    "createdAt": "datetime"
  }
}
```

### DTO Suggestion
```kotlin
data class CreatePostRequest(
    val title: String,
    val content: String
)

data class CreatePostResponse(
    val id: UUID,
    val title: String,
    val content: String,
    val createdAt: Instant
)
```
```

## Critical Rules

1. **Always check spec first**: 구현 전 core-interface 확인 필수
2. **Follow DTO naming**: Operation ID prefix 규칙 준수
3. **Polymorphic responses**: discriminator 패턴 사용
4. **Error responses**: 표준 ErrorResponse 형식

## Related Skills

- `implement` - v0.4.x CODE 단계에서 사용
- `scaffold-domain` - Controller 생성 시 참조

## Related Resources

- **Swagger UI**: https://core-interface-ashen.vercel.app/
- **Repository**: https://github.com/semicolon-devteam/core-interface

## References

- [DTO Patterns](references/dto-patterns.md)
- [Polymorphic Types](references/polymorphic-types.md)
