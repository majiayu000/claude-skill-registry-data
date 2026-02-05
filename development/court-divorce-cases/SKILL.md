---
name: court-divorce-cases
description: 법제처 국가법령정보 API를 통해 이혼 판례를 검색하고 다운로드합니다.
---

# 판례 검색 및 다운로드 스킬

## 목적

법제처 국가법령정보 Open API를 사용하여 이혼 관련 판례를 검색하고 다운로드합니다.

## 사용 시점

다음과 같은 작업을 할 때 사용됩니다:
- 이혼 판례 검색
- 판례 상세 내용 다운로드
- Markdown 파일로 저장

---

## 주요 기능

법제처 Open API를 통한:
- 판례 키워드 검색
- 판례 상세 내용 조회
- Markdown 형식 자동 저장

---

## API 정보

### 법제처 국가법령정보 Open API
- **URL**: https://open.law.go.kr
- **제공 기관**: 법제처
- **데이터**: 대한민국 각급 법원 판례 전문
- **인증**: Open API 키 필요 (무료)

---

## API 인증키 발급

### 1. 국가법령정보 공동활용 회원가입

**절차**:
1. https://open.law.go.kr 접속
2. 회원가입 (무료)
3. 로그인 후 "OPEN API" 메뉴 선택
4. API 키 신청 (자동 승인)
5. 발급된 API 키 확인

**특징**:
- 무료 제공
- 즉시 발급
- XML 형식 응답
- 검색 조건: 판례 분류, 키워드, 사건번호 등

### 2. 법제처 판례 검색 API (권장) ✅

**절차**:
1. https://open.law.go.kr 접속
2. 회원가입 및 로그인
3. "OPEN API" 메뉴에서 API 키 확인
4. 이메일 ID의 @ 앞부분을 OC 파라미터로 사용 (예: g4c@korea.kr → OC=g4c)

**API 정보**:
- **요청주소**: `http://www.law.go.kr/DRF/lawSearch.do`
- **검색 대상**: 판례 (precedent)
- **승인**: 회원가입 시 자동 발급
- **출력 형식**: **XML** (권장, 실제 작동 확인됨), JSON (빈 결과 반환), HTML

**요청 파라미터**:
- `OC`: 사용자 이메일 ID의 @ 앞부분 (필수, 예: nfbs2000@gmail.com → nfbs2000)
- `target`: `prec` (판례 검색, 필수)
- `type`: `XML` (필수, **JSON은 작동하지 않음**)
- `query`: 검색어 (예: "이혼", "유책배우자")
- `search`: 검색 범위 (1=판례명, 2=전문 검색, **기본값: 2 권장**)
- `display`: 결과 개수 (최대 100, 기본값: 20)
- `page`: 페이지 번호 (기본값: 1)
- `org`: 법원 유형 (400201=대법원, 400202=하급심)
- `curt`: 법원명
- `sort`: 정렬 (lasc, ldes, dasc, ddes, nasc, ndes, 기본값: ddes)
- `prncYd`: 선고일자 범위 (예: 20200101~20241231)
- `nb`: 사건번호

**중요 사전 준비**:
1. https://open.law.go.kr 회원가입
2. [OPEN API] → [OPEN API 신청] 메뉴
3. **"판례" 항목 체크** (필수! 체크하지 않으면 "미신청된 목록/본문" 에러 발생)
4. 저장 후 즉시 사용 가능

**응답 필드**:
- `prec`: 판례 정보
  - `판례일련번호`: 고유 ID
  - `판례명`: 사건명
  - `사건번호`: 법원 사건번호
  - `선고일자`: 판결 날짜
  - `법원명`: 판결 법원
  - `법원종류코드`: 법원 유형 코드
  - `사건종류명`: 사건 유형
  - `판결유형`: 판결 종류
  - `판례상세링크`: 상세 페이지 URL

**예시 요청**:
```
http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=prec&type=XML&query=이혼&search=2&display=100
```

