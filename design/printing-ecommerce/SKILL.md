---
name: printing-ecommerce
description: PHP 7.4 + MySQL 기반 인쇄 전자상거래 플랫폼(dsp1830.shop) 개발 가이드. 9개 품목(스티커, 전단지, 명함, 봉투, 카달로그, 포스터, 상품권, 자석스티커, 양식지), 실시간 가격계산기, 교정승인 시스템, KB에스크로 결제를 지원. 이 스킬은 (1) 레이아웃/UI 일관성 문제 해결, (2) 장바구니→주문→완료 플로우 개발, (3) 가격계산기 로직 수정, (4) 추가옵션(코팅/접지/오시) 처리, (5) 견적서 시스템 구현, (6) 관리자 대시보드 개발 시 사용.
---

# 인쇄 쇼핑몰 개발 스킬

## 기술 스택

| 구분 | 기술 |
|------|------|
| Backend | PHP 7.4.33 |
| Database | MySQL 5.7+ (utf8mb4) |
| Frontend | HTML5, CSS3, JavaScript (jQuery) |
| Server | XAMPP (개발) → Cafe24 (운영) |
| Payment | KB에스크로 |
| Email | PHPMailer + 네이버 SMTP |

## 디렉토리 구조

```
dsp1830.shop/
├── index.php                    # 메인 페이지
├── sub/                         # 제품별 페이지
│   ├── sticker_new.php         # 스티커
│   ├── inserted.php            # 전단지
│   ├── namecard.php            # 명함
│   ├── envelope.php            # 봉투
│   ├── cadarok.php             # 카달로그
│   ├── littleprint.php         # 포스터
│   ├── merchandisebond.php     # 상품권
│   ├── msticker.php            # 자석스티커
│   └── ncrflambeau.php         # 양식지
├── mlangprintauto/shop/        # 주문 시스템
│   ├── cart.php                # 장바구니
│   ├── order.php               # 주문서
│   └── order_result.php        # 주문완료
├── admin/                       # 관리자
│   ├── OrderForm/              # 주문관리
│   └── dashboard.php           # 대시보드
├── member/                      # 회원 시스템
│   ├── login.php
│   ├── register.php
│   └── mypage.php
└── inc/                         # 공통 파일
    ├── dbcon.php               # DB 연결
    ├── header.php
    └── footer.php
```

## 핵심 테이블

| 테이블 | 용도 |
|--------|------|
| `shop_temp` | 장바구니 (세션 기반) |
| `orderform` | 주문서 마스터 |
| `orderformtree` | 주문 상세 (1:N) |
| `members` | 회원 정보 |
| `quotations` | 견적서 |
| `proofs` | 교정 시안 |

## 주문 상태 코드

```php
const ORDER_STATUS = [
    'pending'    => '입금대기',
    'paid'       => '결제완료',
    'printing'   => '인쇄중',
    'shipping'   => '배송중',
    'completed'  => '배송완료',
    'cancelled'  => '주문취소'
];
```

## 참고 문서

### 핵심 기능
| 문서 | 내용 | 사용 시점 |
|------|------|----------|
| [order-flow.md](references/order-flow.md) | 5단계 주문 프로세스 | 장바구니→주문완료 개발 시 |
| [db-schema.md](references/db-schema.md) | 전체 테이블 스키마 | DB 작업 시 |
| [price-calculator.md](references/price-calculator.md) | 가격 계산 로직 | 계산기 수정 시 |
| [member-system.md](references/member-system.md) | 회원/로그인/마이페이지 | 회원 기능 개발 시 |
| [payment-system.md](references/payment-system.md) | KB에스크로 결제 | 결제 연동 시 |
| [shipping-system.md](references/shipping-system.md) | 배송 조회/관리 | 배송 기능 개발 시 |

### 인쇄 특화 기능
| 문서 | 내용 | 사용 시점 |
|------|------|----------|
| [proof-system.md](references/proof-system.md) | 교정 승인 시스템 | 시안 확인 기능 개발 시 |
| [file-upload.md](references/file-upload.md) | 인쇄 파일 업로드 | 파일 처리 시 |
| [quotation-system.md](references/quotation-system.md) | 견적서 시스템 | 견적 기능 개발 시 |

### 관리/운영
| 문서 | 내용 | 사용 시점 |
|------|------|----------|
| [admin-dashboard.md](references/admin-dashboard.md) | 관리자 대시보드 | 어드민 개발 시 |
| [email-system.md](references/email-system.md) | 이메일 발송 | 알림 기능 개발 시 |
| [faq-notice.md](references/faq-notice.md) | FAQ/공지사항 | 게시판 개발 시 |
| [coupon-discount.md](references/coupon-discount.md) | 쿠폰/할인 시스템 | 프로모션 개발 시 |

### 디자인
| 문서 | 내용 | 사용 시점 |
|------|------|----------|
| [design-guide.md](references/design-guide.md) | 디자인 리뉴얼 가이드 | UI/UX 작업 시 |

### 기술/보안
| 문서 | 내용 | 사용 시점 |
|------|------|----------|
| [security.md](references/security.md) | 보안 가이드 | 보안 점검 시 |
| [seo-optimization.md](references/seo-optimization.md) | SEO 최적화 | 검색 최적화 시 |
| [error-logging.md](references/error-logging.md) | 에러/로깅 시스템 | 디버깅/모니터링 시 |
| [bug-fixes.md](references/bug-fixes.md) | 버그 수정 이력 | 트러블슈팅 시 |

## 자주 발생하는 문제

### 1. 규격/옵션 표시 불일치
페이지마다 다른 형식으로 표시됨 → **ProductSpecFormatter 사용** (`/includes/ProductSpecFormatter.php`)
- 관련 스킬: `duson-print-rules` 규칙 2-5
- 관련 문서: `bug-fixes.md` #34

### 2. 수량 표시 불일치
전단지의 "연" 단위가 장바구니/주문서에서 다르게 표시됨 → `bug-fixes.md`

### 3. 추가옵션 누락
코팅/접지/오시 옵션이 주문서에 표시 안 됨 → `shop_temp.options` 필드 확인

### 4. 세션 만료
장바구니가 갑자기 비워짐 → `session.gc_maxlifetime` 설정

### 5. 파일 업로드 실패
대용량 인쇄 파일 업로드 시 타임아웃 → `file-upload.md`
