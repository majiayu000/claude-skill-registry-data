---
name: mongodb-queries
description: "ICJC MongoDB 데이터베이스 접근 및 쿼리. Use when: (1) mongodb, mongo, DB, 데이터베이스, 쿼리 관련 요청, (2) collection, document 조회/업데이트/삭제, (3) 데이터 확인이나 디버깅을 위한 DB 조회 필요시. IN7DB(메인앱), AgentDB(에이전트) 데이터베이스 지원."
---

# MongoDB Queries Skill

ICJC 프로젝트의 MongoDB 데이터베이스 접근 및 쿼리를 위한 스킬입니다.

<trigger_conditions>
## 사용 시점

다음 키워드나 상황에서 이 스킬을 사용하세요:
- "mongodb", "mongo", "DB", "데이터베이스", "쿼리"
- "collection", "document", "조회", "업데이트", "삭제"
- 데이터 확인, 디버깅을 위한 DB 조회가 필요할 때
</trigger_conditions>

<database_schema>
## 데이터베이스 구조

### IN7DB (메인 애플리케이션) - 주요 컬렉션
| Collection | 설명 |
|------------|------|
| users | 사용자 (email, name, is_active) |
| orgs | 조직 |
| teams | 팀 |
| team_members | 팀 멤버십 |
| subscriptions | 구독 |
| subscription_plans | 구독 플랜 |
| subscription_plan_templates | 구독 플랜 템플릿 |
| billing_events | 결제 이벤트 |
| payments | 결제 |
| invoices | 청구서 |
| org_promotions | 조직 프로모션 |
| promotion_templates | 프로모션 템플릿 |
| documents | AI Drive 문서 |
| document_chunks | 문서 청크 (벡터) |
| prompts | 프롬프트 |
| prompt_sessions | 프롬프트 세션 |
| prompt_favorites | 즐겨찾기 |
| invitations | 초대 |
| feedbacks | 피드백 |
| feature_flags | 기능 플래그 |
| system_settings | 시스템 설정 |

### AgentDB (Agent 서비스)
| Collection | 설명 |
|------------|------|
| sessions | 채팅 세션 |
| app_states | 앱 상태 |
| user_states | 사용자 상태 |
| projects | 프로젝트 |
| events | 이벤트 로그 |
</database_schema>

<connection>
## 접속 방법

### 컨테이너에서 직접 접속
```bash
# MongoDB 셸 접속
docker exec -it mongodb-primary-dev mongosh

# 특정 DB 접속
docker exec -it mongodb-primary-dev mongosh IN7DB
docker exec -it mongodb-primary-dev mongosh AgentDB
```

### 원라인 쿼리 실행
```bash
# 기본 형식
docker exec mongodb-primary-dev mongosh <DB명> --eval "<쿼리>" --quiet

# 예시
docker exec mongodb-primary-dev mongosh IN7DB --eval "db.users.findOne()" --quiet
```
</connection>

<query_patterns>
## 쿼리 패턴

### 조회 (Read)
```bash
# 단일 문서 조회
docker exec mongodb-primary-dev mongosh IN7DB --eval "db.users.findOne({email: 'test@example.com'})" --quiet

# 여러 문서 조회
docker exec mongodb-primary-dev mongosh IN7DB --eval "db.users.find({is_active: true}).limit(10).toArray()" --quiet

# 특정 필드만 조회
docker exec mongodb-primary-dev mongosh IN7DB --eval "db.users.findOne({email: 'test@example.com'}, {email: 1, name: 1})" --quiet

# 개수 조회
docker exec mongodb-primary-dev mongosh IN7DB --eval "db.users.countDocuments({is_active: true})" --quiet

# Collection 목록
docker exec mongodb-primary-dev mongosh IN7DB --eval "db.getCollectionNames()" --quiet
```

### 수정 (Update)
```bash
# 단일 문서 수정
docker exec mongodb-primary-dev mongosh IN7DB --eval "db.users.updateOne({email: 'test@example.com'}, {\$set: {name: 'New Name'}})" --quiet

# 여러 문서 수정
docker exec mongodb-primary-dev mongosh IN7DB --eval "db.users.updateMany({is_active: false}, {\$set: {is_active: true}})" --quiet
```

### 삭제 (Delete)
```bash
# 단일 문서 삭제
docker exec mongodb-primary-dev mongosh IN7DB --eval "db.users.deleteOne({email: 'test@example.com'})" --quiet

# 여러 문서 삭제
docker exec mongodb-primary-dev mongosh IN7DB --eval "db.users.deleteMany({is_active: false})" --quiet
```

