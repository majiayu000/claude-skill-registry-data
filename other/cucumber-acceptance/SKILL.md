---
name: cucumber-acceptance
description: 기능의 external behavior를 Cucumber 인수 테스트(주 검증층)로 구축 — .feature 실행으로 문서↔코드 드리프트를 구조적으로 차단, Four Layer(Steps→Protocol Driver→SUT), 태그 기반 가역 제외, 기존 JUnit 인수 테스트 이관. "인수 테스트 도입", "Gherkin을 실행 가능하게", "cucumber 셋업" 요청 시 사용. /cucumber-acceptance로 호출.
argument-hint: "[feature 설명 또는 요구사항 문서/.feature 경로]"
---

# Cucumber Acceptance — 실행 가능한 명세를 주 검증층으로

## GOAL

- **성공 = 요구사항의 Gherkin 시나리오가 `.feature` 파일로 실행되어, 기대 수치가 코드와 어긋나면 빌드가 실패하는 상태**
- 기능의 external behavior(고객이 사용하는 것과 기능)를 Cucumber가 **주 검증층**으로 담당 — programmer test 역할까지 겸한다
- 더 세밀한 검증(분기 커버리지·내부 협력)은 JUnit·Mockito가 **보조**
- 문서와 코드의 기대값 드리프트가 구조적으로 불가능해짐 — `.feature`의 Examples 표(검산 전개의 복사본)가 코드와 어긋나면 조용히 남지 못하고 빌드가 실패한다

## CONSTRAINTS

### Hard Rules — 테스트 전략 위계

| 검증 대상 | 도구 | 근거 |
|---|---|---|
| **external behavior** (고객이 쓰는 것과 기능) | **Cucumber `.feature`** (주 검증층) | 비개발자(+AI) 독자가 리뷰하는 실행 계약 |
| **세밀한 분기** (null/blank/미매핑 등 커버리지) | JUnit·Mockito (보조) | Gherkin에 넣으면 가독성 저하 |
| **property-based** ("모든 입력에 대해 성립") | jqwik 등 | Gherkin은 형식 자체가 example-based |
| **문제 도메인의 언어가 코드인 경우** (직렬화·동시성·성능) | 각자의 도구 | "외부 사용자 관점의 도메인 언어"가 성립 안 함 |

- **Gherkin에는 핵심 예시(key examples)만** — 망라적 edge를 시나리오로 나열하면 시나리오 폭발(Specification by Example의 규율). 커버리지용 분기는 unit test로.
- **Protocol Driver 분리** (Dave Farley Four Layer SoC): Steps(글루)는 파싱·위임만, SUT와의 실제 상호작용은 Driver에 격리. step definition에 SUT 호출·HTTP·UI 코드를 직접 넣지 않는다.
- **주 검증층은 빨라야 한다**: in-process driver 우선. Cucumber가 programmer test 역할을 겸하려면 이 전제가 필수다. 채널이 바뀌어도(HTTP·UI) Steps는 불변, Driver만 교체.
- **실행 불가능한 시나리오는 삭제하지 말고 태그로 제외** — 문서 가치는 남기고 실행만 빼는 가역적 처리.
- **숫자의 정본 관계를 문서에 선언**: 검산 근거(왜 이 값인가)는 스펙 문서, `.feature`는 그 수치를 실행으로 강제하는 인수 게이트.

## 적용 패턴

### 도입 시점 — 두 가지

| 시점 | 방식 | 적합 |
|---|---|---|
| **acceptance-first** (기본) | 위임 prompt로 전달받은 승인된 Gherkin 전문(`tdd-plan` 리뷰 승인 직후), 또는 기존 `.feature`를 `.feature` + Runner로 셋업. 미구현 시나리오는 `@pending`으로 두고, RGB가 진행되며 하나씩 태그 해제·green — 태그 해제는 그 시나리오를 통과시킨 Green 단계가 같은 커밋에서 수행한다 | `tdd-plan` 절차를 거친 모든 신규 기능 — 외부 인수 루프 + 내부 TDD 루프의 이중 루프(Dave Farley) |
| **구현 후 이관** (기존 프로젝트) | 기존 JUnit 인수 테스트를 `.feature`로 이관 — 아래 "기존 JUnit 인수 테스트 이관" 절차 | 이미 구현·테스트가 있는 프로젝트에 `tdd-plan` 없이 기능을 추가하는 경우 |

