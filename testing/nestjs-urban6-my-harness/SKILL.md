---
name: nestjs
description: NestJS로 REST API·서비스·영속성 코드를 작성하거나 수정할 때 따르는 관용 패턴·레시피 모음. 모듈·컨트롤러·프로바이더 레이어링, DTO·검증(class-validator·ValidationPipe), 예외 처리(RFC 9457 예외 필터), Prisma 영속성·트랜잭션·페이지네이션, ConfigModule 설정·시크릿 외부화, 비밀번호 해싱 등 보안 기본, Jest 테스트 규약을 제공한다. package.json에 @nestjs/core 의존성이 있거나 nest-cli.json·NestFactory.create·*.module.ts/*.controller.ts/*.service.ts가 보이는 프로젝트에서 엔드포인트·서비스·프로바이더·DTO·예외 필터를 만들 때 반드시 사용. "NestJS로 API 만들어줘", "모듈/컨트롤러/서비스 추가", "Prisma 스키마 매핑", "회원가입 API", "에러 응답 포맷 일관되게" 같은 요청을 NestJS 프로젝트에서 받으면 이 스킬을 참조한다.
---

# nestjs

NestJS 프로젝트에서 백엔드 코드를 **일관되고 관용적으로** 작성하기 위한 참조 스킬입니다. 모듈·컨트롤러·프로바이더 레이어링, DTO·검증, 예외 처리, Prisma 영속성, 설정, 보안 기본, 테스트 규약의 레시피를 담고 있습니다.

## 언제 발동하나

다음이 보이는 프로젝트에서 엔드포인트·서비스·영속성 코드를 작성/수정할 때:
- `package.json`에 `@nestjs/core`, `@nestjs/common` 의존성
- `nest-cli.json`, `main.ts`의 `NestFactory.create(...)` 부트스트랩
- `*.module.ts` / `*.controller.ts` / `*.service.ts` 파일 관례

## 전제

- **TypeScript** — `strict` 모드 기준. 데코레이터 사용(`experimentalDecorators`, `emitDecoratorMetadata` 활성).
- **영속성은 Prisma 중심** — `PrismaService` + `schema.prisma`. 프로젝트가 TypeORM/Mikro-ORM이면 동일 원칙(영속성 경계·리포지토리 추상화)을 그 도구 관용구로 옮긴다.
- **검증은 class-validator + class-transformer**, 전역 `ValidationPipe`.
- **테스트는 Jest**(+ supertest e2e).

## 핵심 원칙

1. **기존 패턴 모방이 최우선.** 이 스킬의 템플릿은 관례가 없을 때의 기본값이다. 프로젝트에 이미 모듈 경계·에러 포맷·네이밍 관례가 있으면 **그것을 따른다**.
2. **모듈 경계 준수.** 기능은 `feature.module.ts`로 캡슐화하고, `controller → service → (prisma) repository` 단방향 의존. 서비스/도메인이 컨트롤러에 의존하지 않는다.
3. **생성자 주입(DI).** 프로바이더는 `constructor(private readonly x: X)`로 주입. 수동 `new`로 의존성을 만들지 않는다.
4. **DTO로 경계 분리.** 요청/응답 DTO 클래스를 두고, Prisma 모델(엔티티)을 요청/응답에 그대로 노출하지 않는다.
5. **검증은 전역 ValidationPipe.** `whitelist: true`, `transform: true`로 DTO 밖 필드를 걸러내고 타입 변환.
6. **에러는 RFC 9457로 통일.** 예외 필터에서 `application/problem+json` 형태로 매핑한다. 프로젝트에 이미 에러 포맷이 있으면 원칙 1에 따라 그것을 따른다.
7. **민감 데이터는 안전하게 다룬다.** 비밀번호·토큰 같은 자격증명은 **평문으로 저장·로그·응답에 노출하지 않는다.** 비밀번호는 해셔(bcrypt/argon2) 프로바이더로 해시해 저장한다. 이건 "나중에 처리" 주석으로 미루지 말고 **처음부터 코드로 반영**한다. 상세는 `references/security.md`.
8. **비밀값은 외부화.** 자격증명·토큰을 코드/커밋에 하드코딩하지 않고 `ConfigModule`+환경변수로.

## 작업별 참조

| 작업 | 참조 |
| --- | --- |
| 모듈 구조·CLI·tsconfig 전제 | `references/project-layout.md` |
| 컨트롤러·요청/응답 DTO·검증·상태코드 | `references/web-layer.md` |
| 서비스(프로바이더)·DI·트랜잭션 | `references/service-layer.md` |
| Prisma 스키마·PrismaService·쿼리·페이지네이션 | `references/persistence-layer.md` |
| 예외 필터·에러 응답(RFC 9457) | `references/exception-handling.md` |
| 비밀번호 해싱·민감 데이터·인증 기본 | `references/security.md` |
| ConfigModule·환경변수·시크릿 외부화 | `references/configuration.md` |
| Jest 단위·e2e·테스트 DB | `references/testing.md` |

## 산출물 정렬

프로젝트나 워크플로우에 **선행 설계 산출물이 있으면 그대로 코드에 반영**한다(없으면 요청만으로 작업한다):

- **API 설계 문서**(엔드포인트·상태코드·에러 포맷)가 있으면 컨트롤러·응답·상태코드를 거기에 맞춘다.
- **DB 스키마/마이그레이션 설계**가 있으면 `schema.prisma`의 모델·제약·인덱스를 거기에 맞춘다.
- 에러 포맷 기본값은 **RFC 9457**이되, 설계 문서나 기존 코드에 다른 규약이 있으면 그것을 따른다.

## 테스트

`references/testing.md`는 **테스트 계층 선택·목 전략의 규약 참조**다. 이 스킬의 기본 책임은 구현과 **기존 테스트 실행을 통한 회귀 확인**까지다. 새 테스트를 대량으로 작성하는 일은, 프로젝트 워크플로우에 테스트 전담 에이전트/단계가 있다면 그쪽에 위임할 수 있다(위임 경계가 있으면 존중한다). 그런 경계가 없으면 `testing.md`의 규약대로 직접 작성한다.

## 검증

구현 후 반드시 빌드·기존 테스트를 실행해 회귀가 없는지 확인한다:
- 빌드/타입체크: `npm run build` (tsc) — 타입 에러가 없어야 한다.
- 린트: `npm run lint`
- 테스트: `npm test`(단위) / `npm run test:e2e`(e2e)
- Prisma: 스키마 변경 시 `npx prisma generate`, 마이그레이션은 `npx prisma migrate dev` / 배포는 `migrate deploy`.

실행한 명령과 결과를 그대로 보고한다. 통과했다고 꾸미지 않는다.
