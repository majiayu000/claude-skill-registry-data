---
name: spring-boot
description: Spring Boot(3.x)로 REST API·서비스·영속성 코드를 작성하거나 수정할 때 따르는 관용 패턴·레시피 모음. 컨트롤러·서비스·리포지토리 레이어링, record DTO·Bean Validation, 예외 처리(RFC 9457 ProblemDetail), JPA·트랜잭션·페이지네이션, 설정·시크릿 외부화, 비밀번호 해싱 등 보안 기본, 테스트 규약을 제공한다. build.gradle(.kts)/pom.xml에 org.springframework.boot 의존성이 있거나 @SpringBootApplication·@RestController·@Entity가 보이는 프로젝트에서 엔드포인트·서비스·엔티티·DTO·예외 핸들러를 만들 때 반드시 사용. "Spring Boot로 API 만들어줘", "컨트롤러/서비스/리포지토리 추가", "JPA 엔티티 매핑", "회원가입 API", "에러 응답 포맷 일관되게" 같은 요청을 Spring 또는 Kotlin+Spring 프로젝트에서 받으면 이 스킬을 참조한다.
---

# spring-boot

Spring Boot 프로젝트에서 백엔드 코드를 **일관되고 관용적으로** 작성하기 위한 참조 스킬입니다. 컨트롤러·서비스·영속성 레이어링, DTO·검증, 예외 처리, JPA, 설정, 보안 기본, 테스트 규약의 레시피를 담고 있습니다.

## 언제 발동하나

Spring Boot 프로젝트에서 엔드포인트·서비스·영속성 코드를 작성/수정할 때 발동한다. 다음 신호로 스택을 판별한다:

- `build.gradle`(`.kts`) 또는 `pom.xml`에 `org.springframework.boot` 의존성
- `@SpringBootApplication` 진입점
- `spring-boot-starter-web`, `spring-boot-starter-data-jpa` 등 스타터
- `@RestController`, `@Entity`, `@Service` 등 스프링 관용 애노테이션

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
6. **에러는 RFC 9457로 통일.** 예외를 `ProblemDetail`(`application/problem+json`)로 매핑한다. 프로젝트에 이미 에러 포맷이 있으면 원칙 1에 따라 그것을 따른다.
7. **민감 데이터는 안전하게 다룬다.** 비밀번호·토큰 같은 자격증명은 **평문으로 저장·로그·응답에 노출하지 않는다.** 비밀번호는 `PasswordEncoder`로 해시해 저장한다. 이건 "나중에 처리" 주석으로 미루지 말고 **처음부터 코드로 반영**한다. 상세는 `references/security.md`.
8. **비밀값은 외부화.** 자격증명·API 키를 코드/커밋에 하드코딩하지 않는다. 환경변수·외부 시크릿으로(`references/configuration.md`).

## 작업별 참조

작업 유형에 따라 해당 문서를 열어 템플릿과 체크리스트를 따른다:

| 작업 | 참조 |
| --- | --- |
| 패키지 구조·빌드 설정·버전 전제 | `references/project-layout.md` |
| 컨트롤러·요청/응답 DTO·검증·상태코드 | `references/web-layer.md` |
| 서비스 로직·트랜잭션·매핑 | `references/service-layer.md` |
| JPA 엔티티·리포지토리·쿼리·페이지네이션 | `references/persistence-layer.md` |
| 예외 처리·에러 응답(RFC 9457) | `references/exception-handling.md` |
| 비밀번호 해싱·민감 데이터·인증 기본 | `references/security.md` |
| 설정·프로파일·시크릿 외부화 | `references/configuration.md` |
| 테스트 슬라이스·통합·Testcontainers | `references/testing.md` |

## 산출물 정렬

프로젝트나 워크플로우에 **선행 설계 산출물이 있으면 그대로 코드에 반영**한다(없으면 요청만으로 작업한다):

- **API 설계 문서**(엔드포인트·상태코드·에러 포맷)가 있으면 컨트롤러·응답·상태코드를 거기에 맞춘다.
- **DB 스키마/마이그레이션 설계**가 있으면 엔티티·제약·인덱스를 거기에 맞춘다.
- 에러 포맷 기본값은 **RFC 9457**이되, 설계 문서나 기존 코드에 다른 규약이 있으면 그것을 따른다.

## 테스트

`references/testing.md`는 **테스트 계층 선택·슬라이스·통합 패턴의 규약 참조**다. 이 스킬의 기본 책임은 구현과 **기존 테스트 실행을 통한 회귀 확인**까지다. 새 테스트를 대량으로 작성하는 일은, 프로젝트 워크플로우에 테스트 전담 에이전트/단계가 있다면 그쪽에 위임할 수 있다(위임 경계가 있으면 존중한다). 그런 경계가 없으면 `testing.md`의 규약대로 직접 작성한다.

## 검증

구현 후 반드시 빌드·기존 테스트를 실행해 회귀가 없는지 확인한다:
- Gradle: `./gradlew build` (또는 `./gradlew test`)
- Maven: `mvn verify` (또는 `mvn test`)

실행한 명령과 결과를 그대로 보고한다. 통과했다고 꾸미지 않는다.
