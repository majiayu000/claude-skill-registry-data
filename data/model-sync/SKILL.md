---
name: model-sync
description: ML 모델 파일 서버 간 동기화. "모델 동기화", "모델 배포", "rsync 모델", "서버로 전송" 요청 시 활성화됩니다.
---

# Model Sync 스킬

## Overview

ML 모델 파일을 여러 서버 간에 동기화하는 스킬입니다.

**중요**: 이 스킬이 활성화되면 Claude가 자동으로 스크립트를 실행합니다. 사용자가 직접 명령어를 입력할 필요가 없습니다.

**핵심 기능:**
- **서버 동기화**: rsync/scp 기반 모델 파일 전송
- **서버 별칭**: 자주 사용하는 서버 별칭 관리
- **경로 관리**: NFS/로컬 모델 경로 자동 매핑
- **버전 관리**: 네이밍 컨벤션 기반 버전 추적
- **무결성 검증**: 전송 후 체크섬 검증

## Script Location

```
SCRIPT: ./scripts/model-sync.sh
```

Claude는 이 스크립트를 Bash 도구로 직접 실행합니다.

## When to Use

이 스킬은 다음 상황에서 활성화됩니다:

**명시적 요청:**
- "모델 동기화해줘"
- "reaper 서버로 모델 배포해줘"
- "모델 파일 전송해줘"
- "서버 간 동기화"
- "rsync로 모델 복사"

**자동 활성화:**
- 모델 배포 요청 시
- 서버 간 파일 전송 요청 시

## Prerequisites

```bash
# SSH 키 설정 확인
ssh-add -l

# rsync 설치 확인
rsync --version

# 스크립트 실행 권한
chmod +x /path/to/agent-skills/ml/model-sync/scripts/model-sync.sh
```

### 서버 설정

`~/.model-sync.yaml` 파일에 서버 별칭 정의:

```yaml
servers:
  reaper:
    host: reaper.internal
    user: june
    model_base: /nfs/train/langdetector/models
  doomfist:
    host: doomfist.internal
    user: june
    model_base: /nfs/train/sori-lab
  local:
    model_base: ~/workspace/models

naming:
  pattern: "{GPU}_{DATE}_{MODEL}_{VERSION}"
  # 예: RTX3090_N2501_LANGDETECTOR_250715
```

## Workflow

### Claude 실행 절차

**Step 1**: 사용자 요청 분석
- 동기화 방향 파악 (push/pull)
- 소스/타겟 서버 및 경로 확인
- 서버 별칭 매핑 (reaper, doomfist 등)

**Step 2**: 스크립트 실행
```bash
# 스크립트 경로
SCRIPT=./scripts/model-sync.sh

# 서버 목록
$SCRIPT servers

# 로컬 → 서버 동기화
$SCRIPT push <local_path> <server>[:<remote_path>]

# 서버 → 로컬 동기화
$SCRIPT pull <server>:<path> <local_path>

# 동기화 상태 비교
$SCRIPT diff <local_path> <server>

# 원격 모델 목록
$SCRIPT list <server> [--filter <pattern>]
```

**Step 3**: 결과 보고
- 전송된 파일 수 및 크기
- 동기화 성공/실패 여부
- 검증 결과 (--verify 사용 시)

### 명령어 레퍼런스

| 작업 | 명령어 |
|------|--------|
| 서버 목록 | `$SCRIPT servers` |
| 모델 배포 | `$SCRIPT push ./model reaper` |
| 모델 가져오기 | `$SCRIPT pull reaper:model_v1 ./` |
| 변경사항 확인 | `$SCRIPT diff ./model reaper` |
| 원격 모델 목록 | `$SCRIPT list reaper` |
| 원격 명령 실행 | `$SCRIPT exec reaper "df -h"` |

### 자주 사용하는 명령

| 용도 | 명령어 |
|------|--------|
| 모델 배포 | `model-sync.sh push ./model reaper` |
| 모델 가져오기 | `model-sync.sh pull reaper:model_v1 ./` |
| 변경사항 확인 | `model-sync.sh diff ./model reaper` |
| 원격 모델 목록 | `model-sync.sh list reaper` |

---

## Examples

### 예시 1: 모델 서버로 배포

```
사용자: langdetector 모델을 reaper로 동기화해줘

Claude: 모델을 reaper 서버로 동기화합니다.

$ model-sync.sh push ./langdetector-v1 reaper

Syncing to reaper (reaper.internal)...
Source: ./langdetector-v1
Target: reaper:/nfs/train/langdetector/models/langdetector-v1

## Transfer Progress

sending incremental file list
config.pbtxt
1/model.onnx
1/model.plan

## Result

| Metric | Value |
|--------|-------|
| Files | 5 |
| Size | 156MB |
| Time | 12.3s |
| Speed | 12.7MB/s |

Sync complete
```

