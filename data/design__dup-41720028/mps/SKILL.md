---
name: mps
description: MPS(Media Processing Suite) - PDF 및 이미지(PNG, JPG)의 워터마크 제거, 블로그 최적화(1200px, WebP/JPEG). PNG 10MB 자동 압축으로 네이버 블로그 한도 준수. PDF는 DPI 자동 계산으로 메모리 절약. 여러 이미지 합치기 지원. 한글 깨짐 및 맞춤법 자동 체크. 로고 삽입은 선택사항(기본 비활성화). 올인원 미디어 처리 스킬.
---

# MPS (Media Processing Suite)

## ⚠️ CLAUDE 처리 지침 (최우선)

### 🚫 로고 삽입 기본 규칙
**기본 동작: 로고 삽입 비활성화**
- PNG/JPG/PDF 처리 시 **로고를 삽입하지 않음**
- 사용자가 명시적으로 "로고 넣어줘", "로고 삽입" 등을 요청할 때만 로고 사용
- 스크립트 호출 시: `logo_path="none"` 또는 로고 매개변수 생략

### ✅ 처리 방법
**1. 단일 PNG/JPG 파일:**
```python
# 워터마크만 제거 (기본)
python /mnt/skills/user/mps/scripts/remove_watermark.py input.png

# 로고 필요시 (사용자가 명시적으로 요청한 경우만)
python /mnt/skills/user/mps/scripts/remove_watermark.py input.png favicon output.png
```

**2. PDF 파일:**
```python
# 워터마크만 제거 (기본)
python /mnt/skills/user/mps/scripts/pdf_smart.py input.pdf none output/ true 1200 webp

# 로고 필요시 (사용자가 명시적으로 요청한 경우만)
python /mnt/skills/user/mps/scripts/pdf_smart.py input.pdf logo.png output/ true 1200 webp
```

**3. 여러 PNG 합치기:**
```python
# 로고 삽입 기능 없음 (원래부터)
python /mnt/skills/user/mps/scripts/merge_png.py dir/ output.png
```

### 📋 사용자 응답 템플릿
사용자가 이미지 업로드 시:
```
워터마크를 제거하겠습니다.
블로그용으로 최적화하시겠습니까?

💡 로고 삽입이 필요하시면 말씀해주세요 (기본: 비활성화)
```

## 🎯 핵심 기능

### 1. PDF 처리 (스마트 모드)
- DPI 자동 계산 (메모리 1.9배 절약)
- 워터마크 제거
- 로고 삽입 (선택사항, 기본 비활성화)
- 블로그 최적화 (1200px, WebP/JPEG)
- 페이지 통합 또는 개별 출력
- **PNG 10MB 자동 압축** ⭐ 네이버 블로그 한도

### 2. 이미지 처리 (고속 모드)
- PNG/JPG 워터마크 제거
- 로고 스마트 배치 (선택사항, 기본 비활성화)
- 배경색 자동 매칭
- 가볍고 빠른 처리
- **PNG 10MB 자동 압축** ⭐ 네이버 블로그 한도

### 3. 공통 기능
- 여러 이미지 한 장으로 합치기
- 블로그 최적화 (용량 90% 감소)
- 한글 깨짐/맞춤법 자동 체크
- WebP/JPEG 동시 생성
- **PNG 10MB 자동 압축** ⭐ 네이버 블로그 한도

## 📊 처리 흐름

### PDF 업로드 시

```
사용자: [PDF 업로드] "블로그용 이미지로 만들어줘"
   ↓
Claude: "PNG로 출력하시겠습니까?
         1. 개별 파일로 나누어 출력
         2. 한 장으로 통합 출력
         
         🎯 자동으로 블로그 최적화됩니다:
         - 목표 너비: 1200px
         - DPI 자동 계산 (메모리 절약)
         - WebP/JPEG 동시 생성"
   ↓
사용자: "한 장으로"
   ↓
결과: 
  - merged_optimized.webp (741 KB) ⭐ 추천
  - merged_optimized.jpg (1.18 MB)
  - merged_optimized.png (9 MB, 원본)
```

### 이미지 업로드 시