**Python 예제 (법제처 판례 검색 API)**:
```python
def search_precedents(oc: str, keyword: str = "이혼", search_type: int = 2, display: int = 100):
    """
    법제처 판례 검색 API로 판례 검색

    Args:
        oc: 사용자 이메일 ID (@ 앞부분)
        keyword: 검색 키워드
        search_type: 1=판례명, 2=전문 검색
        display: 결과 개수 (최대 100)
    """
    base_url = "http://www.law.go.kr/DRF/lawSearch.do"

    params = {
        'OC': oc,
        'target': 'prec',      # 판례 검색
        'type': 'XML',
        'query': keyword,
        'search': search_type,
        'display': display,
        'page': 1
    }

    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        raise Exception(f"API 호출 실패: {response.status_code}")

    # XML 파싱
    root = ET.fromstring(response.content)

    # 결과 추출
    cases = []
    for item in root.findall('.//prec'):
        case = {
            '판례일련번호': item.findtext('판례일련번호', ''),
            '판례명': item.findtext('판례명', ''),
            '사건번호': item.findtext('사건번호', ''),
            '선고일자': item.findtext('선고일자', ''),
            '법원명': item.findtext('법원명', ''),
            '법원종류코드': item.findtext('법원종류코드', ''),
            '사건종류명': item.findtext('사건종류명', ''),
            '판결유형': item.findtext('판결유형', ''),
            '판례상세링크': item.findtext('판례상세링크', '')
        }
        cases.append(case)

    return pd.DataFrame(cases)
```


---

## 이혼 판례 검색 API 사용법

### 1. 판례 목록 조회 (검색)

**API 엔드포인트**:
```
http://www.law.go.kr/DRF/lawSearch.do
```

**Python 예제**:
```python
import requests
import xml.etree.ElementTree as ET
import pandas as pd
from typing import List, Dict

def search_divorce_cases(api_key: str, keyword: str = "유책배우자", display: int = 100):
    """
    이혼 판례 검색

    Args:
        api_key: 국가법령정보 API 키
        keyword: 검색 키워드 (예: "유책배우자", "이혼 사유")
        display: 한 페이지당 결과 수 (최대 100)

    Returns:
        판례 목록 데이터프레임
    """

    base_url = "http://www.law.go.kr/DRF/lawSearch.do"

    params = {
        'OC': api_key,           # API 키
        'target': 'prec',        # 판례 검색
        'type': 'XML',           # XML 형식
        'query': keyword,        # 검색어
        'display': display,      # 결과 수
        'page': 1                # 페이지 번호
    }

    # API 호출
    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        raise Exception(f"API 호출 실패: {response.status_code}")

    # XML 파싱
    root = ET.fromstring(response.content)

    # 판례 목록 추출
    cases = []
    for prec in root.findall('.//PrecService'):
        case = {
            '판례일련번호': prec.findtext('판례일련번호', ''),
            '사건번호': prec.findtext('사건번호', ''),
            '사건명': prec.findtext('사건명', ''),
            '선고일자': prec.findtext('선고일자', ''),
            '법원명': prec.findtext('법원명', ''),
            '사건종류명': prec.findtext('사건종류명', ''),
            '판시사항': prec.findtext('판시사항', ''),
            '판결요지': prec.findtext('판결요지', ''),
            '참조조문': prec.findtext('참조조문', ''),
            '참조판례': prec.findtext('참조판례', '')
        }
        cases.append(case)

    df = pd.DataFrame(cases)

    print(f"검색 결과: {len(df)}건")
    return df

# 사용 예제
api_key = "YOUR_API_KEY_HERE"
divorce_cases = search_divorce_cases(api_key, keyword="유책배우자 이혼")

# CSV 저장
divorce_cases.to_csv('divorce_cases.csv', index=False, encoding='utf-8-sig')
```

### 2. 판례 본문 조회 (상세 내용)

**API 엔드포인트**:
```
http://www.law.go.kr/DRF/lawService.do
```

**요청 파라미터**:
- `OC`: 사용자 이메일 ID (@ 앞부분)
- `target`: `prec` (판례, 필수)
- `type`: `XML` (권장), `HTML`, `JSON`
- `ID`: 판례일련번호 (필수)
- `mobileYn`: `Y` (모바일 최적화, 선택)

