---
name: ubuntu1-deploy
description: "ubuntu1 배포/재배포/롤아웃, second-brain 이미지 빌드·compose up·마이그레이션 배포를 할 때 사용. rsync 경로·이미지 태그·실행 이미지 ID 대조·백업까지 체크리스트로 강제한다."
scope: package
user-invocable: true
---

## 언제 쓰나

- "ubuntu1에 배포해줘" / "재빌드해줘" / "롤아웃해줘" 같은 요청
- second-brain 이미지(server/collector/mcp/web) 빌드 후 ubuntu1 compose 스택 갱신
- 마이그레이션 파일 추가 후 배포 (자동 적용됨 — 아래 5번 참고)

**핵심 전제**: `ubuntu1:~/second-brain-app`는 git 리포가 아니라 로컬 리포의 rsync 사본이다. 로컬에서 커밋해도 ubuntu1에는 반영되지 않는다 — 반드시 rsync로 밀어야 한다. compose에는 `build:` 섹션이 없어 이미지 태그만 참조하므로, 로컬에서 빌드한 이미지를 올리는 게 아니라 **ubuntu1 서버 위에서 직접 빌드**한다.

## 사전점검 체크리스트 (착수 전)

- [ ] 이번 배포가 데이터 변형 마이그레이션을 포함하는가? → 포함하면 4번(백업) 필수
- [ ] `ssh ubuntu1 'bash -l -s'` 로그인 셸로 접속 가능한가 (로그인 셸 없으면 PATH/env 깨짐)
- [ ] 로컬 macOS rsync는 openrsync다 — `-az`(+웹은 `-R`)만 쓸 것, rsync 3.x 전용 옵션(`--info=stats2` 등)은 0바이트 실패 유발
- [ ] Go 변경과 웹 변경을 **같은 rsync 명령에 섞지 않는다** (경로 평탄화 사고 재발 방지, 사고 사례 2 참고)
- [ ] `ubuntu1:~/second-brain-app/docker-compose.ubuntu1.yml`은 리포의 `deploy/ubuntu1-stack/docker-compose.yml`과 **별도 관리** — compose 변경이 있으면 ubuntu1 쪽도 수동 갱신
- [ ] 빌드 태그가 compose가 참조하는 이름과 정확히 일치하는지 사전 확인 (`second-brain-<svc>:ubuntu1`)
- [ ] 개인데이터(SMS·통화·메일 본문, API 키) 출력 금지 — 검증은 집계·개수·해시로만

## 단계별 명령

### 1. Go 소스 전송

```bash
rsync -az --exclude '.git' cmd internal migrations go.mod go.sum Dockerfile FOR-AGENTS.md ubuntu1:~/second-brain-app/
```

### 2. 웹 소스 전송 (Go와 분리된 명령, 반드시 `-R`)

```bash
rsync -azR --exclude node_modules --exclude .next \
  web/src web/package.json web/bun.lock web/next.config.ts web/tsconfig.json web/Dockerfile \
  ubuntu1:~/second-brain-app/
```

전송 직후 메인 Dockerfile이 덮이지 않았는지 확인:

```bash
ssh ubuntu1 "grep -cE '^FROM .* AS (server|collector|mcp)' ~/second-brain-app/Dockerfile"
# 결과가 3이 아니면 즉시 중단 — web/Dockerfile이 메인 Dockerfile을 덮어썼을 가능성 (사고 사례 2)
```

### 3. 이미지 빌드 (ubuntu1 위에서 — compose에 build: 섹션 없음, 직접 빌드)

```bash
ssh ubuntu1 'bash -l -s' <<'EOF'
cd ~/second-brain-app
docker build --target server -t second-brain-server:ubuntu1 .
docker build --target collector -t second-brain-collector:ubuntu1 .
docker build --target mcp -t second-brain-mcp:ubuntu1 .
docker build -f web/Dockerfile -t second-brain-web:ubuntu1 web/
EOF
```

태그는 `deploy/ubuntu1-stack/docker-compose.yml`(및 ubuntu1의 `docker-compose.ubuntu1.yml`)이 참조하는 이름과 **한 글자도 다르면 안 된다**. 다른 태그로 빌드하면 `up -d`가 옛 이미지를 그대로 재시작하고도 정상처럼 보인다 (사고 사례 1).