### 구조 — Four Layer 축소형

```
.feature (Test Case — 문제 도메인 언어)
   ↓
Steps (DSL/글루 — 텍스트 파싱 + Driver 위임만)
   ↓
Protocol Driver (SUT 상호작용 격리 — in-process/HTTP/UI 중 택일)
   ↓
SUT
```

```java
// Steps: 파싱만 하고 위임한다
public class CheckoutSteps {
    private final CheckoutDriver driver = new CheckoutDriver();

    @Given("^할인가 ([\\d,]+)엔인 상품 1건이 담겨 있다$")
    public void 단일_상품(final String price) {
        driver.addLine(yen(price), null);
    }

    @Then("^DDP 세액은 ([\\d,]+)엔이다$")
    public void 세액_확인(final String expected) {
        assertThat(driver.ddpAmount()).isEqualByComparingTo(yen(expected));
    }
}

// Protocol Driver: SUT와의 상호작용을 여기에만 둔다
class CheckoutDriver {
    private final List<Line> lines = new ArrayList<>();
    private BigDecimal ddpAmount;

    void addLine(final BigDecimal price, final String hsCode) { lines.add(new Line(price, hsCode)); }
    void checkOut() { ddpAmount = JapanDdp.calculateDdp(lines.toArray(new Line[0])); }
    BigDecimal ddpAmount() { return ddpAmount; }
}
```

### 결정 표(decision table) 스타일 — 계산 규칙 전용

FitNesse decision table의 방식을 Cucumber `DataTable`로 적용한다.
규칙 하나 = Scenario 하나 = 표 하나. 표의 컬럼은 Driver 입력·기대 출력에 1:1 대응한다.

| 적용 | 제외 |
|---|---|
| 입력 몇 개 → 계산 결과 하나로 요약되는 규칙 (세액·할인·차감 상한) | 상태 전이·순서가 의미를 갖는 흐름 (Given/When/Then 문장이 더 명확함) |
| 앵커 문서의 예제 검산표를 그대로 옮길 수 있는 규칙 | 행마다 다른 사전 조건이 필요한 규칙 |

```gherkin
@pending
Scenario: B-1. DDP 세액 계산
  Then 다음 주문의 DDP 세액이 표와 같다
    | 상품가 | HS코드   | DDP세액 |
    | 30000 |          | 4600   |
    | 30000 | 6109.10 | 5100   |
```

```java
public class DdpSteps {
    private final CheckoutDriver driver = new CheckoutDriver();

    // Empty cells arrive as null (Cucumber-JVM 5+)
    @DataTableType
    public DdpRow ddpRow(final Map<String, String> row) {
        return new DdpRow(yen(row.get("상품가")), row.get("HS코드"), yen(row.get("DDP세액")));
    }

    @Then("^다음 주문의 DDP 세액이 표와 같다$")
    public void DDP_세액_표(final List<DdpRow> rows) {
        SoftAssertions.assertSoftly(softly -> rows.forEach(row ->
            softly.assertThat(driver.ddpAmountFor(row.price(), row.hsCode()))
                  .as(row.toString())
                  .isEqualByComparingTo(row.expected())));
    }
}
```

- **정규식 step이 표당 1개로 줄어든다.** 수치는 셀로 전달되므로 Environment Notes의 `{int}` 쉼표 절단이 발생하지 않는다.
- **`SoftAssertions`로 전 행을 검증한다.** 첫 실패 행에서 중단하지 않고 어긋난 행을 모두 보고한다(FitNesse의 셀 단위 red/green에 해당).
- **Driver는 행마다 새 상태로 SUT를 호출한다.** 행 사이에 상태가 공유되면 행 순서에 결과가 의존한다.
- **`@pending` 단위는 Scenario다.** 한 표의 행은 같은 규칙의 핵심 예시이므로 한 사이클에서 함께 green으로 만든다. 행을 사이클별로 나눠야 할 만큼 표가 크면 규칙이 둘 이상 섞인 것이므로 Scenario를 분리한다.
- **컬럼명은 앵커 문서 검산표의 용어와 일치시킨다.** 문서와 `.feature`의 대조가 컬럼 단위로 가능해진다.

### 타입 경계 — 도메인 타입 ≠ DTO 타입

도메인 모델은 계산의 정확성이 요구하는 타입을 쓴다(금액이면 `BigDecimal`). **DTO는 그
타입을 그대로 사용하지 않는다** — presentation에 용이한 타입을 골라 경계에서 변환한다.
엔·원처럼 소수점이 없는 통화의 응답 금액은 `long`이 맞다.

