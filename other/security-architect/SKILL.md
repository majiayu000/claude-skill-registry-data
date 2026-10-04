---
name: security-architect
description: >
  Designs the security of an already-exposed servlet REST use case with Spring Security — who
  may call each endpoint (public, authenticated, role, group, scope, or only the resource's
  owner), how the caller authenticates (OAuth2 resource server with JWT, opaque-token
  introspection, users owned by the application, API key), the project-wide filter chain, 401
  and 403 bodies, CORS, Actuator and Swagger exposure — into the `32-seguranca.md` partial. Use
  when the request involves securing an endpoint, roles, groups, permissions, "only admins",
  "only the owner can", "the user can only see their own", JWT, Keycloak, Auth0, Cognito,
  OAuth2, API key, 401/403, CORS, or protecting Actuator. Servlet only — not WebFlux. Piece of
  the `/new-feature` pipeline: requires `30-rest.md` in the given folder and stops without it.
argument-hint: "[path of the UC-NNN-<slug> folder]"
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion, Bash(find:*), Bash(ls:*), Bash(grep:*), Bash(sort:*)
model: opus
---

## Available specs

!`find "${CLAUDE_PROJECT_DIR:-.}/docs/use-cases" -mindepth 1 -maxdepth 1 -type d -name 'UC-*' 2>/dev/null | sort`

Empty above → none yet, run `/use-case-design` first. (`find`, not an `ls` glob: under zsh an unmatched glob
aborts the command before any fallback runs.)

## Target

$ARGUMENTS

---

# Security Architect

Designs **who may call each endpoint and how the caller proves who it is**: the authentication
mechanism of the project, the request rules and method-security annotations of each endpoint,
the claims-to-authorities mapping, the ownership check a use case runs, and what the API
answers when the proof or the permission is missing. What `use-case-design` recorded as the
case's `Access` and `rest-api-architect` exposed as endpoints, this skill puts behind the
right door.

**Scope: servlet applications.** Spring MVC on the servlet filter chain. A reactive
application (WebFlux, `SecurityWebFilterChain`) has another filter model and is out of scope
here — say so and stop when the project's web starter is the reactive one.

**Entry rule: without `30-rest.md` there is nothing to protect.** This skill reads
`docs/use-cases/UC-NNN-<slug>/00-caso-de-uso.md`, `10-dominio.md` and `30-rest.md` and treats
them as a contract. Without the REST partial it stops and tells the caller to run
`/rest-api-architect` — access rules written before the endpoints exist protect a guess.

It runs when at least one holds, and only then:

| `00-caso-de-uso.md` § `Access` | Project on disk | What it designs |
|---|---|---|
| A role, a group, a scope, or the owner | any | The rules of this case — plus the project-wide setup when none exists yet |
| Authenticated | no `SecurityFilterChain` yet | The project-wide setup — the first secured case |
| Public | a `SecurityFilterChain` exists | The `permitAll` line and its recorded reason |

None holds — public in an unsecured project, or authenticated in a project whose chain already
denies by default — stop and say which: there is nothing to add, and the consolidated spec
records that the case is covered. An `00-caso-de-uso.md` with no `Access` row (written before
the row existed) is not a reason to stop: ask the question in step 3, and record the answer as
a divergence.

**Exit rule: writes no code.** It emits `32-seguranca.md`. The configuration classes, the
annotations on the controllers and the handlers come from the executor agent, which reads the
partial and the exemplars in `templates/`.

**Rule rule: rules don't live here.** Deny by default, where each check lives, the mechanism
requirements, stateless and CSRF, CORS, the failure bodies and the three-way endpoint proof are
`@.claude/rules/authorization.md`. The statuses are `@.claude/rules/api-rest.md`. This skill
applies and cites them; it doesn't reproduce them.

## How it's invoked

Two paths: `/security-architect` by hand, or chained by `/new-feature` right after REST and
before messaging, jobs and persistence. That's why it does **not** carry
`disable-model-invocation` — a skill the model can't see is a skill the orchestrator can't call
(`@.claude/decisions/0007-pipeline-skills-invocation.md`). The guard against firing out of
order is the entry rule above.

