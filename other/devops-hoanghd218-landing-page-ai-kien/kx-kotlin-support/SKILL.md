---
name: kx-kotlin-support
description: |
  Kotlin 멀티프로젝트 라이브러리 개발 지원 - AWS 서비스 통합(Kinesis, DynamoDB, S3, Lambda, CDK), Spring Boot, JPA, Hibernate, 유틸리티(JSON, CSV, Time, Collection 등).
  Core(최소 의존성), Light(AWS Lambda용), Heavy(Spring Boot + DB용) 3개 서브프로젝트 구조.
  키워드: AWS, Kinesis Task/Worker, CDK CICD, ECS 블루그린, Step Functions, DynamoDB Enhanced, S3 Flow, Spring Batch, QueryDSL, Koin DI, Ktor, kotest
---

# kx_kotlin_support 개발 가이드

## 📋 목차
1. [프로젝트 개요](#1-프로젝트-개요)
2. [서브프로젝트 구조](#2-서브프로젝트-구조)
3. [코딩 표준 및 컨벤션](#3-코딩-표준-및-컨벤션)
4. [주요 패키지 가이드](#4-주요-패키지-가이드)
5. [일반적인 사용 패턴](#5-일반적인-사용-패턴)
6. [테스트 작성 가이드](#6-테스트-작성-가이드)
7. [트러블슈팅](#7-트러블슈팅)
8. [요약 테이블](#8-요약-테이블)

---

## 1. 프로젝트 개요

kx_kotlin_support는 Kotlin 기반의 멀티프로젝트 유틸리티 라이브러리입니다.

### 핵심 가치
- **AWS 네이티브**: Kinesis, DynamoDB, S3, Lambda 등 AWS 서비스와 깊은 통합
- **Kotlin 스러운 코드**: 불변성, Flow, DSL, 확장 함수 중심 설계
- **3단계 의존성 관리**: Core → Light → Heavy 계층 구조
- **실전 검증**: 프로덕션 환경에서 검증된 패턴과 유틸리티

### 아키텍처

```
┌─────────────┐
│   Heavy     │  Spring Boot, JPA, Hibernate, AWS CDK
│             │  (웹서버 + RDS 환경)
└─────────────┘
       ↓
┌─────────────┐
│   Light     │  AWS SDK, Koin, Ktor, External APIs
│             │  (AWS Lambda 환경)
└─────────────┘
       ↓
┌─────────────┐
│    Core     │  최소 의존성 (JSON, CSV, Time, Collection)
│             │  (모든 환경)
└─────────────┘
```

### 주요 사용 사례
- AWS Lambda에서 대용량 CSV 파일 실시간 처리
- AWS CDK로 ECS 블루그린 배포 인프라 구축
- Spring Boot 웹 애플리케이션 + QueryDSL + JPA
- Kinesis Task/Worker 패턴으로 비동기 대량 데이터 처리
- Step Functions로 복잡한 배치 워크플로우 구현

---

## 2. 서브프로젝트 구조

### Core 프로젝트
**목적**: 최소한의 의존성으로 모든 환경에서 사용 가능한 핵심 유틸리티

**주요 특징**:
- AWS SDK 의존성 없음
- Spring 의존성 없음
- 순수 Kotlin + 기본 라이브러리만 사용

**핵심 패키지**:

| 패키지 | 주요 기능 | 설명 |
|--------|-----------|------|
| `net.kotlinx.ai` | AI 텍스트 모델 클라이언트 | AI 모델 연동, 텍스트 입출력 처리 |
| `net.kotlinx.calculator` | 배치 처리 진행률 계산 | 대용량 배치 작업의 청크 분할 및 진행률 추적 |
| `net.kotlinx.collection` | 컬렉션 확장 함수 | List/Map/Set 등의 확장 함수 (diff, flattenAny, groupByFirstCondition 등) |
| `net.kotlinx.concurrent` | 동시성 처리 | 코루틴 실행기, 스레드 관리, StopWatch, CacheMap, MicroBatchQueue |
| `net.kotlinx.core` | 핵심 유틸리티 | 클래스 로딩, 데이터 변환, KDSL, 패키지명 처리 |
| `net.kotlinx.csv` | CSV 파일 처리 | CSV 읽기/쓰기, 집계, Flow 변환 |
| `net.kotlinx.delegate` | 델리게이트 패턴 | Map 기반 속성 델리게이트 (MapAttribute) |
| `net.kotlinx.domain` | 도메인 모델 | 개발자 정보, 메뉴, 쿼리, 트리 구조 등 공통 도메인 |
| `net.kotlinx.exception` | 예외 처리 | KnownException, 예외 체이닝 유틸리티 |
| `net.kotlinx.file` | 파일 처리 | Gzip/Zip 압축, 파일명 처리, 랜덤 셔플 |
| `net.kotlinx.flow` | Flow 확장 | Kotlin Flow 확장 함수 |
| `net.kotlinx.html` | HTML 생성 | HTML 태그 빌더, htmx 지원 |
| `net.kotlinx.id` | ID 생성기 | GUID 대용량 채번기 (하이/로우 방식) |
| `net.kotlinx.io` | 입출력 리소스 | InputResource/OutputResource 추상화 |
| `net.kotlinx.json` | JSON 처리 | Gson/Koson/JsonPath/Serialization 지원 |
| `net.kotlinx.number` | 숫자 확장 | Int/Long/Double/Boolean 확장 함수, 숫자 단축 표현 |
| `net.kotlinx.regex` | 정규식 | 정규식 유틸리티 및 확장 |
| `net.kotlinx.retry` | 재시도 로직 | 백오프 지원 재시도 템플릿 |
| `net.kotlinx.string` | 문자열 확장 | 문자열 변환/검증/암호화, 한글 처리, 결과 데이터 래퍼 |
| `net.kotlinx.system` | 시스템 유틸리티 | OS 타입, 배포 타입, 리소스 홀더, 시스템 구분자 |
| `net.kotlinx.time` | 시간/날짜 처리 | LocalDate/LocalDateTime/Duration 확장, 타임존 처리 |
| `net.kotlinx.validation` | 검증 | Bean Validation, Konform, 조건부 검증 |
| `net.kotlinx.xml` | XML 처리 | XML 데이터 파싱 및 처리 |

### Light 프로젝트
**목적**: AWS Lambda 환경에서 사용하는 AWS 서비스 통합 및 외부 API 연동

**주요 특징**:
- AWS SDK v2 (Kotlin) 사용
- Koin DI 통합
- Ktor 클라이언트 기반 HTTP 통신
- Lambda SnapStart 최적화

**핵심 패키지**:

| 패키지 | 주요 기능 | 설명 |
|--------|-----------|------|
| `net.kotlinx.aws.athena` | Athena 쿼리 | CloudTrail 등 테이블 정의, 쿼리 실행 및 결과 조회 |
| `net.kotlinx.aws.batch` | AWS Batch | 배치 작업 제출 및 관리 |
| `net.kotlinx.aws.bedrock` | Bedrock AI | Claude 등 AI 모델 호출, 프롬프트 관리 |
| `net.kotlinx.aws.cognito` | Cognito | 사용자 풀 관리, 인증/인가 |
| `net.kotlinx.aws.dynamo` | DynamoDB | 테이블 CRUD, Enhanced Client, 멀티 인덱스, Lock 구현 |
| `net.kotlinx.aws.ecs` | ECS | 컨테이너 서비스 관리 |
| `net.kotlinx.aws.eventBridge` | EventBridge | 이벤트 발행 및 구독 |
| `net.kotlinx.aws.firehose` | Firehose | 실시간 로그 스트리밍 |
| `net.kotlinx.aws.kinesis` | **Kinesis** | **실시간 대량 데이터 처리 (Task/Worker 패턴)** |
| `net.kotlinx.aws.lambda` | Lambda | 람다 함수 호출, 디스패치 패턴 (동기/비동기) |
| `net.kotlinx.aws.logs` | CloudWatch Logs | 로그 그룹/스트림 관리, 쿼리 |
| `net.kotlinx.aws.s3` | S3 | 파일 업로드/다운로드, 버킷 관리, Flow 지원 |
| `net.kotlinx.aws.ses` | SES | 이메일 발송 |
| `net.kotlinx.aws.sfn` | Step Functions | 워크플로우 실행 및 관리 |
| `net.kotlinx.aws.sqs` | SQS | 큐 메시지 발행/구독, Worker 패턴 |
| `net.kotlinx.aws.ssm` | Systems Manager | 파라미터 스토어 관리 |
| `net.kotlinx.dooray` | 두레이 | 두레이 메신저 API 연동 |
| `net.kotlinx.github` | GitHub | GitHub API 연동, 저장소/이슈 관리 |
| `net.kotlinx.google` | Google API | Calendar, Drive, OTP, OAuth, Sheet, Vision 등 |
| `net.kotlinx.koin` | Koin DI | Koin 의존성 주입 확장 |
| `net.kotlinx.ktor` | Ktor | Ktor 클라이언트 확장 |
| `net.kotlinx.notion` | Notion API | Notion 페이지/데이터베이스 CRUD |
| `net.kotlinx.openAi` | OpenAI API | ChatGPT 등 OpenAI 모델 호출 |
| `net.kotlinx.slack` | Slack API | Slack 메시지 발송 및 워크플로우 |

### Heavy 프로젝트
**목적**: Spring Boot 웹 애플리케이션 및 RDS 데이터베이스 환경 지원

**주요 특징**:
- Spring Framework 전체 스택
- JPA + Hibernate + QueryDSL
- AWS CDK 인프라 구축 DSL

**핵심 패키지**:

| 패키지 | 주요 기능 | 설명 |
|--------|-----------|------|
| `net.kotlinx.awscdk` | **AWS CDK** | **AWS CDK DSL (CICD, ECS, Lambda, SFN)** |
| `net.kotlinx.dataframe` | 데이터프레임 | Kotlin DataFrame 라이브러리 확장 |
| `net.kotlinx.excel` | Excel 처리 | Apache POI 기반 엑셀 읽기/쓰기 |
| `net.kotlinx.hibernate` | Hibernate | JPA PostListener, PhysicalNamingStrategy |
| `net.kotlinx.jdbc` | JDBC | JDBC 연결 및 쿼리 실행 헬퍼 |
| `net.kotlinx.jpa` | JPA | Entity 탐색, 컬럼/테이블 정보 추출 |
| `net.kotlinx.kqdsl` | Kotlin QueryDSL | QueryDSL Kotlin 확장 (파라미터, Path 처리) |
| `net.kotlinx.spring` | Spring Framework | Spring Batch, MVC, Security, WebFlux 확장 |

---

## 3. 코딩 표준 및 컨벤션

### 기본 원칙

#### 1. 한글 문서화
- 모든 주석, 로그 메시지, 문서는 한글로 작성
- 표준 용어(AWS 리소스명 등)만 예외적으로 영어 사용

#### 2. Kotlin 스러운 코드
- `var` 사용 최소화 → `val` 선호
- `mutableListOf` 사용 최소화 → 불변 컬렉션 선호
- 확장 함수 적극 활용
- Flow/Sequence 활용한 지연 평가

#### 3. 예외 처리
- 모든 예외는 반드시 처리되어야 함
- 불필요한 `catch` 후 로깅만 하는 패턴 지양
- 의미 있는 예외 처리 또는 상위로 전파

### 로거 사용법

**설정 방식**:
```kotlin
import mu.KotlinLogging

class MyClass {
    companion object {
        private val log = KotlinLogging.logger {}
    }
}
```

**로그 작성 시**:
```kotlin
// ✅ 올바른 방식 - {} 블록 사용
log.info { "데이터 ${data.size}개 처리 완료" }
log.warn { "재시도 실패: ${error.message}" }
log.debug { " -> 결과: $result" }

// ❌ 잘못된 방식 - 즉시 평가
log.info("데이터 ${data.size}개 처리 완료")  // 성능 저하
```

**이유**: `{}` 블록을 사용하면 로그 레벨이 비활성화되었을 때 문자열 보간을 하지 않아 성능이 향상됩니다.

### 파일 구성

#### 1. 클래스당 1개 파일
- 각 클래스는 독립된 파일로 분리
- 파일명 = 클래스명

#### 2. 확장 함수는 xxxSupport.kt 파일에
```
MapSupport.kt        // Map 확장 함수
ListStringSupport.kt // List<String> 확장 함수
S3Support.kt         // S3 관련 확장 함수
```

#### 3. 테스트 코드 위치
```
src/test/kotlin/net/kotlinx/[패키지명]/[클래스명]Test.kt
```

### AWS SDK 사용 패턴

**Paginated Flow 사용**:
```kotlin
// ✅ 올바른 방식 - Paginated Flow
fun listAllUsers(userPoolId: String): Flow<User> =
    cognito.listUsersPaginated {
        this.userPoolId = userPoolId
    }.flatMapConcat { it.users!!.asFlow() }

// ❌ 잘못된 방식 - 단일 페이지만 가져옴
fun listUsers(userPoolId: String): List<User> =
    cognito.listUsers {
        this.userPoolId = userPoolId
    }.users!!
```

**이유**: AWS SDK의 List 계열 API는 기본적으로 페이징되어 있습니다. 전체 데이터를 가져오려면 Paginated Flow를 사용해야 합니다.

### Retrofit2 생성 규칙

1. **REST API 1건당 1개 인터페이스**
2. **관련 데이터 객체는 같은 파일 내 정의**
3. **모든 인터페이스와 데이터 객체는 같은 접미어 사용**

예시:
```kotlin
// DoorayDriveApi.kt
interface DoorayDriveApi {
    @GET("/api/drive/files")
    suspend fun listFiles(): DoorayDriveListResponse

    // 관련 데이터 객체
    data class DoorayDriveListResponse(
        val files: List<DoorayDriveFile>
    )

    data class DoorayDriveFile(
        val id: String,
        val name: String
    )
}
```

### Spring Framework 규칙

**성공 응답**:
```kotlin
// Spring Controller에서 성공 메시지 리턴 시
@PostMapping("/save")
fun save(@RequestBody data: MyData): ApiResponse {
    myService.save(data)
    return ApiResponse(true, "데이터가 저장됨")
}
```

### IDE 컴파일 확인
- 작업 후 IDE의 컴파일 에러만 확인
- 별도의 gradle 명령은 실행하지 말 것

---

## 4. 주요 패키지 가이드

### 4.1 AWS Kinesis 실시간 대량 처리

**핵심 개념**: Task/Worker 패턴으로 Kinesis를 통한 비동기 대량 데이터 처리

**요구사항**:
1. 고속 / 병렬 처리가 저렴하게 가능 (샤드1개 월 1.3만원으로 초당 1000개 처리)
2. 수평 확장/축소 가능 (런타임에 샤드 수 조정 가능)
3. 대용량 데이터 처리 가능 (청크단위 요청/응답 처리)
4. 실시간에 가까운(1초 이내도 가능) 반응
5. 요청 / 응답을 flow로 간단하게 사용할 수 있어야함
6. timeout 기능이 있어야 함

#### KinesisTask (요청자)

```kotlin
val task = KinesisTask {
    streamName = "worker-stream"
    checkpointTableName = "system-dev"
    taskName = "demoTaskJob"
    checkpointTtl = 1.hours
}

// 대용량 파일을 Flow로 읽어서 처리
val file: File by ResourceHolder.WORKSPACE.slash("largeFile.csv") lazyLoad "s3://xxxa/demo/largeFile.csv"
val flow = file.toInputResource().toFlow()
    .map { line ->
        json {
            "id" to line[0]
            "query" to line[1]
        }
    }
    .chunked(1000)

// Task 실행 - 결과를 Flow로 수신
task.execute(flow).collect { datas ->
    datas.forEach {
        log.debug { " => [${it}]" }
    }
}
```

#### KinesisWorker (처리자)

```kotlin
val worker = KinesisWorker {
    streamName = "worker-stream"
    checkpointTableName = "system-dev"
    handler = { records ->
        log.info { "워커 테스트: ${records.size}개의 레코드 처리" }
        records.forEach {
            it.result.put("processed", true)
            it.result.put("time", java.time.LocalDateTime.now().toKr01())
            log.debug { " -> ${it.result}" }
            100.milliseconds.delay() //0.1초에 1개씩 처리
        }
    }
    readChunkCnt = 100
    shardCheckInterval = 10.minutes
}
worker.start()
```

**사용 시나리오**:
- 대용량 CSV 파일 처리 (수십만~수백만 건)
- 실시간에 가까운 처리 필요 (1초 이내 반응)
- 수평 확장 가능 (샤드 수 조정)
- 비용 효율적 (샤드 1개 = 월 1.3만원, 초당 1000개 처리)

**주의사항**:
- 오류 처리시 중단시점부터 재시도하는 기능은 없음
- collector를 csv로 만들어서 셀프 구현 필요

---

### 4.2 AWS CDK 인프라 구축

#### CICD 파이프라인 (GitHub + CodeBuild + CodePipeline)

```kotlin
val stack = this
val infra = koin<MyInfra>()
val workBucket = infra.s3.work.load(stack)
val appRole = MyRole.APP_ADMIN.load(stack)
val securityGroup = MySecurityGroup.JOB.load(stack)
val toAdmin = infra.topic.adminAll.load(stack)

val build = CdkCodeBuild {
    chacheBucket = workBucket.iBucket
    role = appRole.iRole
    vpc = infra.vpc.iVpc
    securityGroups = listOf(securityGroup.iSecurityGroup)
    concurrentBuildLimit = 1 //AWS 오류..
    gradleVersion = "8.12.1"
    gradleCmds(":deployAll")
    byGithub(MyProject.GITHUB_ROOT, MyProject.PROJECT_DMP)
    create(stack)
}

CdkCodePipeline {
    codeBuild = build.codeBuild
    role = appRole.iRole
    topics = listOf(toAdmin)
    events = when (deploymentType) {
        DeploymentType.PROD -> listOf(EventSets.CodekPipeline.FAILED) //후킹이 걸려있기 때문에 빌드 성공은 필요없음
        DeploymentType.DEV -> listOf(EventSets.CodekPipeline.FAILED, EventSets.CodekPipeline.SUCCESSED)
    }
    byGithub(MyProject.GITHUB_ROOT, MyProject.PROJECT_DMP, "arn:aws:codeconnections:ap-northeast-2:xxxx")
    create(stack)
}
```

#### ECS 블루그린 배포

```kotlin
val infra = koin<MyInfra>()
val ecr = infra.ecr.api.load(stack)

val webConfig = MyEcs.ECS_CONFIGS[CdkInterface.DEPLOYMENT_TYPE]!!
val web = CdkEcsWeb {
    name = "api"
    config = webConfig
    taskRole = MyRole.APP_ADMIN.load(stack).iRole
    executionRole = MyRole.ECS_TASK.load(stack).iRole
    image = ecr.imageFromStackByTag(deploymentType.name.lowercase())
    vpc = infra.vpc.load(stack).iVpc
    sgWeb = MySecurityGroup.API.load(stack).iSecurityGroup
    sgAlb = MySecurityGroup.ALB.load(stack).iSecurityGroup
    containerInsights = deploymentType == DeploymentType.PROD
    environment += mapOf(
        AwsNaming.Spring.ENV_PROFILE to "default,${CdkInterface.SUFF}"
    )
    certs = listOf(MySms.CERT_DMP.get(stack))
    healthCheck = HealthCheck.builder()
        .interval(20.seconds.toCdk())
        .timeout(10.seconds.toCdk())
        .healthyThresholdCount(2) //디폴트인 5로 하면 체크 전에 내려갈 수 있음.
        .unhealthyThresholdCount(2)
        .path("/api/healthcheck")
        .build()

    when (CdkInterface.DEPLOYMENT_TYPE) {
        DeploymentType.PROD -> createServiceBlueGreen(stack)  //라이브서버는 블루그린 배포
        DeploymentType.DEV -> createServiceRolling(stack)
    }
    cdkLogGroup.addLogAnomalyDetector(stack)
}

//도메인 등록하기
val hostedZone = HostedZoneUtil.load(stack, "xxx.com")
val domain = MyEcs.DOMAINS[CdkInterface.DEPLOYMENT_TYPE]!!
Route53Util.arecord(stack, hostedZone, domain, web.alb.toRecordTarget())
```

#### Step Functions 대량데이터 분할처리

```kotlin
CdkSfn(project, "batch_step") {
    this.lambda = func
    this.iRole = role.iRole

    val stepStart = lambda("StepStart")
    val stepEnd = lambda("StepEnd")

    val modeMap = listOf(
        mapInline("StepMap") {
            next = stepEnd.stateId
            itemPath = "$.option.${stepStart.stateId}.body.datas"
        },
        stepEnd,
    ).join()

    val listMode = run {
        val stepList = lambda("StepList")
        val waitColdstart = wait("WaitColdstart") {
            this.secondsPath = "${AwsNaming.option}.${AwsNaming.waitColdstartSeconds}"
        }
        val waitIpBlock = wait("WaitIpBlock") {
            this.secondsPath = "${AwsNaming.option}.${AwsNaming.waitSeconds}"
        }
        listOf(
            stepList,
            choice("IsCompleted").apply {
                whenMatchesBody(stepList.stateId, AwsNaming.choiceFirst, waitColdstart, stepList)
                whenMatchesBody(stepList.stateId, AwsNaming.choiceRetry, waitIpBlock, stepList)
                otherwise(stepEnd)
            },
        ).join()
    }

    create(
        stepStart,
        choice("WhenMode").apply {
            whenMatches("mode", "List", listMode)
            otherwise(modeMap)
        },
    )
    onErrorHandle(adminAllTopic, dlq.iQueue)
}
```

---

### 4.3 DynamoDB 사용 패턴

#### Enhanced Client 사용

```kotlin
// 데이터 클래스 정의
@DynamoDbBean
data class UserRecord(
    @get:DynamoDbPartitionKey
    var userId: String = "",

    @get:DynamoDbSortKey
    var timestamp: String = "",

    var name: String = "",
    var email: String = ""
)

// Enhanced Client 사용
val table = dynamoDbEnhancedClient.table("users", TableSchema.fromBean(UserRecord::class.java))

// 저장
table.putItem(UserRecord(
    userId = "user123",
    timestamp = LocalDateTime.now().toIso(),
    name = "홍길동",
    email = "hong@example.com"
))

// 조회
val user = table.getItem(Key.builder()
    .partitionValue("user123")
    .sortValue(timestamp)
    .build())

// 쿼리
val results = table.query { r ->
    r.queryConditional(
        QueryConditional.keyEqualTo(Key.builder()
            .partitionValue("user123")
            .build())
    )
}
```

#### DynamoDB 분산 락

```kotlin
val dynamoLock = DynamoLock {
    aws = awsClient
    tableName = "locks"
    ttl = 5.minutes
}

dynamoLock.withLock("my-resource-id") {
    // 크리티컬 섹션 - 다른 인스턴스에서 동시 실행 방지
    processImportantData()
}
```

---

### 4.4 S3 파일 처리

```kotlin
// S3Data로 경로 관리
val s3File = S3Data.parse("s3://my-bucket/path/to/file.csv")

// 파일 업로드
s3.putObject(s3File, file.readBytes())

// 파일 다운로드
val bytes = s3.getObject(s3File)

// CSV 파일을 Flow로 읽기
val flow: Flow<List<String>> = s3File.toInputResource().toFlow()
flow.collect { line ->
    log.info { "라인: ${line.joinToString(",")}" }
}

// S3에 직접 쓰기 (Flow)
val outputFlow: Flow<String> = flowOf("header1,header2", "value1,value2")
s3File.toOutputResource().writeFlow(outputFlow)
```

---

### 4.5 JSON 처리 (GsonData)

**GsonData**: 동적 JSON 조작을 위한 래퍼 클래스 (타입 안전성 낮지만 유연함)

**주의**: kotlin의 엄격한 객체 정의와 어울리지 않으므로 로직에 가급적 사용 금지. 모든 이상은 예외 대신 null을 리턴함.

```kotlin
// JSON 생성
val json = GsonData.obj {
    put("name", "홍길동")
    put("age", 30)
    put("active", true)
}

// JSON 파싱
val parsed = GsonData.parse("""{"name":"홍길동","age":30}""")

// 값 읽기
val name = parsed["name"].str  // "홍길동"
val age = parsed["age"].int    // 30

// 중첩 접근
val nested = GsonData.parse("""{"user":{"profile":{"name":"홍길동"}}}""")
val userName = nested["user"]["profile"]["name"].str

// JsonPath 사용
val nameByPath = nested["$.user.profile.name"].str

// 배열 처리
val array = GsonData.array {
    add("item1")
    add("item2")
    add(GsonData.obj { put("key", "value") })
}

// 반복
array.forEach { item ->
    log.info { "Item: $item" }
}

// 수정
json.put("age", 31)
json.put("newField", "newValue")

// 삭제
json.remove("active")

// 병합
val json2 = GsonData.obj { put("email", "hong@example.com") }
val merged = json + json2
```

**사용 시나리오**:
- Lambda 함수에서 이벤트 파싱
- 외부 API 응답 처리 (스키마가 유동적인 경우)
- 로그 데이터 집계
- **주의**: 프로덕션 로직에는 가급적 사용 금지 (타입 안전성 부족)

---

### 4.6 CSV 처리

```kotlin
// CSV 파일 읽기
val csvFile = File("/path/to/data.csv")
val records: Flow<List<String>> = csvFile.toInputResource().toFlow()

// CSV 파싱 + 변환
records
    .drop(1)  // 헤더 스킵
    .map { line ->
        User(
            id = line[0],
            name = line[1],
            email = line[2]
        )
    }
    .collect { user ->
        processUser(user)
    }

// CSV 쓰기
val output = File("/path/to/output.csv")
output.toOutputResource().use { resource ->
    resource.writeLine(listOf("ID", "Name", "Email"))  // 헤더
    users.forEach { user ->
        resource.writeLine(listOf(user.id, user.name, user.email))
    }
}

// CSV 집계
val aggregated = csvFile.toInputResource()
    .aggregation<MyCsvLine>()  // 타입 추론
    .sum { it.amount }
```

---

### 4.7 Time 처리

```kotlin
// Duration 확장
val duration = 5.minutes
val milliseconds = duration.toMillis()
duration.delay()  // suspend 함수

// LocalDate 확장
val today = LocalDate.now()
val yesterday = today.minusDays(1)
val formatted = today.toKr01()  // "2025-01-15"

// LocalDateTime 확장
val now = LocalDateTime.now()
val isoFormat = now.toIso()  // "2025-01-15T14:30:00"
val krFormat = now.toKr01()  // "2025-01-15 14:30:00"

// Delay
100.milliseconds.delay()  // suspend 함수
```

---

### 4.8 Spring Batch

```kotlin
@Configuration
class BatchJobConfig {

    @Bean
    fun myJob(
        jobBuilderFactory: JobBuilderFactory,
        stepBuilderFactory: StepBuilderFactory
    ): Job {
        return jobBuilderFactory.get("myJob")
            .start(myStep(stepBuilderFactory))
            .build()
    }

    fun myStep(stepBuilderFactory: StepBuilderFactory): Step {
        return stepBuilderFactory.get("myStep")
            .chunk<InputData, OutputData>(100)
            .reader(itemReader())
            .processor(itemProcessor())
            .writer(itemWriter())
            .build()
    }

    fun itemReader(): ItemReader<InputData> {
        // CSV 또는 DB에서 데이터 읽기
    }

    fun itemProcessor(): ItemProcessor<InputData, OutputData> {
        return ItemProcessor { input ->
            // 데이터 변환
            OutputData(input.id, input.name.uppercase())
        }
    }

    fun itemWriter(): ItemWriter<OutputData> {
        return ItemWriter { items ->
            items.forEach { processOutput(it) }
        }
    }
}
```

---

### 4.9 QueryDSL (kqdsl)

```kotlin
// QueryDSL + Kotlin 확장
val qUser = QUser.user

val results = queryFactory
    .selectFrom(qUser)
    .where(
        qUser.name.eq("홍길동"),
        qUser.age.gt(20)
    )
    .orderBy(qUser.createdAt.desc())
    .fetch()

// 동적 쿼리
fun searchUsers(name: String?, minAge: Int?): List<User> {
    return queryFactory
        .selectFrom(qUser)
        .where(
            name?.let { qUser.name.contains(it) },
            minAge?.let { qUser.age.goe(it) }
        )
        .fetch()
}

// 페이징
val pageable = PageRequest.of(0, 20)
val page = queryFactory
    .selectFrom(qUser)
    .offset(pageable.offset)
    .limit(pageable.pageSize.toLong())
    .fetch()
```

---

### 4.10 Koin DI

```kotlin
// 모듈 정의
val myModule = module {
    single { AwsClient() }  // 싱글톤
    single { S3Client(get()) }  // 의존성 주입
    factory { KinesisTask() }  // 매번 새로운 인스턴스
}

// Koin 시작
startKoin {
    modules(myModule)
}

// 의존성 가져오기
val awsClient: AwsClient by inject()
val s3Client = get<S3Client>()

// 레이지 로딩
val kinesis: KinesisTask by koinLazy()
```

---

## 5. 일반적인 사용 패턴

### 패턴 A: Lambda 함수에서 대용량 CSV 처리

```kotlin
class CsvProcessorLambda : RequestHandler<S3Event, String> {

    private val aws by koinLazy<AwsClient>()
    private val log = KotlinLogging.logger {}

    override fun handleRequest(event: S3Event, context: Context): String {
        event.records.forEach { record ->
            val s3Data = S3Data(record.s3.bucket.name, record.s3.`object`.key)

            // CSV를 Flow로 읽어서 처리
            runBlocking {
                s3Data.toInputResource().toFlow()
                    .drop(1)  // 헤더 스킵
                    .chunked(1000)  // 1000개씩 배치 처리
                    .collect { batch ->
                        processBatch(batch)
                    }
            }
        }
        return "처리 완료"
    }

    private suspend fun processBatch(lines: List<List<String>>) {
        log.info { "${lines.size}개 라인 처리 중..." }
        // DynamoDB 저장, Kinesis 전송 등
    }
}
```

---

### 패턴 B: Spring Boot API에서 페이징 + 엑셀 다운로드

```kotlin
@RestController
@RequestMapping("/api/users")
class UserController(
    private val userRepository: UserRepository,
    private val queryFactory: JPAQueryFactory
) {

    companion object {
        private val log = KotlinLogging.logger {}
    }

    @GetMapping
    fun listUsers(pageable: Pageable): Page<User> {
        val qUser = QUser.user
        return queryFactory
            .selectFrom(qUser)
            .orderBy(qUser.createdAt.desc())
            .offset(pageable.offset)
            .limit(pageable.pageSize.toLong())
            .fetchPage(pageable)
    }

    @GetMapping("/export")
    fun exportToExcel(response: HttpServletResponse) {
        response.contentType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        response.setHeader("Content-Disposition", "attachment; filename=users.xlsx")

        val users = userRepository.findAll()

        ExcelWriter().use { excel ->
            excel.createSheet("Users")
            excel.writeHeader(listOf("ID", "Name", "Email", "Created"))
            users.forEach { user ->
                excel.writeRow(listOf(
                    user.id.toString(),
                    user.name,
                    user.email,
                    user.createdAt.toKr01()
                ))
            }
            excel.write(response.outputStream)
        }
    }
}
```

---

### 패턴 C: AWS CDK로 전체 인프라 구축

```kotlin
class MyStack(scope: Construct, id: String) : Stack(scope, id) {

    init {
        // VPC
        val vpc = CdkVpc {
            create(this@MyStack)
        }

        // Security Groups
        val webSg = CdkSecurityGroup {
            vpc = vpc.iVpc
            description = "Web 서버 SG"
            create(this@MyStack)
        }

        // ECR
        val ecr = CdkEcr {
            repositoryName = "my-app"
            create(this@MyStack)
        }

        // ECS Cluster
        val cluster = Cluster(this@MyStack, "Cluster", ClusterProps.builder()
            .vpc(vpc.iVpc)
            .build())

        // ALB + ECS Service (블루그린)
        val web = CdkEcsWeb {
            name = "api"
            image = ecr.imageFromStackByTag("latest")
            vpc = vpc.iVpc
            sgWeb = webSg.iSecurityGroup
            createServiceBlueGreen(this@MyStack)
        }

        // Route53
        val hostedZone = HostedZoneUtil.load(this@MyStack, "example.com")
        Route53Util.arecord(this@MyStack, hostedZone, "api.example.com", web.alb.toRecordTarget())

        // CodePipeline (CICD)
        val build = CdkCodeBuild {
            gradleCmds(":bootJar", ":jib")
            byGithub("owner", "repo")
            create(this@MyStack)
        }

        CdkCodePipeline {
            codeBuild = build.codeBuild
            byGithub("owner", "repo", "arn:aws:codeconnections:...")
            create(this@MyStack)
        }
    }
}
```

---

### 패턴 D: Kinesis + Lambda 실시간 처리 파이프라인

```kotlin
// Producer: 대용량 데이터를 Kinesis로 전송
class DataProducerLambda : RequestHandler<S3Event, String> {

    companion object {
        private val log = KotlinLogging.logger {}
    }

    private val task = KinesisTask {
        streamName = "data-stream"
        checkpointTableName = "checkpoints"
        taskName = "producerJob"
    }

    override fun handleRequest(event: S3Event, context: Context): String {
        runBlocking {
            val s3Data = S3Data.parse(event.records.first().s3.bucket.name, ...)
            val flow = s3Data.toInputResource().toFlow()
                .map { line ->
                    json {
                        "id" to line[0]
                        "data" to line[1]
                    }
                }
                .chunked(1000)

            task.execute(flow).collect { results ->
                log.info { "${results.size}개 처리 완료" }
            }
        }
        return "OK"
    }
}

// Consumer: Kinesis에서 데이터 읽어서 처리
class DataConsumerLambda {

    companion object {
        private val log = KotlinLogging.logger {}
    }

    private val worker = KinesisWorker {
        streamName = "data-stream"
        checkpointTableName = "checkpoints"
        readerName = "consumer01"

        handler = { records ->
            // DynamoDB에 저장
            records.forEach { record ->
                val data = record.result
                dynamoTable.putItem(...)

                record.result.put("processed", true)
            }
        }
    }

    fun start() {
        runBlocking {
            worker.start()  // 무한 루프로 실행
        }
    }
}
```

---

## 6. 테스트 작성 가이드

### 테스트 기본 구조

**위치**: `src/test/kotlin/net/kotlinx/[패키지명]/`

**형식**: kotest BDD 스타일

```kotlin
class MyServiceTest : BeSpecHeavy() {

    init {
        initTest(KotestUtil.PROJECT)

        Given("사용자 데이터가 준비되어 있을 때") {
            val user = User(
                id = "user123",
                name = "홍길동",
                email = "hong@example.com"
            )

            When("사용자를 저장하면") {
                val saved = userService.save(user)

                Then("정상적으로 저장되어야 한다") {
                    saved shouldNotBe null
                    saved.id shouldBe user.id
                    saved.name shouldBe user.name
                }
            }

            When("존재하지 않는 사용자를 조회하면") {
                Then("null을 반환해야 한다") {
                    val notFound = userService.findById("not-exist")
                    notFound shouldBe null
                }
            }
        }

        Given("여러 사용자가 있을 때") {
            val users = listOf(
                User("user1", "홍길동", "hong@example.com"),
                User("user2", "김철수", "kim@example.com")
            )
            users.forEach { userService.save(it) }

            When("전체 사용자를 조회하면") {
                val all = userService.findAll()

                Then("모든 사용자가 반환되어야 한다") {
                    all.size shouldBeGreaterThanOrEqual 2
                }
            }
        }
    }
}
```

---

### Core 프로젝트 테스트

```kotlin
class CollectionSupportTest : BeSpecLog() {
    init {
        initTest(KotestUtil.FAST)

        Given("리스트가 주어졌을 때") {
            val list = listOf(1, 2, 3, 4, 5)

            Then("chunked가 정상 동작해야 한다") {
                val chunks = list.chunked(2)
                chunks.size shouldBe 3
                chunks[0] shouldBe listOf(1, 2)
                chunks[2] shouldBe listOf(5)
            }
        }
    }
}
```

---

### Light 프로젝트 테스트 (AWS 통합)

```kotlin
class S3ServiceTest : BeSpecLight() {

    private val s3: S3Client by koinLazy()

    init {
        initTest(KotestUtil.INTEGRATION)

        Given("S3 버킷이 있을 때") {
            val bucket = "test-bucket"
            val key = "test/file.txt"
            val s3Data = S3Data(bucket, key)

            When("파일을 업로드하면") {
                val content = "Hello World"
                s3.putObject(s3Data, content.toByteArray())

                Then("파일이 정상적으로 업로드되어야 한다") {
                    val downloaded = s3.getObject(s3Data)
                    String(downloaded) shouldBe content
                }
            }

            xThen("파일을 삭제하면") {  // x = skip
                s3.deleteObject(s3Data)

                shouldThrow<NoSuchKeyException> {
                    s3.getObject(s3Data)
                }
            }
        }
    }
}
```

---

### Heavy 프로젝트 테스트 (Spring + JPA)

```kotlin
@SpringBootTest
class UserRepositoryTest : BeSpecHeavy() {

    @Autowired
    private lateinit var userRepository: UserRepository

    @Autowired
    private lateinit var entityManager: EntityManager

    init {
        initTest(KotestUtil.PROJECT)

        Given("사용자 엔티티가 준비되어 있을 때") {
            val user = User(
                name = "홍길동",
                email = "hong@example.com"
            )

            When("엔티티를 저장하면") {
                val saved = userRepository.save(user)
                entityManager.flush()
                entityManager.clear()

                Then("ID가 자동 생성되어야 한다") {
                    saved.id shouldNotBe null
                }

                Then("저장된 데이터를 조회할 수 있어야 한다") {
                    val found = userRepository.findById(saved.id!!).orElse(null)
                    found shouldNotBe null
                    found.name shouldBe "홍길동"
                }
            }
        }
    }
}
```

---

### Mock 사용 지양 원칙

**CLAUDE.md 가이드**: mock 객체를 사용할 필요 없고 해당 객체를 koin 등으로 가져와서 직접 실행

```kotlin
// ❌ 잘못된 방식 - Mock 사용
class MyServiceTest : BeSpecHeavy() {
    @MockK
    private lateinit var userRepository: UserRepository

    init {
        every { userRepository.findById(any()) } returns User(...)
        // ...
    }
}

// ✅ 올바른 방식 - 실제 객체 사용
class MyServiceTest : BeSpecHeavy() {
    private val userRepository: UserRepository by koinLazy()

    init {
        // 실제 DB 또는 테스트 DB 사용
        userRepository.save(User(...))
        val found = userRepository.findById("user123")
        // ...
    }
}
```

---

## 7. 트러블슈팅

### 문제: Kinesis Task가 타임아웃됨

**증상**: `task.execute()` 호출 후 결과를 받지 못하고 타임아웃

**원인**:
- Worker가 실행되지 않음
- Partition Key가 잘못 설정됨
- Checkpoint 테이블 권한 문제

**해결**:
1. Worker가 실행 중인지 확인
   ```kotlin
   worker.start()  // 별도 프로세스에서 실행 필요
   ```

2. Partition Key 확인
   ```kotlin
   // Task는 "taskName-taskId-in" 형식으로 전송
   // Worker는 "in" 타입만 읽음
   ```

3. DynamoDB 테이블 존재 및 권한 확인
   ```bash
   aws dynamodb describe-table --table-name checkpoints
   ```

---

### 문제: GsonData에서 null 값 처리

**증상**: `gson["key"].str` 호출 시 NPE 발생

**원인**: GsonData는 null을 JsonNull로 래핑하지만, `.str` 호출 시 null 반환

**해결**:
```kotlin
// ✅ 올바른 방식 - null 체크
val value = gson["key"].str ?: "기본값"

// ✅ lett 사용
gson["key"].lett { value ->
    // value가 비어있지 않을 때만 실행
    log.info { "값: ${value.str}" }
}

// ❌ 잘못된 방식
val value = gson["key"].str!!  // NPE 위험
```

---

### 문제: AWS CDK 배포 시 권한 오류

**증상**: `cdk deploy` 실행 시 권한 오류

**원인**: IAM Role에 필요한 권한이 없음

**해결**:
1. CloudFormation 실행 권한 확인
2. 생성하려는 리소스의 권한 확인 (ECS, Lambda 등)
3. 필요시 AdministratorAccess 권한으로 테스트

```kotlin
// Role에 권한 추가
role.addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName("AmazonECSFullAccess"))
```

---

### 문제: Spring Boot에서 QueryDSL Q클래스 생성 안 됨

**증상**: QUser, QOrder 등의 Q클래스를 찾을 수 없음

**원인**: Annotation Processor가 실행되지 않음

**해결**:
1. Gradle에서 kapt 플러그인 확인
   ```kotlin
   plugins {
       kotlin("kapt") version "1.9.0"
   }

   dependencies {
       kapt("com.querydsl:querydsl-apt:5.0.0:jakarta")
   }
   ```

2. IDE에서 빌드 실행
   ```bash
   ./gradlew clean build
   ```

3. IntelliJ에서 "Annotation Processors" 활성화
   - Settings → Build → Compiler → Annotation Processors
   - "Enable annotation processing" 체크

---

### 문제: S3 파일 다운로드 시 메모리 부족

**증상**: 대용량 파일(수 GB) 다운로드 시 OutOfMemoryError

**원인**: 전체 파일을 메모리에 로드

**해결**:
```kotlin
// ❌ 잘못된 방식 - 전체 파일 로드
val bytes = s3.getObject(s3Data)
processBytes(bytes)

// ✅ 올바른 방식 - 스트리밍 처리
s3Data.toInputResource().toFlow()
    .collect { line ->
        processLine(line)  // 라인별 처리
    }
```

---

### 문제: Kotest 테스트가 실행되지 않음

**증상**: IntelliJ에서 테스트 실행 버튼이 표시되지 않음

**원인**: Kotest 플러그인 미설치

**해결**:
1. IntelliJ Kotest 플러그인 설치
   - Settings → Plugins → "Kotest" 검색 → 설치

2. Gradle 의존성 확인
   ```kotlin
   testImplementation("io.kotest:kotest-runner-junit5:5.5.0")
   testImplementation("io.kotest:kotest-assertions-core:5.5.0")
   ```

---

## 8. 요약 테이블

### Core 프로젝트 핵심 클래스

| 패키지 | 핵심 클래스/함수 | 설명 |
|--------|------------------|------|
| `json.gson` | `GsonData` | 동적 JSON 조작 래퍼 |
| `csv` | `InputResource.toFlow()` | CSV → Flow 변환 |
| `time` | `LocalDateTime.toKr01()`, `Duration.delay()` | 시간 확장 함수 |
| `collection` | `List.chunked()`, `Map.flatten()` | 컬렉션 확장 |
| `concurrent` | `CoroutineExecutor`, `CacheMap` | 코루틴 실행기, 캐시 |
| `io` | `InputResource`, `OutputResource` | I/O 추상화 |

### Light 프로젝트 핵심 클래스

| 패키지 | 핵심 클래스/함수 | 설명 |
|--------|------------------|------|
| `aws.kinesis.worker` | `KinesisTask`, `KinesisWorker` | 실시간 대량 처리 (Task/Worker 패턴) |
| `aws.dynamo` | `DynamoDbEnhancedClient`, `DynamoLock` | DynamoDB Enhanced + 분산 락 |
| `aws.s3` | `S3Data`, `S3Client` | S3 파일 처리 |
| `aws.lambda` | `LambdaDispatch`, `LambdaInvoker` | Lambda 함수 호출 패턴 |
| `aws.sqs` | `SqsWorker` | SQS Worker 패턴 |
| `koin` | `koinLazy()`, `inject()` | Koin DI 확장 |
| `notion` | `NotionClient` | Notion API 연동 |
| `openAi` | `OpenAiClient` | OpenAI ChatGPT API |

### Heavy 프로젝트 핵심 클래스

| 패키지 | 핵심 클래스/함수 | 설명 |
|--------|------------------|------|
| `awscdk.cicd` | `CdkCodeBuild`, `CdkCodePipeline` | CICD 파이프라인 (GitHub + CodeBuild) |
| `awscdk.ecs` | `CdkEcsWeb` | ECS 블루그린/롤링 배포 |
| `awscdk.sfn` | `CdkSfn` | Step Functions 배치 처리 |
| `spring.batch` | `SpringBatchSupport` | Spring Batch 확장 |
| `kqdsl` | `KqdslParameterSupport` | Kotlin QueryDSL 확장 |
| `hibernate` | `JpaPostListener`, `PhysicalNamingStrategy` | JPA/Hibernate 확장 |
| `excel` | `ExcelWriter`, `ExcelReader` | Apache POI Excel 처리 |

---

### 빠른 참조: 코딩 체크리스트

개발 시 다음을 확인하세요:

- [ ] **로거**: `companion object` + `KotlinLogging.logger {}` + `log.info { }` 블록 사용
- [ ] **불변성**: `var` → `val`, `mutableListOf` → `listOf` 선호
- [ ] **확장 함수**: 새 확장 함수는 `xxxSupport.kt` 파일에 추가
- [ ] **AWS SDK**: Paginated API는 Flow로 변환 (`flatMapConcat`)
- [ ] **예외 처리**: 모든 예외는 반드시 처리 (불필요한 catch 후 로그만 지양)
- [ ] **테스트**: kotest BDD 스타일, Mock 대신 실제 객체 사용
- [ ] **파일 구조**: 클래스당 1개 파일, 테스트는 `src/test/kotlin`
- [ ] **문서화**: 한글로 작성 (표준 용어만 영어)
- [ ] **컴파일 확인**: IDE 컴파일 에러만 확인 (별도 gradle 명령 X)

---

### 추가 학습 자료

- **README.md**: 프로젝트 개요 및 주요 예시 코드
- **CLAUDE.md**: 코딩 표준 및 가이드라인
- **각 패키지의 Support.kt 파일**: 확장 함수 패턴 학습
- **test 디렉토리**: 실제 사용 예시 코드

---

**이 Skill은 kx_kotlin_support 라이브러리를 사용한 개발을 지원하기 위해 작성되었습니다.**