```java
// 도메인: 절사·반올림 규칙이 BigDecimal을 요구한다
BigDecimal ddp = JapanDdp.calculateDdp(lines);

// 경계: presentation 타입으로 좁혀 내보낸다
record DdpResponse(long ddpAmount) {}
return new DdpResponse(ddp.longValueExact());
```

인수 테스트가 검출하지 못하는 오류다.
`BigDecimal.setScale(-2)`처럼 scale이 음수면 Jackson이 `toString()`을 그대로 써서
`{"ddpAmount":4.6E+3}`을 내보내는데, driver가 응답을 다시 `BigDecimal`로 역직렬화하고
`isEqualByComparingTo`로 비교하면 **왕복(round-trip)은 통과한다.** 시나리오가 전부 green인데
직렬화 포맷만 틀린 상태가 된다. 게다가 `BigDecimal.ZERO`를 반환하는 경로는 평범하게 `0`으로
반환되므로 응답 형식이 실행 경로마다 달라진다.

두 가지로 방지한다.

1. **직렬화 포맷은 raw body로 검증하는 테스트를 따로 둔다.** 직렬화는 "문제 도메인의 언어가
   코드인 영역"이라 Gherkin이 아니라 각자의 도구로 다룬다(위 Hard Rules 표).

   ```java
   String body = restTemplate.postForObject("/checkout/ddp", request, String.class);
   assertThat(body).isEqualTo("{\"ddpAmount\":4600}");
   ```

   **Driver의 응답 타입을 좁히는 것으로는 방지되지 않는다** — Jackson의 `ACCEPT_FLOAT_AS_INT`가
   기본 활성이라 `{"ddpAmount":4.6E+3}`을 `long` 필드에 예외 없이 `4600`으로 넣는다(2.18.2에서
   확인). 타입을 맞춰도 숫자가 우연히 일치해 통과한다. 문자열을 직접 검증해야 한다.
2. **실제 채널로 한 번 호출해 직접 확인한다.** 문서에 요청·응답 예시를 적었다면 그 예시는
   실행된 적이 있어야 한다.

```bash
curl -s -X POST localhost:8080/checkout/ddp -H 'Content-Type: application/json' \
  -d '{"lines":[{"goodsPrice":30000,"hsCode":null}]}'
```

### 태그 기반 가역적 제외

```gherkin
@api-enforced   # API 형태로 만족 — 해당 파라미터가 시그니처에 없어 구조적으로 충족, 실행 불가
Scenario: A-3. 배송비는 임계값 판정에 포함하지 않는다
  ...

@pending        # SUT가 아직 그 값을 노출하지 않음 — 노출되면 태그만 해제
Scenario: B-4-1. 무관세 품목이어도 소비세는 부과된다
  ...
```

```java
@ConfigurationParameter(key = FILTER_TAGS_PROPERTY_NAME,
    value = "not @api-enforced and not @pending")
```

실행 트리에서 SKIPPED/ignored로 표시된다 — "did not match this scenario" 메시지는 오류가 아니라 skip 사유 텍스트다.

#### Scenario Outline — Examples 블록 단위로 분리해 한 사이클씩 해제

`Scenario Outline` 하나에 `Examples:` 블록을 **여러 개** 둘 수 있고, 태그는 붙인 위치에
따라 범위가 다르다:

| 태그 위치 | 범위 |
|---|---|
| `Scenario Outline` 위 | 그 Outline의 **모든** Examples 블록에 상속 — 전부 제외 |
| 각 `Examples:` 위 | **그 블록만** 제외 |

Outline 위에만 붙일 수 있다고 보면, 한 표에 4행이 있을 때 태그를 떼는 순간 네 규칙을
한 사이클에서 동시에 green으로 만들어야 한다 — TDD 단위로 너무 크다.
행을 블록으로 분리하면 사이클마다 한 규칙씩 통과시킬 수 있다:

아래는 **두 번째 사이클 도중의 상태**다 — E-1은 통과해 태그가 없고, 나머지는 대기 중:

```gherkin
Scenario Outline: <케이스>. 쿠폰·마일리지 적용 후 최종 결제 금액
  Given ...
  Then 최종 결제 금액은 <최종금액>원이다

  Examples:                          # 이번 사이클에서 통과시킬 한 규칙
    | 케이스 | ... | 최종금액 |
    | E-1   | ... | 20000  |

  @pending                           # 다음 사이클 — 마일리지가 배송비로 이월
  Examples:
    | 케이스 | ... | 최종금액 |
    | E-2   | ... | 2000   |

  @pending                           # 그다음 — 차감 상한
  Examples:
    | 케이스 | ... | 최종금액 |
    | E-3   | ... | 0      |
```

**생애주기 — 분리는 임시 상태다.** 이 분리는 RGB 진행 중에만 존재한다:

1. 새 시나리오를 failing test로 추가할 때 **분리한다**(각 블록에 `@pending`)
2. Green 단계마다 자기 블록의 `@pending`을 같은 커밋에서 **해제한다**
3. 그 Outline이 **전부 green이 되면 한 블록으로 다시 합친다** — 이때 표 헤더가
   한 번만 남는 것이 정상 상태다. 합치는 주체와 시점은 **마지막 `@pending`을 해제한 그
   Green과 같은 커밋**이다 (별도 정리 단계를 두면 아무도 하지 않아 누락된다)
4. 이후 새 시나리오를 추가할 때 다시 1번으로

3번을 생략하면 헤더가 반복된 채 블록이 계속 누적되어, 표 하나로 읽히던 Examples가
읽기 어려워진다. 전부 green인데 블록이 여럿이면 **합치지 않은 것이지 의도된 구조가
아니다.**

### 기존 JUnit 인수 테스트 이관 (기존 프로젝트)

이관은 반복적·기계적 작업이다. 이 스킬을 호출하면
Claude가 아래 절차를 대신 수행하고, 사람은 결과(green + 의도한 SKIPPED)만 확인한다.

1. 요구사항 문서의 Gherkin을 `.feature`로 이관 (문서 쪽에는 "실행되는 원본은 `.feature`" 정본 선언)
2. Runner + Driver + Steps 작성 → 전체 green 확인
3. JUnit에서 **같은 검증을 하던 인수 테스트 제거** (같은 검증이 두 계층에 중복되면 안 됨)
4. 분기 커버리지용 unit test만 JUnit에 잔류
5. `@Order`·`@TestClassOrder` 같은 순서 장치가 있었다면 함께 해체 — `.feature`는 파일에 적힌 순서가 곧 실행·표시 순서라 순서 어노테이션이 불필요하다

## 적용 기준

### 적용 대상
- 고객·이해관계자가 보는 기능의 external behavior
- 요구사항 문서에 Gherkin/기대값 표가 이미 있고, 코드와의 드리프트가 걱정되는 경우
- `tdd-plan` 리뷰에서 승인된 Gherkin 전문 — 재작성 없이 그대로 `.feature`가 된다 (위 "도입 시점"의 acceptance-first)
- 비개발자(PO·QA·도메인 전문가) 또는 AI가 명세를 리뷰·승인하는 워크플로우

### 적용 제외
- 분기 커버리지·내부 협력 검증 → JUnit·Mockito (위계 표 참조)
- property-based 검증 → jqwik 등
- 직렬화·동시성·성능 등 문제 도메인의 언어가 코드인 영역
- **문서↔실행 트리 정렬이 목적의 전부인 경우** — JUnit `@Nested`+`@Order`로 Gherkin 구조를 흉내 내는 것은 격리된 테스트에 "순서 의존"이라는 거짓 신호를 주는 냄새다(Test Desiderata의 Isolated). 정렬이 필요하면 순서 어노테이션이 아니라 이 스킬(실행 가능한 명세)로 푼다.

## Cucumber-JVM 셋업

```kotlin
// build.gradle.kts
testImplementation("io.cucumber:cucumber-java:7.20.1")
testImplementation("io.cucumber:cucumber-junit-platform-engine:7.20.1")
testImplementation("org.junit.platform:junit-platform-suite")
testImplementation("org.assertj:assertj-core")   // assertThat·SoftAssertions (spring-boot-starter-test에 포함)
```

```java
@Suite
@IncludeEngines("cucumber")
@SelectClasspathResource("example/japanddp")   // .feature 위치 (src/test/resources 하위)
@ConfigurationParameter(key = GLUE_PROPERTY_NAME, value = "example.japanddp")
@ConfigurationParameter(key = FILTER_TAGS_PROPERTY_NAME, value = "not @pending")
@ConfigurationParameter(key = PLUGIN_PROPERTY_NAME, value = "pretty")
class RunCucumberTest {
}
```