## Why this is a skill and not a subagent

Form 1, motivated by axes 2 and 9 of the designer's interview: access is decided per use case,
behind a mechanism decided once per project, and no piece owned either — the `authorization.md`
norm sat in the planned list with no reader. The closest rejected form was a security block
inside `rest-api-architect`: it would re-interview a project-wide mechanism inside a
per-endpoint skill and load security content into every REST run, public endpoints included. A
subagent fails the counter-test on all three points: the interview is the task, the reference
fits in `references/` and `templates/`, and the partial is short.

Pinned to `opus`: the partial is what the executor implements verbatim, and an access rule
designed wrong opens an endpoint in silence (`@.claude/decisions/0081-skill-model-required-per-class.md`).
Design record: `@.claude/decisions/0112-security-architect-skill.md` (this repository only).

## Boundary with neighboring skills

| Piece | Decides | Never decides |
|---|---|---|
| `use-case-design` | The business fact `Access`: anyone, any authenticated caller, named roles or groups, only the owner (and who may override it) | Mechanism, annotation, status |
| `domain-modeling` | When `Access` is the owner: the actor the command carries, the owner field on the aggregate, the invariant and the not-found exception it raises | Where the actor comes from |
| `rest-api-architect` | Endpoints, DTOs, the domain error map | Who may call them; the 401/403 rows |
| **this skill** | Mechanism, claims-to-authorities mapping, request rules and method-security per endpoint, the `permitAll` list with reasons, project-wide setup, 401/403 bodies, CORS, Actuator and OpenAPI exposure, how the controller resolves the actor | Tables and columns, the ownership invariant, test shape |
| `persistence-architect` | The final form of a credentials or API-key table this skill asks for | Who may read it |
| `test-architect` | The test shape for every case § 10 lists | Which cases exist |

Two facts cross that line, and each has one owner:

- **The actor in the command** is `10-dominio.md`'s. This skill names where the controller reads
  it from (the principal's claim) in § 5; if the domain partial has no actor while `Access` is
  the owner, that is a requirement to report upstream, never a command field added here.
- **The 401 and 403 rows** of the error map are this partial's § 6. `30-rest.md`'s error map
  keeps the domain rows; consolidation merges both, and this partial wins on the two statuses.

## Procedure

1. **Read the specs.** `00-caso-de-uso.md` (its `Access` row and trigger), `10-dominio.md`
   (command fields, the ownership invariant when there is one), `30-rest.md` (endpoints,
   `operationId`s, error map, the OpenAPI block). Without `30-rest.md`, stop. Apply the entry
   rule.

2. **Survey — every answer the project already gave is inherited, never re-asked.**

   ```bash
   # Stack and mechanism already in the build
   grep -nE "spring-boot-starter-(security|oauth2-resource-server|webflux|web\b|webmvc)" pom.xml build.gradle* 2>/dev/null
   # Security wiring already in the code
   grep -rnE "SecurityFilterChain|@EnableMethodSecurity|oauth2ResourceServer|opaqueToken|httpBasic|UserDetailsService|ApiKey" --include='*.java' src/main 2>/dev/null
   grep -rnE "@PreAuthorize|@PostAuthorize|@Secured|@RolesAllowed" --include='*.java' src/main 2>/dev/null
   # Decisions earlier use cases recorded
   find docs/use-cases -name '32-seguranca.md' 2>/dev/null
   grep -rnE "spring\.security|springdoc|management\.endpoints|app\.security" src/main/resources 2>/dev/null
   ```

   And the active blueprint's `packages.map`: the entry ending in `.config` is where the wiring
   goes; with none (hexagonal, onion), a `security` subpackage of the entry ending in `.rest`.
   Never a package chosen inside this use case.

   | Fact | Inherited from | Asked only when |
   |---|---|---|
   | Mechanism | The starters in the build, the chain on disk, or an earlier `32-seguranca.md` § 2 | None exists — first secured case of the project |
   | Where roles and groups live in the token, prefixes, audience | The converter on disk or an earlier § 3 | Same |
   | Role and group catalog | Constants on disk (`Roles`, `Groups`) or earlier § 3 | A name `Access` uses is not in it yet — added, not asked |
   | OpenAPI / Swagger exposure, Actuator operator role, CORS origins, headers | The chain on disk or an earlier § 4 | Same as mechanism |

   **The first secured case owns every endpoint already on disk.** Deny by default turns every
   endpoint an earlier case published as public into a 401 on the next deploy. List each
   controller mapping step 2 found with no rule, and decide with the user, endpoint by endpoint,
   `permitAll` with a reason or protected from now on — rows in `## Impact on approved use
   cases`, never a silent change of behavior. **The same goes for their web tests:** once the
   security starter is on the classpath, every existing web-slice test runs behind a filter
   chain it never knew about and answers 401. Each existing controller test is an impact row
   too — it imports the project's chain and sends a credential, or proves the public row
   public; § 10 lists them so `test-architect` plans the change.

3. **Interview — only what step 2 did not settle.** `AskUserQuestion`, at most 4 questions per
   call and **never fewer than 2 real options** per question; an axis with one sensible answer
   is decided and recorded (`@CLAUDE.md` § Known pitfalls). Every option states its cost, the
   way `jobs-architect` puts the tables a tool adds inside the option text.

   | Axis | Decides | Skip when |
   |---|---|---|
   | **Mechanism** — who issues the credential: an external identity provider (signed token), a provider that only issues opaque tokens or must revoke instantly, the application itself (users and passwords here), or a machine with a static key | § 2, through `references/mechanism-decision-matrix.md` | Inherited |
   | **Token shape** — where roles and groups sit (a flat `roles` claim, `realm_access.roles`, `groups`, `scope`), the audience this API expects | § 3 | Inherited, or mechanism is not a token |
   | **Roles per endpoint** — which named roles or groups `Access` means, per operation | § 1 | `Access` names them one to one |
   | **Owner override** — may an administrator act on another user's resource? | Whether the actor's roles travel in the command | `Access` is not the owner |
   | **API docs** — OpenAPI document and Swagger UI public, or protected too | § 4 | Inherited |
   | **Browser client** — does a browser on another origin call this API, and from which origins? | CORS in § 4 | Inherited |
   | **Operator role** — which authority reads the actuator endpoints beyond health and info | § 4 | Inherited |

   Never ask about statuses (`@.claude/rules/api-rest.md` decides), annotations, or class
   names — the same checklist `use-case-design` applies before every question.

4. **Choose the mechanism.** Apply `references/mechanism-decision-matrix.md` § 2: the first row
   that matches wins. A second mechanism for the same callers is a divergence to report and ask
   about, never added because one endpoint looked easier with it
   (`@.claude/rules/authorization.md` § Mechanism). Record the winner, the row that decided it,
   one line per rejected mechanism, and the exemplar it maps to:

   | Mechanism | Exemplars |
   |---|---|
   | Resource server, signed token | `templates/SecurityConfig.java.example` + `templates/JwtResourceServerConfig.java.example` |
   | Resource server, opaque token | `templates/SecurityConfig.java.example` + `templates/OpaqueTokenResourceServerConfig.java.example` |
   | Users owned by the application | `templates/SecurityConfig.java.example` + `templates/LocalUsersSecurityConfig.java.example` |
   | API key (machines) | `templates/SecurityConfig.java.example` + `templates/ApiKeyAuthenticationConfig.java.example` |

5. **Fix the access of each endpoint — § 1.** One row per operation of `30-rest.md`: method,
   path, `operationId`, the rule (public · authenticated · role · group · scope · owner), where
   it is enforced (request rule in the chain, or method security on the controller), the
   meta-annotation when the expression repeats (`templates/MethodSecurityAnnotations.java.example`),
   and the three outcomes the rule's § Tests requires. A public row carries its reason.
   Ownership rows say "authenticated in the chain, owner in the use case" — never a SpEL bean
   call (`@.claude/rules/authorization.md` § Boundary).

   **Where the actor comes from.** For every endpoint whose command carries an actor, name the
   principal attribute the controller reads (the token's subject, a claim, the username) and the
   value object it becomes — shape in `templates/CurrentActorResolution.java.example`. The
   controller resolves it; the command receives it; no use case reads the security context.

6. **Fix the project-wide setup — § 4.** Once per project: NEW in the first secured case,
   REUSE afterwards, CHANGE when this case adds a matcher, a role constant or an origin. Each
   component with its exemplar:

   | Component | Exemplar |
   |---|---|
   | Filter chain: stateless, CSRF justified, headers, CORS, request rules in specific-to-general order, deny by default, OpenAPI and Actuator matchers | `SecurityConfig.java.example` |
   | Mechanism wiring | the row of step 4 |
   | 401 entry point and 403 access-denied handler writing Problem Details | `ProblemDetailSecurityHandlers.java.example` |
   | Translation of a method-security denial ahead of the 500 fallback | `SecurityExceptionHandler.java.example` |
   | Method security and the role/group catalog | `MethodSecurityAnnotations.java.example` |
   | Denial and authentication-failure log and metric | `SecurityAuditListener.java.example` |
   | Bearer scheme in the OpenAPI document | `OpenApiSecurityConfig.java.example` |
   | Properties | `application-security.yml.example` |

7. **Fix ownership — § 5.** When `Access` is the owner: the aggregate's owner field and the
   invariant from `10-dominio.md` (cited, not redesigned), the outcome when the actor is not the
   owner — the not-found exception the domain already raises for an absent aggregate, so
   existence is not revealed (`@.claude/rules/authorization.md` § Failure responses) — and the
   override, when step 3 granted one, as the role the command carries. Missing in
   `10-dominio.md` → a requirement to `domain-modeling` in § 11, and the report says the folder
   is not consistent until that partial is updated.

8. **Fix failure responses — § 6.** 401 and 403 per endpoint, the `WWW-Authenticate` header,
   the body shape (`@.claude/rules/api-rest.md` § Error body), and the 404 that replaces 403 for
   ownership. These rows are merged into the error map at consolidation, and this partial wins
   on them.

9. **Hand persistence what it needs — § 7, requirements only.** Users owned by the
   application → the credentials store (username, password hash, enabled flag, roles) and the
   outbound port the user-details service calls; API key → the key store (key id, hash, owner,
   created and revoked timestamps). Named by what they are, never DDL — the same discipline
   `jobs-architect` keeps. `none` for a token mechanism: the provider holds the credentials.

10. **Declare dependencies — § 8.** The security starter, and the resource-server starter for
    a token mechanism. Version column empty: the Boot parent manages both — read `pom.xml`
    first, and never write a version from memory (`@CLAUDE.md` invariant 8). The artifact
    names change between Boot majors too (the resource-server starter gained a `security-`
    infix); take them from what the Initializr's `security` and `oauth2-resource-server`
    dependency ids resolve to for the project's Boot version, never from an older project. The test support
    library is `test-architect`'s § 5, not this list. The executor may write `pom.xml` for
    exactly these rows.

11. **Fix configuration — § 9.** Every property the setup reads (issuer, audiences,
    introspection endpoint and client, CORS origins, the API-key header name), its value per
    profile, and the environment variable behind each secret — never a literal
    (`@.claude/rules/authorization.md` § Credentials and logs). Shape in
    `templates/application-security.yml.example`.

12. **List the contract test cases — § 10.** Per endpoint, the three outcomes of step 5, plus
    the other-actor case at the use case for every ownership row. `test-architect` turns them
    into tests with its own exemplar; this skill only fixes which cases exist.

12b. **Decide the design patterns of this layer.** Run
    `@.claude/skills/gof-design-patterns/SKILL.md` § Design-time use over what this case adds —
    a claims converter that composes several sources is the usual row (Composite), a growing
    `if` over authentication types the usual symptom. The answer goes into `## Design
    patterns` — `none` when nothing matches, and absence is not `none`.

13. **Write the partial.** `docs/use-cases/UC-NNN-<slug>/32-seguranca.md`, from
    `templates/security-spec.md.example`. Eleven numbered blocks plus `## Design patterns`,
    all mandatory, each `none` when empty — absence is not `none`.

14. **Report and stop.** File path; the mechanism and whether it was inherited; the access
    table in one line per endpoint; every `permitAll` with its reason; § 7 and § 8 as lists;
    the requirements to other partials (§ 11). Don't invoke anyone: messaging, jobs and
    persistence run next, and persistence reads § 7 in its first pass.

## What the partial contains

| Block | Fixes |
|---|---|
| 1 · Access per endpoint | Method, path, `operationId`, rule, where enforced, meta-annotation, the three outcomes; a reason on every public row |
| 2 · Mechanism | The mechanism, the matrix row that chose it, the rejected ones, inherited or not, exemplars |
| 3 · Authorities | Where roles, groups and scopes sit in the credential, the prefixes, the audience, the role and group catalog (NEW or REUSE constants) |
| 4 · Project-wide setup | Each component of step 6 with NEW / REUSE / CHANGE; default access; OpenAPI and Actuator exposure; CORS origins; CSRF and headers with their reasons |
| 5 · Ownership | Owner field, actor and its source, the not-owner outcome, the override role — or `none` |
| 6 · Failure responses | 401 / 403 / 404 per endpoint, header, body |
| 7 · Schema requirements | Credential or key store and its port — requirements, never DDL. `none` for a token mechanism |
| 8 · Declared dependencies | Coordinates, version empty when managed |
| 9 · Configuration | Every property, its value per profile, the environment variable behind each secret |
| 10 · Contract test cases | Per endpoint: anonymous, without authority, with authority; per ownership row, the other actor |
| 11 · Deferred and requirements to other partials | Same shape as every partial's `Deferred`, plus each requirement upstream (an actor `10-dominio.md` lacks) |
| Design patterns | Each pattern adopted — step 12b. `none` when none |

Plus `## Impact on approved use cases` and `## Implementation order`, as in every partial.

The exemplars in `templates/` are a **shape reference**, not files to copy. They target the
servlet stack and the Spring Security generation the project's Boot parent manages; the
links they follow are in `references/servlet-reference-links.md`.

## Contract

**Class:** design — the territory is `skill_classes.design` in
`@.claude/schemas/extensions.json`, and `ArchHook.java guard` enforces it. Writes inside the use
case folder and nothing else; a `SecurityConfig` written under `src/` is refused with exit 2.

**Reads** `docs/use-cases/UC-NNN-<slug>/00-caso-de-uso.md`, `10-dominio.md` and `30-rest.md`
(mandatory — stops without the third), earlier cases' `32-seguranca.md`, `pom.xml` (or the Gradle
build), `src/main/resources/application*.yml`, the security wiring on disk, the active
blueprint's `packages.map`, `@.claude/rules/authorization.md`, `@.claude/rules/api-rest.md`,
`@.claude/rules/architecture-ddd.md`, `@.claude/rules/logging.md`,
`@.claude/rules/observability.md`, and `references/`.

**Writes** `docs/use-cases/UC-NNN-<slug>/32-seguranca.md`. Nothing else.

**Owns** the project's authentication mechanism, the claims-to-authorities mapping and the
role and group catalog, each endpoint's access rule and where it is enforced, the `permitAll`
list and its reasons, the project-wide filter chain, the 401 and 403 responses, CORS, and the
OpenAPI and Actuator exposure.

**Does not decide** the use case boundary or its `Access` fact (`00-caso-de-uso.md`), the
actor field, the owner field or the ownership invariant (`10-dominio.md`), endpoints and domain
error rows (`30-rest.md`), tables and columns (`20-persistencia.md`), or the test shape
(`40-testes.md`). Does not write Java, `pom.xml` or `application.yml` — the executor does, from
this partial. Doesn't touch `.claude/rules/**`. Does not design reactive (WebFlux) security.