**Python 예제**:
```python
import xml.etree.ElementTree as ET
import requests
from pathlib import Path

def get_case_detail(oc_id: str, case_serial_no: str):
    """
    특정 판례의 전문(full text) 조회

    Args:
        oc_id: 사용자 이메일 ID (@ 앞부분)
        case_serial_no: 판례일련번호

    Returns:
        판례 전문 내용
    """

    base_url = "http://www.law.go.kr/DRF/lawService.do"

    params = {
        'OC': oc_id,
        'target': 'prec',
        'type': 'XML',
        'ID': case_serial_no,
        'mobileYn': ''
    }

    response = requests.get(base_url, params=params)
    response.raise_for_status()

    root = ET.fromstring(response.content)

    # 판례 상세 정보 추출
    detail = {
        '판례일련번호': case_serial_no,
        '사건번호': root.findtext('.//사건번호', ''),
        '사건명': root.findtext('.//사건명', ''),
        '선고일자': root.findtext('.//선고일자', ''),
        '법원명': root.findtext('.//법원명', ''),
        '사건종류명': root.findtext('.//사건종류명', ''),
        '판시사항': root.findtext('.//판시사항', ''),
        '판결요지': root.findtext('.//판결요지', ''),
        '참조조문': root.findtext('.//참조조문', ''),
        '참조판례': root.findtext('.//참조판례', ''),
        '전문내용': root.findtext('.//전문내용', ''),
        '판례내용': root.findtext('.//판례내용', '')
    }

    return detail


def save_case_to_file(detail: dict, output_dir: str):
    """
    판례 상세 내용을 개별 파일로 저장

    Args:
        detail: 판례 상세 정보 딕셔너리
        output_dir: 출력 디렉토리
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 파일명: {판례일련번호}_{사건번호}.md
    case_id = detail['판례일련번호']
    case_no = detail['사건번호'].replace('/', '_')
    filename = f"{case_id}_{case_no}.md"

    filepath = output_path / filename

    # Markdown 형식으로 저장
    content = f"""# {detail['사건명']}

## 기본 정보
- **판례일련번호**: {detail['판례일련번호']}
- **사건번호**: {detail['사건번호']}
- **선고일자**: {detail['선고일자']}
- **법원명**: {detail['법원명']}
- **사건종류**: {detail['사건종류명']}

## 판시사항
{detail['판시사항']}

## 판결요지
{detail['판결요지']}

## 참조조문
{detail['참조조문']}

## 참조판례
{detail['참조판례']}

## 전문내용
{detail['전문내용'] or detail['판례내용']}
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ 저장 완료: {filename}")
    return filepath


# 사용 예제
oc_id = "nfbs2000"
case_detail = get_case_detail(oc_id, case_serial_no="609501")
save_case_to_file(case_detail, "/path/to/output/dir")
```

---

## 환경 변수 설정

### .env 파일

```bash
# 법제처 판례 검색 API
# 이메일 ID의 @ 앞부분 (예: g4c@korea.kr → g4c)
LAW_OC_ID=your_email_id_before_at
```

---

## 주요 검색 키워드

### 유책배우자 관련
- "유책배우자"
- "유책배우자 이혼 청구"
- "부정행위"
- "간통"
- "악의적 유기"

### 이혼 사유 관련
- "이혼 사유"
- "혼인 계속 곤란 사유"
- "배우자 학대"
- "가정폭력"
- "성격차이"

### 법원별 검색
- "대법원 이혼"
- "가정법원 이혼"
- "고등법원 이혼"

---

## 참고 링크

### 공식 API
- **국가법령정보 Open API**: https://open.law.go.kr/LSO/openApi/guideList.do
- **공공데이터포털 판례 API**: https://www.data.go.kr/data/15057123/openapi.do
- **판례 목록 조회 가이드**: https://open.law.go.kr/LSO/openApi/guideResult.do?htmlName=precListGuide
- **판례 본문 조회 가이드**: https://open.law.go.kr/LSO/openApi/guideResult.do?htmlName=precInfoGuide

### 판례 검색 포털
- **대법원 판례 검색**: https://glaw.scourt.go.kr/wsjo/panre/sjo050.do
- **사법정보공개포털**: https://portal.scourt.go.kr/pgp/index.on?m=PGP1011M01
- **빅케이스**: https://bigcase.ai/
- **LBOX**: https://lbox.kr/

---

## 베스트 프랙티스

### ✅ DO (권장)

- **API 키 보안**: 환경 변수 사용, 코드에 하드코딩 금지
- **점진적 다운로드**: 대량 판례는 페이지 단위로 분할 다운로드
- **오류 처리**: XML 파싱 실패, API 오류 대비 try-except 구현
- **캐싱**: 이미 다운로드한 판례 중복 방지
- **AI 분석 검증**: Gemini 분석 결과를 법률 전문가가 검토
- **개인정보 보호**: 당사자 이름 등 개인정보 마스킹 처리

### ❌ DON'T (비권장)

- API 키를 코드에 직접 작성
- 대량 판례 한 번에 다운로드 (서버 부하)
- XML 파싱 오류 무시
- AI 분석만으로 법적 판단
- 판례 내용 무단 재배포
- 상업적 목적 무단 사용

---

## 법적 고지

**주의사항**:
- 본 스킬은 **교육 및 연구 목적**으로만 사용해야 합니다
- 판례 분석 결과는 **참고용**이며, 법적 효력이 없습니다
- 실제 법률 문제는 **변호사와 상담**하세요
- 판례 데이터의 저작권은 **법제처 및 법원**에 있습니다
- API 이용약관을 준수하세요

---

**스킬 상태**: 완료 ✅
**줄 수**: 500줄 미만 ✅
**베스트 프랙티스**: Anthropic 가이드라인 준수 ✅