```
사용자: [PNG 업로드] "워터마크 제거해줘"
   ↓
Claude: [텍스트 자동 검증]
        "한글 깨짐 체크... ✅ 문제 없음"
   ↓
        "워터마크를 제거하겠습니다.
         블로그용으로 최적화하시겠습니까?
         
         💡 로고 삽입이 필요하시면 말씀해주세요 (기본: 비활성화)"
   ↓
사용자: "예"
   ↓
결과: 
  - output.png (워터마크 제거)
  - output_optimized.webp (741 KB) ⭐
  - output_optimized.jpg (1.18 MB)
```

### 여러 이미지 업로드 시

```
사용자: [3개 PNG 업로드]
   ↓
Claude: "업로드하신 이미지들을 한 장으로 합치시겠습니까?
         
         일반적인 사용 시나리오:
         1. PDF를 개별 PNG로 변환
         2. 원하지 않는 페이지 제외
         3. 선택한 페이지들만 재업로드
         4. 한 장으로 합쳐서 블로그에 사용"
   ↓
사용자: "예"
   ↓
결과: 선택한 페이지가 하나로 합쳐진 최적화 이미지
```

## 🚀 주요 기술

### 1. PNG 10MB 자동 압축 ⭐ NEW

**문제:**
- 네이버 블로그 이미지 업로드 한도: **장당 10MB**
- 고해상도 PDF → PNG 변환 시 종종 10MB 초과

**자동 압축 로직:**
```python
# 1단계: PNG 저장
img.save(output.png, 'PNG')

# 2단계: 10MB 체크
if file_size > 10MB:
    # 방법 1: 1200px로 리사이즈 (아직 안 했다면)
    if width > 1200:
        resize to 1200px
    
    # 방법 2: PNG optimize
    save with optimize=True
    
    # 방법 3: 여전히 10MB 초과 시
    if still > 10MB:
        # JPEG 변환 (품질 85 → 60까지 자동 조정)
        save as JPEG with quality adjustment
        
        print("PNG는 고품질 원본으로 유지됩니다")
        print("JPEG를 블로그 업로드용으로 사용하세요")
```

**결과:**
- ✅ PNG 10MB 이하: 그대로 사용
- ⚠️ PNG 10MB 초과: 
  - PNG: 고품질 원본 유지
  - JPEG: 자동 생성 (블로그 업로드용)

### 2. 스마트 DPI 계산 (PDF 전용)

### 2. 스마트 DPI 계산 (PDF 전용)

**기존 방식:**
```
PDF → 300 DPI (5734px) → 처리 → 1200px로 축소
      ↑ 메모리 낭비!
```

**신규 방식:**
```
PDF → 자동 계산 DPI (159 DPI) → 처리 → 1200px 완성
      ↑ 메모리 1.9배 절약!
```

**DPI 계산 로직:**
```python
# A4 용지 → 1200px 목표
optimal_dpi = 1200 / (210mm / 25.4) × 1.1
= 159 DPI
```

### 3. 배경색 자동 매칭

```python
# 워터마크 주변 100x100px 영역의 평균 색상
sample_region = (x1-100, y1-100, x1-10, y1-10)
background_color = average_rgb(sample_region)
```

### 4. 로고 색상 변환

```python
# 빨간색 유지 (R > 150)
if r > 150 and r > g and r > b:
    keep_original_color()

# 흰색 배경을 이미지 배경색으로 변환
elif r > 200 and g > 200 and b > 200:
    convert_to_background_color()
```

### 5. 블로그 최적화 자동 적용

**최적화 기준 (연구 결과):**
- 파일 크기: 200KB~2MB (권장 500KB)
- 이미지 너비: 1200px
- 포맷: WebP (최고 압축) + JPEG (호환성)
- 로딩 시간: 3초 이내

**결과:**
- WebP: 741 KB (96% 감소) ⭐
- JPEG: 1.18 MB (93.7% 감소)
- PNG: 9 MB (고품질 원본)

## 📦 스크립트 구성

### scripts/pdf_smart.py ⭐ PDF 처리
**기능:**
- DPI 자동 계산
- 워터마크 제거
- 로고 삽입 (선택사항)
- 통일된 크기 크롭
- 블로그 최적화 (WebP/JPEG)

