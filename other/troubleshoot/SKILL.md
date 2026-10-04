---
name: troubleshoot
description: >
  프로젝트 실행 중 발생하는 오류를 진단하고 해결하는 스킬.
  "/troubleshoot"를 입력하거나, 에러 메시지를 붙여넣거나,
  "안 돼요", "오류가 나요", "서버가 안 떠요" 같은 요청에 트리거된다.
  기존 트러블슈팅 가이드(doc/TROUBLESHOOTING.md)를 참조하여 해결한다.
---

# 트러블슈팅

프로젝트 실행 중 오류를 진단하고 해결하는 스킬이다.

## 진단 순서

### Step 1: 에러 분류

에러 메시지를 읽고 다음 중 어디에 해당하는지 판단한다:

| 카테고리 | 키워드 | 확인 대상 |
|----------|--------|-----------|
| MySQL 연결 | `Can't connect to MySQL`, `Connection refused :3307` | Docker 컨테이너 |
| Ollama 연결 | `Connection refused :11434`, `ollama` | Ollama 서버 |
| Python LLM 연결 | `Connection refused :8000`, `LLM 서버` | Python 서버 |
| Spring Boot 기동 | `ApplicationContextException`, `BeanCreation` | application.yml, 의존성 |
| JPA/Hibernate | `SQLSyntaxError`, `ConstraintViolation` | Entity, DDL |
| 응답 품질 | 중국어 출력, 빈 응답, 깨진 텍스트 | 시스템 프롬프트, 필터링 |

### Step 2: 인프라 상태 점검

```bash
# 1. Docker MySQL
docker-compose ps
docker-compose logs --tail=20

# 2. Ollama
curl http://localhost:11434/api/tags

# 3. Python LLM 서버
curl http://localhost:8000/health

# 4. Spring Boot
curl http://localhost:8080/actuator/health  # actuator 설정 시
```

### Step 3: 카테고리별 해결

## 자주 발생하는 오류

### MySQL 연결 실패

**증상:** `Can't connect to MySQL server on 'localhost'`

**확인:**
```bash
docker-compose ps           # 컨테이너 실행 상태
docker-compose up -d        # 중지됐으면 시작
docker-compose logs mysql   # MySQL 로그 확인
```

**원인 & 해결:**
- 컨테이너 미실행 → `docker-compose up -d`
- 포트 충돌 → `netstat -an | grep 3307` 확인
- 인증 오류 → `.env` 파일의 `MYSQL_USER`, `MYSQL_PASSWORD` 확인

### Ollama 연결 실패

**증상:** `Connection refused :11434`

**확인:**
```bash
ollama list                 # 설치된 모델 확인
ollama serve                # 서버 시작
ollama pull qwen2.5:7b      # 모델 없으면 다운로드
```

**원인 & 해결:**
- Ollama 미실행 → `ollama serve`
- 모델 미설치 → `ollama pull qwen2.5:7b`
- GPU 메모리 부족 → 더 작은 모델 사용 또는 `OLLAMA_NUM_GPU=0`

### Python LLM 서버 기동 실패

**증상:** FastAPI 서버가 시작되지 않음

**확인:**
```bash
cd python-llm
.venv/Scripts/python -c "import fastapi; print('OK')"   # 의존성 확인
.venv/Scripts/python -c "from config import get_settings; print(get_settings())"  # 설정 확인
```

**원인 & 해결:**
- 가상환경 미활성화 → `.venv\Scripts\activate`
- 의존성 미설치 → `pip install -r requirements.txt`
- MySQL 연결 실패 → Docker 컨테이너 먼저 시작
- ChromaDB 초기화 실패 → `USE_VECTOR_SEARCH=False`로 비활성화 후 확인

### Spring Boot ↔ Python 연결 실패

**증상:** `LLM 서버를 사용할 수 없습니다` (503)

**확인:**
```bash
curl -X POST http://localhost:8000/infer/medical \
  -H "Content-Type: application/json" \
  -d '{"query": "테스트"}'
```

**원인 & 해결:**
- Python 서버 미실행 → 실행 순서: MySQL → Ollama → Python → Spring Boot
- URL 불일치 → `application.yml`의 `llm.service.url` 확인
- 타임아웃 → `llm.service.timeout.read` 값 증가

### 중국어/깨진 텍스트 출력

**증상:** LLM 응답에 중국어, 한자, 특수 토큰이 포함됨

**원인 & 해결:**
- 시스템 프롬프트 미적용 → `app.py`의 시스템 프롬프트 확인
- 필터링 미동작 → `response_cleaner.py`의 `clean_llm_response()` 확인
- 모델 문제 → `qwen2.5:7b` 등 한국어 지원 모델로 변경

### JPA Entity 불일치

**증상:** `SQLSyntaxErrorException`, 컬럼 not found

**확인:**
```bash
# H2 테스트 DB는 자동 생성이므로 문제 없음
# MySQL은 ddl-auto: update이므로 새 컬럼은 추가되지만 리네이밍은 안 됨
```

**원인 & 해결:**
- 컬럼명 변경 → 마이그레이션 SQL 필요 (`/db-migration` 스킬 사용)
- 테이블명 변경 → `ALTER TABLE RENAME` 필요
- FK 제약조건 → 자식 테이블 데이터 먼저 정리

## 실행 순서 체크리스트

문제가 복합적일 때, 전체 스택을 순서대로 점검한다:

1. [ ] Docker MySQL 실행 (`docker-compose up -d`)
2. [ ] MySQL 접속 확인 (`docker exec -it llm-db mysql -u llm_admin -p`)
3. [ ] Ollama 서버 실행 (`ollama serve`)
4. [ ] Ollama 모델 확인 (`ollama list` → `qwen2.5:7b`, `nomic-embed-text`)
5. [ ] Python 가상환경 활성화 + 서버 시작 (`uvicorn app:app --port 8000`)
6. [ ] Python 헬스체크 (`curl http://localhost:8000/health`)
7. [ ] Spring Boot 실행 (`./gradlew bootRun`)
8. [ ] 프론트엔드 접속 (`http://localhost:8080`)

## 참고 문서

- `doc/TROUBLESHOOTING.md` — 기존 트러블슈팅 이력 (확인 후 중복 방지)
- `doc/SETUP_OLLAMA.md` — Ollama 설치/연동 상세
- 새로운 이슈 해결 시 `doc/TROUBLESHOOTING.md`에 추가한다