### ObjectId 사용
```bash
# ObjectId로 조회
docker exec mongodb-primary-dev mongosh IN7DB --eval "db.users.findOne({_id: ObjectId('507f1f77bcf86cd799439011')})" --quiet
```

### 날짜 쿼리
```bash
# 특정 날짜 이후
docker exec mongodb-primary-dev mongosh IN7DB --eval "db.billing_events.find({created_at: {\$gte: new Date('2024-01-01')}}).toArray()" --quiet
```

### Aggregation
```bash
# 그룹별 집계
docker exec mongodb-primary-dev mongosh IN7DB --eval "db.billing_events.aggregate([{\$group: {_id: '\$org_id', total: {\$sum: '\$amount'}}}]).toArray()" --quiet
```
</query_patterns>

<common_queries>
## 자주 사용하는 쿼리

### 사용자 관련
```bash
# 이메일로 사용자 찾기
docker exec mongodb-primary-dev mongosh IN7DB --eval "db.users.findOne({email: 'EMAIL'})" --quiet

# 활성 사용자 수
docker exec mongodb-primary-dev mongosh IN7DB --eval "db.users.countDocuments({is_active: true})" --quiet
```

### 조직/팀 관련
```bash
# 조직 정보 조회
docker exec mongodb-primary-dev mongosh IN7DB --eval "db.orgs.findOne({_id: ObjectId('ORG_ID')})" --quiet

# 조직의 팀 목록
docker exec mongodb-primary-dev mongosh IN7DB --eval "db.teams.find({org_id: ObjectId('ORG_ID')}).toArray()" --quiet
```

### 구독/결제 관련
```bash
# 조직 구독 상태
docker exec mongodb-primary-dev mongosh IN7DB --eval "db.subscriptions.findOne({org_id: ObjectId('ORG_ID')})" --quiet

# 최근 결제 이벤트
docker exec mongodb-primary-dev mongosh IN7DB --eval "db.billing_events.find({org_id: ObjectId('ORG_ID')}).sort({created_at: -1}).limit(5).toArray()" --quiet
```

### 프로모션 관련
```bash
# 조직의 프로모션
docker exec mongodb-primary-dev mongosh IN7DB --eval "db.org_promotions.find({org_id: ObjectId('ORG_ID')}).toArray()" --quiet

# 프로모션 템플릿
docker exec mongodb-primary-dev mongosh IN7DB --eval "db.promotion_templates.find().toArray()" --quiet
```

### Agent 세션
```bash
# 사용자의 세션 목록
docker exec mongodb-primary-dev mongosh AgentDB --eval "db.sessions.find({user_id: 'USER_ID'}).sort({created_at: -1}).limit(5).toArray()" --quiet
```
</common_queries>

<debugging_queries>
## 디버깅용 쿼리

### 데이터 존재 확인
```bash
# 특정 필드 존재 여부
docker exec mongodb-primary-dev mongosh IN7DB --eval "db.collection.findOne({field: {\$exists: true}})" --quiet

# null 값 확인
docker exec mongodb-primary-dev mongosh IN7DB --eval "db.collection.find({field: null}).toArray()" --quiet
```

### 스키마 분석
```bash
# 샘플 문서 구조 확인
docker exec mongodb-primary-dev mongosh IN7DB --eval "db.collection.findOne()" --quiet

# 인덱스 확인
docker exec mongodb-primary-dev mongosh IN7DB --eval "db.collection.getIndexes()" --quiet
```
</debugging_queries>

<instructions>
## 이 스킬 사용 시 지침

1. **읽기 작업 우선**: 데이터 수정 전에 반드시 현재 상태를 먼저 조회하세요.
2. **--quiet 플래그 사용**: 출력을 깔끔하게 하려면 `--quiet` 플래그를 사용하세요.
3. **$ 이스케이프**: bash에서 `$`는 `\$`로 이스케이프해야 합니다.
4. **ObjectId 사용**: `_id` 필드는 `ObjectId('...')`로 감싸야 합니다.
5. **수정/삭제 주의**: 프로덕션 데이터 수정 전에 반드시 사용자 확인을 받으세요.
6. **백업 권장**: 중요한 데이터 수정 전에 `make mongo-backup-dev`로 백업하세요.
</instructions>
