---
name: spring-boot
description: Spring Boot(3.x)로 REST API·서비스·영속성 코드를 작성/수정할 때 따르는 관용 패턴·레시피. 컨트롤러·서비스·리포지토리 레이어링, DTO·검증, 예외 처리(RFC 9457), JPA, 설정, 테스트 규약을 제공. 대상 프로젝트가 Spring/Spring Boot일 때 발동.
---

# spring-boot

Spring Boot 프로젝트에서 백엔드 코드를 **일관되고 관용적으로** 작성하기 위한 참조 스킬입니다. `backend-impl` 에이전트가 API 계약(`01_api_design.md`)과 데이터 모델(`03_db_design.md`)을 실제 코드로 옮길 때 이 스킬의 레시피를 따릅니다.

## 언제 발동하나

다음이 보이는 프로젝트에서 엔드포인트·서비스·영속성 코드를 작성/수정할 때:
- `build.gradle`(`.kts`) 또는 `pom.xml`에 `org.springframework.boot` 의존성
- `@SpringBootApplication` 진입점
- `spring-boot-starter-web`, `spring-boot-starter-data-jpa` 등 스타터

`backend-impl`이 스택을 Spring Boot로 감지하면 이 스킬을 로드해 절차에 반영합니다.

## 전제

- **Spring Boot 3.x** — Jakarta 네임스페이스(`jakarta.*`, `javax.*` 아님).
- **Java 21** 기준(record, 패턴 매칭 등 활용). 프로젝트가 다른 버전이면 그에 맞춘다.
- 언어는 **Java 중심**으로 예시를 제공한다. 프로젝트가 Kotlin이면 동일 원칙을 Kotlin 관용구로 옮긴다.

## 핵심 원칙

1. **기존 패턴 모방이 최우선.** 이 스킬의 템플릿은 관례가 없을 때의 기본값이다. 프로젝트에 이미 레이어링·에러 포맷·네이밍 관례가 있으면 **그것을 따른다**. 이유 없이 새 규칙을 도입하지 않는다.
2. **레이어 경계 준수.** `web → service → repository` 단방향 의존. 도메인·영속성이 웹 계층에 의존하지 않는다.
3. **생성자 주입.** 필드 주입(`@Autowired` 필드)을 쓰지 않는다. `final` 필드 + 생성자 주입(롬복 `@RequiredArgsConstructor` 또는 명시적 생성자).
4. **DTO로 경계 분리.** JPA 엔티티를 요청/응답에 직접 노출하지 않는다. 요청·응답은 record DTO로.
5. **트랜잭션은 서비스 레이어에서.** 컨트롤러·리포지토리가 아니라 서비스 메서드에 `@Transactional`. 읽기 전용은 `readOnly = true`.
6. **에러는 RFC 9457로 통일.** 예외를 `ProblemDetail`(`application/problem+json`)로 매핑한다. `api-designer`의 기본 에러 포맷과 정렬된다.
7. **비밀값은 외부화.** 자격증명·토큰을 코드/커밋에 하드코딩하지 않는다. 환경변수·외부 시크릿으로.

## 작업별 참조

작업 유형에 따라 해당 문서를 열어 템플릿과 체크리스트를 따른다:

| 작업 | 참조 |
| --- | --- |
| 패키지 구조·빌드 설정·버전 전제 | `references/project-layout.md` |
| 컨트롤러·요청/응답 DTO·검증·상태코드 | `references/web-layer.md` |
| 서비스 로직·트랜잭션·매핑 | `references/service-layer.md` |
| JPA 엔티티·리포지토리·쿼리·페이지네이션 | `references/persistence-layer.md` |
| 예외 처리·에러 응답(RFC 9457) | `references/exception-handling.md` |
| 설정·프로파일·시크릿 외부화 | `references/configuration.md` |
| 테스트 슬라이스·통합·Testcontainers | `references/testing.md` |

## 팀 정렬

- **입력**: `api-designer`의 `01_api_design.md`(엔드포인트·상태코드), `db-migrator`의 `03_db_design.md`(스키마·엔터티)를 그대로 코드에 반영한다.
- **에러 포맷**: `api-designer` 기본값 **RFC 9457**과 일치시킨다(`exception-handling.md`).
- **테스트 작성 주체는 `test-writer`.** `references/testing.md`는 **규약·패턴 참조용**이다. 이 스킬은 backend-impl이 기존 테스트를 실행해 회귀를 확인하는 것까지 돕지만, 새 테스트 작성은 `test-writer`에 위임한다(위임 경계 유지).

## 검증

구현 후 반드시 빌드·기존 테스트를 실행해 회귀가 없는지 확인한다:
- Gradle: `./gradlew build` (또는 `./gradlew test`)
- Maven: `mvn verify` (또는 `mvn test`)

실행한 명령과 결과를 그대로 보고한다. 통과했다고 꾸미지 않는다.