### 예시 2: 원격 모델 가져오기

```
사용자: doomfist에서 최신 ASR 모델 가져와줘

Claude: doomfist에서 모델을 가져옵니다.

$ model-sync.sh list doomfist --filter asr
$ model-sync.sh pull doomfist:RTX3090_N2501_ASR_250820 ./models/

## Available Models (doomfist)

| Model | Size | Modified |
|-------|------|----------|
| RTX3090_N2501_ASR_250820 | 2.1GB | 2025-08-20 |
| RTX3090_N2501_ASR_250715 | 2.0GB | 2025-07-15 |

Pulling: RTX3090_N2501_ASR_250820

## Result

| Metric | Value |
|--------|-------|
| Files | 12 |
| Size | 2.1GB |
| Time | 2m 15s |
| Verified | yes |
```

### 예시 3: 변경사항 확인

```
사용자: 로컬과 서버 모델 차이 확인해줘

Claude: 동기화 상태를 확인합니다.

$ model-sync.sh diff ./langdetector reaper

## Sync Status: langdetector

| File | Local | Remote | Status |
|------|-------|--------|--------|
| config.pbtxt | 2.1KB | 2.1KB | same |
| 1/model.onnx | 45MB | 45MB | same |
| 1/model.plan | 112MB | - | new |

Summary:
- Same: 2 files
- New (local): 1 file
- Modified: 0 files

Run 'model-sync.sh push ./langdetector reaper' to sync
```

### 예시 4: 모델 목록 조회

```
사용자: reaper에 있는 모델 목록 보여줘

Claude: reaper 서버의 모델 목록을 조회합니다.

$ model-sync.sh list reaper

## Models on reaper

| Model | Size | Modified |
|-------|------|----------|
| RTX3090_N2501_LANGDETECTOR_250715 | 156MB | 2025-07-15 |
| RTX3090_N2501_LANGDETECTOR_MMS_251030 | 89MB | 2025-10-30 |
| RTX3090_N2501_FASTCONFORMER_250820 | 2.4GB | 2025-08-20 |

Total: 3 models, 2.6GB
```

---

## Configuration

### 서버 설정 파일

`~/.model-sync.yaml`:

```yaml
servers:
  reaper:
    host: reaper.internal
    user: june
    model_base: /nfs/train/langdetector/models
    ssh_key: ~/.ssh/id_rsa

  doomfist:
    host: doomfist.internal
    user: june
    model_base: /nfs/train/sori-lab

  tracer:
    host: tracer.internal
    user: june
    model_base: /data/models

defaults:
  verify: true
  compress: true
  delete: false  # 원격에서 삭제된 파일 동기화 안 함
```

### rsync 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--compress` | 전송 시 압축 | true |
| `--verify` | 전송 후 체크섬 검증 | true |
| `--delete` | 원격 삭제 파일 동기화 | false |
| `--dry-run` | 실제 전송 없이 미리보기 | false |

---

## Best Practices

**DO:**
- 동기화 전 `diff` 명령으로 변경사항 확인
- 대용량 모델은 `--compress` 옵션 사용
- 중요 모델은 `--verify` 옵션으로 무결성 확인
- 네이밍 컨벤션 준수 (GPU_DATE_MODEL_VERSION)

**DON'T:**
- `--delete` 옵션 무분별하게 사용 (원격 파일 삭제됨)
- 동기화 중 모델 파일 수정
- 네트워크 불안정 시 대용량 전송
- 권한 없는 경로로 동기화 시도

---

## Troubleshooting

### SSH 연결 실패

```bash
# SSH 키 확인
ssh-add -l

# 수동 연결 테스트
ssh reaper.internal

# SSH config 확인
cat ~/.ssh/config
```

### 권한 오류

```bash
# 원격 디렉토리 권한 확인
model-sync.sh exec reaper "ls -la /nfs/train/models"

# 권한 수정
model-sync.sh exec reaper "chmod -R 755 /path/to/model"
```

### 전송 중단/재개

```bash
# 부분 전송 재개 (rsync 기본 지원)
model-sync.sh push ./large_model reaper --resume
```

### 디스크 공간 부족

```bash
# 원격 디스크 확인
model-sync.sh exec reaper "df -h /nfs/train"
```

---

## Resources

| 파일 | 설명 |
|------|------|
| `scripts/model-sync.sh` | 모델 동기화 통합 스크립트 |
| `~/.model-sync.yaml` | 서버 설정 파일 (사용자 정의) |