### 4. (데이터 변형 마이그레이션이 있을 때만) 배포 전 백업

```bash
ssh ubuntu1 'bash -l -s' <<'EOF'
mkdir -p ~/backups
docker exec second-brain-postgres sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -t documents -t chunks -Fc' \
  > ~/backups/pre-<마이그레이션번호>-$(date +%Y%m%d-%H%M).dump
EOF
```

사후 대조를 위해 배포 전 집계 SQL(예: `SELECT count(*), source_type FROM documents GROUP BY source_type`) 결과도 같이 남겨둔다.

### 5. 기동

```bash
ssh ubuntu1 'bash -l -s' <<'EOF'
cd ~/second-brain-app
docker compose --env-file .env.local -f docker-compose.ubuntu1.yml up -d <서비스...>
EOF
```

`--env-file`을 빠뜨리면 환경변수가 비어 들어간다. 마이그레이션은 server 기동 시 `RunMigrations`가 자동 실행한다 — **추적 테이블이 없어 매 부팅마다 전체 재실행**되므로 마이그레이션 SQL은 반드시 멱등해야 한다.

## 검증 체크리스트 (헬스체크로 대체 불가)

**1순위 — 이미지 ID 대조 (다른 모든 검증보다 먼저 실행)**

```bash
ssh ubuntu1 'bash -l -s' <<'EOF'
for svc in server collector mcp web; do
  running=$(docker inspect -f '{{.Image}}' second-brain-ubuntu1-${svc}-1)
  built=$(docker images -q second-brain-${svc}:ubuntu1)
  echo "${svc}: running=${running} built=${built}"
done
EOF
```

`running`과 `built`가 다르면 배포 실패다. `up -d` 출력에 `Recreated`가 없고 `Starting`/`Started`만 있었다면 이 신호다. 헬스체크·엔드포인트 200 응답은 옛 이미지도 통과하므로 증거로 인정하지 않는다.

- [ ] 이미지 ID 일치 (위 명령)
- [ ] `~/bin/verify-mounts.sh; echo exit=$?` → exit=0
- [ ] server 로그에 `migration applied` / `server listening`
- [ ] 워커·수집기 로그에 첫 tick 확인
- [ ] API 스모크 테스트 (응답 본문은 화면에 출력하지 말고 상태 코드·결과 건수만 확인)