**사용:**
```bash
# 한 장 + WebP (로고 없음)
python scripts/pdf_smart.py input.pdf none output/ true 1200 webp

# 개별 + 모든 포맷 (로고 있음)
python scripts/pdf_smart.py input.pdf logo.png output/ false 1200 all
```

**매개변수:**
- `logo`: 로고 경로 또는 "none" (비활성화)
- `merge`: true=한장, false=개별
- `width`: 목표 너비 (기본 1200)
- `format`: webp, jpeg, png, all

### scripts/remove_watermark.py ⭐ 이미지 처리
**기능:**
- PNG/JPG 워터마크 제거
- 로고 삽입 (선택사항)
- 배경색 자동 매칭

**사용:**
```bash
# 워터마크만 제거 (기본)
python scripts/remove_watermark.py input.png

# 로고와 함께
python scripts/remove_watermark.py input.png favicon output.png
```

**특징:**
- 가볍고 빠름 (PDF 변환 없음)
- 메모리 효율적
- 0.5초 이내 처리
- 로고 기본 비활성화

### scripts/optimize_blog.py - 블로그 최적화
**기능:**
- 기존 PNG/JPG 최적화
- 1200px 너비 조정
- WebP + JPEG 생성

**사용:**
```bash
python scripts/optimize_blog.py input.png output.webp
```

### scripts/merge_png.py - 이미지 합치기
**기능:**
- 여러 PNG를 한 장으로 합치기
- 너비 다르면 자동 중앙 정렬

**사용:**
```bash
# 디렉토리 전체
python scripts/merge_png.py /path/to/images/ output.png

# 특정 파일들
python scripts/merge_png.py file1.png file2.png file3.png output.png
```

## 🎨 처리 결과 비교

### PDF 14페이지 예시

| 방식 | DPI | 크기 | 용량 | 메모리 | 시간 |
|------|-----|------|------|--------|------|
| **기존 (300 DPI)** | 300 | 5734 x 44,800px | 18.88 MB | 💥 높음 | 느림 |
| **신규 (스마트)** | 159 | 1200 x 9,375px | 741 KB | ✅ 낮음 | 빠름 |

### 단일 이미지 (5000 x 3000px)

| 작업 | 시간 | 메모리 | 결과 |
|------|------|--------|------|
| **워터마크 제거** | 0.5초 | 100MB | 5000 x 3000px |
| **블로그 최적화** | 1.0초 | 50MB | 1200 x 720px |
| **합계** | 1.5초 | 100MB | WebP 741KB |

## 💡 사용 시나리오

### 시나리오 1: PDF → 블로그 한 장 이미지
```
1. PDF 업로드
2. "한 장으로 통합" 선택
3. 자동 처리:
   - DPI 159로 변환 (메모리 절약)
   - 워터마크 제거
   - 로고 삽입
   - 1200px로 조정
   - WebP/JPEG 생성
4. 결과: 3개 파일 (WebP, JPEG, PNG)
```

### 시나리오 2: 이미지 워터마크 제거
```
1. PNG/JPG 업로드
2. 자동 텍스트 검증
3. 워터마크 제거 (로고 기본 비활성화)
4. 블로그 최적화 (선택)
5. 필요시 로고 삽입 요청
6. 결과: 최적화된 이미지
```

### 시나리오 3: 선택 페이지만 합치기
```
1. PDF → 개별 PNG 변환 (14개)
2. 원하지 않는 페이지 제외 (7개 선택)
3. 7개 PNG 재업로드
4. "한 장으로 합치기" 선택
5. 결과: 7페이지가 하나로 합쳐진 이미지
```

### 시나리오 4: 여러 이미지 일괄 처리
```
1. 여러 PNG 업로드
2. 각각 워터마크 제거
3. 한 장으로 합치기
4. 블로그 최적화
5. 결과: 통합된 최적화 이미지
```

## 📚 블로그 최적화 기준

### 권장 사항 (연구 기반)
```
✅ 파일 크기: 200KB~500KB (최적)
✅ 최대 크기: 2MB
✅ 이미지 너비: 800~1200px
✅ 해상도: 72 DPI (웹용)
✅ 로딩 시간: 3초 이내
✅ 포맷: WebP (압축) + JPEG (호환)
```

