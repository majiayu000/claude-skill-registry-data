---
name: api-development
description: FastAPI 기반 API 개발 스킬. 엔드포인트 생성, 스키마 정의, 미들웨어 작업 시 자동으로 활성화됩니다. endpoint, route, schema, pydantic, fastapi 키워드에 반응합니다.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash
---

# API Development Skill

FastAPI 기반 REST API 개발 전문 스킬입니다.

## 핵심 역량

### 1. 엔드포인트 개발
- RESTful API 설계
- Path/Query/Body 파라미터 처리
- 응답 모델 정의

### 2. 스키마 관리
- Pydantic v2 모델 정의
- Request/Response 스키마
- 유효성 검증

### 3. 미들웨어
- 인증 (JWT, API Key)
- Rate limiting
- CORS 설정
- 에러 핸들링

### 4. 의존성 주입
- FastAPI Depends() 패턴
- 서비스 주입
- 데이터베이스 연결

## 프로젝트 구조

```
src/api/
├── v1/routes/
│   ├── analytics.py
│   ├── competency.py
│   ├── creator.py
│   ├── health.py
│   ├── missions.py
│   └── recommendations.py
├── schemas/
│   ├── request_schemas.py
│   └── response_schemas.py
└── middleware/
    ├── auth.py
    ├── rate_limit.py
    └── error_handler.py
```

## 코딩 컨벤션

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/v1/creators", tags=["creators"])

class CreatorRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    category: str

class CreatorResponse(BaseModel):
    id: str
    name: str
    status: str

@router.post("/", response_model=CreatorResponse)
async def create_creator(
    request: CreatorRequest,
    service: CreatorService = Depends(get_creator_service)
) -> CreatorResponse:
    """크리에이터를 생성합니다."""
    return await service.create(request)
```

## 베스트 프랙티스

- [ ] 모든 엔드포인트에 response_model 지정
- [ ] 적절한 HTTP status code 사용
- [ ] Docstring으로 OpenAPI 문서화
- [ ] Depends()로 의존성 주입
- [ ] 예외는 HTTPException으로 처리