`q` 없는 `/api/v1/search`는 `search.ValidateQueryInput`이 400으로 거부해 스모크로 쓸 수 없다(#285). 무해한 단어를 넣어 200과 결과 건수만 본다.

```bash
ssh ubuntu1 'bash -l -s' <<'EOF'
cd ~/second-brain-app
AUTH="Authorization: Bearer $(grep '^API_KEY=' .env.local | cut -d= -f2-)"
curl -s -H "$AUTH" \
  'http://127.0.0.1:8081/api/v1/search?q=%ED%9A%8C%EC%9D%98&limit=1' \
  | python3 -c 'import json,sys; d=json.load(sys.stdin); print("count:", d.get("count"))'
EOF
```

- [ ] (선택) v0.25.1 입력 검증 확인 — NUL 바이트가 400인지 (`search.ValidateQueryInput`, #282)

```bash
ssh ubuntu1 'bash -l -s' <<'EOF'
cd ~/second-brain-app
AUTH="Authorization: Bearer $(grep '^API_KEY=' .env.local | cut -d= -f2-)"
curl -s -o /dev/null -w '%{http_code}\n' -H "$AUTH" \
  'http://127.0.0.1:8081/api/v1/search?q=a%00b&limit=1'
EOF
```

기대값: `400`. 다른 값이면 v0.25.1 입력 검증이 배포 이미지에 없다는 뜻이다.

- [ ] (선택, **이미지 ID 대조가 MATCH일 때만 실행**) GraphQL 순환 fragment 400 확인 (#282)

> **경고**: 이 요청은 `graphql-go` 검증기의 무한 재귀 버그(순환 fragment에서 스택 오버플로 → 복구 불가 → 프로세스 종료)를 건드린다. v0.25.1 이전 이미지(AST 가드 미적용)에 보내면 **서버 프로세스가 죽는다**. 위 "1순위 — 이미지 ID 대조"가 MATCH임을 먼저 확인한 뒤에만 실행할 것.

```bash
ssh ubuntu1 'bash -l -s' <<'EOF'
cd ~/second-brain-app
AUTH="Authorization: Bearer $(grep '^API_KEY=' .env.local | cut -d= -f2-)"
curl -s -o /dev/null -w '%{http_code}\n' -H "$AUTH" -H 'Content-Type: application/json' \
  -d '{"query":"query { ...A } fragment A on Query { ...B } fragment B on Query { ...A }"}' \
  'http://127.0.0.1:8081/api/v1/graphql'
EOF
```

기대값: `400`(AST 가드가 실행 전에 거부). 요청이 멈추거나 응답이 없으면 즉시 컨테이너 상태(`docker ps`)를 확인할 것 — 프로세스가 죽었을 수 있다.

- [ ] (백업했다면) 배포 후 집계가 사전 집계와 기대한 방향으로만 달라졌는지 대조

## 사고 사례 (2026-09-19 야간, 같은 절차 5회 반복 중 발생)

### 사고 1 — 태그 오기로 옛 이미지 재시작을 "배포 완료"로 오보

`docker build -t second-brain-ubuntu1-server:latest .`처럼 compose가 참조하지 않는 이름으로 빌드 → `up -d`가 옛 이미지를 그대로 재시작 → 헬스체크·엔드포인트가 정상 응답해 배포 완료로 보고. 실제로는 골든셋 폴백·분류 큐 수정 2건이 미배포 상태였다.

**신호**: `up -d` 출력에 `Recreated` 없이 `Starting`/`Started`만 있음.
**방어**: 검증 1순위(이미지 ID 대조)를 항상 먼저 실행.

### 사고 2 — rsync 경로 평탄화로 메인 Dockerfile 덮어쓰기

`rsync -az cmd internal ... web/src web/Dockerfile ubuntu1:~/second-brain-app/`처럼 Go와 웹 파일을 한 명령에 섞어 상대경로(`-R`) 없이 전송 → 마지막 경로 요소만 남아 `web/Dockerfile`이 루트의 메인 Dockerfile을 덮어쓰고 `web/src`가 루트 `src/`로 흩어짐 → 빌드 시 `target stage "server" could not be found`.

**신호**: 빌드 에러 `target stage "X" could not be found`, 또는 루트에 낯선 `src/` 디렉토리 생성.
**방어**: Go/웹 rsync 명령을 분리하고 웹은 반드시 `-R`, 전송 후 `grep -cE '^FROM .* AS (server|collector|mcp)' Dockerfile`이 3인지 확인.

## 롤백

**이미지 문제 (사고 1 유형)**: 직전 정상 배포 시점의 이미지가 로컬(ubuntu1)에 남아있다면 재태깅 후 재기동.

```bash
ssh ubuntu1 'bash -l -s' <<'EOF'
docker tag second-brain-server:ubuntu1 second-brain-server:ubuntu1-broken   # 실패한 이미지 보관
docker tag <이전_정상_이미지_ID> second-brain-server:ubuntu1
cd ~/second-brain-app && docker compose --env-file .env.local -f docker-compose.ubuntu1.yml up -d server
EOF
```

이전 이미지가 이미 삭제됐다면 로컬 리포에서 배포 직전 커밋으로 되돌려 1~3단계를 다시 수행한다.

**데이터 문제 (마이그레이션 부작용)**: 4단계에서 만든 덤프로 복원. 복원 전 사전 집계와 현재 상태를 비교해 실제로 롤백이 필요한 사고인지(예상된 변화가 아닌지) 먼저 확인한다.

```bash
ssh ubuntu1 'bash -l -s' <<'EOF'
docker compose --env-file .env.local -f docker-compose.ubuntu1.yml stop server collector mcp
docker exec -i second-brain-postgres pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" --clean --if-exists < ~/backups/pre-<번호>-<타임스탬프>.dump
docker compose --env-file .env.local -f docker-compose.ubuntu1.yml up -d
EOF
```