### 근거
- Shopify 권장: 2MB 이하, 500KB 최적
- Google PageSpeed: 이미지 최적화 필수
- 사용자 연구: 3초 초과 시 53% 이탈
- WebP: JPEG 대비 25-35% 용량 감소

### 포맷 비교

| 포맷 | 압축률 | 품질 | 호환성 | 권장 |
|------|--------|------|--------|------|
| **WebP** | 최고 (30% 절약) | 우수 | 최신 브라우저 | ⭐ 1순위 |
| **JPEG** | 좋음 | 우수 | 모든 브라우저 | ✅ 2순위 |
| **PNG** | 없음 | 최고 | 모든 브라우저 | 📦 원본용 |

## 🎯 자동 최적화 트리거

Claude가 자동으로 최적화를 **제안**하는 경우:
- ✅ PDF 업로드 (PNG 출력 선택 시)
- ✅ 파일 크기 2MB 초과
- ✅ 이미지 너비 2000px 초과
- ✅ "블로그", "웹" 키워드 언급

Claude가 자동으로 최적화를 **강력 권장**:
- ⚠️ 파일 크기 5MB 초과
- ⚠️ 로딩 시간 3초 초과 예상

## 🔧 기술 세부사항

### 워터마크 위치

**PDF 처리 (DPI 비율 조정):**
```python
# 300 DPI 기준 450px 였으므로
watermark_width = 450 × (159 / 300) = 238px
```

**이미지 처리 (고정 위치):**
```python
# 우측 하단 (450 x 130px)
x1 = width - 450
y1 = height - 130
x2 = width
y2 = height
```

### 2단계 크기 조정 (PDF 전용)

```
1단계: 최적 DPI로 PDF 변환 (159 DPI → 3039px)
2단계: 목표 너비로 정확히 조정 (3039px → 1200px)
```

## 📝 로고 파일

**기본 위치:**
- `/mnt/user-data/uploads/파비콘_테두리있음.png`
- 스킬 내장: `logo.png`

**요구사항:**
- 포맷: PNG (RGBA)
- 권장 크기: 100x100px 이상
- 빨간색 부분: 유지
- 흰색 배경: 자동 변환

## ⚡ 성능 비교

### PDF 처리 (14페이지)

**메모리 사용량:**
```
기존 300 DPI: ~2.5 GB
신규 159 DPI: ~1.3 GB
절약: 1.9배 ✅
```

**처리 시간:**
```
기존: ~180초 (종종 크래시)
신규: ~60초 (안정적)
개선: 3배 빠름 ✅
```

**파일 용량:**
```
원본 PNG: 18.88 MB
WebP: 741 KB (96% 감소) ⭐
JPEG: 1.18 MB (93.7% 감소) ✅
```

### 이미지 처리 (단일)

**처리 속도:**
```
워터마크 제거: 0.5초
블로그 최적화: 1.0초
합계: 1.5초 ✅
```

**메모리 효율:**
```
단일 이미지: ~100MB
10개 합치기: ~300MB
안정적 ✅
```

## 🚨 주의사항

### WebP 제한
- 최대 크기: 16,383 x 16,383px
- 초과 시: JPEG로 자동 전환

### PNG 제한
- PIL 기본 제한 해제됨
- 매우 큰 이미지도 처리 가능

### 메모리 관리
- PDF: DPI 자동 계산으로 최적화
- 이미지: 가볍고 빠른 처리
- 크래시 위험 최소화

### 워터마크 위치
- NotebookLM 워터마크는 항상 우측 하단
- 다른 위치는 수동 조정 필요

## 📦 출력 파일 위치

모든 결과는 `/mnt/user-data/outputs/`에 저장:
- `merged_optimized.webp` - 웹 최적화
- `merged_optimized.jpg` - 범용 호환
- `merged_optimized.png` - 고품질 원본
- `page_XX.webp/jpg/png` - 개별 페이지
- `output.png` - 워터마크 제거된 원본
- `output_optimized.webp/jpg` - 최적화 버전

## 📚 의존성

