---
name: python-backend-fastapi
description: 명시적 `/python-backend-fastapi` 호출 전용 FastAPI 참고서. 일반 Python 백엔드 작성·리뷰에는 자동 적용하지 않는다.
license: MIT
metadata:
  version: "1.0.0"
---

# Python Backend Development Guide (FastAPI)

Python FastAPI 백엔드 개발을 위한 종합 가이드.

## 적용 시점

다음 작업 시 이 가이드를 참조:
- Python 파일 생성/수정
- FastAPI 엔드포인트 작성
- Pydantic 스키마 정의
- 데이터베이스 모델 설계
- 비동기 함수 작성

---

## 핵심 원칙

### 1. 파일/모듈 책임 분리 ⚠️ CRITICAL
- 하드 제한 줄 수가 아니라 **기능/책임 단위**로 모듈을 나눈다
- 한 파일이 여러 유스케이스, 계층, 엔티티 책임을 섞으면 분리한다
- 대형 파일은 자동 실패가 아니라 **분리 검토 신호**로만 사용한다

### 2. 함수 크기 제한
- **최대 50줄**
- **권장 20줄 이하**
- 하나의 함수는 하나의 작업만

### 3. 모듈화 & 재사용성
- 공통 로직은 `utils/` 또는 `core/`로 분리
- 비즈니스 로직은 서비스 레이어에
- 데이터 접근은 리포지토리 패턴

---

## 프로젝트 구조

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 앱 초기화 (< 100줄)
│   ├── api/                    # API 엔드포인트
│   │   ├── __init__.py
│   │   ├── deps.py            # 의존성 주입
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py        # 인증 API (< 300줄)
│   │       ├── users.py       # 사용자 API (< 300줄)
│   │       └── forms.py       # 폼 빌더 API (< 400줄)
│   ├── core/                   # 핵심 설정 및 보안
│   │   ├── config.py          # 환경 설정 (< 200줄)
│   │   ├── security.py        # JWT, 암호화 (< 300줄)
│   │   └── database.py        # DB 연결 (< 100줄)
│   ├── models/                 # SQLAlchemy 모델
│   │   ├── user.py            # User 모델만 (< 150줄)
│   │   └── form.py            # Form 모델만 (< 200줄)
│   ├── schemas/                # Pydantic 스키마
│   │   ├── user.py            # User 스키마 (< 150줄)
│   │   └── form.py            # Form 스키마 (< 200줄)
│   ├── services/               # 비즈니스 로직
│   │   ├── auth_service.py    # 인증 로직 (< 300줄)
│   │   └── user_service.py    # 사용자 관리 (< 400줄)
│   ├── repositories/           # 데이터 접근 레이어
│   │   ├── base.py            # BaseRepository (< 200줄)
│   │   └── user_repository.py # User CRUD (< 250줄)
│   └── utils/                  # 유틸리티
│       ├── validators.py      # 검증 함수 (< 200줄)
│       └── file_handler.py    # 파일 처리 (< 300줄)
├── tests/
│   ├── conftest.py
│   └── test_users.py
├── alembic/                    # DB 마이그레이션
├── requirements.txt
└── .env.example
```

---

## 코딩 규칙

### 1. 타입 힌트 필수

✅ **올바른 예:**
```python
from typing import Optional, List

async def get_user_by_id(
    user_id: str,
    db: AsyncSession
) -> Optional[User]:
    result = await db.execute(
        select(User).where(User.user_id == user_id)
    )
    return result.scalar_one_or_none()
```

❌ **잘못된 예:**
```python
async def get_user_by_id(user_id, db):
    result = await db.execute(
        select(User).where(User.user_id == user_id)
    )
    return result.scalar_one_or_none()
```

---

### 2. 비동기 함수 사용

✅ **올바른 예:**
```python
@router.get("/users/{user_id}")
async def read_user(
    user_id: str,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    user = await user_service.get_user(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(user)
```

---

### 3. Pydantic 스키마 분리

```python
# schemas/user.py
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    employee_id: str = Field(..., min_length=3, max_length=50)
    username: str = Field(..., min_length=3, max_length=100)
    full_name: str = Field(..., max_length=100)
    role: str = Field(..., pattern="^(SystemAdmin|QAManager|Tester|Viewer)$")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=100)
    role: Optional[str] = None

class UserResponse(UserBase):
    user_id: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

---

### 상세 코드 패턴

> 서비스 레이어, 리포지토리, 에러 핸들링, 파일 업로드, 의존성 주입 패턴: [references/code-patterns.md](references/code-patterns.md)

---

## 체크리스트

### 코드 작성 전
- [ ] 파일이 기능/책임 단위로 분리되어 있는지 확인
- [ ] 함수가 50줄을 넘지 않는지 확인
- [ ] 재사용 가능한 로직인지 확인 → utils 분리

### 코드 작성 중
- [ ] 모든 함수/변수에 타입 힌트 추가
- [ ] Docstring 작성 (Args, Returns, Raises)
- [ ] 비동기 함수 사용 (`async`/`await`)
- [ ] Pydantic 스키마 분리
- [ ] 서비스 레이어 패턴 적용

### 코드 작성 후
- [ ] 에러 핸들링 확인
- [ ] 로깅 추가 (중요 작업)
- [ ] 단위 테스트 작성
- [ ] 자동 코드 리뷰 실행

---

## 추가 참고 자료

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [Pydantic 문서](https://docs.pydantic.dev/)
- [SQLAlchemy 2.0 문서](https://docs.sqlalchemy.org/)

---

**버전:** 1.0.0
**최종 업데이트:** 2026-01-16