`./gradlew test`로 다른 JUnit 테스트와 함께 실행된다. IntelliJ에서는 Runner 클래스 실행으로 Feature→Rule→Scenario 트리를 보고, "Cucumber for Java" 플러그인을 설치하면 `.feature` 파일·개별 Scenario에서 직접 실행할 수도 있다.

### Environment Notes — cucumber-java 실전 제약 (직접 확인)

- **정규식 스텝은 `^...$` 앵커 필수** — 앵커가 없으면 Cucumber Expression으로 오인식되어(`([\d,]+)` 등이 CE 문법과 충돌) 모든 스텝이 undefined로 처리된다.
- **glue 클래스는 `public` 필수** — package-private이면 glue 스캔이 클래스를 찾지 못해 리터럴 스텝까지 undefined가 된다.
- **`{int}`는 쉼표 표기를 못 받는다** — "16,666엔" 같은 한국어 표기에서 자동 생성 스켈레톤이 "16"만 `{int}`로 잘라낸다. 정규식 `([\d,]+)` + 쉼표 제거 파싱 헬퍼로 우회한다. **자동 생성 스켈레톤은 "어떤 스텝이 빠졌는지" 찾는 용도로만 쓰고 텍스트를 그대로 신뢰하지 않는다.**

## OUTPUT FORMAT

### 실행 절차 — 대상 파악은 메인, 구축은 에이전트 위임

1. **대상 파악** (메인 컨텍스트) — 위임 prompt로 전달받은 승인된 Gherkin 전문(또는 기존
   `.feature`)과 기존 테스트 현황을 확인해 모드를 정한다: **신규 셋업**(acceptance-first,
   승인된 Gherkin 전문이 있음) 또는 **기존 JUnit 이관**(구현 후 이관)
2. **`tdd-acceptance-builder` 에이전트에 위임** — 대상 문서 경로 + 판정한 모드를 전달.
   `.feature` 작성/이관, Runner+Driver+Steps(Four Layer), 전체 green 확인, 기존 JUnit 정리,
   문서 정본 선언 갱신, 커밋까지 에이전트가 수행한다(아래 "에이전트가 수행하는 세부 단계"를
   에이전트가 자신의 정본으로 참조)
3. **결과 보고** — 에이전트가 반환한 시나리오 수·제외 태그·green/SKIPPED 결과·커밋 해시를
   사용자에게 전달

### 에이전트가 수행하는 세부 단계 (참조용 — 위임 프롬프트에 재기술하지 않음)

1. `.feature` 작성/이관 — `src/test/resources/{package_path}/` 하위. 실행 불가 시나리오는
   태그 부여. 문서에 정본 선언 갱신
2. Runner + Protocol Driver + Steps 작성 — Four Layer 축소형 구조
3. 전체 green 확인 — 태그 제외가 의도한 시나리오만 SKIPPED인지 함께 확인
4. 기존 JUnit 정리 — 중복 인수 테스트 제거, unit test만 잔류, 순서 장치 해체
5. 문서 갱신 — 정본 선언·테스트 위치 표·프로젝트 CLAUDE.md의 두 계층 설명
6. 커밋 — 단계별 분리(인프라 도입 / JUnit 이관 정리 / 문서 갱신). 메시지는
   `docs/reviewable-commits.md`(없으면 `${CLAUDE_PLUGIN_ROOT}/references/reviewable-commits.md`) 표준을
   따르고, 길이는 `../../references/commit-style.md`의 간결성 규칙(제목 + 핵심
   bullet 2~4줄)을 따르며, 한글 메시지는 임시 파일 + `git commit -F`

## FAILURE CONDITIONS

- 망라적 edge case를 시나리오로 나열 (시나리오 폭발 — 핵심 예시만)
- step definition에 SUT 상호작용을 직접 삽입 (Protocol Driver 미분리)
- 실행 불가능한 시나리오를 삭제 (태그 제외로 가역 처리해야 함)
- 이관 후 JUnit에 같은 검증의 인수 테스트 방치 (두 계층 중복)
- 문서↔실행 정렬을 `@Order`류 순서 어노테이션으로 흉내 냄
- property-based·기술 도메인 검증을 Gherkin으로 작성
- 느린 채널(브라우저 등)을 기본 driver로 선택해 주 검증층이 느려짐