### 필수 라이브러리
```bash
pip install pillow numpy pdf2image --break-system-packages
```

### 시스템 요구사항
```bash
# PDF 처리를 위한 poppler 설치
apt-get update && apt-get install -y poppler-utils
```

### 버전
```
Pillow >= 10.0.0
numpy >= 1.24.0
pdf2image >= 1.16.0
```

## 🎉 버전 이력

**v4.2 (로고 기본 비활성화) - 2024-12-13**
- ✅ 로고 삽입 기능 기본값을 비활성화로 변경
- ✅ 워터마크 제거에 집중
- ✅ 필요시 로고 경로를 명시적으로 지정 가능
- ✅ 더 직관적인 사용자 경험

**v4.1 (자동 압축 추가) - 2024-12-08**
- ✅ PNG 10MB 자동 압축 (네이버 블로그 한도)
- ✅ 10MB 초과 시 JPEG 자동 생성
- ✅ 사용자 편의성 대폭 개선

**v4.0 (통합 버전) - 2024-12-08**
- ✅ PDF와 이미지 처리 통합
- ✅ 스크립트 중복 제거
- ✅ 일관된 워크플로우
- ✅ 사용자 경험 개선

**v3.0 (PDF 스킬)**
- ✅ DPI 자동 계산 (메모리 1.9배 절약)
- ✅ 블로그 최적화 자동 적용
- ✅ WebP/JPEG 동시 생성

**v1.0 (이미지 스킬)**
- ✅ 가볍고 빠른 이미지 처리
- ✅ 워터마크 제거 + 로고 삽입
- ✅ PNG 합치기 기능

## 💡 팁

### 빠른 처리 (이미지)
```bash
# 워터마크 제거만 (최고속, 기본)
python remove_watermark.py in.png

# 로고와 함께
python remove_watermark.py in.png favicon temp.png

# 워터마크 제거 + 최적화 (권장)
python remove_watermark.py in.png
python optimize_blog.py temp.png out.webp
```

### 메모리 절약 (PDF)
```bash
# 자동 DPI 계산 (권장, 로고 없음)
python pdf_smart.py input.pdf none output/ true 1200 webp

# 로고와 함께
python pdf_smart.py input.pdf logo.png output/ true 1200 webp

# 수동 DPI 지정 (고급)
python pdf_smart.py input.pdf none output/ true 1200 webp 150
```

### 일괄 처리
```bash
# 여러 이미지 워터마크 제거 (로고 없음)
for img in *.png; do
    python remove_watermark.py "$img"
done

# 로고와 함께
for img in *.png; do
    python remove_watermark.py "$img" favicon "clean_$img"
done

# 합치기
python merge_png.py clean_*.png merged.png

# 최적화
python optimize_blog.py merged.png final.webp
```

## 📋 체크리스트

### 사용 전
- [ ] Python 3.8+ 설치 확인
- [ ] 필수 라이브러리 설치 (Pillow, numpy, pdf2image)
- [ ] poppler-utils 설치 (PDF 처리용)
- [ ] 로고 파일 준비 (PNG, RGBA)

### 사용 후
- [ ] 워터마크 제거 확인
- [ ] 로고 위치 확인
- [ ] WebP 용량 확인 (<2MB)
- [ ] 브라우저 테스트 (WebP 지원)
- [ ] JPEG 폴백 확인 (구형 브라우저)

## 🎯 스킬 선택 가이드

### 이 스킬(MPS)을 사용하세요:
- ✅ PDF 워터마크 제거 필요
- ✅ 이미지 워터마크 제거 필요
- ✅ 블로그 최적화 필요
- ✅ 여러 파일 합치기
- ✅ 올인원 솔루션 선호

### 다른 스킬을 고려하세요:
- 특수한 이미지 편집 (별도 도구)
- 동영상 처리 (FFmpeg 등)
- 고급 PDF 편집 (PyPDF2 등)

---

**버전:** 4.2 (로고 기본 비활성화)
**날짜:** 2024-12-13
**용도:** PDF 및 이미지 통합 처리 + 네이버 블로그 최적화
**이전 스킬:** pdf-watermark-remover (v3.0), image-optimizer (v1.0)
**라이선스:** 동제당한의원 전용
