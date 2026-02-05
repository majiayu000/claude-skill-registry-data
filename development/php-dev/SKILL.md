---
name: php-dev
description: |
  PHP開発支援（Slim/PDO/Composer）。
  PSR-12、PHPStan、PDOでセキュアPHP開発をガイド。
allowed-tools: Read, Grep, Glob, Bash
---

# PHP開発固有設定

このファイルはPHP開発に特化した設定を定義します。

## 公式ドキュメントリファレンス

最新の安定版バージョンは以下の公式ドキュメントを参照してください：

| 技術 | 公式ドキュメント | 用途 |
|-----|----------------|------|
| PHP | [PHP Downloads](https://www.php.net/downloads) | バージョン確認・ダウンロード |
| PHP Supported Versions | [PHP Supported Versions](https://www.php.net/supported-versions.php) | サポート状況確認 |
| Slim Framework | [Slim Framework](https://www.slimframework.com/) | 公式サイト |
| Slim (Packagist) | [slim/slim](https://packagist.org/packages/slim/slim) | 最新版・リリース履歴 |
| PHPUnit | [phpunit/phpunit](https://packagist.org/packages/phpunit/phpunit) | 最新版・リリース履歴 |
| PHPStan | [phpstan/phpstan](https://packagist.org/packages/phpstan/phpstan) | 最新版・リリース履歴 |
| Monolog | [monolog/monolog](https://packagist.org/packages/monolog/monolog) | 最新版・リリース履歴 |

## PHP開発固有のルール

### バージョン要件

最新の安定版バージョンは上記の公式ドキュメントリファレンスで確認してください。

- PHP: 最新の安定版を使用（[公式サイト](https://www.php.net/downloads)で確認）
  - 参考: PHP 8.3以降を推奨（2025年12月時点）
- strict_types宣言を必須とする
- 型ヒントと戻り値の型を使用
- null合体演算子を活用

### コーディング標準
- PSR-12コーディング標準に準拠する
- 意味のある変数名を使用する
- 関数は単一責任原則に従う
- 適切なエラーハンドリングを実装する

### フレームワーク・ツール
- Slim Framework 4.x（軽量API開発）
- Symfony 6.x（フルフレームワークが必要な場合）
- 素のPHP + Composerパッケージ
- PDOでデータベース抽象化（MySQL/Oracle対応）
- Monologでロギング実装
- PHPUnit + Phakeでテスト

### プロジェクト構成
```
src/
├── Controllers/      # コントローラー
├── Models/          # データモデル
├── Services/        # ビジネスロジック
├── Helpers/         # ヘルパー関数
└── Config/          # 設定
public/              # 公開ディレクトリ
├── index.php        # エントリーポイント
├── css/
├── js/
└── images/
vendor/              # Composerパッケージ
tests/               # テストコード
composer.json        # 依存関係定義
phpunit.xml          # PHPUnit設定
```

### composer.json例
```json
{
    "name": "company/project",
    "description": "PHP Application",
    "type": "project",
    "require": {
        "php": "^8.3",
        "monolog/monolog": "^3.0",
        "slim/slim": "^4.0",
        "slim/psr7": "^1.0",
        "ext-pdo": "*",
        "ext-pdo_mysql": "*",
        "ext-pdo_oci": "*"
    },
    "require-dev": {
        "phpunit/phpunit": "^11.0",
        "phake/phake": "^4.0",
        "phpstan/phpstan": "^2.0",
        "squizlabs/php_codesniffer": "^3.0",
        "friendsofphp/php-cs-fixer": "^3.0"
    },
    "comment": "最新版は公式ドキュメントリファレンスのPackagistリンクで確認してください（参考値: 2025年12月時点）",
    "autoload": {
        "psr-4": {
            "App\\": "src/"
        }
    },
    "autoload-dev": {
        "psr-4": {
            "Tests\\": "tests/"
        }
    }
}
```

### データベース対応
- MySQL 8.0
- Oracle Database 19c/21c
- プリペアドステートメント必須
- PDOベースの抽象化層

#### データベース接続例
```php
// config/database.php
return [
    'mysql' => [
        'dsn' => 'mysql:host=localhost;dbname=app;charset=utf8mb4',
        'username' => 'root',
        'password' => 'password',
        'options' => [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES => false,
        ]
    ],
    'oracle' => [
        'dsn' => 'oci:dbname=//localhost:1521/ORCL;charset=AL32UTF8',
        'username' => 'app_user',
        'password' => 'password',
        'options' => [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        ]
    ]
];
```

### ロギング（Monolog）
```php
use Monolog\Logger;
use Monolog\Handler\RotatingFileHandler;
use Monolog\Formatter\LineFormatter;

class LoggerFactory
{
    public static function create(string $name = 'app'): Logger
    {
        $logger = new Logger($name);

        // 日別ローテーション
        $handler = new RotatingFileHandler(
            __DIR__ . '/logs/app.log',
            30,  // 30日間保持
            Logger::INFO
        );

        $formatter = new LineFormatter(
            "[%datetime%] %channel%.%level_name%: %message% %context%\n",
            'Y-m-d H:i:s'
        );
        $handler->setFormatter($formatter);
        $logger->pushHandler($handler);

        return $logger;
    }
}
```

### セキュリティ実装

グローバルセキュリティポリシーを参照してください。

#### PHP追加セキュリティ設定
- すべての入力を検証・フィルタリング
- プリペアドステートメント使用
- XSS対策の実装
- CSRFトークンの実装
- 適切なパスワードハッシュを使用

```php
// セキュリティ例
// 入力検証
$email = filter_var($_POST['email'], FILTER_VALIDATE_EMAIL);

// CSRFトークン生成
$_SESSION['csrf_token'] = bin2hex(random_bytes(32));

// パスワードハッシュ化
$hashedPassword = password_hash($password, PASSWORD_DEFAULT);
```

### テスト要件
- PHPUnit + Phake
- カバレッジ95%以上
- 統合テストの実装
- テスト用DBはSQLite（:memory:）を使用

```php
use PHPUnit\Framework\TestCase;
use Phake;

class UserServiceTest extends TestCase
{
    private $userRepository;
    private $logger;
    private $userService;

    protected function setUp(): void
    {
        $this->userRepository = Phake::mock(UserRepository::class);
        $this->logger = Phake::mock(\Monolog\Logger::class);

        $this->userService = new UserService(
            $this->userRepository,
            $this->logger
        );
    }

    public function testCreateUser(): void
    {
        // テスト実装
        Phake::when($this->userRepository)->create($userData)
            ->thenReturn(['id' => 1] + $userData);

        $user = $this->userService->create($userData);

        Phake::verify($this->userRepository)->create($userData);
        Phake::verify($this->logger)->info('User created', Phake::anyParameters());
    }
}
```

### パフォーマンス
- OPcache有効化
- ファイルベースキャッシュ実装
- 大量データ処理時のメモリ管理
- N+1問題の回避

### よく使うコマンド
```bash
# Composer
composer install
composer require phake/phake --dev
composer require monolog/monolog

# テスト
./vendor/bin/phpunit
./vendor/bin/phpunit --coverage-html coverage
./vendor/bin/phpstan analyse

# コード整形
./vendor/bin/php-cs-fixer fix
./vendor/bin/phpcs --standard=PSR12 src/
```
