---
name: java-spring
description: |
  Java + Spring Boot開発支援。
  NullAway設定、テスト戦略、DIコンテナ設計をガイド。
allowed-tools: Read, Grep, Glob, Bash
---

# Java Spring Boot開発固有設定

このファイルはJava + Spring Boot開発に特化した設定を定義します。

## 公式ドキュメントリファレンス

最新の安定版バージョンは以下の公式ドキュメントを参照してください：

| 技術 | 公式ドキュメント | 用途 |
|-----|----------------|------|
| Java SE | [Oracle Java SE Support Roadmap](https://www.oracle.com/java/technologies/java-se-support-roadmap.html) | LTSバージョン確認 |
| Adoptium (OpenJDK) | [Temurin Releases](https://adoptium.net/temurin/releases/) | OpenJDKダウンロード |
| Spring Boot | [Spring Boot (English)](https://spring.io/projects/spring-boot#learn) | 公式ドキュメント（英語）|
| Spring Boot (日本語) | [Spring Boot (日本語)](https://spring.pleiades.io/projects/spring-boot#learn) | 公式ドキュメント（日本語）|
| Gradle | [Gradle Releases](https://gradle.org/releases/) | バージョン確認・ダウンロード |
| MapStruct | [MapStruct](https://mapstruct.org/) | 公式サイト |
| Error Prone | [Error Prone](https://errorprone.info/) | 公式サイト |
| Spotless | [Spotless GitHub](https://github.com/diffplug/spotless) | 公式リポジトリ |

## Java開発固有のルール

### バージョン要件

最新の安定版バージョンは上記の公式ドキュメントリファレンスで確認してください。

- Java: Java SE LTS版を使用（[Java SE Support Roadmap](https://www.oracle.com/java/technologies/java-se-support-roadmap.html)で確認）
  - 参考: Java 21 LTS以降を推奨（2025年12月時点）
- Spring Boot: 最新の安定版を使用（[公式サイト](https://spring.io/projects/spring-boot#learn)で確認）
  - 参考: Spring Boot 4.0.x以降を推奨（2025年12月時点）
- Gradle: 最新の安定版を使用（[Gradle Releases](https://gradle.org/releases/)で確認）
  - 参考: Gradle 8.x以降を推奨（2025年12月時点）
- Rocky Linux 9

### コーディング標準
- Google Java Style Guide準拠
- NullAwayによるNull安全性チェック
- 型/戻り値を明確にする（@Nullable/@NonNull 等のアノテーション）
### 技術スタック
- Spring MVC (REST API)
- Spring Data JPA
- Spring Security
- Spring Cloud (マイクロサービス)
- MySQL / Oracle Database
- Flyway (マイグレーション)
- NullAway (Null安全性チェック)
- Error Prone (静的解析)

### プロジェクト構成
```
src/
├── main/
│   ├── java/
│   │   └── com/company/project/
│   │       ├── config/          # 設定クラス
│   │       ├── controller/      # RESTコントローラー
│   │       ├── service/         # ビジネスロジック
│   │       ├── repository/      # データアクセス層
│   │       ├── entity/          # JPAエンティティ
│   │       ├── dto/             # データ転送オブジェクト
│   │       ├── mapper/          # DTO-Entityマッパー
│   │       ├── exception/       # カスタム例外
│   │       ├── util/            # ユーティリティ
│   │       └── Application.java # メインクラス
│   └── resources/
│       ├── application.yml      # アプリケーション設定
│       ├── application-dev.yml  # 開発環境設定
│       └── db/migration/        # Flywayマイグレーション
└── test/
    └── java/                    # テストコード
build.gradle                     # Gradleビルド設定
settings.gradle                  # Gradle設定
gradle.properties               # Gradleプロパティ
```

### build.gradle設定例
```gradle
// 最新の安定版バージョンは公式ドキュメントリファレンスで確認してください
plugins {
    id 'java'
    id 'org.springframework.boot' version '4.0.1' // https://spring.io/projects/spring-boot#learn
    id 'io.spring.dependency-management' version '1.1.4'
    id 'com.diffplug.spotless' version '6.23.3' // https://github.com/diffplug/spotless
    id 'net.ltgt.errorprone' version '3.1.0' // https://errorprone.info/
}

dependencies {
    // Spring Boot
    implementation 'org.springframework.boot:spring-boot-starter-web'
    implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
    implementation 'org.springframework.boot:spring-boot-starter-security'
    implementation 'org.springframework.boot:spring-boot-starter-validation'
    implementation 'org.springframework.boot:spring-boot-starter-actuator'

    // Database
    runtimeOnly 'org.postgresql:postgresql'
    implementation 'org.flywaydb:flyway-core'

    // Lombok & MapStruct
    compileOnly 'org.projectlombok:lombok'
    annotationProcessor 'org.projectlombok:lombok'
    // 最新版は https://mapstruct.org/ で確認
    implementation 'org.mapstruct:mapstruct:1.5.5.Final' // 参考値（2025年12月時点）
    annotationProcessor 'org.mapstruct:mapstruct-processor:1.5.5.Final'

    // Null安全性チェック
    // 最新版は https://errorprone.info/ で確認
    errorprone 'com.google.errorprone:error_prone_core:2.44.0' // 参考値（2025年12月時点）
    errorprone 'com.uber.nullaway:nullaway:0.12.15' // 参考値（2025年12月時点）

    // Test
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
    testImplementation 'org.springframework.security:spring-security-test'
}

// NullAway設定
import net.ltgt.gradle.errorprone.CheckSeverity

tasks.withType(JavaCompile).configureEach {
    options.errorprone {
        check("NullAway", CheckSeverity.ERROR)
        option("NullAway:AnnotatedPackages", "com.company.project")
        option("NullAway:TreatGeneratedAsUnannotated", "true")
        option("NullAway:ExcludedFieldAnnotations", "org.springframework.beans.factory.annotation.Autowired")
    }
}
```

### Null安全性
- `@Nullable` と `@NonNull` アノテーションを活用
- NullAwayによる静的解析でNullPointerExceptionを防止
- Optionalの適切な使用
- コンストラクタインジェクションで非nullを保証

```java
import org.springframework.lang.NonNull;
import org.springframework.lang.Nullable;

@Service
public class UserService {
    private final UserRepository repository;

    public UserService(UserRepository repository) {
        this.repository = Objects.requireNonNull(repository);
    }

    @NonNull
    public Optional<UserDto> findById(@NonNull Long id) {
        return repository.findById(id)
            .map(this::toDto);
    }

    @Nullable
    public String getNickname(@NonNull Long userId) {
        return repository.findNicknameById(userId);
    }
}
```

### Docker設定
```dockerfile
# マルチステージビルド for Rocky Linux
FROM gradle:8-jdk17 AS builder
WORKDIR /app
COPY build.gradle settings.gradle ./
COPY gradle ./gradle
COPY src ./src
RUN gradle bootJar --no-daemon

# 実行環境 (Rocky Linux)
FROM rockylinux:9-minimal
RUN microdnf install -y java-17-openjdk-headless && \
    microdnf clean all

WORKDIR /app
COPY --from=builder /app/build/libs/*.jar app.jar

# セキュリティ: 非rootユーザーで実行
RUN groupadd -r spring && useradd -r -g spring spring
USER spring:spring

EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

### セキュリティ実装

グローバルセキュリティポリシーを参照してください。

#### Spring Security追加設定
- JWT認証の実装
- メソッドレベルセキュリティ
- CORS設定の適切な管理
- CSRFトークンの実装

### テスト要件
- JUnit 5 + Mockito
- 単体テストカバレッジ95%以上
- 統合テストの実装
- `@SpringBootTest`で統合テスト
- `@MockBean`でSpringコンテキストテスト

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserService userService;

    @Test
    void testFindById() {
        when(userRepository.findById(1L))
            .thenReturn(Optional.of(new User()));

        Optional<UserDto> result = userService.findById(1L);

        assertTrue(result.isPresent());
    }
}
```

### パフォーマンス最適化
- JPA N+1問題の回避 (`@EntityGraph`, `JOIN FETCH`)
- 適切なインデックス設計
- キャッシュ戦略 (`@Cacheable`, `@CacheEvict`)
- 非同期処理 (`@Async`, `CompletableFuture`)
- コネクションプーリング (HikariCP)

### よく使うコマンド
```bash
# アプリケーション起動
./gradlew bootRun

# テスト実行
./gradlew test
./gradlew test --tests '*IntegrationTest'

# JAR作成
./gradlew clean bootJar

# 依存関係更新チェック
./gradlew dependencyUpdates

# コード整形
./gradlew spotlessApply

# 並列ビルド
./gradlew build --parallel
```
