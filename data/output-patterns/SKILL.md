---
name: output-patterns
description: 리포트 출력 패턴. Excel, HTML 보고서, 콘솔 출력 스타일 가이드.
---

# 리포트 출력 패턴

프로젝트의 표준 리포트 생성 패턴입니다. Excel과 HTML을 동시에 생성합니다.

## 권장 패턴: generate_reports()

**새 플러그인 작성 시 권장하는 통합 출력 API**

```python
from core.tools.io.compat import generate_reports

def run(ctx) -> None:
    results = parallel_collect(ctx, _collect_and_analyze, service="ec2")

    # HTML용 flat 데이터 준비
    flat_data = [
        {
            "account_id": r.account_id,
            "account_name": r.account_name,
            "region": r.region,
            "resource_id": r.resource_id,
            "resource_name": r.name,
            "status": r.status,
            "reason": r.recommendation,
            "cost": r.monthly_cost,
        }
        for r in results
    ]

    # Excel + HTML 동시 생성
    report_paths = generate_reports(
        ctx,
        data=flat_data,
        excel_generator=lambda d: _save_excel(results, d),
        html_config={
            "title": "EC2 미사용 인스턴스 분석",
            "service": "EC2",
            "tool_name": "unused",
            "total": total_count,
            "found": unused_count,
            "savings": total_savings,
        },
        output_dir=output_path,
    )
```

## Excel 출력 패턴

### 기본 사용법

```python
from core.tools.io.excel import Workbook, ColumnDef, Styles

# Workbook 생성
wb = Workbook()  # 한국어 (기본)
wb = Workbook(lang="en")  # 영어

# 컬럼 정의
columns = [
    ColumnDef(header="계정", header_en="Account", width=15, style="data"),
    ColumnDef(header="리전", header_en="Region", width=12, style="center"),
    ColumnDef(header="크기(GB)", header_en="Size(GB)", width=10, style="number"),
    ColumnDef(header="비용", header_en="Cost", width=12, style="currency"),
]

# 시트 생성 및 데이터 추가
sheet = wb.new_sheet("분석 결과", columns=columns)

for item in results:
    style = Styles.danger() if item.unused else None
    sheet.add_row([item.account, item.region, item.size, item.cost], style=style)

# 요약 행
sheet.add_summary_row(["합계", "", total_size, total_cost])

# 저장
wb.save_as(output_dir, prefix="EC2_Unused", region="ap-northeast-2")
```

### 스타일 타입

| style | 설명 | 정렬 |
|-------|------|------|
| `data` | 일반 텍스트 (기본) | 왼쪽, 줄바꿈 |
| `center` | 중앙 정렬 | 중앙, 줄바꿈 |
| `number` | 정수 (1,234) | 오른쪽 |
| `currency` | 통화 ($1,234.56) | 오른쪽 |
| `percent` | 백분율 (12.34%) | 오른쪽 |

### Styles 프리셋

```python
Styles.danger()   # 빨간 배경 + 흰 글씨
Styles.warning()  # 노란 배경
Styles.success()  # 초록 배경
Styles.summary()  # 연노랑 배경 + 볼드 (합계용)
```

### Summary 시트

```python
summary = wb.new_summary_sheet()
summary.add_title("EBS 볼륨 분석 보고서")
summary.add_section("분석 정보")
summary.add_item("분석 일시", "2026-01-23 15:30:00")
summary.add_item("계정 수", "5개")
summary.add_section("분석 결과")
summary.add_item("미사용 볼륨", 23, highlight="danger")
summary.add_item("월간 예상 비용", "$1,234.56", highlight="warning")
```

## HTML 출력 패턴

### AWSReport (권장)

```python
from core.tools.io.html import AWSReport, ResourceItem

# 리포트 생성
report = AWSReport(
    title="EC2 미사용 리소스 분석",
    service="EC2",
    tool_name="unused",
    ctx=ctx,
)

# 요약 정보
report.set_summary(
    total=150,
    found=23,
    savings=1234.56,
)

# 리소스 추가
for item in results:
    report.add_resource(ResourceItem(
        account_id=item["account_id"],
        account_name=item["account_name"],
        region=item["region"],
        resource_id=item["instance_id"],
        resource_name=item.get("name", ""),
        status="unused",
        reason=item["reason"],
        cost=item.get("monthly_cost", 0),
    ))

# 저장 (브라우저 자동 열림)
report.save(output_path)
```

### 간편 API

```python
from core.tools.io.html import create_aws_report

report = create_aws_report(
    title="EC2 미사용",
    service="EC2",
    tool_name="unused",
    ctx=ctx,
    resources=results,  # list[dict]
    total=100,
    found=10,
    savings=500.0,
)
report.save("output.html")
```

### 자동 생성 기능

AWSReport 사용 시 자동 생성:
- 요약 카드 (전체, 발견, 비율, 절감액)
- 계정별 분포 차트 (Pie)
- 리전별 분포 차트 (Bar)
- 상태별 분포 차트 (있는 경우)
- 리소스 상세 테이블 (검색, 정렬, 페이지네이션)

## 콘솔 출력 스타일 가이드

### 표준 심볼 (이모지 사용 금지)

```python
from cli.ui import (
    SYMBOL_SUCCESS,   # ✓ - 완료
    SYMBOL_ERROR,     # ✗ - 에러
    SYMBOL_WARNING,   # ! - 경고
    SYMBOL_INFO,      # • - 정보
    SYMBOL_PROGRESS,  # • - 진행 중
)
```

### 표준 출력 함수

```python
from cli.ui import (
    print_success,      # [green]✓ 메시지[/green]
    print_error,        # [red]✗ 메시지[/red]
    print_warning,      # [yellow]! 메시지[/yellow]
    print_info,         # [blue]• 메시지[/blue]
    print_step_header,  # [bold cyan]Step N: 메시지[/bold cyan]
)
```

### Step 출력 패턴

```python
from cli.ui import console, print_step_header

# Step 헤더
print_step_header(1, "데이터 수집 중...")
# 출력: [bold cyan]Step 1: 데이터 수집 중...[/bold cyan]

# 부작업 완료
console.print("[green]✓ 50개 파일 발견[/green]")
```

### 금지 사항

- **이모지 사용 금지**: `📊`, `🔍`, `⏰`, `🚀` 등
- **이모지 체크마크 금지**: `✅`, `❌` → `✓`, `✗` 사용
- **이모지 경고 금지**: `⚠️` → `!` 사용

## 참조

- `core/tools/io/config.py` - OutputConfig, OutputFormat
- `core/tools/io/compat.py` - generate_reports
- `core/tools/io/excel/workbook.py` - Workbook, Sheet, ColumnDef
- `core/tools/io/html/aws_report.py` - AWSReport, ResourceItem
